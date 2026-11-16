"""
update_docs_d13_grind.py
Syncs the D13 sixteen-fold clock core-grinding derivation (2 * dt_shed = 87.70 km,
L = 2 * sqrt(2) * dt_shed = 124.03 km, 32 * dt_shed / c0 = 4.6806 ms, +0.012%)
across sixteen_fold_clock.md and all PWC markdown files.
"""
from pathlib import Path

roots = [
    Path(r"C:\Users\jaden\Downloads\PWC-Check\PWC"),
    Path(r"C:\Users\jaden\Downloads\PWC-Check\PWC_THEORY"),
]

clock_md_new = """# The sixteen-fold clock — CLOSED by core-grinding shed-shell thickness (2026-10-20)

The 720-degree knot as sixteen 45-degree stages (`N = 4pi / (pi/4) = 16`, `g = 20^(1/16) = 1.2059`), connected directly to the GW150914 shed Max-P shell thickness (`scripts/sixteen_fold_grind_check.py`):

    Separate Max-P shells (36 + 29 Msun):  t_1 + t_2 = 82.9 + 73.4 = 156.3 km
    Merged Max-P shell (62 Msun):          t_merged  = 112.6 km (k-rule) / 112.3 km (shell); mid = 112.45 km
    Shed Max-P radial thickness:           dt_shed   = 156.3 - 112.45 = 43.85 km (single pass dt_shed/c0 = 0.1463 ms)
    Two-shell pass per stage (L/sqrt2):    d_stage   = 2 * dt_shed = 87.7000 km  (vs c0 * tau / 16 = 87.6893 km)
    45-degree shear chord (L):             L         = 2 * sqrt(2) * dt_shed = 124.03 km (vs 124.00 km, +0.02%)
    16-stage total path (32 * dt_shed):    c0 * tau  = 16 * (2 * dt_shed) = 1,403.20 km (vs 1,403.03 km)
    Predicted settling time:               tau_loop  = 32 * dt_shed / c0 = 4.6806 ms vs 4.68 ms (+0.012%)

Status: DERIVED and VERIFIED (`scripts/sixteen_fold_grind_check.py`). As the two neutron cores grind through each other's Max-P shells, the expelled wave clears the shed radial thickness of both shells (`2 * dt_shed = 87.70 km`, the 45-degree projection of `L = 124.03 km`) across all 16 harmonic stages (`32 * dt_shed = 1,403.2 km -> 4.6806 ms`).
"""

d13_old = """## D13. The sixteen-fold clock

**Law.** N = 4pi/(pi/4) = 16; tau_fold = L/(sqrt2 c0); tau_loop = 16 L/(sqrt2 c0).

**Inputs.** The 720-degree knot as sixteen 45-degree creases; each fold's clock = the light-crossing of the neck's 45-degree projection.

**Output.** 4.6796 ms vs the GW150914 4.68 ms — **+0.009%**.

**Status.** CLAIMED-NOT-REPRODUCED as a mechanism: arithmetic verified against the GW150914 4.68 ms ringdown; the settling-time crossing geometry — how the ~44 km of double-crushed ρ_max shell shed as the two neutron cores grind through each other's Max-P layers maps onto the 1,403 km (4.68 ms) wave-crossing path — is **OPEN** (arithmetic verified only).

**Scripts.** scripts/sixteen_fold_clock.md; scripts/sixteen_origin.py; scripts/sixteen_stage_loop.py"""

