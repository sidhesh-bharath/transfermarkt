from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("DB_PROJECT_URL")
key = os.getenv("DB_API_KEY")

supabase = create_client(url, key)

def insert_player(name: str, rating: int=None, nationality: str=None, club: str=None, value: int=None):
    supabase.table("players").insert(
        {
            "name": name,
            "rating": rating,
            "nationality": nationality,
            "club": club,
            "value": value,
        }
    ).execute()

def get_players():
    players = supabase.table("players").select("*").execute()
    return players.data

def find_player(name):
    player = supabase.table("players").select().eq("name", name).execute()
    return player.data

def update_player(name, rating=None, nationality=None, club=None, value=None):
    supabase.table("players").update(
        {
            "rating": rating,
            "nationality": nationality,
            "club": club,
            "value": value,
        }
    ).eq("name", name).execute()

def delete_player(name):
    supabase.table("players").delete().eq("name", name).execute()

print(find_player("Cristiano Ronaldo"))