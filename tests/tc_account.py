import unittest
import requests
import sys
sys.path.append("..")

import bigv
import httpretty


class BigVAccountTests(unittest.TestCase):
    def setUp(self):
        httpretty.enable()
    
    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def testRefresh(self):

        # Create a mock result for the requests.get call
        httpretty.register_uri(httpretty.GET, "https://uk0.bigv.io/accounts/quux",
                               body='{"id":123,"name":"quux","suspended":false,"groups":[{"type":"application/vnd.bigv.group","account_id":1,"id":123,"name":"default","virtual_machines":[{"type":"application/vnd.bigv.virtual-machine","autoreboot_on":false,"cdrom_url":null,"cores":1,"group_id":123,"id":1234,"management_address":"213.123.123.123","memory":1024,"name":"myhostname","power_on":false,"keymap":null,"deleted":false,"hostname":"myhostname.default.myaccountname.uk0.bigv.io","head":null,"hardware_profile":"virtio2013","hardware_profile_locked":false,"discs":[{"type":"application/vnd.bigv.disc","id":1234,"label":"vda","size":25600,"virtual_machine_id":1234,"storage_pool":"tail1-sata1","storage_grade":"sata"}],"network_interfaces":[{"type":"application/vnd.bigv.network-interface","id":1234,"label":null,"ips":["213.123.123.123","2001:ffff:ff:ffff:ffff:ff:fe00:fff"],"vlan_num":1,"mac":"fe:ff:ff:00:ff:ff","extra_ips":{},"virtual_machine_id":1234}]}]}]}',
                               content_type="application/json", status=200)

        # Now execute my code
        account = bigv.BigVAccount(username="foo",password="bar",account="quux")
        self.assertEqual(account.url(), "/accounts/quux")
       
#        self.assertEqual(account.account_id(), 123)
#        self.assertEqual(account.suspended(), False)
        self.assertEqual(account.account, "quux")



if __name__ == '__main__':
    unittest.main()
