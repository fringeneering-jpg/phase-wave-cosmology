# -*- coding: utf-8 -*-
"""
grab_all_final.py — EVERYTHING AT ONCE. One run, all tables, no questions.
Tries each candidate catalog ID; for every one that answers, reads its ReadMe,
parses the table filenames, and downloads ALL of them into refs\.
Run it ONCE. It does the whole hunt.
"""
import os
import re
import requests

OUT = r"C:\Users\jaden\pwc_geo_test\refs"
os.makedirs(OUT, exist_ok=True)
HDRS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

BASE = "https://ftp.bao.ac.cn/viz-bin/asu-tsv"

# every candidate catalog for the ATLAS3D benchmark + the photometry/Sersic data
CATS = [
    "J/MNRAS/432/1709",   # Paper XV: the benchmark (sigma_e, M_dyn, M_*)
    "J/MNRAS/432/1894",   # Paper XXI: the 2D photometry / Sersic profiles
    "J/MNRAS/444/3557",   # Paper XXIII alt / Emsellem
    "J/MNRAS/414/888",    # Paper III (the sample photometry)
]

def get(url, timeout=45):
    r = requests.get(url, headers=HDRS, timeout=timeout)
    return r.text if r.status_code == 200 else None

for cat in CATS:
    print(f"\n=== {cat} ===")
    rm = get(f"{BASE}?-source={cat}/ReadMe&-out.max=unlimited")
    if not rm:
        print("  [NO README - catalog not at this ID]")
        continue
    fname = os.path.join(OUT, cat.replace("/", "_") + "_ReadMe.tsv")
    open(fname, "w", encoding="utf-8", errors="ignore").write(rm)
    print(f"  [README SAVED {len(rm)} bytes]")
    # parse the table filenames from the ReadMe (the 'FileName' / table lines)
    tables = set()
    for line in rm.splitlines():
        m = re.search(r"FileSummary|FileName\s+(\S+\.dat)|^ReadMe|^(\S+\.dat)", line)
        for mm in re.finditer(r"\b(table\w*\.dat|table\d+\.dat)\b", line):
            tables.add(mm.group(1))
    if not tables:
        # the A&A ReadMes list tables as "J/A+A/.../<name> <desc>"
        for mm in re.finditer(r"\b([a-z0-9]+\.dat)\b", rm, re.I):
            tables.add(mm.group(1))
    print(f"  tables found: {sorted(tables)}")
    for t in sorted(tables):
        data = get(f"{BASE}?-source={cat}/{t}&-out.max=unlimited")
        if data and "bobcmn" not in data and len(data) > 1500:
            out = os.path.join(OUT, cat.replace("/", "_") + "_" + t + ".tsv")
            open(out, "w", encoding="utf-8", errors="ignore").write(data)
            print(f"    [LOCKED] {t}: {len(data)} bytes")
        else:
            print(f"    [miss] {t}")

print("\n=== THE FULL SWEEP IS DONE. Check refs\\ ===")
print("\n".join(f"  {f} ({os.path.getsize(os.path.join(OUT,f))} bytes)"
               for f in sorted(os.listdir(OUT)) if "432" in f or "444" in f or "414" in f))
