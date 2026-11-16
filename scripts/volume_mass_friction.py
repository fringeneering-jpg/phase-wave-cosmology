# Volume-to-mass friction scale: the two speeds of the same rho_max substance
import math
c0 = 2.998e8
rho_max = 1.304e15
Y_bow = 5.93e26
Msun = 1.989e30
rho0 = 8.74e-27

print("== 1. The friction law in volume-to-mass form ==")
Vm_max = 1.0/rho_max
v_wall = math.sqrt(2*Y_bow*Vm_max)
print(f"V/M at Max-P = 1/rho_max = {Vm_max:.4e} m^3/kg")
print(f"v_cav = sqrt(2*Y*V/M):  wall at Max-P -> {v_wall/1e3:.0f} km/s  (RBH-1 anchor 954, EXACT)")
print(f"the wave: the medium's own mode, zero displacement volume -> no 1/2 rho v^2 = Y cap;")
print(f"rides c0 = sqrt(stiffness/inertia).  'Drag on light is the speed cap, not energy loss.'")

print("\n== 2. The same substance, two speeds, one scale ==")
kin_wave = 0.5*rho_max*c0**2
print(f"wave kinetic pressure 1/2 rho_max c0^2 = {kin_wave:.3e} Pa = P_max/2")
print(f"vs Y_bow = {Y_bow:.3e} Pa -> {kin_wave/Y_bow:.1f}x above the wall limit: the wave is")
print(f"not friction-capped because it is not being PUSHED through - it IS the medium spreading.")

print("\n== 3. The tau ladder: the released 3 Msun, if it starts at rho_max ==")
M3 = 3*Msun
R0 = (3*M3/(4*math.pi*rho_max))**(1/3)
tau = 4.68e-3
print(f"3 Msun at rho_max = a ball of radius {R0/1e3:.1f} km")
print(f"R0/c0 = {R0/c0*1e3:.2f} ms  vs measured tau = 4.68 ms")
print(f"c0*tau = {c0*tau/1e3:.0f} km = {c0*tau/R0:.1f}x the initial Max-P radius")
print(f"volume decompression in one tau: {(c0*tau/R0)**3:.0f}x -> V/M(tau) = "
      f"{(c0*tau/R0)**3:.1e} m^3/kg; density falls to rho_max/{(c0*tau/R0)**3:.1f}")
R_rho0 = (3*M3/(4*math.pi*rho0))**(1/3)
print(f"full decompression to rho0: R = {R_rho0/3.0857e16:.0f} pc, "
      f"t = {R_rho0/c0/365.25/86400:.0f} yr at c0")

print("\n== 4. The RCP28 discriminator (for when Jaden pastes it) ==")
print(f"if the RCP28 medium has V/M = 1/rho_max = {Vm_max:.4e} m^3/kg (density "
      f"{rho_max:.4e} kg/m^3), it IS the Max-P (his claim, then checkable against its")
print(f"size/mass).  Core density would be 2.3e17; anything else is a different state.")
