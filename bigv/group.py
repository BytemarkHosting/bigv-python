from helpers import BigVResource
from machine import BigVMachine
from disc import BigVDisc
from exceptions import BigVCollision

class BigVGroup(BigVResource):
    def url(self):
        return self.account.url() + "/groups/" + str(self.group_id())

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
        for m in self.account.cmd("GET", self.url() + "/virtual_machines"):
            yield BigVMachine(self.account, m)

    def create_machine(self,name,
                       distribution='wheezy',
                       cores=1,
                       memory=1,
                       discs="sata:25GB",
                       root_password=None,
                       ssh_public_key=None,
                       zone_name=None):

        if self.machine(name=name) != None:
            raise BigVCollision("VM Already exists %s" % mgrp)

        if not isinstance(cores, int):
            cores = int(cores)

        if not isinstance(memory, int) or not isinstance(memory, float):
            try:
                memory = int(memory)
            except ValueError:
                memory = float(memory)

        memory = int(memory * 1024)

        discs = BigVDisc.parse(discs)

        data = dict({
            "virtual_machine": dict({
                "name": name,
                "cores": cores,
                "memory": memory,
                "power_on": True,
            }),
            "discs": discs,
            "reimage": dict({
                "distribution": distribution,
            })
        })
        
        if zone_name != None:
            data["virtual_machine"]["zone_name"] = zone_name

        if root_password != None:
            data["reimage"]["root_password"] = root_password
        
        if ssh_public_key != None:
            data["reimage"]["ssh_public_key"] = ssh_public_key

        self.account.cmd("POST", self.url()+"/vm_create", data=data)

        # We have to invalidate the vm show cache here or we'll get old data back
        self.account.invalidate_cache(self.url()+"/virtual_machines")

        return self.machine(name=name)

    def __str__(self):
        return "<BigVGroup name=%s>" % (self.name())

