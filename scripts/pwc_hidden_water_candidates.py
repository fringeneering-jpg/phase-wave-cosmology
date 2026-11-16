import csv, io, math, urllib.parse, urllib.request

G = 6.67430e-11
AU = 1.495978707e11
M_SUN = 1.98847e30
RHO_SUN = 1.408
RHO_EARTH = 5.514
G_EQ = 7.938e-4
BETA = 4.445
EARTH_SHEAR = (2.7302 / 1.0) ** BETA

def tap_csv(adql):
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=" + urllib.parse.quote(adql) + "&format=csv"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (PWC-Hidden-Audit)"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        return list(csv.DictReader(io.StringIO(resp.read().decode("utf-8"))))

print("=" * 118)
print("PWC HIDDEN WATER-WORLD & EXOMOON-HOST PLAUSIBILITY SCANNER (ZERO FITTED PARAMETERS)")
print("=" * 118)

# --- SCAN 1: UNCONFIRMED KEPLER CANDIDATES (KOI CUMULATIVE TABLE) ---
q_koi = ("select kepoi_name,koi_disposition,koi_period,koi_prad,koi_insol,koi_smass,koi_srad,koi_num_transits "
         "from cumulative where koi_disposition = 'CANDIDATE' and koi_prad between 0.75 and 1.45 "
         "and koi_insol between 0.35 and 1.25 and koi_smass is not null and koi_srad is not null")
kois = tap_csv(q_koi)
koi_hits = []
for r in kois:
    try:
        ms, rs = float(r["koi_smass"]), float(r["koi_srad"])
        per_d, rp, seff = float(r["koi_period"]), float(r["koi_prad"]), float(r["koi_insol"])
        ntran = r["koi_num_transits"] or "?"
        if ms <= 0 or rs <= 0 or per_d <= 0: continue
        a_au = ((ms * ((per_d / 365.256) ** 2)) ** (1.0 / 3.0))
        if a_au < 0.50: continue
        rho_st = RHO_SUN * (ms / (rs ** 3))
        rho_p = RHO_EARTH * ((rp ** 3.7) / (rp ** 3))
        f_rat = math.sqrt(rho_p / rho_st)
        r_eq = math.sqrt(G * ms * M_SUN / G_EQ) / AU
        shear_x = ((r_eq / a_au) ** BETA) / EARTH_SHEAR
        if 1.80 <= f_rat <= 2.20 and shear_x <= (250.0 / EARTH_SHEAR) and a_au < r_eq:
            # Expected Moon TTV amplitude (+/- seconds) if hosting a 1/81 mass-ratio moon at 60 R_p
            v_orb = 2.0 * math.pi * (a_au * AU) / (per_d * 86400.0)
            ttv_sec = (60.0 * rp * 6.371e6 * (1.0 / 82.0)) / v_orb
            koi_hits.append((abs(f_rat - 2.0), r["kepoi_name"], rho_st, a_au, rp, f_rat, shear_x, seff, ntran, ttv_sec))
    except ValueError:
        continue

print(f"\n[1] UNCONFIRMED KEPLER SOLAR-TWIN CANDIDATES PASSING ALL PWC GATES ({len(koi_hits)} FOUND):")
print("-" * 118)
for _, name, rst, a, rp, fr, sh, se, nt, ttv in sorted(koi_hits)[:20]:
    print(f"  {name:<14} | rho*={rst:4.2f} | a={a:5.3f} AU | R={rp:4.2f} Re | f_p/f*={fr:4.2f}x | "
          f"Shear={sh:4.2f}xE | S={se:4.2f} Se | Transits={str(nt):>3} | Pred Moon TTV=+/-{ttv:4.0f}s")

