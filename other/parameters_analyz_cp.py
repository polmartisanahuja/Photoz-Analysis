import numpy as np

#PARAMETERS......................
folder_name = "/Users/polstein/Desktop/des-sv_photoz_output/"
#file_name = "des_all_detmodel_spec_prior_non_cdfs.bpz" 
#file_path = folder_name + file_name 

binning = {}
binning['m'] = np.arange(19,25.,0.5)
binning['zt'] = np.arange(0,1.5,0.1)
binning['zp'] = np.arange(0,1.5,0.1)

xtick = {}
xtick['m'] = np.arange(20,25,1)
xtick['zt'] = np.arange(0.2,1.4,0.2)
xtick['zp'] = np.arange(0.2,1.4,0.2)

ytick = {}
ytick['histogram'] = np.arange(0.1,0.5,0.1)
ytick['median'] = np.arange(-0.3,0.3,0.1)
ytick['sigma'] = np.arange(0.02,0.34,0.05)
ytick['sigma68'] = np.arange(0.05,0.44,0.1)
ytick['of2_rms'] = np.arange(2,20,4)
ytick['of3_rms'] = np.arange(2,13,2)

#estim_list = ['mean', 'median', 'rms', 'sigma68', 'of2_rms' 'of3_rms']
estim_list = ['histogram','median','sigma68','of2_rms','of3_rms']
#field_list = ['vvds02hr', 'vvdsf14', 'cdfs', 'cosmos']
field_list = ['vvds02hr']
colors = ['blue', 'red', 'cyan', 'green']
#colors = ['blue', 'red', 'cyan', 'green']
#field_list = ['vvds02hr', 'cdfs']
N_gal = [1543,1495,1799,3114]
#N_gal = [1543,1799]
zp_col = [1,1,1]
#zt_col = [9,31,0] 
zt_col = [9,33,0] 
m_col = [10,17,3] 
#m_col = [10,16,3] 
code_list = ['bpz','lephare','annz']
estim_label = {'histogram': 'N', 'median': 'Bias', 'rms': '$\sigma$', 'sigma68': '$\sigma_{68}$', 'of2_rms':'>2$\sigma$ (%)', 'of3_rms': '>3$\sigma$ (%)'}
val_max = {'histogram': 0.3,'mean': 0.25, 'median': 0.25, 'rms': 0.15, 'sigma68': 0.4, 'of2_rms': 20, 'of3_rms': 7}
val_min = {'histogram': 0,'mean': -0.25, 'median': -0.25, 'rms': 0.15, 'sigma68': 0.01, 'of2_rms': 0, 'of3_rms': 0}
val_req = {'histogram': 0, 'mean': 0., 'median': 0., 'rms': 0.12, 'sigma68': 0.12, 'of2_rms': 10, 'of3_rms': 1.5}

title = 'Photo-z performance for DES-SV fields'
