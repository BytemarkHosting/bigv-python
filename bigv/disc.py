from helpers import BigVMachineResource

class BigVDisc(BigVMachineResource):
    def machine(self):
        return self.account.machine(machine_id=self.fact("virtual_machine_id"))

    def label(self):
        return self.fact("label")

    def storage_grade(self):
        return self.fact("storage_grade")

    def size(self):
        return self.fact("size")

    def delete(self):
        return self.op("disc delete",dict(disc_label=self.label(),disc_label_confirmation=self.label()))

    def purge(self):
        return self.op("disc purge",dict(disc_label=self.label(),disc_label_confirmation=self.label()))

    def __str__(self):
        return "<BigVDisc label=%s size=%sGB storage_grade=%s>" % (self.label(),self.size()/1024, self.storage_grade())

    def info(self):
        return dict(label=self.label(),
                    grade=self.storage_grade(),
                    size=self.size())

