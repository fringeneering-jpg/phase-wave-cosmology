import os
import re
import urllib.parse
import requests
from bs4 import BeautifulSoup

output_dir = r"C:\Users\jaden\pwc_geo_test\refs"
os.makedirs(output_dir, exist_ok=True)

base_url = "https://groups.physics.ox.ac.uk/atlas3d/"
tables_page = urllib.parse.urljoin(base_url, "tables.html")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("=== ACCESSING OXFORD ATLAS3D REPOSITORY ===")
res = requests.get(tables_page, headers=headers, timeout=30)
if res.status_code != 200:
    print(f"Failed to access {tables_page}, status: {res.status_code}")
    exit(1)

soup = BeautifulSoup(res.text, "html.parser")
links = soup.find_all("a", href=True)

# Look for Paper XV / Paper 15 / Cappellari 2013 tables
target_links = []
for a in links:
    href = a['href']
    text = a.get_text().strip()
    full_url = urllib.parse.urljoin(tables_page, href)
    
    # Catch any table link associated with Paper XV or 2013a
    if any(k in href.lower() for k in ["paper15", "cappellari2013", "table1", "jam", "scaling"]):
        target_links.append((href, full_url))
    elif any(k in text.lower() for k in ["table 1", "paper xv", "scaling relations"]):
        target_links.append((href, full_url))

print(f"Found {len(target_links)} candidate data links:")
for href, url in target_links:
    print(f" -> {href} ({url})")

# Download all matching candidate files
downloaded = 0
for href, url in target_links:
    fname = os.path.basename(urllib.parse.urlparse(url).path)
    if not fname:
        continue
    out_file = os.path.join(output_dir, f"oxford_{fname}")
    try:
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code == 200 and len(r.content) > 200:
            with open(out_file, "wb") as f:
                f.write(r.content)
            print(f"[SAVED] {fname} ({len(r.content):,} bytes) -> {out_file}")
            downloaded += 1
    except Exception as e:
        print(f"Error downloading {url}: {e}")

if downloaded == 0:
    print("\nScanning raw HTML content for inline Table 1 text or alternative links...")
    # Save the full page text as backup reference to check anchors
    with open(os.path.join(output_dir, "atlas3d_oxford_tables_page.html"), "w", encoding="utf-8") as f:
        f.write(res.text)
    print("Saved tables.html source to refs for inspection.")

print("\n=== CURRENT REFS INVENTORY ===")
for f in sorted(os.listdir(output_dir)):
    fp = os.path.join(output_dir, f)
    print(f" {f:<38}: {os.path.getsize(fp):>10,} bytes")
