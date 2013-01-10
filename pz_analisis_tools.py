#! /usr/bin/python

import numpy as np
import math
import scipy
import operator as op
from parameters import *

nan = float('nan')

def dict(cat_col):
	
	cat = {}
	cat['z_phot'] = cat_col[zp_col]
	#cat['z_phot_min'] = cat_col[zp_min_col]
	#cat['z_phot_max'] = cat_col[zp_max_col]
	#cat['err_z_phot'] = (cat['z_phot_max'] - cat['z_phot_min']) / 2
	cat['z_true'] = cat_col[zt_col]
	cat['odds'] = cat_col[odds_col]
	
	return cat

def dict_annz(cat_col):
	
	cat = {}
	cat['z_phot'] = cat_col[zp_col]
	cat['err_z_phot'] = cat_col[err_zp_col]
	cat['z_true'] = cat_col[zt_col]
	
	return cat

def set_binning(cat, z_min = z_min, z_max = z_max):

	try: z_min 
	except: 
		if (cat['z_true'].min() < cat['z_phot'].min()): z_min = cat['z_phot'].min()
		else: z_min = cat['z_true'].min()
		z_min = round(z_min, 2)

	try: z_max
	except: 
		if (cat['z_true'].max() < cat['z_phot'].max()): z_max = cat['z_phot'].max()
		else: z_max = cat['z_true'].max()
		z_max = round(z_max, 2)

	bin_size = (z_max - z_min) / n_bins
	binning = np.arange(z_min, z_max + bin_size / 2., bin_size)
	return binning

def z_cut(cat, x_cut):
	"""Remove galaxies with z_phot > x_cut and < 0"""

	x = cat[zp_col]
	rm_x_pos = []
	for i in range(len(x)):
		#if (x[i] > x_cut): rm_x_pos.append(i)
		if ((x[i] > x_cut) | (x[i] <= 0.01)): rm_x_pos.append(i)
	cat = np.delete(cat, rm_x_pos, 1)
	
	#Print proportions.................................
	N = len(x) #N: Total number of galaxies
	n = len(x) - len(rm_x_pos) #n: Galaxies after cut
	#print "Num. gal = %d" % N
	#print "Num. gal. after $z(photo)<%2.2f$ cut = %d %1.1f\%%\n" % (x_cut, n , 100 * float(n)/float(N) )
	
	return cat, n, N
	
def odds_cut(cat, x_cut):

	x = cat[odds_col]
	rm_x_pos = []
	for i in range(len(x)):
		if (x[i] < x_cut): rm_x_pos.append(i)
	cat = np.delete(cat, rm_x_pos, 1)
	
	#Print proportions.................................
	N = len(x) #N: Total number of galaxies
	n = len(x) - len(rm_x_pos) #n: Galaxies after cut
	#print "Num. gal = %d" % N
	#print "Num. gal. after $odds>%2.2f$ cut = %d %1.1f\%%\n" % (x_cut, n , 100 * float(n)/float(N) )
	
	return cat, n, N
	
def cut(arr, col, value, func):

	x = arr[col]
	rm_x_pos = []
	for i in range(len(x)):
		if (func(x[i], value)): rm_x_pos.append(i)
	arr = np.delete(arr, rm_x_pos, 1)
	
	N = len(x) #N: Total number of galaxies
	n = len(x) - len(rm_x_pos) #n: Galaxies after cut
	
	return arr, float(n) / float(N)
	
def errz_cut(cat, x_cut):

	x = cat[err_zp_col]
	rm_x_pos = []
	for i in range(len(x)):
		if (x[i] > x_cut): rm_x_pos.append(i)
	cat = np.delete(cat, rm_x_pos, 1)
	
	#Print proportions.................................
	N = len(x) #N: Total number of galaxies
	n = len(x) - len(rm_x_pos) #n: Galaxies after cut
	#print "Num. gal = %d" % N
	#print "Num. gal. after $odds>%2.2f$ cut = %d %1.1f\%%\n" % (x_cut, n , 100 * float(n)/float(N) )
	
	return cat, n, N

def c_binning(binning): return binning[:-1] + (binning[1:] - binning[:-1]) / 2

def bin_split(x,y, binning):
	""" Returns an array Y[] containing all the y[] elements 
	splitted in bins according to the defined binning in pop_data.
	The separation in different bins is done through the correspondent
	x value of each y. 
	"""  
	
	Y = []
	l = len(binning) - 1
	for i in range(l+2): Y.append([]) #Seeting Y[] dimension
	inds = np.digitize(x, binning)
	for i in range(len(x)): Y[inds[i]].append(y[i]) #Adding y values in Y
	return Y

