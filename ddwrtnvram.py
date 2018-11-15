#!/usr/bin/env python3

import struct
import io
from os import stat

############## READING AND WRITING NVRAM FILES ################

def readNAsciiBytes(f, n):
  key = f.read(n).decode('ascii')
  return key

def readKeyVal(f, logger):
  tellPos = f.tell()
  # key length 1 byte, key, value length 2 bytes, value
  b = f.read(1)
  if f.tell() == tellPos:
    logger.debug("End of file reached")
    return False
  l = struct.unpack('B', b) # one byte
  l = l[0]
  key = readNAsciiBytes(f, l)
  logger.debug("key: %s" % key)
  # value length
  vl = struct.unpack('H', f.read(2)) # reading uint16
  logger.debug('value length: %s' % vl)
  vl = vl[0]
  value = readNAsciiBytes(f, vl)
  logger.debug("value: %s" % value)
  return (key, value)

def readNvram(filename, logger):
  logger.info("Reading this file: %s" % filename)
  with open(filename, 'rb') as f:
    header = f.read(6) # should start with DD-WRT+
    if header != b'DD-WRT':
      logger.error("Not a dd-wrt nvram bin file!")
      return (1, {})
    else:
      logger.info("DD-WRT nvram file detected")
    count = struct.unpack('H', f.read(2))[0] # reading uint16
    logger.debug("Count is: %s" % count)

    nvram = {}
    while True:
      res = readKeyVal(f, logger)
      if res == False:
        break
      (k, v) = res
      nvram[k]=v
      logger.debug("%s = %s" % (k,v))

    if len(nvram) != count :
      logger.error("Wrong keys count in the file")
      return False

    return nvram

def writeKeyVal(f, kv):
  (k, v) = kv
  f.write(struct.pack('B', len(k)))
  f.write(k.encode('ascii'))
  f.write(struct.pack('H', len(v)))
  f.write(v.encode('ascii'))

def writeNvram(filename, nvram, logger):
  logger.info("Writing to this file: %s" % filename)
  with open(filename, 'wb') as f:
    f.write(b'DD-WRT')
    count = len(nvram)
    f.write(struct.pack('H', count))
    for k, v in nvram.items():
      writeKeyVal(f, (k, v) )
  return True
