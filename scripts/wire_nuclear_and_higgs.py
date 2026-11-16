from pathlib import Path

roots = [
    Path(r"C:\Users\jaden\Downloads\PWC-Check\PWC"),
    Path(r"C:\Users\jaden\Downloads\PWC-Check\PWC_THEORY"),
]

# 1. Update run_full_framework.py to run all 11 new verification scripts in the post-scoreboard hook
for root in roots:
    rp = root / "scripts" / "run_full_framework.py"
    if not rp.exists():
        continue
    txt = rp.read_text(encoding="utf-8")
    anchor = '("Yang-Mills constructive mass gap & UV finiteness (no 0, no oo)", "yang_mills_mass_gap_proof.py"),'
    addition = (
        anchor
        + '\n        ("D35-D42 Zero-parameter anomaly sweep (Voyager, Gaia, EMC, X17, Li-7, Pioneer, eta_B, S8, Tc)", "anomaly_sweep_2026_10_21.py"),'
        + '\n        ("D43 Nuclear force ladder (Bethe-Weizsacker a_V/a_S, X17, pi0=8*X17, 4He, 2H)", "nuclear_force_bunny.py"),'
        + '\n        ("D44-D45 Collider cavitation closure (v from m_p, Z0 53ppm, W+-, Higgs 125.23 GeV, Top 172.58 GeV)", "complete_electroweak_cavitation_closure.py"),'
    )
    if "complete_electroweak_cavitation_closure.py" not in txt and anchor in txt:
        txt = txt.replace(anchor, addition)
        txt = txt.replace(
            '"Cold-Weld Threshold", "N=5 SU(2)"]',
            '"Cold-Weld Threshold", "N=5 SU(2)", "Atomki X17", "Neutral Pion (8 * X17_mid)", "Higgs 0+ Unfold", "Top 45-deg Shear"]'
        )
        rp.write_text(txt, encoding="utf-8")
        print(f"[UPDATED RUNNER] {rp}")

# 2. Update Part V table in PHASE_WAVE_COSMOLOGY_DERIVATIONS.md
table_anchor = "| scripts/yang_mills_mass_gap_proof.py | Yang-Mills constructive mass gap & UV finiteness in the operational middle (no 0, no oo) | — |"
table_addition = """| scripts/yang_mills_mass_gap_proof.py | Yang-Mills constructive mass gap & UV finiteness in the operational middle (no 0, no oo) | — |
| scripts/anomaly_sweep_2026_10_21.py | 11-anomaly zero-parameter sweep (Voyager floor, Gaia wide binaries, EMC, X17, Li-7, Pioneer, eta_B = f_solid^3, S8 = 0.7904, Cuprate Tc = 135 K) | — |
| scripts/nuclear_force_bunny.py | nuclear force ladder: Bethe-Weizsacker a_V = 15.59 MeV & a_S = 17.33 MeV, X17 = 16.84 MeV, neutral pion pi^0 = 8*X17 = 134.997 MeV (+0.015%), 4He & 2H | — |
| scripts/boson_to_higgs_ladder.py | boson-to-Higgs cavitation ladder (X17 -> pi^0 -> W/Z -> 125.23 GeV proton emptiness unfold) | — |
| scripts/complete_electroweak_cavitation_closure.py | full electroweak & collider closure from m_p, alpha, s=1/19, T=27: v = 246.07 GeV, M_Z = 91.1884 GeV (53 ppm solid-debt step), M_W = 80.3595 GeV (-0.07s), M_H = 125.232 GeV (-0.11s), m_t = 172.576 GeV (+0.02s) | — |"""

for root in roots:
    for md in root.rglob("PHASE_WAVE_COSMOLOGY_DERIVATIONS.md"):
        txt = md.read_text(encoding="utf-8")
        if "scripts/complete_electroweak_cavitation_closure.py |" not in txt and table_anchor in txt:
            txt = txt.replace(table_anchor, table_addition)
            md.write_text(txt, encoding="utf-8")
            print(f"[UPDATED TABLE] {md}")
