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

  def test_sshd_enable(self):
    nvram = {}
    from mnvram import MozaiqRouter
    router = MozaiqRouter(nvram)
    router.updateSshd(sshSettingsFile='test/sshd_settings_files/sshd_enable.json')
    self.assertEqual(router.nvram['sshd_enable'], '1')
    self.assertEqual(router.nvram['sshd_port'], '22')
    self.assertEqual(router.nvram['sshd_passwd_auth'], '0')
    self.assertEqual(router.nvram['sshd_forwarding'], '0')

    shouldBe = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCmNQmpuQSQR5iphz+hVZve+no3+TtfLoN8J2MjALtZ1RgiHyIV/q0KnClGz0n+55/bHO3UzDzq+Ps5SnMJcosk8Ywp0Rt0GfTOAAp5qrCvfnb1AihPDoFcOXK/uqrRV5IeY3he3VZ33kCjQ6nFMRFVnSFiTU9JSL05Wi0wmQTD1t/EbLr2m2FhalGh7YzBArJKFJbUEpTFuPHZrdcuQiD9hKxyz6HiZOiplOHGtbVAqrow62zLNHOpquI0NXwuKbD9DaeMmGnbibYurYNEVtnGDKTGTVUn3Pc8EjkjKuZyJpsdB/jZcpvSjcoJGSm17+K6QVriBJy4acUfQWOWaUAd vinod@vinod\nssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDEN3P7Vzm3yLGxWIkz5bEcZ0bVNXefkHLuwV5FWZWDWNZOqJqFwfq6URZDz2Mq3KFRg+4vnyTLA2D6Te8G3sIUlbn4GxSaDaxJwST4EKHnc2pP5dkVzGaAbDNdSL6TLtjImGdrsm8tRdoS6NcMGp5kfBPS2e4piQ4bcrB5hwSszOjxrVrOzAvub/DAzdf4vzlZ3K7mlXp0uG/2aMgSJ8YhoJ6bj388kOCUD5A3kCnJRjQlW2X5t6v6UHDcd4rLmy1gbCGI1ayBlJwFNF98H4sGTG7hhFxMdqj+sDqj4v1hIWygeo4cRTfLwa52RrUtS2K5JkWeZWbK8K3I0ixxJijQFgBntfDLVQXn7bOQ7A3LYMamGLH/qfyevms5iSdtRATyOUjH20EptVShp5lWDBxRFpGuIGDMDyZexxIV71gNBTMNLflfdsfYFtmJVtmeo/0eKbW1YybZ0tWyoF1yG5B7VgZCiZDSwLeG3R68Zr4mHz+mcmuX/ZpOEYxWMlfD1MDfNjUwGkfSNV0etvYJ7d+GJ65jkm+/nV7HCTZHiqtwN2S+N5nf47yKZecz/2uN/ZlH63hTF0qpabldFiVAmEH6LKr93a47IByCsh4bL7PZkxKGVIXKDGtgrsTWheIyvD/O+PZHPJIMLyET7daFAGCZ6YtnnMbzoOmhH9mxyn4PEQ== asbat.elkhairi@gmail.com\n"
    self.assertEqual(router.nvram['sshd_authorized_keys'], shouldBe)

  def test_sshd_disable(self):
    nvram = {}
    from mnvram import MozaiqRouter
    router = MozaiqRouter(nvram)
    router.updateSshd(sshSettingsFile='test/sshd_settings_files/sshd_disable.json')
    self.assertEqual(router.nvram['sshd_enable'], '0')

  def test_sshd_enable_wan_disable(self):
    nvram = {}
    from mnvram import MozaiqRouter
    router = MozaiqRouter(nvram)
    router.updateSshd(sshSettingsFile='test/sshd_settings_files/sshd_enable_wan_disable.json')

    self.assertEqual(router.nvram['sshd_enable'], '1')
    self.assertEqual(router.nvram['sshd_port'], '22')
    self.assertEqual(router.nvram['sshd_passwd_auth'], '0')
    self.assertEqual(router.nvram['sshd_forwarding'], '0')

    shouldBe = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCmNQmpuQSQR5iphz+hVZve+no3+TtfLoN8J2MjALtZ1RgiHyIV/q0KnClGz0n+55/bHO3UzDzq+Ps5SnMJcosk8Ywp0Rt0GfTOAAp5qrCvfnb1AihPDoFcOXK/uqrRV5IeY3he3VZ33kCjQ6nFMRFVnSFiTU9JSL05Wi0wmQTD1t/EbLr2m2FhalGh7YzBArJKFJbUEpTFuPHZrdcuQiD9hKxyz6HiZOiplOHGtbVAqrow62zLNHOpquI0NXwuKbD9DaeMmGnbibYurYNEVtnGDKTGTVUn3Pc8EjkjKuZyJpsdB/jZcpvSjcoJGSm17+K6QVriBJy4acUfQWOWaUAd vinod@vinod\nssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDEN3P7Vzm3yLGxWIkz5bEcZ0bVNXefkHLuwV5FWZWDWNZOqJqFwfq6URZDz2Mq3KFRg+4vnyTLA2D6Te8G3sIUlbn4GxSaDaxJwST4EKHnc2pP5dkVzGaAbDNdSL6TLtjImGdrsm8tRdoS6NcMGp5kfBPS2e4piQ4bcrB5hwSszOjxrVrOzAvub/DAzdf4vzlZ3K7mlXp0uG/2aMgSJ8YhoJ6bj388kOCUD5A3kCnJRjQlW2X5t6v6UHDcd4rLmy1gbCGI1ayBlJwFNF98H4sGTG7hhFxMdqj+sDqj4v1hIWygeo4cRTfLwa52RrUtS2K5JkWeZWbK8K3I0ixxJijQFgBntfDLVQXn7bOQ7A3LYMamGLH/qfyevms5iSdtRATyOUjH20EptVShp5lWDBxRFpGuIGDMDyZexxIV71gNBTMNLflfdsfYFtmJVtmeo/0eKbW1YybZ0tWyoF1yG5B7VgZCiZDSwLeG3R68Zr4mHz+mcmuX/ZpOEYxWMlfD1MDfNjUwGkfSNV0etvYJ7d+GJ65jkm+/nV7HCTZHiqtwN2S+N5nf47yKZecz/2uN/ZlH63hTF0qpabldFiVAmEH6LKr93a47IByCsh4bL7PZkxKGVIXKDGtgrsTWheIyvD/O+PZHPJIMLyET7daFAGCZ6YtnnMbzoOmhH9mxyn4PEQ== asbat.elkhairi@gmail.com\n"
    self.assertEqual(router.nvram['sshd_authorized_keys'], shouldBe)

    self.assertEqual(router.nvram['remote_mgt_ssh'], '0')


  def test_sshd_enable_wan_enable(self):
    nvram = {}
    from mnvram import MozaiqRouter
    router = MozaiqRouter(nvram)
    router.updateSshd(sshSettingsFile='test/sshd_settings_files/sshd_enable_wan_enable.json')

    self.assertEqual(router.nvram['sshd_enable'], '1')
    self.assertEqual(router.nvram['sshd_port'], '22')
    self.assertEqual(router.nvram['sshd_passwd_auth'], '0')
    self.assertEqual(router.nvram['sshd_forwarding'], '0')

    shouldBe = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCmNQmpuQSQR5iphz+hVZve+no3+TtfLoN8J2MjALtZ1RgiHyIV/q0KnClGz0n+55/bHO3UzDzq+Ps5SnMJcosk8Ywp0Rt0GfTOAAp5qrCvfnb1AihPDoFcOXK/uqrRV5IeY3he3VZ33kCjQ6nFMRFVnSFiTU9JSL05Wi0wmQTD1t/EbLr2m2FhalGh7YzBArJKFJbUEpTFuPHZrdcuQiD9hKxyz6HiZOiplOHGtbVAqrow62zLNHOpquI0NXwuKbD9DaeMmGnbibYurYNEVtnGDKTGTVUn3Pc8EjkjKuZyJpsdB/jZcpvSjcoJGSm17+K6QVriBJy4acUfQWOWaUAd vinod@vinod\nssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDEN3P7Vzm3yLGxWIkz5bEcZ0bVNXefkHLuwV5FWZWDWNZOqJqFwfq6URZDz2Mq3KFRg+4vnyTLA2D6Te8G3sIUlbn4GxSaDaxJwST4EKHnc2pP5dkVzGaAbDNdSL6TLtjImGdrsm8tRdoS6NcMGp5kfBPS2e4piQ4bcrB5hwSszOjxrVrOzAvub/DAzdf4vzlZ3K7mlXp0uG/2aMgSJ8YhoJ6bj388kOCUD5A3kCnJRjQlW2X5t6v6UHDcd4rLmy1gbCGI1ayBlJwFNF98H4sGTG7hhFxMdqj+sDqj4v1hIWygeo4cRTfLwa52RrUtS2K5JkWeZWbK8K3I0ixxJijQFgBntfDLVQXn7bOQ7A3LYMamGLH/qfyevms5iSdtRATyOUjH20EptVShp5lWDBxRFpGuIGDMDyZexxIV71gNBTMNLflfdsfYFtmJVtmeo/0eKbW1YybZ0tWyoF1yG5B7VgZCiZDSwLeG3R68Zr4mHz+mcmuX/ZpOEYxWMlfD1MDfNjUwGkfSNV0etvYJ7d+GJ65jkm+/nV7HCTZHiqtwN2S+N5nf47yKZecz/2uN/ZlH63hTF0qpabldFiVAmEH6LKr93a47IByCsh4bL7PZkxKGVIXKDGtgrsTWheIyvD/O+PZHPJIMLyET7daFAGCZ6YtnnMbzoOmhH9mxyn4PEQ== asbat.elkhairi@gmail.com\n"
    self.assertEqual(router.nvram['sshd_authorized_keys'], shouldBe)

    self.assertEqual(router.nvram['remote_mgt_ssh'], '1')
    self.assertEqual(router.nvram['sshd_wanport'], '56')
