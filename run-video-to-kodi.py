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



## Define the Debug variable. If true it doesn't access the website, but just
#  reads from files
#
DEBUG = True


## Open the settings file
#
try:
  f = open('settings.json', 'r')
  settings = json.load(f)
  f.close()
except FileNotFoundError:
  print("settings.json file not found. Have you forgotten to rename settings.json.default?")
  sys.exit(0)




date_val = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


cookiejar = browser_cookie3.firefox(domain_name=settings["domain"])


## First read the front page
#
if DEBUG:
  
  NAME_1 = "20201223_084831_1.txt"
  
  with open(NAME_1, 'r') as f1:
    s_1 = f1.read()

else:

  opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar))
  r = opener.open(settings["website"] + "/")

  s_1 = r.read()
  with open(date_val + "_1.txt", "w") as f1:
    f1.write(s_1.decode('latin_1'))



soup_1 = BeautifulSoup(s_1, 'html.parser')




## Now check for any links that match the specified keywords
#
links = []

for link in soup_1.find_all('a'):
  for x in link.children:
    s = x.string
    if s != None:
      if s.upper().find(settings["keywords"][0])>=0:
        print(link.get('href'))
        links.append(link.get('href'))


if len(links) <= 0:
  print("Didn't find any links. Exiting ...")
  sys.exit(0)




## Now go into the first of those links
#
if DEBUG:
  
  NAME_2 = "20201223_084831_2.txt"
  
  with open(NAME_2, 'r') as f2:
    s_2 = f2.read()
  
else:

  opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar))
  r_2 = opener.open(urllib.parse.urljoin(settings["website"], links[0]))  # Just use the first link

  s_2 = r_2.read()
  with open(date_val + "_2.txt", "w") as f2:
    f2.write(s_2.decode('latin_1'))


soup = BeautifulSoup(s_2, 'html.parser')



## Go through finding all the card decks that seem to contain a video
#
decks = []

for deck in soup.find_all(class_='card'):
  for x_1 in deck.find_all('div', class_="card-body", limit=1):
    x_2 = x_1.find_all(class_="card-title")
    if len(x_2) >= 1:
      decks.append({'href':deck.find('a').get('href'), 'text':x_2[0].string})



if len(decks) <= 0:
  print("Didn't find any decks. Exiting")
  sys.exit(0)



## Allow the user to choose which one to view
#
for i in range(len(decks)):
  print("[{0:2d}]  :  {1}".format(i+1, decks[i]['text']))
  
  
print("Enter number to send (or anything else to cancel):")

s = input()

try:
  i_s = int(s)
except ValueError:
  i_s = -1

if i_s>=1 and i_s<=len(decks):
  print("A good number!")
  URL_3 = urllib.parse.urljoin(settings["website"], decks[i_s-1]['href'])
  print(URL_3)
else:
  print("Nothing entered")
  sys.exit(1)




## Read the selected content
#
if DEBUG:
  
  NAME_3 = "20201223_084831_3.txt"
  
  with open(NAME_3, 'r') as f3:
    s_3 = f3.read()
else:

  opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar))
  r_3 = opener.open(URL_3)

  s_3 = r_3.read()
  with open(date_val + "_3.txt", "w") as f3:
    f3.write(s_3.decode('latin_1'))
  


soup = BeautifulSoup(s_3, 'html.parser')


content_links = []

for link in soup.find_all(type="application/x-mpegURL"):
  content_links.append(link.get('src'))


if len(content_links) < 1:
  print("No content links found. Exiting")
  sys.exit(0)
  
  

## Read the first content file
#
if DEBUG:
  
  NAME_4 = "20201223_084831_4.txt"
  
  with open(NAME_4, 'r') as f4:
    s_4 = f4.read()

else:

  opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar))
  r_4 = opener.open(content_links[0])

  s_4 = r_4.read()
  with open(date_val + "_4.txt", "w") as f4:
    f4.write(s_4.decode('latin_1'))


