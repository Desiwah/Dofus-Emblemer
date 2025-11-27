import os
import requests
import concurrent.futures

# CONFIG
MAX_BACKGROUNDS = 200 
MAX_MOTIFS = 1200
MAX_THREADS = 20
PROXY_BASE = "https://corsproxy.io/?"
ANKAMA_BASE = "https://static.ankama.com/dofus/renderer/emblem"

# !!! IMPORTANT: Save inside 'assets' folder !!!
ASSET_DIR = "assets"
os.makedirs(f"{ASSET_DIR}/backgrounds", exist_ok=True)
os.makedirs(f"{ASSET_DIR}/motifs", exist_ok=True)

def process_image(args):
    id_num, type_name = args
    
    if type_name == 'background':
        ankama_path = f"/1/{id_num}/0xCCCCCC/0x000000/60_60-0.png"
        save_path = f"{ASSET_DIR}/backgrounds/{id_num}.png"
    else:
        ankama_path = f"/{id_num}/1/0xFFFFFF/0x333333/60_60-0.png"
        save_path = f"{ASSET_DIR}/motifs/{id_num}.png"

    if os.path.exists(save_path):
        return None

    # Headers for Proxy
    headers = {'User-Agent': 'Mozilla/5.0'}
    target_url = PROXY_BASE + ANKAMA_BASE + ankama_path

    try:
        r = requests.get(target_url, headers=headers, timeout=5)
        if r.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(r.content)
            return f"[OK] {save_path}"
    except:
        pass
    return None

def run_harvest():
    print("--- STARTING HARVEST TO 'assets/' ---")
    tasks = []
    for i in range(1, MAX_BACKGROUNDS + 1): tasks.append((i, 'background'))
    for i in range(1, MAX_MOTIFS + 1): tasks.append((i, 'motif'))

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        results = executor.map(process_image, tasks)
        for res in results:
            if res: print(res, flush=True)

if __name__ == "__main__":
    run_harvest()
