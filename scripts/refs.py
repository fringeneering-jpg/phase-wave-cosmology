import os
import requests

output_dir = r"C:\Users\jaden\pwc_geo_test\refs"
os.makedirs(output_dir, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# The two remaining tables needed to complete Kill #3
targets = {
    # Paper XV: Dynamical masses, velocity dispersions (sigma_e)
    "atlas3d_paper15_dyn.tsv": "http://ftp.bao.ac.cn/viz-bin/asu-tsv?-source=J/MNRAS/432/1709/table1&-out.max=unlimited",
    # Paper XVII: Multi-Gaussian expansion / photometric profiles & Sersic indices
    "atlas3d_sersic_profiles.tsv": "http://ftp.bao.ac.cn/viz-bin/asu-tsv?-source=J/MNRAS/432/1768/tablec1&-out.max=unlimited"
}

print("=== FETCHING FINAL ATLAS3D PIECES VIA BEIJING ===")
for filename, url in targets.items():
    out_path = os.path.join(output_dir, filename)
    print(f" -> Fetching {filename}...")
    try:
        res = requests.get(url, headers=headers, timeout=45)
        print(f"    Status: {res.status_code} | Bytes: {len(res.text)}")
        if res.status_code == 200 and len(res.text) > 3000 and "<html" not in res.text[:400].lower():
            with open(out_path, "w", encoding="utf-8", errors="ignore") as f:
                f.write(res.text)
            print(f"    [LOCKED!] Saved {filename} ({len(res.text)} bytes)")
        else:
            print(f"    [FAILED] Invalid payload: {res.text[:100].strip()}")
    except Exception as e:
        print(f"    [ERROR] {e}")

print("\n--- FINAL REFS AUDIT ---")
for f in os.listdir(output_dir):
    fp = os.path.join(output_dir, f)
    print(f"  {f}: {os.path.getsize(fp):,} bytes")
