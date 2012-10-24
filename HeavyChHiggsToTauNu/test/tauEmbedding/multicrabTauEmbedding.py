#!/usr/bin/env python

import re
from optparse import OptionParser

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

# Default processing step
#defaultStep = "skim"
#defaultStep = "embedding"
defaultStep = "analysis"
#defaultStep = "analysisTau"
#defaultStep = "signalAnalysis"
#defaultStep = "signalAnalysisGenTau"
#defaultStep = "muonAnalysis"
#defaultStep = "caloMetEfficiency"

# Default embedding version(s) to use
defaultVersions = [
# "v13"
# "v13_1"
# "v13_2"
# "v13_2_seedTest1"
# "v13_2_seedTest2"
# "v13_2_seedTest3"
#    "v13_3",
#    "v13_3_seedTest1",
#    "v13_3_seedTest2",
#    "v13_3_seedTest3",
#    "v13_3_seedTest4",
#    "v13_3_seedTest5",
#    "v13_3_seedTest6",
#    "v13_3_seedTest7",
#    "v13_3_seedTest8",
#    "v13_3_seedTest9",
#    "v13_3_seedTest10",
#    "v14"
#    "v44_3_seed0",
#    "v44_3_seed1",
#    "v44_3_seed2",
    #"v44_2fix", # for hybrid event production only
    #"v44_2fix_seed1", # for hybrid event production only
    #"v44_2fix_seed2", # for hybrid event production only
#    "v44_4_seed0",

#    "v44_4_2" # skim version

#    "v44_4_2_muiso0"
#    "v44_4_2_muiso1"

    "v44_4_2_seed0",
#    "v44_4_2_seed1"
]
skimVersion = "v44_4_2"

# Define the processing steps: input dataset, configuration file, output file
config = {"skim":                 {"workflow": "tauembedding_skim_"+skimVersion,         "config": "muonSkim_cfg.py"},
          "embedding":            {"workflow": "tauembedding_embedding_%s",              "config": "embed.py"},
          "analysis":             {"workflow": "tauembedding_analysis_%s",               "config": "embeddingAnalysis_cfg.py"},
          "analysisTau":          {"workflow": "AOD is the input, wf missing?",          "config": "tauAnalysis_cfg.py"},
          "signalAnalysis":       {"workflow": "tauembedding_analysis_%s",               "config": "../signalAnalysis_cfg.py"},
          "signalAnalysisGenTau": {"workflow": "analysis_v44_4",                         "config": "../signalAnalysis_cfg.py"},
          "EWKMatching":          {"workflow": "tauembedding_analysis_%s",               "config": "../EWKMatching_cfg.py"},
          "muonAnalysis":         {"workflow": "tauembedding_skimAnalysis_"+skimVersion, "config": "muonAnalysisFromSkim_cfg.py"},
          "caloMetEfficiency":    {"workflow": "tauembedding_skimAnalysis_"+skimVersion, "config": "caloMetEfficiency_cfg.py"},
          }


# "Midfix" for multicrab directory name
dirPrefix = ""
#dirPrefix = "_vital"
#dirPrefix += "_Met50"
if defaultStep in ["signalAnalysis", "signalAnalysisGenTau"]:
    dirPrefix += "_systematics"

#dirPrefix += "_test"
#dirPrefix += "_debug"

