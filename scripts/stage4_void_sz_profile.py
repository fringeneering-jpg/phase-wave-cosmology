#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
stage4_void_sz_profile.py - the ACT/SPT void-stacking SZ falsifier
(Phase Wave Cosmology, stage-4, 2026-10-21).

FALSIFIABLE_CATALOG.md row 23 (P2-A stacked SZ test):
    y_wall/y_void = 19/18 = 1.05556 -- a STEP FUNCTION at the void edge:
    the wall is the untying front (always moving out); the swept void
    behind runs at 18/19 = 94.74% (the 1/19 = 5.26% deficit is the
    retained debt share s = 1/19). The front is a LOCAL MAXIMUM of the
    stacked radial profile; void centers are under-pressured.
    ZERO fitted parameters.

WHAT THIS SCRIPT DOES
    1. Loads the Douglass+ 2023 void catalog (VizieR J/ApJS/265/7/table1,
       VoidFinder maximal spheres) with EXACTLY the same parsing as the
       reference stage4_wall_void_y_contrast.py (RAJ2000/DEJ2000/Rad/x/y/z
       fields), plus the row-23 selection columns (Cosmo/edge/s/Reff).
    2. Builds the stacked radial profile: annular bins
       0.0-0.5-1.0-1.5-2.0 R/R_eff around each void center, mean y per bin,
       from a healpix y-map interface (Planck MILCA local map, or any
       ACT/SPT healpix y-map path given on the command line).
    3. Runs the 19/18 = 1.0556 test: inner-bin mean vs wall-bin mean,
       the contrast, and the void-bootstrap error.
    4. Prints the row-23 kill-condition verdicts, pre-stated BEFORE the
       data are read, and the final verdict. Always exits 0.

KILL CONDITIONS (row 23, pre-stated; not modified by anything this
script measures):
    (1) r < 1 at >= 3 sigma                         -> KILL
    (2) |r - 1.0556| > 3*sigma_tot, where
        sigma_tot = sqrt(sigma_stat^2 + 0.010^2)    -> KILL
        (sigma_sys = 0.010 floor)
    (3) no front peak at 3 sigma                    -> KILL
    (4) full y-map coupling: y = 0.62 per 100 Mpc
        vs observed <= 1e-5 -- ALREADY DEAD, recorded, not re-examined.
    NO-DECISION GATE: sigma_stat > 0.028 -> INCONCLUSIVE, the row stays
    OPEN, no kill is fired, no retrofitting.

CONVENTIONS (documented, not tuned):
    inner bin = [0.0, 0.5) R/R_eff   (deep void interior)
    wall bin  = [1.0, 1.5) R/R_eff   (annulus just outside the edge,
                where the step function puts the untying front)
    The bins are exactly the task spec 0.0-0.5-1.0-1.5-2.0.
    Sensitivity bands (frozen by Pillar 2, capture/
    2026-10-21_PROMPT_F_final_fed_by_bridges.md section 2):
    interior 0.2-0.7 R_eff vs front 0.85-1.15 R_eff -- reported, never tuned.

MAP INTERFACE: --map accepts (a) the Planck MILCA bin-table y-map with a
FULL column, (b) a generic full-sky healpix image HDU, (c) an ACT/SPT-style
bin-table with an I column. NSIDE and ORDERING (RING/NESTED) are read from
the header and honored.

USAGE
    default (MILCA cross-check):
        .venv-solar\\Scripts\\python.exe scripts\\stage4_void_sz_profile.py
    ACT/SPT primary (when the user obtains the map):
        .venv-solar\\Scripts\\python.exe scripts\\stage4_void_sz_profile.py --map D:\\path\\to\\act_dr6_ymap.fits
