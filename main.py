import auth

if auth.load_from_session():
    auth.load_from_session()
else:
    option = int("""1. Create account
    2. Sign In""")

    if option == 1:
        auth.user_sign_up()
    else:
        auth.user_sign_in()
