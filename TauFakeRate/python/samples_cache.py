import TauAnalysis.TauIdEfficiency.tools.castor_mirror as mirror

# Import the samples into this namespace
#from samples import qcd_mc, minbias_mc, ztautau_mc, data
from samples import *

mirror.LOCAL_DIRECTORY = "/tmp/tau_commissioning"

_sample_list = [data, minbias_mc, qcd_mc, ztautau_mc, ]

# Update the samples to use any existing local files
for sample in _sample_list:
    mirror.update_sample_to_use_local_files(sample)

# Script usage - copy all files 
if __name__ == "__main__":
    print "Copying CASTOR files to local area:", mirror.LOCAL_DIRECTORY
    # 20 concurrent rfcp jobs
    mirror.mirror_samples(_sample_list, max_jobs = 20)




