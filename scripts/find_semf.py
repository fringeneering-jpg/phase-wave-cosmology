import os

roots = [
    "C:/Users/jaden/Downloads/PWC-Check",
    "C:/Users/jaden/cosmology"
]

keywords = ["343.8", "-0.012", "57/40", "57.0 / 40.0", "a_C", "Ar-40", "Ni-58"]
matches = []

for r in roots:
    if not os.path.exists(r): continue
    for root, dirs, files in os.walk(r):
        if ".venv" in root or "site-packages" in root or ".git" in root:
            continue
        for fn in files:
            if fn.endswith((".py", ".js", ".mjs", ".md")):
                fp = os.path.join(root, fn)
                try:
                    with open(fp, "r", encoding="utf-8", errors="replace") as f:
                        txt = f.read()
                    hits = [k for k in keywords if k in txt]
                    if len(hits) >= 2 and fn not in ("run_coulomb_pb208_test.py", "shell_20_28_falsifier.py", "update_all_and_sparc.py"):
                        matches.append((len(hits), hits, fp, txt))
                except Exception:
                    pass

matches.sort(key=lambda x: x[0], reverse=True)
print("=" * 84)
print(f" FOUND {len(matches)} FILES MATCHING PERIODIC TABLE / COULOMB KEYWORDS")
print("=" * 84)
for count, hits, fp, txt in matches[:6]:
    print(f"\n>>> FILE: {fp} (Hits: {hits})")
    if fp.endswith(".py") or fp.endswith(".js"):
        print(txt[:4000])
    else:
        for line in txt.splitlines():
            if any(k in line for k in keywords):
                print("  " + line[:200])
