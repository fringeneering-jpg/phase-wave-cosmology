# stage3_particle_wave_decompression.py - the particle-to-wave transition (2026-10-18)
# The pasted derivation, checked and extended to ALL the derived knots
# (electron, proton, neutron). Three catches found on the careful read:
#   FIX 1 (transcription): Q_fric ~ A_EM ~ V^(2/3) must GROW with V; the
#     pasted (V0/V)^(2/3) is inverted. With V^(2/3):
#       dV/dt = (gamma eta rho_med v^2) V^(2/3) -> V = V0 (1+t/tau)^3,
#       tau_bloom = 3 V0^(1/3)/(gamma eta rho_med v^2) - the pasted tau and
#       the (1+t/tau)^3 ARE this corrected branch's results.
#   FIX 2 (the coupling): C_matter = 1 - exp(-(rho0/rho_perm)/(1+t/tau)^3)
#     falls as (rho0/rho_perm) (1+t/tau)^-3 - a POWER law - the intended
#     shape (their asymptote matches this, not exp(-rho_perm/rho)).
#   CATCH 3 (the divergence): with that power-law tail the drag falls only
#     as (1+t/tau)^-1 -> INTEGRAL OF f_drag DIVERGES logarithmically: the
#     total momentum transfer per knot is NOT finite. The exponential
#     cutoff C = exp(-(rho_perm/rho0)(1+t/tau)^3) closes it (super-
#     exponential collapse). Reported, not hidden.
import os, sys, json
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
rho_max = F["locked_constants"]["rho_max"]["value"]
rho0 = F["locked_constants"]["rho0"]["value"]

M_E = 9.1093837e-31
M_P = 1.6726219e-27
M_N = 1.6749275e-27
RHO_PERM = 1.0e3          # the atomic lattice's porosity threshold (named)
V0 = {"electron": M_E / rho_max, "proton": M_P / rho_max, "neutron": M_N / rho_max}

# the ISM drive (the Sun's motion): rho_med ~ 1e-21, v ~ 240 km/s
RHO_MED, V_STAR = 1.0e-21, 2.4e5
# the shape driver (gamma eta = 1 for the normalized shape; the physical
# eta is the open knob - see the report)
DRIVE = RHO_MED * V_STAR ** 2

print("=" * 78)
print("THE PARTICLE-TO-WAVE DECOMPRESSION - all three derived knots")
print("=" * 78)
print(f"xi(t) = 1 - V0/V(t): 0 = the localized knot, 1 = the pure wave")
print(f"V(t) = V0 (1 + t/tau_bloom)^3,  rho(t) = rho0/(1+t/tau)^3")
print()
print(f"{'knot':10s} {'V0 (m^3)':>12s} {'tau_bloom (s)':>14s} "
      f"{'peak t/tau':>10s} {'tail slope':>11s} {'int f dt':>10s}")
rows = []
for name in ("electron", "proton", "neutron"):
    V0k = V0[name]
    tau = 3.0 * V0k ** (1.0 / 3.0) / DRIVE      # gamma eta = 1 (the shape)
    # the force curve: G0 (1+s)^2 [1 - exp(-A/(1+s)^3)], A = rho0/rho_perm
    A = (V0k and 0) or None
    rho0k = {"electron": M_E, "proton": M_P, "neutron": M_N}[name] / V0k  # = rho_max
    A = rho0k / RHO_PERM
    s = np.logspace(-4, 6, 2001)
    f = (1 + s) ** 2 * (1 - np.exp(-A / (1 + s) ** 3))
    ipeak = int(np.argmax(f))
    tail = np.gradient(np.log(np.maximum(f[1600:], 1e-60)), np.log(s[1600:]))[-1]
    # the divergence: int_1^inf u^2 [1-exp(-A/u^3)] du ~ int A/u du -> ln
    rows.append({"knot": name, "V0": V0k, "tau_s": tau, "A": A,
                 "peak_stau": s[ipeak], "tail_slope": float(tail),
                 "integral": "DIVERGES (~ ln)"})
    print(f"{name:10s} {V0k:12.2e} {tau:14.3e} {s[ipeak]:10.2f} "
          f"{tail:+11.2f}  DIVERGES (~ln)")
