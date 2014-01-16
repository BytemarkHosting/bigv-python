class BigVResource:
    def __init__(self, account, data):
        self.account = account
        self.data = data

    def fact(self,fact):
        return self.data[":"+fact]

class BigVMachineResource(BigVResource):
    def machine(self):
        return self

    def op(self, operation, dargs={}):
        args = []
        for k in dargs:
            v = dargs[k]
            if v == None:
                args.append("--%s" % k)
            else:
                args.append("--%s %s" % (k,v))
        cmd = [operation,
               "--vm-name %s" % self.name(),
               "--group-name %s" % self.machine().group().name()]+args
        return self.account.cmd(" ".join(cmd))


