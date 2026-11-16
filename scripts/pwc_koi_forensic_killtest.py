import csv, io, json, math, urllib.parse, urllib.request

G = 6.67430e-11
AU = 1.495978707e11
M_SUN = 1.98847e30
RHO_SUN = 1.408
RHO_EARTH = 5.514
G_EQ = 7.938e-4
BETA = 4.445
EARTH_SHEAR = (2.7302 / 1.0) ** BETA

TARGETS = ["K08272.01", "K05737.01", "K06108.01", "K07953.01", "K04878.01"]

def fetch_csv(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (PWC-Forensic-Audit)"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return list(csv.DictReader(io.StringIO(resp.read().decode("utf-8", errors="replace"))))

def fval(row, key, default=None):
    v = row.get(key)
    if v is None or str(v).strip() == "":
        return default
    try:
        return float(v)
    except ValueError:
        return default

print("=" * 122)
print("PWC 3-DATASET FORENSIC FALSIFIER: GAIA DR3 + PIXEL CENTROID SHIFT + 3RD-TRANSIT O-C AUDIT")
print("Targets: K08272.01, K05737.01, K06108.01, K07953.01 (+ K04878.01 Control)")
print("=" * 122)

# -------------------------------------------------------------------------
# 1. NASA EXOPLANET ARCHIVE: DR25 PIXEL CENTROIDS, ROBOVETTER & TRANSIT RHO
# -------------------------------------------------------------------------
in_list = ",".join(f"'{t}'" for t in TARGETS)
q_nasa = (
    "select kepoi_name,kepid,ra,dec,koi_disposition,koi_pdisposition,koi_score,"
    "koi_fpflag_nt,koi_fpflag_ss,koi_fpflag_co,koi_fpflag_ec,"
    "koi_period,koi_period_err1,koi_time0bk,koi_time0bk_err1,koi_duration,koi_depth,"
    "koi_prad,koi_insol,koi_model_snr,koi_num_transits,koi_tce_plnt_num,"
    "koi_smass,koi_srad,koi_steff,koi_srho,koi_srho_err1,koi_srho_err2,"
    "koi_dicco_msky,koi_dicco_msky_err,koi_dikco_msky,koi_dikco_msky_err "
    f"from cumulative where kepoi_name in ({in_list})"
)
nasa_url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=" + urllib.parse.quote(q_nasa) + "&format=csv"
print("[1/3] Querying NASA Exoplanet Archive (DR25 Pixel Centroids, Robovetter Score & Transit Density)...")
nasa_rows = {r["kepoi_name"]: r for r in fetch_csv(nasa_url)}

# -------------------------------------------------------------------------
# 2. ESA GAIA DR3 LIVE TAP CROSS-MATCH (PARALLAX, RUWE, FLAME RADIUS & MASS)
# -------------------------------------------------------------------------
print("[2/3] Querying ESA Gaia DR3 TAP Server (RUWE Binary Check + FLAME Stellar Radius/Mass/Luminosity)...")
gaia_data = {}
for koi in TARGETS:
    r = nasa_rows.get(koi)
    if not r:
        continue
    ra, dec = float(r["ra"]), float(r["dec"])
    q_gaia = (
        "SELECT TOP 3 gs.source_id, gs.phot_g_mean_mag, gs.parallax, gs.ruwe, gs.teff_gspphot, gs.radius_gspphot, "
        "ap.radius_flame, ap.mass_flame, ap.lum_flame, "
        f"DISTANCE(POINT('ICRS', gs.ra, gs.dec), POINT('ICRS', {ra}, {dec}))*3600.0 AS sep_arcsec "
        "FROM gaiadr3.gaia_source AS gs "
        "LEFT JOIN gaiadr3.astrophysical_parameters AS ap ON gs.source_id = ap.source_id "
        f"WHERE 1=CONTAINS(POINT('ICRS', gs.ra, gs.dec), CIRCLE('ICRS', {ra}, {dec}, 0.0020)) "
        "ORDER BY sep_arcsec ASC"
    )
    g_url = ("https://gea.esac.esa.int/tap-server/tap/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=csv&QUERY="
             + urllib.parse.quote(q_gaia))
    try:
        g_rows = fetch_csv(g_url, timeout=45)
        gaia_data[koi] = g_rows
    except Exception as e:
        print(f"  [WARN] Gaia TAP query issue on {koi}: {e}")
        gaia_data[koi] = []

# -------------------------------------------------------------------------
# 3. VIZIER HOLCZER+ (2016) & INDIVIDUAL TRANSIT O-C / MAST TIMING AUDIT
# -------------------------------------------------------------------------
print("[3/3] Querying VizieR Transit Timing Catalog (Holczer+ J/ApJS/225/9) & 3-Transit O-C Curvature...")
ttv_data = {}
for koi in TARGETS:
    num_part = koi.replace("K", "").lstrip("0")  # e.g. 8272.01
    koi_num_int = int(float(num_part))
    # Query Holczer+ 2016 table of individual transit times (table3) if present
    q_viz = f"SELECT * FROM \"J/ApJS/225/9/table3\" WHERE KOI={koi_num_int}"
    v_url = ("http://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=csv&QUERY="
             + urllib.parse.quote(q_viz))
    try:
        v_rows = fetch_csv(v_url, timeout=30)
        ttv_data[koi] = v_rows
    except Exception:
        ttv_data[koi] = []

# Optional: if lightkurve is installed locally, measure direct 3-transit O-C from raw MAST Kepler PDC-SAP flux!
raw_oc_results = {}
try:
    import lightkurve as lk
    import numpy as np
    print("[BONUS] lightkurve detected! Extracting exact per-transit O-C directly from MAST Kepler PDC-SAP flux...")
    for koi in TARGETS:
        r = nasa_rows.get(koi)
        if not r: continue
        kepid = int(r["kepid"])
        per = fval(r, "koi_period")
        t0 = fval(r, "koi_time0bk")
        dur_d = fval(r, "koi_duration", 6.0) / 24.0
        sr = lk.search_lightcurve(f"KIC {kepid}", author="Kepler", cadence="long")
        if len(sr) == 0: continue
        lc = sr.download_all().stitch().remove_nans().flatten(window_length=901)
        t_arr, f_arr = lc.time.value, lc.flux.value
        n_min = int(math.ceil((np.min(t_arr) - t0) / per))
        n_max = int(math.floor((np.max(t_arr) - t0) / per))
        measured_times = []
        for n in range(n_min, n_max + 1):
            t_exp = t0 + n * per
            mask = np.abs(t_arr - t_exp) < (1.5 * dur_d)
            in_tr = np.abs(t_arr - t_exp) < (0.55 * dur_d)
            if np.sum(in_tr) >= 3:
                # Flux-deficit weighted transit mid-time + local depth SNR
                deficit = np.maximum(0.0, 1.0 - f_arr[mask])
                if np.sum(deficit) > 0:
                    t_meas = float(np.sum(t_arr[mask] * deficit) / np.sum(deficit))
                    dip_ppm = float((1.0 - np.mean(f_arr[in_tr])) * 1e6)
                    oc_min = (t_meas - t_exp) * 1440.0
                    measured_times.append((n, t_exp, t_meas, oc_min, dip_ppm))
        raw_oc_results[koi] = measured_times
except ImportError:
    print("  (Note: Python 'lightkurve' package not installed; using catalog ephemeris/VizieR timing. "
          "Run 'pip install lightkurve' if you want raw MAST pixel/flux O-C extraction!)")
except Exception as e:
    print(f"  [WARN] MAST lightcurve pull skipped: {e}")

# -------------------------------------------------------------------------
# 4. MASTER FORENSIC VERDICT PER CANDIDATE
# -------------------------------------------------------------------------
print("\n" + "=" * 122)
print("DETAILED FORENSIC DOSSIER & SURVIVAL VERDICT PER CANDIDATE")
print("=" * 122)

survivors_final = []

for koi in TARGETS:
    r = nasa_rows.get(koi)
    if not r:
        print(f"\n[{koi}] NOT FOUND IN CUMULATIVE TABLE")
        continue

    kepid = r["kepid"]
    per = fval(r, "koi_period", 0.0)
    per_err_min = fval(r, "koi_period_err1", 0.0) * 1440.0
    t0_err_min = fval(r, "koi_time0bk_err1", 0.0) * 1440.0
    rp_kep = fval(r, "koi_prad", 0.0)
    ms_kep = fval(r, "koi_smass", 1.0)
    rs_kep = fval(r, "koi_srad", 1.0)
    seff_kep = fval(r, "koi_insol", 0.0)
    snr = fval(r, "koi_model_snr", 0.0)
    score = fval(r, "koi_score", -1.0)
    ntran = r.get("koi_num_transits") or "?"
    srho_tr = fval(r, "koi_srho")

    # Flags & Pixel Centroids
    fp_nt = int(fval(r, "koi_fpflag_nt", 0))
    fp_ss = int(fval(r, "koi_fpflag_ss", 0))
    fp_co = int(fval(r, "koi_fpflag_co", 0))
    fp_ec = int(fval(r, "koi_fpflag_ec", 0))

    dicco = fval(r, "koi_dicco_msky")
    dicco_e = fval(r, "koi_dicco_msky_err")
    dikco = fval(r, "koi_dikco_msky")
    dikco_e = fval(r, "koi_dikco_msky_err")
    sig_dicco = (dicco / dicco_e) if (dicco is not None and dicco_e and dicco_e > 0) else None
    sig_dikco = (dikco / dikco_e) if (dikco is not None and dikco_e and dikco_e > 0) else None

    # Gaia DR3 Re-Evaluation
    g_list = gaia_data.get(koi, [])
    g_primary = g_list[0] if g_list else {}
    n_Execution_neighbors = len(g_list) - 1 if len(g_list) > 1 else 0
    ruwe = fval(g_primary, "ruwe")
    rs_gaia = fval(g_primary, "radius_flame") or fval(g_primary, "radius_gspphot") or rs_kep
    ms_gaia = fval(g_primary, "mass_flame") or ms_kep
    lum_gaia = fval(g_primary, "lum_flame")

    # Recompute PWC Metrics with Gaia DR3 Corrected Radius & Mass!
    rp_gaia = rp_kep * (rs_gaia / rs_kep)
    a_gaia = (ms_gaia * ((per / 365.256) ** 2)) ** (1.0 / 3.0)
    l_used = lum_gaia if lum_gaia else (seff_kep * ((ms_kep * ((per / 365.256) ** 2)) ** (2.0 / 3.0)))
    seff_gaia = l_used / (a_gaia ** 2)

    rho_st_gaia = RHO_SUN * (ms_gaia / (rs_gaia ** 3))
    mp_gaia_est = rp_gaia ** 3.7
    rho_p_gaia = RHO_EARTH * (mp_gaia_est / (rp_gaia ** 3))
    f_ratio_gaia = math.sqrt(rho_p_gaia / rho_st_gaia)
    r_eq_gaia = math.sqrt(G * ms_gaia * M_SUN / G_EQ) / AU
    shear_gaia = ((r_eq_gaia / a_gaia) ** BETA) / EARTH_SHEAR

    # Evaluate Kill Conditions
    kills = []
    warnings = []

    if any([fp_nt, fp_ss, fp_co, fp_ec]):
        kills.append(f"NASA_FP_FLAG(NT={fp_nt},SS={fp_ss},CO={fp_co},EC={fp_ec})")
    if score >= 0 and score < 0.50:
        kills.append(f"LOW_ROBOVETTER_SCORE({score:.3f}<0.50 -> likely rolling-band/syst ghost)")
    elif score >= 0 and score < 0.80:
        warnings.append(f"MODEST_ROBOVETTER_SCORE({score:.3f})")
    if snr > 0 and snr < 7.1:
        kills.append(f"SUB_THRESHOLD_SNR({snr:.1f}<7.1)")
    elif snr < 10.0:
        warnings.append(f"LOW_SNR({snr:.1f})")

    # Centroid Kills
    if sig_dicco is not None and sig_dicco > 3.0:
        kills.append(f"CENTROID_OOT_SHIFT({dicco:.3f}\", {sig_dicco:.1f}sigma > 3s -> Background Blend!)")
    if sig_dikco is not None and sig_dikco > 3.5:
        warnings.append(f"CENTROID_KIC_OFFSET({dikco:.3f}\", {sig_dikco:.1f}sigma)")

    # Gaia DR3 Kills
    if ruwe is not None and ruwe > 1.40:
        kills.append(f"GAIA_BINARY_RUWE({ruwe:.2f}>1.40 -> Unresolved Stellar Companion!)")
    if n_Execution_neighbors > 0:
        warnings.append(f"CROWDED_APERTURE({n_Execution_neighbors} extra Gaia star(s) within 7.2\" Kepler pixel!)")
    if rp_gaia > 1.45 or rp_gaia < 0.75:
        kills.append(f"GAIA_RADIUS_BLOWUP(R_p={rp_gaia:.2f} Re vs {rp_kep:.2f} Re -> Mini-Neptune Gas Envelope!)")
    if not (1.80 <= f_ratio_gaia <= 2.20):
        kills.append(f"GAIA_OCTAVE_FAIL(f_p/f*={f_ratio_gaia:.2f}x outside [1.80, 2.20] at rho*={rho_st_gaia:.2f} g/cm^3)")
    if not (0.32 <= seff_gaia <= 1.20):
        kills.append(f"GAIA_FLUX_FAIL(S_eff={seff_gaia:.2f} Se outside [0.32, 1.20])")

    # Transit Chord Density Ratio (Photo-eccentric check)
    rho_ratio_tr = (srho_tr / rho_st_gaia) if (srho_tr and rho_st_gaia > 0) else None
    if rho_ratio_tr is not None and (rho_ratio_tr < 0.25 or rho_ratio_tr > 4.0):
        warnings.append(f"TRANSIT_DENSITY_MISMATCH(rho_trans/rho_Gaia={rho_ratio_tr:.2f} -> high eccentricity or blend)")

    verdict = "SURVIVES ALL FORENSIC GATES" if not kills else "FALSIFIED / KILLED"
    if not kills:
        survivors_final.append(koi)

    print(f"\n>>> {koi} (KIC {kepid}) | Period = {per:.3f} d | Transits = {ntran} | SNR = {snr:.1f} | Robovetter Score = {score if score>=0 else 'N/A'}")
    print(f"  [A] GAIA DR3 AUDIT   : RUWE = {f'{ruwe:.3f}' if ruwe else 'N/A'} | Star M={ms_gaia:.2f} Msun, R={rs_kep:.2f}->{rs_gaia:.2f} Rsun, rho*={rho_st_gaia:.2f} g/cm^3")
    print(f"      PWC Re-Evaluation: R_p = {rp_kep:.2f} -> {rp_gaia:.2f} Re | Octave f_p/f* = {f_ratio_gaia:.2f}x | Shear = {shear_gaia:.2f}xE | Flux = {seff_gaia:.2f} Se")
    if rho_ratio_tr is not None:
        print(f"      Transit Chord rho: rho_transit = {srho_tr:.2f} g/cm^3 vs rho_Gaia = {rho_st_gaia:.2f} g/cm^3 (ratio {rho_ratio_tr:.2f}x)")
    print(f"  [B] PIXEL CENTROIDS  : OOT Shift = {f'{dicco:.3f}\" ({sig_dicco:.2f}s)' if sig_dicco is not None else 'N/A'} | "
          f"KIC Shift = {f'{dikco:.3f}\" ({sig_dikco:.2f}s)' if sig_dikco is not None else 'N/A'} | Neighbors <7.2\" = {n_Execution_neighbors}")
    print(f"  [C] O-C TIMING AUDIT : Ephemeris T0_err = +/-{t0_err_min:.1f} min, P_err = +/-{per_err_min:.1f} min/orbit | Holczer TTV rows = {len(ttv_data.get(koi, []))}")
    if koi in raw_oc_results and raw_oc_results[koi]:
        pts = raw_oc_results[koi]
        oc_str = ", ".join([f"N={n}: O-C={oc:+.1f}m ({dip:.0f}ppm)" for n, _, _, oc, dip in pts])
        print(f"      Raw MAST Transits: {oc_str}")
        if len(pts) >= 3:
            curv_min = (pts[1][2] - 0.5 * (pts[0][2] + pts[2][2])) * 1440.0
            print(f"      3-Transit Midpoint Curvature (t1 - (t0+t2)/2) = {curv_min:+.2f} min (Moon keel target: +/-3 to 4 min)")
    if kills:
        for k in kills:
            print(f"  [X] KILL REASON      : {k}")
    if warnings:
        for w in warnings:
            print(f"  [!] CAUTION FLAG     : {w}")
    print(f"  ===> FINAL VERDICT   : {verdict}")

print("\n" + "=" * 122)
print(f"FINAL SURVIVORS AFTER GAIA DR3 + PIXEL CENTROID + TIMING AUDIT: {survivors_final if survivors_final else 'NONE (0)'}")
print("=" * 122)