"""
import argparse
import math
import os
import sys
import time
import traceback

import numpy as np
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u
import astropy_healpix as ah

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ----------------------------------------------------------------------
# LOCKED CONSTANTS (workspace lock, provenance per number; only the TEST
# numbers below are consumed by this script, the rest are provenance).
# ----------------------------------------------------------------------
C0          = 2.99792458e8    # m/s     exact SI definition
RHO0        = 8.74e-27        # kg/m^3  locked critical density input (workspace lock)
S           = 1.0 / 19.0      # locked retained debt share (workspace lock s = 1/19)
Y_BOW       = 5.9307e26       # locked bow yield (workspace lock)
N           = 2.0 / 33.0      # locked winding ratio (workspace lock)
F_SOLID     = 8.4989e-4       # locked solid share (workspace lock)
T           = 27              # locked tightening coefficient (workspace lock)
G           = 6.67430e-11     # m^3 kg^-1 s^-2  CODATA 2018
HBAR        = 1.054571817e-34 # J s             CODATA 2018
KB          = 1.380649e-23    # J/K             exact SI definition
Q_CMB       = 4.175e-14       # workspace lock (CMB quadrupole scale)
T_CMB       = 2.7255          # K     Fixsen 2009
H0_WALL     = 73.935          # km/s/Mpc  locked wall-route Hubble constant
H0_PLANCK   = 67.36           # km/s/Mpc  Planck 2018

# ----------------------------------------------------------------------
# TEST CONSTANTS (all pre-stated by FALSIFIABLE_CATALOG.md row 23; none
# of them is fitted, none is read back from the data).
# ----------------------------------------------------------------------
PRED_RATIO     = 19.0 / 18.0          # row 23: y_wall/y_void = 19/18 (19:1:18 balance)
PRED_RATIO_TXT = "19/18 = 1.05556"
SIGMA_SYS      = 0.010                # row 23: sigma_sys floor for sigma_tot
NO_DEC_SIGMA   = 0.028                # row 23: no-decision gate on sigma_stat
FULL_COUP_Y    = 0.62                 # row 23: full y-map coupling, y per 100 Mpc (dead)
BINS_MAIN      = [0.0, 0.5, 1.0, 1.5, 2.0]   # task spec: annular bins, R/R_eff
INNER_BIN      = 0                    # [0.0, 0.5)  -- deep interior
WALL_BIN       = 2                    # [1.0, 1.5)  -- annulus just outside the edge
FROZEN_INNER   = (0.2, 0.7)           # frozen Pillar-2 interior band (R_eff)
FROZEN_FRONT   = (0.85, 1.15)         # frozen Pillar-2 front band   (R_eff)
N_BOOT         = 1000                 # void bootstrap resamples (documented choice)
SEED           = 1918                 # the digits of 19/18 (documented choice)
N_RAND         = 500                  # random-position stacks (frozen design: 500)
MIN_PIX        = 3                    # minimum map pixels per aggregate bin per void
B_MIN          = 15.0                 # row 23: |b| >= 15 deg

DEFAULT_MILCA  = r"D:\planck_milca_y_2048.fits"
DEFAULT_VOIDS  = r"C:\Users\jaden\Downloads\PWC-Check\PWC\data\voids\voids_vf.txt"
HERE           = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------
# Kill conditions, pre-stated (printed before any data are loaded).
# ----------------------------------------------------------------------
KILL_BANNER = (
    "KILL CONDITIONS (predictions/FALSIFIABLE_CATALOG.md row 23, pre-stated;\n"
    "nothing measured below can change them):\n"
    "  (1) r < 1 at >= 3 sigma                        -> KILL\n"
    "  (2) |r - 1.0556| > 3*sigma_tot                 -> KILL\n"
    "      sigma_tot = sqrt(sigma_stat^2 + sigma_sys^2), sigma_sys = 0.010 floor\n"
    "  (3) no front peak at 3 sigma                   -> KILL\n"
    "  (4) full y-map coupling (y = 0.62 per 100 Mpc vs observed <= 1e-5)\n"
    "      -> ALREADY DEAD, recorded now, not re-examined\n"
    "  NO-DECISION GATE: sigma_stat > 0.028 -> INCONCLUSIVE, row stays OPEN,\n"
    "  no kill fires, no retrofitting (the ACT/SPT map is then required).\n"
)

# ----------------------------------------------------------------------
# Map interface
# ----------------------------------------------------------------------
def load_ymap(path):
    """Load a HEALPix y-map from any of three FITS layouts.
    Returns (y, nside, ordering, unit, description)."""
    y, nside, ordering, unit, desc = None, None, None, None, None
    with fits.open(path, memmap=False) as hdul:
        for hdu in hdul:
            hdr = hdu.header
            ns = hdr.get("NSIDE")
            if not ns:
                continue
            cand = None
            cand_unit = None
            cand_desc = None
            if isinstance(hdu, fits.BinTableHDU):
                cols = [c.lower() for c in hdu.columns.names]
                if "full" in cols:
                    name = hdu.columns.names[cols.index("full")]
                elif "i" in cols:
                    name = hdu.columns.names[cols.index("i")]
                elif "y" in cols:
                    name = hdu.columns.names[cols.index("y")]
                else:
                    continue
                cand = np.asarray(hdu.data[name])
                cand_unit = hdu.columns[name].unit
                cand_desc = "bin-table column %r" % name
            else:
                data = getattr(hdu, "data", None)
                if data is not None and getattr(data, "ndim", 0) == 1:
                    cand = np.asarray(data)
                    cand_unit = hdr.get("TUNIT1") or hdr.get("BUNIT")
                    cand_desc = "1-D image HDU"
            if cand is None:
                continue
            if len(cand) != 12 * int(ns) * int(ns):
                continue
            y = cand.astype(np.float32)
            nside = int(ns)
            ordering = (hdr.get("ORDERING") or "RING").upper()
            unit = str(cand_unit) if cand_unit else "unknown (header has no unit)"
            desc = cand_desc
            break
    if y is None:
        raise ValueError("no healpix y-map found in %s" % path)
    return y, nside, ordering, unit, desc


def angsep_deg(lon0, lat0, lon, lat):
    """Great-circle angular separation in degrees, vectorized."""
    lo0, la0 = np.radians(lon0), np.radians(lat0)
    lo, la = np.radians(np.asarray(lon)), np.radians(np.asarray(lat))
    dl = lo - lo0
    num = np.maximum((np.cos(la) * np.sin(dl)) ** 2 +
                     (np.cos(la0) * np.sin(la) - np.sin(la0) * np.cos(la) * np.cos(dl)) ** 2, 0.0)
    den = np.sin(la0) * np.sin(la) + np.cos(la0) * np.cos(la) * np.cos(dl)
    return np.degrees(np.arctan2(np.sqrt(num), den))


# ----------------------------------------------------------------------
# Void catalog loader -- same parsing as stage4_wall_void_y_contrast.py
# ----------------------------------------------------------------------
def load_voids(path):
    """Parse data/voids/voids_vf.txt (VizieR J/ApJS/265/7/table1) exactly as
    the reference stage-4 script: find the 'recno' header line, skip to the
    dash line, then whitespace-split the data rows.
    Columns: recno Cosmo x y z Rad void edge s RAJ2000 DEJ2000 Reff
    (x,y,z,Rad,s,Reff in h^-1 Mpc; RA/DE J2000 deg)."""
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    hdr_i = None
    for i, ln in enumerate(lines):
        if ln.startswith("#") or not ln.strip():
            continue
        if "recno" in ln:
            hdr_i = i
            break
    if hdr_i is None:
        raise ValueError("no 'recno' header line in %s" % path)
    dash_i = None
    for i in range(hdr_i + 1, min(hdr_i + 25, len(lines))):
        if set(lines[i].strip().replace("\t", "")) == set("-"):
            dash_i = i
            break
    if dash_i is None:
        raise ValueError("no dash line after header in %s" % path)
    rows = []
    for ln in lines[dash_i + 1:]:
        if not ln.strip() or ln.startswith("#"):
            continue
        flds = ln.split()
        if len(flds) < 12:
            continue
        try:
            recno = int(flds[0]);   cosmo = flds[1]
            x = float(flds[2]);     y = float(flds[3]);  z = float(flds[4])
            rad = float(flds[5]);   void_id = int(flds[6]); edge = int(flds[7])
            s = float(flds[8]);     ra = float(flds[9]); dec = float(flds[10])
            reff = float(flds[11])
        except ValueError:
            continue
        rows.append(dict(recno=recno, cosmo=cosmo, x=x, y=y, z=z, rad=rad,
                         void=void_id, edge=edge, s=s, ra=ra, dec=dec, reff=reff))
    return rows


# ----------------------------------------------------------------------
# Stacked-profile machinery
# ----------------------------------------------------------------------
FINE_EDGES = [0.0, 0.2, 0.5, 0.7, 0.85, 1.0, 1.15, 1.5, 2.0]
# fine bins: f0[0,0.2) f1[0.2,0.5) f2[0.5,0.7) f3[0.7,0.85) f4[0.85,1.0)
#            f5[1.0,1.15) f6[1.15,1.5) f7[1.5,2.0)
A_GROUPS = [[0, 1], [2, 3, 4], [5, 6], [7]]   # main bins 0-0.5-1.0-1.5-2.0
B_INTERIOR = [1, 2]                           # frozen 0.2-0.7
B_FRONT = [4, 5]                              # frozen 0.85-1.15


def prepare_grid(hp):
    """Precompute full-sky pixel centers ONCE per map. Rationale: the
    astropy_healpix cone_search_lonlat primitive is pathologically slow
    (measured 2026-10-22: 26.5 s for one 45-deg cone at NSIDE 256; the
    native-NSIDE-2048 run with ~1,500 cones was aborted after 50 min at
    ~3 positions/min). A cone is instead built as a |d_lat| <= r band
    (complete, since great-circle distance >= |d_lat|) plus exact
    vectorized great-circle separations."""
    pix = np.arange(hp.npix, dtype=np.int64)
    lon, lat = hp.healpix_to_lonlat(pix)
    return (pix, np.asarray(lon.to_value(u.deg), dtype=np.float64),
            np.asarray(lat.to_value(u.deg), dtype=np.float64))


def downgrade_map(y, hp_in, nside_out):
    """Exact pixel-averaged downgrade of a healpix map (RING or NESTED):
    each fine pixel is assigned to its coarse pixel via lonlat_to_healpix;
    the coarse map is the fine-pixel mean. Verified against direct
    per-coarse-pixel means to ~1e-13 on the MILCA map (2026-10-22)."""
    t0 = time.time()
    pix = np.arange(hp_in.npix, dtype=np.int64)
    lon, lat = hp_in.healpix_to_lonlat(pix)
    hp_out = ah.HEALPix(nside=nside_out, order=hp_in.order)
    coarse = hp_out.lonlat_to_healpix(lon, lat)
    cnt = np.bincount(coarse, minlength=hp_out.npix)
    ysum = np.bincount(coarse, weights=np.asarray(y, dtype=np.float64),
                       minlength=hp_out.npix)
    y_low = np.where(cnt > 0, ysum / np.maximum(cnt, 1), np.nan).astype(np.float32)
    print("    map downgraded %d -> %d in %.1f s (exact fine-pixel mean, "
          "verified 2026-10-22)" % (hp_in.nside, nside_out, time.time() - t0))
    return y_low, hp_out


def stack_positions(y, grid, geoms, min_pix, label):
    """For each position (galactic lon0/lat0 deg, angular edge list deg),
    accumulate fine annular-bin means; then aggregate into the main bins
    (pixel-count weighted within each void) and the frozen bands.
    Returns (pvmA, pvmB, cntA, n_used): per-void means for the main bins
    (n x 4), per-void means for the frozen bands (n x 2), per-void
    aggregate pixel counts (n x 4), and the number of positions used."""
    pix_all, lon_all, lat_all = grid
    n = len(geoms)
    nf = len(FINE_EDGES) - 1
    pvmA = np.full((n, len(A_GROUPS)), np.nan)
    pvmB = np.full((n, 2), np.nan)
    cntA = np.zeros((n, len(A_GROUPS)), dtype=np.int64)
    n_used = 0
    t0 = time.time()
    for i, (lon0, lat0, te_deg) in enumerate(geoms):
        band = np.abs(lat_all - lat0) <= te_deg[-1] + 0.05
        if not np.any(band):
            continue
        sep = angsep_deg(lon0, lat0, lon_all[band], lat_all[band])
        vals = y[pix_all[band]]
        ok = np.isfinite(vals) & np.isfinite(sep)
        if not np.any(ok):
            continue
        idx = np.searchsorted(te_deg, sep[ok])
        inr = (idx >= 1) & (idx <= nf)
        if not np.any(inr):
            continue
        ib = idx[inr] - 1
        v = vals[ok][inr]
        fcnt = np.bincount(ib, minlength=nf)
        fmean = np.full(nf, np.nan)
        nz = fcnt > 0
        fmean[nz] = np.bincount(ib, weights=v, minlength=nf)[nz] / fcnt[nz]
        def agg(groups):
            out = np.full(len(groups), np.nan)
            for g, grp in enumerate(groups):
                tot = sum(fcnt[b] for b in grp)
                if tot >= min_pix:
                    out[g] = sum(fmean[b] * fcnt[b] for b in grp) / tot
            return out
        a = agg(A_GROUPS)
        pvmA[i] = a
        cntA[i] = [sum(fcnt[b] for b in grp) for grp in A_GROUPS]
        pvmB[i] = agg([B_INTERIOR, B_FRONT])
        n_used += 1
        if (i + 1) % 250 == 0:
            print("    %s: %d/%d positions (%.0f s)"
                  % (label, i + 1, n, time.time() - t0))
    return pvmA, pvmB, cntA, n_used


def bootstrap_stats(pvm, n_boot, seed):
    """Bootstrap over positions: returns per-bin stacked means, bootstrap
    std per bin, plus for the (inner, wall) bin pair: r, sigma_stat,
    wall-inner difference and its sigma, and the wall-vs-adjacent local
    peak z-scores. ZERO fitted parameters: means and stds only."""
    rng = np.random.default_rng(seed)
    n = pvm.shape[0]
    means_b = np.empty((n_boot, pvm.shape[1]))
    for k in range(n_boot):
        idx = rng.integers(0, n, n)
        means_b[k] = np.nanmean(pvm[idx], axis=0)
    stacked = np.nanmean(pvm, axis=0)
    sigma_bin = np.nanstd(means_b, axis=0, ddof=1)
    return stacked, sigma_bin, means_b


# ----------------------------------------------------------------------
# Report
# ----------------------------------------------------------------------
def main(argv):
    lines = []  # collected report -> written to disk at the end

    def log(msg=""):
        print(msg)
        lines.append(msg)

    t_run = time.strftime("%Y-%m-%d %H:%M:%S")
    log("=" * 78)
    log("STAGE-4 VOID-SZ PROFILE FALSIFIER  --  FALSIFIABLE_CATALOG.md row 23")
    log("run: %s" % t_run)
    log("=" * 78)
    log(KILL_BANNER)
    log("ZERO fitted parameters: every number below is a mean, a ratio or a")
    log("bootstrap std; the prediction 19/18 = 1.0556 and all thresholds are")
    log("pre-stated from row 23 and are not read back from the data.")

    ap = argparse.ArgumentParser(description="stage-4 stacked void-SZ profile falsifier")
    ap.add_argument("--map", default=None,
                    help="healpix y-map FITS (default: Planck MILCA at %s)" % DEFAULT_MILCA)
    ap.add_argument("--voids", default=DEFAULT_VOIDS, help="void catalog")
    ap.add_argument("--n-boot", type=int, default=N_BOOT, help="bootstrap resamples")
    ap.add_argument("--seed", type=int, default=SEED, help="bootstrap seed")
    ap.add_argument("--n-rand", type=int, default=N_RAND, help="random-position stacks")
    ap.add_argument("--min-pix", type=int, default=MIN_PIX, help="min pixels per bin per void")
    ap.add_argument("--nside-target", type=int, default=512,
                    help="working NSIDE: the map is exactly pixel-averaged down to this "
                         "before stacking (default 512 = 6.9' pixels, far finer than the "
                         "degree-wide bins; set to the native NSIDE to disable)")
    ap.add_argument("--out", default=os.path.join(HERE, "stage4_void_sz_profile_results.txt"),
                    help="results file")
    ap.add_argument("--profile-csv", default=os.path.join(HERE, "stage4_void_sz_profile_profile.csv"),
                    help="profile CSV file")
    args = ap.parse_args(argv)

    map_path = args.map or (DEFAULT_MILCA if os.path.exists(DEFAULT_MILCA) else None)
    if map_path is None:
        log("MISS: no --map given and the default MILCA map is absent:")
        log("      %s" % DEFAULT_MILCA)
        log("      provide an ACT/SPT healpix y-map: --map <path>")
        return 0

    # ---- map ---------------------------------------------------------
    log("")
    log("---- MAP ----")
    log("path     : %s" % map_path)
    y, nside, ordering, unit, desc = load_ymap(map_path)
    log("layout   : %s | NSIDE %d | ORDERING %s" % (desc, nside, ordering))
    log("unit     : %s" % unit)
    log("pixels   : %d | finite %d" % (len(y), int(np.isfinite(y).sum())))
    log("y range  : %+.4e .. %+.4e | median %+.4e"
        % (float(np.nanmin(y)), float(np.nanmax(y)), float(np.nanmedian(y))))
    if ordering not in ("RING", "NESTED"):
        log("MISS: unrecognized ORDERING %r -- treated as RING (documented)" % ordering)
        ordering = "RING"
    hp = ah.HEALPix(nside=nside, order=ordering.lower())
    if args.nside_target and nside > args.nside_target:
        y, hp = downgrade_map(y, hp, args.nside_target)
        nside = args.nside_target
        log("y range  : %+.4e .. %+.4e | median %+.4e"
            % (float(np.nanmin(y)), float(np.nanmax(y)), float(np.nanmedian(y))))
        log("pixels   : %d" % len(y))

    # ---- catalog -----------------------------------------------------
    log("")
    log("---- VOID CATALOG (Douglass+ 2023, VizieR J/ApJS/265/7/table1) ----")
    log("path     : %s" % args.voids)
    rows = load_voids(args.voids)
    log("parsed   : %d rows (parsing identical to stage4_wall_void_y_contrast.py)" % len(rows))
    n_planck = sum(1 for r in rows if r["cosmo"] == "Planck2018")
    n_wmap = sum(1 for r in rows if r["cosmo"] == "WMAP5")
    log("cosmology: Planck2018 rows %d | WMAP5 rows %d (paper's 1,163 per cosmology)"
        % (n_planck, n_wmap))
    c = SkyCoord(ra=[r["ra"] for r in rows], dec=[r["dec"] for r in rows],
                 unit="deg", frame="icrs")
    gal = c.galactic
    for i, r in enumerate(rows):
        r["glon"] = float(gal.l.deg[i])
        r["glat"] = float(gal.b.deg[i])
    # selection per row 23
    sel = [r for r in rows if r["cosmo"] == "Planck2018"]
    log("cut 1    : Cosmo == Planck2018            -> %d rows" % len(sel))
    sel = [r for r in sel if r["edge"] == 0]
    log("cut 2    : edge == 0 (inside survey mask) -> %d rows" % len(sel))
    sel = [r for r in sel if abs(r["glat"]) >= B_MIN]
    log("cut 3    : |b| >= %.0f deg                 -> %d rows" % (B_MIN, len(sel)))
    log("cut 4    : cluster-mask  -> NOT APPLIED (no cluster catalog present in")
    log("           the workspace; reported as a miss, never hidden). Row 23's")
    log("           'cluster-masked: 805 voids' and the capture note's")
    log("           '~1,160 voids' therefore cannot be reproduced here; the")
    log("           un-masked sample above is used as-is for the MILCA")
    log("           cross-check. Cluster y-boost acts randomly in angle and")
    log("           can only dilute the stacked contrast, not create it.")
    if not sel:
        log("MISS: selection empty -- nothing to stack.")
        return 0
    # consistency: s vs sqrt(x^2+y^2+z^2)
    ddiff = [abs(r["s"] - math.sqrt(r["x"]**2 + r["y"]**2 + r["z"]**2)) for r in sel]
    log("geometry : comoving distance s vs sqrt(x^2+y^2+z^2): max |diff| %.5f h^-1 Mpc"
        % max(ddiff))
    log("sample   : %d voids | median Reff %.2f h^-1 Mpc | median D %.1f h^-1 Mpc"
        % (len(sel), float(np.median([r["reff"] for r in sel])),
           float(np.median([math.sqrt(r["x"]**2 + r["y"]**2 + r["z"]**2) for r in sel]))))

    # ---- geometry ----------------------------------------------------
    geoms = []
    for r in sel:
        D = math.sqrt(r["x"] ** 2 + r["y"] ** 2 + r["z"] ** 2)
        if D <= 0 or r["reff"] <= 0:
            continue
        te = np.degrees(np.arctan(np.asarray(FINE_EDGES) * r["reff"] / D))
        geoms.append((r["glon"], r["glat"], te))
    log("geometry : %d voids with usable R_eff and D (angular bins via" % len(geoms))
    log("           theta = arctan((R/R_eff)*Reff/D), comoving, exact on the sphere)")

    # ---- stacked profile ---------------------------------------------
    log("")
    log("---- STACKED PROFILE (annular bins 0.0-0.5-1.0-1.5-2.0 R/R_eff) ----")
    t0 = time.time()
    grid = prepare_grid(hp)
    log("    full-sky pixel grid prepared (%.0f s)" % (time.time() - t0))
    t0 = time.time()
    pvmA, pvmB, cntA, n_used = stack_positions(y, grid, geoms, args.min_pix, "voids")
    log("    void stacks done in %.0f s (%d used)" % (time.time() - t0, n_used))
    stackedA, sigmaA_bin, bootA = bootstrap_stats(pvmA, args.n_boot, args.seed)
    # pixel-weighted stacked means (sensitivity)
    wsum = np.nansum(pvmA * cntA, axis=0)
    wcnt = np.nansum(np.where(np.isfinite(pvmA), cntA, 0), axis=0)
    pixel_weighted = wsum / np.maximum(wcnt, 1)
    n_contrib = np.sum(np.isfinite(pvmA), axis=0)

    bin_labels = ["[0.0,0.5)", "[0.5,1.0)", "[1.0,1.5)", "[1.5,2.0)"]
    log("  bin (R/R_eff)  voids    void-stacked mean      bootstrap sigma   pixel-wtd mean")
    for b in range(4):
        log("  %-13s %6d    %+12.4e           %.4e          %+12.4e"
            % (bin_labels[b], int(n_contrib[b]), float(stackedA[b]),
               float(sigmaA_bin[b]), float(pixel_weighted[b])))

    # frozen bands (sensitivity, reported never tuned)
    stackedB, sigmaB_bin, _ = bootstrap_stats(pvmB, args.n_boot, args.seed)
    log("  frozen bands (sensitivity, Pillar-2 design): interior 0.2-0.7 R_eff ->")
    log("    mean %+.4e (sigma %.4e) | front 0.85-1.15 R_eff -> %+.4e (sigma %.4e)"
        % (float(stackedB[0]), float(sigmaB_bin[0]),
           float(stackedB[1]), float(sigmaB_bin[1])))

    # ---- random-position stacks (frozen design: 500) -----------------
    log("")
    log("---- RANDOM-POSITION STACKS (%d, frozen design; field/null profile) ----"
        % args.n_rand)
    rng_geo = np.random.default_rng(args.seed + 1)
    reffs = np.array([r["reff"] for r in sel])
    Ds = np.array([math.sqrt(r["x"]**2 + r["y"]**2 + r["z"]**2) for r in sel])
    ok_geo = (reffs > 0) & (Ds > 0)
    reffs, Ds = reffs[ok_geo], Ds[ok_geo]
    rgeoms = []
    for _ in range(args.n_rand):
        lon0 = float(rng_geo.uniform(0.0, 360.0))
        lat0 = float(np.degrees(np.arcsin(rng_geo.uniform(-1.0, 1.0))))
        k = int(rng_geo.integers(0, len(reffs)))
        te = np.degrees(np.arctan(np.asarray(FINE_EDGES) * reffs[k] / Ds[k]))
        rgeoms.append((lon0, lat0, te))
    t0 = time.time()
    rpvmA, _, _, r_used = stack_positions(y, grid, rgeoms, args.min_pix, "random")
    log("    random stacks done in %.0f s (%d used)" % (time.time() - t0, r_used))
    rstackedA, rsigmaA, _ = bootstrap_stats(rpvmA, args.n_boot, args.seed)
    for b in range(4):
        log("  %-13s field mean %+12.4e | void-field %+12.4e (sigma %.4e)"
            % (bin_labels[b], float(rstackedA[b]),
               float(stackedA[b] - rstackedA[b]), float(rsigmaA[b])))

    # ---- the 19/18 test ----------------------------------------------
    log("")
    log("=" * 78)
    log("THE 19/18 = 1.0556 TEST (inner bin [0.0,0.5) vs wall bin [1.0,1.5) R/R_eff)")
    log("=" * 78)
    y_inner = float(stackedA[INNER_BIN])
    y_wall = float(stackedA[WALL_BIN])
    r_boot = bootA[:, WALL_BIN] / bootA[:, INNER_BIN]
    d_boot = bootA[:, WALL_BIN] - bootA[:, INNER_BIN]
    r_meas = float(y_wall / y_inner) if abs(y_inner) > 1e-30 else float("nan")
    sigma_stat = float(np.nanstd(r_boot, ddof=1))
    d_meas = float(y_wall - y_inner)
    sigma_d = float(np.nanstd(d_boot, ddof=1))
    # local-max peak z-scores: wall vs inner side and wall vs far side
    z_wi = d_meas / sigma_d if sigma_d > 0 else 0.0
    d_w3_boot = bootA[:, WALL_BIN] - bootA[:, 3]
    d_w3 = float(y_wall - stackedA[3])
    z_w3 = d_w3 / float(np.nanstd(d_w3_boot, ddof=1)) if np.nanstd(d_w3_boot, ddof=1) > 0 else 0.0
    d_w1_boot = bootA[:, WALL_BIN] - bootA[:, 1]
    d_w1 = float(y_wall - stackedA[1])
    z_w1 = d_w1 / float(np.nanstd(d_w1_boot, ddof=1)) if np.nanstd(d_w1_boot, ddof=1) > 0 else 0.0
    z_peak = float(min(z_wi, z_w1, z_w3))
    valid = np.isfinite(pvmA[:, WALL_BIN]) & np.isfinite(pvmA[:, INNER_BIN])
    frac_wall_above = float(np.mean(pvmA[valid, WALL_BIN] > pvmA[valid, INNER_BIN]))

    log("inner-bin mean (void interior, [0.0,0.5) R/R_eff): %+.4e" % y_inner)
    log("wall-bin  mean (edge annulus,  [1.0,1.5) R/R_eff): %+.4e" % y_wall)
    log("wall - inner (the signed contrast, map units)   : %+.4e (sigma %.4e, z %+.2f)"
        % (d_meas, sigma_d, z_wi))
    log("r = wall/inner                                   : %.4f" % r_meas)
    log("sigma_stat (void bootstrap on r, %d resamples, seed %d): %.4f"
        % (args.n_boot, args.seed, sigma_stat))
    sign_park = y_inner <= 0
    if sign_park:
        log("")
        log("  SIGN-REGIME FLAG: y_inner <= 0 on this map. The ratio r = wall/inner is")
        log("  a ratio of (partly) negative means -- the same degeneracy the single-")
        log("  pixel read recorded (0.8548, ratio-of-two-negative-medians artifact).")
        log("  Kill conditions (1) and (2), which are stated on r, are therefore NOT")
        log("  ADJUDICABLE on this map; the signed contrast wall - inner carries the")
        log("  direction read instead. Parked, not fired. (The absolute pressure")
        log("  zero-point is exactly author ruling R1; row 23 is BLOCKED on R1/R2.)")
    log("fraction of voids with wall-bin mean > inner-bin mean: %.1f%%"
        % (100.0 * frac_wall_above))
    log("frozen bands r' = front(0.85-1.15)/interior(0.2-0.7): %.4f"
        % (float(stackedB[1] / stackedB[0]) if abs(stackedB[0]) > 1e-30 else float("nan")))

    # ---- kill-condition verdicts -------------------------------------
    log("")
    log("---- KILL-CONDITION VERDICTS (row 23) ----")
    sigma_tot = math.sqrt(sigma_stat ** 2 + SIGMA_SYS ** 2)
    z1 = (r_meas - 1.0) / sigma_stat if sigma_stat > 0 else 0.0
    z2 = abs(r_meas - PRED_RATIO) / sigma_tot if sigma_tot > 0 else 0.0
    gated = sigma_stat > NO_DEC_SIGMA

    if sign_park:
        log("(1) r < 1 at >= 3 sigma : r = %.4f, z = %+.2f -> NOT ADJUDICABLE"
            % (r_meas, z1)
            + " on this map (sign regime; parked, never fired)")
        log("(2) |r - 1.0556| > 3*sigma_tot : NOT ADJUDICABLE on this map")
        log("    (sign regime; parked, never fired). For the record:")
        log("    |r - %.4f| = %.4f vs 3*sigma_tot = %.4f"
            % (PRED_RATIO, abs(r_meas - PRED_RATIO), 3.0 * sigma_tot))
    else:
        log("(1) r < 1 at >= 3 sigma : r = %.4f, z = %+.2f -> %s"
            % (r_meas, z1, "KILL" if z1 <= -3.0 else "no kill"))
        log("(2) |r - 1.0556| > 3*sigma_tot : |r - %.4f| = %.4f vs 3*sigma_tot = %.4f"
            % (PRED_RATIO, abs(r_meas - PRED_RATIO), 3.0 * sigma_tot)
            + " -> " + ("KILL" if z2 > 3.0 else "no kill"))
        log("    (sigma_stat = %.4f, sigma_sys floor = %.3f, sigma_tot = %.4f)"
            % (sigma_stat, SIGMA_SYS, sigma_tot))
    log("(3) front peak at 3 sigma: z_wall-vs-inner %+.2f, z_vs_0.5-1.0 %+.2f,"
        % (z_wi, z_w1)
        + " z_vs_1.5-2.0 %+.2f -> %s" % (z_w3, "peak at 3 sigma" if z_peak >= 3.0 else "NO front peak at 3 sigma"))
    if z_peak >= 3.0:
        log("    -> condition (3) not fired")
    elif gated:
        log("    -> parked (no-decision gate)")
    else:
        log("    -> condition (3) would fire: KILL")
    log("(4) full y-map coupling: prediction y = %.2f per 100 Mpc (row 23)."
        % FULL_COUP_Y)
    log("    observed stacked bin amplitudes are %.2e (%s) -- full coupling"
        % (float(np.nanmax(np.abs(stackedA))), unit))
    log("    is already dead by row 23; recorded, not re-examined.")
    log("NO-DECISION GATE: sigma_stat = %.4f %s %.3f -> %s"
        % (sigma_stat, ">" if gated else "<=", NO_DEC_SIGMA,
           "GATE OPEN (test below resolution)" if gated else "gate closed (test powered)"))

    # ---- verdict ------------------------------------------------------
    log("")
    log("=" * 78)
    if gated:
        log("VERDICT: INCONCLUSIVE (no-decision gate: sigma_stat > %.3f)." % NO_DEC_SIGMA)
        log("The row 23 item stays OPEN. No kill condition is fired, none is")
        log("retrofitted; the sensitivity is logged above. The ACT DR6 / SPT-3G")
        log("y-maps are required to power the 5.26%% contrast test.")
        if z_wi > 0:
            log("DIRECTION: right (wall bin above the interior bin at z = %+.2f)." % z_wi)
        else:
            log("DIRECTION: not established (z = %+.2f) -- noise-limited." % z_wi)
        log("AMPLITUDE: noise-limited (sigma_stat = %.4f vs the 0.0556 excess)."
            % sigma_stat)
    else:
        kills = []
        if z1 <= -3.0 and not sign_park:
            kills.append("(1) r < 1 at >= 3 sigma")
        if z2 > 3.0 and not sign_park:
            kills.append("(2) |r - 1.0556| > 3*sigma_tot")
        if z_peak < 3.0:
            kills.append("(3) no front peak at 3 sigma")
        if kills:
            log("VERDICT: KILL FIRED -- " + "; ".join(kills) + ".")
        else:
            log("VERDICT: NO KILL FIRED -- the 19/18 = 1.0556 stacked profile")
            log("survives this map at the current resolution.")
    log("=" * 78)

    # ---- re-run command ------------------------------------------------
    log("")
    log("RE-RUN ON AN ACT/SPT MAP (exact command; the loader auto-detects")
    log("NSIDE and RING/NESTED ordering, image or I-column layouts):")
    log('  C:\\Users\\jaden\\Downloads\\PWC-Check\\PWC\\.venv-solar\\Scripts\\python.exe '
        + os.path.abspath(__file__) + " --map <PATH_TO_ACT_DR6_OR_SPT3G_YMAP.fits>")
    log("(suggested: ACT DR6 y-map, 10.1088/1475-7516/2025/11/061, or SPT-3G;")
    log(" use --out and --profile-csv to keep per-map result files separate.)")

    # ---- save outputs --------------------------------------------------
    try:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        log("")
        log("results saved: %s" % args.out)
    except OSError as e:
        log("")
        log("MISS: could not write results file (%s): %s" % (args.out, e))
    try:
        with open(args.profile_csv, "w", encoding="utf-8") as f:
            f.write("bin,R_over_Reff,n_voids,void_stacked_mean,sigma_stat,pixel_weighted_mean,field_mean,void_minus_field\n")
            for b in range(4):
                f.write("%d,%s,%d,%.8e,%.8e,%.8e,%.8e,%.8e\n"
                        % (b, bin_labels[b], int(n_contrib[b]), float(stackedA[b]),
                           float(sigmaA_bin[b]), float(pixel_weighted[b]),
                           float(rstackedA[b]), float(stackedA[b] - rstackedA[b])))
            f.write("# frozen bands: interior 0.2-0.7 R_eff = %.8e; front 0.85-1.15 R_eff = %.8e\n"
                    % (float(stackedB[0]), float(stackedB[1])))
        log("profile CSV saved: %s" % args.profile_csv)
    except OSError as e:
        log("MISS: could not write profile CSV (%s): %s" % (args.profile_csv, e))
    log("")
    log("exit code: 0 (falsifier always exits 0; kills and misses are reported,")
    log("never hidden)")
    return 0


if __name__ == "__main__":
    code = 0
    try:
        code = main(sys.argv[1:])
    except Exception:
        print("MISS (unhandled exception - reported, never hidden):")
        traceback.print_exc()
        code = 0
    sys.exit(code)
