from ..database.db_functions import create_company
from ..database.initialize_db import create_connection

def company_exists(conn, ticker):
    cur = conn.cursor()
    cur.execute(
        '''SELECT EXISTS(SELECT 1 FROM companies WHERE ticker='{}')'''.format(ticker)
        )
    return cur.fetchone()[0]

def validate_ipo():

    database = "comp3700.db"
    conn = create_connection(database)

    print('\n__________IPO Validation Form__________\n')
    company_name = input('Company Name: ')
    ticker = input('Company Ticker: ')
    if company_exists(conn, ticker) == 1:
        print('\nThis Company is Already Public!\nPlease enter a unique Ticker.\n')
        validate_ipo()
    else:
        total_shares = input('Total Shares: ')
        outstanding_shares = 0
        initial_share_price = input('Initial Share Price ($USD): ')
        current_share_price = initial_share_price
        company_details = (company_name,ticker,total_shares,outstanding_shares,initial_share_price,current_share_price)
        create_company(conn, company_details)
        print('You have successfully taken your company public, congratulations!')
    
