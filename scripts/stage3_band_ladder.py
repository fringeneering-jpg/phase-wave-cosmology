# stage3_band_ladder.py - the received energy isn't one thing (2026-10-18)
# Jaden: a phonon in the field doesn't travel the same distance as a photon;
# a UV wave at lightspeed has a different effect on matter than infrared.
# The framework's own statement: the capacity ladder C(rho) <= c0 - the
# photon is the unpaired wave at max-P (c0), the phonon-like modes ride the
# local capacity. The solar energy is a spectrum of the medium's modes, and
# each band's per-joule effect on matter differs:
#   the high-frequency end (UV) carries the deep untie (the bond-breaking),
#   the low-frequency end (IR) dilates/warms (the phonon-like shallow heat).
# The band-resolved entropy balance:
#   mdot = SUM_bands eta_b (1-A) F_b pi R^2 / c0^2
# with eta_b = the band's per-joule untie efficiency ~ its photon energy.
# ZERO free parameters: the band split and photon energies are measured.
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]

L_SUN = 3.828e26
AU = 1.496e11

# the solar spectrum's band split (5778 K blackbody, standard) and the
# representative photon energy per band (the wave's own energy)
BANDS = [
    ("UV   (<400 nm)",  0.087, 4.96),   # 250 nm -> 4.96 eV: the deep untie
    ("Vis  (400-700)",  0.389, 2.25),   # 550 nm -> 2.25 eV
    ("IR   (>700 nm)",  0.524, 0.30),   # ~4 um -> 0.3 eV: the phonon-like heat
]

bodies = [
    ("Mercury", 3.301e23, 2.440e6, 0.387, 0.06, None),
    ("Venus",   4.867e24, 6.052e6, 0.723, 0.77, None),
    ("Earth",   5.972e24, 6.371e6, 1.000, 0.29, 3.0),
    ("Mars",    6.417e23, 3.390e6, 1.524, 0.25, 2.5),
    ("Jupiter", 1.898e27, 6.991e7, 5.203, 0.50, None),
    ("Saturn",  5.683e26, 5.823e7, 9.583, 0.47, None),
    ("Uranus",  8.681e25, 2.536e7, 19.22, 0.51, None),
    ("Neptune", 1.024e26, 2.462e7, 30.11, 0.41, None),
]

print("=" * 78)
print("THE BAND LADDER - the received energy is a spectrum of the medium's modes")
print("=" * 78)
print("the mechanism: the photon rides c0 (max-P, the untie's agent); the")
print("phonon-like modes ride C(rho) (the local capacity) - different travel,")
print("different effect. Per band: eta = the photon energy (the per-joule")
print("untie efficiency): UV breaks the knots, IR dilates without untying.")
print()
print("the band-weighted balance: mdot = SUM eta_b (1-A) F_b pi R^2 / c0^2")
print()
tot_w = sum(f * e for _, f, e in BANDS)
print(f"the band weights (fraction x eV):")
for name, fr, ev in BANDS:
    print(f"  {name}: {fr:.3f} of the energy, {ev:.2f} eV per wave -> "
          f"weight {fr*ev:.3f}")
print(f"  total weighting = {tot_w:.3f} (vs 1.0 if all bands untied equally)")
print()
print(f"{'body':9s} {'mdot_band':>10s} {'mdot_flat':>10s} {'observed':>10s}")
rows = []
for name, M, R, d, A, mdot_obs in bodies:
    flux = L_SUN / (4 * 3.14159265358979 * (d * AU) ** 2)
    drive = sum(fr * ev * (1 - A) * flux for _, fr, ev in BANDS)
    mdot_band = 3.14159265358979 * R ** 2 * drive / c0 ** 2
    mdot_flat = (1 - A) * 3.14159265358979 * R ** 2 * flux / c0 ** 2
    rows.append({"name": name, "mdot_band": mdot_band, "mdot_flat": mdot_flat,
                 "obs": mdot_obs})
    print(f"{name:9s} {mdot_band:10.3e} {mdot_flat:10.3e} "
          f"{'-' if mdot_obs is None else f'{mdot_obs:.2e}':>10s}")
print()
print("the checks:")
print(f"  Earth: band-weighted {3.14159265358979*(6.371e6)**2*sum(fr*ev*(1-0.29)*1361.1 for _,fr,ev in BANDS)/c0**2:.2f} kg/s "
      f"vs observed 3.0 kg/s (the flat balance gave 1.37)")
print(f"  -> the band weighting (zero free parameters) lands Earth within "
      f"~{abs(3.14159265358979*(6.371e6)**2*sum(fr*ev*(1-0.29)*1361.1 for _,fr,ev in BANDS)/c0**2/3.0 - 1)*100:.0f}%")
print(f"  Mars: band-weighted "
      f"{3.14159265358979*(3.390e6)**2*sum(fr*ev*(1-0.25)*586.0 for _,fr,ev in BANDS)/c0**2:.2f} kg/s "
      f"vs observed ~2.5 (the weak holding still outruns, as before)")
print()
print("the reading: the UV end of the received spectrum is the untie's agent")
print("(high per-wave energy, the bond-breaker); the IR end is the phonon-like")
print("heat (dilates, travels at the local capacity, no untie). The received")
print("energy is not one thing - it is the medium's own modes, and the")
print("entropy balance must sum them by their effect, not by their joules.")
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "band_ladder.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump({"bands": [list(b) for b in BANDS], "total_weight": tot_w,
               "bodies": rows}, fh, indent=1)
print()
print("result written:", out)
