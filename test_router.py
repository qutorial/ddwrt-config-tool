import unittest

from router import Router

class TestRouter(unittest.TestCase):

  def test_wan_hostname(self):
    router = Router()
    router.wan_hostname="hostname"
    self.assertTrue(router.wan_hostname == "hostname")
    self.assertTrue(router.nvram['wan_hostname'] == "hostname")

  def test_router_name(self):
    router = Router()
    router.router_name="hostname"
    self.assertTrue(router.router_name == "hostname")
    self.assertTrue(router.nvram['router_name'] == "hostname")

  def test_name(self):
    router = Router()
    router.name="hostname"
    self.assertTrue(router.name == "hostname")
    self.assertTrue(router.router_name == "hostname")
    self.assertTrue(router.nvram['router_name'] == "hostname")
    self.assertTrue(router.wan_hostname == "hostname")
    self.assertTrue(router.nvram['wan_hostname'] == "hostname")

  def test_passwd(self):
    from passlib.hash import md5_crypt
    router = Router()
    router.password = "HellYeah!"
    self.assertTrue(md5_crypt.verify("HellYeah!", router.nvram['http_passwd']))

  def test_leases(self):
    from ddwrtnvram import readNvram, writeNvram
    from nvramlogging import getTestLogger
    logger = getTestLogger()
    nvram = readNvram ('./test/static.lease.23.bin', logger)
    router = Router(nvram)
    leases = router.leases
    self.assertEqual(len(leases), 2)
    self.assertEqual(leases[0].hostname, "raspberrypi")
    self.assertEqual(leases[1].hostname, "raspberrypi2")
    from lease import Lease
    printerLease = Lease({"hostname": "printer",
      "mac_address": "aa:bb:f8:43:f6:dd",
      "ip_address": "192.168.235.88",
      "lease_time": "500"})
    router.addLease(printerLease)
    leases = router.leases
    self.assertEqual(len(leases), 3)
    self.assertEqual(router.nvram['static_leasenum'], '3')
    self.assertEqual(leases[0].hostname, "printer")
    self.assertEqual(leases[1].hostname, "raspberrypi")
    self.assertEqual(leases[2].hostname, "raspberrypi2")
    self.assertEqual(router.leasesStr(), "AA:BB:F8:43:F6:DD=printer=192.168.235.88=500 B8:27:EB:5E:9C:C0=raspberrypi=192.168.23.41=3600 B8:27:EB:5E:9C:C1=raspberrypi2=192.168.23.42=3601 ")

    # now write, read and then retest
    writeNvram('./test/test.static.leases.router.bin', router.nvram, logger)
    nvram = readNvram ('./test/test.static.leases.router.bin', logger)
    router = Router(nvram)
    leases = router.leases
    self.assertEqual(len(leases), 3)
    self.assertEqual(router.nvram['static_leasenum'], '3')
    self.assertEqual(leases[1].hostname, "raspberrypi")
    self.assertEqual(leases[2].hostname, "raspberrypi2")
    self.assertEqual(leases[0].hostname, "printer")


