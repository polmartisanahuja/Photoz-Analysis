import os as os
import numpy as np
import pz_tools as pt

#Gencat_nonobs............................................
folder = "./"
files = os.listdir(folder)

for name in files:
	zp, zs = np.loadtxt(folder + name, usecols = (1,9), unpack = True)
	dz = zp - zs
	len_before = len(dz)

	mask = dz < 0.5 
	dz = dz[mask]
	len_after = len(dz)

	sig = np.std(dz)
	#sig68 = pt.Sigma68(dz)
	of, _, _ = pt.out_fract(dz, 0.02, 1)

	print "\nName = ", name
	print "Percentage lost = %.3f%%" % (float((len_before - len_after) * 100) / float(len_before))
	print "sig = %.5f" % sig 
	#print "sig68 = %.5f" % sig68
	print "of = %.2f%%" % (of * 100) 
