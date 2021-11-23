import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def initialize_database():
    database = "comp3700.db"

    companies_table = """ CREATE TABLE IF NOT EXISTS companies (
                                        id integer PRIMARY KEY,
                                        company_name text NOT NULL,
                                        ticker text NOT NULL,
                                        total_shares double,
                                        outstanding_shares double,
                                        initial_share_price double,
                                        current_share_price double
                                    ); """

    users_table = """CREATE TABLE IF NOT EXISTS users (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    account_balance double,
                                    account_type text
                                );"""

    portfolio_table = """CREATE TABLE IF NOT EXISTS portfolio (
                                    id integer PRIMARY KEY,
                                    portfolio_id integer,
                                    company_name text NOT NULL,
                                    company_ticker text NOT NULL,
                                    share_count double,
                                    FOREIGN KEY (portfolio_id) REFERENCES users (id)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create companies table
        create_table(conn, companies_table)

        # create users table
        create_table(conn, users_table)

        # create portfolio table
        create_table(conn, portfolio_table)
    else:
        print("Error! cannot create the database connection.")