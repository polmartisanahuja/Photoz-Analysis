#!/usr/bin/env python
# encoding: UTF8
#import yaml
import numpy as np
import tools as tls 
import matplotlib.pylab as plt
import pz_tools as pztls
import matplotlib.gridspec as gridspec
#from slaq_parameters_analyz import *
from pau_bright_parameters_analyz import *
#from pau_faint_parameters_analyz import *
from matplotlib.ticker import MaxNLocator
import textwrap
from matplotlib import rc

rc('text', usetex=True)
rc('font', family='serif')

print "\n"

print "------"
print "Analyz Whole: Photometric redshift analysis"
print "------"

print "\n"

#MAIN.............................
n_estim = len(estim_list)
n_val = len(col_list)
plt.figure(1, figsize=(3,6.5))


cat_all = {}
for i in col_list: cat_all[i], _ = np.loadtxt(file_path, usecols = (col_list[i],1), unpack = True)

print "Catalog information:\n"

zt, zp, od = np.loadtxt(file_path,usecols= (zt_col, zp_col, od_col), unpack = True)

od = tls.od_renorm(od)
od = tls.od2eff(od)

od_cut = eff_cut
eff = 100 * (1 - eff_cut)
dz = (zp - zt) / (1 + zt)
#dz = zp - zt

print "\nCatalog analysis:"

n_od = len(od_cut)
cmap = plt.cm.get_cmap(name='jet')
gs0 = gridspec.GridSpec(1, 1)
gs0.update(bottom = 0.67, top = 0.95) 
ax = plt.subplot(gs0[0])
i = 0
for o in od_cut:
	mask = od > o 	
	plt.hist(dz[mask], histtype = 'step', bins = 100, range = (-val_max['scatter'],val_max['scatter']), normed = True, color = cmap(tls.cmapind(eff_cut[i], eff_lim, id_lim)))
	i += 1
plt.ylabel('N')
plt.xlabel(estim_label['scatter'])
plt.yscale('symlog', linthreshy = 1.)
plt.xlim(xmin = -val_max['scatter'], xmax = val_max['scatter'])
plt.axvline(val_req['bias'], lw = 0.5, ls = 'solid', color = 'black')
plt.xticks(ytick['scatter'], fontsize = 10)

gs1 = gridspec.GridSpec(3, 1)
gs1.update(bottom = 0.05, top = 0.6, hspace=0, wspace=0) 

ax = plt.subplot(gs1[0])
i = 0
for o in od_cut:

	mask = od > o 	
	
	bias = pztls.Median(dz[mask])
	err_bias = pztls.errmedian(dz[mask])
	plt.errorbar(eff[i], bias_times * bias, bias_times * err_bias, c = cmap(tls.cmapind(eff_cut[i], eff_lim, id_lim)), mec = cmap(tls.cmapind(eff_cut[i], eff_lim, id_lim)), markersize = 3, fmt = 'o')
	i += 1

plt.setp( ax.get_xticklabels(), visible=False)
ax.yaxis.set_major_locator(MaxNLocator(prune = 'both'))
#plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.xlim(xmin = 100, xmax = 0)
plt.axhline(val_req['bias'], lw = 0.5, ls = 'solid', color = 'black')
plt.ylabel(estim_label['bias'])
plt.ylim(ymin = -val_max['bias'], ymax = val_max['bias'])
plt.yticks(ytick['bias'])
plt.grid()

ax = plt.subplot(gs1[1])
i = 0
for o in od_cut:

	mask = od > o 	

	sig68 = pztls.Sigma68(dz[mask])
	err_sig68 = pztls.errsigma68(dz[mask])
	plt.errorbar(eff[i], 100 * sig68, 100 * err_sig68, c = cmap(tls.cmapind(eff_cut[i], eff_lim, id_lim)), mec = cmap(tls.cmapind(eff_cut[i], eff_lim, id_lim)), markersize = 3, fmt = 'o')
	i += 1

plt.setp( ax.get_xticklabels(), visible=False)
ax.yaxis.set_major_locator(MaxNLocator(prune = 'both'))
plt.ylabel(estim_label['sigma'])
plt.xlim(xmin = 100, xmax = 0)
plt.ylim(ymin = 0., ymax = val_max['sigma'])
plt.yticks(ytick['sigma'])
plt.axhline(val_req['sigma'], lw = 0.5, ls = 'solid', color = 'black')
plt.grid()

ax = plt.subplot(gs1[2])
i = 0
for o in od_cut:

	mask = od > o 	

	sig68 = pztls.Sigma68(dz[mask])
	of_sig68, err1_of_sig68, err2_of_sig68 = pztls.out_fract(dz[mask], sig68, 3)
	print eff[i], 100 * of_sig68
	plt.errorbar(eff[i], 100 * of_sig68, [[100 * err1_of_sig68, 100 * err2_of_sig68]], c = cmap(tls.cmapind(eff_cut[i], eff_lim, id_lim)), mec = cmap(tls.cmapind(eff_cut[i], eff_lim, id_lim)), markersize = 3, fmt = 'o')
	i +=1

ax.yaxis.set_major_locator(MaxNLocator(prune = 'both'))
plt.xlabel('Completeness (\%)')
plt.ylabel(estim_label['outliers'])
plt.xlim(xmin = 100, xmax = 0)
plt.ylim(ymin = 0., ymax = val_max['outliers'])
plt.yticks(ytick['outliers'])
plt.axhline(val_req['outliers'], lw = 0.5, ls = 'solid', color = 'black')
plt.grid()

#Remove extension...................
i=0
while(file_name[-i] != '.'): i += 1	

plt.savefig('../../Data/Plot/' + file_name[:-i] + '_whole.pdf', dpi = 600, bbox_inches="tight")
