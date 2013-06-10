#!/usr/bin/env python

import re

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabWorkflows as multicrabWorkflows
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabWorkflowsTriggerEff as multicrabWorkflowsTriggerEff
####multicrabWorkflowsTriggerEff.addMetLegSkim_cmssw44X_v5(multicrabWorkflows.datasets)

multicrab = Multicrab("../../HeavyChHiggsToTauNu/test/pattuple/crab_pat.cfg", "../../HeavyChHiggsToTauNu/test/pattuple/patTuple_cfg.py", lumiMaskDir="../../HeavyChHiggsToTauNu/test")

datasets = [

        # Data 2011
        # tau+met trigger
       "Tau_165970-167913_2011A_Nov08",     # 2011A HLT_IsoPFTau35_Trk20_MET45_v{1,2,4,6}, 2011A HLT_IsoPFTau35_Trk20_MET60_v{2,3,4}
       "Tau_170722-173198_2011A_Nov08",    # 2011A HLT_IsoPFTau35_Trk20_MET60_v6
       "Tau_173236-173692_2011A_Nov08",    # 2011A HLT_MediumIsoPFTau35_Trk20_MET60_v1
       "Tau_175832-180252_2011B_Nov19",    # 2011B HLT_MediumIsoPFTau35_Trk20_MET60_v{1,5,6}

        # Fall11
        # Background MC
        "TTJets_TuneZ2_Fall11",
        "WJets_TuneZ2_Fall11",
        "W2Jets_TuneZ2_Fall11",
#        "W3Jets_TuneZ2_Fall11",
	"W3Jets_TuneZ2_v2_Fall11",
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
        "QCD_Pt30to50_TuneZ2_Fall11",
        "QCD_Pt50to80_TuneZ2_Fall11",
        "QCD_Pt80to120_TuneZ2_Fall11",
        "QCD_Pt120to170_TuneZ2_Fall11",
        "QCD_Pt170to300_TuneZ2_Fall11",
        "QCD_Pt300to470_TuneZ2_Fall11",
]
           
workflow = "triggerMetLeg_skim_v44_v5"

tasks = [
     ("MetLeg", datasets),
]

for midfix, datasets in tasks:
    multicrab = Multicrab("../../HeavyChHiggsToTauNu/test/pattuple/crab_pat.cfg", "../../HeavyChHiggsToTauNu/test/pattuple/patTuple_cfg.py", lumiMaskDir="../../HeavyChHiggsToTauNu/test")

    multicrab.extendDatasets(workflow, datasets)

    # local_stage_out doesn't work due to denied permission because we're
    # writing to /store/group/local ... 
    #multicrab.appendLineAll("USER.local_stage_out=1")

    multicrab.appendLineAll("USER.user_remote_dir = /store/group/local/HiggsChToTauNuFullyHadronic/TriggerMETLeg/CMSSW_5_3_X")
    #multicrab.appendLineAll("GRID.maxtarballsize = 40")

    #def addCopyConfig(dataset):
    #    dataset.appendLine("USER.additional_input_files = copy_cfg.py")
    #    dataset.appendCopyFile("../copy_cfg.py")
    #multicrab.forEachDataset(addCopyConfig)

    multicrab.extendBlackWhiteListAll("se_black_list", defaultSeBlacklist)

    prefix = "multicrab_"+midfix
    configOnly = False # Create task configuration only?
    # Leave configOnly as false and specify site whitelist on command line when submitting the jobs

    # Create multicrab task configuration and run 'multicrab -create'
    taskDir = multicrab.createTasks(prefix=prefix, configOnly=configOnly)

    # patch CMSSW.sh, part 2
    #
    # if not configOnly:
    #     import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crabPatchCMSSWsh as patch
    #     import os                                                               
    #     os.chdir(taskDir)                                                       
    #     patch.main(Wrapper(dirs=datasets, input="pattuple"))                     
    #     os.chdir("..")
