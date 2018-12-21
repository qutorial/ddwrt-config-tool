#!./venv/bin/python3

from nvramlogging import getLogger
from nvramargs import getParser, parseArgs
from ddwrtnvram import readNvram, writeNvram
from msettings import readWiFiPasswordsUI
from getpass import getpass
from router import Router
import json

####### mozaiq-specific NVRAM Manipulations #######

def renameRouter(nvram, name):
  router = Router(nvram)
  # changing names and ssids
  router.nvram['ath2_ssid'] = 'mozaiq%s-5ghz-2' % name
  router.nvram['ath1_ssid'] = 'mozaiq%s' % name
  router.nvram['ath1.2_ssid'] = 'mozaiq-byod-%s' % name
  router.nvram['ath0_ssid'] = 'mozaiq%s-5ghz' % name
  router.nvram['ath1.1_ssid'] = 'mozaiq-external-%s' % name
  # changing ip addresses
  router.nvram['ath1.1_ipaddr'] = '192.168.1%s.1' % name
  router.nvram['ath1.2_ipaddr'] = '192.168.2%s.1' % name
  router.nvram['lan_ipaddr'] = '192.168.%s.1' % name
  router.name = 'mozaiq%s' % name

def changeAdminPassword(nvram, password):
  router = Router(nvram)
  router.password = password

def changeWifiPasswords(nvram, internal, external, byod):
  nvram['ath2_wpa_psk'] = '%s' % internal
  nvram['ath1.2_wpa_psk'] = '%s' % byod
  nvram['ath1_wpa_psk'] = '%s' % internal
  nvram['ath1.1_wpa_psk'] = '%s' % external
  nvram['ath0_wpa_psk'] = '%s' % internal

def clearWiFiPsks(nvram):
  router = Router(nvram)
  router.clearWiFiPsks()


def enableApIsolation(nvram):
  nvram['ath1.1_ap_isolate'] = '1' #external
  nvram['ath1.1_isolation'] = '1'
  nvram['ath1.2_ap_isolate'] = '1' #byod
  nvram['ath1.2_isolation'] = '1'


def addStaticLease(nvram, leaseSettingsFile):                  # define a new method to add the static Lease
  router = Router(nvram)
  router.addLeasesFromFile(leaseSettingsFile)


def updateLeaseIps(nvram, router_id):
  router = Router(nvram)
  leaseObjects = router.leases
  if len(leaseObjects) > 0 :
    for leaseObject in  leaseObjects:
      modifyLeaseObject(leaseObject, router_id)

  router.leases = leaseObjects

def modifyLeaseObject(leaseObject, router_id):
  ip_addr = leaseObject.ip_address.split('.')
  third_octet = int(ip_addr[2])
  if third_octet >= 200:
    third_octet = str(200 + router_id)
  elif 100 <= third_octet < 199:
    third_octet = str(100 + router_id)
  else:
    third_octet = str(router_id)
  ip_addr[2] = third_octet

  leaseObject.ip_address = ".".join(ip_addr)
  return leaseObject


################### TOOL UI #########################

def main():
  # prepare args
  parser = getParser('DD-WRT nvram manipulation tool')
  parser.add_argument('nvram', help="input nvram file")
  parser.add_argument('--rename', '-r', type=int, help="new router name as a number, e.g. 33")
  parser.add_argument('--out', '-o', help="nvram file to write output to")
  parser.add_argument('--admin-passwd', '-a', help="change admin password", action='store_true')
  parser.add_argument('--ap-isolation', '-i', help="enable AP Isolation", action='store_true')
  parser.add_argument('--print', '-p', help="print out the new configuration", action='store_true')
  parser.add_argument('--wifi-passwords', '-w', help="file with WiFi passwords")
  parser.add_argument('--clear-wifi-passwords', '-c', help='erase WiFi PSKs from nvram', action='store_true')
  parser.add_argument('--add-static-leases', '-sl', help='include new static leases into nvram')
  args = parseArgs(parser)

  # set up logging
  logger = getLogger(args)

  # choose what to do based on args, continue
  logger.info("NVRAM tool started")

  if not args.print and args.out is None:
    logger.error("Please, specify -p to print or an -out file")
    return

  nvram = readNvram(args.nvram, logger)
  if nvram == False:
    return

  if args.rename is not None:
    renameRouter(nvram, args.rename)

  if args.admin_passwd:
    passwd = getpass("\nPlease, input a new admin password: ")
    changeAdminPassword(nvram, passwd)

  if args.wifi_passwords and args.clear_wifi_passwords:
    logger.error("Please, either clear PSKs or change them from file: -c or -w")
    return
  elif args.wifi_passwords:
    settings = readWiFiPasswordsUI(args.wifi_passwords)
    internal = settings['internal']
    external = settings['external']
    byod = settings['byod']
    changeWifiPasswords(nvram, internal, external, byod)
  elif args.clear_wifi_passwords:
    clearWiFiPsks(nvram)

  if args.ap_isolation:
    enableApIsolation(nvram)

  if args.add_static_leases:
    addStaticLease(nvram, args.add_static_leases)

  updateLeaseIps(nvram, args.rename)

  if args.print:
    for k,v in nvram.items():
      print("%s = '%s'" % (k,v))

  if args.out is not None:
    writeNvram(args.out, nvram, logger)

  logger.info("Done")


if __name__ == "__main__":
  main()
