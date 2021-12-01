class StockExchange:
	def __init__(self, companies):
		self.companies = companies

	def getCompany(self, ticker):
		for company in self.companies:
			if company.ticker == ticker:
				return company

	def varyStockPrices(self, maxPercent):
		pass