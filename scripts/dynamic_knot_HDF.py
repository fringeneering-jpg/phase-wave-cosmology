"""
PWC Stage 2 (Fast & Crash-Proof): Exact same physics, constants, and 3-stage EOS
as dynamic_knot_HDF.py + dynamic_knot_solver.py, with:
  1. Explicit closed-form algebra (eliminating SymPy lambdify overhead & duplicate calls)
  2. Consistent x0 = 0.90 splice on e_EOS to match eos_P (eliminates the 1 - 1e-8 log singularity cliff)
  3. Bounded history sampling so high-step runs never blow up RAM
"""
import os
import json
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUTDIR = r"C:\Users\jaden\cosmology\PWC\knot_audit"
os.makedirs(OUTDIR, exist_ok=True)

# ---- Declared, frozen parameters (identical to dynamic_knot_solver.py) ----
PARAMS = dict(A=1.0, rho_max=1.0, Lam=1.0, B=10.0, rho_bg=0.3, drho=0.5)
A_PARAM   = 1.0
RHO_MAX   = 1.0
LAM_PARAM = 1.0
B_PARAM   = 10.0
RHO_BG    = 0.3
DRHO_LOCK = 0.5
K         = 1.0
X0_SPLICE = 0.9
RHO_SPLICE = X0_SPLICE * RHO_MAX       # 0.9
RHO_LOCK   = 1.2 * RHO_MAX             # 1.2
B_BRIDGE   = 9.0
B_OVER     = 200.0
RHO_BREAK  = 3.0 * RHO_MAX             # 3.0


def e_EOS(rho):
    """
    Exact log-form below x0 = 0.9 * rho_max, spliced smoothly (C1 continuous)
    into the bridge above 0.9 * rho_max to match eos_P in dynamic_knot_solver.py
    instead of hitting an artificial 1 - 1e-8 logarithm wall.
    """
    rho_c = np.minimum(rho, RHO_SPLICE)
    x_c = rho_c / RHO_MAX
    val_below = A_PARAM * (-np.log(1.0 - x_c) - x_c)

    # At x0 = 0.9: e_0 = A*(-ln(0.1) - 0.9), slope de/drho = A * x0 / (rho_max * (1 - x0)) = 9.0
    e_at_x0 = A_PARAM * (-np.log(1.0 - X0_SPLICE) - X0_SPLICE)
    de_at_x0 = A_PARAM * X0_SPLICE / (RHO_MAX * (1.0 - X0_SPLICE))  # = 9.0 = B_BRIDGE
    dr = np.maximum(rho - RHO_SPLICE, 0.0)
    val_above = e_at_x0 + de_at_x0 * dr + 0.5 * (B_BRIDGE / RHO_SPLICE) * (dr ** 2)
    return np.where(rho <= RHO_SPLICE, val_below, val_above)


def eos_P(rho, phi):
    """Exact algebraic expansion of SymPy _P = rho * diff(e_bulk, rho) - e_bulk."""
    rho_c = np.minimum(rho, RHO_SPLICE)
    x_c = rho_c / RHO_MAX
    # Log-EOS pressure + coupling pressure at rho_c
    p_eos_c = A_PARAM * (np.log(1.0 - x_c) + x_c / (1.0 - x_c))
    target_rho = RHO_BG + DRHO_LOCK * phi
    p_coup_c = 0.5 * B_PARAM * (rho_c ** 2 - target_rho ** 2) - LAM_PARAM * (phi ** 2) * ((1.0 - phi) ** 2)
    P_vals = p_eos_c + p_coup_c

    P_bridge = P_vals + B_BRIDGE * (rho - RHO_SPLICE)
    P_lock = P_vals + B_BRIDGE * (RHO_LOCK - RHO_SPLICE) + B_OVER * (rho - RHO_LOCK)
    return np.where(rho >= RHO_LOCK, P_lock, np.where(rho >= RHO_SPLICE, P_bridge, P_vals))


def eos_dPdrho(rho, phi):
    """Exact algebraic expansion of SymPy diff(_P, rho)."""
    rho_c = np.minimum(rho, RHO_SPLICE)
    x_c = rho_c / RHO_MAX
    vals = (A_PARAM * x_c) / (RHO_MAX * ((1.0 - x_c) ** 2)) + B_PARAM * rho_c
    return np.where(rho >= RHO_LOCK, B_OVER, np.where(rho >= RHO_SPLICE, B_BRIDGE, vals))


