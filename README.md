[![Build Status](https://api.travis-ci.com/qutorial/ddwrt-config-tool.svg?branch=master)](https://travis-ci.com/qutorial/ddwrt-config-tool)

# DD-WRT configuration tool for mozaiq
 
Usage

```

./mnvram.py triband.30.bin -r 33 --apisolation --adminpasswd -w mozaiq.wifi.enc -o 33.bin -sl lease_config.json --sshd sshd_config.json


```

This means take triband.30.bin configuration file for the 30 router, rename it to be 33 router,
introduce Acess Point Isolation, change admin passwords for web UI, set wifi passwords from the 
mozaiq.wifi.enc encrypted file and write the result to 33.bin. DHCP performs static IP address 
allocation for users in lease_config.json. SSH is enabled or disabled based on the flags set in the sshd_config.json

See `./mnvram.py -h` for help.


### WiFi settings tool

```
$ ./msettings.py -h
usage: msettings.py [-h] [--verbose] [--storewifi] [--showwifi] wifipasswords

Tool to store settings for ddwrt nvramio

positional arguments:
  wifipasswords  file with WiFi passwords

optional arguments:
  -h, --help     show this help message and exit
  --verbose, -v
  --storewifi    store WiFi passwords
  --showwifi     store WiFi passwords 

```



## Installation

Please, run:

```make install```

or 

```make install-dev``` - for a developer version


It installs the necessary packages with apt and 
builds a virtualenv for python for this tool.

Use `source activate.sh` to have the right python environment
when using the tool.


## Developer

Here is the list of files explained

ddwrtnvram.py - library to read and write DD-WRT binary configuration backup format  
install.sh - script to install this tool   
mnvram.py - user interface for the mozaiq nvram tool - run it to generate configurations   
mozaiq.wifi.enc - request this file with PSKs to set - it contains wifi passwords   
msettings.py - user interface for mozaiq - run it to set WiFi passwords config file   
nvramargs.py - parsing command line arguments - common source   
nvramlogging.py - logging common source   
README.md - this readme   
requirements.txt - pip3 freeze output - dependencies for this project   
settings.py - library to read and write encrypted setttings including wifi passwords   
test - some test scripts   
triband.30.bin - request this file - it is a standard WRT3200ACM configuration for mozaiq   
lease_config.json - static dhcp allocation user config details
sshd_config.json - SSH configuration details like ssh enable/disable, enable/disable ssh remote access, ssh wan port number, ssh auth keys. 




