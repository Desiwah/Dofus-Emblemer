import os
import requests
import concurrent.futures

# --- CONFIGURATION ---
MAX_BACKGROUNDS = 100
MAX_MOTIFS = 2000
MAX_THREADS = 20  # How many downloads at once?

PROXY_BASE = "https://corsproxy.io/?"
ANKAMA_BASE = "https://static.ankama.com/dofus/renderer/emblem"
ASSET_DIR = "assets"

os.makedirs(f"{ASSET_DIR}/backgrounds", exist_ok=True)
os.makedirs(f"{ASSET_DIR}/motifs", exist_ok=True)

def process_image(args):
    id, type_name = args
    
    # Define paths based on type
    if type_name == 'background':
        ankama_path = f"/1/{id}/0xCCCCCC/0x000000/60_60-0.png"
        save_path = f"{ASSET_DIR}/backgrounds/{id}.png"
    else:
        ankama_path = f"/{id}/1/0xFFFFFF/0x333333/60_60-0.png"
        save_path = f"{ASSET_DIR}/motifs/{id}.png"

    # Skip if exists
    if os.path.exists(save_path):
        return f"[SKIP] {save_path}"

    target_url = PROXY_BASE + ANKAMA_BASE + ankama_path
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        # 3 second timeout is plenty if running parallel
        r = requests.get(target_url, headers=headers, timeout=3)
        
        if r.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(r.content)
            return f"[OK] {save_path}"
        else:
            return f"[MISSING] {save_path}" # Silent fail for gaps
            
    except:
        return f"[TIMEOUT] {save_path}"

def run_harvest():
    print(f"--- STARTING MULTI-THREADED HARVEST ({MAX_THREADS} threads) ---")
    
    # Prepare list of tasks
    tasks = []
    
    # Add Backgrounds to queue
    for i in range(1, MAX_BACKGROUNDS + 1):
        tasks.append((i, 'background'))
        
    # Add Motifs to queue
    for i in range(1, MAX_MOTIFS + 1):
        tasks.append((i, 'motif'))

    print(f"Queue size: {len(tasks)} images. Processing...")

    # Run in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        results = executor.map(process_image, tasks)
        
        # Print results as they come in
        for result in results:
            # Only print OK to keep logs clean, or print everything if you want to see speed
            if "[OK]" in result:
                print(result, flush=True)

    print("--- JOB DONE ---")

if __name__ == "__main__":
    run_harvest()
