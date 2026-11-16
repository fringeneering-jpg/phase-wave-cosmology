# stage3_stageC_radial_sun.py - Stage C: the radial Sun in finite-volume shells
# (Perplexity's build order: one-region balance closes -> extend radially.)
# Shell i carries the SAME machinery as Stage B (stall, throttle, heat
# feedback) with the radial energy channels:
#   the heat channel:  L_{i+1} = L_i - draw_i + exo_i   (the medium's flux)
#   the escape channel: R_{i+1} = R_i + vent_i          (the vented waves)
#   the bath:          bath = draw - vent - exo         (the room-making
#                       absorption - the outskirts of the universe)
# The block location is FOUND as the crossing Pi_V = 1 - not prescribed.
# Comparison inputs (stated, not claimed as predictions): the standard
# density anchors, Q_core = 3.92e26 W, T_core = 1.57e7 K, T_surface = 5800 K.
# Model outputs: T_corona, the stall location, the equilibrium corona state,
# and the grid-refinement convergence of the vented total (the residual).
import os, sys, json, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config, pi_v
from stage3_region_balance import run_region, Q_U, F_TIE

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]
n_lad = F["capacity_ladder"]["n"]
f_vent = F["global_anchors"]["f_vent"]["value"]
mdot_deep = F["global_anchors"]["mdot_deep"]["value"]
MP = 1.6726e-27
KB = 1.3806e-23

R_SUN = 6.96e8
Q_CORE = mdot_deep * c0 ** 2           # W  the forge's exotherm (deep source)
EPS_SEALED = 1.0e-5
TAU_CHOKE = 3.18e4                      # s  the derived absorption-limited choke

def build_grid(N=80, r_min=1.0e7, r_max=2.5e9):
    r = np.geomspace(r_min, r_max, N)
    edges = np.concatenate([[r_min], (r[1:] + r[:-1]) / 2, [r_max]])
    return r, np.diff(edges)

def density_profile(r):
    """Comparison input: interior (central 1.5e5), chromosphere (sharp,
    scale 5e5 m), transition (5e5 m), corona floor at 1e-12 kg/m^3."""
    rho = np.empty_like(r, dtype=float)
    interior = r <= R_SUN
    rho[interior] = 1.5e5 * (1.0 - (r[interior] / R_SUN) ** 2) + 2.0e-4
    above = ~interior
    h_full = r - R_SUN
    rho[above] = 2.0e-4 * np.exp(-h_full[above] / 5.0e5)   # chromosphere
    tr = rho <= 1.0e-10
    rho[tr] = 1.0e-10 * np.exp(
        -(h_full[tr] - 5.0e5 * np.log(2.0e-4 / 1.0e-10)) / 5.0e5)
    rho = np.clip(rho, 1.0e-12, None)             # the corona proper
    return rho

def eps_a_profile(r):
    """Field-geometry input (Stage D derives it from PFSS): the EXCHANGE
    BAND. The sealed and open field states BLEND through the corona - a
    broad linear mixing zone, not a wall. eps = the open share of the blend."""
    blend = (r - 1.01 * R_SUN) / (0.9 * R_SUN)
    return np.clip(EPS_SEALED + (1.0 - EPS_SEALED) * blend, EPS_SEALED, 1.0)

