import os
import requests
import time

# CONFIG
# We stick to the known ranges. If Ankama adds more, we increase these numbers.
MAX_BACKGROUNDS = 100 
MAX_MOTIFS = 1000
BASE_URL = "https://static.ankama.com/dofus/renderer/emblem"

# Folders
os.makedirs("backgrounds", exist_ok=True)
os.makedirs("motifs", exist_ok=True)

def download_if_missing(url, path):
    if os.path.exists(path):
        return # Skip existing to save time/bandwidth
    
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                f.write(r.content)
            print(f"+ {path}")
        else:
            pass # 404 is normal for gaps
    except:
        pass
    time.sleep(0.05) # Be polite

print("--- Updating Backgrounds ---")
for i in range(1, MAX_BACKGROUNDS + 1):
    # Black Shield
    url = f"{BASE_URL}/1/{i}/0xCCCCCC/0x000000/60_60-0.png"
    download_if_missing(url, f"backgrounds/{i}.png")

print("--- Updating Motifs ---")
for i in range(1, MAX_ICONS + 1):
    # White Icon
    url = f"{BASE_URL}/{i}/1/0xFFFFFF/0x333333/60_60-0.png"
    download_if_missing(url, f"motifs/{i}.png")
