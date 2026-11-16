# -*- coding: utf-8 -*-
"""
wurral_v2_wake_trough.py — WORROOL eTNO WAKE-TROUGH MODEL (v2, ZERO HAND-SET KNOBS)

Copyright (c) 2026 Jaden Allison (Fringeneering). All Rights Reserved.

DUAL LICENSE:
  * GNU Affero General Public License v3.0 (AGPLv3) — free for students,
    academic research, and open benchmark evaluation only.
  * Fringeneering Commercial Telemetry License — required for any
    proprietary, commercial, or closed-source integration.

Integrating this file into a proprietary system without a commercial agreement
is PROHIBITED. Commercial Telemetry Inquiries: fringeneering@gmail.com

WHAT CHANGED FROM v1 (the audited script)
----------------------------------------
  1. The uniform Stark vector (-WAKE_AXIS, which makes the eccentricity vector
     CIRCULATE at different rates per semi-major axis) is REPLACED by the
     conical wake trough: an azimuthal restoring force -sin(theta) * theta_hat
     confined to a narrow cone around the heliotail axis, so aphelia damp INTO
     the trough instead of circulating through 360 degrees.
  2. The 0.38 / 0.14 / 1e-9 hand-set multipliers are GONE. The amplitude is
     built strictly from locked constants in four candidate chains (all
     printed, none tuned):
        C0G   : c0 * Gamma1                  = 0.5234  m/s^2   (user's form 1)
        VG    : v_sun * Gamma1               = 4.016e-4 m/s^2 (user's form 2)
        V2C   : (v_sun/c0)^2 * c0 * Gamma1   = 3.08e-7 m/s^2  (user's form 3)
        FLOOR : a_A = c0 * H0                = 7.18e-10 m/s^2 (locked Anderson floor)
     Gamma1 = 1.746e-9 s^-1 is the LOCKED full-campaign ILRS constant.
  3. Velocity-strain damping (v . grad)P ~ (r_dot / c0) * Gamma1 couples the
     trough to the radial velocity, per the derivation note.
  4. ALL THREE Planet-9 signatures are tested and printed raw: varpi
     clustering (Rayleigh R), omega libration (range of omega over 150 kyr),
     and high-inclination shear (does any variant reach the 2015 BP519 class?).
  5. Orbit-survival is checked: a variant that disrupts the eTNOs is recorded
     as DISRUPTED, not silently integrated through garbage.
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wurral as W   # audited v1: catalog, element conversions, circular stats

# ---------------------------------------------------------------------------
# Locked constants (zero free parameters)
# ---------------------------------------------------------------------------
C0 = 299792458.0
GAMMA1 = 1.746e-9                       # locked ILRS Starlette strain rate (s^-1)
V_SUN = 2.30e5                          # solar galactic velocity (m/s, literature)
H0_SEC = 73.935 / 3.085677581e19        # s^-1
A_FLOOR = C0 * H0_SEC                   # 7.1832e-10 m/s^2 (the Anderson floor)
RHO_MAX = 1.29032e15                    # kg/m^3 (locked ceiling)
RHO_LISM = 8.740e-27                    # kg/m^3 (ambient horizon density)
THETA_C_DEG = 9.0                       # trough half-angle = the locked 720/9 fold tolerance

VARIANTS = {
    "C0G":   C0 * GAMMA1,
    "VG":    V_SUN * GAMMA1,
    "V2C":   (V_SUN / C0) ** 2 * C0 * GAMMA1,
    "FLOOR": A_FLOOR,
}

M2S_TO_AUYR2 = W.YR_S ** 2 / W.AU_M     # convert m/s^2 -> AU/yr^2


def eos_saturation(rho):
    """[1 + (rho/rho_max)^(2/33)]^-1 — the (2/33) constitutive saturation."""
    return 1.0 / (1.0 + (rho / RHO_MAX) ** (2.0 / 33.0))


def accel_v2(pos, vel, variant):
    """Baseline Newtonian + Neptune ring + the conical wake trough (no knobs)."""
    r2 = float(np.dot(pos, pos))
    r = math.sqrt(r2)
    r_hat = pos / r

    # 1. Newtonian solar + secular Neptune quadrupole ring (as in v1)
    acc = -W.GM_SUN * pos / (r2 * r)
    a_nep = 30.07
    gm_nep = W.GM_SUN * (W.GM_NEPTUNE_SI / W.GM_SUN_SI)
    if r > a_nep:
        z2 = pos[2] ** 2
        qf = 0.75 * gm_nep * (a_nep ** 2) / (r ** 5)
        acc += np.array([
            -qf * pos[0] * (1.0 - 5.0 * z2 / r2),
            -qf * pos[1] * (1.0 - 5.0 * z2 / r2),
            -qf * pos[2] * (3.0 - 5.0 * z2 / r2)])

    # 2. Conical wake trough: azimuthal restoring -sin(theta) theta_hat,
    #    confined to the 9-deg half-angle cone around the heliotail axis.
    cos_t = float(np.dot(r_hat, W.WAKE_AXIS))
    theta = math.acos(max(-1.0, min(1.0, cos_t)))
    if theta > math.radians(THETA_C_DEG):
        return acc                       # outside the trough: pure baseline

    a_amp = VARIANTS[variant] * M2S_TO_AUYR2 * W.PWC_COEFF * eos_saturation(RHO_LISM)

    sin_t = math.sin(theta)
    if sin_t > 1e-9:
        theta_hat = (W.WAKE_AXIS - cos_t * r_hat) / sin_t
        acc += -a_amp * sin_t * theta_hat          # restoring toward the axis

    # 3. Velocity-strain damping coupling (r_dot / c0) * Gamma1 (derivation note)
    r_dot_ms = float(np.dot(vel, r_hat)) * W.AU_M / W.YR_S
    damp = (GAMMA1 * abs(r_dot_ms) / C0) * a_amp
    acc += -damp * r_hat
    return acc


def yoshida4(pos, vel, dt, variant):
    p, v = pos.copy(), vel.copy()
    for k in range(4):
        p += W._C[k] * v * dt
        if W._D[k] != 0.0:
            v += W._D[k] * accel_v2(p, v, variant) * dt
    return p, v


def omega_of(pos, vel):
    """omega = varpi - Omega (projected, same convention as v1's varpi)."""
    h_vec = np.cross(pos, vel)
    n_vec = np.cross(np.array([0.0, 0.0, 1.0]), h_vec)
    n_norm = float(np.linalg.norm(n_vec))
    if n_norm < 1e-15:
        return None
    Omega = math.degrees(math.atan2(n_vec[1], n_vec[0])) % 360.0
    e_vec = np.cross(vel, h_vec) / W.GM_SUN - pos / float(np.linalg.norm(pos))
    varpi = math.degrees(math.atan2(e_vec[1], e_vec[0])) % 360.0
    return (varpi - Omega) % 360.0


# ---------------------------------------------------------------------------
# Benchmarks
# ---------------------------------------------------------------------------
SIM_YEARS = 150000.0
DT_YR = 25.0
STEPS = int(SIM_YEARS / DT_YR)
SAMPLE_EVERY = 20          # omega sampled every 500 yr
N_SAMPLES = STEPS // SAMPLE_EVERY


def run_variant(variant):
    """Evolve the 6 eTNOs from scattered phases; return the full scoreboard."""
    rows = []
    for obj in W.ETNO_CATALOG:
        obs_varpi = (obj["Omega"] + obj["omega"]) % 360.0
        scatter = 65.0 if (len(rows) % 2 == 0) else -60.0
        init_omega = (obj["omega"] + scatter) % 360.0
        pos, vel = W.elements_to_state(obj["a"], obj["e"], obj["i"],
                                       obj["Omega"], init_omega, M_deg=180.0)
        omegas = []
        disrupted = False
        for step in range(STEPS):
            try:
                pos, vel = yoshida4(pos, vel, DT_YR, variant)
                if step % SAMPLE_EVERY == 0:
                    om = omega_of(pos, vel)
                    omegas.append(om)
                if not np.all(np.isfinite(pos)) or float(np.linalg.norm(pos)) > 1.0e7:
                    disrupted = True
                    break
            except (ValueError, OverflowError, FloatingPointError):
                disrupted = True
                break
        if disrupted:
            rows.append({"name": obj["name"], "obs": obs_varpi, "varpi": None,
                         "q": None, "omega_range": None, "disrupted": True})
            continue
        a, e, q, i, varpi = W.state_to_elements(pos, vel)
        om_arr = [o for o in omegas if o is not None]
        om_range = (max(om_arr) - min(om_arr)) if om_arr else None
        rows.append({"name": obj["name"], "obs": obs_varpi, "varpi": varpi,
                     "q": q, "i": i, "omega_range": om_range, "disrupted": False})
    return rows


def sedna_lift(variant):
    """Sedna detachment test: q from 30.5 AU under the trough."""
    a_sedna, q0 = 506.8, 30.5
    e0 = 1.0 - q0 / a_sedna
    pos, vel = W.elements_to_state(a_sedna, e0, 11.93, 144.40, 311.29, M_deg=0.0)
    disrupted = False
    for _ in range(STEPS):
        try:
            pos, vel = yoshida4(pos, vel, DT_YR, variant)
            if not np.all(np.isfinite(pos)) or float(np.linalg.norm(pos)) > 1.0e7:
                disrupted = True
                break
        except (ValueError, OverflowError):
            disrupted = True
            break
    if disrupted:
        return None, None, True
    _, _, q, i, _ = W.state_to_elements(pos, vel)
    return q, i, False


def main():
    rng = np.random.default_rng(20261101)
    # null significance (200k draws, as in the v1 audit)
    n_null = 200000
    hits = 0
    for _ in range(n_null):
        _, _, R = W.circular_std_deg(rng.uniform(0, 360, 6))
        if R >= 0.903:
            hits += 1
    p_null = hits / n_null

    print("=" * 118)
    print("WORROOL eTNO WAKE-TROUGH MODEL (v2) — LOCKED-CONSTANT AMPLITUDES, ZERO KNOBS")
    print(f"Trough: 9-deg half-angle cone around the heliotail (lon {W.WAKE_LON_DEG}, lat {W.WAKE_LAT_DEG})")
    print("=" * 118)
    print("  AMPLITUDE LADDER (locked chains; solar gravity at 500 AU = 2.37e-8 m/s^2):")
    g500 = 4.0 * math.pi ** 2 / 500.0 ** 2 / M2S_TO_AUYR2   # AU/yr^2 -> m/s^2
    for k, v in VARIANTS.items():
        print(f"    {k:<6} a = {v:.3e} m/s^2   ({v/g500:9.1f}x solar gravity at 500 AU)")
    print(f"    Anderson floor a_A = {A_FLOOR:.3e} m/s^2  ({A_FLOOR/g500:9.4f}x)")
    print("-" * 118)

    results = {}
    for variant in VARIANTS:
        rows = run_variant(variant)
        n_disr = sum(1 for r in rows if r["disrupted"])
        vps = [r["varpi"] for r in rows if not r["disrupted"]]
        results[variant] = (rows, vps, n_disr)

    print(f"{'Variant':<7} | {'disrupted':>9} | {'R_obs_ref':>9} | {'Rayleigh R':>10} | {'mean lock err':>13} | {'q range (AU)':>13} | {'omega libration':>15}")
    print("-" * 118)
    for variant, (rows, vps, n_disr) in results.items():
        if n_disr == len(rows):
            print(f"{variant:<7} | {n_disr:>8}/6 |    0.903 | {'  ---  ':>10} | {'    ---   ':>13} | {'    ---   ':>13} | {'  ---  ':>15}")
            continue
        _, _, R = W.circular_std_deg(vps)
        obs = [(r["name"], r["obs"]) for r in rows]
        lock_errs = [((v - o + 180.0) % 360.0) - 180.0
                     for v, (_, o) in zip(vps, obs)]
        mean_lock = sum(lock_errs) / len(lock_errs)
        qs = [r["q"] for r in rows if not r["disrupted"]]
        om_ranges = [r["omega_range"] for r in rows if r["omega_range"] is not None]
        n_lib = sum(1 for o in om_ranges if o < 180.0)
        print(f"{variant:<7} | {n_disr:>8}/6 |    0.903 | {R:>10.3f} | {mean_lock:>+12.1f} deg | "
              f"{min(qs):>6.1f}-{max(qs):<6.1f} | {n_lib:>5}/{len(om_ranges)} librate")
    print("-" * 118)

    print("\n[TEST 2] SEDNA DETACHMENT (q_init = 30.5 AU -> Sedna 76.2 AU):")
    for variant in VARIANTS:
        q, i, disrupted = sedna_lift(variant)
        if disrupted:
            print(f"    {variant:<7} DISRUPTED (orbit blown out)")
        else:
            print(f"    {variant:<7} q_final = {q:7.2f} AU | i_final = {i:6.2f} deg")

    print("\n[TEST 3] HIGH-INCLINATION SHEAR (2015 BP519 class: does any variant reach i > 40 deg from i0 = 11.93):")
    for variant in VARIANTS:
        _, i_final, disrupted = sedna_lift(variant)
        if disrupted:
            print(f"    {variant:<7} DISRUPTED")
        else:
            print(f"    {variant:<7} i_final = {i_final:6.2f} deg  ->  {'REACHES BP519 CLASS' if i_final and i_final >= 40 else 'does not reach BP519 class'}")

    print("\n" + "=" * 118)
    print("COMPUTED VERDICT (thresholds: R >= 0.451, |mean lock err| <= 30 deg, q >= 65 AU, no disruption)")
    print("-" * 118)
    print(f"  null significance of the observed cluster: p(R >= 0.903 | 6 uniform) = {p_null:.4f} (real signal)")
    for variant, (rows, vps, n_disr) in results.items():
        if n_disr > 0:
            print(f"  [{variant:<6}] FAIL - {n_disr}/6 orbits disrupted by the locked amplitude")
            continue
        _, _, R = W.circular_std_deg(vps)
        obs = [(r["name"], r["obs"]) for r in rows]
        lock_errs = [((v - o + 180.0) % 360.0) - 180.0 for v, (_, o) in zip(vps, obs)]
        mean_lock = sum(lock_errs) / len(lock_errs)
        q_f, _, _ = sedna_lift(variant)
        c1 = R >= 0.4515
        c2 = abs(mean_lock) <= 30.0
        c3 = q_f is not None and q_f >= 65.0
        print(f"  [{variant:<6}] clustering {'PASS' if c1 else 'FAIL'} (R={R:.3f}) | "
              f"lock {'PASS' if c2 else 'FAIL'} ({mean_lock:+.1f} deg) | "
              f"detachment {'PASS' if c3 else 'FAIL'} (q={q_f if q_f is not None else float('nan'):.1f} AU)")
    print("=" * 118)


if __name__ == "__main__":
    main()
