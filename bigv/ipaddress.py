import yaml

class BigVIPAddress:
    def __init__(self, account, ip):
        self.account = account
        self.ip = ip
        self._rdns = None

    def rdns(self, newval=None):
        if self._rdns != None:
            return self._rdns
        if newval:
            self.account.cmd(["ip rdns",
                        "--address %s" % self.ip,
                        "--rdns %s" % newval])
        else:
            (rc,so,se) = self.account.cmd(["ip show",
                                        "--address %s" % self.ip])
            self._rdns = yaml.load(so)[":rdns"] 
            return self._rdns

