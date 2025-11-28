import os
import requests
import time
import random

# --- CONFIG ---
BASE_URL = "https://static.ankama.com/dofus/renderer/emblem"
MIN_DELAY = 3.0
MAX_DELAY = 7.0
SCAN_AHEAD_BG = 10     # try next 10 IDs only
SCAN_AHEAD_MOTIF = 50  # try next 50 IDs only

os.makedirs("assets/backgrounds", exist_ok=True)
os.makedirs("assets/motifs", exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "image/*",
    "Referer": "https://www.dofus.com/",
    "Connection": "keep-alive"
}

PROXY_URL = os.getenv("PROXY_URL", None)
PROXIES = {"http": PROXY_URL, "https": PROXY_URL} if PROXY_URL else None

def last_local_id(folder):
    ids = [int(f.split(".")[0]) for f in os.listdir(folder) if f.endswith(".png")]
    return max(ids) if ids else 0

def download(url, path):
    print(f"[?] {path}")
    try:
        r = requests.get(url, headers=HEADERS, proxies=PROXIES, timeout=15)
        if r.status_code == 200 and len(r.content) > 1000:
            with open(path, "wb") as f:
                f.write(r.content)
            print(f" -> Saved")
            return True
        if r.status_code == 404:
            print(" -> 404")
            return False
        print(f" -> HTTP {r.status_code}")
        return False
    except Exception as e:
        print(f" -> Error: {e}")
        return False
    finally:
        time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

def sync(folder, start, count, bg=False):
    ids = list(range(start, start + count))
    random.shuffle(ids)

    found_new = False
    for i in ids:
        if bg:
            url = f"{BASE_URL}/1/{i}/0xCCCCCC/0x000000/60_60-0.png"
            path = f"assets/backgrounds/{i}.png"
        else:
            url = f"{BASE_URL}/{i}/1/0xFFFFFF/0x333333/60_60-0.png"
            path = f"assets/motifs/{i}.png"

        if not os.path.exists(path):
            ok = download(url, path)
            if ok:
                found_new = True
            else:
                break  # stop early when discovery stops
    return found_new

# --- MAIN ---
last_bg = last_local_id("assets/backgrounds")
last_motif = last_local_id("assets/motifs")

print(f"Last BG: {last_bg} | Last Motif: {last_motif}")

updated = False
updated |= sync("assets/backgrounds", last_bg + 1, SCAN_AHEAD_BG, bg=True)
updated |= sync("assets/motifs", last_motif + 1, SCAN_AHEAD_MOTIF)

if not updated:
    print("No new assets discovered.")
else:
    print("New assets added.")