# Define dataset collections
#datasetsData2010 = [
#    "Mu_136035-144114_Apr21", # HLT_Mu9
#    "Mu_146428-147116_Apr21", # HLT_Mu9
#    "Mu_147196-149294_Apr21", # HLT_Mu15_v1
#]
datasetsData2011 = [
    # Run2011A
    "SingleMu_160431-163261_2011A_Nov08",  # HLT_Mu20_v1
    "SingleMu_163270-163869_2011A_Nov08",  # HLT_Mu24_v2
    "SingleMu_165088-166150_2011A_Nov08", # HLT_Mu30_v3
    "SingleMu_166161-166164_2011A_Nov08", # HLT_Mu40_v1
    "SingleMu_166346-166346_2011A_Nov08", # HLT_Mu40_v2
    "SingleMu_166374-167043_2011A_Nov08", # HLT_Mu40_v1
    "SingleMu_167078-167913_2011A_Nov08", # HLT_Mu40_v3
    "SingleMu_170722-172619_2011A_Nov08",  # HLT_Mu40_v5
    "SingleMu_172620-173198_2011A_Nov08", # HLT_Mu40_v5
    "SingleMu_173236-173692_2011A_Nov08", # HLT_Mu40_eta2p1_v1
    # Run2011B
    "SingleMu_173693-177452_2011B_Nov19", # HLT_Mu40_eta2p1_v1
    "SingleMu_177453-178380_2011B_Nov19", # HLT_Mu40_eta2p1_v1
    "SingleMu_178411-179889_2011B_Nov19", # HLT_Mu40_eta2p1_v4
    "SingleMu_179942-180371_2011B_Nov19", # HLT_Mu40_eta2p1_v5
]
datasetsMCnoQCD = [
#    "TTJets_TuneZ2_Fall11",
#    "WJets_TuneZ2_Fall11",
#    "DYJetsToLL_M50_TuneZ2_Fall11",
    #"W2Jets_TuneZ2_Fall11",
    #"W3Jets_TuneZ2_Fall11",
    #"W4Jets_TuneZ2_Fall11",
    "T_t-channel_TuneZ2_Fall11",
    "Tbar_t-channel_TuneZ2_Fall11",
    "T_tW-channel_TuneZ2_Fall11",
    "Tbar_tW-channel_TuneZ2_Fall11",
    "T_s-channel_TuneZ2_Fall11",
    "Tbar_s-channel_TuneZ2_Fall11",
    "WW_TuneZ2_Fall11",
    "WZ_TuneZ2_Fall11",
    "ZZ_TuneZ2_Fall11",
]
datasetsMCQCD = [
    "QCD_Pt20_MuEnriched_TuneZ2_Fall11",
]
datasetsSignal = [
    "TTToHplusBWB_M80_Fall11",
    "TTToHplusBWB_M90_Fall11",
    "TTToHplusBWB_M100_Fall11",
    "TTToHplusBWB_M120_Fall11",
    "TTToHplusBWB_M140_Fall11",
    "TTToHplusBWB_M150_Fall11",
    "TTToHplusBWB_M155_Fall11",
    "TTToHplusBWB_M160_Fall11",
    "TTToHplusBHminusB_M80_Fall11",
    "TTToHplusBHminusB_M90_Fall11",
    "TTToHplusBHminusB_M100_Fall11",
    "TTToHplusBHminusB_M120_Fall11",
    "TTToHplusBHminusB_M140_Fall11",
    "TTToHplusBHminusB_M150_Fall11",
    "TTToHplusBHminusB_M155_Fall11",
    "TTToHplusBHminusB_M160_Fall11",
]

#datasetsData2011 = []
#datasetsMCnoQCD = []
#datasetsMCQCD = []
datasetsSignal = []
#datasetsData2011 = datasetsData2011B

#datasetsMCnoQCD = ["TTJets_TuneZ2_Fall11"]
#datasetsMCnoQCD = ["WJets_TuneZ2_Fall11"]
#datasetsMCnoQCD = ["DYJetsToLL_M50_TuneZ2_Fall11"]

