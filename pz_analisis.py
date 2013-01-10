import numpy as np
import pz_analisis_plots as pl
import pz_analisis_tools as pt
import pweave as pw
import os as os
from parameters import *

#Reading catalog........................................
cat_col = np.loadtxt(cat_file, unpack = True)
if (qual_para == 'PDZbest'): cat_col[odds_col] = cat_col[odds_col]  

#z_bpz cut..............................................
#cat_col, n, N = pt.z_cut(cat_col, z_cut) ###Unificar las funciones de corte en una
#print "Num. gal. after z(photo)<%2.2f cut: %d %1.1f%%" % (z_cut, n , 100 * float(n)/float(N) )

#Seeting dictionary before odds cut......................
#cat_before = pt.dict_annz(cat_col)
#cat_before = pt.dict(cat_col)

#odds cut...............................................
#cat_col, n, N = pt.errz_cut(cat_col, errz_cut)
#cat_col, n, N = pt.odds_cut(cat_col, odds_cut)
#print "Num. gal. after odds> %2.2f cut: %d %1.1f%%" % (odds_cut, n , 100 * float(n)/float(N) )

#Seeting dictionary.....................................
#cat = pt.dict_annz(cat_col)
cat = pt.dict(cat_col)

#Defining binning.......................................
binning = pt.set_binning(cat)
#errz_binning = np.arange(0., 0.1, 0.01)
#print binning

#MAIN...................................................
os.system("mkdir plots")

#zz = np.array([cat['z_phot'], cat['z_true']])
#np.savetxt("zpvszs.txt", zz.T, fmt = '%f' )

#pl.plot_zvsz(cat['z_phot'], cat['z_true'], binning, z_min, z_max)
#pl.plot_dzvserrz(cat_before, cat, binning, Dz_range, z_min, z_max)
#pl.plot_dzvsodds(cat_before, cat, binning, Dz_range, z_min, z_max, qual_para, od_bin)
#pl.plot_histo_nvsz(cat['z_phot'], cat['z_true'], binning)
#pl.plot_dzvsz(cat['z_phot'], cat['z_true'], z_min, z_max, Dz_range)
pl.plot_biasvsz(cat['z_phot'], cat['z_true'], binning, Dz_range)
pl.plot_sigmavsz(cat['z_phot'], cat['z_true'], binning)
pl.plot_outliersvsz(cat['z_phot'], cat['z_true'], binning, 2, outliers2_ref)
pl.plot_outliersvsz(cat['z_phot'], cat['z_true'], binning, 3, outliers3_ref)
#pl.plot_histo_dzvsz(cat['z_phot'], cat['err_z_phot'], cat['z_true'])
