import os
import requests
import time
import random

# --- CONFIGURATION ---
MAX_BACKGROUNDS = 200 
MAX_MOTIFS = 2000 # Increased to match your JS
BASE_URL = "https://static.ankama.com/dofus/renderer/emblem"

os.makedirs("assets/backgrounds", exist_ok=True)
os.makedirs("assets/motifs", exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Referer': 'https://www.dofus.com/',
    'Connection': 'keep-alive'
}

def download_file(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return 

    print(f"[DOWNLOADING] {path} ...")
    
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                f.write(r.content)
            print(f"   -> Success!")
        elif r.status_code == 403:
            print("   -> ⚠️ Blocked (403). Pausing for 60s...")
            time.sleep(60) 
        else:
            print(f"   -> Failed: {r.status_code}")
    except Exception as e:
        print(f"   -> Error: {e}")

    # Random sleep between 1.0 and 2.5 seconds to look human
    time.sleep(random.uniform(1.0, 2.5))

print("--- STARTING BACKGROUNDS ---")
for i in range(1, MAX_BACKGROUNDS + 1):
    # 60x60 Thumbnail
    url = f"{BASE_URL}/1/{i}/0xCCCCCC/0x000000/60_60-0.png"
    download_file(url, f"assets/backgrounds/{i}.png")

print("--- STARTING MOTIFS ---")
for i in range(1, MAX_MOTIFS + 1):
    # 60x60 Thumbnail
    url = f"{BASE_URL}/{i}/1/0xFFFFFF/0x333333/60_60-0.png"
    download_file(url, f"assets/motifs/{i}.png")
