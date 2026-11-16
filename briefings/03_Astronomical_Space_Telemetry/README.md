# Specialist Briefing 03: Precision Astrodynamics, Planetary Ephemerides & Spacecraft Telemetry

**Document:** [`PWC_03_Astronomical_Ephemeris_and_Telemetry.pdf`](./PWC_03_Astronomical_Ephemeris_and_Telemetry.pdf)  
**Target Domain:** Deep-Space Radio-Metric Tracking, Planetary Ephemerides, Satellite Laser Ranging (SLR) & Orbital Station-Keeping

---

## Included Manuscript Sections
- **Title, Abstract & Operational Plenum Axioms**
- **Section 1 — Einstein Foundations, 49/51 One-Way Light Asymmetry & Viking Telemetry:** Resolution of the one-way speed of light paradox on an expanding medium track ($49\%$ outbound / $51\%$ inbound split at $D_0/R_H = 0.03845$) and parameter-free closure of the JPL DE410 Table III Viking 1 & Viking 2 Mars lander range-bias latitude ratio ($0.7246$ predicted vs. $0.7056$ observed, $2.63\%$).
- **Section 2 — Dr. John D. Anderson's Astrodynamic Legacy:** Master Equation of State, unmasking quadratic entropic expansion absorbed into fitted $GM_{\text{app}}(r) = GM_{\text{true}} + a_{\text{entropy}} r^2$, exact reconciliation with the IAU/IERS `TCB`/`TDB`/`TT` relativistic clock ladder, zero-parameter closure of the 5 solar-system anomalies (AU drift $14.88\text{ cm/yr}$, Pioneer 10/11 $+0.14\sigma$, Ulysses polar chimney $-0.03\sigma$, `'Oumuamua` $+0.75\sigma$, Lagrange saddle floor), and 5/5 Earth gravity-assist flyby jump signs ($V_A = 14.6644\text{ mm/s}$).
- **Section 7 — Operational Software & Telemetry Engines (`Wurral` & `Jiba`):**
  - **Wurral 15-Body 1PN EIH + Moyer Propagator:** 50-year unpinned solar-system integration (1978–2026) closing Cassini Saturn range telemetry without empirical Kuiper Belt fudge rings or 343 fitted asteroid knobs.
  - **Jiba Blind SLR Station-Keeping Engine:** Two-parameter ILRS pass solver cutting unmodeled LARES 7-day orbital drift by $99.8\%$ (from $4,913\text{ m/week}$ to $11.86\text{ m}$) across 1,500 days of laser telemetry.
- **Orbital & Solar System Falsification Ledger (Table 22)** & **Full Bibliography**.

---

## Bundled Zero-Parameter Verification Scripts

Run directly with Python 3 (Standard Library only):

```bash
# 1. Secular AU drift, Pioneer 10/11, Ulysses polar chimney, 'Oumuamua & Lagrange saddle floor
python astrodynamic_anomalies_anderson.py

# 2. Expanding-track RK4 + analytical 49/51 split, Viking 1/2 DE410 range biases & JWST chronometer
python treadmill_49_51.py
```

---

## Live Operational Engines & Full Framework Repositories
- **Wurral Astrodynamics & Ephemeris Engine:** [https://github.com/fringeneering-jpg/Wurral](https://github.com/fringeneering-jpg/Wurral)
- **Jiba Satellite Station-Keeping Engine:** [https://github.com/fringeneering-jpg/Jiba](https://github.com/fringeneering-jpg/Jiba)
- **Master GitHub Repository:** [https://github.com/fringeneering-jpg/phase-wave-cosmology](https://github.com/fringeneering-jpg/phase-wave-cosmology)
- **Permanent Zenodo Archive (DOI):** [https://doi.org/10.5281/zenodo.24281039](https://doi.org/10.5281/zenodo.24281039)
- **Author ORCID:** [https://orcid.org/0009-0005-4121-4296](https://orcid.org/0009-0005-4121-4296)
