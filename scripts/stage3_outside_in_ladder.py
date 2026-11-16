# stage3_outside_in_ladder.py - the outside-in nested impedance ladder (2026-10-18)
# Anchored at the CMB/deep-void baseline and marched inward through the
# nested shells (void -> halo -> bulge -> cluster -> corona):
#   dp_k = Z_k J_{V,k}   with  J_{V,k} = SUM Q_i / A_k
#   f_choke,i = (Z_choke J_{V,i} + dp_env) / (Pi_i - p0)
# Level 0: the universal box (p0, rho0, T0 = 2.725 K, H0). Level 1: the
# galactic/cluster crowding -> dp_env. Level 2: the star's own choke.
# The Sun calibrates the drive head (f_choke = 7%); every other star's
# choke follows from its own geometry - the giants' coronae cannot grip.
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config, pi_v

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
rho_max = F["locked_constants"]["rho_max"]["value"]
n_lad = F["capacity_ladder"]["n"]
mdot_deep = F["global_anchors"]["mdot_deep"]["value"]
R_p = F["locked_constants"]["R_p"]["value"]
MP = 1.6726e-27

RHO_COR = 5.02e-13
C_COR = pi_v.capacity(RHO_COR, c0, rho0, n_lad)
Z_CHOKE = RHO_COR * C_COR          # the choke's boundary impedance
D_VU = 1.0 / RHO_COR
P0 = rho0 * c0 ** 2 / 3.0
H0 = rho0 * c0 / (rho_max * R_p) * 3.086e19   # km/s/Mpc
M_SUN = 1.989e30
R_SUN = 6.96e8

# the Sun calibrates the drive head: f_choke = 7%
J_V_SUN = mdot_deep * D_VU / (4 * 3.14159265358979 * (1.09 * R_SUN) ** 2)
HEAD = Z_CHOKE * J_V_SUN / 0.07          # Pi_i - p0 = 0.378 Pa (the frozen head)

stars = [  # name, M (Msun), R (Rsun)
    ("Proxima", 0.1221, 0.1542),
    ("the Sun", 1.0, 1.0),
    ("Sirius A", 2.063, 1.711),
    ("Rigel", 21.0, 78.9),
    ("Betelgeuse", 16.5, 764.0),
]

print("=" * 78)
print("THE OUTSIDE-IN NESTED IMPEDANCE LADDER - the choke per star")
print("=" * 78)
print(f"LEVEL 0 (the universal box): p0 = {P0:.2e} Pa, rho0 = {rho0:.2e},")
print(f"  T0 = 2.725 K, H0 = {H0:.3f} km/s/Mpc - the immutable anchor")
print(f"the choke's impedance: Z_choke = rho_cor C_cor = {Z_CHOKE:.2e} Pa s/m")
print(f"the Sun calibrates the head: f_choke = 7% -> Pi - p0 = {HEAD:.3f} Pa")
print()
print(f"{'star':12s} {'M/Msun':>7s} {'R/Rsun':>7s} {'J_V (m/s)':>10s} "
      f"{'Z*J_V (Pa)':>11s} {'f_choke':>9s}")
rows = []
for name, M, R in stars:
    mdot = mdot_deep * M ** (5.0 / 3.0)
    J_V = mdot * D_VU / (4 * 3.14159265358979 * (1.09 * R * R_SUN) ** 2)
    zj = Z_CHOKE * J_V
    f = zj / HEAD
    rows.append({"name": name, "M": M, "R": R, "J_V": J_V, "ZJ": zj,
                 "f_choke": f})
    print(f"{name:12s} {M:7.3f} {R:7.3f} {J_V:10.3f} {zj:11.3e} {f*100:8.2f}%")
print()
print("the giants' grip collapse: Betelgeuse's vast corona dilutes J_V to")
print("0.22 m/s -> f_choke ~ 0.0013% - the boundary cannot grip (matches the")
print("stellar scaling's stress collapse). The dwarfs grip harder than the Sun.")
print()
print("LEVEL 1 (the environmental crowding - the outside-in squeeze):")
gal = [  # (shell, total Q (m^3/s), boundary radius (m))
    ("the galaxy (1e10 Lsun)", 4.259e9 * 1e10 * D_VU, 5.0e20),
    ("a globular cluster (1e5 stars, 10 pc)", 1e5 * mdot_deep * D_VU, 3.09e17),
    ("a close binary (at 1 AU)", mdot_deep * D_VU, 1.496e11),
]
Z0 = rho0 * c0
for name, Q, R in gal:
    J = Q / (4 * 3.14159265358979 * R ** 2)
    dp = Z0 * J
    print(f"  {name:32s}: J_V = {J:.2e} m/s -> dp_env = {dp:.2e} Pa "
          f"({dp/HEAD*100:.1e}% of the star's head)")
print("  the honest read: the galactic crowding is ~1e-27 Pa - NOTHING at the")
print("  star's choke (the 1/r^2 dilution spreads it). The 'war zone' is real")
print("  only in the extreme cores (the SMBH-adjacent stars). Planets orbit")
print("  through untouched - the sieve.")
print()
print("the matched transition (the trench exponent):")
n = n_lad
gamma = (3.0 / 20.0) * (1.0 - 2.0 * n)     # p ~ rho C^2 ~ rho^(1-2n)
print(f"  p(r) = p0 + dp_choke (R_c/r)^gamma,  gamma = (3/20)(1-2n) = "
      f"{gamma:.4f}")
print(f"  far outside the power term dies; at R_c it matches the choke - the")
print(f"  trench profile bridges the boundary layer to the baseline.")
res = {"rows": rows, "Z_choke": Z_CHOKE, "head_Pa": HEAD,
       "H0_kms_Mpc": H0, "gamma": gamma}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "outside_in_ladder.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
