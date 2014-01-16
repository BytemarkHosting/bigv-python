from helpers import BigVMachineResource
from nic import BigVNic
from disc import BigVDisc

class BigVMachine(BigVMachineResource):
    def group(self):
        return self.account.group(group_id=self.fact("group_id"))

    def deleted(self):
        return self.fact("deleted")

    def cores(self):
        return self.fact("cores")

    def memory(self):
        return self.fact("memory")

    def state(self):
        if self.fact("power_on"):
            return "on"
        else:
            return "off"

    def hostname(self):
        return self.fact("hostname")

    def autoreboot_status(self):
        return self.fact("autoreboot_on")

    def hardware_profile(self):
        return self.fact("hardware_profile")

    def machine_id(self):
        return self.fact("id")

    def name(self):
        return self.fact("name")

    def discs(self):
        for d in self.fact("discs"):
            yield BigVDisc(self.account, d)

    def disc(self,label):
        for d in self.discs():
            if d.label() == label:
                return d

    def nics(self):
        for n in self.fact("network_interfaces"):
            yield BigVNic(self.account, n)

    def nic(self, index):
        return self.nics[index]

    def __str__(self):
        return "<BigVMachine name=%s discs=%d nics=%s>" % (self.name(), len(list(self.discs())), len(list(self.nics())))

    def ips(self):
        ips = []
        return [item for sublist in [list(nic.ips()) for nic in self.nics()] for item in sublist]

    def restart(self):
        return self.op("vm restart")
    
    def shutdown(self):
        return self.op("vm shutdown")

    def start(self):
        return self.op("vm start")

    def stop(self):
        return self.op("vm stop")

    def undelete(self):
        return self.op("vm undelete")

    def delete(self):
        return self.op("vm delete")

    def info(self):
        return dict(name=self.name(),
                    hostname=self.hostname(),
                    cores=self.cores(),
                    memory=self.memory(),
                    state=self.state(),
                    discs=[d.info() for d in self.discs()],
                    nics=[n.info() for n in self.nics()])

    @classmethod
    def mgrp(cls, name, group):
        return "%s.%s" % (name,group)

    @classmethod
    def mgrpacc(cls, name, group, account):
        return "%s.%s.%s" % (name, group, account)
