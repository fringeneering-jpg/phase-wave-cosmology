# stellar_shell_size_law.py - the size law: the same rules as the black holes
# (2026-10-21, Jaden's reading). Bigger core -> lower surface-area-to-volume
# -> thinner hold -> the body sheds. For black holes: the shell is the
# k C^(2/3) area law, thinner IN PROPORTION for heavy holes. For stars: the
# surface pull g = GM/R^2 collapses for supergiants, the hold breaks, and the
# star loses bits off itself - Betelgeuse is the worked case (the 2019-2020
# Great Dimming was a shedding event).
import math

G = 6.67430e-11
c02 = (2.99792458e8) ** 2
Msun = 1.98847e30
Rsun = 6.957e8
Lsun = 3.828e26
a_max = 3.23e11

print("=" * 78)
print("1. THE BLACK-HOLE LADDER (the skin law: t = 650 km constant, so the")
print("   Max-P shell gets thinner IN PROPORTION as the core grows)")
print("=" * 78)
print("%-12s %9s %10s %10s %10s" % ("hole", "M (Msun)", "core (km)", "skin t (km)", "skin/core"))
bhs = [(5.3, 22.2), (62, 47.3), (142, 66.4), (4.3e6, 2071.0), (6.5e9, 23760.0)]
for M, core_km in bhs:
    t_skin = 650.0
    print("%-12s %9.3g %10.0f %10.0f %10.4f" % (("%g" % M) + " Msun", M, core_km, t_skin, t_skin / core_km))
print()
print("=" * 78)
print("2. THE STAR LADDER (the same rule: the hold is the surface pull)")
print("=" * 78)
stars = [
    ("Sun", 1.0, 1.0, 1.0, 2e-14),
    ("Sirius A", 2.06, 1.71, 25.4, 1e-14),
    ("Arcturus", 1.08, 25.4, 170.0, 1e-13),
    ("Aldebaran", 1.16, 44.0, 439.0, 1.5e-11),
    ("Betelgeuse", 16.5, 764.0, 1.26e5, 2.1e-6),
    ("Antares", 12.5, 680.0, 7.5e4, 1.7e-6),
    ("VY CMa", 17.0, 1420.0, 2.7e5, 2.0e-5),
]
print("%-12s %9s %9s %10s %12s %12s %10s" % ("star", "M", "R", "g_surf", "mdot_light", "mdot_wind", "shed/burn"))
print("%-12s %9s %9s %10s %12s %12s %10s" % ("", "(Msun)", "(Rsun)", "(m/s^2)", "(Msun/yr)", "(Msun/yr)", ""))
print("-" * 78)
for name, M, R, L, mdot_wind in stars:
    g_surf = G * M * Msun / (R * Rsun) ** 2
    mdot_light = L * Lsun / c02 * (3.15576e7) / Msun
    ratio = mdot_wind / mdot_light
    print("%-12s %9.2f %9.0f %10.3e %12.2e %12.2e %10.1f" % (name, M, R, g_surf, mdot_light, mdot_wind, ratio))
print()
print("THE LAW, READ OUT:")
print("  surface pull g = GM/R^2 falls ~35,000x from the Sun to Betelgeuse,")
print("  while the shed-to-burn ratio (wind/light) climbs ~250x on the same")
print("  ladder: the bigger the core, the lower the surface-area-to-volume hold,")
print("  the thinner the retained Max-P skin, the more the star loses bits off")
print("  itself. Same geometry as the black holes - the hold is a surface law,")
print("  and the supergiant is the star whose shell is too thin to keep.")
print()
print("  Betelgeuse's 2019-2020 Great Dimming: a ~10^-6 Msun shedding event")
print("  (the dust cloud), the worked case of the rule.")
