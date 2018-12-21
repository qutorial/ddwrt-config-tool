import unittest

class TestMnvram(unittest.TestCase):

  def test_rename(self):
    nvram = {}
    from mnvram import MozaiqRouter
    router = MozaiqRouter(nvram)
    router.renameRouter("newname")
    nvram = router.nvram
    self.assertTrue(nvram['wan_hostname'] == 'mozaiqnewname')
    self.assertTrue(nvram['router_name'] == 'mozaiqnewname')
    for k, v in nvram.items():
      if k.endswith("ssid"):
        self.assertTrue(v.startswith('mozaiq'))


