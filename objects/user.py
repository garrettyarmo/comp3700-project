class User:
	def __init__(self, name, balance, portfolio):
		#self.id: str
		self.name = name
		self.balance = balance
		self.portfolio = portfolio

	#Returns a string
	def generateReport(self, stockExchange):
		output = 'Portfolio Summary for User {}\n'.format(self.name)
		output += 'Cash available to trade: ${}\n'.format(self.balance)
		output += 'Portfolio net worth: ${}\n\n'.format(self.portfolio.getTotalValue(stockExchange))
		output += "{:<14} {:<20} {:<12} {:<10}\n".format('# of Shares','Company Name', 'Ticker', 'Stock Price')
		output += '-----------------------------------------------------------------\n'
		for position in self.portfolio.positions:
			company = stockExchange.getCompany(position.ticker)
			output += "{:<14} {:<20} {:<12} ${:<10}\n".format(position.shareCount, company.name, position.ticker, company.current_price)
		return output
