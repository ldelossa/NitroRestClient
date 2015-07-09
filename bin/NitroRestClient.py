from . import requests
import json


class NitroRestClient(object):

    def __init__(self, netscalerip,username,password):
        self.netscalerip = netscalerip
        self.username = username
        self.password = password
        self.authcookie = None
        self.physicalservers = None
        self.login()

    def login(self):
        url = 'http://%s/nitro/v1/config/login' % self.netscalerip
        header = {'Content-Type': 'application/vnd.com.citrix.netscaler.login+json'}
        payload = {
            "login":
                {
                    "username": self.username,
                    "password": self.password
                }
        }
        loginsession = requests.post(url, data=json.dumps(payload), headers=header)
        authcookie = {'NITRO_AUTH_TOKEN': loginsession.cookies['NITRO_AUTH_TOKEN']}
        self.authcookie = authcookie

    def servernamecheck(self, servername):
        physicalserverlist = self.getphysicalservers()
        for server in physicalserverlist:
            if server['name'].lower() == servername.lower():
                return server['name']
        raise ValueError("Server Name Invalid")

    def disablephysicalserver(self, physicalservername):
        if self.authcookie is None:
            print("Please use the login method to create authentication cookie")
            return
        if physicalservername is None:
            print("Please specify physical server name")
            return
        url = 'http://%s/nitro/v1/config/server?action=disable' % self.netscalerip
        header = {'Content-Type': 'application/vnd.com.citrix.netscaler.server+json'}
        payload = {
            "server": {
                "name": physicalservername,
                "graceful": "YES"
            }
        }
        request = requests.post(url, data=json.dumps(payload), headers=header, cookies=self.authcookie)
        print(request.text)

    def enablephysicalserver(self, physicalservername):
        if self.authcookie is None:
            print("Please use the login method to create authentication cookie")
            return
        if physicalservername is None:
            print("Please specify physical server name")
            return
        url = 'http://%s/nitro/v1/config/server?action=enable' % self.netscalerip
        header = {'Content-Type': 'application/vnd.com.citrix.netscaler.server+json'}
        payload = {
            "server": {
                "name": physicalservername
            }
        }
        request = requests.post(url, data=json.dumps(payload), headers=header, cookies=self.authcookie)
        print(request.text)

    def getphysicalservers(self):
        url = 'http://%s/nitro/v1/config/server' % self.netscalerip
        header = {'Content-Type': 'application/vnd.com.citrix.netscaler.server+json'}
        request = requests.get(url, headers=header, cookies=self.authcookie)
        serverdict = json.loads(request.text)
        #pprint.pprint(serverdict['server'])
        return serverdict['server']

    def getservicegroupbindingsbyservername(self, servername):
        url = 'http://%s/nitro/v1/config/server_servicegroup_binding/%s' % (self.netscalerip, servername)
        request = requests.get(url, cookies=self.authcookie)
        diction = json.loads(request.text)
        return diction['server_servicegroup_binding']

    def getmemberserverstats(self, servicegroupname, port, servername):
        url = 'http://%s/nitro/v1/stat/servicegroupmember?args=servicegroupname:%s,port:%d,servername:%s' \
              % (self.netscalerip, servicegroupname, port, servername)
        request = requests.get(url, cookies=self.authcookie)
        diction = json.loads(request.text)
        return diction['servicegroupmember']

    def getmemberserverstatsbyserver(self, servername):
        # get all service group bindings
        servicegroups = self.getservicegroupbindingsbyservername(servername)
        statslistforserver = []
        # for each service group collected obtain the statistics for given server, add to list, and return
        for servicegroup in servicegroups:
            tempstatlist = self.getmemberserverstats(servicegroup['servicegroupname'],
                                                      servicegroup['port'], servername)
            # split servicegroupname string and place each into more descriptive dictionary keys -- this is for
            # easier identification
            extractedstringlist = tempstatlist[0]['servicegroupname'].split("?")
            tempstatlist[0][u'extractedservicegroup'] = extractedstringlist[0]
            tempstatlist[0][u'extractedservername'] = extractedstringlist[1]
            tempstatlist[0][u'extractedport'] = extractedstringlist[2]
            statslistforserver += tempstatlist
        return statslistforserver

















