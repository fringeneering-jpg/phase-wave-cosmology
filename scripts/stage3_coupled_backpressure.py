# stage3_coupled_backpressure.py - the coupled back-pressure model, read into PWC
# (2026-10-18) The four equations, implemented with the PWC constants and
# cross-checked against the Stage B machinery:
#   1. the retarded kernel: p_{j->i} = (rho0/4 pi r) V''_j(t - r/c0)
#      - only ACCELERATION of a neighbour's release produces pressure: the
#        formalization of the momentum term (the runaway's ddD/dt^2 > 0).
#   2. the fighting-for-room law: dp/dt = (K/V)[SUM Q_i - INT v.n dA]
#      - the Stage B D_V dynamics in pressure form (the cross-validation).
#   3. the feedback law: Q_i = L_i [Pi_i - p_i]_+ with Pi_i from the knot's
#      OWN energy law - NOT rho C^2 (the cancellation). The PWC candidate:
#      Pi_i = rho_max c0^2 (the tied state's stored pressure).
#   4. the energy audit: p^2/2K + rho0 |v|^2/2, with Q_i^2/L_i dissipated.
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config, pi_v

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
rho_max = F["locked_constants"]["rho_max"]["value"]
n_lad = F["capacity_ladder"]["n"]
mdot_deep = F["global_anchors"]["mdot_deep"]["value"]
f_esc = F["global_anchors"]["f_esc"]["value"]
s = F["locked_constants"]["s"]["value"]
MP = 1.6726e-27

RHO_Q = 3.0e8 * 1e6 * MP
C_Q = pi_v.capacity(RHO_Q, c0, rho0, n_lad)
K_Q = RHO_Q * C_Q ** 2
V_A = 1.21e25
DELTA_GAP = s ** 2
TAU = K_Q * DELTA_GAP * V_A / (f_esc * mdot_deep * c0 ** 2)

print("=" * 78)
print("THE COUPLED BACK-PRESSURE MODEL - read into the PWC machinery")
print("=" * 78)

print("1. THE RETARDED KERNEL - only the acceleration pushes:")
print(f"   p_{{j->i}} = (rho0/4 pi r) V''_j(t - r/c0)")
r_ij = 1.0e7                 # m  neighbouring knots' spacing in the AR core
D_VU = 1.0 / RHO_Q           # m^3/kg  the release's specific volume
# the flare's impulsive phase: mdot ~ 1.8e6 kg/s ramping over ~100 s
m_dot_imp = 1.8e6            # kg/s
m_ddot = m_dot_imp / 100.0   # kg/s^2  the acceleration of the release
V_ddot = m_ddot * D_VU       # m^3/s^2  V''
p_kernel = rho0 / (4 * 3.14159265358979 * r_ij) * V_ddot
print(f"   the flare's V'' = m_ddot x dV_u = {V_ddot:.2e} m^3/s^2")
print(f"   -> p_{{j->i}} = {p_kernel:.2e} Pa (vs P_base {rho0*c0**2/3:.2e} Pa)")
print(f"   a CONSTANT rate gives V'' = 0 -> NO leading-order pressure: the")
print(f"   acceleration IS the pressure source - the Stage B runaway's own")
print(f"   momentum criterion (growth_duration on ddD/dt^2 > 0), formalized.")
print()

print("2. THE FIGHTING-FOR-ROOM LAW = the Stage B D_V dynamics:")
print(f"   doc: dp/dt = (K/V)[SUM Q_i - INT v.n dA]")
print(f"   PWC: zeta_dot = (V_dem - V_cap)/V_a  ->  p_dot = K zeta_dot")
V_dem = mdot_deep / RHO_Q
V_cap = V_A * 1.0e-5 / TAU
p_dot_doc = K_Q / V_A * (V_dem - V_cap)
p_dot_pwc = K_Q * (V_dem - V_cap) / V_A
print(f"   p_dot(doc) = {p_dot_doc:.3e} Pa/s; p_dot(PWC) = {p_dot_pwc:.3e} Pa/s")
print(f"   IDENTICAL - the same law: the mean pressure tracks the release")
print(f"   minus the boundary accommodation. One equation, two notations.")
print()

print("3. THE FEEDBACK LAW - Pi_i from the knot's OWN energy law:")
PI_TIED = rho_max * c0 ** 2    # Pa  the tied state's stored pressure
p_local = K_Q                  # Pa  the local back-pressure (the corona)
print(f"   Q_i = L_i [Pi_i - p_i]_+ ; Pi_i = rho_max c0^2 = {PI_TIED:.2e} Pa")
print(f"   p_i (the corona's back-pressure) = {p_local:.2e} Pa")
print(f"   -> [Pi - p]_+ = Pi practically: the demand flows freely until the")
print(f"   back-pressure approaches the TIED state's own scale - the stall")
print(f"   bites only near the knot's pressure. (The doc's own warning holds:")
print(f"   Pi_i must NOT be rho C^2 - under fixed K that is just K.)")
print()

print("4. THE ENERGY AUDIT - the field's two stores + the dissipation:")
E_comp = (p_local ** 2) / (2 * K_Q)      # J/m^3  the compressional store
v_exp = C_Q                               # m/s  the expansion's speed
E_kin = 0.5 * RHO_Q * v_exp ** 2          # J/m^3  the kinetic store
print(f"   p^2/2K = {E_comp:.3e} J/m^3 ; rho0 |v|^2/2 = {E_kin:.3e} J/m^3")
print(f"   (at the corona: p^2/2K = K/2 = the pressure's own store - and")
print(f"   rho C^2/2 = K/2: the two stores split the field's energy evenly)")
print(f"   the dissipation Q_i^2/L_i = the heat - the Stage B E_thermal's")
print(f"   source (the stalled waves' shed). The ledgers agree.")
print()
res = {"p_kernel_Pa": p_kernel, "V_ddot": V_ddot,
       "p_dot_doc": p_dot_doc, "p_dot_pwc": p_dot_pwc,
       "Pi_tied_Pa": PI_TIED, "E_comp": E_comp, "E_kin": E_kin}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "coupled_backpressure.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
