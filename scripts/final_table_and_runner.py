from pathlib import Path

roots = [
    Path(r"C:\Users\jaden\Downloads\PWC-Check\PWC"),
    Path(r"C:\Users\jaden\Downloads\PWC-Check\PWC_THEORY"),
]

# 1. Update run_full_framework.py hook to include all 8 closures
for root in roots:
    rp = root / "scripts" / "run_full_framework.py"
    if not rp.exists():
        continue
    txt = rp.read_text(encoding="utf-8")
    old_target = '("All 4 external rotation catalogs (-2 fits: PROBES, ALFALFA, GHASP, LT)", "run_all_rotation_catalogs.py"),'
    new_target = (
        old_target
        + '\n        ("D34 Navier-Stokes BKM operational-middle regularity (no 0, no oo)", "navier_stokes_bkm_regularity.py"),'
        + '\n        ("Yang-Mills constructive mass gap & UV finiteness (no 0, no oo)", "yang_mills_mass_gap_proof.py"),'
    )
    if "navier_stokes_bkm_regularity.py" not in txt and old_target in txt:
        txt = txt.replace(old_target, new_target)
        txt = txt.replace(
            '["Agreement", "residual", "Leg ", "Predicted", "Two-shell", "Naked + WHIM"]',
            '["Agreement", "residual", "Leg ", "Predicted", "Two-shell", "Naked + WHIM", "BKM Operational", "PWC Medium at t=2.500", "Cold-Weld Threshold", "N=5 SU(2)"]'
        )
        rp.write_text(txt, encoding="utf-8")
        print(f"[UPDATED RUNNER] {rp}")

# 2. Add the 8 new scripts to Part V table in PHASE_WAVE_COSMOLOGY_DERIVATIONS.md
anchor_row = "| scripts/stage3_sparc_lock_01335.py | the bare-subset record (0.2745 dex — the trap) | data/solar/results/sparc_lock_01335.json |"
new_rows = """| scripts/stage3_sparc_lock_01335.py | the bare-subset record (0.2745 dex — the trap) | data/solar/results/sparc_lock_01335.json |
| scripts/run_all_rotation_catalogs.py | all 4 external catalogs under the −2 fits naked recipes (PROBES 1,342, ALFALFA 331, GHASP 81, LT 16) | — |
| scripts/merger_neck_yield.py | 3D-to-2D core-grinding containment yield (a_max * sqrt(2/3) = 2.637e11 vs 2.64e11, −0.10%) | — |
| scripts/lepton_t7_unspool_closed.py | T7 unspooling debt closure (20/19 ratio, tau_mu residual −245 -> +7.7 ppm) | — |
| scripts/t6_lorentz_legs_closed.py | T6 Lorentz legs + submarine hull vs bare neutron exposed-thread drag clock | — |
| scripts/t27_cubic_tempo_closed.py | 3D cubic relief tightening T = 3^3 = 27 (s(1+T) = 28/19, Planck LSS tempo +0.0554%) | — |
| scripts/sixteen_fold_grind_check.py | D13 sixteen-fold clock from GW150914 shed Max-P shell thickness (32 * dt_shed / c0 = 4.6806 ms, +0.012%) | — |
| scripts/navier_stokes_bkm_regularity.py | D34 Beale-Kato-Majda operational-middle regularity (0 < Omega_amb <= ||omega|| <= Omega_cav < oo) | — |
| scripts/yang_mills_mass_gap_proof.py | Yang-Mills constructive mass gap & UV finiteness in the operational middle (no 0, no oo) | — |"""

for root in roots:
    for md in root.rglob("PHASE_WAVE_COSMOLOGY_DERIVATIONS.md"):
        txt = md.read_text(encoding="utf-8")
        if "scripts/yang_mills_mass_gap_proof.py |" not in txt and anchor_row in txt:
            txt = txt.replace(anchor_row, new_rows)
            md.write_text(txt, encoding="utf-8")
            print(f"[UPDATED TABLE] {md}")
