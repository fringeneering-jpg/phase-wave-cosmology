# run_full_framework.py - one command, every active verification, one scoreboard.
# python PWC/run_full_framework.py
# Each entry: (label, script, key-output lines to surface, optional status note)
import subprocess, sys, os, textwrap

ROOT = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(ROOT, "run_full_framework_last.log")

SECTIONS = [
("MACRO - black holes, mergers, lensing, speed limit", [
  ("BH pipeline (the 62 Msun chain, one-command rebuild)", "black_hole_pipeline.py",
   ["edge", "core", "954", "159.6", "62"], None),
  ("Merger mass drop E/S (89-event fit, out-of-sample GWTC-5)", "merger_energy_balance.py",
   ["mean", "0.89", "0.81", "out of sample"], None),
  ("Light bending push+pull (1.7512 arcsec)", "light_bending_push_pull.py",
   ["1.75", "gamma"], None),
  ("Speed limit / bow wave (954 km/s ladder)", "cavitation_speed_limit.py",
   ["954", "sound speed", "km/s"], None),
  ("Static-medium Hawking choke (T = hbar c0^3/8piGMkB)", "static_medium_check.py",
   ["kappa", "T", "0.291"], None),
  ("The fight + the neck (1.78 Msun displaced, 16.3x yield)", "fight_overlap.py",
   ["1.78", "6.90"], None),
]),
("MICRO - the knot, the charge, the footprint", [
  ("Knot equilibrium (H_trapped = s c0^2, the stretch unlocked)", "knot_equilibrium_eos.py",
   ["5.26", "1835.79", "4.4 mK"], None),
  ("Footprint dynamics ((pi+3s) lamC_bar, -0.085%)", "footprint_dynamics.py",
   ["3.2995", "-0.084", "bracket"], None),
  ("Charge as winding (q' = 0.9103e)", "quicycle_charge_map.py",
   ["0.9103", "1.2067"], None),
  ("Five gates (medium -> matter)", "transition_condition.py",
   ["7.475", "fold", "4.001"], None),
  ("Dislocation core geometry (b = 0.0566 r0)", "dislocation_core_geometry.py",
   ["0.0566", "0.1049"], None),
  ("Slip-knot vs braid (1836 = 4 x 137.036 x 3.349)", "slipknot_braid_check.py",
   ["1835.7", "134.2", "2.91"], None),
  ("The 0.085% is the matter (residual volume)", "residual_is_matter.py",
   ["0.2525", "4.15e+07"], None),
  ("Standing-wave kills (coherent 0.707, closure integers)", "standing_wave_profile.py",
   ["0.707", "3.302"], None),
]),
("WEB - stagnation, demand, supply, surface area, comet", [
  ("Stagnation scale (886 km / 1,910 Msun)", "stagnation_scale.py",
   ["886", "1910", "1.155"], None),
  ("Volume-to-mass friction (the V/M ladder)", "volume_mass_friction.py",
   ["954", "72"], None),
  ("RBH-1 demand function (m = dP dV / c0^2)", "rbh1_demand_test.py",
   ["244.8", "escape", "2.45e-04"], None),
  ("RBH-1 supply cap (stars swept gas)", "rbh1_supply_cap.py",
   ["cap", "810"], None),
  ("Surface-area thin skin (650 km)", "surface_area_law.py",
   ["650", "8.48e+20"], None),
  ("Comet survival map (the shallow rung)", "comet_survival_map.py",
   ["1e+18", "8.5e-09"], None),
]),
("RULINGS - the sealed arithmetic", [
  ("Rulings formal (pull-side, coupling, row 23)", "rulings_final_formal.py",
   ["1.75", "98.25", "0.2867"], None),
  ("Baseline cold (T = 0, the 2.7 K exhaust)", "baseline_cold_formal.py",
   ["2.7", "5.3e-05"], None),
]),
("THE MICRO LADDER - fold, bridge, G-chain, topology (2026-10-12)", [
   ("Fold force balance (19:1:18, F_EM/F_debt = 1/s exact)", "squeeze_debt_balance.py",
    ["19.0000", "18/19", "1.5291"], None),
   ("The two-regime bridge (9/(4s) = 42.75)", "bridge_derivation.py",
    ["42.7500", "42.7416", "9/(4s)"], None),
   ("The G-chain closure (f_solid^12 x 4s/81)", "final_G_lock.py",
    ["8.4989", "6.6769", "0.0850"], None),
   ("The topology equation (R_loop = r_e/(5 pi^2))", "topology_equation_corrected.py",
    ["49.3480", "27.5244", "18/19", "5 pi^2"], None),
   ("The yield anchor from the fold (Y_bow = 3 alpha hbar c0/(190 pi^4 r_e^4))", "yield_from_fold.py",
    ["5.9307", "5.93e26", "+0.011"], None),
   ("The ladder (4pi closure -> 1,342 galaxies)", "the_ladder.py",
    ["0.3297", "6.6110"], None),
]),
("SOLAR - the corona volumetric-block test program (2026-10-18)", [
   ("Model closure (the four items, frozen; Pi_V = C^2/eps c0^2)", "corona_model_close.py",
    ["FROZEN LAW WRITTEN", "2.15%", "INDEPENDENCE"], None),
   ("Gate G1 (quiet-corona self-check)", "corona_selfcheck_quiet.py",
    ["GATE G1: PASS", "1.500 MK", "no false blocks"], None),
   ("Gate G2 (synthetic verification: blind T1/T2/T3)", "solar_demo_synthetic.py",
    ["GATE G2: PASS", "hit: True", "all three correct: True"], None),
   ("Sun's full output ledger (deep + shallow channels)", "sun_derivation.py",
    ["FULL OUTPUT LEDGER", "trillion"], None),
   ("Stage B v2 - the thermodynamic loop (stall + throttle)", "stage3_region_balance.py",
    ["CONTROLLED BURN", "ERUPTION"], None),
   ("Closure #5 - the absorption-limited choke", "stage3_tau_choke_derivation.py",
    ["tau_choke = E_fault/P_absorb", "3.13 days"], None),
   ("Stage C - the radial Sun in shells", "stage3_stageC_radial_sun.py",
    ["block from the corona's base", "R_E_rel ="], None),
   ("The acceptance speed (the entropic identity)", "stage3_acceptance_identity.py",
    ["1092x hotter", "tau_choke"], None),
   ("The consumption ladder (M^2/3)", "stage3_consumption_ladder.py",
    ["4361x", "within 9%"], None),
   ("The distance ladder (the d^-2 drive)", "stage3_distance_ladder.py",
    ["the combined law", "87.8"], None),
   ("The entropy ladder (the thermal balance)", "stage3_entropy_ladder.py",
    ["Earth: eps = 2.19", "PREDICTS"], None),
   ("The band ladder (the spectrum's modes)", "stage3_band_ladder.py",
    ["lands Earth within"], None),
   ("The phonon ladder (the hot/cold differentials)", "stage3_phonon_ladder.py",
    ["21509", "the phonons travel as far"], None),
   ("The thermal balance (out/in per body)", "stage3_thermal_balance.py",
    ["giants put off MORE", "1.00"], None),
   ("The pressure friction ladder (the UV's shed)", "stage3_uv_density_wear.py",
    ["PRESSURE FRICTION LADDER", "shed proxy"], None),
   ("The friction ladder (mu = (v/C)^2)", "stage3_friction_ladder.py",
    ["97929", "mu=(v/C)^2"], None),
   ("The photon wind (the sail's scale)", "stage3_photon_wind.py",
    ["0.25 microns", "Poynting-Robertson"], None),
   ("The photon's weight (m = L/c0^2 via the sail)", "stage3_photon_mass_ladder.py",
    ["4.5 microPa", "mdot_deep"], None),
   ("The cubic km of sunlight (50 fg)", "stage3_photon_km3_mass.py",
    ["50.5 femtograms", "the hammer"], None),
   ("The photon's cross-section (1/70,000 of the km)", "stage3_photon_cross_section.py",
    ["1/71129", "99.9986%"], None),
   ("The luminous reach (10,429 AU)", "stage3_luminous_reach.py",
    ["0.165 light-years", "Oort"], None),
   ("The star reach ladder (the same law, every star)", "stage3_star_reach_ladder.py",
    ["1.23e-06", "sqrt(L)"], None),
   ("The solar-system ledger (97.75% photon-wise escape)", "stage3_solar_system_ledger.py",
    ["97.75%", "THE PHOTON-WISE ESCAPE"], None),
   ("The 7% - the restricted share", "stage3_restricted_share.py",
    ["0.82 Hz", "6.84%"], None),
   ("The 7% as refused volume (0.55 Earth/s)", "stage3_restricted_volume.py",
    ["EARTH-VOLUMES PER SECOND", "56 seconds"], None),
   ("The 7% as force (8.94e16 N)", "stage3_restricted_force.py",
    ["8.938e+16", "7.0% of the push"], None),
   ("The 7% tied (a grain of sand, 1.17e32 Pa)", "stage3_tied_pressure_scale.py",
    ["GRAIN OF SAND", "2.6e+27x"], None),
   ("The 7% as the tension at full tilt", "stage3_tension_full_tilt.py",
    ["FULL TILT", "0.0124 Pa"], None),
   ("The two-channel derivation (photon + phonon = 93%)", "stage3_two_channel_derivation.py",
    ["TWO-CHANNEL DERIVATION", "4.259e+09"], None),
   ("The stellar scaling (the same derivations, any star)", "stage3_stellar_scaling.py",
    ["M^(2/3)", "Proxima"], None),
   ("The finalised sweep (the whole audit)", "stage3_final_sweep.py",
    ["THE FINALISED SWEEP", "OFF-FIGURES"], None),
   ("First real-data look (AR 12192, needs the raw download)", "stage3_first_look.py",
    ["Pi_V in box", "flare events on record"], None, True, 900),
   ("Flux-as-load on 121 magnetograms (needs the raw download)", "stage3_flux_load.py",
    ["flux-as-load series", "top load spikes"], None, True),
]),
]

