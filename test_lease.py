import unittest

from lease import Lease

class TestLease(unittest.TestCase):

  def test_lease_tostr(self):
    leaseDict = {"hostname": "host1",
      "mac_address": "aa:bb:f8:43:f6:dd",
      "ip_address": "192.168.235.88",
      "lease_time": "500"}
    
    lease = Lease(leaseDict)
    self.assertEqual(str(lease), "AA:BB:F8:43:F6:DD=host1=192.168.235.88=500 ")

  def test_lease_empty(self):
    lease = Lease()
    self.assertEqual(str(lease), "=== ")
  
  def test_lease_from_str(self):
    lease = Lease()
    s = "aa:bb:f8:43:f6:dd=host1=192.168.235.88=500"
    lease.fromStr(s)
    self.assertEqual(str(lease), "AA:BB:F8:43:F6:DD=host1=192.168.235.88=500 ")
  
  def test_lease_valid(self):
    lease = Lease()
    s = "aa:bb:f8:43:f6:dd=host1=192.168.235.88=500"
    lease.fromStr(s)
    self.assertTrue(lease.isValid()[0])

    s = "rr:bb:f8:43:f6:dd=host1=192.168.235.88=500"
    lease.fromStr(s)
    self.assertFalse(lease.isValid()[0])

    s = "aa:bb:f8:43:f6:dd=,..#$dhost1=192.168.235.88=500"
    lease.fromStr(s)
    self.assertFalse(lease.isValid()[0])

    s = "aa:bb:f8:43:f6:dd=host1=192168.235.88=500"
    lease.fromStr(s)
    self.assertFalse(lease.isValid()[0])

    s = "aa:bb:f8:43:f6:dd=host1=192.168.235.88=-1"
    lease.fromStr(s)
    self.assertFalse(lease.isValid()[0])

    s = "aa:bb:f8:43:f6:dd=host1=192.168.235.88=2600000"
    lease.fromStr(s)
    self.assertFalse(lease.isValid()[0])

    s = "==="
    lease.fromStr(s)
    self.assertFalse(lease.isValid()[0])

    s = "AA:BB:CC:DD:EE:FF==="
    lease.fromStr(s)
    self.assertFalse(lease.isValid()[0])
