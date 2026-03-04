import requests
import xml.etree.ElementTree as ET
import json

FEED_URL = "https://dizipal.bar/dizi-kategori/aksiyon/feed/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

items = []

try:
    r = requests.get(FEED_URL, headers=headers, timeout=15)
    r.raise_for_status()

    root = ET.fromstring(r.content)

    channel = root.find("channel")

    for item in channel.findall("item"):
        title = item.find("title").text if item.find("title") is not None else ""
        link = item.find("link").text if item.find("link") is not None else ""
        pubDate = item.find("pubDate").text if item.find("pubDate") is not None else ""

        items.append({
            "title": title,
            "link": link,
            "pubDate": pubDate
        })

except Exception as e:
    print("Hata:", e)

# HER DURUMDA DOSYA OLUŞSUN
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=4)

print("Toplam kayıt:", len(items))
