def create_company(conn, company):
    """
    Create a new company into the companies table
    :param conn:
    :param company_name:
    :param ticker:
    :param total_shares:
    :param outstanding_shares: initializes to zero
    :param initial_share_price:
    :param current_share_price: initializes to initial_share_price
    :return: id
    """
    sql = ''' INSERT INTO companies(company_name,ticker,total_shares,outstanding_shares,initial_share_price,current_share_price)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, company)
    conn.commit()
    return cur.lastrowid

def create_user(conn, user):
    """
    Create a new user into the users table
    :param conn:
    :param name:
    :param account_balance:
    :param account_type: (individual or organization)
    :return: id
    """
    sql = ''' INSERT INTO users(name, account_balance, account_type)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid

def create_portfolio_record(conn, details):
    """
    Create a new user into the users table
    :param portfolio_id: related to the user_id
    :param company_name:
    :param company_ticker:
    :param share_count:
    :return: id
    """
    sql = ''' INSERT INTO portfolio(portfolio_id, company_name, company_ticker, share_count)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, details)
    conn.commit()
    return cur.lastrowid