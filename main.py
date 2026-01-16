import os
import db
import auth
import shutil
import atexit

atexit.register(auth.update_session)

def clear_screen(text=None):
    width, height = shutil.get_terminal_size()
    
    os.system("cls")
    if text:
        print(f"TRANSFERMARKT | {text}".center(width))
    else:
        # add the actual username functionality here if agreed upon
        print(f"TRANSFERMARKT".center(width))
    
    print()

def do_action():
    clear_screen()
    action = int(input("""1. View Market
2. Buy Players from Inventory
3. Make Transactions
4. Exit
5. Logout and Exit

Choose your action: """))

    if action == 1:
        clear_screen("MARKET")
        player_data = db.get_players()
        print(player_data)
        input()
    elif action == 4:
        clear_screen("EXITTED")
        exit()
    elif action == 5:
        auth.user_logout()
        clear_screen("LOGGED OUT")
        exit()
    
    do_action()

if auth.load_from_session():
    auth.load_from_session()
else:
    clear_screen("LOGIN")
    option = int(input("""1. Create account
2. Sign In

Choose your action: """))

    if option == 1:
        clear_screen("SIGN UP")
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        auth.user_sign_up()
    else:
        clear_screen("SIGN IN")
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        auth.user_sign_in(email, password)

do_action()