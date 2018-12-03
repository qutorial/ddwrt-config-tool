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

