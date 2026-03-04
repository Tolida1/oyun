import requests
from bs4 import BeautifulSoup
import json

URL = "https://dizipal.bar/dizi-kategori/aksiyon/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8",
    "Connection": "keep-alive"
}

items = []

try:
    r = requests.get(URL, headers=headers, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.select("div.grid a"):
        title = a.get_text(strip=True)
        link = a.get("href")

        if title and link:
            items.append({
                "title": title,
                "link": link
            })

except Exception as e:
    print("Hata:", e)

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=4)

print("Toplam:", len(items))