def run_stageC(N=80, verbose=True):
    r, dr = build_grid(N)
    rho = density_profile(r)
    C = pi_v.capacity(rho, c0, rho0, n_lad)
    eps = eps_a_profile(r)
    piv = (C / c0) ** 2 / np.maximum(eps, 1e-9)

    # ---- the FOUND block location: where Pi_V crosses 1 IN THE CORONA ----
    corona = rho <= 1.01e-12
    above = np.where(piv > 1.0)[0]
    blk = [i for i in above if corona[i]]
    r_block = float(r[blk[-1]]) if blk else float("nan")     # outermost blocked shell
    opened = [i for i in range(len(r)) if corona[i] and piv[i] <= 1.0]
    r_open = float(r[opened[0]]) if opened else float("nan")

    # ---- the steady energy channels (volume-weighted demand) ----
    cor_mask = rho <= 1.01e-12
    V_cor = np.sum(4.0 * np.pi * r[cor_mask] ** 2 * dr[cor_mask])
    L = np.zeros(N)
    L[0] = Q_CORE
    vented = np.zeros(N)
    exo = np.zeros(N)
    bath = np.zeros(N)
    for i in range(N):
        if i == 0:
            continue
        V_i = 4.0 * np.pi * r[i] ** 2 * dr[i]
        if r[i] <= R_SUN:
            L[i] = L[i - 1]                # interior: the flux passes through
            continue
        # the corona's untying demand distributes through its volume
        draw = Q_CORE * (V_i / V_cor)
        m_u0 = draw / c0 ** 2
        # the EXCHANGE capacity: the blend's overlap eps*(1-eps) - maximal
        # where the fields mix half-and-half (the exchange geometry itself)
        m_cap = V_i * eps[i] * (1.0 - eps[i]) * rho[i] / TAU_CHOKE
        vent = min(m_u0, m_cap) * c0 ** 2
        exo_i = F_TIE * vent               # the throttle's shed share (on the tied part)
        vented[i] = vent
        exo[i] = exo_i
        bath[i] = draw - vent - exo_i      # the net absorbed (room-making)
        L[i] = max(L[i - 1] - (draw - exo_i), 0.0)

    V_out = float(np.sum(vented))
    B_out = float(np.sum(bath))
    E_out = float(np.sum(exo))
    # the exotherm lives INSIDE the heat channel (L); the outs are vent + bath
    R_E = (V_out + B_out + L[-1]) - Q_CORE       # the global ledger

    # the corona's temperature: the frozen observation equation at 1e-12
    T_corona = f_vent * MP * pi_v.capacity(1.0e-12, c0, rho0, n_lad) ** 2 / KB

    res = {"N": N, "r_block_found": r_block, "r_open_found": r_open,
           "Pi_V_at_corona_base": float(piv[corona][0]),
           "T_corona_MK": float(T_corona) / 1e6,
           "vented_W": V_out, "bath_W": B_out, "exotherm_W": E_out,
           "L_end_W": float(L[-1]), "R_E_W": float(R_E),
           "R_E_rel": float(R_E) / Q_CORE, "Q_core_W": Q_CORE}
    if verbose:
        print(f"  N={N:3d}: block from the corona's base out to r = "
              f"{r_block/R_SUN:.3f} R_sun (opens at {r_open/R_SUN:.3f} R_sun)")
        print(f"          Pi_V at the corona's base = {res['Pi_V_at_corona_base']:.0f}, "
              f"T_corona = {res['T_corona_MK']:.2f} MK")
        print(f"          the exchange band: eps from {EPS_SEALED:.0e} (base) to 1 "
              f"(~1.9 R_sun), mixing peak at eps=0.5 near "
              f"{1.01 + 0.45:.2f} R_sun")
        print(f"          vented = {V_out:.2e} W, bath = {B_out:.2e} W, "
              f"exotherm = {E_out:.2e} W, R_E_rel = {res['R_E_rel']:.2e}")
    return res

if __name__ == "__main__":
    print("=" * 78)
    print("STAGE C - THE RADIAL SUN IN FINITE-VOLUME SHELLS")
    print("=" * 78)
    print(f"Q_core (the forge's exotherm, deep channel) = {Q_CORE:.2e} W  [imposed]")
    print(f"comparison inputs: rho_c = 1.5e5 kg/m^3, photosphere 2e-4, corona 1e-12;")
    print(f"  T_core = 1.57e7 K, T_surface = 5800 K (the phase pin).")
    print(f"model outputs: T_corona (frozen equation), the stall location (FOUND),")
    print(f"  the steady split (vented/bath/exotherm), grid convergence.")
    print()
    r1 = run_stageC(N=40)
    r2 = run_stageC(N=80)
    print()
    print("the comparison table:")
    print(f"  L (imposed via the deep-channel source): {Q_CORE:.2e} W  [anchor, not predicted]")
    print(f"  T_corona (model): {r2['T_corona_MK']:.2f} MK vs observed ~1.5-2 MK")
    print(f"  T_surface (phase pin): 5800 K  [pin input; pin derivation = open item]")
    print(f"  stall location (FOUND): the corona is blocked from its base to "
          f"{r2['r_block_found']/R_SUN:.3f} R_sun")
    print(f"  vented (the coronal escape): {r2['vented_W']:.2e} W vs the observed")
    print(f"    coronal XUV share ~1e21 W")
    print(f"  grid convergence: vented {r1['vented_W']:.3e} (N=40) -> "
          f"{r2['vented_W']:.3e} (N=80) W")
    print(f"  global ledger: R_E_rel = {r2['R_E_rel']:.2e}")
    print()
    res = {"N40": r1, "N80": r2}

    def _finite(v):
        """JSON hygiene: non-finite floats are not valid strict JSON; write them as strings."""
        if isinstance(v, float) and not math.isfinite(v):
            return "nan" if math.isnan(v) else ("inf" if v > 0 else "-inf")
        if isinstance(v, dict):
            return {k: _finite(x) for k, x in v.items()}
        if isinstance(v, (list, tuple)):
            return [_finite(x) for x in v]
        return v

    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    out = os.path.join(config.RESULTS_DIR, "stageC_radial_sun.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(_finite(res), fh, indent=1)
    print("result written:", out)
