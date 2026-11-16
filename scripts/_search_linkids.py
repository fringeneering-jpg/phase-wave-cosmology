import os, re
ids = ["15Q9kLfNg", "18OzNyt9", "1AC6B025", "1Elr7h7U", "1I8B8Bzk", "1N1T_x4F", "1QzqHtyR", "1SIjj1-1", "1bjqh5NN"]
roots = [
  r"C:\Users\jaden\AppData\Roaming\gemini",
  r"C:\Users\jaden\AppData\Local\Google\Gemini",
  r"C:\Users\jaden\Desktop",
  r"C:\Users\jaden\Documents",
]
hits = {}
for root in roots:
    for dirpath, dirs, files in os.walk(root):
        # skip giant cache dirs except Network/CacheStorage
        for fn in files:
            p = os.path.join(dirpath, fn)
            try:
                if os.path.getsize(p) > 30_000_000: continue
                with open(p, "rb") as f:
                    data = f.read()
            except Exception:
                continue
            try: text = data.decode("utf-8", errors="ignore")
            except: text = data.decode("latin-1", errors="ignore")
            for i in ids:
                if i in text:
                    hits.setdefault(p, set()).add(i)
for p, found in sorted(hits.items()):
    print("FILE:", p)
    print("  IDs:", sorted(found))
print("TOTAL HIT FILES:", len(hits))
# also list Downloads top-level files modified today
print("--- Downloads top-level modified today ---")
for fn in os.listdir(r"C:\Users\jaden\Downloads"):
    p = os.path.join(r"C:\Users\jaden\Downloads", fn)
    try:
        if os.path.isfile(p) and os.path.getmtime(p) > 1792483200:  # 2026-10-20 approx
            print("  ", fn, os.path.getsize(p))
    except Exception:
        pass
print("DONE")