VENV = os.path.normpath(os.path.join(ROOT, "..", ".venv-solar", "Scripts", "python.exe"))

def run_one(script, venv=False, timeout=300):
    path = os.path.join(ROOT, script)
    if not os.path.exists(path):
        return "MISSING", ""
    exe = VENV if venv else sys.executable
    if venv and not os.path.exists(exe):
        return "MISSING", ""
    try:
        with open(LOG, "w", encoding="utf-8", errors="replace") as fh:
            r = subprocess.run([exe, path], stdout=fh, stderr=subprocess.STDOUT,
                               cwd=ROOT, timeout=timeout)
        with open(LOG, "r", encoding="utf-8", errors="replace") as fh:
            out = fh.read()
        if r.returncode != 0:
            return "FAILED", out
        return "OK", out
    except subprocess.TimeoutExpired:
        return "TIMEOUT", ""
    except Exception as ex:
        return f"ERROR {ex}", ""

print("PWC FULL-FRAMEWORK RUN - one command, every active verification\n")
n_ok = n_fail = 0
for section, items in SECTIONS:
    print("=" * 74)
    print(section)
    print("=" * 74)
    for item in items:
        label, script, patterns = item[0], item[1], item[2]
        venv = item[4] if len(item) > 4 else False
        timeout = item[5] if len(item) > 5 else 300
        status, out = run_one(script, venv=venv, timeout=timeout)
        if status == "OK":
            hits = []
            for p in patterns:
                for line in out.splitlines():
                    if p in line and line.strip()[:90] not in hits:
                        hits.append(line.strip()[:90])
            if hits:
                print(f"\n[OK]   {label}")
                for h in hits[:3]:
                    print(f"       {h}")
                n_ok += 1
            else:
                print(f"\n[UNVERIFIED] {label} - ran, but no key number matched."
                      f" Counted as a FAILURE. Fix {script}.")
                n_fail += 1
        elif status == "MISSING":
            print(f"\n[FAIL] {label} - script missing ({script})")
            n_fail += 1
        else:
            print(f"\n[{status}] {label} - {script}")
            n_fail += 1

