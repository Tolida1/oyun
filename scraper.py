import requests
import xml.etree.ElementTree as ET
import json

FEED_URL = "https://dizipal.uk/dizi-kategori/aksiyon/feed/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/rss+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://google.com",
    "Connection": "keep-alive"
}

items = []

try:
    r = requests.get(FEED_URL, headers=headers, timeout=15)
    print("Status:", r.status_code)
    r.raise_for_status()

    root = ET.fromstring(r.content)
    channel = root.find("channel")

    for item in channel.findall("item"):
        title = item.find("title").text if item.find("title") is not None else ""
        link = item.find("link").text if item.find("link") is not None else ""

        items.append({
            "title": title,
            "link": link
        })

except Exception as e:
    print("Hata:", e)

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=4)

print("Toplam kayıt:", len(items))
