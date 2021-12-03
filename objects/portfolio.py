from .position import Position

class Portfolio:
	#positions: array of Position objects or None
	def __init__(self, positions = None):
		self.positions = [] if positions is None else positions

	#quantity can be a positive or negative integer. Position is created if it doesn't already exist
	def adjustPosition(self, ticker, delta):
		for position in self.positions:
			if position.ticker == ticker:
				position.shareCount += delta
				if position.shareCount == 0:
					self.positions = [x for x in self.positions if x.shareCount != 0]
				return

		self.positions.append(Position(delta, ticker))

	def getOwnedQuantity(self, ticker):
		for position in self.positions:
			if position.ticker == ticker:
				return position.shareCount

		return 0

	def getTotalValue(self, stockExchange):
		total = 0.0
		for position in self.positions:
			company = stockExchange.getCompany(position.ticker)
			total += company.current_price * position.shareCount

		return total