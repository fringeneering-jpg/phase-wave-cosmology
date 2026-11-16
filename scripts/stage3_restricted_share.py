# stage3_restricted_share.py - the 7%: the choke-restricted untying force (2026-10-18)
# Jaden derived the photon output and the phonon output from the sun's
# vacuum-model total and found 7% EXACTLY unaccounted:
#   0.07 x L_sun = 2.6796e25 W
# and reads it as the UNTYING KNOTS' FORCE being RESTRICTED by the choke,
# amplified by the high heat. The framework's mapping:
#   - the mass reading: 2.6796e25 W / c0^2 = 2.98e8 kg/s = 6.8% of the deep
#     channel: the choke holds back ~7% of the star's untying.
#   - the fault churn: P_restricted / E_fault = the fault's cycle rate
#     (~0.8 Hz) - the nanoflare cadence's own regime (the watch item).
#   - the amplification: the heat's return (the speed-up law's (1+T)) keeps
#     the restricted force hot - the choke holds it, the heat feeds it.
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config, pi_v

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
n_lad = F["capacity_ladder"]["n"]
mdot_deep = F["global_anchors"]["mdot_deep"]["value"]
f_esc = F["global_anchors"]["f_esc"]["value"]
s = F["locked_constants"]["s"]["value"]
MP = 1.6726e-27

L_SUN = 3.828e26
RHO_Q = 3.0e8 * 1e6 * MP
C_Q = pi_v.capacity(RHO_Q, c0, rho0, n_lad)
K_Q = RHO_Q * C_Q ** 2
V_A = 1.21e25
DELTA_GAP = s ** 2
E_FAULT = K_Q * DELTA_GAP * V_A

P_REST = 0.07 * L_SUN           # Jaden's 7%

print("=" * 78)
print("THE 7% - THE CHOKE-RESTRICTED UNTYING FORCE (Jaden's derivation)")
print("=" * 78)
print(f"the vacuum model's total: L_sun = {L_SUN:.3e} W")
print(f"the unaccounted share: 7% = {P_REST:.4e} W")
print(f"the mass reading: P_rest/c0^2 = {P_REST/c0**2:.3e} kg/s")
print(f"  = {P_REST/c0**2/mdot_deep*100:.2f}% of the deep channel - the choke")
print(f"  holds back ~7% of the star's untying per second.")
print()
print("the fault churn (the restricted force vs the fault's inventory):")
E_fault = E_FAULT
churn = P_REST / E_fault
print(f"  E_fault = {E_fault:.2e} J; churn rate = P_rest/E_fault = {churn:.2f} Hz")
print(f"  -> the fault opens/seals ~{churn:.1f} times per second: the")
print(f"  nanoflare cadence's own regime - THE WATCH ITEM (the observed")
print(f"  nanoflare cadence is seconds-scale; the coronal heating budget is")
print(f"  the dissipation fraction of this churn).")
print()
print("the amplification: the heat's return keeps the restricted force hot -")
print("the choke holds it, the heat feeds it (the speed-up law's tightening).")
print("the true total: the vacuum estimate + 7% = "
      f"{L_SUN + P_REST:.3e} W - the star's full untying, of which the")
print("vacuum model sees only the 93% that escapes.")
res = {"P_restricted_W": P_REST, "mass_rate_kg_s": P_REST / c0 ** 2,
       "share_of_deep": P_REST / c0 ** 2 / mdot_deep,
       "fault_churn_Hz": churn, "E_fault_J": E_fault}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "restricted_share.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
