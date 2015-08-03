import re
import json
from .helpers import BigVMachineResource

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
        return self.account.cmd("DELETE", self.url())

    def purge(self):
        return self.account.cmd("DELETE", self.url(), params=dict({"purge": True}))

    def __str__(self):
        return "<BigVDisc label=%s size=%sGB storage_grade=%s>" % (self.label(),self.size()/1024, self.storage_grade())

    def info(self):
        return dict(label=self.label(),
                    grade=self.storage_grade(),
                    size=self.size())

    @classmethod

    #
    # This takes a disc string (as supplied to bigv vm new) and returns a dict.
    #
    def parse(cls, s):
        discs = []
        label = "a"
        for d in re.split(",",str(s)):
            disc = dict({"label": "vd"+label, "storage_grade": "sata", "size": 0})

            m = re.match(r"^([a-z][^:]*)?:?([0-9.]+)(M|G|T)?B?$", d, re.I)

            # Set the grade.
            if m.group(1) is not None:
                disc["storage_grade"] = str(m.group(1))

            # Workout the size            
            try:
                sz = int(m.group(2))
            except ValueError:
                sz = float(m.group(2))

            if m.group(3) is not None:
                sz = {'M': 1, "G": 1024, "T": 1024**2}[m.group(3)] * sz
            else:
                sz = 1024 * sz

            disc["size"] = int(sz)

            discs.append(disc)

            # Increment label
            label = chr(ord(label)+1)
            
        return discs


