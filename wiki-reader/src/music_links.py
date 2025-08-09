import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

years = range(1970, 1980)
base_url = "https://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_number_ones_of_{}"

all_songs = []

for year in years:
    url = base_url.format(year)
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        tables = soup.find_all("table", class_="wikitable")
        for table in tables:
            rows = table.find_all("tr")
            for row in rows[1:]:
                cells = row.find_all("td")
                if len(cells) >= 3:
                    song_cell = cells[1]
                    artist_cell = cells[2]

                    link_tag = song_cell.find("a")
                    if link_tag and link_tag.get("href", "").startswith("/wiki/"):
                        song_title = link_tag.get_text(strip=True)
                        song_link = "https://en.wikipedia.org" + link_tag['href']
                    else:
                        song_title = song_cell.text.strip()
                        song_link = None

                    artist = artist_cell.text.strip()

                    all_songs.append({
                        "year": year,
                        "song": song_title,
                        "link": song_link,
                        "artist": artist
                    })

        print(f"[✓] {year}")
        time.sleep(1.5)

    except Exception as e:
        print(f"[X] {year}: {e}")

df = pd.DataFrame(all_songs)
df.to_csv("1970s_billboard_hot100_links.csv", index=False)
print("✅ Saved to 1970s_billboard_hot100_links.csv")
