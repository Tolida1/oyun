import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re
import os

BASE_URL = "https://dizipal.bar"
OUTPUT_FILE = "dizipal_arsiv.json"

KATEGORILER = {
    'aksiyon': 'Aksiyon',
    'hbomax': 'HBO Max',
    'anime': 'Anime'
}

def load_json():
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_json(data):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def scrape():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")

    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    results = load_json()

    try:
        print("Ana sayfa açılıyor...")
        driver.get(BASE_URL)

        # Sayfa yüklenmesini bekle
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        for slug, ad in KATEGORILER.items():
            print(f"\nKategori: {ad}")

            if slug == "hbomax":
                cat_url = f"{BASE_URL}/platform/{slug}/"
            else:
                cat_url = f"{BASE_URL}/kategori/{slug}/"

            driver.get(cat_url)

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".post-item, article")))

            items = driver.find_elements(By.CSS_SELECTOR, ".post-item, article")

            for item in items:
                try:
                    a = item.find_element(By.TAG_NAME, "a")
                    img = item.find_element(By.TAG_NAME, "img")

                    title = a.get_attribute("title") or a.text
                    url = a.get_attribute("href")
                    image = img.get_attribute("src")

                    key = re.sub(r'\W+', '-', title).lower().strip('-')

                    if key in results:
                        continue

                    print("İçerik:", title)

                    driver.get(url)

                    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                    results[key] = {
                        "isim": title,
                        "resim": image,
                        "bolumler": []
                    }

                    # Bölüm linkleri
                    ep_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='bolum']")

                    if not ep_links:
                        iframes = driver.find_elements(By.TAG_NAME, "iframe")
                        if iframes:
                            results[key]["bolumler"].append({
                                "bolum_baslik": "Film",
                                "link": iframes[0].get_attribute("src")
                            })
                    else:
                        ep_urls = [e.get_attribute("href") for e in ep_links]

                        for i, ep in enumerate(ep_urls, 1):
                            driver.get(ep)
                            wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))

                            iframe = driver.find_element(By.TAG_NAME, "iframe")

                            results[key]["bolumler"].append({
                                "bolum_baslik": f"Bölüm {i}",
                                "link": iframe.get_attribute("src")
                            })

                    save_json(results)

                except Exception as e:
                    print("Hata:", e)
                    continue

    finally:
        driver.quit()
        print("İşlem bitti.")

if __name__ == "__main__":
    scrape()
