import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://en.wikipedia.org"
TIMELINE_URL = "https://en.wikipedia.org/wiki/Timeline_of_United_States_history_(1960%E2%80%931979)"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_event_links():
    res = requests.get(TIMELINE_URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    links = []

    for li in soup.select("ul li a[href^='/wiki/']"):
        href = li.get("href")
        title = li.get("title")
        if title and ":" not in href and not href.startswith("/wiki/Timeline"):
            full_url = BASE_URL + href
            links.append((title, full_url))
    
    return list(set(links))  # 去重

def get_infobox_text(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        infobox = soup.select_one(".infobox")
        if infobox:
            return infobox.get_text(separator="\n").strip()
    except:
        return None
    return None

def scrape_to_csv(output_file="usa_1960s_70s_events.csv"):
    event_links = get_event_links()
    print(f"Found {len(event_links)} unique event pages.")

    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "URL", "Infobox_Text"])
        
        for title, url in event_links:
            print(f"Scraping: {title}")
            infobox = get_infobox_text(url)
            writer.writerow([title, url, infobox if infobox else ""])
            time.sleep(1)  # 避免访问过快被封

    print(f"Saved to {output_file}")

if __name__ == "__main__":
    scrape_to_csv()
