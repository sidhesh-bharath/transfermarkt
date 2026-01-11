import os
from dotenv import load_dotenv
from auth import supabase, get_active_session

load_dotenv()

def create_player(name: str, position: str=None, rating: int=None, nationality: str=None, club: str=None, value: int=None):
    session = get_active_session()
    if not session: return None
    
    supabase.table("players").insert({
        "name": name,
        "position": position,
        "rating": rating,
        "nationality": nationality,
        "club": club,
        "value": value,
        "auth_id": session.user.id
    }).execute()

def get_players():
    get_active_session()
    players = supabase.table("players").select("*").execute()
    return players.data

def find_player(name):
    get_active_session()
    player = supabase.table("players").select().eq("name", name).execute()
    return player.data

def update_player(name, **kwargs):
    get_active_session()
    update_data = {k: v for k, v in kwargs.items() if v is not None}
    supabase.table("players").update(update_data).eq("name", name).execute()

def delete_player(name):
    get_active_session()
    supabase.table("players").delete().eq("name", name).execute()

def create_user(name: str, currency: int=0, players_owned: list=None):
    session = get_active_session()
    if not session: return None
    
    supabase.table("users").insert({
        "auth_id": session.user.id,
        "name": name,
        "currency": currency,
        "players_owned": players_owned or [],
    }).execute()

def get_users():
    get_active_session()
    users = supabase.table("users").select("*").execute()
    return users.data

def find_user(name):
    get_active_session()
    user = supabase.table("users").select().eq("name", name).execute()
    return user.data

def update_user(name: str, currency: int=None, players_owned: list=None):
    session = get_active_session()
    if not session: return None
    
    update_data = {"name": name}
    if currency is not None: update_data["currency"] = currency
    if players_owned is not None: update_data["players_owned"] = players_owned
    
    supabase.table("users").update(update_data).eq("auth_id", session.user.id).execute()

def delete_user():
    session = get_active_session()
    if not session: return None
    supabase.table("users").delete().eq("auth_id", session.user.id).execute()