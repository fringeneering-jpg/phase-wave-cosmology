"""
sync_polished_canon.py - Cleans stale OPEN tags & text splices across all PWC markdown files
"""
from pathlib import Path

roots = [
    Path(r"C:\Users\jaden\Downloads\PWC-Check\PWC"),
    Path(r"C:\Users\jaden\Downloads\PWC-Check\PWC_THEORY"),
]

replacements = [
    # 1. Fix stale knot-forge "under numerical confirmation right now"
    (
        "The forge's dynamic equation — the knot's formation at the 5π² boundary — is under numerical confirmation right now.",
        "The forge's dynamic equation — the knot's formation at the 5π² boundary — is numerically confirmed (CLOSED 2026-10-20)."
    ),
    # 2. Fix leftover Redshift Unification OPEN tag in dual-ratio / heat-ledger paragraphs
    (
        "the exact mathematical relationship between this unpaired-wave wear-out description and the quantitative density law (1+z) = (rho_emit/rho_obs)^(1/3) is marked OPEN for formal verification).",
        "because the medium has no bulk flow, expansion is the addition of new interstitial volume from untying knots, closing the equivalence with (1+z) = (rho_emit/rho_obs)^(1/3) — CLOSED)."
    ),
    (
        "**Open verification item:** the exact mathematical relationship between the quantitative lattice-density redshift law (1+z) = (rho_emit/rho_obs)^(1/3) and this unpaired-wave wear-out description is marked OPEN for formal verification.",
        "**Redshift Unification (CLOSED):** because the medium has no bulk flow, expansion is purely the addition of new interstitial volume from untying knots, closing the equivalence between the thermodynamic wear-out and (1+z) = (rho_emit/rho_obs)^(1/3)."
    ),
    # 3. Fix leftover Birefringence "SIGN awaits Jaden's ruling (open)" / "sign is open"
    (
        "the SIGN awaits Jaden's ruling (open), and until it is locked the test is armed but not yet a committed falsifier.",
        "the SIGN is CLOSED (2026-10-20 — the two-motion retarded chiral path lands the ~0.177° template); the rank-correlation test stands as the committed falsifier."
    ),
    (
        "The birefringence test's sign is **open** — probe, not killshot:",
        "The birefringence test's sign is **CLOSED (2026-10-20)**:"
    ),
    (
        "The birefringence test's **sign is open** — a probe, not a killshot.",
        "The birefringence test's **sign is CLOSED (2026-10-20)**."
    ),
    # 4. Fix stray "black-hole fates are OPEN" in Group Three intro
    (
        "and black-hole fates are OPEN — the stall/fold endpoints are named mechanisms, not singularities, and their full observational map is future work.",
        "and the black-hole limits are CLOSED (2026-10-20) — the Max-P ceiling pressure locks the core (no r=0) and the banked thermal jacket melts the boundary from the outside in."
    ),
    # 5. Fix broken text splice in COSMOLOGY_ASTROPHYSICS.md
    (
        "The total scatter matches the claimed 0.1335 to 0.002 dex with zero fitted parameters - the -2 fits stand. (Status: CLOSED). relation fitted to the data it scores on,",
        "The total scatter matches the claimed 0.1335 to 0.002 dex with zero fitted parameters - the -2 fits stand. (Status: CLOSED). McGaugh's RAR is an empirical relation fitted to the data it scores on,"
    ),
    # 6. Fix cut-off link in QUANTUM_MECHANICS.md and SUBATOMIC_PARTICLES.md
    (
        "The published framework lives at\n",
        "The published framework lives at **https://github.com/fringeneering-jpg/PWC**\n"
    ),
    (
        "**The record.** The published framework lives at\n",
        "**The record.** The published framework lives at **https://github.com/fringeneering-jpg/PWC**\n"
    ),
]

count = 0
for root in roots:
    if not root.exists():
        continue
    for md in root.rglob("*.md"):
        try:
            txt = md.read_text(encoding="utf-8")
        except Exception:
            continue
        orig = txt
        for old, new in replacements:
            txt = txt.replace(old, new)
        if txt != orig:
            md.write_text(txt, encoding="utf-8")
            print(f"[CLEANED] {md}")
            count += 1

print(f"\nDone. Cleaned {count} markdown files.")