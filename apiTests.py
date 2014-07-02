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
  'class for testing the User api'
  
  def __init__(self):
    jsondata = open('apikey.json')
    data = json.load(jsondata)
    self.key = data["key"]
    self.url = data["url"]
    self.ListGroupURL = data["ListGroup"]
    self.AddGroupURL = data["AddGroup"]
    self.GroupDetailsURL = data["GroupDetails"]
    self.UsersInGroup = data["UsersInGroup"]
    self.Ecosystem = data["AppEcosystem"]
    self.ListAppsURL = data["ListApps"]
    self.Groups = None
    self.payload = {'api_key':self.key}
    jsondata.close()
  
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