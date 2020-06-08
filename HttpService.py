import requests
import json
import ipaddress

class HueInterfaceController:
    """
    Interfaces with the Hue Bridge.
    """
    def __init__(self):
        self.token = 'hPKjNr2MNZHYIJVE2PF6RmiSxhXyqcy5IOjOcj8u'
        self.accountUrl = ''
        self.generateBridgeToken = False
        self.availableLightsInTheHouse = 0
        self.fullAccessUrl = self.getFullAccessUrl()
        
    def getHueIpAddress(self):
        response = requests.get("https://discovery.meethue.com/")
        return response.json()[0]["internalipaddress"]

    def createNewAccount(self):
        ip = self.getHueIpAddress()
        
        self.accountUrl = "http://{}/api".format(ip)

        accountMessageJson = {
            'devicetype': 'jonasTest'
        }
        
        response = requests.post(self.accountUrl, json = accountMessageJson, verify=False)
        jsonResponse = response.json()
        
        try:
            return jsonResponse[0]['success']['username']
        except:
            raise ValueError('Failed to Create Account with Error {}: {}'.format(jsonResponse[0]['error']['type'], jsonResponse[0]['error']['description']))
        
    def getFullAccessUrl(self):
        if (self.generateBridgeToken):
            self.token = self.createNewAccount()
            return '{}/api/{}'.format(self.accountUrl, self.token)
        
        return 'http://{}/api/{}'.format(self.getHueIpAddress(), self.token)
                    
    def getAvailableLightsConnected(self):
        lightsUrl = '{}/lights'.format(self.fullAccessUrl)
        response = requests.get(lightsUrl)
        self.availableLightsInTheHouse = len(response.json())
        
service = HueInterfaceController().getAvailableLightsConnected()
