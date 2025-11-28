import os
import requests
import time
import random

# --- CONFIGURATION ---
MAX_BACKGROUNDS = 200 
MAX_MOTIFS = 1200 # Increased range to find everything
BASE_URL = "https://static.ankama.com/dofus/renderer/emblem"

# Create folders
os.makedirs("backgrounds", exist_ok=True)
os.makedirs("motifs", exist_ok=True)

# Headers to look exactly like a Chrome Browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Referer': 'https://www.dofus.com/',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive'
}

def download_file(url, path):
    # If we already have it, skip
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return 

    # Retry loop for resilience
    attempts = 0
    while attempts < 3:
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            
            if r.status_code == 200:
                with open(path, 'wb') as f:
                    f.write(r.content)
                print(f"[OK] {path}")
                return
            
            elif r.status_code == 404:
                # Genuine 404 means gap in IDs. This is fine.
                return 
            
            elif r.status_code == 403 or r.status_code == 429:
                print(f"⚠️ BLOCKED. Sleeping 60s...")
                time.sleep(60) # Wait out the ban
                attempts += 1
                continue
            
            else:
                # Server error, wait briefly
                time.sleep(2)
                attempts += 1

        except Exception as e:
            print(f"[ERR] {e}")
            time.sleep(2)
            attempts += 1
            
    # If we reach here, we failed.

print("--- STARTING POLITE HARVEST ---", flush=True)

# 1. Backgrounds
print(">>> Backgrounds...", flush=True)
for i in range(1, MAX_BACKGROUNDS + 1):
    url = f"{BASE_URL}/1/{i}/0xCCCCCC/0x000000/60_60-0.png"
    download_file(url, f"backgrounds/{i}.png")
    time.sleep(0.2) # Polite delay

# 2. Motifs
print(">>> Motifs...", flush=True)
for i in range(1, MAX_MOTIFS + 1):
    url = f"{BASE_URL}/{i}/1/0xFFFFFF/0x333333/60_60-0.png"
    download_file(url, f"motifs/{i}.png")
    # CRITICAL: Sleep to mimic human browsing speed
    time.sleep(0.3) 

print("--- JOB DONE ---", flush=True)