def Median(x):
	
	x.sort()
	i = int(len(x)*0.5) #Index of the high limit
	return x[i]
	
def errmedian(x):
	"""This function computes the error of the median
	 using a bootstrap method. It uses 1000 values to generate 
	 the distribution of sigma_z and then compute the rms of it """
	 
	y = []
	for i in range(1000):
		xr = resample(x)
		y.append(Median(xr))
	y = np.array(y)
	return np.std(y)
	
def Sigma68(x):
	"""Returns the half-interval where the probability "prob" is comulated 
	around the median, with equal areas in both sides. x[] is the array 
	containing the data dat defines the distribution
	"""
	x.sort()
	i_high = int(len(x) * (0.5 + 0.68 / 2.0)) #Index of the high limit
	i_low = int(len(x) * (0.5 - 0.68 / 2.0)) #Index of the low limit
	return (x[i_high] - x[i_low]) / 2
	
def errsigma68(x):
	"""This function computes the error of the sigma68
	 using a bootstrap method. It uses 1000 values to generate 
	 the distribution of sigma_z and then compute the rms of it """
	 
	y = []
	for i in range(1000):
		xr = resample(x)
		y.append(Sigma68(xr))
	y = np.array(y)
	return np.std(y)
	
def stderr(x):
	""" This function computes the error of the standar 
	deviation of x from the statistical (Variance of variance)"""
	
	m2 = scipy.stats.moment(x,2)
	m4 = scipy.stats.moment(x,4)
	N = len(x)

	factor = ((float(N) - 3) / (float(N) - 1))
	err = (1.0 / 2.0) * (1.0 / math.sqrt(N)) * (1.0 / math.sqrt(m2)) * math.sqrt(m4 - factor * m2 * m2)
	return err
	
def resample(x):
	"""This function takes the array x and then picks up N = dim(x)
	values of x and generates a new array y with these values (also sorted) """
	
	y = []
	r = np.random.random_integers(0, len(x) - 1, len(x))
	y = np.take(x, r)
	y.sort()
	return y
	
def lf(x): return math.log(math.factorial(x))

def Completeness(x_min, n, N):
	dx = 0.0001
	x = np.arange(x_min+dx ,1-dx,dx)
	f = np.exp( lf(N) - lf(n) - lf(N-n) + n * np.log(x) + (N - n) * np.log(1-x) )
	f = f/f.sum()
	norm = f.sum()
	i = np.argmax(f)
	i_low = i
	while ((f[i_low:i].sum() / norm < 0.34) & (i_low > 0) ): i_low -= 1
	i_high = i
	while ((f[i:i_high].sum() / norm < 0.34) & (i_high < len(x)-1)): i_high += 1
	
	return x[i], abs(x[i] - x[i_low]), abs(x[i] - x[i_high])
	
def out_fract(x, sig, num):
	
	n = 0
	N = len(x)
	for i in range(N): 
		if abs(x[i]) > num*sig: n += 1
	
	return Completeness(0, n, N)
	
def sigmavsodds(odds, delta_z, odds_bin):

	y = np.array([])
	std = np.array([])
	errstd = np.array([])
	y  =  bin_split(odds, delta_z, odds_bin)
	l = np.array([])
	
	for i in range(len(y)-2, 0, -1):
		l = np.append(l, y[i])
		std = np.append(std, l.std())
		errstd = np.append(errstd, stderr(l))
			
	std = std[len(std):-len(std)-1:-1]
	errstd = errstd[len(errstd):-len(errstd)-1:-1]
	
	return std, errstd
	
def sigmavserrz(errz, delta_z):

	y = np.array([])
	std = np.array([])
	errstd = np.array([])
	y  =  bin_split(errz, delta_z, errz_binning)
	l = np.array([])
	
	n = 1
	while(len(y[n]) == 0): 
		std = np.append(std, nan)
		errstd = np.append(errstd, nan)
		n = n + 1
	
	for i in range(n,len(y)-1, 1):
		l = np.append(l, y[i])
		std = np.append(std, l.std())
		errstd = np.append(errstd, stderr(l))
	
	return std, errstd

