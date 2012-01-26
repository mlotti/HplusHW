#!/usr/bin/env python

import re

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *

# Processing step
#step = "skim"
#step = "embedding"
#step = "analysis"
#step = "analysisTau"
step = "signalAnalysis"
#step = "muonAnalysis"
#step = "caloMetEfficiency"

# Era of data to use (meaningful only for signalAnalysis
#era = "EPS"
#era = "Run2011A-EPS"
era = "Run2011A"

#version = "v13_1"
#version = "v13_2"
#version = "v13_2_seedTest1"
#version = "v13_2_seedTest2"
#version = "v13_2_seedTest3"
version = "v13_3_seedTest4"
#version = "v13_3_seedTest6"
#version = "v14"

# "Midfix" for multicrab directory name
dirPrefix = ""
#dirPrefix += "_Met50"
#dirPrefix += "_caloMet45"
#dirPrefix += "_caloMet60"
#dirPrefix += "_taueff"
#dirPrefix += "_noTauMatching"
#dirPrefix += "_noTauPtCut"
#dirPrefix += "_tauPt50"
#dirPrefix += "_nJet40"
#dirPrefix += "_noEmuVeto"
#dirPrefix += "_noEmuVetoEnd"
#dirPrefix += "_MCGT"
#dirPrefix += "_forClosureTest"
#dirPrefix = "_TauIdScan"
#dirPrefix = "_iso05"
#dirPrefix = "_test"
#dirPrefix += "_systematics"
#dirPrefix += "_debug"

# Visible pt cut
#
# For embedding use this in the multicrab directory and madhatter
# directory names. Remember to actually change the setting in
# PFEmbeddingSource_cff.py!
#
# For analysis/signalAnalysis, select the embedded dataset with this
# visible pt cut
#vispt = ""
#vispt = "_vispt10"
#vispt = "_vispt20"
#vispt = "_vispt30"
#vispt = "_vispt40"
if step in ["embedding", "analysis", "signalAnalysis"]:
    dirPrefix += "_"+version
if step in ["analysis", "signalAnalysis"]:
    dirPrefix += "_"+era

if step == "signalAnalysis":
    #dirPrefix += "_triggerVertex2010"
    #dirPrefix += "_triggerVertex2011"
    #dirPrefix += "_trigger2010"
    #dirPrefix += "_trigger2011"
    pass

# Define the processing steps: input dataset, configuration file, output file
config = {"skim":           {"input": "AOD",                           "config": "muonSkim_cfg.py", "output": "skim.root"},
          "embedding":      {"input": "tauembedding_skim_v13", "config": "embed.py",   "output": "embedded.root"},
#          "analysis":       {"input": "tauembedding_embedding_v13"+pt,  "config": "embeddingAnalysis_cfg.py"},
          "analysis":       {"input": "tauembedding_embedding_"+version,  "config": "embeddingAnalysis_cfg.py"},
          "analysisTau":    {"input": "pattuple_v18",                       "config": "tauAnalysis_cfg.py"},
#          "signalAnalysis": {"input": "tauembedding_embedding_v13"+pt,  "config": "../signalAnalysis_cfg.py"},
          "signalAnalysis": {"input": "tauembedding_embedding_"+version,  "config": "../signalAnalysis_cfg.py"},
          "muonAnalysis":   {"input": "tauembedding_skim_v13",          "config": "muonAnalysisFromSkim_cfg.py"},
          "caloMetEfficiency": {"input": "tauembedding_skim_v13",         "config": "caloMetEfficiency_cfg.py"},
          }

crabcfg = "crab.cfg"
if step in ["analysis", "analysisTau", "signalAnalysis", "muonAnalysis", "caloMetEfficiency"]:
    crabcfg = "../crab_analysis.cfg"


multicrab = Multicrab(crabcfg, config[step]["config"], lumiMaskDir="..")

