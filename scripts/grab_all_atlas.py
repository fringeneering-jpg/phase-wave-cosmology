import os
import re
import requests

output_dir = r"C:\Users\jaden\pwc_geo_test\refs"
os.makedirs(output_dir, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# The exact archive directories on the open Beijing mirror
catalogs = [
    "http://ftp.bao.ac.cn/ftp/cats/J/MNRAS/432/1709/",  # Paper XV: Dynamical masses & JAM
    "http://ftp.bao.ac.cn/ftp/cats/J/MNRAS/432/1768/",  # Paper XVII: Kinematics & morphology
    "http://ftp.bao.ac.cn/ftp/cats/J/MNRAS/433/2812/"   # Paper XXIII: Photometric decomposition / profiles
]

print("=== SWEEPING ENTIRE CATALOG REPOSITORIES ===")

for cat_url in catalogs:
    cat_name = cat_url.strip("/").split("/")[-1]
    print(f"\n--- Checking catalog directory: {cat_name} ---")
    try:
        r = requests.get(cat_url, headers=headers, timeout=20)
        if r.status_code != 200:
            print(f"Directory index returned status {r.status_code}")
            continue
        
        # Parse all links pointing to .dat, .txt, or ReadMe files
        filenames = re.findall(r'href=[\"\\\']([a-zA-Z0-9_\-\.]+\.(?:dat|txt|tsv)|ReadMe)[\"\\\']', r.text, re.IGNORECASE)
        filenames = list(set(filenames))
        
        if not filenames:
            print("No raw data tables found in standard directory listing.")
            continue
            
        print(f"Found {len(filenames)} files: {', '.join(filenames)}")
        for fn in filenames:
            file_url = f"{cat_url}{fn}"
            dest = os.path.join(output_dir, f"atlas3d_{cat_name}_{fn.lower()}")
            print(f" -> Downloading {fn}...")
            fres = requests.get(file_url, headers=headers, timeout=30)
            if fres.status_code == 200 and len(fres.content) > 50:
                with open(dest, "wb") as f:
                    f.write(fres.content)
                print(f"    Saved {len(fres.content):,} bytes -> {dest}")
    except Exception as e:
        print(f"Error accessing {cat_url}: {e}")

print("\n=== FINAL REFS INVENTORY ===")
for f in sorted(os.listdir(output_dir)):
    fp = os.path.join(output_dir, f)
    print(f" {f:<38}: {os.path.getsize(fp):>10,} bytes")
