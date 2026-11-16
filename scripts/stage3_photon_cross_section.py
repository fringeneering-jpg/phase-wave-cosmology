# stage3_photon_cross_section.py - only a thousandth of the km is the mass?
# (2026-10-18) Jaden's arithmetic: the photons weigh 1/200 of the material
# wind yet push 2000x harder (the (c0/v)^2 of the pressures) - so only
# ~a thousandth of the surface area in that cubic km can be the part with
# the mass. The check: the photon's mass-bearing cross-section = lambda^2;
# the rest of the cell is the DISPLACEMENT (the medium's own motion - the
# wave's ride, the weightless part).
import os, sys, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solar import config

F = config.load_frozen()
c0 = F["locked_constants"]["c0"]["value"]
hbar = 1.054571817e-34

L_SUN = 3.828e26
AU = 1.496e11
FLUX_1 = L_SUN / (4 * 3.14159265358979 * AU ** 2)

# the mean photon energy of the solar spectrum (~1.4 eV) and its wavelength
E_mean = 1.4 * 1.602176634e-19
lam_mean = 2 * 3.14159265358979 * hbar * c0 / E_mean

n_flux = FLUX_1 / E_mean                 # photons / (m^2 s)
n_den = n_flux / c0                      # photons / m^3
cell = n_den ** (-1.0 / 3.0)             # the spacing between photons
frac = (lam_mean ** 2) / (cell ** 2)     # the mass-bearing share of the cell

print("=" * 78)
print("ONLY A THOUSANDTH OF THE KM IS THE MASS - the check")
print("=" * 78)
print(f"the solar spectrum's mean photon: E = {E_mean/1.602e-19:.2f} eV, "
      f"lambda = {lam_mean*1e6:.2f} microns")
print(f"photon number flux at 1 AU: {n_flux:.2e} photons/(m^2 s)")
print(f"photon number density:      {n_den:.2e} photons/m^3")
print(f"the spacing between photons: {cell*1e6:.1f} microns")
print(f"the photon's own cross-section (lambda^2): {lam_mean**2:.2e} m^2")
print(f"the cell's area (spacing^2):              {cell**2:.2e} m^2")
print()
vol_frac = frac ** (3.0 / 2.0)             # lambda^3 / spacing^3
print(f"the mass-bearing AREA share = lambda^2 / spacing^2 = {frac:.2e} = "
      f"1/{1/frac:.0f}")
print(f"the mass-bearing VOLUME share = lambda^3 / spacing^3 = {vol_frac:.2e} "
      f"= 1/{1/vol_frac:.0f}")
print(f"-> the displacement occupies {100*(1-vol_frac):.4f}% of the cubic km")
print()
print("the reading: on the AREA the mass is a thousandth; on the VOLUME it")
print("is 1/70,000 - the photon's mass sits on its own lambda-cubed core, and")
print("99.9986% of the cubic km is the DISPLACEMENT: the medium's own motion")
print("carrying the wave (the weightless part). The wave is its own sieve -")
print("the same ~99.99% emptiness the framework gives matter. The mass is the")
print("core; the ride is the field. And the push still wins by (c0/v)^2")
print("because that 0.0014% arrives at max-P.")
res = {"E_mean_eV": E_mean/1.602e-19, "lam_mean_microns": lam_mean*1e6,
       "n_density": n_den, "spacing_microns": cell*1e6,
       "mass_bearing_share_area": frac, "mass_bearing_share_volume": vol_frac}
os.makedirs(config.RESULTS_DIR, exist_ok=True)
out = os.path.join(config.RESULTS_DIR, "photon_cross_section.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(res, fh, indent=1)
print()
print("result written:", out)
