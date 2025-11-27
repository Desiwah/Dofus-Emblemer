import os
import requests
import concurrent.futures

# --- CONFIGURATION ---
MAX_BACKGROUNDS = 100 
MAX_MOTIFS = 2000
MAX_THREADS = 50  # 50 downloads at once. This solves the speed issue.

# We use corsproxy.io as you requested
PROXY_BASE = "https://corsproxy.io/?"
ANKAMA_BASE = "https://static.ankama.com/dofus/renderer/emblem"
ASSET_DIR = "assets"

# Ensure folders exist
os.makedirs(f"{ASSET_DIR}/backgrounds", exist_ok=True)
os.makedirs(f"{ASSET_DIR}/motifs", exist_ok=True)

def process_image(args):
    id_num, type_name = args
    
    # Define paths
    if type_name == 'background':
        ankama_path = f"/1/{id_num}/0xCCCCCC/0x000000/60_60-0.png"
        save_path = f"{ASSET_DIR}/backgrounds/{id_num}.png"
    else:
        ankama_path = f"/{id_num}/1/0xFFFFFF/0x333333/60_60-0.png"
        save_path = f"{ASSET_DIR}/motifs/{id_num}.png"

    # Optimization: Skip if we already have it
    if os.path.exists(save_path):
        return None 

    target_url = PROXY_BASE + ANKAMA_BASE + ankama_path
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
    }

    # RETRY LOGIC (Try twice)
    for attempt in range(2):
        try:
            # 3 Second Timeout. If it hangs, we kill it.
            r = requests.get(target_url, headers=headers, timeout=3)
            
            if r.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(r.content)
                return f"[OK] {save_path}"
            
            # If 404 (Missing), break loop immediately, don't retry
            elif r.status_code == 404:
                return None 
            
        except:
            # On timeout/error, loop continues to attempt #2
            pass

    # If we reach here, both attempts failed/timed out. 
    # We silently skip to keep the logs clean and speed up.
    return None

def run_harvest():
    print(f"--- STARTING AGGRESSIVE HARVEST ({MAX_THREADS} Threads) ---")
    
    # 1. Build the Task List
    tasks = []
    
    # Add Backgrounds
    for i in range(1, MAX_BACKGROUNDS + 1):
        tasks.append((i, 'background'))
        
    # Add Motifs
    for i in range(1, MAX_MOTIFS + 1):
        tasks.append((i, 'motif'))

    print(f"Queue size: {len(tasks)} images. Processing...")

    # 2. Run in Parallel
    # This executes 50 items at once. Even if one hangs, the others finish.
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        results = executor.map(process_image, tasks)
        
        # Print results as they come in
        count = 0
        for result in results:
            if result:
                print(result, flush=True)
                count += 1

    print(f"--- JOB DONE. Downloaded {count} images. ---")

if __name__ == "__main__":
    run_harvest()
