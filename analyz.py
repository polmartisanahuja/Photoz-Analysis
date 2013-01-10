import numpy as np
import tools
import matplotlib.pylab as plt
import pz_tools as tls
from parameters_analyz import *
import textwrap

#MAIN.............................
n_estim = len(estim_list)
n_val = len(val_list)
plt.figure(1, figsize=(3*n_val,1.5*n_estim))
if(title): plt.suptitle(title, fontsize = 16)
else: plt.suptitle("\n".join(textwrap.wrap('Photo-z results for the "' + file_name + '"', 60)), fontsize = 16)
plt.subplots_adjust(hspace=0,wspace=0) 

cat_all = {}
cat_all['magnitude'],cat_all['redshift'],cat_all['type'],zt_all,od_all = np.loadtxt(file_path, usecols = col, unpack = True)

print "\nm min=", cat_all['magnitude'].min()
print "m max=", cat_all['magnitude'].max()

print "\nz max=", cat_all['redshift'].max()
print "z min=", cat_all['redshift'].min()

print "\nt max=", cat_all['type'].max()
print "t min=", cat_all['type'].min()

n_od = len(od_cut)
mycolors = tools.spectral(n_od, 0.2, 1.0)
i_od = 0
for o in od_cut:
	print "odds>",o

	cat = {}

	dz_all = cat_all['redshift'] - zt_all
	#dz_all = (cat_all['redshift'] - zt_all) / (1 + cat_all['redshift'])

	mask = od_all > o 	
	dz = dz_all[mask] 

	i = 1
	for l in val_list:
		print "  %s" % l	
		cat[l] = cat_all[l][mask]
		dz_bin_all = tls.binsplit(dz_all, cat_all[l], binning[l])
		dz_bin = tls.binsplit(dz, cat[l], binning[l])
		
		j=0
		for e in estim_list:
			print "    %s" % e
			
			if(e == 'scatter'):
				id_od = np.argsort(od_all)
				a = plt.subplot(n_estim, n_val, i + n_val*j)
				plt.scatter(cat_all[l][id_od],dz_all[id_od], c=od_all[id_od], marker = 'o', lw = 0, rasterized=True)	
			else:
				val, err_val = tls.estim(dz_bin, dz_bin_all, e)

				a = plt.subplot(n_estim, n_val, i + n_val*j)
				x = binning[l][:-1] + 0.5 * (binning[l][1] - binning[l][0])
				plt.errorbar(x, val, err_val, color = mycolors[i_od])	

			
			if(j + 1 != n_estim): plt.setp( a.get_xticklabels(), visible=False)
			else: 
				plt.xlabel(l)
				plt.xticks(xtick[l])
				#plt.setp( a.get_xticklabels()[-1], visible=False)
				#plt.setp( a.get_xticklabels()[0], visible=False)

			if(i != 1): plt.setp( a.get_yticklabels(), visible=False)
			else: 
				plt.ylabel(estim_label[e])
				plt.yticks(ytick[e])
				#plt.setp( a.get_yticklabels()[-1], visible=False)
				#plt.setp( a.get_yticklabels()[0], visible=False)

			if((e != 'histogram') and (e != 'completeness')): plt.axhline(y=val_req[e], color = 'black', linewidth = 1, linestyle = 'dashed')		

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

plt.savefig(file_name[:-i] + '.pdf')
