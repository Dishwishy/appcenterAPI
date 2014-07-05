"""
This module is meant to provide quick access to
the AppCenter API
"""
try:
  import requests
except ImportError, e:
  print "*******   WARNING   ********"
  print "you must install the requests library"
  print "copy and paste this command into your terminal"
  print "sudo pip install requests"
  pass

import json

class AppCenter:
  "class for testing the User api"
  
  def __init__(self):
    """
    initialize the info in apikey.json
    this is meant to hold a static API key as well
    as your tenant name
    """
    jsondata = open('apikey.json')
    data = json.load(jsondata)
    self.url = data["url"]
    try:
      self.key = data["key"]
    except NameError:
      self.key = self.getTempKey()

    self.ListGroupURL = data["ListGroup"]
    self.AddGroupURL = data["AddGroup"]
    self.GroupDetailsURL = data["GroupDetails"]
    self.UsersInGroup = data["UsersInGroup"]
    self.Ecosystem = data["AppEcosystem"]
    self.ListAppsURL = data["ListApps"]
    self.Groups = None
    if self.key == "":
        self.key = self.getTempKey()
    self.payload = {'api_key':self.key}
    jsondata.close()

  def getTempKey(self):
    uname = raw_input('username: ')
    passw = raw_input('password: ')
    postdata = {'username' : uname, 'password' : passw}
    keydata = json.loads(requests.post(self.url+"/api1/login", postdata).content)
    return keydata['api-key']
  
  def getGroupPayload(self):
    req = requests.get(self.url+self.ListGroupURL, params=self.payload)
    self.Groups = json.loads(req.text)
  
  def getGroupArray(self):
    if self.Groups is None:
        self.getGroupPayload()
        self.groupNames = self.Groups["groups"]
        return self.groupNames
    else:
        self.groupNames = self.Groups["groups"]
        return self.groupNames

  def getWrapEcosystem(self, appID):
    appEcoUrl = self.Ecosystem
    appEcoUrl = appEcoUrl %(appID)
    req = requests.get(self.url+appEcoUrl, params=self.payload)
    print req.text

  def getAppList(self):
    appListUrl = self.ListAppsURL
    req = requests.get(self.url+appListUrl, params=self.payload)
    self.Apps = json.loads(req.text)

  def getAppPackBund(self):
    appPackBund = []
    for app in self.Apps:
        appPackBund.append(app['packbund'])
    return appPackBund