#! /bin/usr/python3


from bs4 import BeautifulSoup
import urllib
import urllib.parse
import urllib.request
import json
import os.path
import sys

import http.client
import datetime
from base64 import b64encode


import http.cookiejar


import browser_cookie3



## Open the settings file
#
try:
  f = open('settings.json', 'r')
  settings = json.load(f)
  f.close()
except FileNotFoundError:
  print("settings.json file not found. Have you forgotten to rename settings.json.default?")
  sys.exit(0)



