import cloudscraper
from bs4 import BeautifulSoup
import json

URL = "https://dizipal.bar/diziler/"

scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows'}
)

html = scraper.get(URL).text
soup = BeautifulSoup(html, "html.parser")

results = []

for item in soup.select("div.post-item, article"):
    a = item.select_one("a")
    if not a:
        continue

    title = a.get("title") or a.text.strip()
    href = a.get("href")

    if href and not href.startswith("http"):
        href = "https://dizipal.bar" + href

    results.append({
        "title": title,
        "url": href
    })

with open("diziler.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Tamamlandı:", len(results))
