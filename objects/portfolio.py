class Portfolio:
	#positions: array of Position objects or None
	def __init__(self, positions):
		self.positions = [] if positions is None else positions

	#quantity can be a positive or negative integer
	def adjustPosition(self, ticker, delta):
		for position in positions:
			if position.ticker == ticker:
				position.shareCount += delta
				break

	def getOwnedQuantity(self, ticker):
		for position in positions:
			if position.ticker == ticker:
				return position.shareCount

		return 0