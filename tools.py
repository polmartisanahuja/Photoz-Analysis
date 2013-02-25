import numpy as np
import matplotlib.pyplot as plt

def context(n_filt):
	i = np.arange(0,n_filt)
	a = pow(2,i)
	return a.sum()

def spectral(nc, c_min, c_max):
	dc = (c_max - c_min) / nc
	cmap = plt.cm.get_cmap(name='spectral')
	mycolors = [cmap(i) for i in np.arange(c_min,c_max,dc)]
	return mycolors
