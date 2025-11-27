import os
import requests
import time

# --- CONFIGURATION ---
MAX_BACKGROUNDS = 100 
MAX_MOTIFS = 2000

# Proxy
PROXY_BASE = "https://corsproxy.io/?"
ANKAMA_BASE = "https://static.ankama.com/dofus/renderer/emblem"
ASSET_DIR = "assets"

# Create folders
os.makedirs(f"{ASSET_DIR}/backgrounds", exist_ok=True)
os.makedirs(f"{ASSET_DIR}/motifs", exist_ok=True)

def download_file(ankama_path, save_path):
    if os.path.exists(save_path):
        return 
    
    # URL
    target_url = PROXY_BASE + ANKAMA_BASE + ankama_path
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
    }

    # FAST RETRY LOOP
    # We only try 2 times max.
    for attempt in range(2):
        try:
            # TIMEOUT IS NOW 2 SECONDS
            # If it takes longer than 2s, we kill it.
            r = requests.get(target_url, headers=headers, timeout=2)
            
            if r.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(r.content)
                print(f"[OK] {save_path}", flush=True)
                return
            
            elif r.status_code == 404:
                # Instant fail for missing files
                return 
            
        except Exception:
            # If timeout or error, just try one more time or skip
            pass
    
    # If we get here, it timed out twice. Move on.
    # We don't print "Fail" to keep logs clean, just skip it.

print("--- STARTING SPEED RUN ---", flush=True)

# 1. Backgrounds
print(">>> Scanning Backgrounds...", flush=True)
for i in range(1, MAX_BACKGROUNDS + 1):
    path = f"/1/{i}/0xCCCCCC/0x000000/60_60-0.png"
    download_file(path, f"{ASSET_DIR}/backgrounds/{i}.png")

# 2. Motifs
print(">>> Scanning Motifs...", flush=True)
for i in range(1, MAX_MOTIFS + 1):
    path = f"/{i}/1/0xFFFFFF/0x333333/60_60-0.png"
    download_file(path, f"{ASSET_DIR}/motifs/{i}.png")

print("--- JOB DONE ---", flush=True)
