import sys

from HiggsAnalysis.NtupleAnalysis.main import Process, PSet, Analyzer
from HiggsAnalysis.NtupleAnalysis.AnalysisBuilder import AnalysisBuilder

from HiggsAnalysis.NtupleAnalysis.parameters.hplus2hwAnalysis import allSelections


import ROOT

###################
## OPTIONS
###################

prefix      = "Hplus2hwAnalysis"
postfix     = " "
dataEras    = ["2016"]
searchModes = ["1500to3000"]

ROOT.gErrorIgnoreLevel = 0

blacklist = ["ChargedHiggs_HplusTB_HplusToTauNu_M_350_2tau","ChargedHiggs_HplusTB_HplusToTauNu_M_1500_2tau","ZJetsToQQ_HT600toInf","QCD_Pt_50to80","QCD_Pt_80to120","QCD_Pt_120to170","QCD_Pt_170to300","QCD_Pt_300to470","WJetsToLNu_old"]
whitelist = []

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

#    process.addDatasetsFromMulticrab(sys.argv[1])
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
                              doSystematicVariations = False
			      )



    builder.build(process, allSelections)


    process.run()


if __name__ == "__main__":
    main()
