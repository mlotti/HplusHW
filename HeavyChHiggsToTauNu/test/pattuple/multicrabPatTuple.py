#!/usr/bin/env python

import re

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.certifiedLumi as lumi

multicrab = Multicrab("crab_pat.cfg", lumiMaskDir="..")

multicrab.extendDatasets(
    "AOD",
    [
########
#
# 42X
#
########
        # Data 2010 (Apr21 ReReco)
#        "JetMETTau_Tau_136035-139975_Apr21", # HLT_SingleLooseIsoTau20
#        "JetMETTau_Tau_140058-141881_Apr21", # HLT_SingleLooseIsoTau20_Trk5
#        "BTau_141956-144114_Apr21",          # HLT_SingleIsoTau20_Trk5
#        "BTau_146428-148058_Apr21",          # HLT_SingleIsoTau20_Trk15_MET20
#        "BTau_148822-149182_Apr21",          # HLT_SingleIsoTau20_Trk15_MET25_v3
#        "BTau_149291-149294_Apr21",          # HLT_SingleIsoTau20_Trk15_MET25_v4

        # Data 2011 
#       "Tau_160431-163869_May10",           # 2011A HLT_IsoPFTau35_Trk20_MET45_v{1,2,4}
#       "Tau_165088-165633_Prompt",          # 2011A HLT_IsoPFTau35_Trk20_MET45_v6
#       "Tau_165970-167913_Prompt",          # 2011A HLT_IsoPFTau35_Trk20_MET60_v{2,3,4}
#       "Tau_170722-172619_Aug05",           # 2011A HLT_IsoPFTau35_Trk20_MET60_v6
#       "Tau_172620-173198_Prompt",          # 2011A HLT_IsoPFTau35_Trk20_MET60_v6
       "Tau_173236-173692_Prompt",          # 2011A HLT_MediumIsoPFTau35_Trk20_MET60_v1
#       "Tau_175860-177452_Prompt",          # 2011B HLT_MediumIsoPFTau35_Trk20_MET60_v1
#       "Tau_177718-178380_Prompt",          # 2011B HLT_MediumIsoPFTau35_Trk20_MET60_v1
#       "Tau_178420-179889_Prompt",          # 2011B HLT_MediumIsoPFTau35_Trk20_MET60_v5
#       "Tau_179959-180252_Prompt",          # 2011B HLT_MediumIsoPFTau35_Trk20_MET60_v6

#       "Tau_Single_165970-167913_Prompt",   # 2011A HLT_IsoPFTau35_Trk20_v{2,3,4}
#       "Tau_Single_170722-172619_Aug05",    # 2011A HLT_IsoPFTau35_Trk20_v6
#       "Tau_Single_172620-173198_Prompt",   # 2011A HLT_IsoPFTau35_Trk20_v6
#       "Tau_Single_173236-173692_Prompt",   # 2011A HLT_MediumIsoPFTau35_Trk20_v1
#       "Tau_Single_175860-177452_Prompt",   # 2011B HLT_MediumIsoPFTau35_Trk20_v1
#       "Tau_Single_177718-178380_Prompt",   # 2011B HLT_MediumIsoPFTau35_Trk20_v1
#       "Tau_Single_178420-179889_Prompt",   # 2011B HLT_MediumIsoPFTau35_Trk20_v5
#       "Tau_Single_179959-180252_Prompt",   # 2011B HLT_MediumIsoPFTau35_Trk20_v6

        # Muon data samples
#       "SingleMu_160431-163261_May10",      # 2011A
#       "SingleMu_163270-163869_May10",      # 2011A
#       "SingleMu_165088-165633_Prompt",     # 2011A
#       "SingleMu_165970-166150_Prompt",     # 2011A
#       "SingleMu_166161-166164_Prompt",     # 2011A
#       "SingleMu_166346-166346_Prompt",     # 2011A
#       "SingleMu_166374-166967_Prompt",     # 2011A
#       "SingleMu_167039-167043_Prompt",     # 2011A
#       "SingleMu_167078-167913_Prompt",     # 2011A
#       "SingleMu_172620-173198_Prompt",     # 2011A
#       "SingleMu_173236-173692_Prompt",     # 2011A
#       "SingleMu_175860-176469_Prompt",     # 2011B
#       "SingleMu_176545-177053_Prompt",     # 2011B
#       "SingleMu_177074-177452_Prompt",     # 2011B
#       "SingleMu_177718-178380_Prompt",     # 2011B
#       "SingleMu_178420-178866_Prompt",     # 2011B
#       "SingleMu_178871-179889_Prompt",     # 2011B
#       "SingleMu_179959-180252_Prompt",     # 2011B

        # Summer11
        # Signal MC (WH)
#        "TTToHplusBWB_M80_Summer11",
#        "TTToHplusBWB_M90_Summer11",
#        "TTToHplusBWB_M100_Summer11",
        "TTToHplusBWB_M120_Summer11",
#        "TTToHplusBWB_M140_Summer11",
#        "TTToHplusBWB_M150_Summer11",
#        "TTToHplusBWB_M155_Summer11",
#        "TTToHplusBWB_M160_Summer11",
        # Signal MC (HH)
#        "TTToHplusBHminusB_M80_Summer11",
#        "TTToHplusBHminusB_M90_Summer11",
#        "TTToHplusBHminusB_M100_Summer11",
#        "TTToHplusBHminusB_M120_Summer11",
#        "TTToHplusBHminusB_M140_Summer11",
#        "TTToHplusBHminusB_M150_Summer11",
#        "TTToHplusBHminusB_M155_Summer11",
#        "TTToHplusBHminusB_M160_Summer11",
        # Signal MC (Heavy)
#        "HplusTB_M180_Summer11",
#        "HplusTB_M190_Summer11",
#        "HplusTB_M200_Summer11",
#        "HplusTB_M220_Summer11",
#        "HplusTB_M250_Summer11",
#        "HplusTB_M300_Summer11",

        # Background MC
#        "QCD_Pt30to50_TuneZ2_Summer11",
#        "QCD_Pt50to80_TuneZ2_Summer11",
#        "QCD_Pt80to120_TuneZ2_Summer11",
#        "QCD_Pt120to170_TuneZ2_Summer11",
#        "QCD_Pt170to300_TuneZ2_Summer11",
#        "QCD_Pt300to470_TuneZ2_Summer11",
#        "QCD_Pt20_MuEnriched_TuneZ2_Summer11",
#        "TTJets_TuneZ2_Summer11",
#        "WJets_TuneZ2_Summer11",
#        "W3Jets_TuneZ2_Summer11",
#        "DYJetsToLL_M50_TuneZ2_Summer11",
#        "T_t-channel_TuneZ2_Summer11",
#        "Tbar_t-channel_TuneZ2_Summer11",
#        "T_tW-channel_TuneZ2_Summer11",
#        "Tbar_tW-channel_TuneZ2_Summer11",
#        "T_s-channel_TuneZ2_Summer11",
#        "Tbar_s-channel_TuneZ2_Summer11",
#        "WW_TuneZ2_Summer11",
#        "WZ_TuneZ2_Summer11",
#        "ZZ_TuneZ2_Summer11",

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
#        "TTToHplusBHminusB_M155_Fall11",
#        "TTToHplusBHminusB_M160_Fall11",
        # Signal MC (Heavy)
#        "HplusTB_M180_Fall11",
#        "HplusTB_M190_Fall11",
#        "HplusTB_M250_Fall11",
#        "HplusTB_M300_Fall11",
        # Background MC
#        "QCD_Pt120to170_TuneZ2_Fall11",
#        "QCD_Pt300to470_TuneZ2_Fall11",
#        "TTJets_TuneZ2_Fall11",
#        "WJets_TuneZ2_Fall11",
#        "DYJetsToLL_M50_TuneZ2_Fall11",
#        "T_t-channel_TuneZ2_Fall11",
#        "Tbar_t-channel_TuneZ2_Fall11",
#        "T_tW-channel_TuneZ2_Fall11",
#        "T_s-channel_TuneZ2_Fall11",
#        "Tbar_s-channel_TuneZ2_Fall11",
#        "WZ_TuneZ2_Fall11",
#        "ZZ_TuneZ2_Fall11",
        ])

