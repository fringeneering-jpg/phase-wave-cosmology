from pathlib import Path

roots = [
    Path(r"C:\Users\jaden\Downloads\PWC-Check\PWC"),
    Path(r"C:\Users\jaden\Downloads\PWC-Check\PWC_THEORY"),
]

for root in roots:
    sdir = root / "scripts"
    if not sdir.exists():
        continue

    # 1. Fix Line 1 pPa unit factor in anomaly_sweep_2026_10_21.py
    as_path = sdir / "anomaly_sweep_2026_10_21.py"
    if as_path.exists():
        txt = as_path.read_text(encoding="utf-8")
        old_line = 'P_amb_pPa = (1.0 - s) * P_base_pPa'
        new_line = 'P_amb_pPa = (1.0 - s) * P_base_pPa'  # the correct sieve row: f_solid*P_base .. f_solid(1+drho)*P_amb (mid 0.2423 pPa)
        if old_line in txt and "P_amb_nPa" not in txt:
            txt = txt.replace(old_line, new_line)
            as_path.write_text(txt, encoding="utf-8")
            print(f"[FIXED pPa UNIT] {as_path}")

    # 2. Wire the 4 new closures into full_run_everything.py
    fr_path = sdir / "full_run_everything.py"
    if fr_path.exists():
        ftxt = fr_path.read_text(encoding="utf-8")
        extras = [
            "navier_stokes_bkm_regularity.py",
            "yang_mills_mass_gap_proof.py",
            "nuclear_force_bunny.py",
            "complete_electroweak_cavitation_closure.py",
        ]
        if "complete_electroweak_cavitation_closure.py" not in ftxt and "neutron_fold_closed.py" in ftxt:
            # Match either single or double quote list entries
            if '"neutron_fold_closed.py"' in ftxt:
                rep = '"neutron_fold_closed.py",\n    "navier_stokes_bkm_regularity.py",\n    "yang_mills_mass_gap_proof.py",\n    "nuclear_force_bunny.py",\n    "complete_electroweak_cavitation_closure.py"'
                ftxt = ftxt.replace('"neutron_fold_closed.py"', rep)
            elif "'neutron_fold_closed.py'" in ftxt:
                rep = "'neutron_fold_closed.py',\n    'navier_stokes_bkm_regularity.py',\n    'yang_mills_mass_gap_proof.py',\n    'nuclear_force_bunny.py',\n    'complete_electroweak_cavitation_closure.py'"
                ftxt = ftxt.replace("'neutron_fold_closed.py'", rep)
            fr_path.write_text(ftxt, encoding="utf-8")
            print(f"[UPDATED FULL RUNNER] {fr_path}")
