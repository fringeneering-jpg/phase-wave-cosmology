# stage3_uv_density_wear.py - the UV's best absorber is the dense gas; the
# distance wear is nothing at solar-system scale (2026-10-18)
# Jaden: "sheds specifically as heat - the best effects should be HIGH
# DENSITY GAS for UV absorption, and the normal distance effects should
# scale by only the energy rate of normal lightspeed travel (redshift),
# basically nothing on a solar-system scale, mere lightminutes/lighthours."
# 1. the UV shed = the friction mu = (v/C)^2 times the gas column: the
#    denser the gas, the faster the luminous energy sheds as heat.
# 2. the wear (the redshift) = H_wall * (d/c0): ~1e-14 over the whole
#    solar system - the distance effects are the pure 1/d^2 dilution.
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config, pi_v

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
rho_max = F["locked_constants"]["rho_max"]["value"]
n_lad = F["capacity_ladder"]["n"]
R_p = F["locked_constants"]["R_p"]["value"]

H_wall = rho0 * c0 / (rho_max * R_p)     # s^-1  the wear's rate

# (name, surface density kg/m^3, gas pressure Pa (measured), scale height m, fate)
atmospheres = [
    ("Venus",   65.0,  9.2e6,  1.5e4, "the 92-bar CO2 sheds ALL the UV high up"),
    ("Jupiter", 0.2,   1.0e5,  3.0e4, "the deep field sheds the UV in the upper layers"),
    ("Earth",   1.2,   1.013e5, 8.5e3, "1 bar + ozone sheds the UV"),
    ("Mars",    0.02,  6.4e2,  1.1e4, "6 mbar: the UV REACHES THE SURFACE (thin can't shed it)"),
]

print("=" * 78)
print("THE PRESSURE FRICTION LADDER - the photon at c0 vs the dense pressured field")
print("=" * 78)
print(f"{'atmosphere':12s} {'rho':>9s} {'P_gas (Pa)':>11s} {'C km/s':>8s} "
      f"{'mu':>8s} {'shed proxy':>11s}")
rows = []
for name, rho, Pg, H, fate in atmospheres:
    C = pi_v.capacity(rho, c0, rho0, n_lad)
    K_med = rho * C ** 2                  # the MEDIUM's stiffness at that state
    mu = (c0 / C) ** 2
    col = rho * H
    shed = mu * col
    rows.append({"name": name, "rho": rho, "P_gas_Pa": Pg, "K_medium_Pa": K_med,
                 "C_km_s": C/1e3, "mu": mu, "column": col, "shed": shed})
    print(f"{name:12s} {rho:9.3f} {Pg:11.3e} {C/1e3:8.0f} {mu:8.0f} "
          f"{shed:11.3e}")
    print(f"{'':12s}  {fate}")
print()
print("the reading: the photon arrives at baseline c0 (max-P). The atmosphere's")
print("density (the matter) raises the MEDIUM's local state - its stiffness")
print("K = rho C^2 is immense (Venus 2.4e15 Pa vs the gas's own 9.2e6 Pa - the")
print("field's stiffness vs the matter's pressure) - and the capacity ladder")
print("lowers C with that density. mu = (c0/C)^2 then scales the deceleration,")
print("and the shed's energy IS the heat output. Descending each scale height")
print("compounds it: rho grows, C falls, mu grows, the shed grows - the rapid")
print("brake. Venus: the highest density+pressure state, the fastest shed;")
print("Mars: the lowest, the UV survives to the surface.")
print()
print("the wear (the redshift over distance), at H_wall = 2.39e-18 s^-1:")
AU_s = 1.496e11 / c0                     # light-seconds per AU
wear_per_AU = H_wall * AU_s
print(f"  light-seconds per AU = {AU_s:.0f} s; wear per AU = {wear_per_AU:.2e}")
for d_AU, name in [(1.0, "Earth"), (5.2, "Jupiter"), (30.1, "Neptune"),
                   (50.0, "the Kuiper belt")]:
    print(f"  {name:18s} at {d_AU:5.1f} AU: wear = {H_wall * d_AU * AU_s:.2e} "
          f"({d_AU * AU_s / 3600:.1f} light-hours traveled)")
print()
print("the reading: over the whole solar system the luminous wear is ~1e-14 -")
print("nothing. The distance effects ARE the pure 1/d^2 dilution; the UV's")
print("shedding is the DENSITY's work (the friction), not the distance's.")
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "uv_density_wear.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump({"atmospheres": rows, "wear_per_AU": wear_per_AU,
               "H_wall": H_wall}, fh, indent=1)
print()
print("result written:", out)
