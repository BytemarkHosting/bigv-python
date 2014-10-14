class BigVResource:
    def __init__(self, account, data):
        self.account = account
        self.data = data

    def fact(self,fact):
        if fact in self.data:
            return self.data[fact]
        else:
            return None

class BigVMachineResource(BigVResource):
    def machine(self):
        return self

    def op(self, operation, dargs={}):
        args = []
        for k in dargs.keys():
            key = k.replace("_","-")
            v = dargs[k]
            if v == None:
                args.append("--%s" % key)
            else:
                args.append("--%s %s" % (key,v))
        cmd = [operation,
               "--vm-name %s" % self.machine().name(),
               "--group-name %s" % self.machine().group().name()]+args
        return self.account.cmd(" ".join(cmd))


