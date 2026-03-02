import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
import os

# --- AYARLAR ---
BASE_URL = "https://dizipal.bar"
OUTPUT_FILE = "dizipal_arsiv.json"

# Örnek kategoriler
KATEGORILER = {
    'aksiyon': 'Aksiyon',
    'hbomax': 'HBO Max',
    'anime': 'Anime'
}

# Chrome başlatıcı (sürümü otomatik algıla)
def get_driver():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless=new")  # GitHub Actions için headless
    # Sürüm otomatik, GitHub Actions ile uyumlu
    driver = uc.Chrome(options=options)
    return driver

# Scraper fonksiyonu
def scrape():
    results = {}
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            try:
                results = json.load(f)
            except:
                results = {}

    driver = get_driver()

    try:
        print("🛡️ Cloudflare geçiliyor...")
        driver.get(BASE_URL)
        time.sleep(15)  # Cloudflare bekleme

        for slug, ad in KATEGORILER.items():
            cat_url = f"{BASE_URL}/platform/{slug}/" if slug == 'hbomax' else f"{BASE_URL}/kategori/{slug}/"
            print(f"\n📂 Kategori: {ad}")
            driver.get(cat_url)
            time.sleep(5)

            items = driver.find_elements(By.CSS_SELECTOR, ".post-item, article")
            content_links = []
            for item in items:
                try:
                    a = item.find_element(By.TAG_NAME, "a")
                    img = item.find_element(By.TAG_NAME, "img")
                    content_links.append({
                        "title": a.get_attribute("title") or a.text,
                        "url": a.get_attribute("href"),
                        "img": img.get_attribute("src")
                    })
                except:
                    continue

            for content in content_links:
                key = re.sub(r'\W+', '-', content['title']).lower().strip('-')
                if key in results: continue

                print(f"🔍 İnceleniyor: {content['title']}")
                driver.get(content['url'])
                time.sleep(3)

                results[key] = {
                    "isim": content['title'],
                    "resim": content['img'],
                    "bolumler": []
                }

                ep_elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='bolum']")
                if not ep_elements:
                    iframes = driver.find_elements(By.TAG_NAME, "iframe")
                    if iframes:
                        results[key]["bolumler"].append({
                            "bolum_baslik": "Film",
                            "link": iframes[0].get_attribute("src")
                        })
                else:
                    ep_urls = [el.get_attribute("href") for el in ep_elements]
                    for i, ep_url in enumerate(ep_urls, 1):
                        try:
                            driver.get(ep_url)
                            WebDriverWait(driver, 7).until(
                                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
                            )
                            iframe = driver.find_element(By.TAG_NAME, "iframe")
                            real_video_link = iframe.get_attribute("src")
                            results[key]["bolumler"].append({
                                "bolum_baslik": f"Bölüm {i}",
                                "link": real_video_link
                            })
                            print(f"   ✅ {i}. Bölüm linki alındı.")
                            time.sleep(1)
                        except:
                            print(f"   ⚠️ {i}. Bölümde hata oluştu.")
                            continue

                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f"❌ Hata: {e}")
    finally:
        driver.quit()
        print("🏁 İşlem bitti.")

if __name__ == "__main__":
    scrape()
