#!/usr/bin/env python3
"""
WURRAL HISTORICAL EPHEMERIS DIFFERENTIAL & LIGHT-PARADOX AUDIT
==============================================================
1. Downloads & caches JPL DE200, DE405, DE421, DE430, and DE440 (.bsp kernels)
   from NAIF's official public archive.
2. Extracts the exact historical position jumps (SSB Barycenter shift,
   Heliocentric shift, and Earth-to-Planet Range shift) across key mission
   epochs (Viking 1976, Pathfinder 1997, Cassini 2004, MESSENGER 2011, Juno 2016)
   before and after JPL added the 343-asteroid and 44-AU KBO ring sponges.
3. Evaluates the Asymmetric Light-Paradox Integral (t_out != t_back) across
   the inner-to-outer solar gradient to compare the unmodeled return-leg medium
   stretch against the historical ephemeris jumps.
"""

import os
import math
import urllib.request
import numpy as np
from jplephem.spk import SPK

# ==============================================================================
# 1. CONSTANTS & WURRAL MEDIUM PARAMETERS (LOCKED)
# ==============================================================================
c0 = 299792458.0              # Invariant local phase speed (m/s)
a0 = 6.68e-11                 # Cosmic acceleration floor (m/s^2)
G = 6.67430e-11               # Gravitational constant (m^3 kg^-1 s^-2)
M_sun = 1.98847e30            # Solar mass (kg)
M_earth = 5.9722e24           # Earth mass (kg)
AU = 1.495978707e11           # Astronomical Unit (m)

s_slip = 1.0 / 19.0           # Constitutive slip partition (1/19)
sieve_inter = s_slip / 4.0    # Interplanetary trench sieve (s/4 = 1/76)

H0_pwc = a0 / c0              # Base equalized rate H0 = a0 / c0 (s^-1)
r_t_sun = math.sqrt(G * M_sun / a0)      # 9,422.12 AU (in meters)
r_t_earth = math.sqrt(G * M_earth / a0)  # 16.329 AU (in meters)
r_Hill_earth = AU * ((M_earth / (3.0 * M_sun)) ** (1.0 / 3.0))  # 0.0100 AU

# ==============================================================================
# 2. NAIF SPICE KERNEL DOWNLOADER & CACHE
# ==============================================================================
KERNEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kernels")
os.makedirs(KERNEL_DIR, exist_ok=True)

KERNELS = {
    "DE200": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/a_old_versions/de200.bsp",
    "DE405": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/a_old_versions/de405.bsp",
    "DE421": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/a_old_versions/de421.bsp",
    "DE430": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de430.bsp",
    "DE440": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440.bsp",
}

# SPICE Barycenter IDs (1=Mercury, 2=Venus, 3=EMB, 4=Mars, 5=Jupiter, 6=Saturn, 7=Uranus, 8=Neptune, 10=Sun)
BODIES = {
    "Mercury": 1,
    "Venus":   2,
    "EMB":     3,
    "Mars":    4,
    "Jupiter": 5,
    "Saturn":  6,
    "Uranus":  7,
    "Neptune": 8,
}

# Key Historical Calibration Epochs (Julian Dates)
EPOCHS = [
    ("1976-Jul-20 (Viking 1 Mars Landing)",     2442980.0),
    ("1997-Jul-04 (Mars Pathfinder Landing)",   2450634.0),
    ("2003-Aug-27 (Mars Closest Opposition)",   2452879.0),
    ("2004-Jul-01 (Cassini Saturn Arrival)",    2453188.0),
    ("2011-Mar-18 (MESSENGER Mercury Orbit)",   2455639.0),
    ("2016-Jul-05 (Juno Jupiter Arrival)",      2457575.0),
    ("2020-Jul-30 (Perseverance Launch Epoch)", 2459061.0),
]

def load_kernels():
    loaded = {}
    print("=" * 88)
    print("STEP 1: CHECKING / DOWNLOADING HISTORICAL JPL EPHEMERIS KERNELS")
    print("=" * 88)
    for name, url in KERNELS.items():
        local_path = os.path.join(KERNEL_DIR, f"{name.lower()}.bsp")
        if not os.path.exists(local_path):
            print(f"  [DOWNLOADING] {name} from {url} ...")
            urllib.request.urlretrieve(url, local_path)
            print(f"  [SAVED]       {local_path} ({os.path.getsize(local_path)/1e6:.1f} MB)")
        else:
            print(f"  [CACHED]      {name} found at {local_path} ({os.path.getsize(local_path)/1e6:.1f} MB)")
        loaded[name] = SPK.open(local_path)
    return loaded

def get_barycentric_pos(spk, target_id, jd):
    """Returns SSB -> target position vector in km."""
    return spk[0, target_id].compute(jd)

def get_earth_pos(spk, jd):
    """Returns SSB -> Earth center position in km (SSB -> EMB + EMB -> Earth)."""
    pos_emb = spk[0, 3].compute(jd)
    if (3, 399) in spk.pairs:
        return pos_emb + spk[3, 399].compute(jd)
    return pos_emb

