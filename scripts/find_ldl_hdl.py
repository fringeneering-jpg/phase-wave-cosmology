import os

roots = [
    "C:/Users/jaden/Downloads/PWC-Check",
    "C:/Users/jaden/cosmology"
]

keywords = ["LDL", "HDL", "low-density", "high-density", "two-state", "water", "cavitation"]
for r in roots:
    if not os.path.exists(r): continue
    for root, _, files in os.walk(r):
        if ".venv" in root or ".git" in root or "site-packages" in root: continue
        for fn in files:
            if fn.endswith((".md", ".py", ".txt", ".tex")):
                fp = os.path.join(root, fn)
                try:
                    with open(fp, "r", encoding="utf-8", errors="replace") as f:
                        txt = f.read()
                    hits = [k for k in ["LDL", "HDL", "low-density liquid", "high-density liquid"] if k.lower() in txt.lower()]
                    if hits:
                        print(f">>> HIT in {fp}: {hits}")
                        for line in txt.splitlines():
                            if any(h.lower() in line.lower() for h in hits):
                                print("   ", line[:160])
                except Exception:
                    pass
