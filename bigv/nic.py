from .helpers import BigVResource
from .ipaddress import BigVIPAddress

class BigVNic(BigVResource):
    def ips(self):
        for i in self.fact("ips"):
            yield BigVIPAddress(self.account, i)

    def mac(self):
        return self.fact("mac")

    def machine(self):
        return self.bigv.machine(machine_id=self.fact("virtual_machine_id"))

    def info(self):
        return dict(ips=[i.ip for i in self.ips()],
                    mac=self.mac())


