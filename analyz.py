#!/usr/bin/env python
# encoding: UTF8
#import yaml
import numpy as np
import tools as tls 
import matplotlib.pylab as plt
import pz_tools as pztls
from slaq_parameters_analyz import *
import textwrap
from matplotlib import rc

rc('text', usetex=True)
rc('font', family='serif')

print "\n"

print "------"
print "Analyz: Photometric redshift analysis"
print "------"

print "\n"

#MAIN.............................
n_estim = len(estim_list)
n_val = len(col_list)
plt.figure(1, figsize=(9,1.5*n_estim))
#if(title): mytitle = plt.suptitle(title, fontsize = 16, y = 0.93)
#else: plt.suptitle("\n".join(textwrap.wrap('Photo-z results for the "' + file_name + '"', 60)), fontsize = 16)
plt.subplots_adjust(hspace=0,wspace=0) 

cat_all = {}
for i in col_list: cat_all[i], _ = np.loadtxt(file_path, usecols = (col_list[i],1), unpack = True)

#Template rescaling.........
#cat_all['type'] -= 1 
#cat_all['type'] *= 10 

print "Catalog information:\n"

for i in col_list:
	print "\n" + i + " min =", cat_all[i].min()
	print i + " max =", cat_all[i].max()

zt_all, zp_all, od_all = np.loadtxt(file_path,usecols= (zt_col, zp_col, od_col), unpack = True)

if (error == 'True'): od_all = pztls.err2od(od_all)

od_all = tls.od_renorm(od_all)
od_all = tls.od2eff(od_all)

od_cut = eff_cut
#od_cut = tls.od_cut(od_all, eff_cut)

print "\nCatalog analysis:"

n_od = len(od_cut)
#mycolors = tls.spectral(n_od, 0.0, 1.0)
cmap = plt.cm.get_cmap(name='jet')
i_od = 0
for o in od_cut:
	print "\nodds>",o

	cat = {}

	dz_all = zp_all - zt_all
	#dz_all = (zp_all - zt_all) / (1 + zt_all)

	mask = od_all > o 	
	#mask = (zp_all >= 0) 	
	#mask = (od_all < o) & (cat_all['redshift'] >= 0) 	
	dz = dz_all[mask]
	#dz = dz_all
	

	#General values....................
	sigma68_all = pztls.Sigma68(dz)
	errsigma68_all = pztls.errsigma68(dz)
	rms_all = pztls.rms(dz)
	bias_all = pztls.Median(dz)
	errbias_all = pztls.errmedian(dz)
	comp_all, errcomp1_all, errcomp2_all = pztls.Completeness(0,len(dz),len(dz_all))
	#out_frac_all_sigma68, errout_frac1_all_sigma68, errout_frac2_all_sigma68 = pztls.out_fract(dz, sigma68_all, 3)
	out_frac_all_rms_2, errout_frac1_all_rms_2, errout_frac2_all_rms_2 = pztls.out_fract(dz, rms_all, 2)
	out_frac_all_rms_3, errout_frac1_all_rms_3, errout_frac2_all_rms_3 = pztls.out_fract(dz, rms_all, 3)


	print "\nResults using the entire catalog:"
	print "Sigma68 = %.5f +/- %.5f" %(sigma68_all,errsigma68_all)
	print "Bias = %.5f +/- %.5f" %(bias_all,errbias_all)
	print "Completeness = %.5f +%.5f/-%.5f" %(comp_all, errcomp1_all, errcomp2_all)
	print "2sig Outliers fraction (rms) = %.5f +%.5f/-%.5f" %(out_frac_all_rms_2, errout_frac1_all_rms_2, errout_frac2_all_rms_2)
	print "3sig Outliers fraction (rms) = %.5f +%.5f/-%.5f\n" %(out_frac_all_rms_3, errout_frac1_all_rms_3, errout_frac2_all_rms_3)
	print "Generation of plots...\n"

	#Bin splitting......................
	i = 1
	for l in col_list:
		print "  %s" % l	
		cat[l] = cat_all[l][mask]
		dz_bin_all = pztls.binsplit(dz_all, cat_all[l], binning[l])
		dz_bin = pztls.binsplit(dz, cat[l], binning[l])
		
		j=0
		for e in estim_list:
			print "    %s" % e
			
			if(e == 'scatter'):
				id_od = np.argsort(od_all)
				a = plt.subplot(n_estim, n_val, i + n_val*j)
				#plt.scatter(cat_all[l][id_od],dz_all[id_od], c=cmap( (od_all[id_od] - od_cut.min()) / (od_cut.max() - od_cut.min()) ), marker = 'o', lw = 0, rasterized=True)	
				plt.scatter(cat_all[l][id_od],dz_all[id_od], c=cmap(tls.cmapind(od_all[id_od],eff_lim, id_lim)), marker = 'o', s = 2.5, lw = 0, rasterized=True)	
			else:
				val, err_val = pztls.estim(dz_bin, dz_bin_all, e)

				a = plt.subplot(n_estim, n_val, i + n_val*j)
				x = binning[l][:-1] + 0.5 * (binning[l][1] - binning[l][0])
			#	plt.errorbar(x, val, err_val, color = cmap( (o - od_cut.min()) / (od_cut.max() - od_cut.min()) ))	
				plt.errorbar(x, val, err_val, color = cmap(tls.cmapind(o, eff_lim, id_lim)))
				#np.savetxt('./' + e + '_vs_' + l + '.txt', np.array([x, val ,err_val]).T, fmt = '%.4f')
			
			if(j + 1 != n_estim): plt.setp( a.get_xticklabels(), visible=False)
			else: 
				plt.xlabel(col_label[l])
				plt.xticks(xtick[l])
				#plt.setp( a.get_xticklabels()[-1], visible=False)
				#plt.setp( a.get_xticklabels()[0], visible=False)

			if(i != 1): plt.setp( a.get_yticklabels(), visible=False)
			else: 
				plt.ylabel(estim_label[e])
				plt.yticks(ytick[e])
				#plt.setp( a.get_yticklabels()[-1], visible=False)
				#plt.setp( a.get_yticklabels()[0], visible=False)

			if(type(val_req[e]) == float): plt.axhline(y=val_req[e], color = 'black', linewidth = 1, linestyle = 'dashed')		

			plt.xlim(xmin = binning[l][0], xmax = binning[l][-1])
			plt.ylim(ymax = val_max[e])
			if((e == 'bias') or (e == 'scatter')): plt.ylim(ymin = - val_max[e])
			else: plt.ylim(ymin = 0)

			j += 1
		i += 1
	i_od +=1

#Remove extension...................
i=0
while(file_name[-i] != '.'): i += 1	

#plt.savefig('../../Data/Plot/' + file_name[:-i] + '.pdf', dpi = 600)
#plt.savefig('../../Data/Plot/' + file_name[:-i] + '.pdf', dpi = 600, bbox_inches="tight", bbox_extra_artists=[mytitle])
plt.savefig('../../Data/Plot/' + file_name[:-i] + '.pdf', dpi = 600, bbox_inches="tight")
