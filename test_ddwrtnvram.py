import unittest

from nvramlogging import getTestLogger
from os import remove

class TestNvramCoding(unittest.TestCase):

  def test_nvram_coding(self):
    logger = getTestLogger()
    remove('test/nvram.bin')
    from ddwrtnvram import readNvram, writeNvram
    nvram = {'foo' : 'bar'}
    self.assertTrue(writeNvram('test/nvram.bin', nvram, logger))
    nvram2 = readNvram('test/nvram.bin', logger)
    self.assertTrue(nvram2['foo'] == 'bar')


