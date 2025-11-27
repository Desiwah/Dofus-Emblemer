import os
import requests
import time

# --- CONFIGURATION ---
MAX_BACKGROUNDS = 85
MAX_MOTIFS = 1500
BASE_URL = "https://static.ankama.com/dofus/renderer/emblem"

# Create folders
os.makedirs("backgrounds", exist_ok=True)
os.makedirs("motifs", exist_ok=True)

# Headers to look like a real browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Referer': 'https://www.dofus.com/'
}

def download_with_retry(url, path):
    if os.path.exists(path):
        return 
    
    attempts = 0
    while attempts < 5:
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            
            # SUCCESS
            if r.status_code == 200:
                with open(path, 'wb') as f:
                    f.write(r.content)
                print(f"[OK] {path}")
                return
            
            # RENDERING (WAIT AND RETRY)
            elif r.status_code == 202:
                print(f"[WAIT] {path} is generating... (202)")
                time.sleep(1.5) # Wait for server to render
                attempts += 1
                continue # Retry loop
            
            # BLOCKED (WAIT LONGER)
            elif r.status_code == 403 or r.status_code == 429:
                print(f"[BLOCKED] Rate limit. Sleeping 10s...")
                time.sleep(10)
                attempts += 1
                continue

            # NOT FOUND
            elif r.status_code == 404:
                # Normal for gaps
                return
            
            else:
                print(f"[ERR] {r.status_code}: {url}")
                return

        except Exception as e:
            print(f"[EXC] {e}")
            time.sleep(1)
            attempts += 1
            
    print(f"[FAIL] Could not download {path} after retries.")

print("--- STARTING SMART HARVEST ---")

# 1. Backgrounds
for i in range(1, MAX_BACKGROUNDS + 1):
    url = f"{BASE_URL}/1/{i}/0xCCCCCC/0x000000/60_60-0.png"
    download_with_retry(url, f"backgrounds/{i}.png")
    time.sleep(0.1)

# 2. Motifs
for i in range(1, MAX_MOTIFS + 1):
    url = f"{BASE_URL}/{i}/1/0xFFFFFF/0x333333/60_60-0.png"
    download_with_retry(url, f"motifs/{i}.png")
    time.sleep(0.1)

print("--- DONE ---")
