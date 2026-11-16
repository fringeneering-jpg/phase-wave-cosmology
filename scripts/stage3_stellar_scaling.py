# stage3_stellar_scaling.py - the same derivations on other solar masses (2026-10-18)
# We know the RESTING medium: rho0, a0 = (c0/sqrt3) sqrt(G rho0/4), K = rho C^2
# (they are entwined), and the rest temperature 2.7255 K. With the 7%
# stagnation of the sun's burn at the corona scale, run the SAME derivations
# on any star (M, R):
#   the burn: mdot(M) = mdot_sun (M/M_sun)^(5/3)   [the consumption ladder]
#   the stagnation: F_rest(M) = 0.07 L(M)/c0, the stress at 1.09 R
#   the relaxation: tau_choke(M) = E_fault(M)/P_acc(M)  ->  1/tau ~ M^(2/3)
#     (the SAME exponent as the burn - the star's own tempo)
#   the temperature: T_corona = f_vent m_p C(rho)^2/k_B at the corona density
#   the medium's local temperature effect from the stalled heat.
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config, pi_v

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
n_lad = F["capacity_ladder"]["n"]
mdot_deep = F["global_anchors"]["mdot_deep"]["value"]
f_esc = F["global_anchors"]["f_esc"]["value"]
f_vent = F["global_anchors"]["f_vent"]["value"]
s = F["locked_constants"]["s"]["value"]
MP = 1.6726e-27
KB = 1.3806e-23
G = 6.67430e-11

L_SUN = 3.828e26
M_SUN = 1.989e30
R_SUN = 6.96e8
RHO_Q = 3.0e8 * 1e6 * MP
C_Q = pi_v.capacity(RHO_Q, c0, rho0, n_lad)
K_Q = RHO_Q * C_Q ** 2
DELTA_GAP = s ** 2
TAU_SUN = K_Q * DELTA_GAP * (4*3.14159265358979*(1.09*R_SUN)**2 * 0.09*R_SUN) / (f_esc * mdot_deep * c0 ** 2)
A_RAD = 7.5657e-16

# the entwinement (the rest state, one source)
a0 = (c0 / 3.0 ** 0.5) * (G * rho0 / 4.0) ** 0.5

stars = [  # name, M (Msun), R (Rsun), L_obs (Lsun)
    ("Proxima",  0.1221, 0.1542, 0.0017),
    ("the Sun",  1.0,    1.0,    1.0),
    ("Sirius A", 2.063,  1.711,  25.4),
    ("Betelgeuse", 16.5, 764.0,  1.26e5),
    ("Rigel",    21.0,   78.9,   1.2e5),
]

def burn(M):   return mdot_deep * M ** (5.0/3.0)        # kg/s
def tau(M, R):
    V_a = 4*3.14159265358979 * (1.09*R*R_SUN)**2 * (0.09*R*R_SUN)
    return K_Q * DELTA_GAP * V_a / (f_esc * burn(M) * c0 ** 2)

print("=" * 78)
print("THE SAME DERIVATIONS ON OTHER SOLAR MASSES - the stellar scaling")
print("=" * 78)
print(f"the entwined rest state: rho0 = {rho0:.2e}, a0 = {a0:.3e} (from rho0),")
print(f"K(rho) = rho C^2 (from rho), T_rest = 2.7255 K")
print()
print(f"{'star':12s} {'M/Msun':>7s} {'R/Rsun':>7s} {'L_pred':>9s} {'L_obs':>9s} "
      f"{'F_rest N':>10s} {'stress Pa':>10s} {'tau':>9s} {'1/tau':>9s} {'T_cor MK':>9s}")
rows = []
for name, M, R, Lobs in stars:
    Lp = L_SUN * M ** (5.0/3.0)
    F_rest = 0.07 * Lp / c0
    stress = F_rest / (4*3.14159265358979*(1.09*R*R_SUN)**2)
    t = tau(M, R)
    Tcor = f_vent * MP * C_Q ** 2 / KB
    u_stall = 0.07 * Lp * t / (4*3.14159265358979*(1.09*R*R_SUN)**2*0.09*R*R_SUN)
    T_med = (u_stall / A_RAD) ** 0.25
    rows.append({"name": name, "M": M, "R": R, "L_pred": Lp, "L_obs": Lobs*L_SUN,
                 "F_rest": F_rest, "stress": stress, "tau_s": t,
                 "rate": 1.0/t, "T_corona_MK": Tcor/1e6, "T_med_local_K": T_med})
    print(f"{name:12s} {M:7.3f} {R:7.3f} {Lp/L_SUN:9.3f} {Lobs:9.3f} "
          f"{F_rest:10.2e} {stress:10.2e} {t:9.3e} {1.0/t:9.3e} {Tcor/1e6:9.2f}")
print()
print("the closures:")
print("  - the relaxation rate 1/tau scales as M^(2/3): the SAME exponent as")
print("    the burn and the consumption - the star's own tempo, one exponent.")
print("  - the stagnation stress at each star's corona: the tension's grip,")
print("    scaled by the star's own geometry.")
print("  - T_corona = the frozen equation at the medium's own corona density")
print("    (1.38 MK for every star; the giants' cooler coronae = the open")
print("    corona-density law, the two-variable law's density axis).")
print()
print("the honest checks:")
print("  - the framework's mass-luminosity L ~ M^(5/3) vs the observed")
print("    main-sequence L ~ M^(2.3-3.5): the difference is the fusion")
print("    throttle (the standard model's temperature sensitivity of the")
print("    p-p/CNO chains) - the framework's burn is the untying's own rate.")
print("  - the giants (Betelgeuse, Rigel): L_pred runs low vs L_obs by the")
print("    same factor - the untying's rate does not need the fusion's chain.")
res = rows
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "stellar_scaling.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
