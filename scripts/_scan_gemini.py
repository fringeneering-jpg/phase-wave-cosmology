import os, re
roots = [r"C:\Users\jaden\AppData\Roaming\gemini"]
terms = ["black hole", "black-hole", "phase wave", "pwc", "proton", "knot", "14:38", "max-p", "cold-weld", "chiral", "untie", "fringeneering"]
pat = re.compile("|".join(terms), re.IGNORECASE)
seen = set()
out = []
for root in roots:
    for dirpath, dirs, files in os.walk(root):
        for fn in files:
            p = os.path.join(dirpath, fn)
            try:
                if os.path.getsize(p) > 30_000_000:
                    continue
                with open(p, "rb") as f:
                    data = f.read()
            except Exception:
                continue
            if not data:
                continue
            try:
                text = data.decode("utf-8", errors="ignore")
            except Exception:
                text = data.decode("latin-1", errors="ignore")
            if pat.search(text):
                for m in pat.finditer(text):
                    s = max(0, m.start()-120)
                    e = min(len(text), m.end()+160)
                    snippet = re.sub(r"\s+", " ", text[s:e])
                    key = (p, m.group(0))
                    if key not in seen:
                        seen.add(key)
                        out.append((p, m.group(0), snippet))
for p, term, snip in out[:60]:
    print("FILE:", p)
    print("  TERM:", term)
    print("  CTX :", snip[:280])
    print()
print("TOTAL:", len(out))
