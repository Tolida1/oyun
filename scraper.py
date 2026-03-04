import requests
import json

API_URL = "https://dizipal.bar/wp-json/wp/v2/posts?categories=50295&per_page=100"

headers = {
    "User-Agent": "Mozilla/5.0"
}

items = []

try:
    r = requests.get(API_URL, headers=headers, timeout=15)
    print("Status:", r.status_code)
    r.raise_for_status()

    data = r.json()

    for post in data:
        items.append({
            "title": post["title"]["rendered"],
            "link": post["link"],
            "date": post["date"],
            "excerpt": post["excerpt"]["rendered"]
        })

except Exception as e:
    print("Hata:", e)

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=4)

print("Toplam:", len(items))
