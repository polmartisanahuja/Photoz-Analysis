#! /usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import pz_analisis_tools as tool
from scipy.stats.mstats import *
from parameters import *

nan = float('nan')

def plot_zvsz(z_phot, z_true, binning, z_min, z_max):
	
	plt.figure(figsize=(13, 7))
	
	plt.subplot(121)	
	plt.plot(z_true, z_phot, 'o', markersize = 1)
	plt.plot([z_min, z_max], [z_min, z_max], linewidth = 1, color = 'red')
	plt.axis('scaled')
	plt.xlim(xmin = z_min, xmax = z_max)
	plt.ylim(ymin = z_min, ymax = z_max)
	plt.xlabel("z(true)")
	plt.ylabel("z(phot)")
	
	plt.subplot(122)
	H = tool.migration_matrix(z_phot, z_true, binning)
	H = H.T
	plt.pcolor(binning, binning, H)
	plt.axis('scaled')
	plt.xlim(xmin = z_min, xmax = z_max)
	plt.ylim(ymin = z_min, ymax = z_max)
	plt.ylabel("z(phot)")
	plt.xlabel("z(true)")
	plt.title("Transition Matrix z(true)$\\rightarrow$z(phot)")
	#plt.colorbar(aspect = 30, orientation = 'horitzontal', fraction = 0.03).set_label("Probability")
	plt.colorbar(aspect = 30, fraction = 0.03).set_label("Probability")
	
	plt.savefig(plot_folder + "zvsz.png", bbox_inches='tight')
	#plt.savefig(plot_folder + "zvsz.pdf", bbox_inches='tight')
	plt.close()
				
def plot_dzvsz(z_phot, z_true, z_min, z_max, Dz_range):
	
	if(delta_z_str == "$\Delta z$"): delta_z = z_phot - z_true
	if(delta_z_str == "$\Delta z/(1+z)$"): delta_z = (z_phot - z_true) / (1 + z_true)
	
	plt.figure(figsize=(7, 13))
										
	plt.subplot(211)	
	plt.plot(z_true, delta_z, 'o', markersize = 1)
	plt.axhline( 0, linewidth = 1, color = 'red')
	plt.xlim(xmin = z_min, xmax = z_max)
	plt.ylim(ymin = -Dz_range, ymax = Dz_range)
	plt.xlabel("z(true)")
	plt.ylabel(delta_z_str)

	plt.subplot(212)
	plt.plot(z_phot, delta_z, 'o', markersize = 1)
	plt.axhline( 0, linewidth = 1, color = 'red')
	plt.xlim(xmin = z_min, xmax = z_max)
	plt.ylim(ymin = -Dz_range, ymax = Dz_range)
	plt.xlabel("z(phot)")
	plt.ylabel(delta_z_str)
		
	plt.savefig(plot_folder + "dzvsz.png")
	plt.close()
	
