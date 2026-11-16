import os
import requests

output_dir = r"C:\Users\jaden\pwc_geo_test\refs"
os.makedirs(output_dir, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

readmes = {
    "Paper XV (Dynamical)": "http://ftp.bao.ac.cn/viz-bin/asu-tsv?-source=J/MNRAS/432/1709/ReadMe",
    "Paper XXI (Sersic)": "http://ftp.bao.ac.cn/viz-bin/asu-tsv?-source=J/MNRAS/432/1894/ReadMe"
}

print("=== READING ARCHIVE SCHEMAS ===")
for label, url in readmes.items():
    print(f"\n--- {label} ---")
    try:
        res = requests.get(url, headers=headers, timeout=30)
        lines = res.text.splitlines()
        
        # Extract the File Table Section from the CDS ReadMe
        in_file_section = False
        table_lines = []
        for line in lines:
            if "FileName" in line and "Lrecl" in line:
                in_file_section = True
            if in_file_section:
                table_lines.append(line)
                if len(table_lines) > 25:
                    break
        
        if table_lines:
            print("\n".join(table_lines[:20]))
        else:
            # Print first 25 non-empty lines if header differs
            print("\n".join([l for l in lines if l.strip()][:25]))
    except Exception as e:
        print(f"Error fetching {label}: {e}")

print("\n=== COMPLETE ===")
