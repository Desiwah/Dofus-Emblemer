import os
import requests
import time

# CONFIG
MAX_BACKGROUNDS = 100 
MAX_MOTIFS = 1200

# Using the IO Proxy as requested
PROXY_BASE = "https://corsproxy.io/?"
ANKAMA_BASE = "https://static.ankama.com/dofus/renderer/emblem"

# Create folders
os.makedirs("backgrounds", exist_ok=True)
os.makedirs("motifs", exist_ok=True)

def download_file(ankama_path, save_path):
    if os.path.exists(save_path):
        print(f"[SKIP] {save_path}", flush=True)
        return 
    
    # Construct URL: Proxy + Ankama
    # Example: https://corsproxy.io/?https://static.ankama.com/...
    target_url = PROXY_BASE + ANKAMA_BASE + ankama_path
    
    try:
        # User-Agent to look like a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        r = requests.get(target_url, headers=headers, timeout=20)
        
        if r.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(r.content)
            # flush=True makes this show up IMMEDIATELY in logs
            print(f"[OK] {save_path}", flush=True)
        else:
            # 404 is normal for gaps
            # Print only if it's NOT a 404 so we don't spam errors for empty IDs
            if r.status_code != 404:
                print(f"[ERR] {r.status_code} for {save_path}", flush=True)
            
    except Exception as e:
        print(f"[EXC] {e}", flush=True)
    
    # Sleep 0.2s to be polite
    time.sleep(0.2) 

print("--- STARTING FAST HARVEST (IO) ---", flush=True)

# 1. Backgrounds
print(">>> Downloading Backgrounds...", flush=True)
for i in range(1, MAX_BACKGROUNDS + 1):
    # Black Shield
    path = f"/1/{i}/0xCCCCCC/0x000000/60_60-0.png"
    download_file(path, f"backgrounds/{i}.png")

# 2. Motifs
print(">>> Downloading Motifs...", flush=True)
for i in range(1, MAX_MOTIFS + 1):
    # White Icon
    path = f"/{i}/1/0xFFFFFF/0x333333/60_60-0.png"
    download_file(path, f"motifs/{i}.png")

print("--- JOB DONE ---", flush=True)
