#!/usr/bin/env python

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabWorkflows as multicrabWorkflows
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

cfg = "signalAnalysis_cfg.py"
#cfg = "signalAnalysis2_cfg.py"
#cfg = "QCDMeasurement_cfg.py"
multicrab = Multicrab("crab_analysis.cfg", cfg)

# Select the workflow (version corresponds to pattuples)
#workflow = "analysis_v44_4"

# Tau+MET trigger
workflow = "analysis_taumet_v53_2"

# QuadJet80 tritgger
#workflow = "analysis_quadjet_v53_2"

# QuadJet75_55_38_20_BTagIP_VBF trigger
#workflow = "analysis_quadjetbtag_v53_2"

# QuadPFJet75_55_38_20_BTagCSV_VBF trigger for data
# QuadPFJetXX_61_44_31_BTagCSV_VBF trigger for MC, XX specified below with mc_pfjettrigger variable
#workflow = "analysis_quadpfjetbtag_v53_2"
mc_pfjettrigger = "78"
#mc_pfjettrigger = "82"


# Do W+jets weighting?
doWJetsWeighting = False
doWJetsWeighting = True

# Change this to true if you want to run the PAT on the fly (for
# datasets where no pattuples are produced, or for testing something
# where information not stored in pattuples is needed). 
runPatOnTheFly = False
#runPatOnTheFly = True
if runPatOnTheFly:
    raise Exception("runPatOnTheFly is not supported ATM")

# For minimal set of datasets remove the 200k signal samples, and
# single top signal samples
minimalDatasets = True
minimalDatasets = False


# Uncomment below the datasets you want to process
# The dataset definitions are in python/tools/multicrabWorkflows.py

# Data: single tau + MET
datasetsData_2011 = [
    "Tau_160431-167913_2011A_Nov08",    # 2011A HLT_IsoPFTau35_Trk20_MET45_v{1,2,4,6}, 2011A HLT_IsoPFTau35_Trk20_MET60_v{2,3,4}
    "Tau_170722-173198_2011A_Nov08",    # 2011A HLT_IsoPFTau35_Trk20_MET60_v6
    "Tau_173236-173692_2011A_Nov08",    # 2011A HLT_MediumIsoPFTau35_Trk20_MET60_v1]
    "Tau_175832-180252_2011B_Nov19",    # 2011B HLT_MediumIsoPFTau35_Trk20_MET60_v{1,5,6}
]

