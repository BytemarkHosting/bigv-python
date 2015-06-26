from helpers import BigVMachineResource
from nic import BigVNic
from disc import BigVDisc

class BigVMachine(BigVMachineResource):

    def url(self):
        return self.account.url() + "/groups/" + str(self.group_id()) + "/virtual_machines/" + str(self.vm_id())

    def vm_id(self):
        return self.fact("id")
    
    def group_id(self):
        return self.fact("group_id")

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

    def machine(self):
        return self

    def name(self):
        return self.fact("name")
        
    def zone_name(self):
        return self.fact("zone_name")

    def discs(self):
        for d in self.account.cmd("GET", self.url() + "/discs"):
            yield BigVDisc(self.account, d)

    def disc(self,label):
        for d in self.discs():
            if d.label() == label:
                return d

    def create_disc(self, label, size, grade="sata"):
        #
        # Tidy up our size argument
        #
        if not isinstance(size, int) or not isinstance(size, float):
            try:
                size = int(size)
            except ValueError:
                size = float(size)

        #
        # Now make it an integer and turn it into MiB.
        #
        size = int(size * 1024)

        if self.disc(label):
            raise BigVCollision("Disk %s already exists!" % label)

        self.account.cmd("POST", self.url() + "/discs", 
            data= dict({"label": label, "storage_grade": grade, "size": size}))

        self.account.invalidate_cache(self.url())

        return self.disc(label)

    def nics(self):
        for n in self.account.cmd("GET", self.url() + "/nics"):
            yield BigVNic(self.account, n)

    def nic(self, index):
        return self.nics[index]

    def __str__(self):
        return "<BigVMachine name=%s>" % (self.name())

    def ips(self):
        ips = []
        return [item for sublist in [list(nic.ips()) for nic in self.nics()] for item in sublist]
    
    def signal(self, signal, keys=None):
        data = dict({"signal": signal})

        if signal == "sendkey":
            data["data"] = keys
            
        return self.account.cmd("POST", self.url()+"/signal", data=data)

    def reset(self):
        return self.signal("reset")

    def shutdown(self):
        return self.signal("powerdown")
    
    def cad(self):
        return self.signal("sendkey",keys="ctrl-alt-del")

    def start(self):
        return self.account.cmd("PUT", self.url(), data=dict({"power_on": True}))

    def stop(self):
        return self.account.cmd("PUT", self.url(), data=dict({"power_on": False, "autoreboot_on": False}))
    
    def restart(self):
        if self.power_on():
           self.account.cmd("PUT", self.url(), data=dict({"power_on": False}))

        return self.start()

    def undelete(self):
        return self.account.cmd("PUT", self.url(), data=dict({"deleted": False}))

    def delete(self):
        return self.account.cmd("DELETE", self.url())

    def info(self):
        return dict(name=self.name(),
                    hostname=self.hostname(),
                    cores=self.cores(),
                    memory=self.memory(),
                    state=self.state(),
                    zone_name=self.zone_name(),
                    deleted=self.deleted(),
                    hardware_profile=self.hardware_profile(),
                    discs=[d.info() for d in self.discs()],
                    nics=[n.info() for n in self.nics()])

    @classmethod
    def mgrp(cls, name, group):
        return "%s.%s" % (name,group)

    @classmethod
    def mgrpacc(cls, name, group, account):
        return "%s.%s.%s" % (name, group, account)
