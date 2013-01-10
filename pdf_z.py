import math
import sys
import numpy as np
import matplotlib.pyplot as plt
import os as os
#from pdf_parameters import *

#Parameters..........................................
#n_pdf = 30
width = 0.1
z_resol = 0.001 #Must me set according to the probs file returned in BPZ
z_min = 0.01
z_max = 6.0 
#odds_cut = 0.65
folder = "/Users/pmarti/Dropbox/Tesi/photoz/mock.r260.n1e6.s10.121027_42NB.100A/BPZ/bright/"
probs_file = "mock.r260.n1e6.s10.121027_42NB.100A_noisy_i22.5_6CE_NEW_interp9_defaultprior.probs"
photoz_file = "mock.r260.n1e6.s10.121027_42NB.100A_noisy_i22.5_6CE_NEW_interp9_defaultprior.bpz"

#BPZ..................................................
code = 'bpz'
id_index = 0
z_bpz_index = 1
z_true_index = 9 
odds_index = 5

#LePhare..............................................
#code = 'lephare'
#id_index = 0
#z_bpz_index = 1
#z_true_index = 7
#odds_index = 6

#Functions............................................
def plot_pdf():
	for n in range(0, n_gal, int(n_gal / n_pdf)):
		plt.plot(z, pz[n])
		plt.axvline(z_phot[n], color = 'black', label = 'zp = %2.2f odds = %2.2f' % (z_phot[n], odds[n]))
		plt.axvline(z_true[n], color = 'red', label = 'zt = %2.2f' % z_true[n])
		plt.xlim(xmax = 1.5)
		plt.legend()
		#plt.xlim(xmin = 0.2, xmax = 0.9)
		plt.xlabel('z')
		plt.ylabel('P(z)')

		np.savetxt(folder + 'pz/pz_' + str(n) + '.txt', np.array([z, pz[n]]).T, fmt = '%.5f')
		plt.savefig(folder + 'pz/pz_' + str(n) + '.png')
		plt.close()

def z_hist(z):
	hist, x = np.histogram(z, bins = edges) 
	return hist

def plot_z_hist():

	print "\nHISTOGRAM PARAMETERS:"
	print "\tNum. bins = %d" % n_bins
	print "\tz-range = [%3.3f,%3.3f]" % (z_min, z_max)
	print "\tWidth of bins = %3.3f" % width

	hist = z_hist(z_true)
	plt.fill_between(c_edges, hist, 0, label = 'z_true')
	hist = z_hist(z_phot)
	plt.plot(c_edges, hist, '-', color = 'r', linewidth=2.0, label = 'z_phot')
	hist = nz_pdf()
	np.savetxt(folder + "Nz.txt",np.array([c_edges, hist]).T, fmt = '%.5f')
	plt.plot(c_edges, hist, '-', color = 'g', linewidth=2.0, label = 'z_pdf')
	plt.legend()
	#plt.xlim(xmin = 0.2, xmax = 0.9)
	#plt.ylim(ymax = 700)
	plt.xlabel('z')
	plt.ylabel('Counts')
	#plt.savefig(folder + '/pz/z_hist.png')
	#plt.show()
	plt.savefig(folder + "Nz.png")
	plt.close()

def nz_pdf():

	#Looking for the pz array index of the low edge of the histogram
	i = 0
	while(z[i] <  z_min): i = i + 1 
	i_min = i - 1
	#print "zmin=",z[i_min]

	#Looking for the pz array index of the high edge of the histogram
	i = 0
	while(z[i] <  z_max): i = i + 1 
	i_max = i - 1
	#print "zmax=",z[i_max]

	s = np.zeros(n_bins)

	#Summing over all pdfs
	print "\nSUMMING:"
	for n in range(n_gal):
		sys.stdout.write("\r\tComplete %2.2f%%" % (100 * float(n) / float(n_gal)) )
		sys.stdout.flush()
		for i in range(n_bins):
			l = i_min + n_width * i
			r = l + n_width
			#print "zl, zr=",z[l], z[r]
			s[i] = s[i] + pz[n][l:r].sum()

	if(code == 'lephare'): s = (n_gal * s) / s.sum() 
	return s
	
#MAIN.................................................

print "******************************************"
print "*                                        *"
print "*         Photo-z PDFs by P.Marti        *" 
print "*                                        *"
print "******************************************"

#Reading probs and photoz output files
print "\nREADING INPUT FILES:\n\t..."
probs = np.loadtxt(probs_file)
bpz = np.loadtxt(photoz_file, unpack = True)

#Seeting main arrays
z_phot = bpz[z_bpz_index]
z_true = bpz[z_true_index]
odds = bpz[odds_index]
edges = np.arange(z_min, z_max + width, width)
print "edges,len(edges)=",edges,len(edges)
c_edges = edges[:-1] + (edges[1:] - edges[:-1]) / 2
print "c_edges,len(c_edges)=",c_edges,len(c_edges)

if(code == 'bpz'): 
	pz = np.delete(probs, 0, 1)
	#z = np.arange(0.01,2.01,z_resol)
	z = np.arange(0.01,6.505,z_resol)

if(code == 'lephare'): 
	pz = probs
	z = np.loadtxt(zph_file)

#Erase defectuos galaxies with nan pz
#rm_x_pos = []
#for i in range(len(pz)):
#	if(math.isnan(pz[i].sum())): rm_x_pos.append(i)
#pz = np.delete(pz, rm_x_pos, 0)
#z_phot = np.delete(z_phot, rm_x_pos, 0)
#z_true = np.delete(z_true, rm_x_pos, 0)
#odds = np.delete(odds, rm_x_pos, 0)

#Erase galaxies with low odds value 
#rm_x_pos = []
#for i in range(len(z_true)):
#	if(odds[i] < odds_cut): rm_x_pos.append(i)
#pz = np.delete(pz, rm_x_pos, 0)
#z_phot = np.delete(z_phot, rm_x_pos, 0)
#z_true = np.delete(z_true, rm_x_pos, 0)
#odds = np.delete(odds, rm_x_pos, 0)

n_width = int(width / z_resol)
n_bins = len(c_edges)
n_gal = len(pz)
print "\tn_gal =", n_gal
print "\tpdf resolution = %3.3f" % z_resol

#Call functions
#plot_pdf()
plot_z_hist()
