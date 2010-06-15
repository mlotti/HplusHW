from TauAnalysis.TauIdEfficiency.ntauples.sample_builder import build_sample
import os

'''

samples.py

Central defintion of data sources for commissioning.

$Id: samples.py,v 1.4 2010/06/12 00:39:01 friis Exp $

'''

# Locations of the luminosity maps
_DATA_LUMI_MAP_FILE = os.path.join(
    os.environ['CMSSW_BASE'], 'src/TauAnalysis/TauIdEfficiency/test/'
    'commissioning', 'dataLumiMap.json')

_MC_LUMI_MAP_FILE = os.path.join(
    os.environ['CMSSW_BASE'], 'src/TauAnalysis/TauIdEfficiency/test/'
    'commissioning', 'mcLumiMap.json')


# Arugments: lumi map file, name of output collection, merge/add, list of samples
# to take from the JSON file
print "loading definition of Ztautau signal Monte Carlo samples..."
ztautau_mc = build_sample(_MC_LUMI_MAP_FILE, "mc_ztt", "merge", "Ztautau")

# Merge multiple pt hat bins
print "loading definition of QCD background Monte Carlo samples..."
qcd_mc = build_sample(_MC_LUMI_MAP_FILE, "mc_qcd", "merge", "QCD_Pt15", "QCD_Pt30", "QCD_Pt80", "QCD_Pt170")
#qcd_mc = build_sample(_MC_LUMI_MAP_FILE, "mc_qcd", "merge", "QCD_Pt15")

print "loading definition of min. Bias background Monte Carlo samples..."
minbias_mc = build_sample(_MC_LUMI_MAP_FILE, "mc_minbias", "merge", "minBias")

# For data, we use the add mode, to concatenate data
print "loading definition of Data samples..."
data = build_sample(_DATA_LUMI_MAP_FILE, "data", "add", "Data_part01")
