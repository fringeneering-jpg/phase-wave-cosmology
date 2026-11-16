"""
sync_no_zeros_field_law.py
1. Replaces stale 'c_loc = 0' / 'drops to zero at the ceiling' with the finite
   Max-P yield floor (C(rho_max) = 954 km/s, C(rho_core) = 72 km/s > 0; close to a stop, never zero).
2. Clarifies the eddy-free floor: zero wound knots/macro-eddies, never dead zero field motion
   (sum-to-ambient chiral-magnetic wibble Omega_amb > 0, because any movement affects the whole field).
3. Wires scripts/navier_stokes_bkm_regularity.py into D34 and Lodgements 1 & 3.
"""
from pathlib import Path

roots = [
    Path(r"C:\Users\jaden\Downloads\PWC-Check\PWC"),
    Path(r"C:\Users\jaden\Downloads\PWC-Check\PWC_THEORY"),
]

replacements = [
    # 1. Replace 'c_loc = 0' and 'drops — to zero at the ceiling' with non-zero Max-P yield cap
    (
        "the complete stop, c_loc = 0 — finite and regular",
        "the near-stop at the Max-P yield cap (c_loc -> C_min > 0, 954 km/s at rho_max, never dead zero) — finite and regular"
    ),
    (
        "this stop — c_loc = 0, finite and regular —",
        "this near-stop — c_loc capped at the finite Max-P yield (954 km/s at rho_max, never zero), finite and regular —"
    ),
    (
        "C(ρ) = √(2Y_bow/ρ) drops — to zero at the ceiling;",
        "C(ρ) = √(2Y_bow/ρ) drops toward the finite Max-P yield cap (954 km/s at ρ_max, 72 km/s at ρ_core — close to a stop relative to c₀, never zero);"
    ),
    (
        "C(ρ) = √(2Y_bow/ρ)\n\ndrops — to zero at the ceiling.",
        "C(ρ) = √(2Y_bow/ρ)\n\ndrops toward the finite Max-P yield cap (954 km/s at ρ_max, 72 km/s at ρ_core — close to a stop relative to c₀, never zero)."
    ),
    (
        "the local wave-speed limit drops — to zero at the ceiling.",
        "the local wave-speed limit drops toward the finite Max-P yield cap (954 km/s at ρ_max, 72 km/s at ρ_core — close to a stop relative to c₀, never zero)."
    ),
    (
        "(C(rho) -> 0 at the ceiling)",
        "(C(rho) -> C_min = 954 km/s at rho_max, capped above zero by mechanical yield)"
    ),
    (
        "(c_loc -> 0)",
        "(c_loc -> C_min > 0 at the Max-P yield cap)"
    ),
    (
        "ending in the Terminal Acoustic Stall (c_loc = 0)",
        "ending in the Terminal Acoustic Stall (c_loc -> C_min > 0 at the Max-P yield cap)"
    ),
    (
        "ending in\nthe Terminal Acoustic Stall (c_loc = 0)",
        "ending in\nthe Terminal Acoustic Stall (c_loc -> C_min > 0 at the Max-P yield cap)"
    ),
    # 2. Update the eddy-free floor so Law 1 (No zeros: sum-to-ambient) is explicit
    (
        "The floor is not a dead ocean; it is a live, perfectly ordered flow with no knots in it.",
        "The floor is not a dead ocean and never hits a literal zero: because P(ρ, s) = (1−s)ρc₀²/3 is a continuous chiral-magnetic field where any movement anywhere ripples through the whole tension network, the unknotted floor idles on the non-zero sum-to-ambient wibble (0 < Ω_ambient ≤ ‖ω‖ ≤ Ω_cavitation < ∞, `scripts/navier_stokes_bkm_regularity.py`) — a live, ordered field with no closed knots in it."
    ),
    # 3. Update D34 in PHASE_WAVE_COSMOLOGY_DERIVATIONS.md with the BKM Operational Middle receipt
    (
        "**Scripts.** scripts/navier_stokes_answer.py; scripts/eddy_free_floor.py; scripts/cavitation_speed_limit.py; scripts/static_medium_check.py",
        "**Scripts.** scripts/navier_stokes_bkm_regularity.py (Beale-Kato-Majda operational-middle proof: 0 < Omega_amb <= ||omega|| <= Omega_cav < oo, cavitation at x_weld = 0.95); scripts/navier_stokes_answer.py; scripts/eddy_free_floor.py; scripts/cavitation_speed_limit.py; scripts/static_medium_check.py"
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
            print(f"[UPDATED] {md}")
            count += 1

print(f"\nDone. Updated {count} markdown files with the non-zero field law & BKM operational middle.")