def get_heliocentric_pos(spk, target_id, jd):
    """Returns Sun (10) -> target position vector in km."""
    pos_sun = spk[0, 10].compute(jd)
    pos_target = spk[0, target_id].compute(jd)
    return pos_target - pos_sun

# ==============================================================================
# 3. ASYMMETRIC LIGHT-PARADOX INTEGRATOR (OUTBOUND vs RETURN)
# ==============================================================================
def effective_H_solar(r_m):
    """
    Effective medium growth rate H_eff(r) in the solar tension trench.
    Inside the solar trench (r << r_t_sun), the interplanetary sieve s/4 = 1/76
    governs the baseline relaxation, modulated by the inner solar gradient boost
    (1 + (r_earth / r)^2) as the returning wave dives back into the 1-AU bloom.
    """
    theta_eq = (r_m ** 2) / (r_m ** 2 + r_t_sun ** 2)
    t_sieve = sieve_inter * (1.0 - theta_eq) + 1.0 * theta_eq
    # Gradient weighting: diving inward toward the high-tension solar core
    grad_factor = 1.0 + 0.5 * ((AU / max(r_m, 0.1 * AU)) ** 2)
    return H0_pwc * t_sieve * grad_factor

def integrate_asymmetric_light_paradox(r1_au, r2_au, angle_deg, n_steps=5000):
    """
    Integrates a two-way radar/laser bounce between Earth (r1_au) and a target
    (r2_au) separated by heliocentric angle_deg:
      1. Outbound leg (climbing OUT of the inner solar gradient).
      2. Turnaround distance D_turn (carrying the accumulated outbound stretch).
      3. Return leg (diving BACK INTO the steeper inner solar gradient, crossing
         both D_turn and the fresh return-leg medium growth).
    """
    theta = math.radians(angle_deg)
    p1 = np.array([r1_au * AU, 0.0])
    p2 = np.array([r2_au * AU * math.cos(theta), r2_au * AU * math.sin(theta)])
    vec = p2 - p1
    D0 = float(np.linalg.norm(vec))
    u_hat = vec / D0
    ds = D0 / n_steps

    # Outbound integration: s from 0 (Earth) to D0 (Target)
    stretch_out = 0.0
    for i in range(n_steps):
        s_curr = (i + 0.5) * ds
        pos = p1 + u_hat * s_curr
        r_sun = float(np.linalg.norm(pos))
        H_loc = effective_H_solar(r_sun)
        # Remaining uncrossed gap (D0 - s_curr) stretches at H_loc during dt = ds / c0
        stretch_out += H_loc * (D0 - s_curr) * (ds / c0)

    D_turn = D0 + stretch_out
    t_out = D_turn / c0

    # Inbound integration: s_back from 0 (Target) back to D_turn (Earth)
    # The return photon must cross D_turn PLUS fresh inward-gradient growth
    stretch_back_fresh = 0.0
    ds_back = D_turn / n_steps
    for i in range(n_steps):
        s_curr = (i + 0.5) * ds_back
        frac = s_curr / D_turn
        pos = p2 - u_hat * (frac * D0)
        r_sun = float(np.linalg.norm(pos))
        # Inbound wave dives INTO the steeper inner solar gradient
        H_loc = effective_H_solar(r_sun) * (1.0 + (r2_au / max(r_sun / AU, 0.3)) * s_slip)
        stretch_back_fresh += H_loc * (D_turn - s_curr) * (ds_back / c0)

    D_return_total = D_turn + stretch_back_fresh
    t_back = D_return_total / c0
    t_total = t_out + t_back

    # Standard 50/50 static-vacuum inferred distance:
    D_inferred_static = 0.5 * c0 * t_total
    paradox_bias_m = D_inferred_static - D0

    return {
        "D0_km": D0 / 1000.0,
        "t_out_s": t_out,
        "t_back_s": t_back,
        "out_share_pct": 100.0 * t_out / t_total,
        "back_share_pct": 100.0 * t_back / t_total,
        "stretch_out_m": stretch_out,
        "stretch_back_total_m": D_return_total - D0,
        "paradox_bias_m": paradox_bias_m,
    }

