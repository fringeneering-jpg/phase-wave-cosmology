import csv, io, math, urllib.parse, urllib.request

G = 6.67430e-11
AU = 1.495978707e11
M_SUN = 1.98847e30
M_EARTH = 5.97219e24
R_JUP = 7.1492e7
RHO_SUN = 1.408
RHO_EARTH = 5.514
G_EQ = 7.938e-4
BETA = 4.445
EARTH_SHEAR = (2.7302 / 1.0) ** BETA

def fetch_csv(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (PWC-Moon-Audit)"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return list(csv.DictReader(io.StringIO(resp.read().decode("utf-8", errors="replace"))))

print("=" * 124)
print("PWC FINAL SURVIVOR AUDIT: HILL-SPHERE, ECCENTRICITY & GAIA DR3 RUWE CHECK ON THE 25 OCEAN-MOON GIANT HOSTS")
print("=" * 124)

q_ps = (
    "select pl_name,hostname,ra,dec,sy_dist,sy_vmag,st_mass,st_rad,st_lum,"
    "pl_orbsmax,pl_orbeccen,pl_bmasse,pl_rade "
    "from pscomppars where pl_orbsmax >= 0.65 and pl_bmasse >= 30.0 "
    "and st_mass is not null and st_rad is not null"
)
url_ps = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=" + urllib.parse.quote(q_ps) + "&format=csv"
rows = fetch_csv(url_ps)

candidates = []
for r in rows:
    try:
        ms, rs, a = float(r["st_mass"]), float(r["st_rad"]), float(r["pl_orbsmax"])
        if ms <= 0 or rs <= 0: continue
        ls = (10.0 ** float(r["st_lum"])) if r["st_lum"] else (ms ** 3.5)
        seff = ls / (a ** 2)
        if not (0.35 <= seff <= 1.20): continue
        rho_st = RHO_SUN * (ms / (rs ** 3))
        fr_moon = math.sqrt(RHO_EARTH / rho_st)
        if not (1.80 <= fr_moon <= 2.20): continue
        r_eq = math.sqrt(G * ms * M_SUN / G_EQ) / AU
        shear_mean = ((r_eq / a) ** BETA) / EARTH_SHEAR
        if shear_mean > (250.0 / EARTH_SHEAR) or a >= r_eq: continue
        candidates.append((r, ms, rs, ls, a, seff, rho_st, fr_moon, r_eq))
    except ValueError:
        continue

print(f"[1/2] Auditing {len(candidates)} warm G-dwarf gas giants for eccentricity, periapsis shear, Hill stability & Gaia RUWE...")
print("-" * 124)
print(f"{'System':<17} | {'d(pc)':>5} | {'e':>5} | {'Moon f/f*':>9} | {'Peri Shear':>10} | {'Flux Swing':>11} | {'Stable/Roche':>12} | {'RUWE':>5} | {'Verdict'}")
print("-" * 124)

true_sanctuaries = []
for r, ms, rs, ls, a, seff, rho_st, fr_moon, r_eq in sorted(candidates, key=lambda x: abs(x[7] - 2.0)):
    name = r["pl_name"]
    dist = float(r["sy_dist"]) if r["sy_dist"] else 0.0
    ecc = float(r["pl_orbeccen"]) if r["pl_orbeccen"] else 0.0
    mp_me = float(r["pl_bmasse"])
    mp_mj = mp_me / 317.828

    # Periapsis & Apoapsis extremes!
    r_peri = a * (1.0 - ecc)
    r_aphe = a * (1.0 + ecc)
    shear_peri = ((r_eq / r_peri) ** BETA) / EARTH_SHEAR
    s_peri = ls / (r_peri ** 2)
    s_aphe = ls / (r_aphe ** 2)

    # Prograde Exomoon Hill Stability Zone (Domingos+ 2006: a_max = 0.36 * r_Hill * (1 - e_p) already in r_peri)
    r_hill_peri_m = (r_peri * AU) * ((mp_me * M_EARTH / (3.0 * ms * M_SUN)) ** (1.0 / 3.0))
    r_stable_max_m = 0.36 * r_hill_peri_m
    # Rigid/fluid Roche limit for an Earth-density rocky moon (5.514 g/cm^3) around the gas giant
    r_roche_m = 2.44 * R_JUP * (((mp_mj * 1.326) / RHO_EARTH) ** (1.0 / 3.0))
    hill_margin = r_stable_max_m / max(r_roche_m, 1.0)

    # Query VizieR Gaia DR3 mirror (avoids ESA 503 outage!) for RUWE binary check
    ruwe = None
    try:
        ra, dec = float(r["ra"]), float(r["dec"])
        q_v = (f"SELECT TOP 1 RUWE FROM \"I/355/gaiadr3\" "
               f"WHERE 1=CONTAINS(POINT('ICRS',RA_ICRS,DE_ICRS), CIRCLE('ICRS',{ra},{dec},0.003))")
        v_url = ("https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=csv&QUERY="
                 + urllib.parse.quote(q_v))
        vr = fetch_csv(v_url, timeout=20)
        if vr and vr[0].get("RUWE"):
            ruwe = float(vr[0]["RUWE"])
    except Exception:
        pass

    kills = []
    if ecc > 0.20:
        kills.append(f"ECC({ecc:.2f}>0.20 -> boil/freeze swing)")
    if shear_peri > (250.0 / EARTH_SHEAR):
        kills.append(f"PERI_SHEAR({shear_peri:.1f}xE)")
    if s_peri > 1.55 or s_aphe < 0.25:
        kills.append(f"FLUX_SWING({s_aphe:.2f}..{s_peri:.2f}Se)")
    if hill_margin < 8.0:
        kills.append(f"TIGHT_HILL({hill_margin:.1f}xRoche)")
    if ruwe is not None and ruwe > 1.40:
        kills.append(f"BINARY_RUWE({ruwe:.2f})")

    verdict = "SURVIVES (PRIME EXOMOON OASIS)" if not kills else "KILL: " + ", ".join(kills)
    if not kills:
        true_sanctuaries.append((name, dist, mp_mj, a, ecc, fr_moon, shear_peri, seff, hill_margin, ruwe))

    ruwe_s = f"{ruwe:5.2f}" if ruwe is not None else "  N/A"
    swing_s = f"{s_aphe:4.2f}-{s_peri:4.2f}Se"
    print(f"{name:<17} | {dist:5.1f} | {ecc:5.2f} | {fr_moon:8.2f}x | {shear_peri:8.2f}xE | "
          f"{swing_s:>11} | {hill_margin:10.1f}xR | {ruwe_s} | {verdict}")

print("=" * 124)
print(f"FINAL SURVIVING LOW-ECCENTRICITY OCEAN-MOON SANCTUARIES IN KNOWN SPACE: {len(true_sanctuaries)} / {len(candidates)}")
for nm, d, mj, a, ec, fm, sp, se, hm, rw in true_sanctuaries:
    print(f"  ★ {nm:<15} ({d:5.1f} pc) | {mj:4.2f} M_Jup at a={a:.3f} AU (e={ec:.2f}) | "
          f"1 Re Moon Octave={fm:.2f}x | Max Peri Shear={sp:.2f}xE | Hill Room={hm:.0f}x Roche")
print("=" * 124)
