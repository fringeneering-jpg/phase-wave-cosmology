# anchor_closure_test.py - THE ANCHOR CLOSURE: does the taut field's own tension set the ceiling?
# (2026-10-21, auditor run; locked constants only, no GW150914 masses; kill conditions pre-stated)
# Test 1: rho_max = (2*Y_bow/c0^2)^(1/(1-2n)) * rho0^(-2n/(1-2n))  vs the shell read 1.304e15
# Test 2: the two C(rho_max) routes - capacity ladder vs yield law (must agree at the ceiling)
# Test 3: the T2 resting-density algebra check (0.24880013 vs stated 1/4)
# Verdict rules (pre-stated): CLOSED only if the LOCKED n = 0.0606 closes within 0.4% on both
# tests; otherwise rho_max -> BACK-SOLVED pending the author's ruling on the n-origin.
import math

c0 = 2.99792458e8          # m/s, locked (Maxwell)
rho0 = 8.74e-27            # kg/m^3, locked
rho_max_shell = 1.304e15   # kg/m^3, the GW150914 shell read (the number under test)
n = 0.0606                 # locked capacity exponent
Y_bow = 5.9307e26          # Pa, locked (the densification's yield, from the electron's own pieces)

print("=" * 78)
print("TEST 1 + 2 - THE ANCHOR CLOSURE (locked constants only)")
print("=" * 78)

C_yield = math.sqrt(2.0 * Y_bow / rho_max_shell)          # the yield route
C_ladder = c0 * (rho0 / rho_max_shell) ** n               # the capacity-ladder route
C_gap = (C_ladder / C_yield - 1.0) * 100.0

n_closing = math.log(C_yield / c0) / math.log(rho0 / rho_max_shell)
rho_max_closed = ((2.0 * Y_bow / c0**2) ** (1.0 / (1.0 - 2.0 * n))
                  * rho0 ** (-2.0 * n / (1.0 - 2.0 * n)))
resid = (rho_max_closed / rho_max_shell - 1.0) * 100.0

print(f"C_yield  (sqrt(2*Y_bow/rho_max)) : {C_yield/1e3:10.2f} km/s")
print(f"C_ladder (c0*(rho0/rho_max)^n)  : {C_ladder/1e3:10.2f} km/s")
print(f"C-gap    (ladder vs yield)      : {C_gap:+10.4f} %   (must be 0)")
print(f"n_closing required              : {n_closing:.6f}  vs locked n = {n}  ({100*(n_closing/n - 1):+.4f} %)")
print(f"rho_max_closed at locked n      : {rho_max_closed:.5e} kg/m^3")
print(f"GW150914 shell read             : {rho_max_shell:.5e} kg/m^3")
print(f"residual                        : {resid:+.4f} %")
print()
print("VERDICT (per pre-stated kill):")
if abs(resid) <= 0.4 and abs(C_gap) <= 0.4:
    print("  CLOSED - the taut field's tension sets the ceiling; rho_max -> DERIVED")
else:
    print(f"  NOT CLOSED - residual {resid:+.3f} % / C-gap {C_gap:+.3f} % at the LOCKED n.")
    print("  The ceiling is owed on the ledger: rho_max -> BACK-SOLVED pending the")
    print(f"  author's ruling on the n-origin (closing needs n = {n_closing:.6f}, "
          f"+{100*(n_closing/n - 1):.3f} %).")

print()
print("=" * 78)
print("TEST 3 - THE T2 RESTING-DENSITY ALGEBRA (ruling 3: finite-geometry equilibrium)")
print("=" * 78)
required = 0.24880013
stated = 0.25
print(f"required eta*(<v>/c0) = {required}   vs stated eta = 1/4, <v> = c0 -> {stated}")
print(f"discrepancy           = {100*(required/stated - 1):+.4f} %")
print("VERDICT: as printed, rho0 cancels from the rho_dot equations; the equilibrium does")
print("not deliver rho0 = 8.74e-27. OPEN - the finite bounding scale must be named")
print("(candidate: the Hubble-wall front / R_H) before rho0's DERIVED label can stand.")
