import pweave as pw
import os as os
import pweave as pw
from parameters import *

os.system("cp $ROUTINESPATH/pz_report/pz_report.Plw ./" + code + "_" + cat_file[:-4] + "_report.Plw")
pw.pweave(code + "_" + cat_file[:-4] + "_report.Plw", doctype = 'tex')
os.system("rm " + code + "_" + cat_file[:-4] + "_report.Plw")


