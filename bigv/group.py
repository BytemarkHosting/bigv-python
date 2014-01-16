from helpers import BigVResource
from machine import BigVMachine

class BigVGroup(BigVResource):
    def group_id(self):
        return self.fact("id")

    def name(self):
        return self.fact("name")

    def machine(self, name=None, machine_id=None):
        if(name == None and machine_id == None):
            return None
        for m in self.machines():
            if name != None and m.name() == name:
                return m
            if machine_id != None and m.machine_id() == machine_id:
                return m

    def machines(self):
        for m in self.fact("virtual_machines"):
            yield BigVMachine(self.account, m)

    def __str__(self):
        return "<BigVGroup name=%s machines=%d>" % (self.name(), len(self.machines()))


