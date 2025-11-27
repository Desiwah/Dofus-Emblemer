import os
import requests
import time
import random

# CONFIG
MAX_BACKGROUNDS = 100
MAX_MOTIFS = 1200
BASE_URL = "https://static.ankama.com/dofus/renderer/emblem"

# Create folders in the ROOT directory
os.makedirs("backgrounds", exist_ok=True)
os.makedirs("motifs", exist_ok=True)

def download_if_missing(url, path):
    if os.path.exists(path):
        return 
    
    try:
        # HEADERS: Make Ankama think we are a real PC
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Referer': 'https://www.dofus.com/',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        
        r = requests.get(url, headers=headers, timeout=10)
        
        if r.status_code == 200:
            with open(path, 'wb') as f:
                f.write(r.content)
            print(f"OK: {path}")
        else:
            # If 404, it just means that specific ID doesn't exist (gaps are normal)
            # If 202/403, it means blocked, but we print to debug
            pass 
            
    except Exception as e:
        print(f"Error: {e}")
    
    # Sleep to prevent blocking
    time.sleep(0.05) 

print("--- Updating Backgrounds ---")
for i in range(1, MAX_BACKGROUNDS + 1):
    url = f"{BASE_URL}/1/{i}/0xCCCCCC/0x000000/60_60-0.png"
    download_if_missing(url, f"backgrounds/{i}.png")

print("--- Updating Motifs ---")
for i in range(1, MAX_MOTIFS + 1):
    url = f"{BASE_URL}/{i}/1/0xFFFFFF/0x333333/60_60-0.png"
    download_if_missing(url, f"motifs/{i}.png")
