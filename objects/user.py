import json
from .company import Company

class User:
    id: str
    name: str
    balance: float
    positions = []

    def setID(self):
        _id = input('Enter a unique ID: ')
        if _id in self.listRecords("id"):
            print('This ID already exists, please try again.')
            self.setID()
        else:
            self.id = _id
        
    def setName(self):
        _name = input('Enter Name: ')
        if _name in self.listRecords("name"):
            print('This name is taken, please try again.\n')
            self.setName()
        else:
            self.name = _name
        
    def setBalance(self): 
        _balance = float(input('Enter initial deposit amount ($USD): '))
        if _balance <= 0:
            print('Initial deposit must be greater than zero.')
            self.setBalance()
        else:
            self.balance = _balance

    def saveNewUser(self):
        try:
            self.positions = []
            with open("./users.json", "r") as file:
                data = json.load(file)

            data["users"].append(self.__dict__)
        
            with open("./users.json", "w") as file:
                json.dump(data, file, indent=4)
            
            print('Account Successfully Created\n')
        except Exception as e:
            print(e)

    def listRecords(self, columnName):
        with open("./users.json", "r") as file:
            data = json.load(file)
            
        list = []
        for user in data["users"]:
            list.append(user["{}".format(columnName)])
        
        return list
    
    def listUserRecords(self, columnName):
        with open("./users.json", "r") as file:
            data = json.load(file)
            
        list = []
        for user in data["users"]:
            if user["id"] == self.id:
                if columnName == 'balance':
                    list.append(user["balance"])
                elif columnName == 'positions':
                    for pos in user["positions"]:
                        list.append(pos)
                else:
                    for pos in user["positions"]:
                        list.append(pos["{}".format(columnName)])
        
        return list

    def populate_exisiting_user(self):
        _user_id = input('Enter User ID: ')
        if _user_id in self.listRecords("id"):
            with open("./users.json", "r") as file:
                data = json.load(file)

            for i in data["users"]:
                if i["id"] == _user_id:
                    self.id = i["id"]
                    self.name = i["name"]
                    self.balance = i["balance"]
                    self.positions = i["positions"]
                    return True
        else:
            print('User ID does not exist, please try again.\n')
            return False
        

    def viewPortfolio(self):

        with open("./users.json", "r") as file:
            data = json.load(file)
        for user in data["users"]:
            if user["id"] == self.id:
                print('\nPortfolio Summary for User Number: {}'.format(self.id))
                print('Cash available to trade: ${}\n'.format(user["balance"]))
                print("{:<14} {:<20} {:<12} {:<10}".format('# of Shares','Company Name', 'Ticker', 'Purchase Price'))
                print('-----------------------------------------------------------------')
                for position in user["positions"]:
                    print("{:<14} {:<20} {:<12} ${:<10}".format(position["number_of_shares"], position["company_name"], position["ticker"], position["purchase_price"]))

        print('\n')

    def buyShares(self):

        buy_ticker = input('Enter the ticker of the company you want to purchase: ').upper()

        if buy_ticker in Company().listRecords("ticker"):

            buy_quan = int(input('Enter number of shares to purchase: '))
            buy_company = Company().getCompany(buy_ticker)
            available_shares = buy_company["total_shares"] - buy_company["outstanding_shares"]
            purchase_total = float(buy_quan) * buy_company["current_price"]
            user_balance = float(self.listUserRecords("balance")[0])
            if purchase_total > user_balance:
                print('The ${} request exceeds your available balance of ${}\nPlease try again.\n'.format(purchase_total, user_balance))
                self.buyShares()
            elif buy_quan > available_shares:
                print('Your request exceeds the available shares of {}'.format(buy_company["name"]))
                self.buyShares()
            else:
                self.updatePortfolio(buy_quan, buy_company["name"], buy_ticker, buy_company["current_price"])
                self.updateCompany(buy_ticker, buy_quan)
                
                print('You purchased {} shares of {} for ${}!\n'.format(buy_quan, buy_company["name"], purchase_total))
        else:
            print('This ticker does not exist, please try again.\n')

    def sellShares(self):

        sell_ticker = input('Enter the ticker of the company you want to sell: ').upper()
    
        positions = self.listUserRecords("positions")

        for pos in positions:
            
            if pos["ticker"] == sell_ticker:

                num_owned = pos["number_of_shares"]
                
                print('You own {} shares of {}'.format(num_owned, sell_ticker))

                sell_quan = int(input('Enter number of shares to sell: '))

                if sell_quan > num_owned:
                    print('Your request of {} shares exceeds your {} owned shares\nPlease try again\n'.format(sell_quan, num_owned))
                    self.sellShares()
                else:
                    sell_company = Company().getCompany(sell_ticker)
                    
                    sale_total = float(sell_quan) * sell_company["current_price"]
                    
                    sell_quan = sell_quan * -1

                    self.updatePortfolio(sell_quan, sell_company["name"], sell_ticker, sell_company["current_price"])
                    self.updateCompany(sell_ticker, sell_quan)
                    print('You sold {} shares of {} for ${}!\n'.format(sell_quan * -1, sell_company["name"], sale_total))            
            
                
    def updatePortfolio(self, number_of_shares, company_name, ticker, purchase_price):
        try:
            print('Updating portfolio...')
            new_position = {
                "number_of_shares": number_of_shares,
                "company_name": company_name,
                "ticker": ticker,
                "purchase_price": purchase_price
            }

            with open("./users.json", "r+") as file:
                data = json.load(file)

            for user in data["users"]:
                if user["id"] == self.id:

                    cost = number_of_shares * purchase_price
                    user["balance"] = user["balance"] - cost
                    userOwnerTickers = self.listUserRecords("ticker")
                    
                    if ticker not in userOwnerTickers:
                        user["positions"].append(new_position)
                    else:
                        for pos in user["positions"]:
                            if pos["ticker"] == ticker:
                                if pos["number_of_shares"] == (number_of_shares * -1):
                                    user["positions"].remove(pos)
                                else:
                                    pos["number_of_shares"] = pos["number_of_shares"] + number_of_shares
                else:
                    print('Error Line 153')
            with open("./users.json", "w") as file:
                json.dump(data, file, indent=4)
            
            print('Added portfolio entry\n')
        except Exception as e:
            print(e)

    def updateCompany(self, ticker, number_of_shares):
        try:
            print('Updating companies list...')
            with open("./companies.json", "r+") as file:
                data = json.load(file)

            for company in data["companies"]:
                if company["ticker"] == ticker:
                    company["outstanding_shares"] = company["outstanding_shares"] + number_of_shares

            with open("./companies.json", "w") as file:
                json.dump(data, file, indent=4)
            
            print('Company Updated\n')
        except Exception as e:
            print(e)