def biasvsz(z, delta_z, binning):
	
	#Computing median & mean...........................
	y = np.array([])
	median = np.array([])
	errmed = np.array([])
	mean = np.array([])
	errmean = np.array([])
	y  =  bin_split(z, delta_z, binning) 
	
	for i in range(1,len(y)-1):
		l = np.array(y[i])
		if len(y[i]) > 1:
			med = Median(l)
			
			median = np.append(median, med)
			errmed = np.append(errmed, errmedian(l))
			mean = np.append(mean,l.mean())
			errmean = np.append(errmean, l.std() / math.sqrt(len(l)) )
		else:
			median = np.append(median, nan)
			errmed = np.append(errmed, nan)
			mean = np.append(mean, nan)
			errmean = np.append(errmean, nan)
			
	print "median=", median 
	return median, errmed, mean, errmean
	
def sigmavsz(z, delta_z, binning):

	#Computing sigma68 & std..........................
	y = np.array([])
	sigma68 = np.array([])
	errsig68 = np.array([])
	std = np.array([])
	errstd = np.array([])
	y  =  bin_split(z, delta_z, binning) 
	
	for i in range(1,len(y)-1):
		l = np.array(y[i])
		if len(y[i]) > 1:
			sig68 = Sigma68(l)
			
			sigma68 = np.append(sigma68, sig68)
			errsig68 = np.append(errsig68, errsigma68(l))
			std = np.append(std, l.std())
			errstd = np.append(errstd, stderr(l))
			
		else:
			sigma68 = np.append(sigma68, nan)
			errsig68 = np.append(errsig68, nan)
			std = np.append(std, nan)
			errstd = np.append(errstd, nan)


	#print "sig68=", sigma68
	#print "std=", std
	return sigma68, errsig68, std, errstd
	
def outliersvsz(z, delta_z, binning, sig):
	
	#Computing outliers fraction in z bins.............
	y = np.array([])
	out_frac68 = np.array([])
	out_frac = np.array([])
	out_frac68_low = np.array([])
	out_frac_low = np.array([])
	out_frac68_high = np.array([])
	out_frac_high = np.array([])
	y  =  bin_split(z, delta_z, binning) 
		
	for i in range(1,len(y)-1):
		l = np.array(y[i])
		if len(y[i]) > 1:
			of68, of68_low, of68_high  = out_fract(l, Sigma68(l), sig)
			of, of_low, of_high = out_fract(l, l.std(), sig)
			
			out_frac68 = np.append(out_frac68, of68)
			out_frac = np.append(out_frac, of)
			out_frac68_low = np.append(out_frac68_low, of68_low)
			out_frac_low = np.append(out_frac_low, of_low)
			out_frac68_high = np.append(out_frac68_high, of68_high)
			out_frac_high = np.append(out_frac_high, of_high)
		else:
			out_frac68 = np.append(out_frac68, nan)
			out_frac = np.append(out_frac, nan)
			out_frac68_low = np.append(out_frac68_low, nan)
			out_frac_low = np.append(out_frac_low, nan)
			out_frac68_high = np.append(out_frac68_high, nan)
			out_frac_high = np.append(out_frac_high, nan)
			
	print "out_frac68=", out_frac68
	return out_frac68, out_frac68_low, out_frac68_high, out_frac, out_frac_high, out_frac_low
	
def migration_matrix(z_phot, z_true, binning):
	"""Columns are z_spec and rows z_photo. Columns are normalized to 1"""
	
	if(binning[0] == 0.): binning = np.concatenate((binning, [10.]), axis = 0)
	else: binning = np.concatenate(([0.], binning, [10.]), axis = 0)

	#Creating migration matrix with under and overflows
	H, xedges, yedges = np.histogram2d(z_true, z_phot, binning)
	
	#Normalizing columns of migration matrix
	row_sum = H.sum(axis=1)
	for i in range(len(row_sum)): 
		if(row_sum[i] == 0.): row_sum[i] = 1  
	H = (H.T / row_sum).T
	
	#Since can not be underflows when binning[0] = 0. we do..
	if(binning[0] == 0.): 
		H = H[0:-1, 0:-1]
		xedges = xedges[0:-1]
		yedges = yedges[0:-1]
	else: 
		H = H[1:-1, 1:-1]
		xedges = xedges[1:-1]
		yedges = yedges[1:-1]
	
	return H
	
def hist_oddscut(z_before, z, binning):
	
	hist_before = np.histogram(z_before, binning)
	hist = np.histogram(z, binning)
	
	#complet = hist[0].astype(float) / hist_before[0].astype(float)  
	
	return hist[0], hist_before[0]
