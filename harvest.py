import os
import requests
import time
import random

# --- CONFIG ---
BASE_URL = "https://static.ankama.com/dofus/renderer/emblem"
MIN_DELAY = 3.0
MAX_DELAY = 8.0

# How far ahead to look for new assets each run
SCAN_AHEAD_BG = 30
SCAN_AHEAD_MOTIF = 100

os.makedirs("assets/backgrounds", exist_ok=True)
os.makedirs("assets/motifs", exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "image/*",
    "Referer": "https://www.dofus.com/",
}

PROXY_URL = os.getenv("PROXY_URL", None)
PROXIES = {"http": PROXY_URL, "https": PROXY_URL} if PROXY_URL else None


def last_local_id(folder):
    ids = [int(f.split(".")[0]) for f in os.listdir(folder) if f.endswith(".png")]
    return max(ids) if ids else 0


def download(url, path):
    try:
        r = requests.get(url, headers=HEADERS, proxies=PROXIES, timeout=15)
        status = r.status_code

        if status == 200 and len(r.content) > 1000:
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"[OK] {path}")
            return True

        print(f"[MISS {status}] {path}")
        return None  # missing asset → continue scanning

    except Exception as e:
        print(f"[ERROR] {path} -> {e}")
        return None  # do not stop scanning

    finally:
        time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))


def sync(folder, start, count, bg=False):
    ids = list(range(start, start + count))
    random.shuffle(ids)

    found_any = False

    for i in ids:
        if bg:
            url = f"{BASE_URL}/1/{i}/0xCCCCCC/0x000000/60_60-0.png"
            path = f"assets/backgrounds/{i}.png"
        else:
            url = f"{BASE_URL}/{i}/1/0xFFFFFF/0x333333/60_60-0.png"
            path = f"assets/motifs/{i}.png"

        if not os.path.exists(path):
            result = download(url, path)
            if result is True:
                found_any = True

    return found_any


# --- MAIN ---
last_bg = last_local_id("assets/backgrounds")
last_motif = last_local_id("assets/motifs")

print(f"Last background: {last_bg}")
print(f"Last motif: {last_motif}")

updated = False
updated |= sync("assets/backgrounds", last_bg + 1, SCAN_AHEAD_BG, bg=True)
updated |= sync("assets/motifs", last_motif + 1, SCAN_AHEAD_MOTIF)

if updated:
    print("New assets added.")
else:
    print("No new assets discovered.")
