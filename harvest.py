import os
import requests
import time

# --- CONFIGURATION ---
MAX_BACKGROUNDS = 200 
MAX_MOTIFS = 1200
BASE_URL = "https://static.ankama.com/dofus/renderer/emblem"

# Directories
os.makedirs("assets/backgrounds", exist_ok=True)
os.makedirs("assets/motifs", exist_ok=True)

# Headers to look like a real Chrome Browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Referer': 'https://www.dofus.com/',
    'Connection': 'keep-alive'
}

def is_valid_image(path):
    """Checks if file exists and is larger than 1KB (not an error text file)"""
    if not os.path.exists(path):
        return False
    if os.path.getsize(path) < 1000: # Less than 1KB is usually a corrupted error message
        return False
    return True

def download_file(url, path):
    # SKIP if we already have a valid image
    if is_valid_image(path):
        return 

    print(f"[DOWNLOADING] {path} ...")
    
    attempts = 0
    while attempts < 3:
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            
            if r.status_code == 200:
                with open(path, 'wb') as f:
                    f.write(r.content)
                print(f"   -> Success!")
                return
            elif r.status_code == 404:
                return # Gap in IDs
            elif r.status_code == 403:
                print("   -> ⚠️ Blocked (403). Waiting 20s...")
                time.sleep(20)
                attempts += 1
            else:
                time.sleep(1)
                attempts += 1
        except Exception as e:
            print(f"   -> Error: {e}")
            attempts += 1
            
    # Sleep to mimic human browsing
    time.sleep(0.2)

print("--- REPAIRING BACKGROUNDS ---")
for i in range(1, MAX_BACKGROUNDS + 1):
    url = f"{BASE_URL}/1/{i}/0xCCCCCC/0x000000/60_60-0.png"
    download_file(url, f"assets/backgrounds/{i}.png")

print("--- REPAIRING MOTIFS ---")
for i in range(1, MAX_MOTIFS + 1):
    url = f"{BASE_URL}/{i}/1/0xFFFFFF/0x333333/60_60-0.png"
    download_file(url, f"assets/motifs/{i}.png")

print("\n--- REPAIR COMPLETE. UPLOAD TO GITHUB. ---")
