import requests
import json
import ipaddress

class HueInterfaceController:
    """
    Interfaces with the Hue Bridge.
    """
    def __init__(self):
        if (self.isConnectedToInternet() == False):
            return
        
        self.token = 'hPKjNr2MNZHYIJVE2PF6RmiSxhXyqcy5IOjOcj8u'
        self.accountUrl = ''
        self.generateBridgeToken = False
        self.fullAccessUrl = self.__getFullAccessUrl()
    
    def isConnectedToInternet(self):
        testUrl = "http://www.google.com/"
        timeoutSeconds = 5
        
        try:
            _ = requests.get(testUrl, timeout=timeoutSeconds)
            return True
        except requests.ConnectionError:
            print("No internet connection! Should ping the display.")
            
        return False
    
    def __getHueIpAddress(self):
        """
        Returns the IP Address of the Hue Bridge
        """
        response = requests.get("https://discovery.meethue.com/")
        return response.json()[0]["internalipaddress"]

    def __createNewAccount(self):
        """
        Returns a token to access the Bridge.
        """
        ip = self.__getHueIpAddress()
        
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
        
    def __getFullAccessUrl(self):
        """
        Returns the full url to access the Bridge.
        """
        if (self.generateBridgeToken):
            self.token = self.__createNewAccount()
            return '{}/api/{}'.format(self.accountUrl, self.token)
        
        return 'http://{}/api/{}'.format(self.__getHueIpAddress(), self.token)
                    
    def getAvailableLightsConnected(self):
        """
        Returns the available lights connected to the Bridge.
        Returns false if the device is not connected to the internet.
        """
        if (self.isConnectedToInternet() == False):
            return;            
        
        url = '{}/lights'.format(self.fullAccessUrl)
        response = requests.get(url)
        
        return len(response.json())
    
    def toggleHueLights(self, lightId, state):
        """
        Toggles the lights according to the light id. Returns true if successful.
        Returns false if the device is not connected to the internet.
        """
        if (self.isConnectedToInternet() == False):
            return;
        
        url = '{}/lights/{}/state'.format(self.fullAccessUrl, lightId)
        
        # Python representation of the dictionary body
        # e.g. returns {'on': True} 
        pythonStateBody = {'on': state}
        
        # Python representation of the dictionary body
        # e.g. returns {'on': true} 
        stateBody = json.dumps(pythonStateBody)
        response = requests.put(url, data = stateBody)
        
        # Get the server response
        responseCode = response.json()[0].keys()
        responseCode = next(iter(responseCode))
        
        return responseCode == 'success'
    
    def changeHueLightBrightness(self, lightId, brightness):
        """
        Change the brightness of the light according to the light id.
        """
        if (self.isConnectedToInternet() == False):
            return;
        
        url = '{}/lights/{}/state'.format(self.fullAccessUrl, lightId)
        
        # Sanity check so the values stay within range
        if (brightness > 254):
            brightness = 254
        elif (brightness < 1):
            brightness = 0
        
        # The Hue Bridge doesn't turn off if value = 0, so we need to explicitly
        # tell this to turn off
        if (brightness > 0):
            state = True
        else:
            state = False
            
        # Python representation of the dictionary body
        # e.g. returns {'on': True} 
        pythonStateBody = {'on': state, 'bri': brightness}
        
        # Python representation of the dictionary body
        # e.g. returns {'on': true} 
        # pythonStateBody = json.dumps(pythonStateBody)
        
        # Make the Http request
        response = requests.put(url, data = pythonStateBody)
        print(response.status_code)
        # Get the server response
        responseCode = response.json()[0].keys()
        responseCode = next(iter(responseCode))
        
        return responseCode == 'success'
    
    def turnOffAllTheLights(self):
        """
        Turns off all the lights.
        """
        if (self.isConnectedToInternet() == False):
            return;
        
        lightCount = self.getAvailableLightsConnected()
        
        for x in range(lightCount):
            self.toggleHueLights(x, False)


service = HueInterfaceController().getAvailableLightsConnected()

