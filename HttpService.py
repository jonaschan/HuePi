import requests
import json
import ipaddress

class HueInterfaceController:
	"""
	Interfaces with the Hue Bridge.
	"""	
	def getHueIpAddress(self):
		response = requests.get("https://discovery.meethue.com/")
		return response.json()[0]["internalipaddress"]
		
	def getUserToken(self):
		return "token"
		
	def createNewAccount(self):
		ip = self.getHueIpAddress()
		
		accountUrl = "https://{}/api/".format(ip)
		print(accountUrl)
		accountMessageJson = {
			'devicetype': 'jonasTest'
		}
		
		response = requests.post(accountUrl, json = accountMessageJson, verify=False)
		print(response)
	

service = HueInterfaceController().createNewAccount()
