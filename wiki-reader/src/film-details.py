import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# 替换为你的CSV文件
df_input = pd.read_csv("1970s_american_films.csv")

fields_of_interest = {
    "release date": "release_date",
    "running time": "runtime",
    "country": "country",
    "language": "language"
}

film_details = []

for index, row in df_input.iterrows():
    title = row["title"]
    url = row["link"]

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        infobox = soup.find("table", class_="infobox vevent")

        data = {
            "title": title,
            "link": url
        }

        if infobox:
            rows = infobox.find_all("tr")
            for r in rows:
                th = r.find("th")
                td = r.find("td")
                if th and td:
                    field = th.text.strip().lower()
                    value = td.text.strip()
                    for key in fields_of_interest:
                        if key in field:
                            data[fields_of_interest[key]] = value

        film_details.append(data)
        print(f"[✓] {index+1}/{len(df_input)} {title}")
        time.sleep(1.5)

    except Exception as e:
        print(f"[X] {title}: {e}")
        continue

df_output = pd.DataFrame(film_details)
df_output.to_csv("1970s_film_metadata.csv", index=False)
print("✅ Saved to 1970s_film_metadata.csv")
