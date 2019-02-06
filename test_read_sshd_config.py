import unittest
from read_sshd_config import readSshdSettings

class TestReadSshdConfig(unittest.TestCase):

  def test_read_sshd_config(self):
    sshd_config = readSshdSettings("sshd_config.json")

    shouldBe = {
                "sshd_status": "enable",
                "wan_port_ssh_remote_access": "enable",
                "ssh_wan_port_number": "22",
                "authorized_keys": [
                                    "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCmNQmpuQSQR5iphz+hVZve+no3+TtfLoN8J2MjALtZ1RgiHyIV/q0KnClGz0n+55/bHO3UzDzq+Ps5SnMJcosk8Ywp0Rt0GfTOAAp5qrCvfnb1AihPDoFcOXK/uqrRV5IeY3he3VZ33kCjQ6nFMRFVnSFiTU9JSL05Wi0wmQTD1t/EbLr2m2FhalGh7YzBArJKFJbUEpTFuPHZrdcuQiD9hKxyz6HiZOiplOHGtbVAqrow62zLNHOpquI0NXwuKbD9DaeMmGnbibYurYNEVtnGDKTGTVUn3Pc8EjkjKuZyJpsdB/jZcpvSjcoJGSm17+K6QVriBJy4acUfQWOWaUAd vinod@vinod",
                                    "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDEN3P7Vzm3yLGxWIkz5bEcZ0bVNXefkHLuwV5FWZWDWNZOqJqFwfq6URZDz2Mq3KFRg+4vnyTLA2D6Te8G3sIUlbn4GxSaDaxJwST4EKHnc2pP5dkVzGaAbDNdSL6TLtjImGdrsm8tRdoS6NcMGp5kfBPS2e4piQ4bcrB5hwSszOjxrVrOzAvub/DAzdf4vzlZ3K7mlXp0uG/2aMgSJ8YhoJ6bj388kOCUD5A3kCnJRjQlW2X5t6v6UHDcd4rLmy1gbCGI1ayBlJwFNF98H4sGTG7hhFxMdqj+sDqj4v1hIWygeo4cRTfLwa52RrUtS2K5JkWeZWbK8K3I0ixxJijQFgBntfDLVQXn7bOQ7A3LYMamGLH/qfyevms5iSdtRATyOUjH20EptVShp5lWDBxRFpGuIGDMDyZexxIV71gNBTMNLflfdsfYFtmJVtmeo/0eKbW1YybZ0tWyoF1yG5B7VgZCiZDSwLeG3R68Zr4mHz+mcmuX/ZpOEYxWMlfD1MDfNjUwGkfSNV0etvYJ7d+GJ65jkm+/nV7HCTZHiqtwN2S+N5nf47yKZecz/2uN/ZlH63hTF0qpabldFiVAmEH6LKr93a47IByCsh4bL7PZkxKGVIXKDGtgrsTWheIyvD/O+PZHPJIMLyET7daFAGCZ6YtnnMbzoOmhH9mxyn4PEQ== asbat.elkhairi@gmail.com"
                                    ]

                }


    self.assertEqual(sshd_config['sshd_status'], shouldBe['sshd_status'])
    self.assertEqual(sshd_config['wan_port_ssh_remote_access'], shouldBe['wan_port_ssh_remote_access'])
    self.assertEqual(sshd_config['ssh_wan_port_number'], shouldBe['ssh_wan_port_number'])
    for i in range(0, len(sshd_config['authorized_keys'])):
        self.assertEqual(sshd_config['authorized_keys'][i], shouldBe['authorized_keys'][i])
