import os
import json
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("DB_PROJECT_URL")
SUPABASE_ANON_KEY = os.getenv("DB_API_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def save_session(access_token, refresh_token):
    session_data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

    with open("session.json", "w") as session_file:
        json.dump(session_data, session_file, indent=4)

def load_from_session():
    if os.path.exists("session.json"):
        with open("session.json", "r") as session_file:
            session_contents = session_file.read()
            if not session_contents:
                return False
            else:
                session_data = json.loads(session_contents)
                supabase.auth.set_session(session_data["access_token"], session_data["refresh_token"])
                
                return True
    else:
        return False

def user_sign_up(email, password):
    response = supabase.auth.sign_up({
    "email" :email,
    "password": password,
})
    save_session(response.session.access_token, response.session.refresh_token)

def user_sign_in(email, password):
    if not load_from_session():
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })

        save_session(response.session.access_token, response.session.refresh_token)

    print(f"Logged in successfully as {email}")

def user_logout():
    supabase.auth.sign_out()
    if os.path.exists("session.json"): 
        os.remove("session.json")
    print("Logged out successfully")

session = user_sign_in("sidheshbharath21@gmail.com", "Sidhesh@2011")