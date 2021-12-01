import json

class Company:
	def __init__(self, name, ticker, total_shares, available_shares, initial_price, current_price):
		self.name = name
		self.ticker = ticker
		self.total_shares = total_shares
		self.available_shares = available_shares
		self.initial_price = initial_price
		self.current_price = current_price


def viewPublicCompanies():
	with open("./companies.json", "r") as file:
		data = json.load(file)

	print('\nAll Current Public Companies\n')
	print("{:<20} {:<8} {:<16} {:<8}".format('Company Name','Ticker','Current Price', 'Available Shares'))
	print('---------------------------------------------------------------------')
	for i in data["companies"]:
		available_shares = i["total_shares"] - i["outstanding_shares"]
		print("{:<20} {:<8} ${:<16} {:<8}".format(i["name"], i["ticker"], i["current_price"], available_shares))
	print('\n')
			
		
		
		