datasetsMC_2011 = [
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

datasetsData_Tau_2012 = [
    "Tau_190456-190738_2012A_Jul13",
    "Tau_190782-190949_2012A_Aug06",
    "Tau_191043-193621_2012A_Jul13",
    "Tau_193834-196531_2012B_Jul13",
    "Tau_198022-198523_2012C_Aug24",
    "Tau_198941-202504_2012C_Prompt",
    "Tau_201191-201191_2012C_Dec11",
    "Tau_202972-203742_2012C_Prompt",
    "Tau_203777-208686_2012D_Prompt",
]

datasetsData_MultiJet_2012 = [
    "MultiJet_190456-190738_2012A_Jul13",
    "MultiJet_190782-190949_2012A_Aug06",
    "MultiJet_191043-193621_2012A_Jul13",
    "MultiJet_193834-194225_2012B_Jul13",
    "MultiJet_194270-196531_2012B_Jul13",
    "MultiJet_198022-198523_2012C_Aug24",
    "MultiJet_198941-200601_2012C_Prompt",
    "MultiJet_200961-202504_2012C_Prompt",
    "MultiJet_202792-203742_2012C_Prompt",
]

datasetsMC_2012 = []
if not minimalDatasets:
    datasetsMC_2012.extend([
    "TTToHplusBWB_M80_Summer12",
    "TTToHplusBWB_M90_Summer12",
    "TTToHplusBWB_M100_Summer12",
    "TTToHplusBWB_M120_Summer12",
    "TTToHplusBWB_M140_Summer12",
    "TTToHplusBWB_M150_Summer12",
    "TTToHplusBWB_M155_Summer12",
    "TTToHplusBWB_M160_Summer12",

    "TTToHplusBHminusB_M80_Summer12",
    "TTToHplusBHminusB_M100_Summer12",
    "TTToHplusBHminusB_M120_Summer12",
    "TTToHplusBHminusB_M140_Summer12",
    "TTToHplusBHminusB_M150_Summer12",
    "TTToHplusBHminusB_M155_Summer12",
    "TTToHplusBHminusB_M160_Summer12",

    "Hplus_taunu_t-channel_M80_Summer12",
    "Hplus_taunu_t-channel_M90_Summer12",
    "Hplus_taunu_t-channel_M100_Summer12",
    "Hplus_taunu_t-channel_M120_Summer12",
    "Hplus_taunu_t-channel_M140_Summer12",
    "Hplus_taunu_t-channel_M150_Summer12",
    "Hplus_taunu_t-channel_M155_Summer12",
    "Hplus_taunu_t-channel_M160_Summer12",

    "Hplus_taunu_tW-channel_M80_Summer12",
    "Hplus_taunu_tW-channel_M90_Summer12",
    "Hplus_taunu_tW-channel_M100_Summer12",
    "Hplus_taunu_tW-channel_M120_Summer12",
    "Hplus_taunu_tW-channel_M140_Summer12",
    "Hplus_taunu_tW-channel_M150_Summer12",
    "Hplus_taunu_tW-channel_M155_Summer12",
    "Hplus_taunu_tW-channel_M160_Summer12",

    "Hplus_taunu_s-channel_M80_Summer12",
    "Hplus_taunu_s-channel_M90_Summer12",
    "Hplus_taunu_s-channel_M100_Summer12",
    "Hplus_taunu_s-channel_M120_Summer12",
    "Hplus_taunu_s-channel_M140_Summer12",
    "Hplus_taunu_s-channel_M150_Summer12",
    "Hplus_taunu_s-channel_M155_Summer12",
    "Hplus_taunu_s-channel_M160_Summer12",

    "HplusTB_M180_Summer12",
    "HplusTB_M190_Summer12",
    "HplusTB_M200_Summer12",
    "HplusTB_M220_Summer12",
    "HplusTB_M250_Summer12",
    "HplusTB_M300_Summer12",
    ])

datasetsMC_2012.extend([
    "TTToHplusBWB_M80_ext_Summer12",
    "TTToHplusBWB_M90_ext_Summer12",
    "TTToHplusBWB_M100_ext_Summer12",
    "TTToHplusBWB_M120_ext_Summer12",
    "TTToHplusBWB_M140_ext_Summer12",
    "TTToHplusBWB_M150_ext_Summer12",
    "TTToHplusBWB_M155_ext_Summer12",
    "TTToHplusBWB_M160_ext_Summer12",

    "TTToHplusBHminusB_M80_ext_Summer12",
    "TTToHplusBHminusB_M90_Summer12",
    "TTToHplusBHminusB_M100_ext_Summer12",
    "TTToHplusBHminusB_M120_ext_Summer12",
    "TTToHplusBHminusB_M140_ext_Summer12",
    "TTToHplusBHminusB_M150_ext_Summer12",
    "TTToHplusBHminusB_M155_ext_Summer12",
    "TTToHplusBHminusB_M160_ext_Summer12",

    "HplusTB_M180_ext_Summer12",
    "HplusTB_M190_ext_Summer12",
    "HplusTB_M200_ext_Summer12",
    "HplusTB_M220_ext_Summer12",
    "HplusTB_M250_ext_Summer12",
    "HplusTB_M300_ext_Summer12",
    "HplusTB_M400_Summer12",
    "HplusTB_M500_Summer12",
    "HplusTB_M600_Summer12",

    "QCD_Pt30to50_TuneZ2star_Summer12",
    "QCD_Pt50to80_TuneZ2star_Summer12",
    "QCD_Pt80to120_TuneZ2star_Summer12",
    "QCD_Pt120to170_TuneZ2star_Summer12",
    "QCD_Pt170to300_TuneZ2star_Summer12",
    "QCD_Pt170to300_TuneZ2star_v2_Summer12",
    "QCD_Pt300to470_TuneZ2star_Summer12",
    "QCD_Pt300to470_TuneZ2star_v2_Summer12",
    "QCD_Pt300to470_TuneZ2star_v3_Summer12",

    "WW_TuneZ2star_Summer12",
    "WZ_TuneZ2star_Summer12",
    "ZZ_TuneZ2star_Summer12",
    "TTJets_TuneZ2star_Summer12",
    "WJets_TuneZ2star_v1_Summer12",
    "WJets_TuneZ2star_v2_Summer12",
    "W1Jets_TuneZ2star_Summer12",
    "W2Jets_TuneZ2star_Summer12",
    "W3Jets_TuneZ2star_Summer12",
    "W4Jets_TuneZ2star_Summer12",
    "DYJetsToLL_M50_TuneZ2star_Summer12",
#    "DYJetsToLL_M10to50_TuneZ2star_Summer12",
    "T_t-channel_TuneZ2star_Summer12",
    "Tbar_t-channel_TuneZ2star_Summer12",
    "T_tW-channel_TuneZ2star_Summer12",
    "Tbar_tW-channel_TuneZ2star_Summer12",
    "T_s-channel_TuneZ2star_Summer12",
    "Tbar_s-channel_TuneZ2star_Summer12",
])

def mcWorkflow():
    if "quadpfjetbtag" in workflow:
        return workflow.replace("quadpfjetbtag", "quadpfjet%sbtag" % mc_pfjettrigger)
    return workflow

# Disable W+jets weighting if requested
if not doWJetsWeighting:
    for name in [
        "WJets_TuneZ2star_v1_Summer12",
        "WJets_TuneZ2star_v2_Summer12",
        "W1Jets_TuneZ2star_Summer12",
        "W2Jets_TuneZ2star_Summer12",
        "W3Jets_TuneZ2star_Summer12",
        "W4Jets_TuneZ2star_Summer12",
        ]:

        multicrabWorkflows.datasets.getDataset(name).getWorkflow(mcWorkflow()).removeArg("wjetsWeighting")

# Add the datasest to the multicrab system
if "v44" in workflow:
    datasets = []
    datasets.extend(datasetsData_2011)
    datasets.extend(datasetsMC_2011)

    multicrab.extendDatasets(workflow, datasets)
elif "v53" in workflow:
    datasets = []
    if "taumet" in workflow:
        datasets.extend(datasetsData_Tau_2012)
        datasets.extend(datasetsMC_2012)
    elif "quadjet" in workflow:
        datasets.extend(datasetsData_MultiJet_2012)
        datasets.extend(datasetsMC_2012)
    elif "quadpfjet" in workflow:
        datasets.extend(datasetsData_MultiJet_2012)
    else:
        raise Exception("Unsupported workflow %s" % workflow)

    multicrab.extendDatasets(workflow, datasets)
    if "quadpfjetbtag" in workflow:
        wf_mc = mcWorkflow()
        multicrab.extendDatasets(wf_mc, datasetsMC_2012)

output = ["histograms.root"]
if "signalAnalysis" in cfg:
    output.append("pickEvents.txt")
multicrab.addCommonLine("CMSSW.output_file = %s" % ",".join(output))

multicrab.appendLineAll("GRID.maxtarballsize = 35")

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

prefix += "_"+workflow

# Generate configuration only?
configOnly=True
#configOnly=False
# Genenerate configuration and create the crab tasks
multicrab.createTasks(prefix=prefix, configOnly=configOnly)

