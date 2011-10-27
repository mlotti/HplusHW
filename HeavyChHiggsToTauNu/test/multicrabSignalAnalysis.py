#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *


cfg = "signalAnalysis_cfg.py"
#cfg = "QCDMeasurement_cfg.py"
multicrab = Multicrab("crab_analysis.cfg", cfg)

# Select the pattuple version to use as an input
pattupleVersion = "pattuple_v18"

#era = "EPS"
era = "Run2011A"

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
datasetsEPS = [
        "Tau_160431-161176_May10",           # HLT_IsoPFTau35_Trk20_MET45_v1
        "Tau_161217-163261_May10",           # HLT_IsoPFTau35_Trk20_MET45_v2
        "Tau_163270-163869_May10",           # HLT_IsoPFTau35_Trk20_MET45_v4
        "Tau_165088-165633_Prompt",          # HLT_IsoPFTau35_Trk20_MET45_v6
        "Tau_165970-166164_Prompt",          # HLT_IsoPFTau35_Trk20_MET60_v2
        "Tau_166346-166346_Prompt",          # HLT_IsoPFTau35_Trk20_MET60_v3
        "Tau_166374-167043_Prompt",          # HLT_IsoPFTau35_Trk20_MET60_v2
        "Tau_167078-167913_Prompt",          # HLT_IsoPFTau35_Trk20_MET60_v4
]
datasetsRun2011A = datasetsEPS + [
        "Tau_170722-172619_Aug05",           # HLT_IsoPFTau35_Trk20_MET60_v6
        "Tau_172620-173198_Prompt",          # HLT_IsoPFTau35_Trk20_MET60_v6
        "Tau_173236-173692_Prompt",          # HLT_MediumIsoPFTau35_Trk20_MET60_v1
]

datasetsMC = [
        # MC Signal (WH)
        "TTToHplusBWB_M80_Summer11",
        "TTToHplusBWB_M90_Summer11",
        "TTToHplusBWB_M100_Summer11",
        "TTToHplusBWB_M120_Summer11",
        "TTToHplusBWB_M140_Summer11",
        "TTToHplusBWB_M150_Summer11",
        "TTToHplusBWB_M155_Summer11",
        "TTToHplusBWB_M160_Summer11",

        # MC Signal (HH)
        "TTToHplusBHminusB_M80_Summer11",
        "TTToHplusBHminusB_M90_Summer11",
        "TTToHplusBHminusB_M100_Summer11",
        "TTToHplusBHminusB_M120_Summer11",
        "TTToHplusBHminusB_M140_Summer11",
        "TTToHplusBHminusB_M150_Summer11",
        "TTToHplusBHminusB_M155_Summer11",
        "TTToHplusBHminusB_M160_Summer11",

	# MC Signal (heavy H+ from process pp->tbH+)
#        "HplusTB_M180_Summer11",
#        "HplusTB_M190_Summer11",
#        "HplusTB_M200_Summer11",
#        "HplusTB_M220_Summer11",
#        "HplusTB_M250_Summer11",
#        "HplusTB_M300_Summer11",

        # MC Background
        "QCD_Pt30to50_TuneZ2_Summer11",
        "QCD_Pt50to80_TuneZ2_Summer11",
        "QCD_Pt80to120_TuneZ2_Summer11",
        "QCD_Pt120to170_TuneZ2_Summer11",
        "QCD_Pt170to300_TuneZ2_Summer11",
        "QCD_Pt300to470_TuneZ2_Summer11",
        "TTJets_TuneZ2_Summer11",
        "WJets_TuneZ2_Summer11",
        "DYJetsToLL_M50_TuneZ2_Summer11",
        "T_t-channel_TuneZ2_Summer11",
        "Tbar_t-channel_TuneZ2_Summer11",
        "T_tW-channel_TuneZ2_Summer11",
        "Tbar_tW-channel_TuneZ2_Summer11",
        "T_s-channel_TuneZ2_Summer11",
        "Tbar_s-channel_TuneZ2_Summer11",
        "WW_TuneZ2_Summer11",
        "WZ_TuneZ2_Summer11",
        "ZZ_TuneZ2_Summer11",
        ]

datasets = []
if era == "EPS":
    datasets += datasetsEPS
elif era == "Run2011A":
    datasets += datasetsRun2011A
else:
    raise Exception("Wrong value for 'era' %s, supported are 'EPS', 'Run2011A'" % era)
datasets += datasetsMC

# Add the datasest to the multicrab system
multicrab.extendDatasets(pattupleVersion, datasets)

output = ["histograms.root"]
if "signalAnalysis" in cfg:
    output.append("pickEvents.txt")
multicrab.addCommonLine("CMSSW.output_file = %s" % ",".join(output))

# Set the era to MC datasets
def setPuEra(dataset):
    if dataset.isMC():
        dataset.appendArg("puWeightEra="+era)
multicrab.forEachDataset(setPuEra)

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

# Generate configuration only
#multicrab.createTasks(prefix=prefix, configOnly=True)

# Genenerate configuration and create the crab tasks
multicrab.createTasks(prefix=prefix)
