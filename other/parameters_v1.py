import numpy as np

#PARAMETERS......................
folder_name = "/Users/polstein/Desktop/"
file_name = "bright.bpz"
file_path = folder_name + file_name 

binning = {}
binning['magnitude'] = np.arange(16,22.5,0.5)
binning['redshift'] = np.arange(0,1.2,0.1)
binning['type'] = np.arange(1,6,0.5)

estim_list = ['scatter', 'histogram', 'completeness', 'bias', 'sigma', 'outliers']
estim_label = {'scatter': ' Scatter $\Delta z$', 'histogram': 'Counts', 'completeness': 'Efficiency (%)', 'bias': 'Median', 'sigma': '$\sigma_{68}$ (%)', 'outliers': 'Outliers (%)'}
val_max = {'scatter':0.2, 'histogram':4000,'completeness':100, 'bias': 0.005, 'sigma': 1.5, 'outliers': 15}
val_req = {'scatter':0., 'histogram': 0,'completeness': 0, 'bias': 0., 'sigma': 0.35, 'outliers': 3}

val_list = ['magnitude', 'redshift', 'type']
col = [10,1,4,9,5] #m, z, t, zt, od
od_cut = [0., 0.45, 0.65, 0.8]

