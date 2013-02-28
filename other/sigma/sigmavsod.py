import numpy as np
import pz_analisis_tools as pt
import matplotlib.pyplot as plt

#Gencat_nonobs............................................
cat_file = "des_auto_bpz.bpz"

#Main.....................................................
cat = np.loadtxt(cat_file, usecols = (1,5,9), unpack = True)

zp = cat[0]
zs = cat[2]
od = cat[1]
dz = zs - zp

print zp, zs, od

binning = np.arange(0,1.01,0.05)
c_od = pt.c_binning(binning)
n_bin = len(binning) - 1 

sig68 = np.zeros(n_bin)
std = np.zeros(n_bin)

for i in range(n_bin):
	mask = (od > binning[i]) & (od < 1.0)
	x = np.compress(mask, dz)
	sig68[i] = pt.Sigma68(x)
	std[i] = np.std(x)

plt.plot(od, dz, 'o', color = 'black', markersize = 2)
plt.plot(c_od, sig68, 'g', linewidth = 2, label = '$\sigma_{68}$')
plt.plot(c_od, std, 'b', linewidth = 2, label = 'RMS')
plt.axhline(y = 0, linestyle = 'dashed', linewidth = 1, color = 'red')
plt.xlabel("odds")
plt.ylabel("$\Delta z$")
plt.ylim(ymax = 0.5, ymin = -0.5)
plt.xlim(xmax = 0., xmin = 1.)
plt.legend(loc = 'lower right')

plt.savefig("/Users/pmarti/Desktop/sigvsodds.png")
