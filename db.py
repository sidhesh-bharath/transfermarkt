import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("DB_PROJECT_URL")
key = os.getenv("DB_API_KEY")
supabase = create_client(url, key)

def create_player(name: str, position: str=None, rating: int=None, nationality: str=None, club: str=None, value: int=None, inventory: int=10):
    supabase.table("players").insert({
        "name": name,
        "position": position,
        "rating": rating,
        "nationality": nationality,
        "club": club,
        "value": value,
        "inventory": inventory,
    }).execute()

def get_players():
    players = supabase.table("players").select("*").execute()
    return players.data

def find_player(name: str):
    player = supabase.table("players").select().eq("name", name).execute()
    return player.data

def update_player(name: str, **kwargs):
    update_data = {k: v for k, v in kwargs.items() if v is not None}
    supabase.table("players").update(update_data).eq("name", name).execute()

def delete_player(name: str):
    supabase.table("players").delete().eq("name", name).execute()

def create_user(auth_id: str, name: str=None, currency: int=0, players_owned: list=None):
    supabase.table("users").insert({
        "auth_id": auth_id,
        "name": name,
        "currency": currency,
        "players_owned": players_owned or [],
    }).execute()

def get_users():
    users = supabase.table("users").select("*").execute()
    return users.data

def find_user(auth_id: str):
    user = supabase.table("users").select().eq("auth_id", auth_id).execute()
    return user.data

def update_user(auth_id: str, name: str=None, currency: int=None, players_owned: list=None):
    update_data = {"name": name}
    if currency is not None: update_data["currency"] = currency
    if players_owned is not None: update_data["players_owned"] = players_owned
    
    supabase.table("users").update(update_data).eq("auth_id", auth_id).execute()

def delete_user(auth_id):
    supabase.table("users").delete().eq("auth_id", auth_id).execute()