def plot_dzvsodds(cat_before, cat, binning, Dz_range, z_min, z_max, qual_para, od_bin):
	
	if(delta_z_str == "$\Delta z$"): delta_z = cat_before['z_phot'] - cat_before['z_true']
	if(delta_z_str == "$\Delta z/(1+z)$"): delta_z = (cat_before['z_phot'] - cat_before['z_true']) / (1 + cat_before['z_true'])

	od_min = cat_before['odds'].min()
	od_max = cat_before['odds'].max()
	#if(od_max > 1.0): od_max = 1. 
	
	odds_binning = np.arange(od_min, od_max, od_bin)
	
	odds_bin = tool.c_binning(odds_binning)
	s_y, err_s_y = tool.sigmavsodds(cat_before['odds'], delta_z, odds_bin = odds_binning)
	mult = 1
	
	plt.figure(figsize=(13, 7))
	
	plt.subplot(121)
	plt.plot(cat_before['odds'], delta_z, 'o', markersize = 1)
	plt.errorbar(odds_bin, mult*s_y, mult*err_s_y, color = 'green', label = "cumulative RMSx" + str(mult))
	plt.axhline( 0, linewidth = 1, color = 'red')
	plt.axvline( odds_cut, linewidth = 1, color = 'blue', label = qual_para + " cut = " + str(odds_cut))
	plt.xlim(xmin = 0, xmax = 1)
	if (qual_para == 'odds'): plt.xlim(xmin = 0, xmax = 1)
	if (qual_para == 'PDZbest'): plt.xlim(xmin = 0, xmax = 100)
	plt.ylim(ymin = -Dz_range, ymax = Dz_range)
	plt.xlabel(qual_para)
	plt.ylabel(delta_z_str)
	
	z_bin = tool.c_binning(binning)
	n_true, N_true = tool.hist_oddscut(cat_before['z_true'], cat['z_true'], binning)
	n_phot, N_phot = tool.hist_oddscut(cat_before['z_phot'], cat['z_phot'], binning)
	
	#c:completeness
	c_true = np.array([])
	c_true_high = np.array([])
	c_true_low = np.array([])
	
	c_phot = np.array([])
	c_phot_high = np.array([])
	c_phot_low = np.array([])
	
	for i in range(len(binning)-1):
		
		if N_true[i] > 1: c, c_low, c_high = tool.Completeness(0, n_true[i], N_true[i])
		else:
			c = nan
			c_high = nan
			c_low = nan
			
		c_true = np.append(c_true, c)
		c_true_high = np.append(c_true_high, c_high)
		c_true_low = np.append(c_true_low, c_low)
		
		if N_phot[i] > 1: c, c_low, c_high = tool.Completeness(0, n_phot[i], N_phot[i])
		else:
			c = nan
			c_high = nan
			c_low = nan
		
		c_phot = np.append(c_phot, c)
		c_phot_high = np.append(c_phot_high, c_high)
		c_phot_low = np.append(c_phot_low, c_low)
		
	err_c_true = [c_true_low, c_true_high]
	err_c_phot = [c_phot_low, c_phot_high]
	
	plt.subplot(122)
	plt.errorbar(z_bin, c_true, err_c_true, color = 'blue', label = "z(true)")
	plt.errorbar(z_bin, c_phot, err_c_phot, color = 'red', label = "z(phot)")
	plt.ylabel("Completeness")
	plt.xlabel("z")
	plt.xlim(xmin = z_min, xmax = z_max)
	plt.ylim(ymin = 0, ymax = 1.)
	plt.legend(loc = 'best')

	plt.savefig(plot_folder + "odds_cut.png", bbox_inches='tight')
	plt.close()

def plot_dzvserrz(cat_before, cat, binning, Dz_range, z_min, z_max):
	
	if(delta_z_str == "$\Delta z$"): delta_z = cat_before['z_phot'] - cat_before['z_true']
	if(delta_z_str == "$\Delta z/(1+z)$"): delta_z = (cat_before['z_phot'] - cat_before['z_true']) / (1 + cat_before['z_true'])

	errz_bin = tool.c_binning(errz_binning)
	s_y, err_s_y = tool.sigmavserrz(cat_before['err_z_phot'], delta_z)
	
	mult = 1
	
	plt.figure(figsize=(13, 7))
	
	plt.subplot(121)
	plt.plot(cat_before['err_z_phot'], delta_z, 'o', markersize = 1) 
	plt.errorbar(errz_bin, mult*s_y, mult*err_s_y, color = 'green', label = "cumulative RMSx" + str(mult))
	plt.axhline( 0, linewidth = 1, color = 'red')
	plt.axvline( errz_cut, linewidth = 1, color = 'blue', label = "ERR z(phot) cut = " + str(errz_cut))
	plt.xlim(xmin = 0, xmax = yrange_sigma * sigma_ref)
	plt.ylim(ymin = -Dz_range, ymax = Dz_range)
	plt.xlabel("ERR z(phot)")
	plt.ylabel(delta_z_str)
	plt.legend(loc = 'best')
	
	z_bin = tool.c_binning(binning)
	n_true, N_true = tool.hist_oddscut(cat_before['z_true'], cat['z_true'], binning)
	n_phot, N_phot = tool.hist_oddscut(cat_before['z_phot'], cat['z_phot'], binning)
	
	#c:completeness
	c_true = np.array([])
	c_true_high = np.array([])
	c_true_low = np.array([])
	
	c_phot = np.array([])
	c_phot_high = np.array([])
	c_phot_low = np.array([])
	
	for i in range(len(binning)-1):
		
		if N_true[i] > 1: c, c_low, c_high = tool.Completeness(0, n_true[i], N_true[i])
		else:
			c = nan
			c_high = nan
			c_low = nan
			
		c_true = np.append(c_true, c)
		c_true_high = np.append(c_true_high, c_high)
		c_true_low = np.append(c_true_low, c_low)
							
		if N_phot[i] > 1: c, c_low, c_high = tool.Completeness(0, n_phot[i], N_phot[i])
		else:
			c = nan
			c_high = nan
			c_low = nan
		
		c_phot = np.append(c_phot, c)
		c_phot_high = np.append(c_phot_high, c_high)
		c_phot_low = np.append(c_phot_low, c_low)
	
	err_c_true = [c_true_low, c_true_high]
	err_c_phot = [c_phot_low, c_phot_high]
	
	plt.subplot(122)
	plt.errorbar(z_bin, c_true, err_c_true, color = 'blue', label = "z(true)")
	plt.errorbar(z_bin, c_phot, err_c_phot, color = 'red', label = "z(phot)")
	plt.ylabel("Completeness")
	plt.xlabel("z")
	plt.xlim(xmin = z_min, xmax = z_max)
	plt.ylim(ymin = 0, ymax = 1.)
	plt.legend(loc = 'best')

	plt.savefig(plot_folder + "errz_cut.png")
	plt.close()
	
