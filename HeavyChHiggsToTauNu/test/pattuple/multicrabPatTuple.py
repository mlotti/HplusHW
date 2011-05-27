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
        # Data 2011 (May10 ReReco)
        # Data 2011 (PromptReco)

        # Signal MC (WH)

        # Signal MC (HH)

        # Background MC
#        "QCD_Pt15to30_TuneZ2_Summer11",
#        "QCD_Pt30to50_TuneZ2_Summer11",
#        "QCD_Pt50to80_TuneZ2_Summer11",
#        "QCD_Pt80to120_TuneZ2_Summer11",
#        "QCD_Pt120to170_TuneZ2_Summer11",
#        "QCD_Pt170to300_TuneZ2_Summer11",
        ])

# local_stage_out doesn't work due to denied permission because we're
# writing to /store/group/local ...
multicrab.appendLineAll("USER.local_stage_out=1")

multicrab.appendLineAll("GRID.maxtarballsize = 15")
multicrab.appendArgAll("runOnCrab=1")

reco_re = re.compile("(?P<reco>Reco_v\d+_[^_]+_)")
run_re = re.compile("^(?P<pd>[^_]+?)_((?P<trig>[^_]+?)_)?(?P<frun>\d+)-(?P<lrun>\d+)_")

def addOutputName(dataset):
    path = dataset.getDatasetPath().split("/")
    name = path[2].replace("-", "_")
    name += "_"+path[3]
    name += "_pattuple_v12_test4"

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

# Create multicrab task configuration and run 'multicrab -create'
multicrab.createTasks()

# Create task configuration only
#multicrab.createTasks(configOnly=True)
