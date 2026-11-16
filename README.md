# Phase Wave Cosmology (PWC): A Placeholder-Free Electromagnetic Continuum Framework

**„Die Trägheit eines Körpers ist absolut von seinem Energiegehalt abhängig“**  
*(The inertia of a body is absolutely dependent upon the content of its energy)*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24281039.svg)](https://doi.org/10.5281/zenodo.24281039)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0005--4121--4296-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0009-0005-4121-4296)
[![Manuscript License: CC BY-SA 4.0](https://img.shields.io/badge/Manuscript-CC%20BY--SA%204.0-lightgrey.svg)](./LICENSE-PAPER)
[![Code License: AGPLv3 + Commercial](https://img.shields.io/badge/Code-GNU%20AGPLv3%20%2B%20Commercial-blue.svg)](./LICENSE)

- **Master Preprint (Zenodo DOI):** [https://doi.org/10.5281/zenodo.24281039](https://doi.org/10.5281/zenodo.24281039)
- **Author:** Jaden John Allison — Phase Wave Cosmology Collaboration / Fringeneering ([ORCID: 0009-0005-4121-4296](https://orcid.org/0009-0005-4121-4296))
- **Companion Operational Engines:**
  - [**Wurral Astrodynamics Engine**](https://github.com/fringeneering-jpg/wurral) — 15-body relativistic 1PN EIH + Moyer deep-space propagator (50-year unpinned planetary & Cassini telemetry without empirical Kuiper fudge rings)
  - [**Jiba Station-Keeping Engine**](https://github.com/fringeneering-jpg/jiba) — Near-Earth satellite orbital station-keeping & ILRS laser telemetry engine ($99.8\%$ reduction in unmodeled LARES orbital drift across 1,500 days)

---

## Overview

This repository houses the complete 136-page master manuscript ([`Phase_Wave_Cosmology_v1.0.pdf`](./Phase_Wave_Cosmology_v1.0.pdf)), full LaTeX source ([`paper_clean.tex`](./paper_clean.tex)), three domain-specific specialist briefing packages ([`briefings/`](./briefings/)), and the complete suite of zero-free-parameter Python verification scripts ([`scripts/`](./scripts/)).

**Phase Wave Cosmology (PWC)** substantiates physical space as a continuous, compressible electromagnetic plenum governed by the operational principles that **"PRESSURE, GEOMETRY AND DENSITY AFFECT ENERGY"** and **"heat hates pressure"**, enacting the ontological restoration $m = L/c_0^2$ (radiation energy as primary baseline; inertial mass as confined wave energy) across 41 orders of magnitude without dark matter halos, dark energy ($\Lambda \equiv 0$), point particles, or central singularities:

| Locked Continuum Constant | Symbol / Identity | Value |
| :--- | :--- | :--- |
| Ambient Plenum Rest Density | $\rho_0$ | $8.74 \times 10^{-27}\text{ kg/m}^3$ |
| Ambient Electromagnetic Wave Speed | $c_0 = 1/\sqrt{\mu_0\varepsilon_0}$ | $2.99792458 \times 10^8\text{ m/s}$ |
| Maximum Acoustic Yield Ceiling | $\rho_{\max}$ | $1.3040143 \times 10^{15}\text{ kg/m}^3$ |
| Universal Cosmic Untying Rate | $H_0 = \frac{\rho_0 c_0}{\rho_{\max} R_p}$ | $2.39607 \times 10^{-18}\text{ s}^{-1}$ ($73.935\text{ km/s/Mpc}$) |
| Terminal Galactic Acceleration Floor | $a_0 = \frac{c_0 H_0}{2\pi}$ | $1.1432 \times 10^{-10}\text{ m/s}^2$ |

### Manuscript Architecture (136 Pages)
1. **Section 1 — Albert Einstein:** Mass-energy continuum ($m = L/c_0^2$), the 1920 Leiden ether address, expanding-track $49/51$ round-trip light-time split, Viking 1/2 dual-transponder range biases, and the JWST high-$z$ assembly window (`JADES-GS-z14-0`: $2,004.6\text{ Myr}$, $6.91\times \Lambda\text{CDM}$).
2. **Section 2 — Dr. John D. Anderson:** The Master Equation of State ($H(r) = H_0\sqrt{1 - r_s/r}$), Eisenhart metric lift, unmasking ephemeris-absorbed expansion in $GM$, resolution of the 5 solar-system anomalies (AU drift, Pioneer 10/11, Ulysses polar chimney, `'Oumuamua`, Lagrange saddle floor), and 5/5 Earth flyby jump closures.
3. **Section 3 — Lord Ernest Rutherford:** Continuous subatomic mechanics, real-space neutron doublet closure ($+0.78233\text{ MeV}$ split, $\mu_n$, beam-vs-bottle lifetime resolution), Penning trap cyclotron clock-rate bias ($+1.0817\text{ MeV}$ surface dress, $169/170$ internal seam relief), and the light-nuclei weld ladder ($Q_{\text{weld}} = 91.8462\text{ keV}$).
4. **Section 4 — Dr. John Williamson & Quicycle Mechanics:** The electron as a $720^\circ$ toroidal chiral knot ($19:1:18$ force balance), sealed 5-knot $2\text{-}1\text{-}2$ proton cage ($m_p R_p c_0 = 4\hbar$, $R_p = 0.8422\text{ fm}$), and the closed-form subatomic ledger (Table 7).
5. **Section 5 — Stacy McGaugh & Mordehai Milgrom:** Zero-fit derivation of $a_0 = c_0 H_0 / (2\pi)$, $+24.313\%$ phonon decompression bloom, 4-for-4 out-of-sample galactic rotation sweep across 1,770 galaxies (`PROBES`, `ALFALFA`, `GHASP`, `LITTLE THINGS`) retiring 5 standard fitting parameters, Bullet Cluster bow-shock & lensing closure, and singularity-free black hole shells (`GW150914` $3.0\,M_\odot$ yield & 16-fold ringdown).
6. **Section 6 — Maxwell, Faraday, Riemann, Aristotle:** Physical electromagnetic medium mechanics, proof of Aristotle's void limit, exact $3 \times (1/3) = 1$ hydrostatic gravitational redshift cancellation, and constitutive 2-anchor polytrope Equation of State.
7. **Section 7 — Empirical Software & Telemetry Engines:** Full benchmarking of [**Wurral**](https://github.com/fringeneering-jpg/wurral) (1978–2026 planetary & Cassini range telemetry) and [**Jiba**](https://github.com/fringeneering-jpg/jiba) (thrusterless LEO/MEO station-keeping across 6 ILRS geodetic satellites).
8. **Section 8 — Cosmology, Gapless Continuum Axioms & Empirical Predictions:** Seven Gapless Physical Laws, Navier–Stokes regularity and Yang–Mills mass gap bounds, Type Ia supernova deceleration parameter $q_0 = -9/19 = -0.4737$ ($\Lambda \equiv 0$, DES 5-Year $0.27\sigma$ match), $^7\text{Li}$ Spite plateau closure, and the 23-test Master Falsification Matrix.
9. **Section 9 — Appendix:** Standalone Python 3 Standard Library verification suite.

---

## Specialist Briefing Packages ([`briefings/`](./briefings/))

For domain-focused technical review, three self-contained PDF briefings (sliced directly from the locked master PDF with full bibliography and paired verification scripts) are provided in [`briefings/`](./briefings/):

| Package Directory | Briefing PDF | Pages | Included Sections | Bundled Verification Scripts |
| :--- | :--- | :---: | :--- | :--- |
| [`briefings/01_Quicycle_Subatomic/`](./briefings/01_Quicycle_Subatomic/) | [`PWC_Briefing_01_Subatomic_Quicycle.pdf`](./briefings/01_Quicycle_Subatomic/PWC_Briefing_01_Subatomic_Quicycle.pdf) | 21 | Title/Abstract, Sec 3, Sec 4 (incl. Table 7), References | `pwc_neutron.py`, `proton_electron_ledger.py` |
| [`briefings/02_McGaugh_Galactic_RAR/`](./briefings/02_McGaugh_Galactic_RAR/) | [`PWC_Briefing_02_Galactic_RAR_and_Wurral.pdf`](./briefings/02_McGaugh_Galactic_RAR/PWC_Briefing_02_Galactic_RAR_and_Wurral.pdf) | 45 | Title/Abstract, Sec 5, Sec 7, References | `run_all_rotation_catalogs_new_a0.py`, `astrodynamic_anomalies_anderson.py` |
| [`briefings/03_Astrodynamics_Cosmology/`](./briefings/03_Astrodynamics_Cosmology/) | [`PWC_Briefing_03_Astrodynamics_and_Cosmology.pdf`](./briefings/03_Astrodynamics_Cosmology/PWC_Briefing_03_Astrodynamics_and_Cosmology.pdf) | 76 | Title/Abstract, Sec 1, Sec 2, Sec 7, Sec 8 (incl. Table 25), References | `unmask_entropic_gravity_and_dark_energy_kill.py`, `treadmill_49_51.py` |

---

## Running the Zero-Parameter Verification Scripts

All core analytical verification scripts execute deterministically under standard **Python 3.10+** with **zero adjustable fitting parameters**. The eight Appendix scripts require only the **Python Standard Library** (`math`, `sys`):

```bash
# Section 1: Expanding-track 49/51 light-time split, Viking 1/2 biases & JWST chronometer
python scripts/treadmill_49_51.py

# Section 2: Master Anderson EOS & the 5 solar-system astrodynamic anomalies
python scripts/astrodynamic_anomalies_anderson.py

# Section 3: Rutherford real-space neutron doublet & 7/3 geometric magnetic moment
python scripts/pwc_neutron.py

# Section 5: Binary black hole merger neck yield (GW150914) & 16-fold harmonic ringdown
python scripts/merger_neck_yield.py
python scripts/sixteen_fold_grind_check.py

# Section 6: Master 2-anchor polytrope EOS & "heat hates pressure" 28/19 speed-up law
python scripts/universal_eos.py
python scripts/heat_hates_pressure.py

# Section 8: Unmasking entropic gravity, q0 = -9/19 & Dark Energy elimination (Lambda = 0)
python scripts/unmask_entropic_gravity_and_dark_energy_kill.py
```

To run the specialist briefing copies (which also print the DOI and companion repository verification ledger):

```bash
python briefings/01_Quicycle_Subatomic/pwc_neutron.py
python briefings/02_McGaugh_Galactic_RAR/astrodynamic_anomalies_anderson.py
python briefings/03_Astrodynamics_Cosmology/unmask_entropic_gravity_and_dark_energy_kill.py
python briefings/03_Astrodynamics_Cosmology/treadmill_49_51.py
```

*(Note: Catalog-ingestion scripts in `scripts/` that process external astronomical survey tables such as SPARC/PROBES/ALFALFA use `numpy` and `pandas`.)*

### Recompiling the LaTeX Manuscript
To build [`Phase_Wave_Cosmology_v1.0.pdf`](./Phase_Wave_Cosmology_v1.0.pdf) from [`paper_clean.tex`](./paper_clean.tex) using TeX Live or MiKTeX:

```bash
pdflatex -interaction=nonstopmode -file-line-error paper_clean.tex
pdflatex -interaction=nonstopmode -file-line-error paper_clean.tex
```

---

## Repository Structure

```text
phase-wave-cosmology/
├── Phase_Wave_Cosmology_v1.0.pdf   # Locked 136-page master manuscript
├── paper_clean.tex                 # Complete LaTeX source (zero margin overflows)
├── briefings/                      # 3 domain-specific specialist briefing packages
│   ├── 01_Quicycle_Subatomic/
│   ├── 02_McGaugh_Galactic_RAR/
│   └── 03_Astrodynamics_Cosmology/
├── scripts/                        # Master archive of Python verification & derivation scripts
├── LICENSE                         # GNU AGPLv3 + Commercial Dual License (for all code/scripts)
├── LICENSE-PAPER                   # CC BY-SA 4.0 International License (for manuscript/docs)
└── README.md
```

---

## Dual Licensing

This repository is distributed under a strict split license separating the scientific text from executable software and simulation code:

1. **Manuscript, Specialist Briefings & Documentation ([`LICENSE-PAPER`](./LICENSE-PAPER)):**  
   `Phase_Wave_Cosmology_v1.0.pdf`, `paper_clean.tex`, `briefings/**/*.pdf`, and `README.md` are licensed under the **Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)**.
2. **Verification Scripts & Simulation Engines ([`LICENSE`](./LICENSE)):**  
   All Python scripts (`scripts/**/*.py`, `briefings/**/*.py`) and companion simulation engines ([Wurral](https://github.com/fringeneering-jpg/wurral) and [Jiba](https://github.com/fringeneering-jpg/jiba)) are dual-licensed under the **GNU Affero General Public License v3.0 (GNU AGPLv3)** for open-source/academic research and a separate **Fringeneering Commercial License** for closed-source, proprietary aerospace, satellite constellation, or operational telemetry deployment. Commercial inquiries: `fringeneering@gmail.com`.

---

## Citation

```bibtex
@article{Allison2026PWC,
  author       = {Allison, Jaden John},
  title        = {Die Tr{\"a}gheit eines K{\"o}rpers ist absolut von seinem Energiegehalt abh{\"a}ngig --- Phase Wave Cosmology: A Placeholder-Free Electromagnetic Continuum Framework},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.24281039},
  url          = {https://doi.org/10.5281/zenodo.24281039},
  note         = {Code and verification suite: https://github.com/fringeneering-jpg/phase-wave-cosmology}
}
```
