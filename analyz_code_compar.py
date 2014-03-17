#!/usr/bin/env python
import numpy as np
import matplotlib.pylab as plt
import tools as tls
import pz_tools as pztls 
#from pau_bright_parameters_analyz_comp import *
from pau_faint_parameters_analyz_comp import *
from matplotlib import rc

rc('text', usetex=True)
rc('font', family='serif')

print "\n"

print "------"
print "Analyz: Photometric redshift code compare"
print "------"

print "\n"

#MAIN.............................
n_estim = len(estim_list)
n_field = len(filt_list)
n_col = len(col_list)
print 'n_estim=', n_estim 
print 'n_field=', n_field 
print 'n_col=', n_col 

plt.figure(1, figsize=(3 * n_col,1.5*n_estim))
plt.subplots_adjust(hspace=0,wspace=0) 
mytitle = plt.suptitle(sample + ' sample', y = 0.93)

j = 0
for c in col_list:
	print " %s" % c

	i = 0
	for f in filt_list:
		print "\n Filt set:",f
		
		file = folder_name + file_name + f + '_' + sample + flag + '.bpz' 

		zt, zp, od = np.loadtxt(file,usecols= (zt_col, zp_col, od_col), unpack = True)
		dz = (zp - zt) / (1 + zt)
		dz_all = np.copy(dz)
		
		_, X = np.loadtxt(file, usecols= (0, col_list[c]), unpack = True)
		X_all = np.copy(X)

		od = tls.od_renorm(od)
		od = tls.od2eff(od)

		mask = (od > 0.5)
		dz = dz[mask]
		X = X[mask]
		print 'Completness=', 100*float(len(X))/float(len(X_all))
		
		print len(dz), len(dz_all)

		dz_bin = pztls.binsplit(dz, X, binning[c])
		dz_bin_all = pztls.binsplit(dz_all, X_all, binning[c])
		k = 0
		for e in estim_list:
			print "    %s" % e
			
			val, err_val = pztls.estim(dz_bin,dz_bin_all,e)

			index = 1 + j + n_col * k
			print index

			a = plt.subplot(n_estim, n_col, index)
			x = binning[c][:-1] + 0.5 * (binning[c][1:] - binning[c][:-1])

			#plt.plot(x, val, color = colors[i])	
			if(f != '_default'): plt.errorbar(x, val, err_val, color = colors[i], label = filt_label[i])
			else: plt.errorbar(x, val, err_val, lw = 1.5, color = colors[i], label = filt_label[i])

			if(k + 1 != n_estim): 
				plt.setp( a.get_xticklabels(), visible=False)
				plt.xticks(xtick[c])
			else: 
				plt.xlabel(col_label[c])
				plt.xticks(xtick[c])

			if(j != 0): 
				plt.setp( a.get_yticklabels(), visible=False)
				plt.yticks(ytick[e])
			else: 
				plt.ylabel(estim_label[e])
				plt.yticks(ytick[e])

			plt.xlim(xmin = binning[c][0], xmax = binning[c][-1])
			plt.ylim(ymax = val_max[e])
			if((e == 'bias') or (e == 'scatter')): plt.ylim(ymin = - val_max[e])
			else: plt.ylim(ymin = 0)

			if(type(val_req[e]) == float):	plt.axhline(y=val_req[e], color = 'black', linewidth = 0.5, linestyle = 'dashed')	
			
			if(index == 1): plt.legend(loc = 'best', prop={'size':7}, ncol=2, numpoints = 1)

			k += 1
		i += 1
	j +=1

plt.savefig('../../Data/Plot/' + file_name + '_' + sample + '_filt_sets_compar.pdf', bbox_inches="tight", bbox_extra_artists=[mytitle])
