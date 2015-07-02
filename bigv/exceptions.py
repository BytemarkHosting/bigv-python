class BigVProblem(Exception):
    def __init__(self,msg, http_status=None, http_method=None, url=None):
        self.msg = msg
        self.http_status = http_status
        self.http_method = http_method
        self.url = url

    @classmethod
    def check_response(cls,resp):
        if resp.status_code >= 400:
            raise BigVProblem(resp.reason,resp.status_code,resp.request.method,resp.url)

    def http_error(self):
        if self.http_status != None:
            s = str(self.msg) + " (HTTP "+str(self.http_method)+" "+str(self.url)+" returned "+str(self.http_status)+")"
        else:
            s = "None"

        return s 

    def __str__(self):
        return repr(self.msg)

class BigVGroupMissing(BigVProblem): pass

class BigVCollision(BigVProblem): pass

class BigVAuthProblem(BigVProblem): pass

