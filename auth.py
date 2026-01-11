import os
import json
import time
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("DB_PROJECT_URL")
key = os.getenv("DB_API_KEY")
supabase = create_client(url, key)

SESSION_FILE = "session.json"

def save_session(session):
    if session:
        with open(SESSION_FILE, "w") as f:
            json.dump({
                "access_token": session.access_token,
                "refresh_token": session.refresh_token,
            }, f)

def load_session_from_file():
    if os.path.exists(SESSION_FILE) and os.path.getsize(SESSION_FILE) > 0:
        try:
            with open(SESSION_FILE, "r") as f:
                data = json.load(f)
                res = supabase.auth.set_session(data["access_token"], data["refresh_token"])
                return res.session
        except:
            return None
    return None

def get_active_session():
    session = supabase.auth.get_session()
    if not session:
        session = load_session_from_file()
    if session and session.expires_at < time.time():
        try:
            res = supabase.auth.refresh_session()
            session = res.session
            save_session(session)
        except:
            return None
    return session

def sign_up_user(email, password):
    session = get_active_session()
    if session: return session.user, session
    res = supabase.auth.sign_up({"email": email, "password": password})
    if res.session: save_session(res.session)
    return res.user, res.session

def sign_in_user(email, password):
    session = get_active_session()
    if session: return session.user, session
    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
    if res.session: save_session(res.session)
    return res.user, res.session

def logout_user():
    supabase.auth.sign_out()
    if os.path.exists(SESSION_FILE): os.remove(SESSION_FILE)

def get_user_info():
    get_active_session()
    res = supabase.auth.get_user()
    return res.user