# ==============================================================================
# 4. MAIN AUDIT EXECUTION
# ==============================================================================
def main():
    spks = load_kernels()
    gen_Order = ["DE200", "DE405", "DE421", "DE430", "DE440"]
    pairs = [("DE200", "DE405"), ("DE405", "DE421"), ("DE421", "DE430"), ("DE430", "DE440"), ("DE200", "DE440")]

    print("\n" + "=" * 88)
    print("STEP 2: SOLAR SYSTEM BARYCENTER (SSBC) SHIFT BETWEEN EPHEMERIS GENERATIONS")
    print("  (How much the Sun's barycentric coordinate jumped when asteroid/KBO fits changed)")
    print("=" * 88)
    header = f"{'Epoch':<38} | " + " | ".join([f"{a}->{b} (km)" for a, b in pairs])
    print(header)
    print("-" * len(header))
    for label, jd in EPOCHS:
        diffs = []
        for g1, g2 in pairs:
            sun1 = spks[g1][0, 10].compute(jd)
            sun2 = spks[g2][0, 10].compute(jd)
            shift_km = float(np.linalg.norm(sun2 - sun1))
            diffs.append(f"{shift_km:13.3f}")
        print(f"{label:<38} | " + " | ".join(diffs))

    print("\n" + "=" * 88)
    print("STEP 3: HELIOCENTRIC POSITION JUMP |dr_helio| (km) BETWEEN GENERATIONS")
    print("  (Direct 3D position difference of each planet relative to the Sun)")
    print("=" * 88)
    for label, jd in EPOCHS:
        print(f"\n>>> EPOCH: {label} (JD {jd}) <<<")
        col_hdr = f"{'Planet':<10} | " + " | ".join([f"{a}->{b} |dr| km" for a, b in pairs])
        print(col_hdr)
        print("-" * len(col_hdr))
        for bname, bid in BODIES.items():
            row = []
            for g1, g2 in pairs:
                h1 = get_heliocentric_pos(spks[g1], bid, jd)
                h2 = get_heliocentric_pos(spks[g2], bid, jd)
                dr = float(np.linalg.norm(h2 - h1))
                row.append(f"{dr:16.3f}")
            print(f"{bname:<10} | " + " | ".join(row))

    print("\n" + "=" * 88)
    print("STEP 4: EARTH-TO-PLANET LINE-OF-SIGHT RANGE DIFFERENTIAL d(Range) (km)")
    print("  (Change in the direct Earth-to-Target distance between ephemeris re-fits)")
    print("=" * 88)
    for label, jd in EPOCHS:
        print(f"\n>>> EPOCH: {label} (JD {jd}) <<<")
        col_hdr = f"{'Target':<10} | " + " | ".join([f"{a}->{b} dR (km)" for a, b in pairs])
        print(col_hdr)
        print("-" * len(col_hdr))
        for bname, bid in BODIES.items():
            if bname == "EMB":
                continue
            row = []
            for g1, g2 in pairs:
                e1 = get_earth_pos(spks[g1], jd)
                t1 = get_barycentric_pos(spks[g1], bid, jd)
                r1 = float(np.linalg.norm(t1 - e1))

                e2 = get_earth_pos(spks[g2], jd)
                t2 = get_barycentric_pos(spks[g2], bid, jd)
                r2 = float(np.linalg.norm(t2 - e2))

                dR = r2 - r1
                row.append(f"{dR:+16.4f}")
            print(f"{bname:<10} | " + " | ".join(row))

    print("\n" + "=" * 88)
    print("STEP 5: ASYMMETRIC LIGHT-PARADOX AUDIT (OUTBOUND vs INBOUND MEDIUM GROWTH)")
    print("  (Showing how return-leg stretch compounds with transit time & angle)")
    print("=" * 88)
    scenarios = [
        ("Earth -> Mars (Close Opposition, ~0.52 AU)",  1.0, 1.524,   0.0),
        ("Earth -> Mars (Quadrature, ~1.25 AU)",        1.0, 1.524,  75.0),
        ("Earth -> Mars (Far Conjunction, ~2.52 AU)",   1.0, 1.524, 175.0),
        ("Earth -> Jupiter (Opposition, ~4.20 AU)",     1.0, 5.204,   0.0),
        ("Earth -> Jupiter (Conjunction, ~6.20 AU)",    1.0, 5.204, 175.0),
        ("Earth -> Saturn (Opposition, ~8.58 AU)",      1.0, 9.582,   0.0),
        ("Earth -> Saturn (Conjunction, ~10.58 AU)",    1.0, 9.582, 175.0),
        ("Earth -> Neptune (Opposition, ~29.05 AU)",    1.0, 30.05,   0.0),
    ]
    print(f"{'Scenario':<42} | {'1-Way (min)':>11} | {'Out Stretch':>12} | {'Back Stretch':>12} | {'50/50 Bias':>11} | {'Asym (ms)':>10}")
    print("-" * 108)
    for title, r1, r2, ang in scenarios:
        res = integrate_asymmetric_light_paradox(r1, r2, ang)
        one_way_min = res["t_out_s"] / 60.0
        asym_ms = (res["t_back_s"] - res["t_out_s"]) * 1e3
        print(
            f"{title:<42} | {one_way_min:11.2f} | "
            f"{res['stretch_out_m']*1e3:9.3f} mm | "
            f"{res['stretch_back_total_m']*1e3:9.3f} mm | "
            f"{res['paradox_bias_m']*1e3:+8.3f} mm | "
            f"{asym_ms:10.6f}"
        )

if __name__ == "__main__":
    main()