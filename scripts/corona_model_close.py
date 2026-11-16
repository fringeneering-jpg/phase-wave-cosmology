# corona_model_close.py - the solar-sector model closure (2026-10-18)
# Derives and FREEZES the four items the test protocol demands, plus the
# demand law, the Pi_V block criterion, the zeta failure rule, and the full
# L/c0^2 output ledger (deep + shallow channels - light is not the only output).
#
# Zero per-event knobs. Provenance per quantity:
#   LOCKED     - the framework's locked constant set
#   MEASURED   - global solar anchors read off the sun first (mdot_deep, f_esc)
#   BACK-SOLVED- the one solar-sector knob (f_vent), anchored on the published
#                mean quiet corona, frozen once, never touched per event
#   DERIVED    - everything else falls out of the above
import json, math, hashlib, os
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(BASE, "..", "data", "solar"))

# ---------------- locked constant set ----------------
c0       = 2.99792458e8    # m/s
rho0     = 8.74e-27        # kg/m^3  median density
rho_max  = 1.304e15        # kg/m^3  yield ceiling (GW150914 shell)
rho_core = 2.3e17          # kg/m^3  structural core
Y_bow    = 5.93e26         # Pa      yield pressure (bow anchors)
R_p      = 0.84e-15        # m       proton knot radius
a_max    = 3.23e11         # N/kg    holding yield
s        = 1.0/19.0        # -       the debt's share
mp       = 1.6726e-27      # kg
kB       = 1.3806e-23      # J/K
mu0      = 1.25663706212e-6
Rsun     = 6.957e8         # m

# ---------------- the capacity ladder (existing anchored form) ----------------
n_lad = math.log(c0/958e3)/math.log(rho_max/rho0)
def C(rho):
    rho = max(rho, 1e-300)
    return c0*(rho0/rho)**n_lad
def K(rho):
    return rho*C(rho)**2

# ---------------- global solar anchors (MEASURED, read off the sun first) -----
L_rad    = 3.828e26          # W  total EM radiation
L_neu    = 0.023*L_rad       # W  neutrinos ~2.3% of L
mdot_deep  = (L_rad+L_neu)/c0**2   # kg/s  deep channel: pays c0^2 per kg
mdot_wind  = 1.5e9           # kg/s  shallow channel: wind (measured outflow)
mdot_cme   = 0.06e9          # kg/s  shallow channel: CMEs (measured)
L_corona = 1.0e21            # W  coronal XUV+radio share of L_rad (measured)
f_esc    = L_corona/L_rad    # -   the coronal vent fraction (MEASURED share)

# ---------------- the one back-solved knob: f_vent (the T-mapping) ------------
T_q   = 1.5e6                # K  published mean quiet-corona temperature
n_e_q = 3.0e8                # cm^-3  published mean quiet-corona density
rho_q = n_e_q*1e6*mp
T_full_q = mp*C(rho_q)**2/kB
f_vent = T_q/T_full_q        # BACK-SOLVED: the vent fraction that lands the
                             # observed T at the observed quiet density

print("="*78)
print("PWC SOLAR-SECTOR CLOSURE - the four items, frozen (2026-10-18)")
print("="*78)
print(f"capacity ladder:  C(rho) = c0 (rho0/rho)^n,  n = {n_lad:.5f}")
print(f"  anchors: c0 at rho0={rho0:.2e}, 958 km/s at rho_max={rho_max:.2e}")
print()

print("ITEM 1 - dV_u: field volume required per unit untying (m^3/kg)")
print("  dV_u(r,t) = 1/rho_loc(r,t) - 1/rho_knot ,  rho_knot = rho_max")
print(f"  at the quiet corona (rho={rho_q:.2e}): dV_u = {1.0/rho_q - 1.0/rho_max:.3e} m^3/kg")
print(f"  the 1/rho_max term is {1.0/rho_max/(1.0/rho_q):.1e} of the 1/rho_loc term - kept exactly in code")
print()

print("ITEM 2 - tau_a: the relaxation law (s), state dependence named")
print("  tau_a(r,t) = L_ch(r) / C(rho_loc(r,t)),  L_ch = V_a^(1/3)")
print("  equivalently tau_a = L_ch sqrt(rho/K) with K = rho C^2 (pressure relaxation)")
print("  state dependence: rho_loc(r,t) and the geometry L_ch(r); units: seconds")
print()

