import os
import requests

output_dir = r"C:\Users\jaden\pwc_geo_test\refs"
os.makedirs(output_dir, exist_ok=True)

# Headers to mimic a standard browser request and bypass automated API blocks
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Direct raw file URLs for the tables from VizieR mirrors
targets = {
    "atlas3d_cappellari.tsv": "https://cdsarc.cds.unistra.fr/viz-bin/nph-Cat/txt?J/MNRAS/413/813/table1.dat",
    "coma_michard_andreon.tsv": "https://cdsarc.cds.unistra.fr/viz-bin/nph-Cat/txt?J/A+A/490/923/table.dat"
}

for filename, url in targets.items():
    out_path = os.path.join(output_dir, filename)
    print(f"--- FETCHING {filename} ---")
    try:
        response = requests.get(url, headers=headers, timeout=60)
        if response.status_code == 200:
            with open(out_path, "w", encoding="utf-8", errors="ignore") as f:
                f.write(response.text)
            print(f"[SUCCESS] Saved to {out_path} ({len(response.text)} bytes)")
        else:
            print(f"[FAILED] Server returned status code {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Direct pull failed: {e}")

print("\n--- RAW PULL COMPLETE ---")