#!/usr/bin/env python
"""passage_run.py — PWC passage-chart numerical passes (2026-10-08).

RUN 1: Bernoulli stagnation of the ambient (gas EoS P = rho c0^2/3).
RUN 2: Max-P cap thickening above the 954 km/s threshold (shell-sourced).
RUN 3: the through-flow fold with c_loc(rho) instead of c_s — does v_c converge to 954?
"""
import numpy as np

c0 = 2.99792458e8
Y = 5.93e26
rho_max = 1.304e15
rho0 = 8.74e-27
stall_rho = rho0 * np.exp(1.5)          # c_loc -> 0 at 4.48 rho0 (EoS carrier law)

print("=" * 70)
print("RUN 1 — Bernoulli stagnation: rho_stag = rho_amb * exp(3 v^2 / 2 c0^2)")
print("=" * 70)
for v in [954e3, 3000e3, 1e7, 0.1 * c0, c0]:
    ratio = np.exp(1.5 * v ** 2 / c0 ** 2)
    print(f"  v = {v/1e3:12.1f} km/s   rho_stag/rho_amb = {ratio:.6g}")
print(f"  stall density = {stall_rho/rho0:.4f} rho0  <- stagnation at exactly v = c0")
print("  => ram compression of rho0 ambient is 1e-5..4.5x: the visible bow is")
print("     accumulated ambient at ~rho0, not compressed medium. Cap must be shell-sourced.")

print()
print("=" * 70)
print("RUN 2 — cap thickening above threshold: r_cap*l_cap = r_shell^2 * v/(2 c0)")
print("=" * 70)
for v in [800e3, 954e3, 1000e3, 2000e3, 3000e3, 1e7]:
    state = "BELOW cap (no cap)" if v < 954e3 else "cap forms"
    ratio = np.sqrt(v / (2 * c0))
    print(f"  v = {v/1e3:12.1f} km/s  r_cap/r_shell = {ratio:.4f}   [{state}]")
print("  RBH-1 shell edge 64-91 Mm -> cap ~ 2.6-3.6 Mm at 954 km/s: sub-resolution")
print("  (matches repo: shell bow wave < 1e-9 pc). The 192 pc structure is gas pile.")

print()
print("=" * 70)
print("RUN 3 — the fold with c_loc(rho): v_c = max[rho(1-rho/rho_max) c_loc(rho)]/rho_amb")
print("=" * 70)

def cloc(rho):
    x = rho / rho0
    return c0 * np.sqrt(np.clip(1.0 - (2.0 / 3.0) * np.log(x), 0.0, None))

def F(rho):
    return rho * (1.0 - rho / rho_max) * cloc(rho)

rhos = np.geomspace(rho0, stall_rho, 4000)
Fm = F(rhos)
imax = int(np.argmax(Fm))
print(f"  max through-flow capacity at rho/rho0 = {rhos[imax]/rho0:.4f}"
      f"  (stall at {stall_rho/rho0:.4f})")
print(f"  F_max / (rho0 c0) = {Fm[imax]/(rho0*c0):.4f}"
      f"  ->  v_c(rho_amb=rho0) = {Fm[imax]/rho0/1e3:.4g} km/s   vs  c0 = {c0/1e3:.4g} km/s")
print(f"  v_c(rho_amb=rho_max) = {Fm[imax]/rho_max*1e3:.3g} km/s  -> sealed at any speed")
print("  VERDICT: the c_loc-corrected fold does NOT converge to 954.")
print("  Three thresholds, three regimes:")
print("    through-flow fold: 1.57 c0 (unreachable sub-c -> matter never drags)")
print("    cap formation:     954 km/s (Y alone, shell stagnation)")
print("    locked state:      0 (rho_max ambient, ceiling)")

print()
print("=" * 70)
print("RUN 4 — pulsar bow-shock check (literature numbers, wind confound flagged)")
print("=" * 70)
rows = [
    ("PSR B2224+65 (Guitar)", 1600, "uncertain distance (repo log)"),
    ("PSR B1508+55", 1083, "+1.3 sigma vs 954 (repo log)"),
    ("PSR J2124-3358", 100, "bow shock at LOW v: wind-ISM balance, not drag"),
    ("PSR J0437-4715", 104, "nearest millisecond pulsar, no bow shock"),
]
print(f"  {'name':22s} {'v km/s':>9s}   note")
for n, v, note in rows:
    print(f"  {n:22s} {v:9d}   {note}")
print("  Standard bow-shock standoff: R_bs = sqrt(E_dot/(4 pi c rho_amb v^2))")
print("  -> bow shocks form at LOW v in DENSE ambient (wind balance), so the")
print("     drag-ridge test must use wakes/asymmetry, not bow presence alone.")
