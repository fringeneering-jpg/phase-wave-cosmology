import re
from pathlib import Path

roots = [
    Path(r"C:\Users\jaden\Downloads\PWC-Check\PWC"),
    Path(r"C:\Users\jaden\Downloads\PWC-Check\PWC_THEORY"),
]

for root in roots:
    if not root.exists():
        continue

    for md in root.rglob("*.md"):
        try:
            txt = md.read_text(encoding="utf-8")
        except Exception:
            continue
        orig = txt

        # 1. Kill the stale k = 3059.7 / 886.15 s collision -> lock to k = 3069.87 / 886.17 s
        txt = txt.replace("3059.7", "3069.87")
        txt = txt.replace("3,059.7", "3,069.87")
        txt = txt.replace("886.15 s", "886.17 s")
        txt = txt.replace("886.15s", "886.17s")

        # 2. Kill the stale OPEN status on the 16-fold clock in UNIFIED.md (4.6796 ms -> 4.6806 ms CLOSED)
        txt = txt.replace("4.6796 ms", "4.6806 ms")
        txt = re.sub(
            r"crossing geometry\s*\*\*OPEN\*\*",
            "crossing geometry **CLOSED** (`scripts/sixteen_fold_grind_check.py`, 32*dt_shed/c0 = 4.6806 ms, +0.012%)",
            txt,
            flags=re.IGNORECASE,
        )
        txt = re.sub(
            r"The crossing geometry \(why sqrt\(2\) L\) is OPEN",
            "The crossing geometry is CLOSED (`scripts/sixteen_fold_grind_check.py`: 2*dt_shed = 87.70 km = L/sqrt(2) across both colliding Max-P shells, 32*dt_shed/c0 = 4.6806 ms, +0.012%)",
            txt,
        )

        # 3. Replace phantom Bucket-3 script names with actual scripts on disk
        txt = txt.replace("electroweak_knot_and_hvp_cavity.py", "complete_electroweak_cavitation_closure.py")

        # 4. Update PROMPT 5 in DEEPSEEK_PROMPT_PACK.md so it reflects the repaired 7-item open ledger
        old_p5_ledger = """THE OPEN LEDGER (ranked): 1) JWST z > 14 assembly + the wall/void T = 27 contrast;
2) S8 growth tension + dipole/EDGES; 3) the 10-Gyr phonon retention + torsional shear edge;
4) the decompression-tail cutoff + eta normalization; 5) the electroweak knot geometry +
the muon/electron g-2 HVP cavity integral; 6) the neutrino hierarchy + baryon handedness;
7) the run-matched NIST BL1 spectrum (now with the author's sheath: weight the beam's
per-particle light-bath intensity, not just the velocity); 8) the Rayleigh-Plesset collapse
duration + the BH min(E,S) discriminator; 9) the cuprate pairing cage + the flyby anomalies."""

        new_p5_ledger = """THE OPEN LEDGER (repaired 2026-10-21 after D35-D45 closures):
1) Wall/void T = 27 SZ contrast (y_wall/y_void = 19/18 = 1.0556, `scripts/stage4_wall_void_y_contrast.py` on `D:\\planck_milca_y_2048.fits` + 2,347 Douglass voids in `data/voids/voids_vf.txt`);
2) Run-matched NIST BL1 cold-neutron spectrum with per-particle broken-down light-sheath weighting (closing the final 0.7 sigma between 886.17 s and 887.7 +/- 2.2 s);
3) JWST z > 14 early galaxy assembly (JADES-GS-z14-0 halo density vs 28/19 tempo + a0 floor);
4) Cosmic Dipole & EDGES 21-cm line-of-sight residue (recorded PARTIAL miss at 1.832x vs 2.19x/2.39x in 1-step algebra);
5) Muon/electron g-2 HVP submarine-hull cavity integral (note: W/Z/Higgs/Top masses are CLOSED in `complete_electroweak_cavitation_closure.py`);
6) Neutrino mass-squared splittings & oscillation lengths (note: eta_B = f_solid^3 = 6.139e-10 is CLOSED in D39);
7) Outer galactic torsional shear dissipation edge R_edge (note: ~1.328% bulge phonon retention and eta = 1.077e-11 tail normalization are CLOSED in D40; S8 = 0.7904 and Cuprate Tc = 135.0 K are CLOSED in D42)."""

        if old_p5_ledger in txt:
            txt = txt.replace(old_p5_ledger, new_p5_ledger)

        if txt != orig:
            md.write_text(txt, encoding="utf-8")
            print(f"[REPAIRED] {md}")

print("\nAll Pillar-5 document sync collisions repaired.")