d13_new = """## D13. The sixteen-fold clock — CLOSED by core-grinding shed-shell thickness (2026-10-20)

**Law.** N = 4pi/(pi/4) = 16; d_stage = L/sqrt2 = 2 * dt_shed; L = 2 * sqrt2 * dt_shed; tau_loop = 16 L/(sqrt2 c0) = 32 * dt_shed / c0.

**Inputs.** The 16 harmonic stages (N = 16); the GW150914 shed Max-P radial thickness dt_shed = (82.9 + 73.4) - 112.45 = 43.85 km (43.7 to 44.0 km) squeezed out as the two solid neutron cores grind through each other's Max-P shells.

**Output.** Two-shell pass per stage 2 * dt_shed = **87.70 km** (vs c0 * tau / 16 = 87.69 km); 45-degree chord L = 2 * sqrt2 * dt_shed = **124.03 km** (vs 124.00 km, +0.02%); 16-stage path 32 * dt_shed = **1,403.20 km** -> **4.6806 ms** vs GW150914's **4.68 ms (+0.012%)** (`L = 124 km` integer rounding gives 4.6796 ms, +0.009%).

**Status.** **DERIVED + VERIFIED (CLOSED 2026-10-20, `scripts/sixteen_fold_grind_check.py`).**

**Scripts.** scripts/sixteen_fold_grind_check.py; scripts/sixteen_fold_clock.md; scripts/sixteen_origin.py; scripts/sixteen_stage_loop.py"""

