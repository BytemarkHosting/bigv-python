import time
import subprocess
import requests
import json
import re

from requests.auth import HTTPBasicAuth

from group import BigVGroup
from exceptions import BigVProblem,BigVCollision,BigVGroupMissing
from machine import BigVMachine

class BigVAccount:
    def __init__(self,username,password,account,yubikey=None,location="https://uk0.bigv.io"):
        self.username = username
        self.password = password
        self.location = location
        self.yubikey = yubikey
        self.account = account
        self._cmd_cache = dict()
        self._session_token = None
        self.data = None

    def url(self):
        return "/accounts/"+self.account
        
    def session_token(self):
        if self._session_token != None:
            return self._session_token
        else:
            creds = dict(username=self.username,password=self.password)
            if self.yubikey:
                creds["yubikey"] = self.yubikey
            st = requests.post("https://auth.bytemark.co.uk/session", data=creds)
            BigVProblem.check_response(st)
            self._session_token = st.text
            return self._session_token

    def cmd(self, method, url, params=None, data=None):
        if method == "GET" and url in self._cmd_cache:
            return self._cmd_cache[url]

        if method == "PUT" or method == "POST":
            headers = {"Content-type": "application/json" }
        else:
            headers = dict()

        # auth = HTTPBasicAuth(self.username, self.password)
        headers['Authorization'] = 'Bearer %s' % self.session_token()

        if data and not isinstance(data, str):
            data = json.dumps(data)

        r = requests.request(method, self.location+url, params=params, headers=headers, data=data)
        BigVProblem.check_response(r)
        if 'content-type' in r.headers and re.search('^application/(vnd\.bigv\..*\+)?json$', r.headers['content-type']):
           result = json.loads(r.text)
        else:
           result = r.text

        if method == "GET":
            self._cmd_cache[url] = result
        else:
            self.invalidate_cache(url)

        return (result)

    def groups(self):
        for g in self.cmd("GET", self.url() + "/groups"):
            yield BigVGroup(self, g)

    def group(self, name=None, group_id=None):
        if(name == None and group_id == None):
            return None
        for g in self.groups():
            if name != None and g.name() == name:
                return g
            if group_id != None and g.group_id() == group_id:
                return g

    def create_group(self, name):

        if self.group(name=name) != None:
            raise BigVCollision("Group already exists %s" % name)

        if self.group(group_id=name) != None:
            raise BigVCollision("Group ID already exists %s" % name)

        self.cmd("POST", self.url()+"/groups", data=dict({"name": name}))

        return self.group(name=name)

    def invalidate_cache(self, url=None):
        if url and url in self._cmd_cache:
            del self._cmd_cache[url]
        else:
            self._cmd_cache = dict()

    def machines(self, group=None, include_deleted=True):
        for g in self.groups():
            for m in g.machines(include_deleted):
                yield m

    def machine(self, namegroup=None, machine_id=None):
        if(namegroup == None and machine_id == None):
            return None
        for m in self.machines():
            mng = BigVMachine.mgrp(m.name(), m.group().name())
            if namegroup != None and mng == namegroup:
                return m
            if machine_id != None and m.machine_id() == machine_id:
                return m
