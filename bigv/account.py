import time
import subprocess
import yaml

from group import BigVGroup
from exceptions import BigVProblem,BigVCollision,BigVGroupMissing

from machine import BigVMachine

class BigVAccount:
    def __init__(self,username,password,account,yubikey=None,location="https://uk0.bigv.io"):
        self.username = username
        self.password = password
        self.account = account
        self.location = location
        self.yubikey = yubikey
        self._account_cache = None

    def cmd(self, command,bigv="/usr/bin/bigv"):
        if command.__class__ == list:
            command = " ".join(command)
        command_args = [bigv]+command.split(" ")
        command_args += [ "--username", self.username,
                    "--password",  self.password,
                    "--account", self.account,
                    "--location", self.location,
                    "--batch",
                    "--yaml"]
        if self.yubikey:
            command_args.append("--yubikey")
            command_args.append(self.yubikey)
        else:
            command_args.append("--no-yubikey")
        proc = subprocess.Popen(command_args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        proc.wait()
        if proc.returncode != 0:
            raise BigVProblem(proc.stderr.read())
        return (proc.returncode, proc.stdout, proc.stderr)

    def _account_show(self):
        if self._account_cache != None:
            return self._account_cache
        else:
            (rc,so,se) = self.cmd("account show")
            if rc == 0:
                ydata = yaml.load(so.read())
                self._account_cache = ydata
                return ydata
            else:
                raise BigVProblem(msg=se.read())

    def groups(self):
        for g in self._account_show()[":groups"]:
            yield BigVGroup(self, g)

    def group(self, name=None, group_id=None):
        if(name == None and group_id == None):
            return None
        for g in self.groups():
            if name != None and g.name() == name:
                return g
            if group_id != None and g.group_id() == group_id:
                return g

    def create_machine(self,name,group,
                       distribution='wheezy',
                       group_create=True,
                       cores=1,
                       memory=1,
                       discs="sata:25GB",
                       rdns=None,
                       root_password=None,
                       wait=True):
        tngrp = BigVMachine.mgrp(name, group)
        if self.machine(namegroup=tngrp) != None:
            raise BigVCollision("VM Already exists %s" % mgrp)
        if self.group(name=group) == None:
            raise BigVGroupMissing(group=group,msg="No such group: %s" % group)
        cmd_params = ["vm new",
                      "--vm-name %s" % name,
                        "--vm-distribution %s" % distribution,
                        "--vm-cores %s" % cores,
                        "--vm-memory %s" % memory,
                        "--vm-discs %s" % discs,
                        "--group-name %s" % group]
        if rdns != None:
            cmd_params.append("--rdns %s" % rdns)
        if root_password != None:
            cmd_params.append("--vm-root-password %s" % root_password)
        if wait == False:
            cmd_params.append("--no-wait")
        self.cmd(cmd_params)
        # We have to invalidate the vm show cache here or we'll get old data back
        self.invalidate_cache()
        return self.machine(namegroup=tngrp)

    def invalidate_cache(self):
        self._account_cache = None

    def machines(self, group=None):
        for g in self.groups():
            for m in g.machines():
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
