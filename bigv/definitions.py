import requests
import json
import re
import itertools

from exceptions import BigVProblem

# Usage:
# >>> bigv.BigVDefinitions(location='https://uk0.bigv.io').fact('distributions')
# [u'centos5', u'centos6', u'centos7', u'jessie', u'precise', u'symbiosis', u'trusty', u'utopic', u'vivid', u'wheezy', u'winstd2012', u'winweb2k8r2']
class BigVDefinitions:
    def __init__(self,location="https://uk0.bigv.io"):
        self._def_cache = None
        self.location = location
        
    def definitions_raw(self):
        if self._def_cache != None:
            return self._def_cache
        else:
            r = requests.get(self.location+"/definitions",headers={'Accept':'application/json'})
            BigVProblem.check_response(r) # raises exception if it's >= 400
            if 'content-type' in r.headers and re.search('^application/(vnd\.bigv\..*\+)?json$', r.headers['content-type']):
               self._def_cache = json.loads(r.text)
               return self._def_cache
    
    def fact(self,key):
        lists = filter(lambda i: i != None, map(lambda i: i['id'] == key and i['data'] or None, self.definitions_raw()))
        #http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
        return [item for sublist in list(itertools.chain(lists)) for item in sublist]