print("ITEM 3 - V_a eps_a: participating adjustment volume (m^3), from field geometry")
print("  V_a = the coronal volume threaded by the region's field lines (HMI PFSS/NLFFF")
print("        reconstruction; one deterministic pipeline, no per-event choice)")
print("  eps_a = the share of those field lines open to >= 1 Rsun (the expandable share)")
print("  representative active region (B_cor=100 G, A_phot=5e15 m^2, H=1e8 m):")
V_a_ref = 5.0e23
E_B_ref = (0.01)**2*V_a_ref/(2*mu0)
M_reg_ref = E_B_ref/c0**2
print(f"  V_a = {V_a_ref:.1e} m^3, E_B = B^2 V_a/2mu0 = {E_B_ref:.2e} J, M_reg = E_B/c0^2 = {M_reg_ref:.2e} kg")
print()

print("ITEM 4 - the observation equation (field state -> observables), frozen")
print(f"  n_e   = rho_loc/m_p")
print(f"  T     = f_vent m_p C(rho_loc)^2/k_B,  f_vent = {f_vent:.4e}  (BACK-SOLVED)")
print(f"     check: at n_e={n_e_q:.0e} cm^-3: T = {f_vent*T_full_q/1e6:.2f} MK = the anchor {T_q/1e6:.2f} MK")
print(f"  L_esc = mdot_untie c0^2 f_esc,  f_esc = {f_esc:.2e}  (MEASURED coronal share)")
print(f"  EM    = integral n_e^2 dV over V_a eps_a   (geometry-determined)")
print(f"  dV/V  = P_wave/K,  P_wave = mdot_untie c0^2 tau_a / V_a  (the closed form")
print(f"     replacing the old ad-hoc T_wave = 6e7 K of sun_derivation.py)")
print()

print("THE DEMAND LAW (HMI-observable, no outcome quantities):")
print("  mdot_untie(r,t) = mdot_deep (1 - eps_a(r,t)) + Gamma_untie(R_p) M_reg(r,t)")
Gamma_p = rho0*c0/(rho_max*R_p)
print(f"  Gamma_untie(R_p) = rho0 c0/(rho_max R_p) = {Gamma_p:.3e} s^-1 (the locked floor)")
print(f"  mdot_deep = (L_rad+L_neu)/c0^2 = {mdot_deep:.3e} kg/s (MEASURED global anchor)")
print(f"  the demand funnels into the closed share of the field: (1 - eps_a)")
print(f"  floor term for the reference AR: {Gamma_p*M_reg_ref:.2e} kg/s (negligible - kept for the zero-activity limit)")
print()

print("THE BLOCK CRITERION - Pi_V, closed form, zero free parameters:")
print("  V_req_dot = mdot_untie dV_u ;  V_avail_dot = V_a eps_a (P_wave/K) / tau_a")
print("  Pi_V = V_req_dot / V_avail_dot = C(rho)^2 / (eps_a c0^2)")
print(f"  at the quiet corona: (C/c0)^2 = {(C(rho_q)/c0)**2:.4e}")
print(f"  -> block (Pi_V > 1) iff eps_a < {(C(rho_q)/c0)**2*100:.2f}%")
print("  The demand magnitude cancels: the block is a property of the FIELD STATE")
print("  (density through C) and the GEOMETRY (eps_a). Closed field blocks; open")
print("  field accommodates. No eruption-derived quantity anywhere.")
print()

