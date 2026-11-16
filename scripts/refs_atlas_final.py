import os
import requests

output_dir = r"C:\Users\jaden\pwc_geo_test\refs"
os.makedirs(output_dir, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# The verified VizieR catalog tables for ATLAS3D
atlas_targets = {
    "atlas3d_sample.tsv": "http://ftp.bao.ac.cn/viz-bin/asu-tsv?-source=J/MNRAS/413/813/atlas3d&-out.max=unlimited",
    "atlas3d_kinematics.tsv": "http://ftp.bao.ac.cn/viz-bin/asu-tsv?-source=J/MNRAS/414/888/tableb1&-out.max=unlimited",
    "atlas3d_stellar_mass.tsv": "http://ftp.bao.ac.cn/viz-bin/asu-tsv?-source=J/MNRAS/448/3484/table4&-out.max=unlimited"
}

print("=== FETCHING VERIFIED ATLAS3D SYSTEM TABLES ===")
for filename, url in atlas_targets.items():
    out_path = os.path.join(output_dir, filename)
    print(f" -> Pulling {filename}...")
    try:
        res = requests.get(url, headers=headers, timeout=40)
        lines = [l for l in res.text.splitlines() if not l.startswith('#') and l.strip()]
        print(f"    Status: {res.status_code} | Total Bytes: {len(res.text):,} | Data Rows: {len(lines)}")
        if res.status_code == 200 and len(res.text) > 3000 and "Error=" not in res.text:
            with open(out_path, "w", encoding="utf-8", errors="ignore") as f:
                f.write(res.text)
            print(f"    [LOCKED!] Saved to {out_path}")
        else:
            print(f"    [FAILED] Rejected. Preview: {res.text[:120].strip()}")
    except Exception as e:
        print(f"    [ERROR] {e}")

print("=== VERIFYING REFS INVENTORY ===")
for f in sorted(os.listdir(output_dir)):
    fp = os.path.join(output_dir, f)
    print(f" {f:<32}: {os.path.getsize(fp):>9,} bytes")