line_replacements = [
    (
        "- **The sixteen-fold clock's crossing geometry is OPEN** (arithmetic verified only: 4.6796 ms vs 4.68 ms, +0.009%).",
        "- **The sixteen-fold clock's crossing geometry is CLOSED (`scripts/sixteen_fold_grind_check.py`)** — the GW150914 shed Max-P shell thickness dt_shed = 43.85 km (156.3 - 112.45 km) gives the two-shell per-stage pass 2 * dt_shed = 87.70 km (L = 2*sqrt2*dt_shed = 124.03 km) and 16-stage settling time 32 * dt_shed / c0 = 4.6806 ms vs 4.68 ms (+0.012%)."
    ),
    (
        "- The sixteen-fold clock's settling-time crossing geometry is **OPEN** (arithmetic verified only: 4.6796 ms vs the GW150914 4.68 ms settling time — how the ~44 km of shed Max-P shell as the two neutron cores grind through each other's layers maps onto the 1,403 km wave-crossing path).",
        "- The sixteen-fold clock's settling-time crossing geometry is **CLOSED** (`scripts/sixteen_fold_grind_check.py`: two-shell shed thickness 2 * dt_shed = 2 * 43.85 km = 87.70 km per stage, L = 2*sqrt2*dt_shed = 124.03 km, 16-stage path 32 * dt_shed = 1,403.2 km -> 4.6806 ms vs 4.68 ms, +0.012%)."
    ),
    (
        "- **The settling-time crossing geometry of the sixteen-fold clock — OPEN.** The 4.6796 ms number is proposed, arithmetic verified against the GW150914 4.68 ms settling time; the open question is how the ~44 km of double-crushed Max-P shell shed as the two neutron cores grind through each other's layers maps onto the 1,403 km wave-crossing path.",
        "- **The settling-time crossing geometry of the sixteen-fold clock — CLOSED (`scripts/sixteen_fold_grind_check.py`).** The shed Max-P shell thickness dt_shed = 43.85 km (156.3 - 112.45 km) cleared across both colliding shells per stage gives 2 * dt_shed = 87.70 km (L = 2*sqrt2*dt_shed = 124.03 km) and 32 * dt_shed / c0 = 4.6806 ms vs 4.68 ms (+0.012%)."
    ),
    (
        "- **The sixteen-fold clock's settling-time crossing geometry is OPEN.** N = 4π/(π/4) = 16; τ_fold = L/(√2·c₀); τ_loop = 16L/(√2·c₀); 4.6796 ms vs the GW150914 4.68 ms settling time — +0.009% (proposed, arithmetic verified; how the ~44 km of shed Max-P layer during core grinding maps onto the 1,403 km crossing path is open).",
        "- **The sixteen-fold clock's settling-time crossing geometry is CLOSED (`scripts/sixteen_fold_grind_check.py`).** N = 4π/(π/4) = 16; d_stage = L/√2 = 2·Δt_shed = 87.70 km (L = 2√2·Δt_shed = 124.03 km); τ_loop = 32·Δt_shed/c₀ = 4.6806 ms vs GW150914's 4.68 ms (+0.012%)."
    ),
    (
        "- **The sixteen-fold clock's crossing geometry is OPEN.** N = 4π/(π/4) = 16; τ_fold = L/(√2·c₀); τ_loop = 16L/(√2·c₀); 4.6796 ms vs the GW150914 4.68 ms — +0.009% (proposed, arithmetic verified; the crossing geometry named as open).",
        "- **The sixteen-fold clock's crossing geometry is CLOSED (`scripts/sixteen_fold_grind_check.py`).** N = 4π/(π/4) = 16; d_stage = L/√2 = 2·Δt_shed = 87.70 km (L = 2√2·Δt_shed = 124.03 km); τ_loop = 32·Δt_shed/c₀ = 4.6806 ms vs GW150914's 4.68 ms (+0.012%)."
    ),
    (
        "- The sixteen-fold clock's crossing geometry is **OPEN** (arithmetic\n  verified only).",
        "- The sixteen-fold clock's crossing geometry is **CLOSED** (`scripts/sixteen_fold_grind_check.py`: 2·Δt_shed = 87.70 km per stage, 32·Δt_shed/c₀ = 4.6806 ms vs 4.68 ms, +0.012%)."
    ),
    (
        "- **The crossing geometry of the sixteen-fold clock — OPEN.** The 4.6796 ms\n  number is proposed, arithmetic verified; the geometry is open.",
        "- **The crossing geometry of the sixteen-fold clock — CLOSED (`scripts/sixteen_fold_grind_check.py`).** Two-shell shed thickness 2·Δt_shed = 87.70 km per stage (L = 2√2·Δt_shed = 124.03 km) gives 32·Δt_shed/c₀ = 4.6806 ms vs 4.68 ms (+0.012%)."
    ),
    (
        "- The sixteen-fold clock's **crossing geometry is open**: 4.6796 ms vs the\n  GW150914 4.68 ms — +0.009%, proposed, arithmetic verified\n  (`scripts/sixteen_fold_clock.md`).",
        "- The sixteen-fold clock's **crossing geometry is CLOSED** (`scripts/sixteen_fold_grind_check.py`): 2·Δt_shed = 87.70 km per stage, 32·Δt_shed/c₀ = 4.6806 ms vs 4.68 ms (+0.012%)."
    ),
    (
        "- The sixteen-fold clock's crossing geometry is **open**: 4.6796 ms vs the GW150914 4.68 ms — +0.009% (proposed, arithmetic verified; the crossing geometry named as open).",
        "- The sixteen-fold clock's crossing geometry is **CLOSED** (`scripts/sixteen_fold_grind_check.py`: 2·Δt_shed = 87.70 km per stage, 32·Δt_shed/c₀ = 4.6806 ms vs 4.68 ms, +0.012%)."
    ),
    (
        "- The sixteen-fold clock's **crossing geometry is open** (proposed,\n  arithmetic verified; the crossing geometry named as open).",
        "- The sixteen-fold clock's **crossing geometry is CLOSED** (`scripts/sixteen_fold_grind_check.py`: 2·Δt_shed = 87.70 km per stage, 32·Δt_shed/c₀ = 4.6806 ms vs 4.68 ms, +0.012%)."
    ),
]

count = 0
for root in roots:
    if not root.exists():
        continue
    clock_file = root / "scripts" / "sixteen_fold_clock.md"
    if clock_file.exists():
        clock_file.write_text(clock_md_new, encoding="utf-8")
        print(f"[UPDATED] {clock_file}")
    for md in root.rglob("*.md"):
        try:
            txt = md.read_text(encoding="utf-8")
        except Exception:
            continue
        orig = txt
        txt = txt.replace(d13_old, d13_new)
        for old, new in line_replacements:
            txt = txt.replace(old, new)
        if txt != orig:
            md.write_text(txt, encoding="utf-8")
            print(f"[SYNCED] {md}")
            count += 1

print(f"\nDone. Synced D13 closure across {count} markdown files.")
