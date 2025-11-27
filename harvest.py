import os
import requests
import time

# CONFIG
MAX_BACKGROUNDS = 100 
MAX_MOTIFS = 1500
# We use the proxy to handle the "202 Processing" delays for us
PROXY_BASE = "https://wsrv.nl/?url=static.ankama.com/dofus/renderer/emblem"

# Create folders
os.makedirs("backgrounds", exist_ok=True)
os.makedirs("motifs", exist_ok=True)

def download_via_proxy(ankama_path, save_path):
    # Skip if we already have it
    if os.path.exists(save_path):
        # Optional: Print less to keep logs clean
        # print(f"[SKIP] {save_path}") 
        return 
    
    # Retry loop for the proxy
    attempts = 0
    while attempts < 3:
        try:
            # &output=png ensures we get a standard image format
            # &n=-1 tells the proxy to fetch immediately
            full_url = f"{PROXY_BASE}{ankama_path}&output=png&n=-1"
            
            r = requests.get(full_url, timeout=30)
            
            if r.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(r.content)
                print(f"[OK] {save_path}")
                return
            
            elif r.status_code == 404:
                # 404 from Proxy usually means 404 from Origin (Gap in IDs)
                return 
            
            elif r.status_code == 429:
                # Rate limit on the proxy side
                time.sleep(2)
                attempts += 1
            else:
                # Other error
                attempts += 1
                
        except Exception as e:
            print(f"[ERR] {e}")
            attempts += 1
    
    # If we get here, it failed 3 times
    print(f"[FAIL] Could not download {save_path}")

print("--- Starting Proxy Harvest ---")

# 1. Backgrounds
print(">>> Downloading Backgrounds...")
for i in range(1, MAX_BACKGROUNDS + 1):
    # Path: /1/ID/0xCCCCCC/0x000000/60_60-0.png
    path = f"/1/{i}/0xCCCCCC/0x000000/60_60-0.png"
    download_via_proxy(path, f"backgrounds/{i}.png")

# 2. Motifs
print(">>> Downloading Motifs...")
for i in range(1, MAX_MOTIFS + 1):
    # Path: /ID/1/0xFFFFFF/0x333333/60_60-0.png
    path = f"/{i}/1/0xFFFFFF/0x333333/60_60-0.png"
    download_via_proxy(path, f"motifs/{i}.png")

print("--- Job Complete ---")
