import os
import requests
import time

# CONFIG
MAX_BACKGROUNDS = 100
MAX_MOTIFS = 2000
PROXY_BASE = "https://corsproxy.io/?"
ANKAMA_BASE = "https://static.ankama.com/dofus/renderer/emblem"
ASSET_DIR = "assets"

# Create directories: assets/backgrounds and assets/motifs
os.makedirs(f"{ASSET_DIR}/backgrounds", exist_ok=True)
os.makedirs(f"{ASSET_DIR}/motifs", exist_ok=True)

def download_file(ankama_path, save_path):
    if os.path.exists(save_path):
        # print(f"[SKIP] {save_path}", flush=True)
        return 
    
    # Retry loop (Try 3 times per image)
    for attempt in range(3):
        try:
            target_url = PROXY_BASE + ANKAMA_BASE + ankama_path
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
            }
            
            # Increased timeout to 30s for slow proxies
            r = requests.get(target_url, headers=headers, timeout=30)
            
            if r.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(r.content)
                print(f"[OK] {save_path}", flush=True)
                return # Success, exit function
            
            elif r.status_code == 404:
                return # Doesn't exist, stop retrying
            
            else:
                # Server error, wait and retry
                time.sleep(2)
                
        except Exception as e:
            print(f"[WARN] Attempt {attempt+1} failed for {save_path}: {e}", flush=True)
            time.sleep(2)
            
    print(f"[FAIL] Gave up on {save_path}", flush=True)

print("--- STARTING TANK HARVEST ---", flush=True)

# 1. Backgrounds
print(">>> Downloading Backgrounds...", flush=True)
for i in range(1, MAX_BACKGROUNDS + 1):
    path = f"/1/{i}/0xCCCCCC/0x000000/60_60-0.png"
    download_file(path, f"{ASSET_DIR}/backgrounds/{i}.png")

# 2. Motifs
print(">>> Downloading Motifs...", flush=True)
for i in range(1, MAX_MOTIFS + 1):
    path = f"/{i}/1/0xFFFFFF/0x333333/60_60-0.png"
    download_file(path, f"{ASSET_DIR}/motifs/{i}.png")

print("--- JOB DONE ---", flush=True)
