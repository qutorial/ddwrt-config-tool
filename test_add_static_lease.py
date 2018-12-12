
import unittest

class TestAddStaticLease(unittest.TestCase):

  def test_add_static_lease(self):
    nvram = {'static_leases':''}
    from mnvram import addStaticLease
    addStaticLease(nvram,"lease_config.json", 33)

    shouldBe = "00:28:F8:43:F6:11=host1=192.168.33.44=300 00:28:F8:43:F6:11=host2=192.168.133.66=500 00:28:F8:43:F6:11=host3=192.168.233.88=500 "

    self.assertEqual(nvram['static_leases'], shouldBe)

