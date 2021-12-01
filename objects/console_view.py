class ConsoleView:
	def __init__(self, controller)
		self.controller = controller

	def run(self):
		print('\n______________Welcome to Team 17\'s Stock Brokerage System______________\n')

		while(true):
			login_type = input('Enter "company" to take a company public\nEnter "user" to login or sign up\nEnter "exit" to leave the program\n')

			if login_type.lower() == 'company':
				self.createIPO()
				ipo_token = new_company.requestIPO()
				if ipo_token:
					new_company.submitIPO()

			elif login_type.lower() == 'user':
				login_or_signup = input('Enter "login" to login to an existing account: \nEnter "signup" to create an account: \n')
				loggedIn = False
				if login_or_signup.lower() == 'signup':
					self.createUser()
					loggedIn = True
			
				elif login_or_signup.lower() == 'login':
					loggedIn = self.login()
				else:
					print('Invalid input\n\n')

				while(loggedIn):
						loggedIn = self.userMenu()

			elif login_type.lower() == 'exit':
				print('Goodbye!')
				self.controller.notifyExit()
				break

	#Returns False if user logged out
	def userMenu(self):
		print('__________________________________')
		print('_______/\______Menu______/\_______')
		action = input('Enter "0" to view your portfolio\nEnter "1" to buy shares\nEnter "2" to sell shares\nEnter "logout" to log out\n__________________________________\n')
		if action.lower() == '0':
			self.printPortfolio()
		elif action.lower() == '1':
			viewPublicCompanies()
			self.buyShares()
		elif action.lower() == '2':
			self.printPortfolio()
			self.sellShares()
		elif action.lower() == 'logout':
			print('Logging out\n')
			self.controller.logout()
			return False
		else:
			print('Invalid Input: please try again.\n')
		return True

	def createIPO(self):
		while(True):
			_name = input('Enter Company Name: ')
			if self.controller.doesCompanyNameExist(_name):
				print('This name is taken, please try again.\n')
			else:
				break

		while(True):
			_ticker = input('Enter Company Ticker: ').upper()
			if self.controller.doesTickerExist(_ticker):
				print('This ticker is not available, please try again.')
			else:
				break

		while(True):
			_total_shares = int(input('How many total shares?: '))
			if _total_shares < 1:
				print('Total shares must be greater than zero.')
			else:
				break

		while(True):
			_initial_price = float(input('Enter Initial Price per Share ($USD): '))
			if _initial_price <= 0:
				print('Initial share price must be greater than zero')
			else:
				break

		self.controller.createIPO(_name, _ticker, _total_shares, _initial_price)
		print('Company Successfully Listed\n')

	def createUser(self):
		while(True):
			_name = input('Enter Name: ')
			if self.controller.doesUserNameExist(_name):
				print('This name is taken, please try again.\n')
			else:
				break

		while(True):
			_balance = float(input('Enter initial deposit amount ($USD): '))
			if _balance <= 0:
				print('Initial deposit must be greater than zero.')
			else:
				break

		self.controller.createUser(_name, _balance)
		print('Account Successfully Created\n')

	def login(self):
		_user_name = input('Enter Name: ')
		loginSuccess = self.controller.login(_user_name);
		if loginSuccess:
			print('\n_____Welcome back {}_____\n'.format(_user_name))
		else:
			print('User name does not exist, please try again.\n')
		return loginSuccess

	def printPortfolio(self):
		print(self.controller.getUserReport())

	def buyShares(self):
		buy_ticker = input('Enter the ticker of the company you want to purchase: ').upper()

		if self.controller.doesTickerExist(buy_ticker):
			while(True):
				buy_quan = int(input('Enter number of shares to purchase: '))
				if buy_quan > 0:
					break
				else
					print('Quantity must be greater than zero.')

			try:
				cost = self.controller.buyShares(buy_ticker, buy_quan)
				print('\nYou purchased {} shares of {} for ${}!\n'.format(buy_quan, buy_ticker, cost))
			except ValueError as err:
				print(err)
				self.buyShares()
		else:
			print('This ticker does not exist, please try again.\n')
			

	def sellShares(self):
		sell_ticker = input('Enter the ticker of the company you want to sell: ').upper()

		if self.controller.doesTickerExist(sell_ticker):
			num_owned = self.controller.getOwnedQuantity(sell_ticker)
			print('You own {} shares of {}'.format(num_owned, sell_ticker))

			sell_quan = int(input('Enter number of shares to sell: '))
			if sell_quan > num_owned:
				print('Your request of {} shares exceeds your {} owned shares\nPlease try again\n'.format(sell_quan, num_owned))
				self.sellShares()
			else:
				sale_total = self.controller.sellShares()
				print('\nYou sold {} shares of {} for ${}!\n'.format(sell_quan, sell_ticker, sale_total))