def main():
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("--step", dest="step", default=defaultStep,
                      help="Processing step, one of %s (default: %s)" % (", ".join(config.keys()), defaultStep))
    parser.add_option("--version", dest="version", action="append", default=[],
                      help="Data version(s) to use as an input for 'analysis', 'signalAnalysis', or output for 'skim', 'embedding' (default: %s)" % ", ".join(defaultVersions))
    parser.add_option("--midfix", dest="midfix", default=dirPrefix,
                      help="String to add in the middle of the multicrab directory name (default: %s)" % dirPrefix)
    parser.add_option("--configOnly", dest="configOnly", action="store_true", default=False,
                      help="Generate multicrab configurations only, do not create crab jobs (default is to create crab jobs)")

    (opts, args) = parser.parse_args()
    step = opts.step
    versions = opts.version
    if len(versions) == 0:
        versions = defaultVersions

    tmp = "Processing step %s" % step
    if step in ["skim", "embedding", "analysis", "signalAnalysis","EWKMatching"]:
        inputOutput = "input"
        if step in ["skim", "embedding"]:
            inputOutput = "output"
        if step == "skim" and len(versions) > 1:
            raise Exception("There should be no need to run skim with multiple output versions, you specified %d versions" % len(versions))

        tmp += ", embedded versions '%s' as %s" % (", ".join(versions), inputOutput)
        print tmp

        for v in versions:
            print "########################################"
            print
            print " Creating tasks for embedding %s %s" % (inputOutput, v)
            print
            print "########################################"

            createTasks(opts, step, v)
    else:
        print tmp
        createTasks(opts, step)


def createTasks(opts, step, version=None):
    # Pick crab.cfg
    crabcfg = "crab.cfg"
    if step in ["analysis", "analysisTau", "signalAnalysis", "signalAnalysisGenTau", "muonAnalysis", "caloMetEfficiency","EWKMatching"]:
        crabcfg = "../crab_analysis.cfg"

    # Setup directory naming
    dirName = ""
    if step in ["embedding", "analysis", "signalAnalysis", "EWKMatching"]:
        dirName += "_"+version
    dirName += opts.midfix

    # Create multicrab
    multicrab = Multicrab(crabcfg, config[step]["config"], lumiMaskDir="..")


    # Select the datasets based on the processing step and data era
    datasets = []
    if step in ["analysisTau", "signalAnalysisGenTau"]:
        datasets.extend(datasetsMCnoQCD)
    else:
    #    datasets.extend(datasetsData2010)
        datasets.extend(datasetsData2011)
        datasets.extend(datasetsMCnoQCD)
        datasets.extend(datasetsMCQCD)
    if step in ["skim", "embedding", "signalAnalysis","EWKMatching"]:
        datasets.extend(datasetsSignal)

    # Setup the version number for tauembedding_{embedding,analysis} workflows
    workflow = config[step]["workflow"]
    if step in ["embedding", "analysis", "signalAnalysis","EWKMatching"]:
        workflow = workflow % version

    multicrab.extendDatasets(workflow, datasets)

    multicrab.appendLineAll("GRID.maxtarballsize = 30")
    if not step in ["skim", "analysisTau"]:
        multicrab.extendBlackWhiteListAll("ce_white_list", ["jade-cms.hip.fi"])

    # Let's do the naming like this until we get some answer from crab people
    if step in ["skim", "embedding"]:
        multicrab.addCommonLine("USER.publish_data_name = Tauembedding_%s_%s" % (step, version))

    # For this workflow we need one additional command line argument
    if step == "signalAnalysisGenTau":
        multicrab.appendArgAll("doTauEmbeddingLikePreselection=1")

    multicrab.extendBlackWhiteListAll("se_black_list", defaultSeBlacklist)

    # Create multicrab task(s)
    prefix = "multicrab_"+step+dirName
    taskDirs = multicrab.createTasks(configOnly = opts.configOnly, prefix=prefix, over500JobsMode=Multicrab.SPLIT)
        
    # patch CMSSW.sh
    if not opts.configOnly and step in ["skim", "embedding"]:
        import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crabPatchCMSSWsh as patch
        import os
        for td, dsets in taskDirs:
            os.chdir(td)
            patch.main(Wrapper(dirs=dsets, input={"skim": "skim",
                                                  "embedding": "embedded"}[step]))
            os.chdir("..")

    if len(taskDirs) > 1:
        print 
        print "Created multicrab directories"
        print "\n".join( [x[0] for x in taskDirs] )

# patch CMSSW.sh
class Wrapper:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)



if __name__ == "__main__":
    main()
