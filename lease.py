#!./venv/bin/python3

# IP Static Lease
class Lease:
  def __init__(self, leaseDict={}): # dictionary with mac, host, ip and time
    for k in ['mac_address', 'hostname', 'ip_address', 'lease_time']:
        if not k in leaseDict:
            leaseDict[k] = ""
            
    self.mac_address = leaseDict['mac_address']
    self.hostname = leaseDict['hostname']
    self.ip_address = leaseDict['ip_address']
    self.lease_time = leaseDict['lease_time']
    
  def __str__(self):
      return "=".join([self.mac_address.upper(), self.hostname.lower(), self.ip_address, self.lease_time]) + " "
  
  def __repr__(self):
    return str(self)

  # get it from "="-separated string
  def fromStr(self, s):
    parts = s.split('=')
    if len(parts) != 4:
      return False
    self.mac_address = parts[0]
    self.hostname = parts[1]
    self.ip_address = parts[2]
    self.lease_time = parts[3]
    return self.isValid()
  
  def isValid(self):
    import re
    if re.match("^([0-9a-fA-F]{2}:){5}([0-9a-fA-F]{2}){1}$", self.mac_address) is None:
      return (False, "Invalid mac address")
    
    if re.match("^([a-z0-9]){1,63}$", self.hostname) is None:
      return (False, "Invalid hostname")
    
    if not is_valid_ipv4_address(self.ip_address):
      return (False, "Invalid IP address")
    
    try:
      lt = int(self.lease_time)
      if lt <= 0 or lt > 2592000: # it is 30 days
        return (False, "Too large or to small lease time")
    except:
      return (False, "Invalid lease time string")
    
    return (True, "Valid static lease")



import socket

def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True