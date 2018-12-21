
import unittest
from router import Router
from ddwrtnvram import readNvram
from nvramlogging import getTestLogger
from lease import Lease


class TestLeasesRouter(unittest.TestCase):

  def test_leases_router(self):
    logger = getTestLogger()
    nvram = readNvram("./test/static.lease.23.bin", logger)
    router = Router(nvram)
    s = router.leasesStr()
    shouldBe = 'B8:27:EB:5E:9C:C0=raspberrypi=192.168.23.41=3600 B8:27:EB:5E:9C:C1=raspberrypi2=192.168.23.42=3601 '
    self.assertEqual(s, shouldBe)
    self.assertEqual(s, router.nvram['static_leases'])
    self.assertEqual(router.nvram['static_leasenum'], '2')

    leaseDict = {"hostname": "Host1",
        "mac_address": "aa:bb:f8:43:f6:dd",
        "ip_address": "192.168.235.88",
        "lease_time": "500"}

    lease = Lease(leaseDict)
    router.addLease(lease)
    self.assertEqual(len(router.leases), 3)
    self.assertEqual(router.nvram['static_leasenum'],  '3')
    s = router.leasesStr()
    shouldBe = "AA:BB:F8:43:F6:DD=host1=192.168.235.88=500 B8:27:EB:5E:9C:C0=raspberrypi=192.168.23.41=3600 B8:27:EB:5E:9C:C1=raspberrypi2=192.168.23.42=3601 "
    self.assertEqual(s, shouldBe)
