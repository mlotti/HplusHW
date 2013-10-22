#!/usr/bin/env python

import re

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

datasets_Tau = [
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

datasets_MultiJet = [
    "MultiJet_190456-190738_2012A_Jul13",
    "MultiJet_190782-190949_2012A_Aug06",
    "MultiJet_191043-193621_2012A_Jul13",
#    "MultiJet_193834-194225_2012B_Jul13",
#    "MultiJet_194270-196531_2012B_Jul13",
#    "MultiJet_198022-198523_2012C_Aug24",
#    "MultiJet_198941-203742_2012C_Prompt",
#    "MultiJet_203777-208686_2012D_Prompt",
    "MultiJet1Parked_198022-198523_2012C_Nov05",
]

datasets_Tau_W13 = [
    "Tau_190456-193621_2012A_Jan22",
    "TauParked_193834-196531_2012B_Jan22",
    "TauParked_198022-202504_2012C_Jan22",
    "TauParked_202972-203742_2012C_Jan22",
    "TauParked_203777-208686_2012D_Jan22",
]

datasets_Signal = [
    "TTToHplusBWB_M80_Summer12",
    "TTToHplusBWB_M90_Summer12",
    "TTToHplusBWB_M100_Summer12",
    "TTToHplusBWB_M120_Summer12",
    "TTToHplusBWB_M140_Summer12",
    "TTToHplusBWB_M150_Summer12",
    "TTToHplusBWB_M155_Summer12",
    "TTToHplusBWB_M160_Summer12",

    "TTToHplusBWB_M80_ext_Summer12",
    "TTToHplusBWB_M90_ext_Summer12",
    "TTToHplusBWB_M100_ext_Summer12",
    "TTToHplusBWB_M120_ext_Summer12",
    "TTToHplusBWB_M140_ext_Summer12",
    "TTToHplusBWB_M150_ext_Summer12",
    "TTToHplusBWB_M155_ext_Summer12",
    "TTToHplusBWB_M160_ext_Summer12",

    "TTToHplusBHminusB_M80_Summer12",
    "TTToHplusBHminusB_M90_Summer12",
    "TTToHplusBHminusB_M100_Summer12",
    "TTToHplusBHminusB_M120_Summer12",
    "TTToHplusBHminusB_M140_Summer12",
    "TTToHplusBHminusB_M150_Summer12",
    "TTToHplusBHminusB_M155_Summer12",
    "TTToHplusBHminusB_M160_Summer12",

    "TTToHplusBHminusB_M80_ext_Summer12",
    "TTToHplusBHminusB_M100_ext_Summer12",
    "TTToHplusBHminusB_M120_ext_Summer12",
    "TTToHplusBHminusB_M140_ext_Summer12",
    "TTToHplusBHminusB_M150_ext_Summer12",
    "TTToHplusBHminusB_M155_ext_Summer12",
    "TTToHplusBHminusB_M160_ext_Summer12",

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
    "HplusTB_M400_Summer12",
    "HplusTB_M500_Summer12",
    "HplusTB_M600_Summer12",

    "HplusTB_M180_ext_Summer12",
    "HplusTB_M190_ext_Summer12",
    "HplusTB_M200_ext_Summer12",
    "HplusTB_M220_ext_Summer12",
    "HplusTB_M250_ext_Summer12",
    "HplusTB_M300_ext_Summer12",
]

datasets_Signal_TB = [
    "HplusToTBbar_M180_Summer12",
    "HplusToTBbar_M200_Summer12",
    "HplusToTBbar_M220_Summer12",
    "HplusToTBbar_M240_Summer12",
    "HplusToTBbar_M250_Summer12",
    "HplusToTBbar_M260_Summer12",
    "HplusToTBbar_M280_Summer12",
    "HplusToTBbar_M300_Summer12",
    "HplusToTBbar_M350_Summer12",
    "HplusToTBbar_M400_Summer12",
    "HplusToTBbar_M500_Summer12",
    "HplusToTBbar_M600_Summer12",
    "HplusToTBbar_M700_Summer12",
]

datasets_QCD = [
    "QCD_Pt30to50_TuneZ2star_Summer12",
    "QCD_Pt50to80_TuneZ2star_Summer12",
    "QCD_Pt80to120_TuneZ2star_Summer12",
    "QCD_Pt120to170_TuneZ2star_Summer12",
    "QCD_Pt170to300_TuneZ2star_Summer12",
    "QCD_Pt170to300_TuneZ2star_v2_Summer12",
    "QCD_Pt300to470_TuneZ2star_Summer12",
    "QCD_Pt300to470_TuneZ2star_v2_Summer12",
    "QCD_Pt300to470_TuneZ2star_v3_Summer12",
]

datasets_VV =[
    "WW_TuneZ2star_Summer12",
    "WZ_TuneZ2star_Summer12",
    "ZZ_TuneZ2star_Summer12",
]

datasets_TT = [
#    "TTJets_TuneZ2star_Summer12",
    "TTJets_FullLept_TuneZ2star_Summer12",
    "TTJets_SemiLept_TuneZ2star_Summer12",
    "TTJets_Hadronic_TuneZ2star_ext_Summer12",
]


datasets_EWK = [
    "WJets_TuneZ2star_v1_Summer12",
    "WJets_TuneZ2star_v2_Summer12",
    "W1Jets_TuneZ2star_Summer12",
    "W2Jets_TuneZ2star_Summer12",
    "W3Jets_TuneZ2star_Summer12",
    "W4Jets_TuneZ2star_Summer12",
    "DYJetsToLL_M50_TuneZ2star_Summer12",
    "DYJetsToLL_M10to50_TuneZ2star_Summer12"
]

datasets_SingleTop = [
    "T_t-channel_TuneZ2star_Summer12",
    "Tbar_t-channel_TuneZ2star_Summer12",
    "T_tW-channel_TuneZ2star_Summer12",
    "Tbar_tW-channel_TuneZ2star_Summer12",
    "T_s-channel_TuneZ2star_Summer12",
    "Tbar_s-channel_TuneZ2star_Summer12",
]

workflow = "pattuple_taumet_v53_3"
#workflow = "pattuple_quadjet_v53_3"

tasks = []
if "taumet" in workflow:
    tasks.extend([
            ("Tau_W13", datasets_Tau_W13),
            ])
elif "quadjet" in workflow:
    tasks.extend([
            ("MultiJet", datasets_MultiJet),
            ])
    # These are run as non-triggered for taumet workflow, no need to rerun for quadjet
    for name in ["TTToHplusBWB_M100_ext_Summer12", "TTToHplusBWB_M160_ext_Summer12", "HplusTB_M200_ext_Summer12", "HplusTB_M400_Summer12"]:
        try:
            del datasets_Signal[datasets_Signal.index(name)]
        except ValueError:
            pass

tasks = []
tasks.extend([
    ("Signal", datasets_Signal),
     ("Signal_TB", datasets_Signal_TB),
    ("QCD_VV_SingleTop", datasets_QCD+datasets_VV+datasets_SingleTop),
    ("TT", datasets_TT),
    ("EWK", datasets_EWK),
])

# patch CMSSW.sh
#
# Running CMSSW again in each job just to copy the file seems to
# somehow "linearize" the file, and the subsequent file access is fast
# class Wrapper:
#     def __init__(self, **kwargs):
#         self.__dict__.update(kwargs)

for midfix, datasets in tasks:
    multicrab = Multicrab("crab_pat.cfg", lumiMaskDir="..")

    multicrab.extendDatasets(workflow, datasets)

    # local_stage_out doesn't work due to denied permission because we're
    # writing to /store/group/local ...
    #multicrab.appendLineAll("USER.local_stage_out=1")

    #multicrab.appendLineAll("GRID.maxtarballsize = 35")

    #def addCopyConfig(dataset):
    #    dataset.appendLine("USER.additional_input_files = copy_cfg.py")
    #    dataset.appendCopyFile("../copy_cfg.py")
    #multicrab.forEachDataset(addCopyConfig)

    multicrab.extendBlackWhiteListAll("se_black_list", defaultSeBlacklist)

    prefix = "multicrab_"+workflow+"_"+midfix
    configOnly = False # Create task configuration only?
    configOnly = True
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
