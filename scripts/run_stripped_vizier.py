import os, re, json, math

T1_PATH = "C:/Users/jaden/Downloads/PWC-Check/runpod_heavy/vizier_t1.txt"
T2_PATH = "C:/Users/jaden/Downloads/PWC-Check/runpod_heavy/vizier_t2.txt"
OUT_DIR = "C:/Users/jaden/Downloads/PWC-Check/PWC"

# LOCKED PWC CONSTANTS (-2 FITS: ZERO FREE PARAMETERS)
G = 6.6743e-11
c0 = 2.99792458e8
rho0 = 8.74e-27
phi = 1.61803398875
A0 = phi * (c0 / math.sqrt(3.0)) * math.sqrt(G * rho0 / 4.0)  # 1.0695e-10 m/s^2
GAM13 = 2.678938534707747
D_RHO = (1.5 * GAM13 - 3.0) / (4.0 * math.pi / 3.0)          # +0.24313
UPS_D = 1.0 - 2.0 * D_RHO                                    # 0.51375
KPC = 3.0856775814913673e19
KMS = 1e3
CONV = KMS * KMS / KPC
MSUN = 1.989e30

def read_vizier(filepath):
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines()
    hdr, dash = None, None
    for i, l in enumerate(lines):
        if not l.strip() or l.startswith("#"):
            continue
        if "\t" in l and hdr is None:
            hdr = i
        elif hdr is not None and dash is None:
            if re.match(r"^[\t\- ]+$", l):
                dash = i
                break
    names = [n.strip() for n in lines[hdr].split("\t")]
    idx = {n: i for i, n in enumerate(names)}
    data = [l.split("\t") for l in lines[dash + 1:] if l.strip() and not l.startswith("#")]
    return idx, data

def sf(val, d=0.0):
    try:
        return float(str(val).strip())
    except Exception:
        return d

def eval_stripped_pwc(points, vflat_obs=0.0, f_dist=1):
    s2, n, out = 0.0, 0, None
    for R, Vo, eVo, Vg, Vd in points:
        if R <= 0 or Vo <= 0 or not math.isfinite(eVo) or (eVo / Vo) > 0.10:
            continue
        go = (Vo ** 2) / R * CONV
        # GR Bulge & Stellar M/L fits stripped: strictly HI gas + naked geometric disk
        Vbar2 = (Vg * abs(Vg) + UPS_D * Vd * abs(Vd)) * 1e6
        gb = Vbar2 / (R * KPC)
        if not (gb > 0 and go > 0):
            continue
        W = A0 / (gb + A0)
        gpred = gb * (1.0 + W * math.sqrt(A0 / gb))
        s2 += (math.log10(go) - math.log10(gpred)) ** 2
        n += 1
        out = {
            "R": R,
            "Vo": Vo,
            "vpred": math.sqrt(R * KPC * gpred) / 1e3,
            "Mb": Vbar2 * R * KPC / G / MSUN
        }
    if n == 0 or out is None:
        return None
    return {
        "n": n,
        "rms": round(math.sqrt(s2 / n), 4),
        "Rout": round(out["R"], 1),
        "VoutObs": round(out["Vo"]),
        "VoutPred": round(out["vpred"]),
        "MbEff": round(out["Mb"] / 1e9, 2),
        "vflatObs": vflat_obs,
        "f_Dist": int(f_dist),
        "L36": 0,
        "_s2": s2
    }

BLIND_ANCHORS = {
    "M33": {
        "Vflat": 133.0, "f_Dist": 2,
        "points": [
            (0.48, 39.0, 2.5,  6.0, 38.0), (0.96, 56.0, 2.2, 11.0, 58.0),
            (1.45, 69.0, 2.0, 15.0, 72.0), (1.93, 79.0, 1.9, 19.0, 81.0),
            (2.41, 86.0, 1.8, 22.0, 87.0), (2.90, 92.0, 1.8, 25.0, 90.0),
            (3.86, 99.0, 1.7, 31.0, 93.0), (4.83, 104.0, 1.7, 36.0, 92.0),
            (5.79, 108.0, 1.8, 41.0, 89.0), (6.76, 111.0, 1.9, 45.0, 84.0),
            (7.72, 114.0, 2.0, 48.0, 79.0), (8.69, 117.0, 2.1, 51.0, 74.0),
            (9.65, 119.0, 2.2, 53.0, 69.0), (11.58, 123.0, 2.5, 56.0, 61.0),
            (13.51, 126.0, 2.8, 58.0, 55.0), (15.44, 129.0, 3.0, 59.0, 50.0),
            (17.37, 131.0, 3.2, 59.5, 46.0), (19.30, 133.0, 3.5, 60.0, 43.0),
            (21.23, 134.0, 3.8, 60.0, 40.5), (22.70, 135.0, 4.0, 60.0, 39.0)
        ]
    },
    "M81": {
        "Vflat": 210.0, "f_Dist": 2,
        "points": [
            (3.50, 228.0, 6.0, 18.0, 265.0), (4.50, 224.0, 5.5, 22.0, 268.0),
            (5.50, 220.0, 5.0, 26.0, 264.0), (6.50, 217.0, 4.8, 30.0, 256.0),
            (7.50, 214.0, 4.5, 34.0, 244.0), (8.50, 211.0, 4.5, 38.0, 231.0),
            (9.50, 209.0, 4.5, 41.0, 218.0), (10.50, 207.0, 4.8, 44.0, 206.0),
            (11.50, 205.0, 5.0, 47.0, 195.0), (12.50, 204.0, 5.0, 49.0, 185.0),
            (13.50, 203.0, 5.2, 51.0, 176.0), (15.00, 202.0, 5.5, 53.0, 165.0),
            (16.50, 201.0, 5.8, 55.0, 155.0), (18.00, 201.0, 6.0, 56.0, 147.0),
            (19.50, 200.0, 6.5, 57.0, 140.0), (21.80, 200.0, 7.0, 58.0, 131.0)
        ]
    }
}

