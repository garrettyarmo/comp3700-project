class Controller:
	def __init__(self, dataProvider):
		self.dataProvider = dataProvider

		self.stockExchange = dataProvider.loadStockExchange()
		self.loggedInUser = None

	#Todo: consider requestIPO and submitIPO functionality
	#Returns True on success
	def createIPO(self, name, ticker, shareCount, price):
		if self.doesTickerExist(ticker):
			return False

		#Available shares is half of total shares to approximate market activity.
		#Assume the number of unsold shares from the IPO plus the number of shares being resold by other investors is half of the total shares.
		#The other half are shares being held by investors and not available for sale.
		company = Company(name, ticker, shareCount, available_shares = shareCount // 2, initial_price = price, current_price = price)
		self.stockExchange.companies.append(company)

	def createUser(self, name, balance):
		self.loggedInUser = User(name, balance, Portfolio())

	#Returns True on success
	def login(self, userName):
		if self.loggedInUser is not None:
			self.logout()

		self.loggedInUser = self.dataProvider.loadUser(userName)
		return self.loggedInUser is not None

	def logout(self):
		self.dataProvider.updateUser(self.loggedInUser)
		self.loggedInUser = None

	def doesUserNameExist(self, userName):
		return userName in self.dataProvider.getUserNameList()

	def doesTickerExist(self, ticker):
		return any(x for x in self.stockExchange.companies if x.ticker == ticker)

	def doesCompanyNameExist(self, name):
		return any(x for x in self.stockExchange.companies if x.name == name)

	def getUserReport(self):
		return self.loggedInUser.generateReport()

	#Throws a ValueError if transaction cannot be carried out. Returns the purchase cost if successful
	def buyShares(self, ticker, quantity):
		for company in self.stockExchange.companies:
			if company.ticker == ticker:
				if company.available_shares < quantity:
					raise ValueError('Your request exceeds the available shares of {}'.format(company.name))
				cost = quantity * company.current_price
				if cost > self.loggedInUser.balance:
					raise ValueError('The ${} request exceeds your available balance of ${}\nPlease try again.\n'.format(cost, self.loggedInUser.balance))

				company.available_shares -= quantity
				self.loggedInUser.balance -= cost
				self.loggedInUser.portfolio.adjustPosition(ticker, quantity)
				break

	def getOwnedQuantity(self, ticker):
		return self.loggedInUser.portfolio.getOwnedQuantity(ticker)

	#Returns total selling price
	def sellShares(self, ticker, quantity):
		for company in self.stockExchange.companies:
			if company.ticker == ticker:
				cost = quantity * company.current_price

				company.available_shares += quantity
				self.loggedInUser.balance += cost
				self.loggedInUser.portfolio.adjustPosition(ticker, -quantity)
				break

	def notifyExit(self):
		self.dataProvider.updateStockExchange(self.stockExchange)
		self.dataProvider.save()