#!./venv/bin/python3

from getpass import getpass
import io
import json
from os import stat
import pyAesCrypt

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