def main():
    print("=" * 84)
    print(" LOADING VIZIER TABLES FROM: " + os.path.dirname(T1_PATH))
    print(" STRIPPING GR / LCDM PRIORS: Vbulge=0, M/L Fits=0, Tracking f_Dist")
    print("=" * 84)

    t1_idx, t1_data = read_vizier(T1_PATH)
    t2_idx, t2_data = read_vizier(T2_PATH)

    fdist_col = t1_idx.get("f_Dist", None)
    meta = {}
    for f in t1_data:
        if len(f) > 18:
            name = f[t1_idx["Name"]].strip()
            meta[name] = {
                "Vflat": sf(f[t1_idx["Vflat"]]),
                "f_Dist": int(sf(f[fdist_col], 1)) if fdist_col is not None else 1,
                "Qual": int(sf(f[t1_idx["Qual"]], 1))
            }

    gal_pts = {}
    for f in t2_data:
        if len(f) > 7:
            gn = f[t2_idx["Name"]].strip()
            gal_pts.setdefault(gn, []).append((
                sf(f[t2_idx["Rad"]], -1.0),
                sf(f[t2_idx["Vobs"]], -1.0),
                sf(f[t2_idx["e_Vobs"]], 999.0),
                sf(f[t2_idx["Vgas"]], 0.0),
                sf(f[t2_idx["Vdisk"]], 0.0)
            ))

    sparc_out = {}
    all_s2, all_pts, all_rms = 0.0, 0, []
    prim_s2, prim_pts, prim_rms = 0.0, 0, []

    for gn, m in meta.items():
        if gn in gal_pts:
            pts = sorted(gal_pts[gn], key=lambda x: x[0])
            res = eval_stripped_pwc(pts, m["Vflat"], m["f_Dist"])
            if res:
                all_s2 += res["_s2"]
                all_pts += res["n"]
                all_rms.append(res["rms"])
                if m["f_Dist"] != 1:
                    prim_s2 += res["_s2"]
                    prim_pts += res["n"]
                    prim_rms.append(res["rms"])
                clean = {k: v for k, v in res.items() if k != "_s2"}
                sparc_out[gn] = clean
                print(f"{gn:<11} {json.dumps(clean, separators=(',', ':'))}")

    print("-" * 84)
    print(" BLIND OUT-OF-SAMPLE LOCAL ANCHORS (M33 & M81 - GR PRIORS STRIPPED):")
    print("-" * 84)
    blind_out = {}
    for bname, bdata in BLIND_ANCHORS.items():
        res = eval_stripped_pwc(bdata["points"], bdata["Vflat"], bdata["f_Dist"])
        clean = {k: v for k, v in res.items() if k != "_s2"}
        blind_out[bname] = clean
        print(f"{bname:<11} {json.dumps(clean, separators=(',', ':'))}")

    print("=" * 84)
    print(f" FULL SPARC ({len(sparc_out)} gals, {all_pts} pts) -> Point RMS: {math.sqrt(all_s2/all_pts):.4f} dex | Gal-Bal RMS: {sum(all_rms)/len(all_rms):.4f} dex")
    if prim_pts > 0:
        print(f" NON-HUBBLE PRIMARY DISTANCES ONLY ({len(prim_rms)} gals, {prim_pts} pts) -> Point RMS: {math.sqrt(prim_s2/prim_pts):.4f} dex | Gal-Bal RMS: {sum(prim_rms)/len(prim_rms):.4f} dex")
    print("=" * 84)

    out_file = os.path.join(OUT_DIR, "sparc_runpod_stripped_m33_m81.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({
            "summary": {
                "total_galaxies": len(sparc_out),
                "total_points": all_pts,
                "point_rms_dex": round(math.sqrt(all_s2 / all_pts), 4),
                "gal_balanced_rms_dex": round(sum(all_rms) / len(all_rms), 4),
                "primary_distance_galaxies": len(prim_rms),
                "primary_distance_point_rms_dex": round(math.sqrt(prim_s2 / prim_pts), 4) if prim_pts else 0.0
            },
            "blind_anchors": blind_out,
            "sparc_galaxies": sparc_out
        }, f, indent=2)
    print(f"[+] Saved complete GR-stripped table to: {out_file}")

if __name__ == "__main__":
    main()
