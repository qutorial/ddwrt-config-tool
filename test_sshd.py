import unittest

from router import Router


class TestSSHD(unittest.TestCase):
    def test_sshd_enable(self):

        nvram = {'sshd_enable':'0',
                 'sshd_wanport': '33',
                 'sshd_port': '44',
                 'sshd_passwd_auth': '0',
                 'sshd_authorized_keys': '',
                 'sshd_forwarding': '0',
                 }

        router = Router(nvram)
        router.changeSshdStatus(True)
        self.assertEqual(router.nvram['sshd_enable'], '1')
        self.assertEqual(router.nvram['sshd_wanport'], '22')
        self.assertEqual(router.nvram['sshd_port'], '22')
        self.assertEqual(router.nvram['sshd_passwd_auth'], '1')
        self.assertEqual(router.nvram['sshd_authorized_keys'], '')
        self.assertEqual(router.nvram['sshd_forwarding'], '0')

    def test_sshd_disable(self):
        nvram = {'sshd_enable': '1',
                 'sshd_wanport': '22',
                 'sshd_port': '22',
                 'sshd_passwd_auth': '1',
                 'sshd_authorized_keys': '',
                 'sshd_forwarding': '0',
                 }

        router = Router(nvram)
        router.changeSshdStatus(False)
        self.assertEqual(router.nvram['sshd_enable'], '0')


if __name__ == '__main__':
    unittest.main()