# --- SCAN 2: NON-TRANSITING RADIAL-VELOCITY WORLDS & WARM GAS-GIANT EXOMOON HOSTS ---
q_ps = ("select pl_name,discoverymethod,st_mass,st_rad,st_lum,pl_orbsmax,pl_rade,pl_bmasse,pl_bmassprov "
        "from pscomppars where pl_orbsmax >= 0.65 and st_mass is not null and st_rad is not null")
ps_rows = tap_csv(q_ps)
rv_hits, moon_hosts = [], []

for r in ps_rows:
    try:
        ms, rs, a = float(r["st_mass"]), float(r["st_rad"]), float(r["pl_orbsmax"])
        if ms <= 0 or rs <= 0: continue
        ls = (10.0 ** float(r["st_lum"])) if r["st_lum"] else (ms ** 3.5)
        seff = ls / (a ** 2)
        if not (0.35 <= seff <= 1.20): continue
        rho_st = RHO_SUN * (ms / (rs ** 3))
        r_eq = math.sqrt(G * ms * M_SUN / G_EQ) / AU
        shear_x = ((r_eq / a) ** BETA) / EARTH_SHEAR
        if shear_x > (250.0 / EARTH_SHEAR) or a >= r_eq: continue

        has_r = bool(r["pl_rade"]) and ("M-R" not in (r.get("pl_bmassprov") or ""))
        mp = float(r["pl_bmasse"]) if r["pl_bmasse"] else 0.0
        rp = float(r["pl_rade"]) if r["pl_rade"] else 0.0

        # Branch A: Non-transiting RV rocky/super-Earth candidates (no direct transit radius, Msini <= 3.5 Me)
        if r["discoverymethod"] == "Radial Velocity" and 0.5 <= mp <= 3.5:
            rp_est = mp ** (1.0 / 3.7)
            rho_p = RHO_EARTH * (mp / (rp_est ** 3))
            fr = math.sqrt(rho_p / rho_st)
            if 1.80 <= fr <= 2.20 and rp_est <= 1.45:
                rv_hits.append((abs(fr - 2.0), r["pl_name"], rho_st, a, mp, rp_est, fr, shear_x, seff))

        # Branch B: Warm Gas Giants (>30 Me) around 1.1-1.7 g/cm^3 stars -> 1.0 Re rocky moon hits 2:1 octave + built-in keel!
        if mp >= 30.0:
            fr_moon = math.sqrt(RHO_EARTH / rho_st)  # 1.0 Earth-twin moon around this giant
            if 1.80 <= fr_moon <= 2.20:
                moon_hosts.append((abs(fr_moon - 2.0), r["pl_name"], rho_st, a, mp/317.8, fr_moon, shear_x, seff))
    except ValueError:
        continue

print(f"\n[2] OVERLOOKED NON-TRANSITING RV WORLDS AROUND SOLAR TWINS ({len(rv_hits)} FOUND):")
print("-" * 118)
for _, name, rst, a, mp, rpe, fr, sh, se in sorted(rv_hits)[:15]:
    print(f"  {name:<20} | rho*={rst:4.2f} | a={a:5.3f} AU | Msini={mp:4.2f} Me (~{rpe:4.2f} Re) | "
          f"f_p/f*={fr:4.2f}x | Shear={sh:4.2f}xE | S={se:4.2f} Se")

print(f"\n[3] 'NON-CANDIDATE' WARM GAS GIANTS HOSTING 2:1-OCTAVE OCEAN-MOON ZONES ({len(moon_hosts)} FOUND):")
print("    (Giant provides automatic spin/obliquity keel; a 1.0 Re rocky moon hits the 2:1 stellar shell octave!)")
print("-" * 118)
for _, name, rst, a, mj, frm, sh, se in sorted(moon_hosts)[:20]:
    print(f"  {name:<20} | rho*={rst:4.2f} | a={a:5.3f} AU | Host={mj:5.2f} M_Jup | "
          f"Moon f/f*={frm:4.2f}x | Shear={sh:4.2f}xE | S={se:4.2f} Se")
print("=" * 118)
