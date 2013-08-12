import numpy as np

#PARAMETERS......................
folder_name = "./"
file_name = "mock.r260.n1e6.s10.121027_42NB.100A_noisy_i22.5_6CE_NEW_interp9_calibratedprior.bpz" 
file_path = folder_name + file_name 

binning = {}
binning['magnitude'] = np.arange(16,22.5,0.5)
binning['redshift'] = np.arange(0,1.2,0.1)
binning['type'] = np.arange(1,6,0.5)

xtick = {}
xtick['magnitude'] = np.arange(17,22,1)
xtick['redshift'] = np.arange(0.2,1.2,0.2)
xtick['type'] = np.arange(2,6,1)

ytick = {}
ytick['scatter'] = np.arange(-0.3,0.4,0.2)
ytick['histogram'] = np.arange(5000,16000,5000)
ytick['completeness'] = np.arange(20,81,20)
ytick['bias'] = np.arange(-0.0015,0.002,0.001)
ytick['sigma'] = np.arange(0.2,1.5,0.4)
ytick['outliers'] = np.arange(2,13,2)


estim_list = ['scatter', 'histogram', 'completeness', 'bias', 'sigma', 'outliers']
estim_label = {'scatter': 'z(ph)-z(tr)', 'histogram': 'Counts', 'completeness': 'Efficiency (%)', 'bias': 'Median', 'sigma': '$\sigma_{68}$ (%)', 'outliers': 'Outliers (%)'}
val_max = {'scatter':0.4, 'histogram':20000,'completeness':100, 'bias': 0.0025, 'sigma': 1.5, 'outliers': 15}
val_req = {'scatter':0., 'histogram': 0,'completeness': 0, 'bias': 0., 'sigma': 0.35, 'outliers': 3}

title = 'Photo-z performance for the PAU Bright Sample $i_{AB}<22.5$'

col_list = {'magnitude':10, 'redshift':1, 'type':4}
#col_list = {'redshift':1}
zt_col = 9
od_col = 5      #Odds or error column: in the case of error column set error to True in the line below, otherwise set it to False.
error = 'False'

#col = [10,1,4,9,5] #m, z, t, zt, od
                   #od_cut = [0.,0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
od_cut = [0.0,0.2,0.4,0.6,0.8]
