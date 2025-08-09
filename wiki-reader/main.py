import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://en.wikipedia.org/wiki/List_of_American_films_of_{}"
all_films = []

# 爬取1970到1979年
for year in range(1970, 1980):
    print(f"Fetching films for {year}...")
    url = base_url.format(year)
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        tables = soup.find_all("table", {"class": "wikitable"})
        
        for table in tables:
            rows = table.find_all("tr")[1:]
            for row in rows:
                cells = row.find_all("td")
                if cells:
                    title_cell = cells[0]
                    link = title_cell.find("a")
                    if link and link.get("href", "").startswith("/wiki/"):
                        film_title = link.get_text(strip=True)
                        film_link = "https://en.wikipedia.org" + link["href"]
                        all_films.append({
                            "year": year,
                            "title": film_title,
                            "link": film_link
                        })
        time.sleep(1.5)  # 加上访问间隔
    except Exception as e:
        print(f"Error on {year}: {e}")
        continue

# 存为CSV
df_all = pd.DataFrame(all_films)
df_all.to_csv("1970s_american_films.csv", index=False)
print("Saved as 1970s_american_films.csv")
