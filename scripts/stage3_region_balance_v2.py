# stage3_region_balance_v2.py - the four-patch refactor (2026-10-18)
# Patch 1: the heat/pressure feedback - the stall's trapped heat drives MORE
#          untying (m_u scales with E_thermal, not just the gap opening).
# Patch 2: the decoupled ledger - E_baseline / E_thermal / E_tied / E_radiated
#          as INDEPENDENT accounts; the residual is the real comparison.
# Patch 3: the governor's latent heat - the m_tie re-pairing RELEASES energy
#          (the tying's exothermic) -> dumped into E_thermal, never deleted.
# Patch 4: the timestep sync + the rolling growth_duration (no sticky flags).
import numpy as np

# --- the framework's locked + stated values ---
c0 = 2.99792458e8
rho0 = 8.74e-27
n_lad = 0.0606
s = 1.0 / 19.0
MP = 1.6726e-27
Q_U = c0**2                      # the phase-change price (J/kg, the ruling)
Q_TIE = c0**2                    # the tying's released price (the same's)

RHO_Q = 3.0e8 * 1e6 * MP         # the quiescent coronal density's proxy
def capacity(rho):
    return c0 * (rho0 / max(rho, 1e-30)) ** n_lad
C_Q = capacity(RHO_Q)

# the region (the AR 12192 box, the stated's)
V_A = 1.21e25                     # m^3
L_CH = 2.30e8                     # m
TAU_AC = L_CH / C_Q
EPS0 = 1.0e-5                     # the SEALED core share
EPS_MAX = 0.30
DELTA_GAP = s**2                  # the 2-D wave-gap fraction
D_V_UNIT = 1.0 / RHO_Q
mdot_deep = 4.26e9                # kg/s the sun's own M = L/c0^2 (the honest anchor)
m_tie0 = 3.8e8                    # kg/s the throttle's capacity (the stated's)
P_STALL = 1.0e-4                  # Pa the stall's pressure (the stated proxy)

# the heat feedback's gain: the trapped heat's FRACTION of the baseline's
# drives the untying (the normalized's - no raw-Joule blowup)
ALPHA_H = 1.0 / 1.0e28          # the 1/E_start: the heat's fraction's gain

def run_region(m_u0, tau_choke, t_end=86400.0, dt=10.0, verbose=True):
    # the four independent accounts
    E_baseline = 1.0e28           # the field's energy at the start
    E_thermal = 0.0               # the trapped heat (the buoyant layer's)
    E_tied = 0.0                  # the energy locked in the knots
    E_radiated = 0.0              # the energy vented through
    E_start = E_baseline

    D_V = 0.0
    eps = EPS0
    hist = {"t": [], "zeta": [], "eps": [], "m_u": [], "E_thermal": [], "verdict": ""}
    t_fault = None
    t_runaway = None
    growth_duration = 0.0
    dD_prev = None

    n = int(t_end / dt)
    for k in range(n):
        # PATCH 4: all the rates at the tick's start, one m_u for the whole step
        m_u_heat_mult = 1.0 + ALPHA_H * E_thermal
        m_u = (m_u0 / max(1.0 - eps, 1e-6)) * m_u_heat_mult
        over = max((capacity(RHO_Q)**2 * RHO_Q) * (D_V / V_A) - P_STALL, 0.0) / max(P_STALL, 1e-30)
        m_tie = min(m_tie0 * over, m_tie0 / DELTA_GAP)

        V_dem = D_V_UNIT * m_u
        V_cap = V_A * eps / tau_choke
        dD = V_dem - V_cap
        D_V = max(D_V + dD * dt, 0.0)
        zeta = D_V / V_A

        # PATCH 1: the stall's heat accumulates when the demand exceeds the cap
        if dD > 0:
            E_thermal += (m_u * Q_U * dt) * min(zeta, 1.0)      # the trapped share's
        # PATCH 3: the governor's tying RELEASES its heat into the thermal pool
        E_thermal += m_tie * Q_TIE * dt
        E_tied += m_tie * Q_TIE * dt
        # the vented's: the fraction the choke lets through
        E_radiated += min(V_cap, V_dem) * RHO_Q * Q_U * dt
        # the field's baseline shrinks by the untied's (the retained's)
        E_baseline -= m_u * Q_U * dt * (1.0 - eps)

        if t_fault is None and eps <= EPS0 and zeta >= DELTA_GAP:
            t_fault = k * dt
        if zeta < DELTA_GAP:
            eps = EPS0
        elif zeta < 2 * DELTA_GAP:
            eps = EPS0 + (EPS_MAX - EPS0) * (zeta - DELTA_GAP) / DELTA_GAP
        else:
            eps = EPS_MAX

        ddD = (dD - dD_prev) / dt if dD_prev is not None else 0.0
        dD_prev = dD
        # PATCH 4: the rolling growth_duration (resets on the deceleration)
        growth_duration = growth_duration + dt if (dD > 0 and ddD > 0) else 0.0
        if t_runaway is None and growth_duration >= 300.0:
            t_runaway = k * dt
        if zeta > 1.0:
            break
        if k % (max(n // 12, 1)) == 0:
            hist["t"].append(k * dt); hist["zeta"].append(zeta)
            hist["eps"].append(eps); hist["m_u"].append(m_u)
            hist["E_thermal"].append(E_thermal)

    # PATCH 2: the independent ledger's residual
    R_E = E_start - (E_baseline + E_thermal + E_tied + E_radiated)

    if t_fault is None:
        verdict = "accommodates (no fault)"
    elif zeta > 1.0 or t_runaway is not None:
        verdict = "ERUPTION (the runaway wins)"
    else:
        verdict = "blocked-settles (confined: the dam re-held)"
    rec = {"m_u0": m_u0, "tau_choke": tau_choke, "t_fault": t_fault,
           "t_runaway": t_runaway, "zeta_final": float(zeta),
           "E_thermal": E_thermal, "E_tied": E_tied, "E_radiated": E_radiated,
           "R_E": float(R_E), "verdict": verdict}
    if verbose:
        print(f"  m_u0={m_u0:.2e}, tau={tau_choke:7.1f}s: "
              f"fault@{None if t_fault is None else f'{t_fault/3600:.2f}h'} "
              f"runaway@{None if t_runaway is None else f'{t_runaway/3600:.2f}h'} "
              f"zeta={zeta:.3f} E_th={E_thermal:.2e} R_E={R_E:+.2e} -> {verdict}")
    return rec

print("=" * 78)
print("STAGE B v2 - THE FOUR-PATCH REFACTOR (the heat's feedback engine)")
print("=" * 78)
print(f"the region: V_a={V_A:.2e}, delta_gap=s^2={DELTA_GAP:.5f}, eps0={EPS0}, "
      f"eps_max={EPS_MAX}, alpha_h={ALPHA_H:.0e}")
print(f"the throttle: m_tie0={m_tie0:.2e} kg/s, P_STALL={P_STALL:.1e} Pa (the stated)")
print()
print("the three regimes at the 9-hour choke (tau = 32400 s):")
for D in (0.1, 0.5, 400.0):
    run_region(D * mdot_deep * (1 - EPS0), 32400.0)
print()
print("the same at the acoustic choke (tau = 5 s):")
for D in (0.1, 0.5, 400.0):
    run_region(D * mdot_deep * (1 - EPS0), TAU_AC)
print()
print("the honest ledger note: the residual R_E is the REAL comparison now -")
print("the four accounts are independent, the tying's heat is routed, and the")
print("heat feedback drives the runaway through the thermal channel, not just")
print("the geometry's.")
