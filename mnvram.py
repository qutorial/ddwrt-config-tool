#!./venv/bin/python3

from nvramlogging import getLogger
from nvramargs import getParser, parseArgs
from ddwrtnvram import readNvram, writeNvram
from msettings import readWiFiPasswordsUI
from getpass import getpass
from router import Router
import json

####### mozaiq-specific NVRAM Manipulations #######

class MozaiqRouter(Router):

  def __init__(self, nvram={}):
    super(MozaiqRouter, self).__init__(nvram)

  def renameRouter(self, name):
    # changing names and ssids
    self.nvram['ath2_ssid'] = 'mozaiq%s-5ghz-2' % name
    self.nvram['ath1_ssid'] = 'mozaiq%s' % name
    self.nvram['ath1.2_ssid'] = 'mozaiq-byod-%s' % name
    self.nvram['ath0_ssid'] = 'mozaiq%s-5ghz' % name
    self.nvram['ath1.1_ssid'] = 'mozaiq-external-%s' % name
    # changing ip addresses
    self.nvram['ath1.1_ipaddr'] = '192.168.1%s.1' % name
    self.nvram['ath1.2_ipaddr'] = '192.168.2%s.1' % name
    self.nvram['lan_ipaddr'] = '192.168.%s.1' % name
    self.name = 'mozaiq%s' % name

  def changeAdminPassword(self, password):
    self.password = password

  def changeWifiPasswords(self, internal, external, byod):
    self.nvram['ath2_wpa_psk'] = '%s' % internal
    self.nvram['ath1.2_wpa_psk'] = '%s' % byod
    self.nvram['ath1_wpa_psk'] = '%s' % internal
    self.nvram['ath1.1_wpa_psk'] = '%s' % external
    self.nvram['ath0_wpa_psk'] = '%s' % internal

  def eraseWiFiPsks(self):
    self.clearWiFiPsks()

  def enableApIsolation(self):
    self.nvram['ath1.1_ap_isolate'] = '1' #external
    self.nvram['ath1.1_isolation'] = '1'
    self.nvram['ath1.2_ap_isolate'] = '1' #byod
    self.nvram['ath1.2_isolation'] = '1'

  def addStaticLease(self, leaseSettingsFile):
    self.addLeasesFromFile(leaseSettingsFile)

  def updateLeaseIps(self, router_id):
    leaseObjects = self.leases
    if len(leaseObjects) > 0 :
      for leaseObject in leaseObjects:
        self.modifyLeaseObject(leaseObject, router_id)

    self.leases = leaseObjects

  @staticmethod
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

  def updateSshd(self, newState):
      if newState == 'enable':
          self.changeSshdStatus(True)
      else:
          self.changeSshdStatus(False)

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
  parser.add_argument('--sshd', help='sshd enable(true)/disable(false)/donot-change', default=None)
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

  router = MozaiqRouter(nvram)

  if args.add_static_leases:
    router.addStaticLease(args.add_static_leases)

  if args.rename is not None:
    router.renameRouter(args.rename)
    router.updateLeaseIps(args.rename)

  if args.admin_passwd:
    passwd = getpass("\nPlease, input a new admin password: ")
    router.changeAdminPassword(passwd)

  if args.wifi_passwords and args.clear_wifi_passwords:
    logger.error("Please, either clear PSKs or change them from file: -c or -w")
    return
  elif args.wifi_passwords:
    settings = readWiFiPasswordsUI(args.wifi_passwords)
    internal = settings['internal']
    external = settings['external']
    byod = settings['byod']
    router.changeWifiPasswords(internal, external, byod)
  elif args.clear_wifi_passwords:
    router.eraseWiFiPsks()

  if args.ap_isolation:
    router.enableApIsolation()

  if args.sshd is not None:
    router.updateSshd(args.sshd)

  if args.print:
    for k,v in nvram.items():
      print("%s = '%s'" % (k,v))

  if args.out is not None:
    writeNvram(args.out, nvram, logger)

  logger.info("Done")

if __name__ == "__main__":
  main()