# local_stage_out doesn't work due to denied permission because we're
# writing to /store/group/local ...
#multicrab.appendLineAll("USER.local_stage_out=1")

multicrab.appendLineAll("GRID.maxtarballsize = 15")
multicrab.appendArgAll("runOnCrab=1")

reco_re = re.compile("^(?P<reco>Run[^_]+_[^_]+_v\d+_[^_]+_)")
run_re = re.compile("^(?P<pd>[^_]+?)_((?P<trig>[^_]+?)_)?(?P<frun>\d+)-(?P<lrun>\d+)_")

def addOutputName(dataset):
    path = dataset.getDatasetPath().split("/")
    name = path[2].replace("-", "_")
    name += "_"+path[3]
    name += "_pattuple_v20_test1"

    # Add the begin run in the dataset name to the publish name in
    # order to distinguish pattuple datasets from the same PD
    if dataset.isData():
        m = run_re.search(dataset.getName())
        frun = m.group("frun")
        trig = ""
        if m.group("trig"):
            trig = m.group("trig")+"_"

        m = reco_re.search(name)
        name = reco_re.sub(m.group("reco")+trig+frun+"_", name)

    dataset.appendLine("USER.publish_data_name = "+name)
multicrab.forEachDataset(addOutputName)

def addSplitMode(dataset):
    if dataset.isMC():
        dataset.appendLine("CMSSW.total_number_of_events = -1")
    else:
        dataset.appendLine("CMSSW.total_number_of_lumis = -1")
multicrab.forEachDataset(addSplitMode)

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

# Create multicrab task configuration and run 'multicrab -create'
multicrab.createTasks(prefix=prefix)

# Create task configuration only
#multicrab.createTasks(prefix=prefix, configOnly=True)
