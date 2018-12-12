import unittest
from nvramlogging import getTestLogger
from lease import Lease
from read_leases import readLeases


class TestReadLeases(unittest.TestCase):

  def test_read_leases(self):
    leaseObjectArray = readLeases("lease_config.json")

    leaseDicts = {"user1": {"hostname": "host1",
                            "mac_address": "00:28:f8:43:f6:11",
                            "ip_address": "192.168.35.44",
                            "lease_time": "300"},
                  "user3": {"hostname": "host3",
                            "mac_address": "00:28:f8:43:f6:11",
                            "ip_address": "192.168.235.88",
                            "lease_time": "500"},
                  "user2": {"hostname": "host2",
                            "mac_address": "00:28:f8:43:f6:11",
                            "ip_address": "192.168.135.66",
                            "lease_time": "500"}
                  }

    shouldBe = []
    for user in sorted(leaseDicts):
      leaseDict= leaseDicts[user]
      shouldBe.append(Lease(leaseDict))

    for leaseObjA,leaseObjB in zip(leaseObjectArray, shouldBe):
      self.assertEqual(leaseObjA.mac_address, leaseObjB.mac_address)
      self.assertEqual(leaseObjA.hostname, leaseObjB.hostname)
      self.assertEqual(leaseObjA.ip_address, leaseObjB.ip_address)
      self.assertEqual(leaseObjA.lease_time, leaseObjB.lease_time)
