from abc import ABC, abstractmethod

#Abstract base class that allows different data sources to be implemented (JSON, sqlite, etc)
#Call save() to permanently save the results of any operations
class DataProvider(ABC):
	@abstractmethod
	def save(self):
		pass

	#Return User object or None if does not exist
	@abstractmethod
	def loadUser(self, name):
		pass

	#Update or create new user
	@abstractmethod
	def updateUser(self, user):
		pass

	#Returns an array of strings
	@abstractmethod
	def getUserNameList(self):
		pass

	#Creates an empty StockExchange if one doesn't exist already
	@abstractmethod
	def loadStockExchange(self):
		pass

	@abstractmethod
	def updateStockExchange(self, stockExchange):
		pass