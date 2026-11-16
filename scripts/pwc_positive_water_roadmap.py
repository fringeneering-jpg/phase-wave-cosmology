import csv, io, math, urllib.parse, urllib.request

G = 6.67430e-11
AU = 1.495978707e11
M_SUN = 1.98847e30
RHO_SUN = 1.408
RHO_EARTH = 5.514
G_EQ = 7.938e-4
BETA = 4.445
EARTH_SHEAR = (2.7302 / 1.0) ** BETA

def fetch_csv(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (PWC-Target-Roadmap)"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return list(csv.DictReader(io.StringIO(resp.read().decode("utf-8", errors="replace"))))

print("=" * 124)
print("PWC POSITIVE WATER-WORLD ROADMAP: F6V-K2V SOLAR NEIGHBORHOOD TARGETS (< 30 PARSECS) & CIRCULAR EXOMOON OASES")
print("=" * 124)

# 1. Query nearby planet-hosting F6-K2 stars (< 35 pc) whose stellar density sits in the 0.85 - 2.05 g/cm^3 2:1 Octave Window!
q_stars = (
    "select distinct hostname,sy_dist,sy_vmag,st_spectype,st_teff,st_mass,st_rad,st_lum "
    "from pscomppars where sy_dist <= 35.0 and st_teff between 4900 and 6350 "
    "and st_mass is not null and st_rad is not null"
)
url_s = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=" + urllib.parse.quote(q_stars) + "&format=csv"
stars = fetch_csv(url_s)

prime_hosts = []
for s in stars:
    try:
        ms, rs = float(s["st_mass"]), float(s["st_rad"])
        dist = float(s["sy_dist"])
        vmag = float(s["sy_vmag"]) if s["sy_vmag"] else 99.0
        teff = float(s["st_teff"])
        ls = (10.0 ** float(s["st_lum"])) if s["st_lum"] else (ms ** 3.5)
        rho_st = RHO_SUN * (ms / (rs ** 3))
        # Required rocky planet bulk density for exact 2:1 shell octave (f_p / f_* = 2.0 -> rho_p = 4 * rho_*)
        req_rho_p = 4.0 * rho_st
        # Physically achievable iron/silicate rocky planet density band: 3.8 g/cm^3 (Mars-like silicate) to 7.8 g/cm^3 (Fe-rich super-Earth)
        if 3.80 <= req_rho_p <= 7.80:
            a_1se = math.sqrt(ls)  # Exact 1.00 S_earth orbital groove
            r_eq = math.sqrt(G * ms * M_SUN / G_EQ) / AU
            shear_1se = ((r_eq / a_1se) ** BETA) / EARTH_SHEAR
            if shear_1se <= 2.50 and a_1se < r_eq:
                # Reflex RV amplitude K (cm/s) of a 1.0 M_earth planet at a_1se
                v_kepl = math.sqrt(G * ms * M_SUN / (a_1se * AU))
                k_cms = (5.972e24 / (ms * M_SUN)) * v_kepl * 100.0
                prime_hosts.append((dist, s["hostname"], s.get("st_spectype") or f"{teff:.0f}K",
                                    vmag, rho_st, req_rho_p, a_1se, r_eq, shear_1se, k_cms))
    except ValueError:
        continue

print(f"\n[1] NEARBY KNOWN PLANET-HOSTING F/G/EARLY-K STARS WITH OPEN 2:1 WATER GROOVES ({len(prime_hosts)} WITHIN 35 PC):")
print("    (Prime targets for ESPRESSO / HARPS-3 / HWO direct imaging — sorted by distance from Earth!)")
print("-" * 124)
print(f"{'Host Star':<16} | {'Dist':>6} | {'SpType':<9} | {'Vmag':>4} | {'rho*':>5} | {'Req rho_p (2:1)':>15} | {'1 Se Groove':>11} | {'Frost R_eq':>10} | {'Shear':>6} | {'1Me RV'}")
print("-" * 124)
for dist, hname, sp, vm, rst, rqp, a1, req, sh, kcm in sorted(prime_hosts)[:22]:
    print(f"{hname:<16} | {dist:4.1f}pc | {sp[:9]:<9} | {vm:4.1f} | {rst:5.2f} | {rqp:10.2f} g/cc | "
          f"{a1:8.3f} AU | {req:7.2f} AU | {sh:5.2f}x | {kcm:4.1f}cm/s")

# 2. Check ALL confirmed planets (including newly confirmed HD 20794 d & low-eccentricity Exomoon Giants) in those grooves!
q_pl = (
    "select pl_name,hostname,sy_dist,st_teff,st_mass,st_rad,st_lum,pl_orbsmax,pl_orbeccen,pl_bmasse,pl_rade "
    "from pscomppars where pl_orbsmax >= 0.60 and st_teff between 4900 and 6350 "
    "and st_mass is not null and st_rad is not null"
)
pl_rows = fetch_csv(q_pl)
rocky_near, circular_giants = [], []

for r in pl_rows:
    try:
        ms, rs, a = float(r["st_mass"]), float(r["st_rad"]), float(r["pl_orbsmax"])
        ecc = float(r["pl_orbeccen"]) if r["pl_orbeccen"] else 0.0
        ls = (10.0 ** float(r["st_lum"])) if r["st_lum"] else (ms ** 3.5)
        seff = ls / (a ** 2)
        if not (0.30 <= seff <= 1.35): continue
        rho_st = RHO_SUN * (ms / (rs ** 3))
        r_eq = math.sqrt(G * ms * M_SUN / G_EQ) / AU
        r_peri = a * (1.0 - ecc)
        shear_peri = ((r_eq / r_peri) ** BETA) / EARTH_SHEAR
        mp = float(r["pl_bmasse"]) if r["pl_bmasse"] else 0.0
        dist = float(r["sy_dist"]) if r["sy_dist"] else 999.0

        # Super-Earths / Rocky RV candidates (1 - 7 M_earth) in F/G/K grooves
        if 0.8 <= mp <= 7.0 and 0.85 <= rho_st <= 2.05:
            rocky_near.append((dist, r["pl_name"], rho_st, a, ecc, mp, seff, shear_peri))
        # Low-eccentricity (e <= 0.18) Gas Giants hosting calm 2:1 Ocean-Moon sanctuaries
        elif mp >= 30.0 and ecc <= 0.18 and 1.15 <= rho_st <= 1.75 and shear_peri <= 2.8:
            fr_m = math.sqrt(RHO_EARTH / rho_st)
            circular_giants.append((dist, r["pl_name"], rho_st, a, ecc, mp/317.83, fr_m, seff, shear_peri))
    except ValueError:
        continue

print(f"\n[2] CONFIRMED F/G/EARLY-K SUPER-EARTHS IN OR NEAR THE GROOVE ({len(rocky_near)} FOUND):")
print("-" * 124)
for dist, nm, rst, a, ec, mp, se, sp in sorted(rocky_near)[:10]:
    print(f"  {nm:<18} ({dist:5.1f} pc) | rho*={rst:4.2f} g/cc | a={a:5.3f} AU (e={ec:.2f}) | M={mp:4.2f} Me | S={se:4.2f} Se | PeriShear={sp:5.2f}xE")

print(f"\n[3] CALM LOW-ECCENTRICITY (e <= 0.18) GAS GIANTS HOSTING PRIME 2:1 OCEAN-MOON SANCTUARIES ({len(circular_giants)} FOUND):")
print("-" * 124)
for dist, nm, rst, a, ec, mj, fm, se, sp in sorted(circular_giants)[:15]:
    print(f"  ★ {nm:<16} ({dist:5.1f} pc) | rho*={rst:4.2f} g/cc | a={a:5.3f} AU (e={ec:.2f}) | {mj:4.2f} M_Jup | 1Re Moon={fm:4.2f}x | S={se:4.2f} Se | PeriShear={sp:4.2f}xE")
print("=" * 124)
