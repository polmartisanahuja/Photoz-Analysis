#!/usr/bin/env python
import numpy as np
import matplotlib.pylab as plt
import pz_tools_cp as tls
from parameters_analyz_cp import *

print "\n"

print "------"
print "Analyz: Photometric redshift code compare"
print "------"

print "\n"

#MAIN.............................
n_estim = len(estim_list)
n_field = len(field_list)
n_code = len(code_list)
print 'n_estim=', n_estim 
print 'n_field=', n_field 
print 'n_code=', n_code 

plt.figure(1, figsize=(3 * n_code,1.5*n_estim))
#plt.suptitle(title, fontsize = 10)
plt.subplots_adjust(hspace=0,wspace=0) 

j = 0
for c in code_list:
	print " %s" % c

	dz_all = np.array([])
	X_all = np.array([])

	i = 0
	for f in field_list:
		print "\n field",f
		
		print m_col
	
		zt, zp, m = np.loadtxt(folder_name + f + '/' + c + '_' + f + '.txt', usecols= (zt_col[j],zp_col[j],m_col[j]), unpack = True)

		mask = (zp >= 0)
		zt = zt[mask]
		zp = zp[mask]
		m = m[mask]

		#id_rand = np.random.permutation(N_gal[i])
		#zt = zt[:N_gal[i]][id_rand]
		#zp = zp[:N_gal[i]][id_rand]
		#m = m[:N_gal[i]][id_rand]
		
		X = zt 
		X_label = 'zt'
		X_axis_label = 'mag $i_{AB}$'
		X_axis_label = 'z-spec'
		dz = zp - zt
		dz_all = np.append(dz, dz_all)
		X_all = np.append(X, X_all)

		dz_bin = tls.binsplit(dz, X, binning[X_label])
		if(i == n_field - 1):
			dz_bin_all = tls.binsplit(dz_all, X_all, binning[X_label])
		
		k=0
		for e in estim_list:
			print "    %s" % e
			
			val, err_val = tls.estim(dz_bin,e)

			index = 1 + j + n_code * k
			#print 'index=',index
			a = plt.subplot(n_estim, n_code, index)
			x = binning[X_label][:-1] + 0.5 * (binning[X_label][1] - binning[X_label][0])

			plt.plot(x, val, color = colors[i])	
			if(i == n_field - 1):
				val, err_val = tls.estim(dz_bin_all,e)
				if(e == 'histogram'): plt.plot(x, val, color = 'black', lw = 2)	
				else: plt.errorbar(x, val, err_val, color = 'black', lw = 2)	

			
			if(k + 1 != n_estim): plt.setp( a.get_xticklabels(), visible=False)
			else: 
				plt.xlabel(X_axis_label)
				plt.xticks(xtick[X_label])

			if(j != 0): plt.setp( a.get_yticklabels(), visible=False)
			else: 
				plt.ylabel(estim_label[e])
				plt.yticks(ytick[e])
			if(k == 0): plt.title(code_list[j])


			plt.xlim(xmin = binning[X_label][0], xmax = binning[X_label][-1])
			plt.ylim(ymax = val_max[e], ymin = val_min[e])
			plt.axhline(y=val_req[e], color = 'black', linewidth = 1, linestyle = 'dashed')	

			k += 1
		i += 1
	j +=1

plt.savefig('/Users/polstein/Desktop/analy_photoz.pdf')
