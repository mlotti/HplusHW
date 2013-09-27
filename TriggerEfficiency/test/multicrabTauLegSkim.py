#!/usr/bin/env python

import re

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabWorkflows as multicrabWorkflows
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabWorkflowsTriggerEff as multicrabWorkflowsTriggerEff
####multicrabWorkflowsTriggerEff.addMetLegSkim_cmssw44X_v5(multicrabWorkflows.datasets)
####multicrabWorkflowsTriggerEff.addTauLegSkim_cmssw44X_v5(multicrabWorkflows.datasets)

multicrab = Multicrab("../../HeavyChHiggsToTauNu/test/pattuple/crab_pat.cfg", "../../HeavyChHiggsToTauNu/test/pattuple/patTuple_cfg.py", lumiMaskDir="../../HeavyChHiggsToTauNu/test")

datasets_SingleMu = [
    "SingleMu_165970-167913_2011A_Nov08_RAWRECO",
    "SingleMu_170722-173198_2011A_Nov08_RAWRECO",
    "SingleMu_173236-173692_2011A_Nov08_RAWRECO",
    "SingleMu_175832-180252_2011B_Nov19_RAWRECO",
]

datasets_DY = [
     "DYJetsToLL_TuneZ2_MPIoff_M50_7TeV_madgraph_tauola_GENRAW",
]
           
workflow = "triggerTauLeg_skim_v44_v5"

tasks = [
     ("TauLeg", datasets_SingleMu+datasets_DY),
]

for midfix, datasets in tasks:
    multicrab = Multicrab("../../HeavyChHiggsToTauNu/test/pattuple/crab_pat.cfg", "../../HeavyChHiggsToTauNu/test/pattuple/patTuple_cfg.py", lumiMaskDir="../../HeavyChHiggsToTauNu/test")

    multicrab.extendDatasets(workflow, datasets)

    multicrab.appendLineAll("CMSSW.total_number_of_lumis = -1")

    # local_stage_out doesn't work due to denied permission because we're
    # writing to /store/group/local ... 
    #multicrab.appendLineAll("USER.local_stage_out=1")

    multicrab.appendLineAll("USER.user_remote_dir = /store/group/local/HiggsChToTauNuFullyHadronic/TriggerTauLeg/CMSSW_4_4_X")
    #multicrab.appendLineAll("GRID.maxtarballsize = 40")

    #def addCopyConfig(dataset):
    #    dataset.appendLine("USER.additional_input_files = copy_cfg.py")
    #    dataset.appendCopyFile("../copy_cfg.py")
    #multicrab.forEachDataset(addCopyConfig)

    def modify(datasets):
	datasets.appendArg("doTauHLTMatching=0")
    multicrab.forEachDataset(modify)

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