# Define dataset collections
datasetsData2010 = [
    "Mu_136035-144114_Apr21", # HLT_Mu9
    "Mu_146428-147116_Apr21", # HLT_Mu9
    "Mu_147196-149294_Apr21", # HLT_Mu15_v1
]
datasetsData2011_EPS = [
    "SingleMu_Mu_160431-163261_May10",  # HLT_Mu20_v1
    "SingleMu_Mu_163270-163869_May10",  # HLT_Mu24_v2
    "SingleMu_Mu_165088-166150_Prompt", # HLT_Mu30_v3
    "SingleMu_Mu_166161-166164_Prompt", # HLT_Mu40_v1
    "SingleMu_Mu_166346-166346_Prompt", # HLT_Mu40_v2
    "SingleMu_Mu_166374-167043_Prompt", # HLT_Mu40_v1
    "SingleMu_Mu_167078-167913_Prompt", # HLT_Mu40_v3
]
datasetsData2011_Run2011A_noEPS = [
    "SingleMu_Mu_170722-172619_Aug05",  # HLT_Mu40_v5
    "SingleMu_Mu_172620-173198_Prompt", # HLT_Mu40_v5
    "SingleMu_Mu_173236-173692_Prompt", # HLT_Mu40_eta2p1_v1
]
datasetsData2011_Run2011A = datasetsData2011_EPS + datasetsData2011_Run2011A_noEPS
datasetsData2011 = datasetsData2011_Run2011A
datasetsMCnoQCD = [
    "TTJets_TuneZ2_Summer11",
    "WJets_TuneZ2_Summer11",
    "DYJetsToLL_M50_TuneZ2_Summer11",
    "W3Jets_TuneZ2_Summer11",
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
datasetsMCQCD = [
    "QCD_Pt20_MuEnriched_TuneZ2_Summer11",
]
datasetsSignal = [
    "TTToHplusBWB_M80_Summer11",
    "TTToHplusBWB_M90_Summer11",
    "TTToHplusBWB_M100_Summer11",
    "TTToHplusBWB_M120_Summer11",
    "TTToHplusBWB_M140_Summer11",
    "TTToHplusBWB_M150_Summer11",
    "TTToHplusBWB_M155_Summer11",
    "TTToHplusBWB_M160_Summer11",
    "TTToHplusBHminusB_M80_Summer11",
    "TTToHplusBHminusB_M90_Summer11",
    "TTToHplusBHminusB_M100_Summer11",
    "TTToHplusBHminusB_M120_Summer11",
    "TTToHplusBHminusB_M140_Summer11",
    "TTToHplusBHminusB_M150_Summer11",
    "TTToHplusBHminusB_M155_Summer11",
    "TTToHplusBHminusB_M160_Summer11",
]

# Select the datasets based on the processing step and data era
datasets = []
if step == "analysisTau":
    datasets.extend(datasetsMCnoQCD)
else:
#    datasets.extend(datasetsData2010)
    if step in ["analysis", "signalAnalysis"]:
        if era == "EPS":
            datasets.extend(datasetsData2011_EPS)
        elif era == "Run2011A-EPS":
            datasets.extend(datasetsData2011_Run2011A_noEPS)
        elif era == "Run2011A":
            datasets.extend(datasetsData2011_Run2011A)
        else:
            raise Exception("Unsupported era %s" % era)
    else:
        datasets.extend(datasetsData2011)
    datasets.extend(datasetsMCnoQCD)
    datasets.extend(datasetsMCQCD)

if step in ["skim", "embedding", "signalAnalysis"]:
    datasets.extend(datasetsSignal)

multicrab.extendDatasets(config[step]["input"], datasets)

multicrab.appendLineAll("GRID.maxtarballsize = 15")
if step != "skim":
    multicrab.extendBlackWhiteListAll("ce_white_list", ["jade-cms.hip.fi"])


# Define the processing version number, meaningful for skim/embedding
path_re = re.compile("_tauembedding_.*")
tauname = "_tauembedding_%s_%s" % (step, version)

reco_re = re.compile("^Run[^_]+_(?P<reco>[^_]+_v\d+_[^_]+_)")

# Override the default number of jobs
# Goal: ~5 hour jobs
skimNjobs = {
    "WJets_TuneZ2_Summer11": 1000, # ~10 hours
    "TTJets_TuneZ2_Summer11": 500,
    "QCD_Pt20_MuEnriched_TuneZ2_Summer11": 490,
    "DYJetsToLL_M50_TuneZ2_Summer11": 1000,
    "T_t-channel_TuneZ2_Summer11": 490,
    "Tbar_t-channel_TuneZ2_Summer11": 160,
    "T_tW-channel_TuneZ2_Summer11": 90,
    "Tbar_tW-channel_TuneZ2_Summer11": 90,
    "T_s-channel_TuneZ2_Summer11": 50,
    "Tbar_s-channel_TuneZ2_Summer11": 10,
    "WW_TuneZ2_Summer11": 200,
    "WZ_TuneZ2_Summer11": 200,
    "ZZ_TuneZ2_Summer11": 350,
    }
muonAnalysisNjobs = { # goal: 30k events/job
    "SingleMu_Mu_160431-163261_May10": 2,
    "SingleMu_Mu_163270-163869_May10": 5,
    "SingleMu_Mu_165088-166150_Prompt": 6,
    "SingleMu_Mu_166161-166164_Prompt": 1,
    "SingleMu_Mu_166346-166346_Prompt": 1,
    "SingleMu_Mu_166374-167043_Prompt": 4,
    "SingleMu_Mu_167078-167913_Prompt": 3,
    "SingleMu_Mu_170722-172619_Aug05": 5,
    "SingleMu_Mu_172620-173198_Prompt": 8,
    "SingleMu_Mu_173236-173692_Prompt": 4,
    
    "WJets_TuneZ2_Summer11": 60,
    "TTJets_TuneZ2_Summer11": 17,
    "QCD_Pt20_MuEnriched_TuneZ2_Summer11": 5,
    "DYJetsToLL_M50_TuneZ2_Summer11": 15,
    "T_t-channel_TuneZ2_Summer11": 3,
    "Tbar_t-channel_TuneZ2_Summer11": 2,
    "T_tW-channel_TuneZ2_Summer11": 4,
    "Tbar_tW-channel_TuneZ2_Summer11": 4,
    "T_s-channel_TuneZ2_Summer11": 1,
    "Tbar_s-channel_TuneZ2_Summer11": 1,
    "WW_TuneZ2_Summer11": 8,
    "WZ_TuneZ2_Summer11": 8,
    "ZZ_TuneZ2_Summer11": 8,
    }
   

# Modification function for skim/embedding steps
def modify(dataset):
    name = ""

    if dataset.isData() or step != "skim":
        dataset.appendLine("CMSSW.total_number_of_lumis = -1")
    else:
        # split by events can only be used for MC and in skim step
        # embedding step is impossible, because the counters are saved
        # in the lumi sections, and will get doubly counted in split
        # by events mode
        dataset.appendLine("CMSSW.total_number_of_events = -1")

    path = dataset.getDatasetPath().split("/")
    if step == "skim":
        name = path[2].replace("-", "_")
        name += "_"+path[3]
        name += tauname

        if dataset.isData():
            frun = dataset.getName().split("_")[1].split("-")[0]
            m = reco_re.search(name)
            name = reco_re.sub(m.group("reco")+frun+"_", name)

        dataset.useServer(False)

        try:
            njobs = skimNjobs[dataset.getName()]
            dataset.setNumberOfJobs(njobs)
#            if njobs > 490:
#                dataset.useServer(True)
        except KeyError:
            pass


    else:
        name = path_re.sub(tauname, path[2])
        name = name.replace("local-", "")

    if dataset.isData() and step in ["generation", "embedding"]:
        dataset.appendArg("overrideBeamSpot=1")

    dataset.appendLine("USER.publish_data_name = "+name)
    dataset.appendLine("CMSSW.output_file = "+config[step]["output"])
    dataset.appendLine("USER.additional_input_files = copy_cfg.py")
    dataset.appendCopyFile("copy_cfg.py")

# Modification step for analysis steps
def modifyAnalysis(dataset):
    if dataset.isMC():
        dataset.appendArg("puWeightEra="+era)
    if step == "signalAnalysis":
        dataset.appendArg("tauEmbeddingInput=1")
        dataset.appendArg("doPat=1")
        if dataset.getName() in datasetsData2011_Run2011A_noEPS:
            dataset.appendArg("tauEmbeddingCaloMet=caloMetSum")
#    if step == "analysisTau":
#        if dataset.getName() == "WJets":
#            dataset.setNumberOfJobs(100)

def modifyMuonAnalysis(dataset):
    if dataset.isMC():
        dataset.appendArg("puWeightEra="+era)
    try:
        dataset.setNumberOfJobs(muonAnalysisNjobs[dataset.getName()])
    except KeyError:
        pass
    
# Apply the modifications
if step in ["analysis", "analysisTau","signalAnalysis"]:
    if step != "signalAnalysis":
        multicrab.appendLineAll("CMSSW.output_file = histograms.root")
    multicrab.forEachDataset(modifyAnalysis)
elif step in ["muonAnalysis", "caloMetEfficiency"]:
    multicrab.appendLineAll("CMSSW.output_file = histograms.root")
    multicrab.forEachDataset(modifyMuonAnalysis)
else: # skim or embedding
    multicrab.forEachDataset(modify)

multicrab.extendBlackWhiteListAll("se_black_list", defaultSeBlacklist)

# Create the multicrab task
prefix = "multicrab_"+step+dirPrefix

configOnly=False
#configOnly=True
taskDir = multicrab.createTasks(configOnly=configOnly, prefix=prefix)

# patch CMSSW.sh
class Wrapper:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

if not configOnly and step in ["skim", "embedding"]:
    import patchSkimEmbedding as patch
    import os
    os.chdir(taskDir)
    patch.main(Wrapper(dirs=datasets, input={"skim": "skim",
                                             "embedding": "embedded"}[step]))
    os.chdir("..")
