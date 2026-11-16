import os

PWC_ROOTS = [
    "C:/Users/jaden/Downloads/PWC-Check/PWC",
    "C:/Users/jaden/Downloads/PWC-Check/PWC_THEORY"
]

ADDITION = """

### The GR-Prior Strip & Primary-Distance Split (`scripts/run_stripped_vizier.py`, CLOSED 2026-10-22)

When the full VizieR SPARC catalog (`vizier_t1.txt` / `vizier_t2.txt`, 166 galaxies, 2,807 quality-filtered points with $e_{V}/V \\le 0.10$) is stripped of all General Relativity and $\\Lambda$CDM mass-modeling priors ($V_{\\text{bulge}} = 0$, $L_{3.6}$ mass-to-light fitting removed, locked strictly to $\\Upsilon_D = 1 - 2\\Delta\\rho_{\\text{geom}} = 0.51375$ and $a_0 = \\phi a_{0,\\text{bare}} = 1.0695 \\times 10^{-10}\\text{ m/s}^2$):

1. **Full 166-Galaxy Stripped Catalog (2,807 points):** Point RMS = **0.2911 dex**, Galaxy-Balanced RMS = **0.1845 dex**.
2. **Primary Geometric Distances Only ($f_{\\text{Dist}} \\ge 2$, stripping $\\Lambda$CDM Hubble-flow distance priors — 75 galaxies, 1,146 points):** Point RMS drops by nearly 0.10 dex to **0.1925 dex**, and Galaxy-Balanced RMS drops to **0.1633 dex**. The largest apparent outliers in the raw table (`UGC05253`, `UGC06787`, `UGC02916`, `F561-1`, `UGC11914`) are overwhelmingly $f_{\\text{Dist}} = 1$ Hubble-flow distance artifacts.
3. **Blind Out-of-Sample Local Group / M81 Group Anchors ($-2$ fits, $V_b = 0$):**
   - **M33 (NGC 0598):** $N = 20$, **RMS = 0.0580 dex** ($R_{\\text{out}} = 22.7\\text{ kpc}$, $V_{\\text{obs}} = 135\\text{ km/s}$, $V_{\\text{pred}} = 147\\text{ km/s}$).
   - **M81 (NGC 3031):** $N = 16$, **RMS = 0.0367 dex** ($R_{\\text{out}} = 21.8\\text{ kpc}$, $V_{\\text{obs}} = 200\\text{ km/s}$, $V_{\\text{pred}} = 194\\text{ km/s}$).
"""

patched = set()
for base in PWC_ROOTS:
    if not os.path.exists(base):
        continue
    for root, _, files in os.walk(base):
        for fn in files:
            if fn in ("PHASE_WAVE_COSMOLOGY_UNIFIED.md", "UNIVERSE_QUANTIFICATION.md"):
                fp = os.path.abspath(os.path.join(root, fn))
                if fp in patched:
                    continue
                with open(fp, "r", encoding="utf-8") as f:
                    txt = f.read()
                if "The GR-Prior Strip & Primary-Distance Split" not in txt:
                    txt += ADDITION
                    with open(fp, "w", encoding="utf-8") as f:
                        f.write(txt)
                    print("[+] Patched: " + fp)
                patched.add(fp)
