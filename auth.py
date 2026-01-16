import db
import os
import keyring
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("DB_PROJECT_URL")
SUPABASE_ANON_KEY = os.getenv("DB_API_KEY")
KEYRING_SERVICE = "transfermarkt"

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def save_session(access_token, refresh_token):
    keyring.set_password(KEYRING_SERVICE, "access_token", access_token)
    keyring.set_password(KEYRING_SERVICE, "refresh_token", refresh_token)

def update_session():
    if supabase.auth.get_session():
        session = supabase.auth.get_session()
        save_session(session.access_token, session.refresh_token)

def load_from_session():
    if keyring.get_password(KEYRING_SERVICE, "access_token") and keyring.get_password(KEYRING_SERVICE, "refresh_token"):
        access_token = keyring.get_password(KEYRING_SERVICE, "access_token")
        refresh_token = keyring.get_password(KEYRING_SERVICE, "refresh_token")
        
        session = supabase.auth.set_session(access_token, refresh_token)

        user = session.user

        return True, user.id
    else:
        False, None

def user_sign_up(email, password):
    response = supabase.auth.sign_up({
        "email" :email,
        "password": password,
    })

    print()
    input("Press enter after confirming your Email... ")
    
    # if not verified keep checking and waiting for enter somehow
    response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password,
    })

    print()
    user_name = input("Enter a username: ")
    db.create_user(response.user.id, user_name)

    save_session(response.session.access_token, response.session.refresh_token)

    return response.user.id

def user_sign_in(email, password):
    if not load_from_session()[0]:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })

        save_session(response.session.access_token, response.session.refresh_token)

        return response.user.id

def user_logout():
    supabase.auth.sign_out()
    if keyring.get_password(KEYRING_SERVICE, "access_token") and keyring.get_password(KEYRING_SERVICE, "refresh_token"):
        keyring.delete_password(KEYRING_SERVICE, "access_token")
        keyring.delete_password(KEYRING_SERVICE, "refresh_token")

    print()
    input("Logged out successfully...")