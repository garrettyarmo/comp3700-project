from ..database.db_functions import create_user, create_portfolio_record
from ..database.initialize_db import create_connection
from .ipo_interface import company_exists

def user_exists(conn, id):
    cur = conn.cursor()
    cur.execute(
        '''SELECT EXISTS(SELECT 1 FROM companies WHERE id ='{}')'''.format(id)
        )
    return cur.fetchone()[0]

def position_exists(conn, user_id, ticker):
    cur = conn.cursor()
    cur.execute(
        '''SELECT EXISTS(SELECT 1 FROM portfolio WHERE company_ticker = '{}' AND portfolio_id = '{}')'''.format(ticker, user_id)
        )
    return cur.fetchone()[0]

def create_new_user():
    database = "comp3700.db"
    conn = create_connection(database)

    print('\n__________New User Registration Form__________\n')
    name = input('Full Name: ')
    account_balance = input('Enter amount to be deposited ($USD): ')
    account_type = input('Enter "i" if you\'re an indivdual user\nEnter "o" if you represent an organization: ')
    if account_type.lower() == 'i':
        account_type = 'individual'
    elif account_type.lower() == 'o':
        account_type = 'organization'
    else:
        print('Invalid Input')
        create_new_user()

    user_details = (name,account_balance,account_type)
    user = create_user(conn, user_details)
    print('\nYour account id is {}\n'.format(user))
    return user

def login_existing_user():
    database = "comp3700.db"
    conn = create_connection(database)

    _user_id = input('Enter your user ID: ')

    if user_exists(conn, _user_id) == 1:
        curr = conn.cursor()
        current_user_row = curr.execute('SELECT name FROM users WHERE id={}'.format(_user_id))
        for row in current_user_row:
            print('\nWelcome back {}!'.format(row[0]))
        return _user_id
    else:
        print('\nThis user id does not exist.\n')

def view_public_companies():
    database = "comp3700.db"
    conn = create_connection(database)
    curr = conn.cursor()
    public_companies = curr.execute('SELECT * FROM companies')
    print('\nAll Current Public Companies\n')
    print("{:<23} {:<8} {:<8}".format('Company Name','Ticker','Current Price'))
    print('-----------------------------------------------------')
    for company in public_companies:
        print("{:<23} {:<8} ${:<8}".format(company[1], company[2], company[6]))

def buy_shares(user_id):
    database = "comp3700.db"
    conn = create_connection(database)
    curr1 = conn.cursor()
    curr2 = conn.cursor()
    curr3 = conn.cursor()
    company_ticker = input('Enter Ticker to buy: ')
    company_ticker = company_ticker.upper()

    if company_exists(conn, company_ticker) == 0:
        print('This company does not exist!\n')
        buy_shares(user_id)

    company = curr1.execute('SELECT * FROM companies WHERE ticker = \'{}\''.format(company_ticker)).fetchone()
    company_name = company[1]
    outstanding_shares = company[4]
    total_shares = company[3]
    available_shares = total_shares - outstanding_shares
    share_price = company[6]

    user = curr2.execute('SELECT * FROM users WHERE id = {}'.format(user_id)).fetchone()
    user_balance = user[2]
    purchase_quantity = float(input('Enter share quantity: '))
    purchase_price = purchase_quantity * share_price
    if purchase_quantity > available_shares:
        print('Your requested quantity exceeds the {} available shares'.format(available_shares))
        buy_shares(user_id)
    elif purchase_price > user_balance:
        print('This purchase exceeds your account balance of {}.'.format(user_balance))
        buy_shares(user_id)

    if position_exists(conn, user_id, company_ticker) == 1:
        print('Position Exists...')
        outstanding_shares = outstanding_shares + purchase_quantity
        curr3.execute('UPDATE portfolio SET share_count = share_count + ? WHERE company_ticker = ? AND portfolio_id = ?',
        (purchase_quantity, company_ticker, user_id))
        conn.commit()

    else:
        print('position does not exist...')
        details = (user_id, company_name, company_ticker, purchase_quantity)
        outstanding_shares = outstanding_shares + purchase_quantity
        create_portfolio_record(conn, details)
        
    curr3.execute('UPDATE companies SET outstanding_shares = ? WHERE ticker = ?',
        (outstanding_shares, company_ticker))
    conn.commit()

    new_balance = user_balance - purchase_price
    curr3.execute('UPDATE users SET account_balance = ? WHERE id = ?',
        (new_balance, user_id))
    conn.commit()

    print('Successful purchase: You bought {} shares of {} stock for ${}!'.format(purchase_quantity, company_name, purchase_price))

def sell_shares(user_id):
    database = "comp3700.db"
    conn = create_connection(database)
    curr = conn.cursor()
    company_ticker = input('Enter Ticker to sell: ')
    company_ticker = company_ticker.upper()

    if position_exists(conn, company_ticker) == 0:
        print('You do not own any shares of {}!\n'.format(company_ticker))
        sell_shares(user_id)

    position = curr.execute('SELECT * FROM portfolio WHERE ticker = \'{}\' AND portfolio_id = {}'.format(company_ticker, user_id)).fetchone()
    for position in position:
        print(position)

def handle_user_transactions(user_id):
    action = input('Buy or Sell?: ')
    if action.lower() == 'buy':
        buy_shares(user_id) 
    elif action.lower() == 'sell':
        sell_shares(user_id)

def view_portfolio(user_id):
    
    database = "comp3700.db"
    conn = create_connection(database)
    curr = conn.cursor()

    positions = curr.execute('SELECT * FROM portfolio WHERE id={}'.format(user_id))
    print('\nPortfolio Summary for User Number: {}\n'.format(user_id))
    print("{:<10} {:<20} {:<8}".format('# of Shares','Company Name', 'Ticker'))
    print('-----------------------------------------------------')
    for position in positions:
        print("{:<10} {:<20} ${:<8}".format(position[4], position[2], position[3]))