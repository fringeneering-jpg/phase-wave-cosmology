# Derivation attempt 2: the +10.1% Sigma residual (2026-10-08, Jaden's "hunt it down")
import math
G = 6.6743e-11
rho_max = 1.304e15
rho_core = 2.3e17
a_max = 3.23e11
c0 = 2.99792458e8
Msun = 1.989e30
k = 0.868899

print("== 1. The fitted column, recomputed precisely ==")
# Sigma = M_med / (4 pi R_c^2), M_med = k * C^(2/3) Msun, R_c = (3 C Msun /(4 pi rho_core))^(1/3)
Sigma_k = k*Msun**(1/3)*(4*math.pi*rho_core/3.0)**(2/3)/(4*math.pi)
print(f"Sigma_k = {Sigma_k:.6e} kg/m^2   (OPEN_WORK: 8.48e20)")

print("\n== 2. Candidate laws ==")
cands = [
    ("sheet 2 pi G S = a_max", a_max/(2*math.pi*G)),
    ("sheet, a_hold(rho_max) = c0 sqrt(4 pi G rho_max)", c0*math.sqrt(4*math.pi*G*rho_max)/(2*math.pi*G)),
    ("ball (4pi/3) G rho R = a_max at rho_max", 3*a_max/(4*math.pi*G)),
    ("(11/10) sheet", 11*a_max/(20*math.pi*G)),
    ("(11/15) ball", 11*a_max/(20*math.pi*G)),
]
for lab, S in cands:
    print(f"  {lab:44s}: {S:.6e}   ratio to fitted: {S/Sigma_k:.5f}")

print("\n== 3. Near-miss ratios (mechanism required - the framework rule) ==")
r_sheet = Sigma_k/(a_max/(2*math.pi*G))
r_ball = Sigma_k/(3*a_max/(4*math.pi*G))
print(f"Sigma_k / sheet = {r_sheet:.5f} ;  11/10 = 1.1  (dev {100*(r_sheet/1.1-1):+.3f}%)")
print(f"Sigma_k / ball  = {r_ball:.5f} ;  11/15 = 0.73333  (dev {100*(r_ball/(11/15)-1):+.3f}%)")
g = 16*math.pi**3*(1/137.036)/3.0
print(f"sqrt(g) = sqrt(16 pi^3 alpha/3) = {math.sqrt(g):.5f}  (dev from r_sheet: "
      f"{100*(r_sheet/math.sqrt(g)-1):+.3f}%)")
print(f"1.053^2 = {(20/19.0)**2:.4f} (dev {100*(r_sheet/(20/19.0)**2-1):+.3f}%)")

print("\n== 4. Verdict ==")
print("Two clean-looking forms ((11/10) sheet and (11/15) ball, identical by 3/2 geometry)")
print("match the fitted column to +0.09% but carry NO mechanism yet; sqrt(g) is 0.23% away.")
print("Per the framework's own rule (near-misses without mechanism are reported, not claimed),")
print("the residual is NOT closed. What a mechanism would need: the skin's self-pull is not")
print("2 pi G S (the infinite sheet) but the sheet's pull averaged over the skin's own")
print("thickness with the 1/r^2 dilution to the core's surface - or the 11/15 as the sheet")
print("fraction of the ball column in the thin-skin limit.")
