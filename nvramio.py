#!/usr/bin/env python3

import logging
import argparse
import struct
from getpass import getpass
import io
import pyAesCrypt
import json
from os import stat

logger = False

def parseArgs():
  parser = argparse.ArgumentParser(description='Tool to read DD-WRT NVRAM files')
  parser.add_argument('-nvram', help="nvram file to read and work on")
  parser.add_argument('-rename', type=int, help="new router name as a number, e.g. 33")
  parser.add_argument('-out', help="nvram file to write output to")
  parser.add_argument('-adminpasswd', help="change admin password", action='store_true')
  parser.add_argument('-wifipasswd', help="change wifi password", action='store_true')
  parser.add_argument('-apisolation', help="enable AP Isolation", action='store_true')
  parser.add_argument('--verbose', '-v', action='count')
  parser.add_argument('--print', '-p', help="print out the new configuration", action='store_true')
  parser.add_argument('--storewifi', help="store WiFi passwords", action='store_true')
  parser.add_argument('--showwifi', help="store WiFi passwords", action='store_true')
  parser.add_argument('--wifisettings', help="file with WiFi passwords")
  args = parser.parse_args()
  return args

def getLogger(args):
  logger = logging.getLogger('nvram_tool')
  if args.verbose is None:
    logger.setLevel(logging.ERROR)
  elif args.verbose == 1:
      logger.setLevel(logging.INFO)
  elif args.verbose >= 2:
      logger.setLevel(logging.DEBUG)
  ch = logging.StreamHandler()
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  ch.setFormatter(formatter)
  logger.addHandler(ch)
  return logger

############ ENCRYPTED STORAGE OF SETTINGS ####################

bufferSize = 64 * 1024

def writeSettingsToFile(settings, filename, password):
  global bufferSize
  settingsStr = json.dumps(settings).encode('utf-8')
  fIn = io.BytesIO(settingsStr)
  with open(filename, "wb") as fOut:
    pyAesCrypt.encryptStream(fIn, fOut, password, bufferSize)

def readSettingsFromFile(filename, password):
  global bufferSize
  with open(filename, "rb") as fIn:
    fOut = io.BytesIO()
    size = stat(filename).st_size
    pyAesCrypt.decryptStream(fIn, fOut, password, bufferSize, size)
    fJson = io.StringIO(fOut.getvalue().decode('utf-8'))
    return json.load(fJson)

def storeWiFiSettings(filename):
  print("About to save WiFi passwords in %s" % filename)
  password = getpass("Please, provide password to encrypt the settings: ")
  internal = getpass("Please, provide Internal PSK: ")
  external = getpass("Please, provide External PSK: ")
  byod = getpass("Please, provide BYOD PSK: ")
  settings = { 'internal': internal, 'external': external, 'byod': byod }
  writeSettingsToFile(settings, filename, password)

def readWiFiSettingsUI(filename):
  password = getpass("Please, provide password to decrypt the WiFi settings: ")
  settings = readSettingsFromFile(filename, password)
  return settings
def showWiFiSettings(filename):
  settings = readWiFiSettingsUI(filename)
  for k, v in settings.items():
    print("%s = '%s'" %(k, v))

############## READING AND WRITING NVRAM FILES ################

def readNAsciiBytes(f, n):
  key = f.read(n).decode('ascii')
  return key

def readKeyVal(f):
  global logger
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

def readNvram(filename):
  global logger
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
      res = readKeyVal(f)
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

def writeNvram(filename, nvram):
  global logger
  logger.info("Writing to this file: %s" % filename)
  with open(filename, 'wb') as f:
    f.write(b'DD-WRT')
    count = len(nvram)
    f.write(struct.pack('H', count))
    for k, v in nvram.items():
      writeKeyVal(f, (k, v) )
  return True

############## NVRAM Manipulations ################

def renameRouter(nvram, name):
  # changing names and ssids
  nvram['wan_hostname'] = 'mozaiq%s' % name
  nvram['ath2_ssid'] = 'mozaiq%s' % name
  nvram['ath1_ssid'] = 'mozaiq%s' % name
  nvram['ath1.2_ssid'] = 'mozaiq-byod-%s' % name
  nvram['ath0_ssid'] = 'mozaiq%s' % name
  nvram['ath1.1_ssid'] = 'mozaiq-external-%s' % name
  nvram['router_name'] = 'mozaiq%s' % name
  # changing ip addresses
  nvram['ath1.1_ipaddr'] = '192.168.1%s.1' % name
  nvram['ath1.2_ipaddr'] = '192.168.2%s.1' % name
  nvram['lan_ipaddr'] = '192.168.%s.1' % name

def hashPassword(password):
  from passlib.hash import md5_crypt
  return md5_crypt.using(salt_size=8).hash(password)

def changeAdminPassword(nvram, password):
  nvram['http_passwd'] = hashPassword(password)

def changeWifiPasswords(nvram, internal, external, byod):
  nvram['ath2_wpa_psk'] = '%s' % internal
  nvram['ath1.2_wpa_psk'] = '%s' % byod
  nvram['ath1_wpa_psk'] = '%s' % internal
  nvram['ath1.1_wpa_psk'] = '%s' % external
  nvram['ath0_wpa_psk'] = '%s' % internal

def enableApIsolation(nvram):
  nvram['ath1.1_ap_isolate'] = '1' #external
  nvram['ath1.1_isolation'] = '1'
  nvram['ath1.2_ap_isolate'] = '1' #byod
  nvram['ath1.2_isolation'] = '1'

##################### MAIN ######################
def main():
  global logger
  args = parseArgs()

  logger = getLogger(args)
  logger.info("NVRAM tool started")

  if not args.print and args.out is None and not args.storewifi and not args.showwifi:
    logger.error("Please, specify -p to print or an -out file or --storewifi or --showwifi")
    return

  if args.storewifi or args.showwifi:
    if args.wifisettings is None:
      logger.error("Please specify --wifisettings file")
      return
    if args.storewifi:
      storeWiFiSettings(args.wifisettings)
    elif args.showwifi:
      showWiFiSettings(args.wifisettings)
    return

  if args.nvram is None:
    logger.error("For these settings you need to specify -nvram file, please")
    return

  nvram = readNvram(args.nvram)
  if nvram == False:
    return

  if args.rename is not None:
    renameRouter(nvram, args.rename)

  if args.adminpasswd:
    passwd = getpass("\nPlease, input a new admin password: ")
    changeAdminPassword(nvram, passwd)

  if args.wifipasswd and args.wifisettings is None:
    logger.error("Please, provide --wifisettings file if you wish to change wifi passwords. Create one with --storewifi.")
    return
  elif args.wifipasswd:
    settings = readWiFiSettingsUI(args.wifisettings)
    internal = settings['internal']
    external = settings['external']
    byod = settings['byod']
    changeWifiPasswords(nvram, internal, external, byod)

  if args.apisolation:
    enableApIsolation(nvram)

  if args.print:
    for k,v in nvram.items():
      print("%s = '%s'" % (k,v))

  if args.out is not None:
    writeNvram(args.out, nvram)

  logger.info("Done")


if __name__ == "__main__":
  main()
