"""
This module is meant to provide quick access to
the AppCenter API
"""
import sys

try:
    import requests
except ImportError, e:
    print "*******   WARNING   ********"
    print "you must install the requests library"
    print "copy and paste this command into your terminal"
    print "sudo pip install requests"
    pass

import json
import urllib


class AppCenter:
    "class for testing the User api"

    class BaseAPI1Exception(Exception):
        pass

    class FetchKeyError(BaseAPI1Exception):
        pass

    DEBUG = False

    def __init__(self):
        """
        initialize the info in apikey.json
        this is meant to hold a static API key as well
        as your tenant name

        :raises self.FetchKeyError: if the api key can not be fetched.
        """
        jsondata = open('apikey.json')
        data = json.load(jsondata)
        self.url = data["url"]
        self.key = data.get("key", "")
        if not self.key:
            self.key = self.getTempKey()
            if self.key is False:
                raise self.FetchKeyError("Could not get temporary api key")

        self.ListGroupURL = data["ListGroup"]
        self.AddGroupURL = data["AddGroup"]
        self.GroupDetailsURL = data["GroupDetails"]
        self.UsersInGroup = data["UsersInGroup"]
        self.Ecosystem = data["AppEcosystem"]
        self.ListAppsURL = data["ListApps"]
        self.AddUserURL = data["AddUser"]
        self.Groups = None
        jsondata.close()

    def getTempKey(self):
        """
        Gets a temporary key based on user's username and password

        :return: False if there was an error, or the api key if not.
        :rtype: str,bool
        """
        import getpass

        try:
            uname = raw_input('username: ')
        except KeyboardInterrupt:
            print "\nAborted"
            return False

        try:
            passw = getpass.getpass("password: ")
        except KeyboardInterrupt:
            print "\nAborted"
            return False

        postdata = {'username': uname, 'password': passw}
        response = self.post(self.url + "/api1/login", postdata)
        try:
            return response['api-key']
        except KeyError:
            print "No key data returned."
            return False

    class InvalidAPIResponse(BaseAPI1Exception):
        pass

    class ErrorAPI1Response(BaseAPI1Exception):
        pass


    def _get_response(self, verb, url, params=None):
        """
        Combines the logic of post-processing the appcenter api1 response.

        A valid api1 response MUST have a x-nukona-status header in it.
        A valid api1 response MUST be json encoded and MUST have a 'status' field in it,
        indicating success or failure.

        :param verb: the http verb, i.e. 'GET', or 'POST.
        :type verb: str,unicode
        :param url: the URL including any get-query parameters already added.
        :type url: str,unicode
        :param params: optional parameters used only for POST
        :type params: dict,None
        :return: the dictionary of the results
        :rtype:dict
        :raises AppCenter.InvalidAPIResponse: if the response is not a valid API1 response
        :raises AppCenter.ErrorAPI1Response: if the response is an error response
        """
        if self.key:
            connector = "?" if not url.find('?') > 0 else '&'
            url += connector + urllib.urlencode({'api_key': self.key})
        if verb == 'GET':
            assert(params is None)
            req = requests.get(url)
        elif verb == 'POST':
            req = requests.post(url, params)

        if 'x-nukona-status' not in req.headers:
            raise self.InvalidAPIResponse('No "x-nukona-status" header in response.')

        try:
            response = json.loads(req.content)
        except ValueError:
            raise self.InvalidAPIResponse("Response could not be decoded: Not json perhaps?")

        if response['status'] == 'error' or req.headers['x-nukona-status'] != '1':
            raise self.ErrorAPI1Response({'code': req.headers['x-nukona-status'], 'message': response['message']})
        return response


    def get(self, url):
        return self._get_response('GET', url)

    def post(self, url, params):
        return self._get_response('POST', url, params)

    def getGroupPayload(self):
        response = self.get(self.url + self.ListGroupURL)
        if response is False:
            return False
        self.Groups = response

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
        appEcoUrl = appEcoUrl % (appID)
        req = requests.get(self.url + appEcoUrl)
        print req.text

    def getAppList(self):
        appListUrl = self.ListAppsURL
        req = requests.get(self.url + appListUrl)
        self.Apps = req.text
        print req.text

    def getAppPackBund(self):
        appPackBund = []
        for app in self.Apps:
            appPackBund.append(app['packbund'])
        return appPackBund

    def listGroupNames(self):
        if self.Groups is None:
            self.getGroupPayload()

        self.groupNames = self.Groups["groups"]

        for g in self.groupNames:
            print g['name']

    def listGroupIds(self):
        if self.Groups is None:
            self.getGroupPayload()

        self.groupIds = self.Groups["groups"]

        for g in self.groupIds:
            print "%(id)s: %(name)s" % g

    def addUserManually(self):
        uname = raw_input("username: ")
        fname = raw_input("first name: ")
        lname = raw_input("last name: ")
        email = raw_input("email: ")
        passwd = raw_input("password (optional): ")
        if passwd == "":
            userPayload = {'username': uname, 'first_name': fname, 'last_name': lname, 'email': email}
        else:
            userPayload = {'username': uname, 'first_name': fname, 'last_name': lname, 'email': email,
                           'password': passwd}
        userPayload = json.dumps(userPayload)
        print userPayload
        self.post(self.url+self.AddUserURL, userPayload)





if __name__ == "__main__":
    try:
        ac = AppCenter()
        ac.listGroupIds()
    except AppCenter.BaseAPI1Exception as e:
        print e
        sys.exit(1)


