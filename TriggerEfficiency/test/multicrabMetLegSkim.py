#!/usr/bin/env python

import re

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabWorkflows as multicrabWorkflows
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabWorkflowsTriggerEff as multicrabWorkflowsTriggerEff
multicrabWorkflowsTriggerEff.addMetLegSkim_cmssw44X_v1(multicrabWorkflows.datasets)

multicrab = Multicrab("../../HeavyChHiggsToTauNu/test/pattuple/crab_pat.cfg", "../../HeavyChHiggsToTauNu/test/pattuple/patTuple_cfg.py", lumiMaskDir="../../HeavyChHiggsToTauNu/test")

datasets = [
########
#
# 44X
#
########

        # Data 2011
        # tau+met trigger
       "Tau_165970-167913_2011A_Nov08",     # 2011A HLT_IsoPFTau35_Trk20_MET45_v{1,2,4,6}, 2011A HLT_IsoPFTau35_Trk20_MET60_v{2,3,4}
       "Tau_170722-173198_2011A_Nov08",    # 2011A HLT_IsoPFTau35_Trk20_MET60_v6
       "Tau_173236-173692_2011A_Nov08",    # 2011A HLT_MediumIsoPFTau35_Trk20_MET60_v1
       "Tau_175832-180252_2011B_Nov19",    # 2011B HLT_MediumIsoPFTau35_Trk20_MET60_v{1,5,6}

        # single mu
#       "SingleMu_160431-163261_2011A_Nov08",     # 2011A
#       "SingleMu_163270-163869_2011A_Nov08",     # 2011A
#       "SingleMu_165088-165633_2011A_Nov08",     # 2011A
#       "SingleMu_165970-166150_2011A_Nov08",     # 2011A
#       "SingleMu_166161-166164_2011A_Nov08",     # 2011A
#       "SingleMu_166346-166346_2011A_Nov08",     # 2011A
#       "SingleMu_166374-166967_2011A_Nov08",     # 2011A
#       "SingleMu_167039-167043_2011A_Nov08",     # 2011A
#       "SingleMu_167078-167913_2011A_Nov08",     # 2011A
#       "SingleMu_170722-172619_2011A_Nov08",     # 2011A
#       "SingleMu_172620-173198_2011A_Nov08",     # 2011A
#       "SingleMu_173236-173692_2011A_Nov08",     # 2011A
#       "SingleMu_175860-176469_2011A_Nov19",     # 2011B
#       "SingleMu_176545-177053_2011B_Nov19",     # 2011B
#       "SingleMu_177074-177452_2011B_Nov19",     # 2011B
#       "SingleMu_177718-178380_2011B_Nov19",     # 2011B
#       "SingleMu_178420-178866_2011B_Nov19",     # 2011B
#       "SingleMu_178871-179889_2011B_Nov19",     # 2011B
#       "SingleMu_179959-180252_2011B_Nov19",     # 2011B

        # Fall11
        # Signal MC (WH)
#        "TTToHplusBWB_M80_Fall11",
#        "TTToHplusBWB_M90_Fall11",
#        "TTToHplusBWB_M100_Fall11",
#        "TTToHplusBWB_M120_Fall11",
#        "TTToHplusBWB_M140_Fall11",
#        "TTToHplusBWB_M150_Fall11",
#        "TTToHplusBWB_M155_Fall11",
#        "TTToHplusBWB_M160_Fall11",
        # Signal MC (HH)
#        "TTToHplusBHminusB_M80_Fall11",
#        "TTToHplusBHminusB_M90_Fall11",
#        "TTToHplusBHminusB_M100_Fall11",
#        "TTToHplusBHminusB_M120_Fall11",
#        "TTToHplusBHminusB_M140_Fall11",
#        "TTToHplusBHminusB_M150_Fall11",
#        "TTToHplusBHminusB_M155_Fall11",
#        "TTToHplusBHminusB_M160_Fall11",
        # Signal MC (Heavy)
#        "HplusTB_M180_Fall11",
#        "HplusTB_M190_Fall11",
#        "HplusTB_M200_Fall11",
#        "HplusTB_M220_Fall11",
#        "HplusTB_M250_Fall11",
#        "HplusTB_M300_Fall11",
        # Background MC
        "TTJets_TuneZ2_Fall11",
        "WJets_TuneZ2_Fall11",
        "W2Jets_TuneZ2_Fall11",
        "W3Jets_TuneZ2_Fall11",
        "W4Jets_TuneZ2_Fall11",
        "DYJetsToLL_M10to50_TuneZ2_Fall11",
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
#        "QCD_Pt20_MuEnriched_TuneZ2_Fall11",
        "QCD_Pt30to50_TuneZ2_Fall11",
        "QCD_Pt50to80_TuneZ2_Fall11",
        "QCD_Pt80to120_TuneZ2_Fall11",
        "QCD_Pt120to170_TuneZ2_Fall11",
        "QCD_Pt170to300_TuneZ2_Fall11",
        "QCD_Pt300to470_TuneZ2_Fall11",

######
# 44X high PU
#         "TTToHplusBWB_M90_Fall11_HighPU",
#         "TTToHplusBWB_M160_Fall11_HighPU",
#         "TTJets_TuneZ2_Fall11_HighPU",
]
#datasets = ["Tau_165970-167913_2011A_Nov08"]
           


workflow = "triggerMetLeg_skim_cmssw44X_v1"
multicrab.extendDatasets(workflow, datasets)

# local_stage_out doesn't work due to denied permission because we're
# writing to /store/group/local ...
#multicrab.appendLineAll("USER.local_stage_out=1")

multicrab.appendLineAll("GRID.maxtarballsize = 30")

def addCopyConfig(dataset):
    dataset.appendLine("USER.additional_input_files = copy_cfg.py")
    dataset.appendCopyFile("../../HeavyChHiggsToTauNu/test/copy_cfg.py")
multicrab.forEachDataset(addCopyConfig)

# For collision data stageout from US doesn't seem to be a problem
#allowUS = ["TT", "TTJets", "TTToHplusBWB_M90", "TTToHplusBWB_M100", "TTToHplusBWB_M120", "TTToHplusBWB_M140", "TTToHplusBWB_M160"]
#def blacklistUS(dataset):
#    if dataset.isMC() and not dataset.getName() in allowUS:
#        dataset.extendBlackWhiteList("se_black_list", ["T2_US"])
#multicrab.forEachDataset(blacklistUS)

# Many failures with 60307 and 70500 from T2_UK_London_Brunel for
# pattuple_v6_1 while the similar jobs stageout fine in other T2s
multicrab.extendBlackWhiteListAll("se_black_list", defaultSeBlacklist)

prefix = "multicrab"
configOnly = False # Create task configuration only?
# Leave configOnly as false and specify site whitelist on command line when submitting the jobs

# Create multicrab task configuration and run 'multicrab -create'
taskDir = multicrab.createTasks(prefix=prefix, configOnly=configOnly)

# patch CMSSW.sh
#
# Running CMSSW again in each job just to copy the file seems to
# somehow "linearize" the file, and the subsequent file access is fast
#class Wrapper:
#    def __init__(self, **kwargs):
#        self.__dict__.update(kwargs)
#
#if not configOnly:
#    import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crabPatchCMSSWsh as patch
#    import os
#    os.chdir(taskDir)
#    patch.main(Wrapper(dirs=datasets, input="pattuple"))
#    os.chdir("..")