print()
print("the window (the overlap span - where the grip AND the coupling are")
print("BOTH significant; outside it one of the two is negligible):")
for name in ("electron", "proton", "neutron"):
    V0k = V0[name]
    tau = 3.0 * V0k ** (1.0 / 3.0) / DRIVE
    rho0k = {"electron": M_E, "proton": M_P, "neutron": M_N}[name] / V0k
    A = rho0k / RHO_PERM
    s = np.logspace(-4, 7, 4001)
    f = (1 + s) ** 2 * (1 - np.exp(-A / (1 + s) ** 3))
    ipeak = int(np.argmax(f))
    half = f[ipeak] / 2.0
    lo = s[:ipeak][int(np.argmin(np.abs(f[:ipeak] - half)))]
    hi = s[ipeak:][int(np.argmin(np.abs(f[ipeak:] - half)))]
    fwhm = hi - lo
    print(f"  {name:10s}: peak at s ~ {A**(1/3):,.0f} (= A^(1/3)), FWHM "
          f"[{lo:,.0f} .. {hi:,.0f}] = {fwhm:,.0f} tau = {fwhm*tau:.2e} s")
print(f"  -> THE WINDOW IS THE PHASE CHANGE - and there are NO ZEROS:")
print(f"  the EM wave COMPRESSES into the particle: the footprint shrinks, the")
print(f"  density spikes, it SEEMS solid - but the field is still there, tiny")
print(f"  but nonzero (that tiny footprint IS the charge). Before the window")
print(f"  the grip is small - not zero; after the window the coupling is")
print(f"  small - not zero. The window is where BOTH are significant, not")
print(f"  where they exist. Compression does not delete the field; it squeezes")
print(f"  it - the same wave, the same charge, a smaller footprint.")
print()
print("the sides (the lateral deflection - the share that pulls sideways):")
s = np.logspace(-4, 7, 4001)
for name in ("electron", "proton", "neutron"):
    rho0k = {"electron": M_E, "proton": M_P, "neutron": M_N}[name] / V0[name]
    A = rho0k / RHO_PERM
    f_fwd = (1 + s) ** 2 * (1 - np.exp(-A / (1 + s) ** 3))
    f_lat = (1 + s) ** 2 * np.exp(-A / (1 + s) ** 3)
    tot = f_fwd + f_lat
    lat_share = f_lat / tot
    print(f"  {name:10s}: forward peaks at s~{A**(1/3):,.0f}; lateral share at the")
    print(f"            peak = {lat_share[int(np.argmax(f_fwd))]*100:.1f}% of the grip;")
    print(f"            late (s = 1e6): {lat_share[-1]*100:.4f}% - the diluted wave")
    print(f"            flows AROUND the atoms: the sides take over (the slip,")
    print(f"            with a residual forward share that never reaches zero)")
print(f"  the honest note: the lateral share is the grip's complement DURING the")
print(f"  transition; after it the wave is mostly sides - the slip around the")
print(f"  atoms - with a residual forward coupling that never reaches zero.")
print(f"  The teardrop tail is the phase change's late remnant.")
print()
print("the compression (the same field, squeezed - the charge is the field):")
LAM_C = 2.426e-12                       # the electron's Compton wavelength
V_WAVE = LAM_C ** 3                     # the wave's extent at the Compton scale
V_KNOT = M_E / rho_max                  # the knot's volume at the ceiling
print(f"  the wave's footprint: lambda^2 = {(LAM_C**2):.2e} m^2")
print(f"  the knot's footprint: R_p^2    = {(0.84e-15)**2:.2e} m^2")
print(f"  -> the compression shrinks the footprint {(LAM_C/0.84e-15)**2:.1e}x")
print(f"  the density: rho_max/rho0 = {rho_max/rho0:.1e}x - the same field at")
print(f"  ~1e41x the density: that is what 'seems solid'. And the charge?")
print(f"  THE CHARGE IS THE COMPRESSED FIELD ITSELF - it never goes to zero,")
print(f"  it just lives at the tiny footprint. Compression keeps the wave;")
print(f"  solidity is the density, not a new substance.")
print()
print("the catches (kept):")
print(f"  - the proton blooms {(V0['proton']/V0['electron'])**(1/3):.1f}x SLOWER")
print(f"    (tau ~ V0^(1/3) ~ m^(1/3)); its window is 12.2x longer in seconds")
print(f"  - the forward tail ~ (1+s)^-1: the pure-power-law integral diverges")
print(f"    logarithmically; the exponential cutoff (the super-exponential")
print(f"    collapse) closes it - still open, now bounded by the window")
print(f"  - tau's normalization: eta ~ 1e-11 needed for the heliospheric scale")
print(f"    (the friction ladder's own mu) - the SHAPE is exact, the knob named")
res = rows
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "particle_wave_decompression.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
