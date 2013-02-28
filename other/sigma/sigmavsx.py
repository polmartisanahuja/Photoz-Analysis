import numpy as np
import pz_analisis_tools as pt
import matplotlib.pyplot as plt

#Gencat_nonobs............................................
cat_file = "mock.r260.n1e6.s10.121027_42NB.100A_lump_dx1_noisy_i22.5_nonobs.bpz"
#cat_file = "mock.r260.n1e6.s10.121027_42NB.100A_noisy_i22.5.bpz"

#Main.....................................................
cat = np.loadtxt(cat_file, unpack = True)

zp = cat[1]
zs = cat[9]
od = cat[5]
m = cat[10]
dz = zp - zs

ax = m 
ax_label = 'mag'

print zp, zs, od, m

plt.plot(ax, dz, 'o', color = 'black', markersize = 2)

#binning = np.arange(0,1.01,0.05)
binning = np.arange(14,22.5,0.5)
c_bin = pt.c_binning(binning)
n_bin = len(binning) - 1 

sig68 = np.zeros(n_bin)
std = np.zeros(n_bin)

for i in range(n_bin):
	mask = (ax > binning[i]) & (ax < binning[i+1])
	#mask = (ax > binning[i]) & (ax < binning[-1])
	x = np.compress(mask, dz)
	sig68[i] = pt.Sigma68(x)
	std[i] = np.std(x)

np.savetxt('/Users/pmarti/Desktop/sigvs' + ax_label + '.txt', np.array([c_bin, sig68, std]).T)

plt.plot(c_bin, sig68, 'g', linewidth = 2, label = '$\sigma_{68}$')
plt.plot(c_bin, std, 'b', linewidth = 2, label = 'RMS')
plt.axhline(y = 0, linestyle = 'dashed', linewidth = 1, color = 'red')
plt.xlabel(ax_label)
plt.ylabel("$\Delta z$")
#plt.ylim(ymax = 0.2, ymin = -0.2)
plt.legend(loc = 'best')

plt.savefig("/Users/pmarti/Desktop/sigvs" + ax_label + ".png")
