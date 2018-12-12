#!./venv/bin/python3

from lease import Lease
from read_leases import readLeases


class Router:

  def __init__(self, nvram={}):
    self.nvram = nvram

  @property
  def wan_hostname(self):
    return self.nvram['wan_hostname']

  @wan_hostname.setter
  def wan_hostname(self, value):
    self.nvram['wan_hostname'] = value

  @property
  def router_name(self):
    return self.nvram['router_name']

  @router_name.setter
  def router_name(self, value):
    self.nvram['router_name'] = value

  @property
  def name(self):
    return self.nvram['router_name']

  @name.setter
  def name(self, value):
    self.router_name = value
    self.wan_hostname = value
  
  @property
  def password(self):
    return self.nvram['http_passwd']
  
  @password.setter
  def password(self, value):
    self.nvram['http_passwd'] = Router.hashPassword(value)
  
  @staticmethod
  def hashPassword(password):
    from passlib.hash import md5_crypt
    return md5_crypt.using(salt_size=8).hash(password)
  
  @staticmethod
  def normalizeLeases(leases):
    res = {}
    for l in leases:
      res[l.hostname] = l
    return sorted(res.values(),key=lambda x: x.hostname)
  
  @property
  def leases(self):
    leases = []
    if len(self.nvram['static_leases']) > 0:
      for l in self.nvram['static_leases'].split(' '):
        lease = Lease()
        if lease.fromStr(l):
          leases += [lease]
        elif len(l) > 1:
          raise Exception("Couldn't parse lease: %s" % l)
    return leases

  @leases.setter
  def leases(self, leases):
    self.nvram['static_leases'] = Router.leasesToStr(Router.normalizeLeases(leases))
    self.nvram['static_leasenum'] = str(len(self.leases))

  @staticmethod
  def leasesToStr(leases):
    return "".join(map(lambda l: str(l), leases))
  
  def leasesStr(self):
    return Router.leasesToStr(self.leases)
  
  def addLease(self, lease):
    self.leases += [lease]

  def clearWiFiPsks(self):
    for k, v in self.nvram.items():
      if k.endswith('wpa_psk'):
        self.nvram[k] = ''

  def modifyThirdOctet(self, leaseSettingsFile, router_id):
    leaseList = readLeases(leaseSettingsFile)
    for leaseObject in leaseList:
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
    for lease in leaseList:
        self.addLease(lease)
