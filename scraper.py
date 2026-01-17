import requests
from bs4 import BeautifulSoup
import db
import time

def get_data():
    mens_leagues = [
    "Premier League",
    "EFL Championship",
    "EFL League One",
    "EFL League Two",
    "LALIGA EA SPORTS",
    "Bundesliga",
    "2. Bundesliga",
    "3. Liga",
    "Serie A Enilive",
    "Serie B",
    "Ligue 1 McDonald's",
    "Ligue 2",
    "Eredivisie",
    "Liga Portugal",
    "Belgian Pro League",
    "Scottish Premiership",
    "Austrian Bundesliga",
    "Swiss Super League",
    "Allsvenskan",
    "Eliteserien",
    "Ekstraklasa",
    "Super Lig",
    "Russian Premier League",
    "Major League Soccer",
    "MLS Next Pro",
    "Roshn Saudi League",
    "Liga MX",
    "Campeonato Brasileiro Série A",
    "Campeonato Brasileiro Série B",
    "Argentine Primera División",
    "Chilean Primera División",
    "Categoría Primera A",
    "J1 League",
    "K League 1",
    "Chinese Super League",
    "Indian Super League",
    "Persian Gulf Pro League",
    "Egyptian Premier League",
    "South African Premier Division",
    "Botola Pro",
    "Tunisian Ligue Professionnelle 1",
    "A-League",
    "New Zealand Football Championship"
]


    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/143.0.0.0 Safari/537.36"
    }

    player_links = []
    page_no = 1

    while page_no != 11:
        main_url = f"https://www.ea.com/games/ea-sports-fc/ratings?page={page_no}"
        print(f"\nScraping ratings page {page_no}")

        response = requests.get(main_url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        counter = 0
        new_found = False

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]

            if "/games/ea-sports-fc/ratings/player-ratings/" in href:
                full_url = "https://www.ea.com" + href

                if full_url not in player_links:
                    player_links.append(full_url)
                    counter += 1
                    new_found = True

                if counter == 100:
                    break

        if not new_found:
            break

        page_no += 1
        time.sleep(1)

    for link in player_links:
        response_1 = requests.get(link, headers=headers)
        soup_1 = BeautifulSoup(response_1.text, "lxml")

        data_names = soup_1.find_all("span", class_="AthletePage_playerName__WSrAu")
        seen = set()
        names = []
        for tag in data_names:
            text = tag.get_text(strip=True)
            if text not in seen:
                seen.add(text)
                names.append(text)
        full_name = " ".join(names)

        data_position = soup_1.find_all(
            "div", class_="Tag_tag__AdaK1 generated_utility19__bAi0N Tag_lg__lL80n Tag_solid__4BJMQ"
        )
        final_pos = list({tag.get_text(strip=True) for tag in data_position})
        print(f"Position(s): {final_pos}")

        spans = soup_1.find_all(
            "span",
            class_="Typography_typography__BbhVA generated_body2__1oQ_U Typography_margins__Rl7Bs"
        )
        nation = spans[5].get_text(strip=True)
        club = spans[7].get_text(strip=True)
        data_ovr = soup_1.find_all("h4", class_="Typography_typography__BbhVA generated_headline5__Qi8nQ Typography_margins__Rl7Bs")
        ovr_string = data_ovr[0].get_text(strip=True).split()
        ovr = int(ovr_string[-1])
        league = spans[6].get_text(strip=True)
        is_female = False
        if league not in mens_leagues:
            print("Skipping female player")
            continue
        print(f"\nName: {full_name}")
        print("League:", league)
        print("Nation:", nation)
        print("Club:", club)
        print("Overall Rating:", ovr)

        if not db.find_player(full_name):
            db.create_player(full_name, final_pos[0], ovr, nation, club, None)


if __name__ == "__main__":
    get_data()