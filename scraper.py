import requests
from bs4 import BeautifulSoup
import db
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

START_PAGE = 1
END_PAGE = 2
MAX_WORKERS = 10
LINKS_PER_PAGE = 100

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}
session.headers.update(headers)

stats_lock = Lock()
successful_scrapes = 0

def parse_player_page(link):
    global successful_scrapes
    try:
        response = session.get(link, timeout=15)
        soup_1 = BeautifulSoup(response.text, "lxml")

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

        spans = soup_1.find_all(
            "span", class_="Typography_typography__BbhVA generated_body2__1oQ_U Typography_margins__Rl7Bs"
        )
        
        if len(spans) < 8: return 

        nation = spans[5].get_text(strip=True)
        league = spans[6].get_text(strip=True)
        club = spans[7].get_text(strip=True)

        club_mapping = {"Lombardia FC": "Inter Milan", "Milano FC": "AC Milan"}
        club = club_mapping.get(club, club)

        data_ovr = soup_1.find_all("h4", class_="Typography_typography__BbhVA generated_headline5__Qi8nQ Typography_margins__Rl7Bs")
        ovr = int(data_ovr[0].get_text(strip=True).split()[-1])

        if not db.find_player(full_name):
            db.create_player(full_name, final_pos[0], ovr, nation, club, None)
            
        with stats_lock:
            successful_scrapes += 1

    except Exception:
        pass

def get_data():
    player_links = []
    
    scrape_start = time.perf_counter()
    
    for page_no in range(START_PAGE, END_PAGE + 1):
        main_url = f"https://www.ea.com/games/ea-sports-fc/ratings?gender=0&page={page_no}"
        try:
            response = session.get(main_url, timeout=15)
            soup = BeautifulSoup(response.text, "lxml")
            counter = 0
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]
                if "/games/ea-sports-fc/ratings/player-ratings/" in href:
                    full_url = "https://www.ea.com" + href
                    if full_url not in player_links:
                        player_links.append(full_url)
                        counter += 1
                if counter >= LINKS_PER_PAGE:
                    break
        except Exception:
            continue

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(parse_player_page, player_links)
    
    scrape_end = time.perf_counter()
    total_time = scrape_end - scrape_start

    print("\n" + "="*40)
    print("           SCRAPER STATS")
    print("="*40)
    print(f"Total Successful Records: {successful_scrapes}")
    print(f"Total Time Taken:         {total_time:.2f}s")
    
    if successful_scrapes > 0:
        avg_time = total_time / successful_scrapes
        print(f"Avg Time Per Record:      {avg_time:.4f}s")
    else:
        print("No records were successfully scraped.")
    print("="*40)

if __name__ == "__main__":
    get_data()