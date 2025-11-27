import os
import requests
import time

# --- CONFIGURATION ---
# We scan past the known limit to catch new updates automatically
MAX_BACKGROUNDS = 100 
MAX_MOTIFS = 2000

# Proxy to bypass firewall
PROXY_BASE = "https://corsproxy.io/?"
ANKAMA_BASE = "https://static.ankama.com/dofus/renderer/emblem"

# Create folders
os.makedirs("backgrounds", exist_ok=True)
os.makedirs("motifs", exist_ok=True)

def download_file(ankama_path, save_path):
    # Optimization: Don't re-download if we already have it
    if os.path.exists(save_path):
        # print(f"[EXISTS] {save_path}", flush=True) 
        return 
    
    target_url = PROXY_BASE + ANKAMA_BASE + ankama_path
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 10s timeout is enough. If it takes longer, it probably doesn't exist.
        r = requests.get(target_url, headers=headers, timeout=10)
        
        if r.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(r.content)
            print(f"[NEW] Downloaded: {save_path}", flush=True)
            
        elif r.status_code == 404:
            # THIS IS KEY: 404 means "Not released yet". This is NOT a crash.
            # We just ignore it silently or print a small msg
            pass 
            
        else:
            print(f"[ERR] Status {r.status_code} for {save_path}", flush=True)

    except Exception as e:
        # If proxy times out, it usually means the file doesn't exist or proxy is busy.
        # We catch the error so the script DOES NOT CRASH.
        print(f"[WARN] skipped {save_path} (Timeout/Error)", flush=True)
    
    # Tiny sleep to allow the connection to close properly
    time.sleep(0.1)

print("--- STARTING UPDATE CHECK ---", flush=True)

# 1. Backgrounds
print(f"Scanning 1-{MAX_BACKGROUNDS} Backgrounds...", flush=True)
for i in range(1, MAX_BACKGROUNDS + 1):
    # Black Shield
    path = f"/1/{i}/0xCCCCCC/0x000000/60_60-0.png"
    download_file(path, f"backgrounds/{i}.png")

# 2. Motifs
print(f"Scanning 1-{MAX_MOTIFS} Motifs...", flush=True)
for i in range(1, MAX_MOTIFS + 1):
    # White Icon
    path = f"/{i}/1/0xFFFFFF/0x333333/60_60-0.png"
    download_file(path, f"motifs/{i}.png")

print("--- UPDATE COMPLETE ---", flush=True)
