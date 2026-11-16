import astropy.units as u
from sunpy.net import Fido, attrs as a
res = Fido.search(a.Time("2014-10-22T00:00:00", "2014-10-22T00:15:00"),
                  a.Instrument.aia, a.Wavelength(94*u.angstrom))
for i in range(min(3, len(res[0]))):
    row = res[0][i]
    print(i, row["Start Time"], row["url"])
