import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# 修改为你需要的年份范围
years = list(range(1970, 1980))
base_url = "https://en.wikipedia.org/wiki/Category:{}_American_novels"

novel_links = []

for year in years:
    url = base_url.format(year)
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        content_div = soup.find("div", class_="mw-category")
        if not content_div:
            content_div = soup.find("div", class_="mw-category-generated")

        if content_div:
            for link in content_div.find_all("a", href=True):
                title = link.text.strip()
                full_url = "https://en.wikipedia.org" + link['href']
                novel_links.append({"title": title, "year": year, "link": full_url})
        print(f"[✓] Year {year} done")
        time.sleep(1.5)
    except Exception as e:
        print(f"[X] Error fetching {url}: {e}")

df = pd.DataFrame(novel_links)
df.to_csv("1970s_american_novels.csv", index=False)
print("✅ Saved to 1970s_american_novels.csv")
