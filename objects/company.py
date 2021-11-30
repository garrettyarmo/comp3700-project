import json

class Company:
    name: str
    ticker:str
    total_shares: int
    outstanding_shares: int
    initial_price: float
    current_price: float

    def setName(self):
        _name = input('Enter Company Name: ')
        if _name in self.listRecords("name"):
            print('This name is taken, please try again.\n')
            self.setName()
        else:
            self.name = _name

    def setTicker(self):
        _ticker = input('Enter Company Ticker: ').upper()
        if _ticker in self.listRecords("ticker"):
            print('This ticker is not available, please try again.')
            self.setTicker()
        else:
            self.ticker = _ticker

    def setShares(self):
        _total_shares = int(input('How many total shares?: '))
        if _total_shares < 1:
            print('Total shares must be greater than zero.')
            self.setShares()
        else:
            self.total_shares = _total_shares
            self.outstanding_shares = 0

    def setPrice(self):
        _initial_price = float(input('Enter Initial Price per Share ($USD): '))
        if _initial_price <= 0:
            print('Initial share price must be greater than zero')
            self.setPrice()
        else:
            self.initial_price = _initial_price
            self.current_price = self.initial_price

    def requestIPO(self):
        token = True
        public_ticker_list = self.listRecords("ticker")
        if self.ticker in public_ticker_list:
            print('This company is already listed publicly')
            token = False
            return token
        else:
            return token

    def submitIPO(self):
        try:
            with open("./companies.json", "r") as file:
                data = json.load(file)

            data["companies"].append(self.__dict__)
        
            with open("./companies.json", "w") as file:
                json.dump(data, file, indent=4)
            
            print('Company Successfully Listed\n')
        except Exception as e:
            print(e)

    def listRecords(self, columnName):
        with open("./companies.json", "r") as file:
            data = json.load(file)
            
        list = []
        for company in data["companies"]:
            list.append(company["{}".format(columnName)])
        
        return list

    def getCompany(self, ticker:str):
        if ticker in self.listRecords("ticker"):
            with open("./companies.json", "r") as file:
                data = json.load(file)
            for company in data["companies"]:
                if company["ticker"] == ticker:
                    name = company["name"]
                    total_shares = company["total_shares"]
                    outstanding_shares = company["outstanding_shares"]
                    current_price = company["current_price"]
        
                    return {
                        "name": name,
                        "ticker": ticker,
                        "total_shares": total_shares,
                        "outstanding_shares": outstanding_shares,
                        "current_price": current_price
                    }
        else:
            print('Ticker does not exist')
        

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
            
        
        
        

