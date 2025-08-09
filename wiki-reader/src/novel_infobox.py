import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# 请替换为你自己的 CSV 路径
df_input = pd.read_csv("1970s_american_novels.csv")

fields_of_interest = {
    "language": "language",
    "genre": "genre",
    "publication date": "publication_date",
    "published": "publication_place"
}

results = []

for idx, row in df_input.iterrows():
    title = row["title"]
    url = row["link"]
    year = row["year"]
    data = {"title": title, "year": year, "link": url}

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        infobox = soup.find("table", class_="infobox")

        if infobox:
            rows = infobox.find_all("tr")
            for row in rows:
                th = row.find("th")
                td = row.find("td")
                if th and td:
                    field = th.text.strip().lower()
                    value = td.text.strip()
                    if field in fields_of_interest:
                        data[fields_of_interest[field]] = value

        results.append(data)
        print(f"[✓] {idx+1}/{len(df_input)} {title}")
        time.sleep(1.5)

    except Exception as e:
        print(f"[X] {title}: {e}")

df = pd.DataFrame(results)
df.to_csv("1970s_novels_infobox_info.csv", index=False)
print("✅ Saved to 1970s_novels_infobox_info.csv")
