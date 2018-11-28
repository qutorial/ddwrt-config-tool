import unittest

class TestSettingsDecoding(unittest.TestCase):

  def test_read_settings(self):
    from settings import writeSettingsToFile
    settings = {'foo' : 'bar'}
    writeSettingsToFile(settings, 'test/settings.enc', "123")
    from settings import readSettingsFromFile
    settings = readSettingsFromFile('test/settings.enc', "123")
    self.assertTrue(len(settings) > 0)
    self.assertTrue(settings['foo'] == 'bar')