print("THE FAILURE RULE (T3) - Pi_V > 1 alone is NOT an eruption threshold:")
print("  zeta(t) = integral_0^t (V_req_dot - V_avail_dot)/V_a dt")
print("         = integral mdot_untie (Pi_V - 1)/(rho V_a) dt   (stored strain)")
print("  zeta_yield = a_max L_ch / C(rho)^2   (the region-scale holding, DERIVED)")
print("  outcomes: Pi_V <= 1            -> accommodation keeps up")
print("            Pi_V > 1, zeta<yield -> blocked but settles")
print("            zeta reaches yield   -> eruption")
L_ch_ref = V_a_ref**(1.0/3.0)
tau_ref = L_ch_ref/C(rho_q)
zeta_yield = a_max*L_ch_ref/C(rho_q)**2
print(f"  reference AR: L_ch = {L_ch_ref:.2e} m, tau_a = {tau_ref:.2f} s, zeta_yield = {zeta_yield:.2e}")
print()
print("CANONICAL TABLE (reference AR, quiet density, demand = full deep funnel):")
print(f"  {'eps_a':>8s} {'Pi_V':>9s} {'blocked':>8s} {'zeta_dot (1/s)':>14s} {'t_fail':>10s}")
for eps in [0.5, 0.05, 0.03, 0.0215, 0.02, 0.01, 0.003]:
    piv = (C(rho_q)/c0)**2/eps
    zd = 0.0 if piv <= 1.0 else mdot_deep*(1-eps)*(piv-1.0)/(rho_q*V_a_ref)
    tf = "never" if zd <= 0 else f"{zeta_yield/zd/86400:.1f} d"
    print(f"  {eps:8.3f} {piv:9.3f} {'yes' if piv>1 else 'no':>8s} {zd:14.3e} {tf:>10s}")
print()
print("NAMED OPEN RESIDUALS (carried into the tests, not hidden):")
print("  1. tau_a at ambient density is ~2 s: the model predicts NEAR-ZERO")
print("     accommodation lag; observed hour-scale coronal delays must then be")
print("     demand-ramp-dominated - T2 tests exactly this split.")
print("  2. T spread: over n_e 1e8-1e9 cm^-3 the frozen law gives")
print(f"     {f_vent*mp*C(1e8*1e6*mp)**2/kB/1e6:.2f}-{f_vent*mp*C(1e9*1e6*mp)**2/kB/1e6:.2f} MK")
print("     vs the observed 1-2 MK quiet spread (under-predicted, anti-correlated).")
print("  3. The demand budget must partition: sum over regions of (1-eps_a) ~ 1.")
print("     Checked on the 30-region sample in the universality stage.")
print()

