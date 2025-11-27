import os
import requests
import time

# CONFIG
MAX_BACKGROUNDS = 100 
MAX_MOTIFS = 1200
BASE_URL = "https://static.ankama.com/dofus/renderer/emblem"
ASSET_DIR = "assets" # New parent folder

# Create nested folders: assets/backgrounds and assets/motifs
os.makedirs(f"{ASSET_DIR}/backgrounds", exist_ok=True)
os.makedirs(f"{ASSET_DIR}/motifs", exist_ok=True)

def download_if_missing(url, path):
    if os.path.exists(path):
        return 
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        r = requests.get(url, headers=headers, timeout=10)
        
        if r.status_code == 200:
            with open(path, 'wb') as f:
                f.write(r.content)
            print(f"OK: {path}")
        else:
            print(f"Missing ({r.status_code}): {path}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(0.05) 

print("--- Updating Backgrounds ---")
for i in range(1, MAX_BACKGROUNDS + 1):
    url = f"{BASE_URL}/1/{i}/0xCCCCCC/0x000000/60_60-0.png"
    # Save to assets/backgrounds
    download_if_missing(url, f"{ASSET_DIR}/backgrounds/{i}.png")

print("--- Updating Motifs ---")
for i in range(1, MAX_MOTIFS + 1):
    url = f"{BASE_URL}/{i}/1/0xFFFFFF/0x333333/60_60-0.png"
    # Save to assets/motifs
    download_if_missing(url, f"{ASSET_DIR}/motifs/{i}.png")
