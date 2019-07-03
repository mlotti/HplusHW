import sys

from HiggsAnalysis.NtupleAnalysis.main import Process, PSet, Analyzer
from HiggsAnalysis.NtupleAnalysis.AnalysisBuilder import AnalysisBuilder
from HiggsAnalysis.NtupleAnalysis.parameters.hplus2hwAnalysis_muon import allSelections

import ROOT

###################
## OPTIONS
###################

prefix      = "Hplus2hwAnalysis"
postfix     = " "
dataEras    = ["2016"]
searchModes = ["350to3000"]

ROOT.gErrorIgnoreLevel = 0

#blacklist = ["SingleMuon_Run2016E_03Feb2017_v1_276831_277420","SingleMuon_Run2016F_03Feb2017_v1_277932_278800","SingleMuon_Run2016F_03Feb2017_v1_278801_278808","SingleMuon_Run2016D_03Feb2017_v1276315_276811","SingleMuon_Run2016G_03Feb2017_v1_278820_280385","SingleMuon_Run2016H_03Feb2017_ver2_v1_281613_284035"]

blacklist = ["SingleElectron_Run2016B_03Feb2017_ver2_v2_273150_275376",
  "SingleElectron_Run2016C_03Feb2017_v1_275656_276283",
  "SingleElectron_Run2016D_03Feb2017_v1_276315_276811",
  "SingleElectron_Run2016E_03Feb2017_v1_276831_277420",
  "SingleElectron_Run2016F_03Feb2017_v1_277932_278800",
  "SingleElectron_Run2016F_03Feb2017_v1_278801_278808",
  "SingleElectron_Run2016G_03Feb2017_v1_278820_280385",
  "SingleElectron_Run2016H_03Feb2017_ver2_v1_281613_284035",
  "SingleElectron_Run2016H_03Feb2017_ver3_v1_284036_284044"]


#blacklist = []

#whitelist = ["DYJetsToLL_M_50_ext1","SingleMuon_Run2016G_03Feb2017_v1_278820_280385","SingleMuon_Run2016H_03Feb2017_ver2_v1_281613_284035","SingleMuon_Run2016H_03Feb2017_ver3_v1_284036_284044"]
#whitelist= ["TT","SingleMuon_Run2016F_03Feb2017_v1_278801_278808"]
whitelist= []

###################
## MAIN
###################

def main():


    # Require at least two arguments (script-name, path to multicrab)
    if len(sys.argv) < 2:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        sys.exit(0)
    else:
        pass


    ###################
    ## SETUP THE PROCESS
    ###################

    maxEvents = {}

    process = Process(prefix, maxEvents = maxEvents)


    ###################
    ## ADD DATASETS
    ###################

    process.addDatasetsFromMulticrab(sys.argv[1],blacklist=blacklist,whitelist=whitelist)


    ##################
    ## BUILD ANALYSIS MODULES
    ###################

    builder = AnalysisBuilder(prefix,
                              dataEras,
                              searchModes,
			      ### OPRIONS ###
                              usePUreweighting       = True,
                              useTopPtReweighting    = False,
                              doSystematicVariations = False,
			      analysisType 	     = "HToHW")



    builder.build(process, allSelections)


    process.run()


if __name__ == "__main__":
    main()
