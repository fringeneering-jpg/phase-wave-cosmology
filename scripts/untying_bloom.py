# untying_bloom.py - the framework's own mechanisms in the decompression (2026-10-18)
# The subatomic derivations ARE the inputs: the knot's volume is the electron's
# own (lambda_bar_C's scale), its density's the tied state's, the bloom time's
# the tau_choke's (the solar derivation's 9-hour), the medium's the local's.
# The V(t) = V0.(1+t/tau_bloom)^3 and the dual-coupling force, all framework.
import numpy as np
from scipy.integrate import quad

c0 = 2.9979e8
m_e = 9.109e-31
lam_bar = 3.8616e-13        # the electron's reduced Compton (the framework's)
rho_max = 1.304e15
tau_choke = 9.0 * 3600.0    # the solar derivation's 9-hour (the framework's)
v_star = 220e3              # the sun's galactic speed (m/s)
rho_med = 8.74e-27          # the ambient's

# the knot's own volume: the lambda_bar^3's sphere (the single wave's footprint)
V0 = (4.0/3.0) * np.pi * lam_bar**3
rho0_knot = m_e / V0
# the porosity threshold: the lattice's spacing density (the wave-gap's scale's)
rho_perm = rho_max * (1.0/19.0)**2    # the delta_gap's share's (the s^2's)

# the bloom time: the framework's own - the choke's equalization, not the fit
tau_bloom = tau_choke

def V(t): return V0 * (1.0 + t/tau_bloom)**3
def rho(t): return rho0_knot / (1.0 + t/tau_bloom)**3
def G_EM(t): return (1.0 + t/tau_bloom)**2           # the V^(2/3) grip's
def C_matter(t): return 1.0 - np.exp(-(1.0 + t/tau_bloom)**3 * rho0_knot/rho_perm)
def f_drag(t): return G_EM(t) * C_matter(t)

print("THE UNTYING'S BLOOM - the framework's own numbers:")
print(f"  the knot: V0 = {V0:.3e} m^3 (the lambda_bar's sphere), rho0 = {rho0_knot:.3e} kg/m^3")
print(f"  the porosity: rho_perm = {rho_perm:.3e} kg/m^3 (the s^2 gap's share)")
print(f"  the bloom time: tau_bloom = tau_choke = {tau_bloom/3600:.1f} h (the solar's)")
print()
# the transition's key moments
for t in [0.0, 0.1*tau_bloom, tau_bloom, 3.0*tau_bloom, 10.0*tau_bloom, 30.0*tau_bloom]:
    print(f"  t/tau = {t/tau_bloom:5.1f}: V/V0 = {V(t)/V0:9.1f}, rho = {rho(t):.3e}, "
          f"grip = {G_EM(t):7.1f}, slip = {1.0-C_matter(t):.3e}")
print()
# the peak of the drag (the heliosphere's bow's flattening)
ts = np.logspace(-6, 2, 500) * tau_bloom
fs = f_drag(ts)
i_peak = np.argmax(fs)
print(f"  THE DRAG'S PEAK: t = {ts[i_peak]/tau_bloom:.3f} x tau_bloom "
      f"(= {ts[i_peak]/3600:.1f} h), the force {fs[i_peak]:.2f} x G0")
print()
# the total momentum transfer per knot (the closed form's)
G0 = 1.0
I, err = quad(lambda t: f_drag(t), 0, np.inf, limit=200)
print(f"  THE TOTAL MOMENTUM TRANSFER: integral f_drag dt = {I:.3f} x G0.tau_bloom")
print(f"  (per electron knot, the particle-to-wave ticket's full price's)")
