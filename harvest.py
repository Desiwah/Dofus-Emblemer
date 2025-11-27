import os
import requests
import time
import urllib.parse

# --- CONFIGURATION ---
MAX_BACKGROUNDS = 100 
MAX_MOTIFS = 1500

# PROXY: We use corsproxy.io as requested
# It acts as a tunnel to Ankama
PROXY_BASE = "https://corsproxy.io/?"

# Create folders
os.makedirs("backgrounds", exist_ok=True)
os.makedirs("motifs", exist_ok=True)

def download_file(ankama_url, save_path):
    if os.path.exists(save_path):
        return 
    
    # Retry loop (Try 3 times)
    for attempt in range(3):
        try:
            # Construct the Proxy URL
            # Format: https://corsproxy.io/?https://static.ankama...
            target_url = PROXY_BASE + ankama_url
            
            # Headers to look like a browser accessing the proxy
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36',
                'Origin': 'https://github.com'
            }
            
            r = requests.get(target_url, headers=headers, timeout=20)
            
            if r.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(r.content)
                print(f"[OK] {save_path}")
                return # Success, exit function
            
            elif r.status_code == 404:
                # Real 404 from Ankama means image doesn't exist. Don't retry.
                # print(f"[404] Gap at {save_path}")
                return 
            
            else:
                # Other error (403, 500, etc) - wait and retry
                time.sleep(2)
                
        except Exception as e:
            print(f"[ERR] Attempt {attempt+1}: {e}")
            time.sleep(1)
            
    print(f"[FAIL] Gave up on {save_path}")

print("--- Starting IO Proxy Harvest ---")

BASE = "https://static.ankama.com/dofus/renderer/emblem"

# 1. Backgrounds
print(">>> Downloading Backgrounds...")
for i in range(1, MAX_BACKGROUNDS + 1):
    # Black Shield
    url = f"{BASE}/1/{i}/0xCCCCCC/0x000000/60_60-0.png"
    download_file(url, f"backgrounds/{i}.png")

# 2. Motifs
print(">>> Downloading Motifs...")
for i in range(1, MAX_MOTIFS + 1):
    # White Icon
    url = f"{BASE}/{i}/1/0xFFFFFF/0x333333/60_60-0.png"
    download_file(url, f"motifs/{i}.png")

print("--- Job Complete ---")
