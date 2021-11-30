from objects.company import Company, viewPublicCompanies
from objects.user import User

print('\n______________Welcome to Team 17\'s Stock Brokerage System______________\n')

valid_input = False
while not valid_input:

    login_type = input('Enter "company" to take a company public\nEnter "user" to login or sign up\n')

    if login_type.lower() == 'company':
        new_company = Company()
        new_company.setName()
        new_company.setTicker()
        new_company.setShares()
        new_company.setPrice()
        ipo_token = new_company.requestIPO()
        if ipo_token:
            new_company.submitIPO()

    elif login_type.lower() == 'user':
        login_or_signup = input('Enter "login" to login to an existing account: \nEnter "signup" to create an account: \n')
        if login_or_signup.lower() == 'signup':
            user = User()
            user.setID()
            user.setName()
            user.setBalance()
            user.saveNewUser()
            users = user.listRecords("name")
            valid_input = True
            
        elif login_or_signup.lower() == 'login':
            user = User()
            user.populate_exisiting_user()
            print('\n_____Welcome back {}_____\n'.format(user.name))
            valid_input = True
        else:
            valid_input = False
            
valid_input = False
while not valid_input:
    print('__________________________________')
    print('_______/\______Menu______/\_______')
    action = input('Enter "0" to view your portfolio\nEnter "1" to buy shares\nEnter "2" to sell shares\nEnter "exit" to leave the program\n__________________________________\n')
    if action.lower() == '0':
        user.viewPortfolio()
    elif action.lower() == '1':
        viewPublicCompanies()
        user.buyShares()
    elif action.lower() == '2':
        user.viewPortfolio()
        user.sellShares()
    elif action.lower() == 'exit':
        print('Goodbye!')
        valid_input = True
    else:
        print('Invalid Input: please try again.\n')

    