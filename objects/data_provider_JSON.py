import json
from os.path import exists

class DataProviderJSON():
	def __init__(self, userFilename, exchangeFilename):
		self.userFilename = userFilename
		self.exchangeFilename = exchangeFilename

		if exists(userFilename):
			with open(userFilename, 'r') as file:
				self.userData = json.load(file)
		self.userData = 
		self.companyData = 

	def save(self):

	def loadUser(self, name):

	def updateUser(self, user):

	def getUserNameList(self):

	def loadStockExchange(self):

	def updateStockExchange(self, stockExchange):