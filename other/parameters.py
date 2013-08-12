import numpy as np

#Input parameters.........................................
survey_name = "DES-VVDS "
author = "Pol Marti Sanahuja"
cat_file = "/Users/polstein/Dropbox/PhD_pmarti/Data/Photoz/DES-SV/vvds02hr/des_vvds02hr_detmodel_petro_JHK_spec_prior.bpz" 
plot_folder = "./plot"

code = "BPZ"
qual_para = "odds"

#Fields positions.........................................
zp_col = 1 #Column where the z(photo) in the catalog is
zp_min_col = 2 #Column where the z(photo) lower limit due to photo-z error is
zp_max_col = 3 #Column where the z(photo) upper limit due to photo-z error is
zt_col = 9 #Column where the z(true) in the catalog is
odds_col = 5

#Catalog cuts.............................................
#z_cut = 10.0 #Removes all galaxies with z > z_cut
#odds_cut = 0.0 #Removes all galaxies with odds < odds_cut
z_cut = 10.0 #Removes all galaxies with z > z_cut
odds_cut = 0.0 #Removes all galaxies with odds < odds_cut
#odds_cut = 0.65 #Removes all galaxies with odds < odds_cut

#Scientific Requeriments..................................
bias_ref = 0. #Scientific requeriment for the bias
sigma_ref = 0.12 #Scientific requeriment for the photo-z precision
outliers2_ref = 0.1 #Scientific requeriment for the 2sigma outliers fractions
outliers3_ref = 0.015 #Scientific requeriment for the 3sigma outliers fractions

#Predefined Binning.......................................
n_bins = 15 #Number of bins equalsized across the z axis where estimators will be computed
z_min = 0. #Lower limit of the z range analisis
z_max = 1.5 #Upper limit of the z range analisis
od_bin = 0.05 #Width of the quality parameter bins

#Metrics plots limits.....................................
Dz_range = 0.75 # (-Dz_range, Dz_range) is the range where dzvsz and biasvsz plots will be plotted 
delta_z_str = "$\Delta z$"
#delta_z_str = "$\Delta z/(1+z)$"
yrange_sigma = 5
yrange_out2 = 0.3
yrange_out3 = 0.3
nzvsz_ymax = 7000
