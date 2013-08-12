#!/usr/bin/env python
import numpy as np
import matplotlib.pylab as plt
from parameters_analyz_cp import *

print "\n"

print "------"
print "Analyz: Photometric redshift code scatter compare"
print "------"

print "\n"

field_list += ['all']

#MAIN.............................
n_field = len(field_list)
n_code = len(code_list)
print 'n_field=', n_field 
print 'n_code=', n_code 

plt.figure(1, figsize=(3 * n_code,1.5 * n_field))
plt.subplots_adjust(hspace=0,wspace=0) 

e = 'median'
N_new = 1000

j = 0
for c in code_list:
	print " %s" % c

	dz_all = np.array([])
	X_all = np.array([])

	i = 0
	for f in field_list:
		print "\n field",f
		
		if(f != 'all'): 
			zt, zp, m = np.loadtxt(folder_name + f + '/' + c + '_' + f + '.txt', usecols= (zt_col[j],zp_col[j],m_col[j]), unpack = True)

			mask = (zp >= 0)
			zt = zt[mask]
			zp = zp[mask]
			m = m[mask]

			N = len(zt)
			id_rand = np.random.permutation(N)
			zt = zt[id_rand]
			zp = zp[id_rand]
			m = m[id_rand]
		
			X = m 
			X_label = 'm'
			X_axis_label = 'mag $i_{AB}$'
			#X_axis_label = 'z-spec'
			dz = zp - zt

			dz_all = np.append(dz, dz_all)
			X_all = np.append(X, X_all)

		index = 1 + j + n_code * i
		a = plt.subplot(n_field, n_code, index)
		if(f != 'all'): plt.scatter(X, dz, s = 5, c = colors[i], lw = 0, rasterized = True)	
		else: 
			N = len(X_all)
			id_rand = np.random.permutation(N)
			plt.scatter(X_all[id_rand], dz_all[id_rand], s = 5, c = 'black', lw = 0, rasterized = True)	
		
		if(i + 1 != n_field): plt.setp( a.get_xticklabels(), visible=False)
		else: 
			plt.xlabel(X_axis_label)
			plt.xticks(xtick[X_label])

		if(j != 0): plt.setp( a.get_yticklabels(), visible=False)
		else: 
			plt.ylabel('z(ph) - z(sp)')
			plt.yticks(5 * ytick[e])
		if(i == 0): plt.title(code_list[j])


		plt.xlim(xmin = binning[X_label][0], xmax = binning[X_label][-1])
		plt.ylim(ymax = 5 * val_max[e], ymin = 5 * val_min[e])
		plt.axhline(y=val_req[e], color = 'black', linewidth = 1, linestyle = 'dashed')	

		i += 1
	j +=1

plt.savefig('/Users/polstein/Desktop/analy_scatter.pdf')
