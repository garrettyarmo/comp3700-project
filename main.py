from functions.database.initialize_db import initialize_database
from functions.interfaces.ipo_interface import validate_ipo
from functions.interfaces.user_interface import create_new_user, handle_user_transactions, login_existing_user, view_portfolio, view_public_companies

def main():

    initialize_database()

    inp = input('\n\n*************** Hello and Welcome to our Stock Brokerage System ***************\n\nType "User" to login to a user account\nType "Company" to take a company public: ')
    if inp.lower() == 'user':

        user_input = input('\nEnter "login" if you\'re a returning user\nEnter "signup" to create an account\nEnter "exit" to quit: ')
        if user_input.lower() == 'exit':
            pass
        elif user_input.lower() == 'signup':
            user_id = create_new_user()
        elif user_input.lower() == 'login':
            user_id = login_existing_user()
        else:
            print('***Invalid Input***')
            main()
        
        exit_condition = True
        while (exit_condition):
            user_input = input('\nEnter "0" - To View Public Companies\nEnter "1" - To View Portfolio\nEnter "2" - To Initiate a Transaction\n')
            if user_input == '0':
                view_public_companies()
            elif user_input == '1':
                view_portfolio(user_id)
            elif user_input == '2':
                handle_user_transactions(user_id)

    elif inp.lower() == 'company':
        validate_ipo()
        main()
    else:
        print('***Invalid Input***')
        main()

if __name__ == "__main__":
    main()