#!./venv/bin/python3

from lease import Lease
from read_leases import readLeases
from read_sshd_config import readSshdSettings


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

  def addLeasesFromFile(self,leaseSettingsFile):
    leaseList = readLeases(leaseSettingsFile)
    for lease in leaseList:
        self.addLease(lease)

  def changeSshdStatus(self, enableSshd):
    if enableSshd:
      self.nvram['sshd_enable'] = '1'
      self.nvram['sshd_port'] = '22'
      self.nvram['sshd_passwd_auth'] = '0'
      self.nvram['sshd_authorized_keys'] = ''
      self.nvram['sshd_forwarding'] = '0'
    else:
      self.nvram['sshd_enable'] = '0'

  def enableWanSsh(self, enableRemoteAccess, wanPort=22):
    if enableRemoteAccess:
      self.nvram['remote_mgt_ssh'] = '1'
      self.nvram['sshd_wanport'] = str(wanPort)
    else:
      self.nvram['remote_mgt_ssh'] = '0'

  def addSshKey(self, sshKey):
    sshKey += '\n'
    self.nvram['sshd_authorized_keys'] += sshKey

  def addSshKeys(self, sshKeys):
    for key in sshKeys:
      self.addSshKey(key)

  def enableSshKeyAuth(self, authorizedKeys):
    if len(authorizedKeys):
      self.addSshKeys(authorizedKeys)

  def handleSshdSettings(self, sshSettingsFile):
    sshdSettings = readSshdSettings(sshSettingsFile)

    if sshdSettings['sshd_status'] == 'enable':
      self.changeSshdStatus(True)
      if sshdSettings['wan_port_ssh_remote_access'] == 'enable':
        self.enableWanSsh(enableRemoteAccess=True, wanPort=sshdSettings['ssh_wan_port_number'])
      else:
        self.enableWanSsh(enableRemoteAccess=False)

      self.enableSshKeyAuth(sshdSettings['authorized_keys'])

    elif sshdSettings['sshd_status'] == 'disable':
      self.changeSshdStatus(False)












