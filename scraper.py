import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://dizipal.bar/dizi-kategori/aksiyon/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(BASE_URL, headers=headers, timeout=10)

if r.status_code != 200:
    print("Siteye erişilemedi:", r.status_code)
    exit()

soup = BeautifulSoup(r.text, "html.parser")

items = []

# Grid içindeki linkleri al
for a in soup.select("div.grid a"):
    title = a.get_text(strip=True)
    link = a.get("href")

    if title and link:
        items.append({
            "title": title,
            "link": link
        })

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=4)

print("Bitti. output.json oluşturuldu.")
