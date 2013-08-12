import numpy as np

#PARAMETERS......................
folder_name = "./"
file_name = "annz_cosmos.txt" 
file_path = folder_name + file_name 

binning = {}
binning['magnitude'] = np.arange(17,23.,0.5)
binning['redshift'] = np.arange(0,1.5,0.1)
binning['type'] = np.arange(1,6,0.5)

xtick = {}
xtick['magnitude'] = np.arange(20,24,1)
xtick['redshift'] = np.arange(0.2,1.4,0.2)
xtick['type'] = np.arange(2,6,1)

ytick = {}
ytick['scatter'] = np.arange(-0.9,0.9,0.4)
ytick['histogram'] = np.arange(500,3900,500)
ytick['completeness'] = np.arange(20,81,20)
ytick['bias'] = np.arange(-0.27,0.24,0.1)
ytick['sigma'] = np.arange(4,28,4)
ytick['outliers'] = np.arange(2,13,2)

estim_list = ['sigma']
estim_label = {'scatter': 'z(ph)-z(tr)', 'histogram': 'Counts', 'completeness': 'Efficiency (%)', 'bias': 'Median', 'sigma': '$\sigma_{68}$ (%)', 'outliers': 'Outliers (%)'}
val_max = {'scatter':1.2, 'histogram':4000,'completeness':100, 'bias': 0.25, 'sigma': 30., 'outliers': 15}
val_req = {'scatter':0., 'histogram': 0,'completeness': 0, 'bias': 0., 'sigma': 12.0, 'outliers': 1.5}

title = 'Photo-z performance for DES-VVDS with Calibrated prior'

#col_list = {'magnitude':16, 'redshift':1, 'type':4}
#col_list = {'redshift':0}
col_list = {'magnitude':3}
zt_col = 0 
zp_col = 1
od_col = 2      #Odds or error column: in the case of error column set error to True in the line below, otherwise set it to False.
error = 'False'
od_cut = [0]
