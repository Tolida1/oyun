import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://dizipal.bar/dizi-kategori/aksiyon/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

items = []

try:
    r = requests.get(BASE_URL, headers=headers, timeout=15)
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

# HER DURUMDA DOSYA OLUŞSUN
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=4)

print("Bitti.")
