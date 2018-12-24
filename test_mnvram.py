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

  def test_update_sshd_enable(self):

    nvram = {'sshd_enable': '0',
             'sshd_wanport': '33',
             'sshd_port': '44',
             'sshd_passwd_auth': '0',
             'sshd_authorized_keys': '',
             'sshd_forwarding': '0',
             }

    from mnvram import MozaiqRouter
    router = MozaiqRouter(nvram)
    router.updateSshd('enable')
    self.assertEqual(router.nvram['sshd_enable'], '1')
    self.assertEqual(router.nvram['sshd_wanport'], '22')
    self.assertEqual(router.nvram['sshd_port'], '22')
    self.assertEqual(router.nvram['sshd_passwd_auth'], '1')
    self.assertEqual(router.nvram['sshd_authorized_keys'], '')
    self.assertEqual(router.nvram['sshd_forwarding'], '0')

  def test_update_sshd_disable(self):
    nvram = {'sshd_enable': '1',
             'sshd_wanport': '22',
             'sshd_port': '22',
             'sshd_passwd_auth': '1',
             'sshd_authorized_keys': '',
             'sshd_forwarding': '0',
             }

    from mnvram import MozaiqRouter
    router = MozaiqRouter(nvram)
    router.updateSshd('disable')
    self.assertEqual(router.nvram['sshd_enable'], '0')

