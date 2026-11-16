import os, math

p_dir = "C:/Users/jaden/Downloads/PWC-Check/PWC/scripts"
for fn in ["quantify_pt_c.py", "quantify_pt_d.py"]:
    fp = os.path.join(p_dir, fn)
    if os.path.exists(fp):
        print("=" * 84)
        print(" FILE: " + fp)
        print("=" * 84)
        with open(fp, "r", encoding="utf-8", errors="replace") as f:
            print(f.read()[:4500])
