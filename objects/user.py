import json
from .company import Company

class User:
	def __init__(self, name, balance, portfolio):
		#self.id: str
		self.name = name
		self.balance = balance
		self.portfolio = portfolio

	#Returns a string
	def generateReport(self):
		output = 'Portfolio Summary for User Number: {}\n'.format(self.name)
		output += 'Cash available to trade: ${}\n\n'.format(self.balance)
		output += "{:<14} {:<20} {:<12} {:<10}".format('# of Shares','Company Name', 'Ticker', 'Purchase Price')
		output += '-----------------------------------------------------------------\n'
		for position in self.portfolio.positions:
			output += "{:<14} {:<20} {:<12} ${:<10}\n".format(position["number_of_shares"], position["company_name"], position["ticker"], position["purchase_price"])