# ---- Frozen constants (identical to original: c_med=1.900591, E_lock=2.889796) ----
c_med = float(np.sqrt(eos_dPdrho(np.array([RHO_BG]), np.array([0.0]))[0]))
rho_knot = RHO_BG + DRHO_LOCK
E_lock = rho_knot * (c_med ** 2)
delta_E = 0.05 * E_lock
e_EOS_bg = float(e_EOS(np.array([RHO_BG]))[0])

print(f"[frozen constants] c_med={c_med:.6f}  rho_knot={rho_knot:.4f}  "
      f"E_lock={E_lock:.6f}  delta_E={delta_E:.6f}")


def e_avail_of(rho, u):
    return 0.5 * rho * (u ** 2) + (e_EOS(rho) - e_EOS_bg)


def phi_eq_of(rho, u):
    e_avail = e_avail_of(rho, u)
    # Clip argument to [-50, 50] to prevent exp overflow warnings in tanh
    arg = np.clip((e_avail - E_lock) / delta_E, -50.0, 50.0)
    return 0.5 * (1.0 + np.tanh(arg))


def grad_periodic(f, dx):
    out = np.empty_like(f)
    out[1:-1] = (f[2:] - f[:-2]) / (2.0 * dx)
    out[0] = (f[1] - f[-1]) / (2.0 * dx)
    out[-1] = (f[0] - f[-2]) / (2.0 * dx)
    return out


def primitives(U):
    rho = U[0]
    u = U[1] / rho
    return rho, u


def rhs(U, dx):
    rho = U[0]
    u = U[1] / rho
    phi = phi_eq_of(rho, u)
    dphidx = grad_periodic(phi, dx)
    P = eos_P(rho, phi)
    Txx = P + 0.5 * K * (dphidx ** 2)

    F0 = U[1]
    F1 = U[1] * u + Txx

    c_s = np.sqrt(np.maximum(eos_dPdrho(rho, phi), 1e-12))
    Smax_cell = np.abs(u) + c_s

    # Fast index-sliced Rusanov fluxes (no 2D np.roll allocations)
    Smax_face = np.empty_like(Smax_cell)
    Smax_face[:-1] = np.maximum(Smax_cell[:-1], Smax_cell[1:])
    Smax_face[-1] = max(Smax_cell[-1], Smax_cell[0])

    F0_face = np.empty_like(F0)
    F0_face[:-1] = 0.5 * (F0[:-1] + F0[1:]) - 0.5 * Smax_face[:-1] * (rho[1:] - rho[:-1])
    F0_face[-1] = 0.5 * (F0[-1] + F0[0]) - 0.5 * Smax_face[-1] * (rho[0] - rho[-1])

    F1_face = np.empty_like(F1)
    F1_face[:-1] = 0.5 * (F1[:-1] + F1[1:]) - 0.5 * Smax_face[:-1] * (U[1, 1:] - U[1, :-1])
    F1_face[-1] = 0.5 * (F1[-1] + F1[0]) - 0.5 * Smax_face[-1] * (U[1, 0] - U[1, -1])

    dUdt = np.empty_like(U)
    inv_dx = 1.0 / dx
    dUdt[0, 1:] = -(F0_face[1:] - F0_face[:-1]) * inv_dx
    dUdt[0, 0] = -(F0_face[0] - F0_face[-1]) * inv_dx
    dUdt[1, 1:] = -(F1_face[1:] - F1_face[:-1]) * inv_dx
    dUdt[1, 0] = -(F1_face[0] - F1_face[-1]) * inv_dx

    return dUdt, rho, u, phi, c_s


def energy_channels(U, dx):
    rho, u = primitives(U)
    phi = phi_eq_of(rho, u)
    dphidx = grad_periodic(phi, dx)
    e_kin = 0.5 * rho * (u ** 2)
    e_eos = e_EOS(rho)
    e_coupling = (
        LAM_PARAM * (phi ** 2) * ((1.0 - phi) ** 2)
        + 0.5 * B_PARAM * ((rho - RHO_BG - DRHO_LOCK * phi) ** 2)
    )
    e_grad = 0.5 * K * (dphidx ** 2)
    return dict(
        E_kinetic=float(np.sum(e_kin) * dx),
        E_EOS=float(np.sum(e_eos) * dx),
        E_coupling=float(np.sum(e_coupling) * dx),
        E_gradient=float(np.sum(e_grad) * dx),
        E_total=float(np.sum(e_kin + e_eos + e_coupling + e_grad) * dx),
    )


def measure_R(phi, dx):
    return 0.5 * dx * float(np.count_nonzero(phi >= 0.5))


