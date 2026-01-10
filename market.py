import db
from time import sleep
from random import randrange

def calc_new_value(value):
    scope = value / 10
    ceil = int(value + scope)
    floor = int(value - scope)

    new_value = randrange(floor, ceil)
    return int(new_value)

def update_values():
    players = db.get_players()
    for player in players:
        value = player["value"]
        new_value = calc_new_value(value)
        db.update_player(player["name"], player["rating"], player["nationality"], player["club"], new_value)

open = True
while open:
    update_values()
    sleep(60)