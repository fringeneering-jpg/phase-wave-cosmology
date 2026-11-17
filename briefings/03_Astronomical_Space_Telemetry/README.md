# Specialist Briefing 03: Precision Astrodynamics, Planetary Ephemerides & Spacecraft Telemetry (v1.1)

**Document:** [`PWC_03_Astronomical_Ephemeris_and_Telemetry.pdf`](./PWC_03_Astronomical_Ephemeris_and_Telemetry.pdf)  
**Target Domain:** Deep-Space Radio-Metric Tracking, Planetary Ephemerides, Binary Asteroid Dynamics (DART / ESA *Hera*), Satellite Laser Ranging (SLR) & Orbital Station-Keeping

---

## Included Manuscript Sections
- **Title, Abstract & Operational Plenum Axioms**
- **Section 1 — Einstein Foundations, 49/51 One-Way Light Asymmetry & Viking Telemetry:** Resolution of the one-way speed of light paradox on an expanding medium track ($49\%$ outbound / $51\%$ inbound split at $D_0/R_H = 0.03845$) and parameter-free closure of the JPL DE410 Table III Viking 1 & Viking 2 Mars lander range-bias latitude ratio ($0.7246$ predicted vs. $0.7056$ observed, $2.63\%$).
- **Section 2 — Dr. John D. Anderson's Astrodynamic Legacy:** Master Equation of State, unmasking quadratic entropic expansion absorbed into fitted $GM_{\text{app}}(r) = GM_{\text{true}} + a_{\text{entropy}} r^2$, exact reconciliation with the IAU/IERS `TCB`/`TDB`/`TT` relativistic clock ladder, zero-parameter closure of the 5 solar-system anomalies (AU drift $14.88\text{ cm/yr}$, Pioneer 10/11 $+0.14\sigma$, Ulysses polar chimney $-0.03\sigma$, `'Oumuamua` $+0.75\sigma$, Lagrange saddle floor), and 5/5 Earth gravity-assist flyby jump signs ($V_A = 14.6644\text{ mm/s}$).
- **Section 7 — Operational Software & Telemetry Engines (`Wurral` & `Jiba`) & Pre-Registered v1.1 Blind Falsifiers:**
  - **Wurral 15-Body 1PN EIH + Moyer Propagator:** 50-year unpinned solar-system integration (1976–2026) closing Cassini Saturn range telemetry without empirical Kuiper Belt fudge rings or 339 fitted asteroid knobs, plus planetary spin-flattening lock ($1.20\%$ mean residual across 6 unlocked planets).
  - **Jiba Blind SLR Station-Keeping Engine:** Two-parameter ILRS pass solver cutting unmodeled LARES 7-day orbital drift by $99.8\%$ (from $4,913.3\text{ m/week}$ to $11.86\text{ m}$) across 1,500+ days of laser telemetry.
  - **Pre-Registered Blind Test 1 — ESA *Hera* / Dimorphos Bulk Density & Spin-Shape Lock (Timestamped 2026-11-17):** Zero-parameter 3-stage derivation of Dimorphos's immediate post-DART period reduction ($-26.39 - 5.38 - 1.20 = \mathbf{-32.97\text{ min}}$ vs. $-33.0\text{ min}$ immediate observed; remaining $-16.6\text{ s}$ matching delayed 3-week rubble settling) and explicit bulk-density kill-fork ($\rho_{\text{Dim}} \ge 2,100\text{–}2,500\text{ kg/m}^3$ PWC normal silicate rubble vs. $\rho_{\text{Dim}} = 1,540 \pm 220\text{ kg/m}^3$ Newtonian point-mass requirement at pinned $\beta_{\text{helio}} = 2.0 \pm 0.3$).
  - **Pre-Registered Blind Test 2 — 2028–2034 Mars–Saturn Unpinned DSN Range Ladder (`ESCAPADE` / `MRO` / `TGO`):** Following explicit falsification of InSight SEIS background marsquake modulation ($p = 0.80\text{–}0.95$), pre-registers the 2028 antisymmetric range dipole (`2028-01-19` outward lift, `2028-05-10` node / `7.840 AU` min separation on `2028-05-18`, `2028-09-22` inward push) and monotonic strengthening into `2030` ($7.630\text{ AU}$), `2032` ($7.498\text{ AU}$), and `2034` ($7.478\text{ AU}$).
  - **Pre-Registered Benchtop Lab Falsifier:** Cold tunnel-ionization ($100\text{ fs}$) endothermic untying trough ($2\text{–}10\text{ cm}$ standoff, $0.5\text{ T}$ ion shield, $0.1\text{–}10\text{ mTorr}$ vacuum).
- **Orbital & Solar System Falsification Ledger (Table 22, incl. rows 18a–18c)** & **Full Bibliography**.

---

## Bundled Zero-Parameter Verification Scripts

Run directly with Python 3 (Standard Library only):

```bash
# 1. Secular AU drift, Pioneer 10/11, Ulysses polar chimney, 'Oumuamua & Lagrange saddle floor
python astrodynamic_anomalies_anderson.py

# 2. Expanding-track RK4 + analytical 49/51 split, Viking 1/2 DE410 range biases & JWST chronometer
python treadmill_49_51.py

# 3. Pre-registered DART / Dimorphos 3-stage period reduction (-32.97 min) & ESA Hera density kill-fork
python dart_dimorphos_pwc_audit.py
```

---

## Live Operational Engines & Full Framework Repositories
- **Wurral Astrodynamics & Ephemeris Engine:** [https://github.com/fringeneering-jpg/Wurral](https://github.com/fringeneering-jpg/Wurral)
- **Jiba Satellite Station-Keeping Engine:** [https://github.com/fringeneering-jpg/Jiba](https://github.com/fringeneering-jpg/Jiba)
- **Master GitHub Repository:** [https://github.com/fringeneering-jpg/phase-wave-cosmology](https://github.com/fringeneering-jpg/phase-wave-cosmology)
- **Permanent Zenodo Archive (Concept DOI):** [https://doi.org/10.5281/zenodo.24281039](https://doi.org/10.5281/zenodo.24281039)
- **Author ORCID:** [https://orcid.org/0009-0005-4121-4296](https://orcid.org/0009-0005-4121-4296)
