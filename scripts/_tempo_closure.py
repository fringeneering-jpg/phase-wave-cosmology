s = 1.0/19.0
T = 3**3
mult = s*(1+T)
ratio_obs = 380.0/258.0
print("T = 3^3 =", T)
print("s(1+T) = 28/19 =", 28.0/19.0)
print("observed tempo ratio 380/258 =", ratio_obs)
print("match: %+.4f%%" % (100*(28.0/19.0/ratio_obs - 1)))
print("implied LSS tempo time: 380 / (28/19) = %.3f kyr  (vs 258 kyr)" % (380.0/(28.0/19.0)))
print("T demanded by the peak: %.2f" % (ratio_obs*19 - 1))
