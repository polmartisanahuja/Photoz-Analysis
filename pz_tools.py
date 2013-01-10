import numpy as np
import math
import scipy

def binsplit(a, x, x_binning):

	n_bin = len(x_binning) - 1
	a_split = [] 
	for i in range(n_bin):
		mask = (x > x_binning[i]) & (x < x_binning[i+1])
		a_split += [a[mask]]
	return a_split 

def estim(a_split, a_split_all, estimator):
	
	n_bin = len(a_split)
	val = np.zeros(n_bin) 	
	
	if(estimator == 'histogram'):
		err_val = np.zeros(n_bin) 	
		for i in range(n_bin): 
			val[i] = len(a_split[i])
			err_val[i] = math.sqrt(val[i])
		
	if(estimator == 'completeness'):
		err_val = np.zeros((2, n_bin))
		for i in range(n_bin): 
			val[i], err_val[0][i], err_val[1][i] =  Completeness(0,len(a_split[i]), len(a_split_all[i]))
		val *= 100	
		err_val *= 100	

	if(estimator == 'bias'): 
		err_val = np.zeros(n_bin) 	
		for i in range(n_bin): 
			val[i] = Median(a_split[i])
			err_val[i] = errmedian(a_split[i])

	if(estimator == 'sigma'):
		err_val = np.zeros(n_bin) 	
		for i in range(n_bin): 
			val[i] = Sigma68(a_split[i])
			err_val[i] = errsigma68(a_split[i])
		val *= 100	
		err_val *= 100	

	if(estimator == 'outliers'):
		err_val = np.zeros((2, n_bin))
		for i in range(n_bin): 
			val[i], err_val[0][i], err_val[1][i] = out_fract(a_split[i], Sigma68(a_split[i]), 3)
		val *= 100	
		err_val *= 100	
		
	return val, err_val

def Median(x):
	
	if(len(x)>10):
		x.sort()
		i = int(len(x)*0.5) #Index of the high limit
		return x[i]
	else: return np.nan
	
def errmedian(x):
	"""This function computes the error of the median
	 using a bootstrap method. It uses 1000 values to generate 
	 the distribution of sigma_z and then compute the rms of it """
	if(len(x) > 30): 
		y = []
		for i in range(1000):
			xr = resample(x)
			y.append(Median(xr))
		y = np.array(y)
		return np.std(y)
	else:	return np.nan
		
def Sigma68(x):
	"""Returns the half-interval where the probability "prob" is comulated 
	around the median, with equal areas in both sides. x[] is the array 
	containing the data dat defines the distribution
	"""
	if(len(x) > 30): 
		x.sort()
		i_high = int(len(x) * (0.5 + 0.68 / 2.0)) #Index of the high limit
		i_low = int(len(x) * (0.5 - 0.68 / 2.0)) #Index of the low limit
		return (x[i_high] - x[i_low]) / 2
	else: return np.nan
	
def errsigma68(x):
	"""This function computes the error of the sigma68
	 using a bootstrap method. It uses 1000 values to generate 
	 the distribution of sigma_z and then compute the rms of it """
	 
	if(len(x) > 30): 
		y = []
		for i in range(1000):
			xr = resample(x)
			y.append(Sigma68(xr))
		y = np.array(y)
		return np.std(y)
	else: return np.nan
	
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
	dx = 0.000001
	x = np.arange(x_min+dx ,1-dx,dx)
	f = np.exp( lf(N) - lf(n) - lf(N-n) + n * np.log(x) + (N - n) * np.log(1-x) )
	f = f/f.sum()
	norm = f.sum()
	i = np.argmax(f)
	i_low = i
	while ((f[i_low:i].sum() / norm < 0.34) & (i_low > 0)): 
		i_low -= 1
	i_high = i
	while ((f[i:i_high].sum() / norm < 0.34) & (i_high < len(x)-1)): i_high += 1
	
	return x[i], abs(x[i] - x[i_low]), abs(x[i] - x[i_high])
	
def out_fract(x, sig, num):
	
	n = 0
	N = len(x)
	for i in range(N): 
		if abs(x[i]) > num*sig: n += 1
	
	return Completeness(0, n, N)
