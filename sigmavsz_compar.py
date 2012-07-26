#from enviromental import *
import numpy as np
import os as os
from parameters import *
import matplotlib.pyplot as plt
import pz_analisis_plots as pl
import pz_analisis_tools as pt

#Gencat_nonobs............................................
#cat_in_folder = tesi + "photoz/mock.r260.PAU.a005.s1019.111109_CWL_FWHM/compare/bpz_output_faint_interp2/"
#cat_in_folder = tesi + "photoz/mock.r260.PAU.a005.s1019.111109_42NB.100A/BPZ/bright/calibration_errors/polvseusebio/bpz_output_interp8/"
#cat_in_folder = tesi + "photoz/mock.r260.PAU.a005.s1019.111109_42NB.100A/BPZ/bright/calibration_errors/bpz_output/"

#Main.....................................................
sig68 = []
err_sig68 = []

files = os.listdir(cat_in_folder)
shape = len(files)

for name in files:
	
	cat_file = cat_in_folder + name
	print cat_file 
	
	#Reading catalog........................................
	cat_col = np.loadtxt(cat_file, unpack = True)
	
	#z_bpz cut..............................................
	cat_col, n, N = pt.z_cut(cat_col, z_cut) ###Unificar las funciones de corte en una
	#print "Num. gal. after z(photo)<%2.2f cut: %d %1.1f%%" % (z_cut, n , 100 * float(n)/float(N) )
	
	#Seeting dictionary before odds cut......................
	cat_before = pt.dict(cat_col)

	#odds cut...............................................
	cat_col, n, N = pt.odds_cut(cat_col, odds_cut)
	#print "Num. gal. after odds> %2.2f cut: %d %1.1f%%" % (odds_cut, n , 100 * float(n)/float(N) )
	
	#Seeting dictionary.....................................
	cat = pt.dict(cat_col)

	#Defining binning.......................................
	binning = pt.set_binning(cat)
	
	z_bin = pt.c_binning(binning)
	
	sp_y, err_sp_y = pl.plot_syvsz(cat['z_phot'], cat['z_true'], binning, "sigma", "$\sigma$", "$\sigma_{68}$", "z(true)" , sigma_ref)
	
	sig68 = np.append(sig68, sp_y)
	err_sig68 = np.append(err_sig68, err_sp_y)

sig68 = np.reshape(sig68, (shape, -1))
err_sig68 = np.reshape(err_sig68, (shape, -1))

plt.close()

for i in range(len(sig68)): plt.errorbar(z_bin, sig68[i], err_sig68[i], label = files[i])
#for i in range(len(sig68)): plt.plot(z_bin, sig68[i], label = files[i])
plt.rcParams['legend.fontsize'] = 'small'
plt.axhline( y = sigma_ref, linewidth = 1, color = 'red')
plt.xlim(xmin = z_min, xmax = z_max)
plt.ylim(ymin = 0.0, ymax = 0.35)
plt.xlabel("z(true)")
plt.ylabel("$\sigma_{68}$")
plt.legend(loc = 'best')


plt.savefig("sig68vsz_compar.png")
