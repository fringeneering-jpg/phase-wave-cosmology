# Arithmetic on Jaden's stated numbers (labeled consequences, not derivations)
# Hunch: M = L/c0^2 where "0" = medium pressure (or tension); heat escapes the medium
# when it cavitates to form knots.  Check each identity against framework constants.

c0 = 2.998e8
c0sq = c0**2
mu0 = 4e-7 * 3.141592653589793   # N/A^2 (defined)
eps0 = 1.0 / (mu0 * c0sq)
rho_max = 1.304e15
rho0 = 8.74e-27
mp = 1.6726e-27
G = 6.6743e-11

print("== Identity 1: c0^2 = 1/(mu0 eps0) = P_max/rho_max = L ==")
print(f"  1/(mu0*eps0) = {1/(mu0*eps0):.6e} m^2/s^2")
print(f"  P_max = rho_max*c0^2 = {rho_max*c0sq:.4e} Pa")
print(f"  P_max/rho_max = {rho_max*c0sq/rho_max:.6e}  == c0^2 = {c0sq:.6e}")
print(f"  L = c0^2 = {c0sq:.4e} J/kg  (specific latent heat)")

print("\n== Identity 2: tying heat m*c0^2 = P_max * V_collapsed ==")
Vp = mp / rho_max
print(f"  proton collapsed volume at rho_max: V = m_p/rho_max = {Vp:.4e} m^3")
print(f"  P_max*V = {rho_max*c0sq*Vp:.4e} J")
print(f"  m_p*c0^2 = {mp*c0sq:.4e} J   -> equal? {abs(rho_max*c0sq*Vp - mp*c0sq) < 1e-20}")

print("\n== Identity 3: tying heat spread over the knot's T7 reach = resting pressure P0 ==")
reach = 3*mp/rho0          # T7: per-proton volume, 0.57 m^3
heat_density = mp*c0sq / reach
P0 = rho0*c0sq/3.0
print(f"  T7 reach volume 3*m_p/rho0 = {reach:.4f} m^3")
print(f"  tying heat per reach volume = m_p*c0^2/(3 m_p/rho0) = {heat_density:.4e} J/m^3")
print(f"  resting pressure P0 = rho0*c0^2/3 = {P0:.4e} Pa")
print(f"  equality (exact by construction): ratio = {heat_density/P0:.10f}")

print("\n== Identity 4: the Joukowsky demand function m = dP*V/c0^2 ==")
dv = 954e3                # km/s -> m/s bow-wave speed scale
print(f"  m = rho_max*dv*V/c0 per unit V: m/V = {rho_max*dv/c0:.4e} kg/m^3")
print(f"  (i.e. pressure spike rho_max*c0*dv over c0^2)")

print("\n== Cross-check: how big is P0 next to CMB radiation pressure? ==")
a = 7.5657e-16; T = 2.7255
print(f"  P_CMB = aT^4/3 = {a*T**4/3:.3e} Pa vs P0 = {P0:.3e} Pa, ratio {P0/(a*T**4/3):.2e}")

print("\n== The freeze bookkeeping (formation heat per unit final volume) ==")
fm = 0.05/0.95
print(f"  formation-expelled heat density = rho_m*c0^2 = {fm*rho0*c0sq:.3e} J/m^3")
print(f"  = {3*fm:.4f} x P0   (3*f_matter, f_matter = 5/95)")
