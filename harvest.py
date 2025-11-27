import os
import requests
import time

# CONFIG
MAX_BACKGROUNDS = 100 
MAX_MOTIFS = 1200
# We use wsrv.nl as a middleman to bypass Ankama's firewall
PROXY_BASE = "https://wsrv.nl/?url=static.ankama.com/dofus/renderer/emblem"

# Create folders
os.makedirs("backgrounds", exist_ok=True)
os.makedirs("motifs", exist_ok=True)

def download_via_proxy(ankama_path, save_path):
    if os.path.exists(save_path):
        return 
    
    try:
        # Construct Proxy URL
        # We append &output=png to ensure we get a clean image
        full_url = f"{PROXY_BASE}{ankama_path}&output=png"
        
        r = requests.get(full_url, timeout=15)
        
        if r.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(r.content)
            print(f"OK: {save_path}")
        else:
            print(f"Failed ({r.status_code}): {save_path}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    # Tiny sleep to be polite to the proxy
    time.sleep(0.1) 

print("--- Downloading Backgrounds (via Proxy) ---")
for i in range(1, MAX_BACKGROUNDS + 1):
    # Path suffix: /1/ID/0xCCCCCC/0x000000/60_60-0.png
    path = f"/1/{i}/0xCCCCCC/0x000000/60_60-0.png"
    download_via_proxy(path, f"backgrounds/{i}.png")

print("--- Downloading Motifs (via Proxy) ---")
for i in range(1, MAX_MOTIFS + 1):
    # Path suffix: /ID/1/0xFFFFFF/0x333333/60_60-0.png
    path = f"/{i}/1/0xFFFFFF/0x333333/60_60-0.png"
    download_via_proxy(path, f"motifs/{i}.png")

print("\n--- Done! Check your folders. ---")
