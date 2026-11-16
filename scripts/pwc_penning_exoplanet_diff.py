import csv, io, math, urllib.parse, urllib.request

RHO_SUN, RHO_EARTH = 1.408, 5.514
PEN_STAR, PEN_ROCK = -0.00088, -0.00733  # Section 6.1: H/He star (-0.088%) vs Fe/Si rock (-0.733%)
SCALE_OCTAVE = math.sqrt((1.0 / (1.0 + PEN_ROCK)) / (1.0 / (1.0 + PEN_STAR)))  # 1.003243 (+0.324%)

q = ("select pl_name,sy_dist,st_mass,st_rad,st_lum,pl_orbsmax,pl_orbeccen,pl_bmasse "
     "from pscomppars where pl_orbsmax >= 0.55 and pl_bmasse >= 30.0 and st_mass is not null and st_rad is not null")
url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=" + urllib.parse.quote(q) + "&format=csv"
rows = list(csv.DictReader(io.StringIO(urllib.request.urlopen(url, timeout=60).read().decode("utf-8"))))

print(f"Penning-to-True Wave Inventory Octave Multiplier: x{SCALE_OCTAVE:.6f} (+{(SCALE_OCTAVE-1)*100:.3f}%)")
flips = 0
for r in rows:
    ms, rs, a = float(r["st_mass"]), float(r["st_rad"]), float(r["pl_orbsmax"])
    ecc = float(r["pl_orbeccen"]) if r["pl_orbeccen"] else 0.0
    ls = (10.0 ** float(r["st_lum"])) if r["st_lum"] else (ms ** 3.5)
    if ms <= 0 or rs <= 0 or ecc > 0.20: continue
    s_peri, s_aphe = ls / ((a*(1-ecc))**2), ls / ((a*(1+ecc))**2)
    if s_peri > 1.55 or s_aphe < 0.25: continue
    rho_st = RHO_SUN * (ms / (rs ** 3))
    f_raw = math.sqrt(RHO_EARTH / rho_st)
    f_true = f_raw * SCALE_OCTAVE
    in_raw = (1.80 <= f_raw <= 2.20)
    in_true = (1.80 <= f_true <= 2.20)
    if in_raw != in_true:
        flips += 1
        print(f"  [BOUNDARY FLIP] {r['pl_name']:<16} | Raw Octave={f_raw:.4f}x ({in_raw}) -> True Octave={f_true:.4f}x ({in_true})")
print(f"Total boundary flips across entire NASA catalog: {flips}")