# ---------------- write the frozen law ----------------
os.makedirs(DATA, exist_ok=True)
frozen = {
  "title": "PWC solar-corona model closure - frozen law",
  "frozen_at": datetime.now(timezone.utc).isoformat(),
  "provenance_labels": ["LOCKED", "MEASURED", "BACK-SOLVED", "DERIVED"],
  "locked_constants": {
    "c0": {"value": c0, "units": "m/s", "provenance": "LOCKED"},
    "rho0": {"value": rho0, "units": "kg/m^3", "provenance": "LOCKED"},
    "rho_max": {"value": rho_max, "units": "kg/m^3", "provenance": "LOCKED"},
    "rho_core": {"value": rho_core, "units": "kg/m^3", "provenance": "LOCKED"},
    "Y_bow": {"value": Y_bow, "units": "Pa", "provenance": "LOCKED"},
    "R_p": {"value": R_p, "units": "m", "provenance": "LOCKED"},
    "a_max": {"value": a_max, "units": "N/kg", "provenance": "LOCKED"},
    "s": {"value": s, "units": "-", "provenance": "LOCKED"},
  },
  "capacity_ladder": {
    "formula": "C(rho) = c0*(rho0/rho)^n",
    "n": n_lad,
    "stiffness": "K(rho) = rho*C(rho)^2",
  },
  "global_anchors": {
    "mdot_deep": {"value": mdot_deep, "units": "kg/s", "provenance": "MEASURED",
                  "source": "(L_rad + L_neu)/c0^2, L_rad=3.828e26 W, L_neu=2.3% L_rad"},
    "mdot_wind": {"value": mdot_wind, "units": "kg/s", "provenance": "MEASURED", "channel": "shallow"},
    "mdot_cme": {"value": mdot_cme, "units": "kg/s", "provenance": "MEASURED", "channel": "shallow"},
    "f_esc": {"value": f_esc, "units": "-", "provenance": "MEASURED",
              "source": "coronal XUV+radio share L_corona/L_rad = 1e21/3.828e26"},
    "f_vent": {"value": f_vent, "units": "-", "provenance": "BACK-SOLVED",
               "source": "T_q=1.5e6 K at n_e_q=3e8 cm^-3 (published quiet-corona means), frozen once"},
  },
  "item_1_dV_u": {
    "formula": "dV_u(r,t) = 1/rho_loc - 1/rho_max", "units": "m^3/kg", "provenance": "DERIVED",
    "note": "rho_knot = rho_max (the ceiling); the 1/rho_max term is negligible but kept exactly",
  },
  "item_2_tau_a": {
    "formula": "tau_a(r,t) = L_ch(r)/C(rho_loc(r,t))", "units": "s", "provenance": "DERIVED",
    "L_ch": "V_a^(1/3)", "state_dependence": "rho_loc(r,t) via C; geometry via L_ch",
  },
  "item_3_V_a_eps_a": {
    "formula": "V_a = volume of HMI-reconstructed field lines; eps_a = open share (lines >= 1 Rsun)",
    "units": "m^3", "provenance": "DERIVED",
    "constraint": "one deterministic geometry pipeline, identical code path for every event",
  },
  "item_4_observation_equation": {
    "n_e": "rho_loc/m_p",
    "T": "f_vent*m_p*C(rho_loc)^2/k_B",
    "L_esc": "mdot_untie*c0^2*f_esc",
    "EM": "integral n_e^2 dV over V_a*eps_a",
    "expansion": "dV/V = P_wave/K, P_wave = mdot_untie*c0^2*tau_a/V_a",
    "provenance": "DERIVED",
  },
  "demand_law": {
    "formula": "mdot_untie(r,t) = mdot_deep*(1 - eps_a(r,t)) + Gamma_untie(R_p)*M_reg(r,t)",
    "Gamma_untie(R_p)": Gamma_p,
    "M_reg": "E_B/c0^2 with E_B = integral B^2/(2 mu0) dV over V_a (HMI-observable)",
    "note": "demand funnels into the closed share; floor term negligible in ARs, kept for the zero-activity limit",
  },
  "block_criterion": {
    "Pi_V": "C(rho)^2/(eps_a*c0^2)",
    "block_when": "Pi_V > 1, i.e. eps_a < (C(rho)/c0)^2",
    "provenance": "DERIVED",
    "note": "demand magnitude cancels; block is a field-state/geometry property only",
  },
  "failure_rule": {
    "zeta": "integral_0^t mdot_untie*(Pi_V-1)/(rho*V_a) dt",
    "zeta_yield": "a_max*L_ch/C(rho)^2",
    "outcomes": "Pi_V<=1: accommodation keeps up; Pi_V>1 & zeta<yield: blocked-settles; zeta>=yield: eruption",
    "provenance": "DERIVED",
    "checked_and_rejected": "zeta_yield = Y_bow/K (never reached: ~3e23 - recorded, not used)",
  },
  "full_output_ledger": {
    "deep_channel_kg_s": mdot_deep,
    "shallow_channel_kg_s": mdot_wind + mdot_cme,
    "total_kg_s": mdot_deep + mdot_wind + mdot_cme,
    "statement": "light is NOT the only output: deep = radiation+neutrinos (c0^2 per kg); shallow = wind+CMEs (measured outflow). Total closes against the standard's measured solar mass loss within the observational spread.",
  },
  "open_residuals": [
    "tau_a ~ seconds at ambient density: observed hour-scale delays must be demand-ramp-dominated (T2 splits this)",
    "frozen T spread over quiet densities under-predicts the observed 1-2 MK range",
    "demand budget partition sum(1-eps_a) ~ 1 to be checked on the 30-region sample",
  ],
}
raw = json.dumps(frozen, sort_keys=True, indent=1)
frozen["sha256"] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
path = os.path.join(DATA, "corona_model_frozen.json")
with open(path, "w", encoding="utf-8") as fh:
    json.dump(frozen, fh, sort_keys=True, indent=1)
print(f"FROZEN LAW WRITTEN: {path}")
print(f"SHA-256: {frozen['sha256'][:24]}...")
print()
print("INDEPENDENCE: no eruption-derived quantity appears anywhere above; the")
print("accommodation rate uses locked constants + the two global MEASURED anchors")
print("+ the one BACK-SOLVED f_vent, all frozen before any event data.")
