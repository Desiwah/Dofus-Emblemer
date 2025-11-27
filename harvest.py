import os
import requests
import time

# --- CONFIGURATION ---
MAX_BACKGROUNDS = 100 
MAX_MOTIFS = 2000

# We use wsrv.nl because it returns 404s faster than corsproxy
PROXY_BASE = "https://wsrv.nl/?url=static.ankama.com/dofus/renderer/emblem"
ASSET_DIR = "assets"

os.makedirs(f"{ASSET_DIR}/backgrounds", exist_ok=True)
os.makedirs(f"{ASSET_DIR}/motifs", exist_ok=True)

def download_file(ankama_path, save_path):
    if os.path.exists(save_path):
        return 
    
    # &n=-1 tells wsrv to not wait/queue, just fail fast if needed
    target_url = f"{PROXY_BASE}{ankama_path}&output=png&n=-1"
    
    try:
        # TIMEOUT = 2 SECONDS. 
        # If it takes longer than 2s, it's definitely a gap. Kill it.
        r = requests.get(target_url, timeout=2)
        
        if r.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(r.content)
            print(f"[OK] {save_path}", flush=True)
            
        elif r.status_code == 404 or r.status_code == 400:
            # 404 = Missing (Gap)
            print(f"[GAP] {save_path} (Missing)", flush=True)
            
        else:
            print(f"[ERR] Status {r.status_code}", flush=True)

    except Exception:
        # If it times out, we assume it's a gap and just move on instantly
        print(f"[SKIP] {save_path} (Timeout)", flush=True)

print("--- STARTING BULLDOZER HARVEST ---", flush=True)

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
