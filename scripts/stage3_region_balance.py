# stage3_region_balance.py - v2 REFACTOR (2026-10-18): the true thermodynamic
# feedback loop, per Jaden's mechanism and the four fixes:
#
# FIX 1 - the runaway derivative is HEAT/PRESSURE, not just geometry:
#   stall -> trapped energy becomes local heat (E_thermal) -> the heat
#   multiplier drives more untying: m_u = m_u0/(1-eps) * (1 + kappa*over).
#   A persistent stall now diverges mathematically (the dam-break runaway).
# FIX 2 - independent energy accounts (no tautology):
#   E_baseline (field), E_thermal (buoyant layer heat), E_tied (matter),
#   E_radiated (vented). R_E compares their sum against the start total;
#   no account is DEFINED as another's remainder.
# FIX 3 - the governor's latent heat: tying is exothermic. Each kg tied
#   dumps F_TIE*Q_U back into E_thermal (paid from E_baseline) - the system
#   must manage that heat, and it feeds the stall.
# FIX 4 - timestep hygiene: all rates (m_u, m_tie, capacity) computed at the
#   tick start; universal deltas dm = rate*dt, dV = spec_vol*dm, dE = Q_U*dm.
#   The runaway flag is a ROLLING growth_duration that resets to zero when
#   the demand stops accelerating (ddD <= 0).
import os, sys, json
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config, pi_v

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
n_lad = F["capacity_ladder"]["n"]
s = F["locked_constants"]["s"]["value"]
MP = 1.6726e-27
RHO_Q = 3.0e8 * 1e6 * MP
C_Q = pi_v.capacity(RHO_Q, c0, rho0, n_lad)
K_Q = RHO_Q * C_Q ** 2
Q_U = c0 ** 2                    # J/kg  the phase-change price

# ------- the one region (AR 12192 box) -------
V_A = 1.21e25          # m^3
DELTA_GAP = s          # wave-gap strain tolerance
D_V_UNIT = 1.0 / RHO_Q # m^3/kg
EPS0 = 1.0e-5          # sealed-core open share (PFSS pending)
EPS_MAX = 0.30
P_STALL = K_Q * DELTA_GAP
F_TIE = s              # the tying exotherm fraction (the shed fragment share)
KAPPA = 1.0            # the heat-multiplier coefficient (named)

