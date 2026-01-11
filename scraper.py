import requests
from bs4 import BeautifulSoup

def get_data():
    main_url = "https://www.ea.com/games/ea-sports-fc/ratings"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/143.0.0.0 Safari/537.36"
    }
    response = requests.get(main_url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml") 

    player_links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if "/games/ea-sports-fc/ratings/player-ratings/" in href:  
            full_url = "https://www.ea.com" + href 
            if full_url not in player_links:
                player_links.append(full_url)   

    for link in player_links:
        response_1 = requests.get(link, headers=headers)
        soup_1 = BeautifulSoup(response_1.text, "lxml") 

        data_names = soup_1.find_all("span", class_="AthletePage_playerName__WSrAu")
        names = []
        for name_tag in data_names:
            text = name_tag.get_text(strip=True)
            if text not in names:
                names.append(text)
        full_name = " ".join(names)
        print(f"Name:{full_name}")

        data_position = soup_1.find_all(
            "div", class_="Tag_tag__AdaK1 generated_utility19__bAi0N Tag_lg__lL80n Tag_solid__4BJMQ"
        )
        positions = []
        for pos_tag in data_position:
            pos = pos_tag.get_text(strip=True)
            positions.append(pos)
        final_pos = list(set(positions))
        print(f"Postion(s): {final_pos}")
        
        spans = soup_1.find_all("span", class_="Typography_typography__BbhVA generated_body2__1oQ_U Typography_margins__Rl7Bs")
        nation = spans[5].get_text(strip=True)
        club = spans[7].get_text(strip=True)
        print("Nation:", nation)
        print("Club:", club)


get_data()
