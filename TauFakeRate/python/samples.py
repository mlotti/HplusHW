from TauAnalysis.TauIdEfficiency.ntauples.sample_builder import build_sample
import os

'''

samples.py

Central defintion of data sources for commissioning.

$Id: samples.py,v 1.6 2010/06/17 00:41:43 friis Exp $

'''

# Locations of the luminosity maps
_DATA_LUMI_MAP_FILE = os.path.join(
    os.environ['CMSSW_BASE'], 'src/HiggsAnalysis/TauFakeRate/data/'
    '', 'dataLumiMap.json')

_MC_LUMI_MAP_FILE = os.path.join(
    os.environ['CMSSW_BASE'], 'src/HiggsAnalysis/TauFakeRate/data/'
    '', 'mcLumiMap.json')


# Arugments: lumi map file, name of output collection, merge/add, list of samples
# to take from the JSON file
print "loading definition of Ztautau signal Monte Carlo samples..."
ztautau_mc = build_sample(_MC_LUMI_MAP_FILE, "mc_ztt", "merge", datasets = ["Ztautau"])

# Merge multiple pt hat bins
#
# CV: restrict analysis to first pt hat bin for now...
#
print "loading definition of QCD background Monte Carlo samples..."
##qcd_mc = build_sample(_MC_LUMI_MAP_FILE, "mc_qcd", "merge", "QCD_Pt15", "QCD_Pt30", "QCD_Pt80", "QCD_Pt170")
qcd_mc = build_sample(_MC_LUMI_MAP_FILE, "mc_qcd", "merge", datasets = ["QCD_Pt15"])

print "loading definition of min. Bias background Monte Carlo samples..."
minbias_mc = build_sample(_MC_LUMI_MAP_FILE, "mc_minbias", "merge", datasets = ["minBias"])

# For data, we use the add mode, to concatenate data
print "loading definition of Data samples..."
data = build_sample(_DATA_LUMI_MAP_FILE, "data", "add", datasets = ["Data_part01"])

# Small test mc sample
print "loading mc test"
mc_test   = build_sample(_MC_LUMI_MAP_FILE, "mc_test", "merge", datasets = ["MC_test"])

# Small test data sample
print "loading data test"
data_test = build_sample(_DATA_LUMI_MAP_FILE, "data_test", "add", datasets = ["Data_test"])

