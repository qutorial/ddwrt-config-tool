#!/usr/bin/env python3

from nvramlogging import getLogger
from nvramargs import getParser, parseArgs
from ddwrtnvram import readNvram, writeNvram
from msettings import readWiFiPasswordsUI
from getpass import getpass
import json

####### mozaiq-specific NVRAM Manipulations #######

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

def clearWiFiPsks(nvram):
  for k, v in nvram.items():
    if k.endswith('wpa_psk'):
      nvram[k] = ''


def enableApIsolation(nvram):
  nvram['ath1.1_ap_isolate'] = '1' #external
  nvram['ath1.1_isolation'] = '1'
  nvram['ath1.2_ap_isolate'] = '1' #byod
  nvram['ath1.2_isolation'] = '1'


def add_staticLease(nvram, leaseSettingsFile, router_id):                  # define a new method to add the static Lease
  with open("lease_config.json") as f:
    tmpl = json.load(f)

  static_leases = tmpl['static_leases']
  entries = []
  for hostname in static_leases:
    lease_details = static_leases[hostname]
    ip_addr = lease_details['ip_address'].split('.')
    third_octet = int(ip_addr[2])
    if third_octet >= 200:
      third_octet = str(200+router_id)
    elif 100 <= third_octet < 199:
      third_octet = str(100+router_id)
    else:
      third_octet = str(router_id)
    ip_addr[2] = third_octet
    lease_details['ip_address'] = ".".join(ip_addr)
    entry = lease_details['mac_address'] + "=" + lease_details['hostname'] + "=" + lease_details['ip_address'] + "=" + \
            lease_details['lease_time']
    print(entry)
    entries.append(entry)

  final_text = " ".join(entries)
  nvram['static_leases'] = final_text


################### TOOL UI #########################

def main():
  # prepare args
  parser = getParser('DD-WRT nvram manipulation tool')
  parser.add_argument('nvram', help="input nvram file")
  parser.add_argument('--rename', '-r', type=int, help="new router name as a number, e.g. 33")
  parser.add_argument('--out', '-o', help="nvram file to write output to")
  parser.add_argument('--adminpasswd', '-a', help="change admin password", action='store_true')
  parser.add_argument('--apisolation', '-i', help="enable AP Isolation", action='store_true')
  parser.add_argument('--print', '-p', help="print out the new configuration", action='store_true')
  parser.add_argument('--wifipasswords', '-w', help="file with WiFi passwords")
  parser.add_argument('--clearwifipasswords', '-c', help='erase WiFi PSKs from nvram', action='store_true')
  parser.add_argument('--add_static_lease', '-sl', help='include new static leases into nvram')
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

  if args.adminpasswd:
    passwd = getpass("\nPlease, input a new admin password: ")
    changeAdminPassword(nvram, passwd)

  if args.wifipasswords and args.clearwifipasswords:
    logger.error("Please, either clear PSKs or change them from file: -c or -w")
    return
  elif args.wifipasswords:
    settings = readWiFiPasswordsUI(args.wifipasswords)
    internal = settings['internal']
    external = settings['external']
    byod = settings['byod']
    changeWifiPasswords(nvram, internal, external, byod)
  elif args.clearwifipasswords:
    clearWiFiPsks(nvram)

  if args.apisolation:
    enableApIsolation(nvram)

  if args.add_static_lease:
    add_staticLease(nvram, args.add_static_lease, args.rename)

  if args.print:
    for k,v in nvram.items():
      print("%s = '%s'" % (k,v))

  if args.out is not None:
    writeNvram(args.out, nvram, logger)

  logger.info("Done")




if __name__ == "__main__":
  main()
