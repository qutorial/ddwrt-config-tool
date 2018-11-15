#!/usr/bin/env python3

from getpass import getpass
from settings import writeSettingsToFile, readSettingsFromFile
from nvramlogging import getLogger
from nvramargs import getParser, parseArgs

################### mozaiq specific settings ########################################

def storeWiFiPasswords(filename):
  print("About to save WiFi passwords in %s" % filename)
  password = getpass("Please, provide password to encrypt the settings: ")
  internal = getpass("Please, provide Internal PSK: ")
  external = getpass("Please, provide External PSK: ")
  byod = getpass("Please, provide BYOD PSK: ")
  settings = { 'internal': internal, 'external': external, 'byod': byod }
  writeSettingsToFile(settings, filename, password)

def readWiFiPasswordsUI(filename):
  password = getpass("Please, provide password to decrypt the WiFi passwords: ")
  settings = readSettingsFromFile(filename, password)
  return settings

def showWiFiPasswords(filename):
  settings = readWiFiPasswordsUI(filename)
  for k, v in settings.items():
    print("%s = '%s'" %(k, v))

def main():
  parser = getParser('Tool to store settings for ddwrt nvramio')
  parser.add_argument('--storewifi', help="store WiFi passwords", action='store_true')
  parser.add_argument('--showwifi', help="store WiFi passwords", action='store_true')
  parser.add_argument('wifipasswords', help="file with WiFi passwords")
  args = parseArgs(parser)
  logger = getLogger(args)
  if args.storewifi:
    storeWiFiPasswords(args.wifipasswords)
  elif args.showwifi:
    showWiFiPasswords(args.wifipasswords)
  else:
    logger.error("Please, select --storewifi or --showwifi")
    return

if __name__ == "__main__":
  main()
