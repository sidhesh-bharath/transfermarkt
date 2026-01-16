import os
import db
import auth
import shutil
import atexit

atexit.register(auth.update_session)

def clear_screen(user_name=None, text=None):
    width, height = shutil.get_terminal_size()
    
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

    if text and user_name:
        print(f"{user_name} | TRANSFERMARKT | {text}".center(width))
    elif text and not user_name:
        print(f"TRANSFERMARKT | {text}".center(width))
    elif not text and user_name:
        print(f"{user_name} | TRANSFERMARKT".center(width))
    else:
        print(f"TRANSFERMARKT".center(width))
    
    print()

def do_action(user_name):
    clear_screen(user_name, "Dashboard")
    action = int(input("""1. View Market
2. Buy Players from Inventory
3. Make Transactions
4. Exit
5. Logout and Exit

Choose your action: """))

    if action == 1:
        clear_screen(user_name, "Markt")
        player_data = db.get_players()
        print(player_data)
        input()
    elif action == 4:
        clear_screen(user_name, "Exitted")
        exit()
    elif action == 5:
        auth.user_logout()
        clear_screen(user_name, "Logged Out")
        exit()
    
    do_action(user_name)

if auth.load_from_session()[0]:
    status, user = auth.load_from_session()
    user_name = db.find_user(user)[0]["name"]
else:
    clear_screen("Login")
    option = int(input("""1. Create account
2. Sign In

Choose your action: """))

    if option == 1:
        clear_screen("Sign Up")
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        user = auth.user_sign_up(email, password)
        user_name = db.find_user(user)[0]["name"]

        print()
        input(f"Signed up as {user_name} - {email}")
    else:
        clear_screen("Sign In")
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        
        try:
            user = auth.user_sign_in(email, password)
            user_name = db.find_user(user)[0]["name"]

            print()
            input(f"Signed in as {user_name} - {email}...")
        except:
            print()
            input("Invalid credentials entered...")
            exit()

do_action(user_name)