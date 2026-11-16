# Integrate the "Refining Black Hole Shell Density" chat with the V/M friction scale
import math
c0 = 2.998e8
rho_max = 1.304e15
Y = 5.93e26
Msun = 1.989e30

print("== Chat numbers re-verified ==")
V_shed = 3*Msun/rho_max
print(f"shed volume 3 Msun at rho_max = {V_shed:.3e} m^3  (chat: 4.57e15)")
print(f"rho_max from the shell: 10.87 Msun / (4pi/3)(159.6^3-47.3^3) km^3 = "
      f"{10.87*Msun/((4*math.pi/3)*((159.6e3)**3-(47.3e3)**3)):.4e}  (chat: 1.304e15)")

print("\n== The dropped ambient floor: x = 10 kg/cm^3 = 1e7 kg/m^3 ==")
x = 1.0e7
V_exp = V_shed*(rho_max/x)
R_exp = (3*V_exp/(4*math.pi))**(1/3)
t_exp = R_exp/c0
print(f"expansion volume = 4.57e15 * (1.304e15/1e7) = {V_exp:.3e} m^3")
print(f"sphere radius = {R_exp/1e3:,.0f} km ; at c0: t = {t_exp:.3f} s  <- Jaden's 0.2 s pulse width")
rho_tau = rho_max/((c0*4.68e-3/103e3)**3)
print(f"at the ringdown tau = 4.68 ms: R = 1,403 km, rho = {rho_tau:.3e} (2,528x decompressed)")

print("\n== The V/M friction timeline (the scale he asked for) ==")
rows = [("t=0 (ringdown start, held Max-P)", 103e3, 1.0/rho_max, "954 km/s (held)"),
        ("t = tau = 4.68 ms", 1403e3, 1.94e-12, "0.16 c0 if held"),
        ("t = 0.17 s (ambient floor 1e7)", 5.22e7, 1.0/x, ">= c0: friction dissolved")]
for lab, R, Vm, cap in rows:
    vcap = math.sqrt(2*Y*Vm)/c0
    print(f"  {lab:38s} R={R/1e3:>9,.0f} km  V/M={Vm:.2e} m^3/kg  cap={cap}")
print(f"the wave rides c0 the whole time (free); V/M grows 1.304e8x and the friction cap")
print(f"rises from 954 km/s to c0 - the decompression IS the friction dissolving.")

print("\n== Chat's own claim, now on the scale ==")
print('chat line 544: "the structural tension ... violently snapped it back to ambient density')
print('(10 kg/cm^3). The resistance scaling dictates the speed and force of that expansion."')
print("-> speed = c0 (free wave); the 'force' = the cap the held state would face; the")
print("ambient floor x is the ONE input the chat left isolated algebraically (lines 920-926),")
print("the number that got dropped from the framework (framework ambient = rho0 = 8.74e-27, 34")
print("orders lower; the chat's 1e7 is a LOCAL post-hole density, not the cosmological rest).")
