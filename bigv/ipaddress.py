import yaml

class BigVIPAddress:
    def __init__(self, account, ip):
        self.account = account
        self.ip = ip
        self._rdns = None

    def url(self):
        return "/ips/" + str(self.group_ip)

    def rdns(self, newval=None):
        if newval:
            x = self.account.cmd("PUT", self.url, data=dict({"rdns": newval}))
        else:
            x = self.account.cmd("GET", self.url())

        return x["rdns"]