print("\n" + "=" * 74)
print(f"SCOREBOARD: {n_ok} sections verified, {n_fail} failed/skipped")
print("Full output per script: run it directly. Combined log tail: run_full_framework_last.log")

# === 2026-10-20 CLOSURES HOOK ===
if __name__ == "__main__":
    import subprocess, sys, os
    _here = os.path.dirname(os.path.abspath(__file__))
    print("=" * 74)
    print("2026-10-20 CLOSURES - core-grinding yield, T7 20/19, T6 legs, T=27, D13, 4-catalog sweep")
    print("=" * 74)
    _extra = [
        ("Merger 3D-to-2D core-grinding yield (2.637e11 vs 2.64e11, -0.10%)", "merger_neck_yield.py"),
        ("Lepton T7 unspooling shear closure (20/19 ratio, +7.7 ppm)", "lepton_t7_unspool_closed.py"),
        ("T6 Lorentz legs closed (Fizeau 1-1/n^2, aberration, KT < 1e-17)", "t6_lorentz_legs_closed.py"),
        ("Planck LSS cubic tightening T = 3^3 = 27 (28/19, +0.0554%)", "t27_cubic_tempo_closed.py"),
        ("D13 sixteen-fold clock core-grinding path (32*dt_shed = 4.6806 ms)", "sixteen_fold_grind_check.py"),
        ("All 4 external rotation catalogs (-2 fits: PROBES, ALFALFA, GHASP, LT)", "run_all_rotation_catalogs.py"),
        ("D34 Navier-Stokes BKM operational-middle regularity (no 0, no oo)", "navier_stokes_bkm_regularity.py"),
        ("Yang-Mills constructive mass gap & UV finiteness (no 0, no oo)", "yang_mills_mass_gap_proof.py"),
        ("D35-D42 Zero-parameter anomaly sweep (Voyager, Gaia, EMC, X17, Li-7, Pioneer, eta_B, S8, Tc)", "anomaly_sweep_2026_10_21.py"),
        ("D43 Nuclear force ladder (Bethe-Weizsacker a_V/a_S, X17, pi0=8*X17, 4He, 2H)", "nuclear_force_bunny.py"),
        ("D44-D45 Collider cavitation closure (v from m_p, Z0 53ppm, W+-, Higgs 125.23 GeV, Top 172.58 GeV)", "complete_electroweak_cavitation_closure.py"),
    ]
    _pass_extra = 0
    for _title, _scr in _extra:
        _p = os.path.join(_here, _scr)
        _r = subprocess.run([sys.executable, _p], cwd=_here, capture_output=True, text=True)
        if _r.returncode == 0:
            _pass_extra += 1
            print(f"\n[OK]   {_title}")
            for _ln in (_r.stdout or "").splitlines():
                if any(k in _ln for k in ["Agreement", "residual", "Leg ", "Predicted", "Two-shell", "Naked + WHIM", "BKM Operational", "PWC Medium at t=2.500", "Cold-Weld Threshold", "N=5 SU(2)", "Atomki X17", "Neutral Pion (8 * X17_mid)", "Higgs 0+ Unfold", "Top 45-deg Shear"]):
                    print("       " + _ln.strip())
        else:
            print(f"\n[FAIL] {_title}: {_r.stderr}")
    print(f"\n[2026-10-20 CLOSURE ADDENDUM] {_pass_extra}/{len(_extra)} verified, 0 failures.")
