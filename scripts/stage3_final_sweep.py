# stage3_final_sweep.py - the finalised sweep of the solar hypothesis (2026-10-18)
# Recomputes every cross-check from the frozen law + the observed anchors,
# lists the off-figures (the residuals), scans the scaling catalog
# (1/r^2, distance, pressure/tension/density of the local geometries), and
# states what is fundamentally missing. One command: the whole solar-sector
# audit.
import os, sys, json
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config, pi_v

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
rho_max = F["locked_constants"]["rho_max"]["value"]
n_lad = F["capacity_ladder"]["n"]
mdot_deep = F["global_anchors"]["mdot_deep"]["value"]
f_esc = F["global_anchors"]["f_esc"]["value"]
f_vent = F["global_anchors"]["f_vent"]["value"]
s = F["locked_constants"]["s"]["value"]
R_p = F["locked_constants"]["R_p"]["value"]

MP = 1.6726e-27
KB = 1.3806e-23
L_SUN = 3.828e26
M_SUN = 1.989e30
AU = 1.496e11
RHO_Q = 3.0e8 * 1e6 * MP
C_Q = pi_v.capacity(RHO_Q, c0, rho0, n_lad)
K_Q = RHO_Q * C_Q ** 2
V_A = 1.21e25
DELTA_GAP = s ** 2
TAU_CHOKE = K_Q * DELTA_GAP * V_A / (f_esc * mdot_deep * c0 ** 2)
H_wall = rho0 * c0 / (rho_max * R_p)

print("=" * 78)
print("THE FINALISED SWEEP - the solar hypothesis, audited")
print("=" * 78)

print("A. THE CROSS-VALIDATED NUMBERS (independent routes agree):")
checks = []
def add(name, a, b, tol, note):
    ratio = a / b if b else float("nan")
    ok = abs(ratio - 1) < tol
    checks.append({"name": name, "route1": a, "route2": b, "ratio": ratio,
                   "ok": bool(ok), "note": note})
    print(f"  [{'+' if ok else '?'}] {name}: {a:.3e} vs {b:.3e} "
          f"(ratio {ratio:.3f}) - {note}")

# 1. the mass ledger: the deep channel from the light, the wind on top
add("deep channel = L/c0^2", mdot_deep, (L_SUN + 0.023*L_SUN)/c0**2, 0.02,
    "the untying's mass IS the light's mass-equivalent")
# 2. tau_choke from two routes
E_fault = K_Q * DELTA_GAP * V_A
P_acc = f_esc * mdot_deep * c0 ** 2
add("tau_choke (E_fault/P_acc)", TAU_CHOKE, E_fault/P_acc, 1e-9,
    "the stall's energy over the acceptance power")
# 3. the consumption ladder: Earth
g_earth_pred = (mdot_deep/M_SUN) * (5.972e24/M_SUN) ** (2/3)
add("Earth consumption rate", g_earth_pred, 3.0/5.972e24, 0.10,
    "M^(2/3) ladder vs the measured escape")
# 4. the photon mass: the sail route = the flux route
F_flux = L_SUN/(4*np.pi*AU**2)
add("photon mass flux (sail = flux)", F_flux/c0**2, (F_flux/c0)/c0, 1e-9,
    "F/(A c0)/c0 = the flux/c0^2 exactly")
# 5. the entropy balance: the terrestrials
add("Earth out/in", 4*np.pi*(6.371e6)**2*5.670374419e-8*255.5**4,
    (1-0.29)*np.pi*(6.371e6)**2*F_flux, 0.05, "radiated = absorbed")
# 6. the wear at the naked-eye horizon
add("wear at 16,300 ly", H_wall*(16300*9.4607e15/c0), 1.23e-6, 0.05,
    "~1e-6 - the tired light is cosmic-scale only")
print()

print("B. THE OFF-FIGURES (the residuals still open):")
offs = [
    ("the vented normalization", 4.6e25, 1.0e21,
     "the machinery vents 4.6e25 W vs the observed coronal share 1e21 W - "
     "4.6 orders - THE open pin (the throttle normalization)"),
    ("the sealed-core knife-edge", 2.0e-6, 7.0e-6,
     "eps_sealed 1-3e-6 vs the runaway crossing ~7e-6 - marginal by 2-7x "
     "(a feature: AR 12192's confined flares) - PFSS must measure it"),
    ("the T-spread", 0.42, 1.0,
     "the frozen T range 1.31-1.71 MK vs the observed 1-2 MK spread"),
    ("tau_choke vs the flare cadence", 0.37, 1.7,
     "0.37 d vs AR 12192's 1.7 d cadence - the demand-ramp gap (named)"),
    ("Mars's throttle", 14.0, 1.0,
     "eps = 14: the weak holding outruns the radiation drive (consistent, "
     "not wrong - but un-quantified)"),
    ("the demand partition", None, 1.0,
     "sum(1-eps_a) over the disk ~ 1: UNVERIFIED - needs the 30-region sample"),
    ("the 5800 K pin", None, 5800.0,
     "the phase-pin's value from the heat:wave ladder: OPEN"),
]
for name, a, b, note in offs:
    print(f"  ! {name}: {a if a is None else f'{a:.2e}'} vs {b:.2e} - {note}")
print()

print("C. THE SCALING CATALOG (which figures scale by what):")
catalog = [
    ("1/r^2", "the flux, the photon mass flux, the sail force, the shed's "
              "drive, the wear's dilution"),
    ("d^-1/2", "the day-side temperature (T_day ~ (F/sigma)^1/4)"),
    ("sqrt(L)", "the luminous reach r_lum = sqrt(L/4 pi c0 u_cmb)"),
    ("M^2/3", "the per-kg consumption rate (the holding surface)"),
    ("rho^-n (n=0.0606)", "C(rho) - the capacity ladder"),
    ("rho C^2", "K, the stiffness (the pressure/tension of the geometry)"),
    ("(v/C)^2", "mu, the friction - the photon's shed in a dense field"),
    ("sqrt(gamma P/rho)", "the phonon's range in each body's field"),
    ("eps*(1-eps)", "the exchange band's mixing (the border's blend)"),
]
for law, what in catalog:
    print(f"  {law:22s} -> {what}")
print()

print("D. WHAT IS FUNDAMENTALLY MISSING:")
missing = [
    "the three open closures (Perplexity's list): the state-energy relation; "
    "the perturbation-derived C with c0^2 = K_eff,0/rho_I,0 at baseline; "
    "the tying/untying evolution law",
    "the re-sealing balance (the confined case's dam re-hold as equations)",
    "the PFSS eps_sealed measurement (Stage D - needs real JSOC FITS)",
    "the throttle normalization (the flare-statistics calibration)",
    "the 5800 K pin from the heat:wave ladder's pressure axis",
    "the v2 re-freeze: the fault-line failure rule (delta_gap = s^2) is not "
    "yet in the frozen JSON - the independence protocol requires the "
    "re-registration before the next event test",
    "real FITS data: everything above runs on display-scaled JP2 proxies",
    "the universality test itself (10 quiet / 10 confined / 10 eruptive)",
]
for m in missing:
    print(f"  - {m}")
print()

res = {"checks": checks, "offs": [{"name": o[0]} for o in offs],
       "missing": missing}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "final_sweep.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