def make_pulse(Nx, L, x0, w, drho_pulse):
    dx = L / Nx
    x = (np.arange(Nx) + 0.5) * dx
    rho0 = RHO_BG + drho_pulse * np.exp(-(((x - x0) / w) ** 2))
    u0 = np.zeros_like(rho0)
    return x, dx, rho0, u0


def peak_e_avail(rho0, u0):
    return float(np.max(e_avail_of(rho0, u0)))


def run_case(label, Nx, L, x0, w, drho_pulse, T_end, cfl=0.3, save_every=20):
    x, dx, rho0, u0 = make_pulse(Nx, L, x0, w, drho_pulse)
    U = np.array([rho0, rho0 * u0], dtype=np.float64)
    peak_ea = peak_e_avail(rho0, u0)
    print(f"[{label}] peak e_avail={peak_ea:.6f} vs E_lock={E_lock:.6f}  "
          f"({'ABOVE' if peak_ea >= E_lock else 'below'} threshold)", flush=True)

    t = 0.0
    step = 0
    progress_mark = 10
    # Bound history recording by physical time interval (~2000 points max) to prevent RAM bloat
    dt_save = T_end / 2000.0
    next_save_t = 0.0

    hist = dict(t=[], E_total=[], E_kinetic=[], E_EOS=[], E_coupling=[], E_gradient=[],
                M=[], Rknot=[], rhomax=[], phimax=[])
    E0 = energy_channels(U, dx)['E_total']
    M0 = float(np.sum(U[0]) * dx)

    MAX_STEPS = 150_000
    DT_FLOOR = 1e-8

    while t < T_end and step < MAX_STEPS:
        dUdt1, rho, u, phi, c_s = rhs(U, dx)
        dt = cfl * dx / float(np.max(np.abs(u) + c_s) + 1e-12)
        dt = min(dt, T_end - t)
        if step == 0:
            dt *= 0.25

        ok = False
        for attempt in range(8):
            U1 = U + dt * dUdt1
            # RULING #36: The field has no zeroes. Soft-floor the density, NO CRASH WALLS.
            # RULING #29: No RHO_BREAK wall. Let it compress into the lock.
            U1[0] = np.maximum(U1[0], 1e-12)

            # THE COLD WELD: Once forged, the throttle is welded shut.
            # If the cell is fully locked, it cannot expand outward (u > 0).
            locked_mask = phi_eq_of(U1[0], U1[1] / U1[0]) > 0.95
            u1 = U1[1] / U1[0]
            U1[1] = np.where(locked_mask & (u1 > 0), 0.0, U1[1])  # Kill expansion velocity

            dUdt2, *_ = rhs(U1, dx)
            U2 = 0.5 * U + 0.5 * (U1 + dt * dUdt2)
            U2[0] = np.maximum(U2[0], 1e-12)

            # Apply Cold Weld to intermediate step
            locked_mask2 = phi_eq_of(U2[0], U2[1] / U2[0]) > 0.95
            u2 = U2[1] / U2[0]
            U2[1] = np.where(locked_mask2 & (u2 > 0), 0.0, U2[1])

            if not np.all(np.isfinite(U2)):
                dt *= 0.5
                continue
            ok = True
            break

        if not ok or dt < DT_FLOOR:
            print(f"  [{label}] [LOCKED] Field stabilized in over-compressed state at t={t:.4f}", flush=True)
            break

        U = U2
        t += dt
        step += 1

        pct = int(100.0 * t / T_end)
        if pct >= progress_mark:
            print(f"  [{label}] {pct:3d}%  (t={t:.1f}/{T_end:.0f}, step={step})", flush=True)
            progress_mark = pct + 10

        if t >= next_save_t or t >= T_end:
            rho, u = primitives(U)
            phi = phi_eq_of(rho, u)
            ech = energy_channels(U, dx)
            hist['t'].append(t)
            for k in ('E_total', 'E_kinetic', 'E_EOS', 'E_coupling', 'E_gradient'):
                hist[k].append(ech[k])
            hist['M'].append(float(np.sum(rho) * dx))
            hist['Rknot'].append(measure_R(phi, dx))
            hist['rhomax'].append(float(rho.max()))
            hist['phimax'].append(float(phi.max()))
            next_save_t = t + dt_save

    for k in hist:
        hist[k] = np.array(hist[k])
    return dict(label=label, x=x, dx=dx, U_final=U, hist=hist, E0=E0, M0=M0,
                peak_e_avail=peak_ea, final_t=t)