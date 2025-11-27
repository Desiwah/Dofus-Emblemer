import os
import requests
import time

# --- CONFIGURATION ---
MAX_BACKGROUNDS = 100 
MAX_MOTIFS = 1200

# We use wsrv.nl to proxy the request. 
# Ankama sees the request coming from them, not you.
# We append &output=png to ensure we get a clean image file.
PROXY_BASE = "https://wsrv.nl/?url=static.ankama.com/dofus/renderer/emblem"

# Create folders
os.makedirs("backgrounds", exist_ok=True)
os.makedirs("motifs", exist_ok=True)

def download_via_proxy(ankama_path, save_path):
    if os.path.exists(save_path):
        print(f"[SKIP] {save_path}")
        return 
    
    try:
        # Construct the Proxy URL
        # URL structure: https://wsrv.nl/?url=static.ankama.../path&output=png
        url = f"{PROXY_BASE}{ankama_path}&output=png"
        
        # We don't need complex headers for the proxy, standard is fine
        r = requests.get(url, timeout=20)
        
        if r.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(r.content)
            print(f"[OK] {save_path}")
        else:
            # If the proxy returns 404, it means the image doesn't exist on Ankama
            print(f"[MISSING] {save_path} (Status: {r.status_code})")
            
    except Exception as e:
        print(f"[ERROR] {save_path}: {e}")
    
    # Sleep is still good to be polite to the free proxy service
    time.sleep(0.1) 

print("--- Downloading Backgrounds via Proxy ---")
for i in range(1, MAX_BACKGROUNDS + 1):
    # Path: /1/ID/0xCCCCCC/0x000000/60_60-0.png
    # Black Shield, Grey Icon
    path = f"/1/{i}/0xCCCCCC/0x000000/60_60-0.png"
    download_via_proxy(path, f"backgrounds/{i}.png")

print("--- Downloading Motifs via Proxy ---")
for i in range(1, MAX_MOTIFS + 1):
    # Path: /ID/1/0xFFFFFF/0x333333/60_60-0.png
    # White Icon, Grey Shield
    path = f"/{i}/1/0xFFFFFF/0x333333/60_60-0.png"
    download_via_proxy(path, f"motifs/{i}.png")

print("--- Harvest Complete ---")
