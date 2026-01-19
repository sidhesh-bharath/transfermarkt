import requests
from bs4 import BeautifulSoup
import db
import time
from concurrent.futures import ThreadPoolExecutor

START_PAGE = 1
END_PAGE = 10
MAX_WORKERS = 20
LINKS_PER_PAGE = 100

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=MAX_WORKERS, pool_maxsize=MAX_WORKERS)
session.mount('https://', adapter)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br"
}
session.headers.update(headers)

def parse_player_page(link):
    try:
        response = session.get(link, timeout=10)
        soup_1 = BeautifulSoup(response.content, "lxml")

        data_names = soup_1.find_all("span", class_="AthletePage_playerName__WSrAu")
        full_name = " ".join(dict.fromkeys([t.get_text(strip=True) for t in data_names]))

        data_position = soup_1.find_all("div", class_="Tag_tag__AdaK1 generated_utility19__bAi0N Tag_lg__lL80n Tag_solid__4BJMQ")
        final_pos = list({tag.get_text(strip=True) for tag in data_position})

        spans = soup_1.find_all("span", class_="Typography_typography__BbhVA generated_body2__1oQ_U Typography_margins__Rl7Bs")
        if len(spans) < 8: return None

        nation = spans[5].get_text(strip=True)
        club = spans[7].get_text(strip=True)
        club = {"Lombardia FC": "Inter Milan", "Milano FC": "AC Milan"}.get(club, club)

        data_ovr = soup_1.find("h4", class_="generated_headline5__Qi8nQ")
        ovr = int(data_ovr.get_text(strip=True).split()[-1]) if data_ovr else 0

        return {
            "name": full_name,
            "pos": final_pos[0] if final_pos else "N/A",
            "ovr": ovr,
            "nation": nation,
            "club": club
        }
    except Exception:
        return None

def get_data():
    player_links = []
    successful_scrapes = 0
    scrape_start = time.perf_counter()
    
    print(f"--- Phase 1: Collecting links from {START_PAGE} to {END_PAGE} ---")
    for page_no in range(START_PAGE, END_PAGE + 1):
        main_url = f"https://www.ea.com/games/ea-sports-fc/ratings?gender=0&page={page_no}"
        try:
            response = session.get(main_url, timeout=15)
            soup = BeautifulSoup(response.content, "lxml")
            counter = 0
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]
                if "/games/ea-sports-fc/ratings/player-ratings/" in href:
                    full_url = "https://www.ea.com" + href
                    if full_url not in player_links:
                        player_links.append(full_url)
                        counter += 1
                if counter >= LINKS_PER_PAGE: break
            print(f"Page {page_no}: Found {counter} player links.")
        except Exception as e:
            print(f"Error on page {page_no}: {e}")

    print(f"\n--- Phase 2: Scraping {len(player_links)} players using {MAX_WORKERS} workers ---")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = list(executor.map(parse_player_page, player_links))

    scraped_data = [r for r in results if r is not None]
    print(f"Successfully scraped {len(scraped_data)} profiles.")

    print("\n--- Phase 3: Sorting data by OVR (Descending) ---")
    scraped_data.sort(key=lambda x: x['ovr'], reverse=True)

    print("\n--- Phase 4: Adding to Database ---")
    for p in scraped_data:
        if not db.find_player(p['name']):
            db.create_player(p['name'], p['pos'], p['ovr'], p['nation'], p['club'], None)
            successful_scrapes += 1
            print(f"Stored: {p['name']} (OVR: {p['ovr']})")
        else:
            print(f"Skipped (Already exists): {p['name']}")
    
    total_time = time.perf_counter() - scrape_start

    print("\n" + "="*40)
    print("           SCRAPER STATS")
    print("="*40)
    print(f"Total New Records Stored: {successful_scrapes}")
    print(f"Total Time Taken:         {total_time:.2f}s")
    
    if successful_scrapes > 0:
        avg_time = total_time / len(scraped_data)
        print(f"Avg Time Per Profile:     {avg_time:.4f}s")
    print("="*40)

if __name__ == "__main__":
    get_data()