#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *


cfg = "signalAnalysis_cfg.py"
#cfg = "signalAnalysis2_cfg.py"
#cfg = "QCDMeasurement_cfg.py"
multicrab = Multicrab("crab_analysis.cfg", cfg)

# Select the workflow (version corresponds to pattuples)
#workflow = "analysis_v25c"
workflow = "analysis_v44_4"

# Change this to true if you want to run the PAT on the fly (for
# datasets where no pattuples are produced, or for testing something
# where information not stored in pattuples is needed). 
runPatOnTheFly = False
#runPatOnTheFly = True
if runPatOnTheFly:
    pattupleVersion = "AOD"


# Uncomment below the datasets you want to process
# The dataset definitions are in python/tools/multicrabDatasets.py

# Data: single tau + MET
datasetsData = [
    "Tau_160431-167913_2011A_Nov08",    # 2011A HLT_IsoPFTau35_Trk20_MET45_v{1,2,4,6}, 2011A HLT_IsoPFTau35_Trk20_MET60_v{2,3,4}
    "Tau_170722-173198_2011A_Nov08",    # 2011A HLT_IsoPFTau35_Trk20_MET60_v6
    "Tau_173236-173692_2011A_Nov08",    # 2011A HLT_MediumIsoPFTau35_Trk20_MET60_v1]
    "Tau_175832-180252_2011B_Nov19",    # 2011B HLT_MediumIsoPFTau35_Trk20_MET60_v{1,5,6}
]

datasetsMC = [
        # MC Signal (WH)
        "TTToHplusBWB_M80_Fall11",
        "TTToHplusBWB_M90_Fall11",
        "TTToHplusBWB_M100_Fall11",
        "TTToHplusBWB_M120_Fall11",
        "TTToHplusBWB_M140_Fall11",
        "TTToHplusBWB_M150_Fall11",
        "TTToHplusBWB_M155_Fall11",
        "TTToHplusBWB_M160_Fall11",

        # MC Signal (HH)
        "TTToHplusBHminusB_M80_Fall11",
        "TTToHplusBHminusB_M90_Fall11",
        "TTToHplusBHminusB_M100_Fall11",
        "TTToHplusBHminusB_M120_Fall11",
        "TTToHplusBHminusB_M140_Fall11",
        "TTToHplusBHminusB_M150_Fall11",
        "TTToHplusBHminusB_M155_Fall11",
        "TTToHplusBHminusB_M160_Fall11",

	# MC Signal (heavy H+ from process pp->tbH+)
        "HplusTB_M180_Fall11",
        "HplusTB_M190_Fall11",
        "HplusTB_M200_Fall11",
        "HplusTB_M220_Fall11",
        "HplusTB_M250_Fall11",
        "HplusTB_M300_Fall11",

        # MC Background
        "QCD_Pt30to50_TuneZ2_Fall11",
        "QCD_Pt50to80_TuneZ2_Fall11",
        "QCD_Pt80to120_TuneZ2_Fall11",
        "QCD_Pt120to170_TuneZ2_Fall11",
        "QCD_Pt170to300_TuneZ2_Fall11",
        "QCD_Pt300to470_TuneZ2_Fall11",
#       "QCD_Pt20_MuEnriched_TuneZ2_Fall11",
        "TTJets_TuneZ2_Fall11",
        "WJets_TuneZ2_Fall11",
        "W2Jets_TuneZ2_Fall11",
        "W3Jets_TuneZ2_Fall11",
        "W4Jets_TuneZ2_Fall11",
        "DYJetsToLL_M50_TuneZ2_Fall11",
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

datasets = []
datasets.extend(datasetsData)
datasets.extend(datasetsMC)

# Add the datasest to the multicrab system
multicrab.extendDatasets(workflow, datasets)

output = ["histograms.root"]
if "signalAnalysis" in cfg:
    output.append("pickEvents.txt")
multicrab.addCommonLine("CMSSW.output_file = %s" % ",".join(output))

# Force all jobs go to jade, in some situations this might speed up
# the analysis (e.g. when there are O(1000) Alice jobs queueing, all
# CMS jobs typically go to korundi).
#if not runPatOnTheFly:
#    multicrab.extendBlackWhiteListAll("ce_white_list", ["jade-cms.hip.fi"])


# If PAT is ran on the fly, add the
# "doPat=1" command line argument for all datasets. In addition it
# could be wise to decrease the number of jobs as the defaults are
# adjusted for the pattuple file size, and when only histograms or
# small ntuples are produced, stageout is not the issue
if runPatOnTheFly:
    multicrab.appendArgAll("doPat=1")

    #multicrab.modifyLumisPerJobAll(lambda nlumis: nlumis*2)
    #multicrab.modifyNumberOfJobsAll(lambda njobs: njobs*0.5)

prefix = "multicrab"
if "QCD" in cfg:
    prefix += "_QCD"

# Generate configuration only?
configOnly=True
#configOnly=False
# Genenerate configuration and create the crab tasks
multicrab.createTasks(prefix=prefix, configOnly=configOnly)