def plot_syvsz(z_phot, z_true, binning, s ,s_label, sp_label, x_label , y_ref, sig = "nan"):

	z_bin = tool.c_binning(binning)
	
	if(x_label == "z(true)"): z = z_true
	if(x_label == "z(phot)"): z = z_phot 
	
	if(delta_z_str == "$\Delta z$"): delta_z = z_phot - z_true
	if(delta_z_str == "$\Delta z/(1+z)$"): delta_z = (z_phot - z_true) / (1 + z_true)
	
	#sp: estimator percentage (median, sigma68, ...)
	#s: estimator (mean, sigma, ...)
	
	if(s == "bias"): 
		sp_y, err_sp_y, s_y , err_s_y = tool.biasvsz(z, delta_z, binning)
		np.savetxt('/Users/polstein/Desktop/' + s + '_' + x_label + '.txt', np.array([z_bin, sp_y, err_sp_y]).T, fmt = '%5.5f')
	if(s == "sigma"): 
		sp_y, err_sp_y, s_y , err_s_y = tool.sigmavsz(z, delta_z, binning)
		plt.ylim(ymax = yrange_sigma * sigma_ref)
		np.savetxt('/Users/polstein/Desktop/' + s + '_' + x_label + '.txt', np.array([z_bin, sp_y, err_sp_y]).T, fmt = '%5.5f')
	if(s == str(sig) + "$\sigma$ outliers fraction"): 
		sp_y, err_sp_y_low, err_sp_y_high, s_y , err_s_y_low, err_s_y_high  = tool.outliersvsz(z, delta_z, binning, sig)
		err_sp_y = [err_sp_y_low, err_sp_y_high]
		err_s_y = [err_s_y_low, err_s_y_high]
		np.savetxt('/Users/polstein/Desktop/' + s + '_' + x_label + '.txt', np.array([z_bin, s_y, err_s_y_low, err_s_y_high]).T, fmt = '%5.5f')
		if(sig == 2): plt.ylim(ymax = yrange_out2)
		if(sig == 3): plt.ylim(ymax = yrange_out3)
		
	plt.errorbar(z_bin, s_y, err_s_y, color = 'black', label = s_label)
	plt.errorbar(z_bin, sp_y, err_sp_y, color = 'blue', label = sp_label)
	plt.axhline( y = y_ref, linewidth = 1, color = 'red')
	if(s != "bias"): plt.ylim(ymin = 0)
	#plt.ylim(ymax = 0.25)
	plt.xlim(xmin = z_min, xmax = z_max)
	plt.xlabel(x_label)
	plt.ylabel(s + " " + delta_z_str)
	plt.legend(loc = 'best')
	
	return sp_y, err_sp_y
		
def plot_biasvsz(z_phot, z_true, binning, Dz_range):
	
	plt.figure(figsize=(7, 13))
										
	plt.subplot(211)	
	plot_syvsz(z_phot, z_true, binning, "bias", "mean", "median", "z(true)" , bias_ref)
	plt.ylim(ymin = -Dz_range, ymax = Dz_range)
	
	plt.subplot(212)
	plot_syvsz(z_phot, z_true, binning, "bias", "mean", "median", "z(phot)" , bias_ref)
	plt.ylim(ymin = -Dz_range, ymax = Dz_range)
		
	plt.savefig(plot_folder + "biasvsz.png")
	#plt.savefig(plot_folder + "biasvsz.pdf")
	plt.close()
	
