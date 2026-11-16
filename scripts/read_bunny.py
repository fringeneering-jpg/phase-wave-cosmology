import os, math

roots = [
    "C:/Users/jaden/Downloads/PWC-Check/PWC",
    "C:/Users/jaden/Downloads/PWC-Check/PWC_THEORY"
]

# 1. Print exact contents of nuclear_force_bunny.py so we use your exact locked SEMF baseline
for r in roots:
    p = os.path.join(r, "scripts", "nuclear_force_bunny.py")
    if os.path.exists(p):
        print("=" * 84)
        print(" FOUND LOCKED BASELINE: " + p)
        print("=" * 84)
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            print(f.read())
        break
