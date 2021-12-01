import json
from os.path import exists

from .stock_exchange import StockExchange
from .company import Company
from .user import User
from .position import Position
from .portfolio import Portfolio

class DataProviderJSON():
	def __init__(self, userFilename, exchangeFilename):
		self.userFilename = userFilename
		self.exchangeFilename = exchangeFilename

		if exists(userFilename):
			with open(userFilename, 'r') as file:
				self.userData = json.load(file)
		else:
			self.userData = {"users": {}}

		if exists(exchangeFilename):
			with open(exchangeFilename, 'r') as file:
				self.exchangeData = json.load(file)
		else:
			self.exchangeData = {"companies": []}

	def save(self):
		with open(self.userFilename, 'w') as file:
			json.dump(self.userData, file, indent=4)
		with open(self.exchangeFilename, 'w') as file:
			json.dump(self.exchangeData, file, indent=4)

	#There may be a simpler way to serialize this to JSON. Pickle is also an option
	def loadUser(self, name):
		if not name in self.userData["users"]:
			return None

		userDict = self.userData["users"][name]
		positions = [Position(**positionDict) for positionDict in userDict["portfolio"]["positions"]]
		return User(name, userDict["balance"], Portfolio(positions))

	def updateUser(self, user):
		positions = [position.__dict__ for position in user.portfolio.positions]
		userDict = {"balance": user.balance, "portfolio": {"positions": positions}}
		self.userData["users"][user.name] = userDict

	def getUserNameList(self):
		return self.userData["users"].keys()

	def loadStockExchange(self):
		return StockExchange([Company(**companyDict) for companyDict in self.exchangeData["companies"]])

	def updateStockExchange(self, stockExchange):
		companies = [company.__dict__ for company in stockExchange.companies]
		self.exchangeData["companies"] = companies