def plot_sigmavsz(z_phot, z_true, binning):
	
	plt.figure(figsize=(7, 13))
										
	plt.subplot(211)	
	plot_syvsz(z_phot, z_true, binning, "sigma", "$\sigma$", "$\sigma_{68}$", "z(true)" , sigma_ref)
	v = plt.axis()
	
	plt.subplot(212)
	plot_syvsz(z_phot, z_true, binning, "sigma", "$\sigma$", "$\sigma_{68}$", "z(phot)" , sigma_ref)
	plt.axis(v)
		
	plt.savefig(plot_folder + "sigmavsz.png")
	#plt.savefig(plot_folder + "sigmavsz.pdf") 
	plt.close()
	
def plot_outliersvsz(z_phot, z_true, binning, sig, y_ref):

	plt.figure(figsize=(7, 13))
										
	plt.subplot(211)
	plot_syvsz(z_phot, z_true, binning, str(sig) + "$\sigma$ outliers fraction", "$\sigma$", "$\sigma_{68}$", "z(true)" , y_ref, sig)
	v = plt.axis()
	
	plt.subplot(212)
	plot_syvsz(z_phot, z_true, binning, str(sig) + "$\sigma$ outliers fraction", "$\sigma$", "$\sigma_{68}$", "z(phot)" , y_ref, sig)
	plt.axis(v)
	
	plt.savefig(plot_folder + str(sig) + "sig_outliersvsz.png")
	#plt.savefig(plot_folder + str(sig) + "sig_outliersvsz.pdf")
	plt.close()
	
def plot_histo_nvsz(z_phot, z_true, binning):
	
	plt.hist(z_true, bins = binning, color = 'blue', label = "z(true)", log = True )
	plt.hist(z_phot, bins = binning, histtype = 'step', label = "z(phot)", color = 'red', log = True)
	
	plt.xticks(np.arange(0, 10, 0.5))
	
	plt.ylim(ymin = 0.5, ymax = nzvsz_ymax)
	plt.xlim(xmax = z_max)
	
	plt.xlabel("z")
	plt.ylabel("N")
	
	plt.legend(loc = 'best')
	
	plt.savefig(plot_folder + "Nz.png")
	plt.close()
	
def plot_histo_dzvsz(z_phot, err_z_phot, z_true):
	
	for i in range(len(err_z_phot)):
		if (err_z_phot[i] == 0): print z_phot[i], z_true[i]

	#Erase defectuos galaxies with err_z_phot = 0
	#rm_x_pos = []
	#for i in range(len(err_z_phot)):
	#	if(err_z_phot[i] < 0.00000001): rm_x_pos.append(i)
	#err_z_phot = np.delete(err_z_phot, rm_x_pos, 0)	
	#z_phot = np.delete(z_phot, rm_x_pos, 0)
	#z_true = np.delete(z_true, rm_x_pos, 0)

	delta_z = (z_phot - z_true) / err_z_phot 

	plt.figure(figsize=(13, 7))
	
	plt.subplot(121)	
	
	dz_lim = 10
	n_bins = 80.
	z_range = (- dz_lim, dz_lim)
	
	n, bins, patches = plt.hist(delta_z, n_bins, z_range, normed = True)
	y_gaus = plt.mlab.normpdf(bins, 0, 1)
	plt.plot(bins, y_gaus, color = 'red', label = "Normal")
	
	plt.xlabel("z(phot) - z(true) / z(phot) error")
	plt.ylabel("fraction")
	
	plt.legend(loc = 'best')
	
	plt.subplot(122)
	
	n, bins, patches = plt.hist(delta_z, n_bins, z_range, normed = True, cumulative = True)
	y_gaus = y_gaus.cumsum() * (2 * dz_lim / n_bins)
	plt.plot(bins, y_gaus, color = 'red', label = "Normal")
	
	plt.xlabel("z(phot) - z(true) / z(phot) error")
	plt.ylabel("cumulative")
	
	plt.legend(loc = 'best')
	
	plt.savefig(plot_folder + "histo_dzvsz.png")
	plt.close()