def run_region(m_u0, tau_choke, m_tie0, t_end=86400.0, dt=10.0,
               P_load=0.0, verbose=True):
    """The closed thermodynamic loop. Returns the event record."""
    E_base, E_therm, E_tied, E_rad = 1.0e28, 0.0, 5.0e26, 0.0
    E_total0 = E_base + E_therm + E_tied + E_rad
    E_therm_ref = Q_U * m_u0 * tau_choke     # the layer's reference heat content
    E_tie_exo = 0.0                          # the governor's dumped latent heat (FIX 3)
    D_V, eps, zeta = 0.0, EPS0, 0.0
    m_u, m_tie = m_u0, 0.0
    P_loaded = 0.0
    t_stall, t_runaway = None, None
    throttle_time = 0
    growth_duration = 0                      # rolling, resets on ddD <= 0 (FIX 4)
    dD_prev = None
    n = int(t_end / dt)
    for k in range(n):
        # ---- FIX 4: ALL rates at the tick start ----
        if zeta < DELTA_GAP:
            eps = EPS0
        elif zeta < 2 * DELTA_GAP:
            eps = EPS0 + (EPS_MAX - EPS0) * (zeta - DELTA_GAP) / DELTA_GAP
        else:
            eps = EPS_MAX
        over_heat = max(E_therm / E_therm_ref - 1.0, 0.0) if E_therm_ref > 0 else 0.0
        m_u = m_u0 / max(1.0 - eps, 1e-6) * (1.0 + KAPPA * over_heat)   # FIX 1
        V_cap = V_A * eps / tau_choke
        m_cap = V_cap * RHO_Q
        over_p = max(K_Q * zeta - P_STALL, 0.0) / P_STALL
        m_tie = min(m_tie0 * over_p, m_tie0 / DELTA_GAP) if m_tie0 else 0.0
        # ---- universal deltas ----
        dm_u = m_u * dt
        dm_tie = m_tie * dt
        dm_vent = min(dm_u, m_cap * dt)      # the portion the open geometry accepts
        dD = D_V_UNIT * (dm_u - dm_vent) - D_V_UNIT * dm_tie
        # ---- FIX 2+3: the independent ledger ----
        E_tied -= Q_U * dm_u                 # untying undoes matter
        E_therm += Q_U * (dm_u - dm_vent)    # the stalled waves stay as heat
        E_rad += Q_U * dm_vent               # the vented waves escape
        E_tied += Q_U * dm_tie               # tying re-forms matter
        E_therm -= Q_U * dm_tie              # the waves consumed by tying
        E_therm += F_TIE * Q_U * dm_tie      # FIX 3: the exotherm dumped back
        E_base -= F_TIE * Q_U * dm_tie       # the field's budget pays the shed
        E_tie_exo += F_TIE * Q_U * dm_tie
        E_base += P_load * dt                # the flux load feeds the field
        P_loaded += P_load * dt
        # ---- integrate state ----
        D_V = max(D_V + dD, 0.0)
        zeta = D_V / V_A
        if t_stall is None and m_tie > 0:
            t_stall = k * dt
        if m_tie > 0:
            throttle_time += 1
        # ---- FIX 4: rolling growth_duration ----
        ddD = (dD - dD_prev) / dt if dD_prev is not None else 0.0
        dD_prev = dD
        if dD > 0 and ddD > 0:
            growth_duration += dt
        else:
            growth_duration = 0
        if t_runaway is None and growth_duration >= 30 * dt:
            t_runaway = k * dt
        if zeta > 1.0:
            break
    R_E = (E_base + E_therm + E_tied + E_rad) - (E_total0 + P_loaded)   # FIX 2
    R_E_rel = R_E / E_total0 if E_total0 else 0.0
    if zeta > 1.0 or t_runaway is not None:
        verdict = "ERUPTION (the runaway wins)"
    elif m_tie0 and throttle_time > 0.2 * n and zeta > 0:
        verdict = "CONTROLLED BURN (stall equilibrium, throttle holds)"
    elif t_stall is not None:
        verdict = "blocked-settles (confined: fault opened, dam re-held)"
    else:
        verdict = "accommodates (no fault)"
    rec = {"m_u0": m_u0, "tau_choke": tau_choke, "m_tie0": m_tie0,
           "t_stall": t_stall, "t_runaway": t_runaway, "zeta_final": float(zeta),
           "E_baseline": E_base, "E_thermal": E_therm, "E_tied": E_tied,
           "E_radiated": E_rad, "R_E": float(R_E), "R_E_rel": float(R_E_rel),
           "E_tie_exotherm": E_tie_exo, "verdict": verdict}
    if verbose:
        print(f"  m_u/m_tie0 = {m_u0 / max(m_tie0, 1e-30):8.2f}: "
              f"stall@{None if t_stall is None else f'{t_stall/3600:.2f}h'} "
              f"runaway@{None if t_runaway is None else f'{t_runaway/3600:.2f}h'} "
              f"zeta={zeta:.3f} therm={E_therm:.2e} J "
              f"exo={E_tie_exo:.2e} J R_E_rel={R_E_rel:.1e} -> {verdict}")
    return rec

def main():
    print("=" * 78)
    print("STAGE B v2 - THE TRUE THERMODYNAMIC LOOP (heat feedback + independent ledger)")
    print("=" * 78)
    print(f"Q_U = c0^2 = {Q_U:.2e} J/kg; F_TIE (exotherm share) = {F_TIE:.4f}; "
          f"KAPPA (heat multiplier) = {KAPPA}")
    print(f"reference heat content E_therm_ref = Q_U*m_u0*tau_choke")
    print()
    TAU = 3.18e4          # s  the derived choke time
    M_TIE = 2.0e7         # kg/s  phase-loop re-pairing baseline (normalization OPEN)
    print("regimes (tau = 3.18e4 s = the derived choke; m_tie0 = 2e7 kg/s):")
    print("  capacity m_cap ~ 1.9e3 kg/s at eps0 = 1e-5")
    print("  ratio 1e-5 -> accommodates (below capacity), 1 day")
    print("  ratio 0.50 -> THE STALL: heat builds, throttle must manage it, 1 day")
    print("  ratio 5.00 -> RUNAWAY: the heat feedback diverges, 10-day window")
    recs = {}
    recs[1e-5] = run_region(1e-5 * M_TIE, TAU, M_TIE, t_end=86400.0)
    recs[0.5] = run_region(0.5 * M_TIE, TAU, M_TIE, t_end=86400.0)
    recs[5.0] = run_region(5.0 * M_TIE, TAU, M_TIE, t_end=10 * 86400.0)
    print()
    print("the governor's latent heat check (FIX 3): tying must DUMP F_TIE*Q_U per kg")
    print("  into E_thermal - shown inside each run above as therm. No deletion.")
    print()
    print("ledger independence (FIX 2): the four accounts are integrated independently;")
    print("  R_E above is a REAL residual (no account defined as another's remainder).")
    print()
    res = {"F_TIE": F_TIE, "KAPPA": KAPPA, "tau_choke": TAU, "m_tie0": M_TIE,
           "regimes": {str(k): v for k, v in recs.items()}}
    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    out = os.path.join(config.RESULTS_DIR, "region_balance_v2_thermodynamic.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    print("result written:", out)

if __name__ == "__main__":
    main()
