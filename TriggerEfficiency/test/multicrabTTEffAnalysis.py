#!/usr/bin/env python

#analysis = "TauLeg2012"
#analysis = "MetLeg2012"
analysis = "MetLegWMuons2012"
#analysis = "TauLeg2011"
#analysis = "MetLeg2011"
#analysis = "QuadJet2012"

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab import *
#import ElectroWeakAnalysis.TauTriggerEfficiency.tools.multicrabDatasets as tteffDatasets
#multicrabDatasets.datasets = tteffDatasets.datasets

#import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabWorkflowsTriggerEff as multicrabWorkflowsTriggerEff
#multicrabWorkflowsTriggerEff.addMetLegSkim_vXXX(datasets)
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabWorkflows as multicrabWorkflows
#import ElectroWeakAnalysis.TauTriggerEfficiency.tools.multicrabDatasets2011 as multicrabDatasetsTTEff
import HiggsAnalysis.TriggerEfficiency.tools.multicrabDatasets2012 as multicrabDatasetsTTEff
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabWorkflowsTauEmbedding as multicrabDatasetsEmbedding

#multicrabDatasets2011.addMetLegSkim_V00_10_11_CMSSW445_v4(multicrabWorkflows.datasets)
#multicrabWorkflows.printAllDatasets()
if analysis[:-4] == "TauLeg":
    multicrabDatasetsTTEff.addTauLegSkim_v44_v5(multicrabWorkflows.datasets)
if analysis[:-4] == "MetLeg":
#    	multicrabDatasetsTTEff.addMetLegSkim(multicrabWorkflows.datasets)
    multicrabDatasetsTTEff.addMetLegSkim_CaloMETCorr(multicrabWorkflows.datasets)
#if analysis[:-4] == "MetLegWMuons":
#    multicrabDatasetsEmbedding.addEmbeddingSkim_v53_3(multicrabWorkflows.datasets)
if analysis[:-4] == "QuadJet":
    multicrabDatasetsTTEff.addQuadJetSkim(multicrabWorkflows.datasets)
#multicrabWorkflows.printAllDatasets()

lumiMaskDir="/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions11/7TeV/Reprocessing"
year = analysis[-4:]
if year == "2012":
#    lumiMaskDir="/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Prompt"
    lumiMaskDir="../../../HiggsAnalysis/HeavyChHiggsToTauNu/test"

multicrab = Multicrab("crab.cfg_TTEffAnalyzer", 
                      "TTEffAnalyzer3_cfg.py", 
                      lumiMaskDir=lumiMaskDir)


# Uncomment below the datasets you want to process
# The dataset definitions are in python/tools/multicrabDatasets.py

#from HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabDatasets import collisionData11Nov08Nov19,mcFall11

datasetsData2011TauLeg = [
    "SingleMu_165970-167913_2011A_Nov08_RAWRECO",
    "SingleMu_170722-173198_2011A_Nov08_RAWRECO",
    "SingleMu_173236-173692_2011A_Nov08_RAWRECO",
    "SingleMu_175832-180252_2011B_Nov19_RAWRECO"
]
datasetsMC2011TauLeg = [
#    "DYJetsToLL_TuneZ2_MPIoff_M50_7TeV_madgraph_tauola_GENRAW"
    "DYToTauTau_M20_CT10_TuneZ2_7TeV_powheg_pythia_tauola_TTEffSkim_v447_v1"
]

datasetsData2011MetLeg = [
    "Tau_165970-167913_2011A_Nov08",    # 2011A HLT_IsoPFTau35_Trk20_MET45_v{1,2,4,6}, 2011A HLT_IsoPFTau35_Trk20_MET60_v{2,3,4}
    "Tau_170722-173198_2011A_Nov08",    # 2011A HLT_IsoPFTau35_Trk20_MET60_v6
    "Tau_173236-173692_2011A_Nov08",    # 2011A HLT_MediumIsoPFTau35_Trk20_MET60_v1]
    "Tau_175832-180252_2011B_Nov19",    # 2011B HLT_MediumIsoPFTau35_Trk20_MET60_v{1,5,6}
]
datasetsMC2011 = [
        # MC Background
        "QCD_Pt30to50_TuneZ2_Fall11",
        "QCD_Pt50to80_TuneZ2_Fall11", 
        "QCD_Pt80to120_TuneZ2_Fall11",
        "QCD_Pt120to170_TuneZ2_Fall11",
        "QCD_Pt170to300_TuneZ2_Fall11",
        "QCD_Pt300to470_TuneZ2_Fall11",
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
datasetsData2012TauLeg = [
        "TauPlusX_190456-193621_2012A_Jan22",
        "TauPlusX_193834-196531_2012B_Jan22",
        "TauPlusX_198022-203742_2012C_Jan22",
        "TauPlusX_203777-208686_2012D_Jan22",
#        "TauPlusX_190456-190738_2012A_Jul13",
#        "TauPlusX_190782-190949_2012A_Aug06",
#        "TauPlusX_191043-193621_2012A_Jul13",
#        "TauPlusX_193834-196531_2012B_Jul13",
#        "TauPlusX_198022-198523_2012C_Aug24",
#        "TauPlusX_198941-199608_2012C_Prompt",
#        "TauPlusX_199698-203742_2012C_Prompt",
#        "TauPlusX_203777-208686_2012D_Prompt"
]
datasetsMC2012TauLeg = [
        "DYToTauTau_M_20_CT10_TuneZ2star_powheg_tauola_Summer12",
        "DYToTauTau_M_20_CT10_TuneZ2star_v2_powheg_tauola_Summer12",

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
        "DYJetsToLL_M10to50_TuneZ2star_Summer12",
        "T_t-channel_TuneZ2star_Summer12",
        "Tbar_t-channel_TuneZ2star_Summer12",
        "T_tW-channel_TuneZ2star_Summer12",
        "Tbar_tW-channel_TuneZ2star_Summer12",
        "T_s-channel_TuneZ2star_Summer12",
        "Tbar_s-channel_TuneZ2star_Summer12"
]
datasetsData2012MetLeg = [
        "Tau_190456-193621_2012A_Jan22",
        "TauParked_193834-196531_2012B_Jan22",
        "TauParked_198022-202504_2012C_Jan22",
        "TauParked_202972-203742_2012C_Jan22",
        "TauParked_203777-208686_2012D_Jan22",
#	"Tau_190456-190738_2012A_Jul13",	# 2012A HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v2
#        "Tau_190782-190949_2012A_Aug06",
#        "Tau_191043-193621_2012A_Jul13",
#        "Tau_193834-196531_2012B_Jul13",
#        "Tau_198022-198523_2012C_Aug24",
#        "Tau_198941-200601_2012C_Prompt",
#        "Tau_200961-202504_2012C_Prompt",
#        "Tau_202792-203742_2012C_Prompt",
#        "Tau_203777-208686_2012D_Prompt"
]
datasetsMC2012MetLeg = [
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
        "DYJetsToLL_M10to50_TuneZ2star_Summer12",
        "T_t-channel_TuneZ2star_Summer12",
        "Tbar_t-channel_TuneZ2star_Summer12",
        "T_tW-channel_TuneZ2star_Summer12",
        "Tbar_tW-channel_TuneZ2star_Summer12",
        "T_s-channel_TuneZ2star_Summer12",
        "Tbar_s-channel_TuneZ2star_Summer12"
]
datasetsData2012MetLegWMuons = [
        "SingleMu_190456-193621_2012A_Jan22",
        "SingleMu_193834-196531_2012B_Jan22",
        "SingleMu_198022-200381_2012C_Jan22",
        "SingleMu_200466-203742_2012C_Jan22",
        "SingleMu_203777-205834_2012D_Jan22",
        "SingleMu_205908-207100_2012D_Jan22",
        "SingleMu_207214-208686_2012D_Jan22",
]
datasetsMC2012MetLegWMuons = [
        "WJets_TuneZ2star_v1_Summer12",
        "WJets_TuneZ2star_v2_Summer12",
        "W1Jets_TuneZ2star_Summer12",
        "W2Jets_TuneZ2star_Summer12",
        "W3Jets_TuneZ2star_Summer12",
        "W4Jets_TuneZ2star_Summer12",
        "TTJets_TuneZ2star_Summer12",
        "TTJets_FullLept_TuneZ2star_Summer12",
        "TTJets_SemiLept_TuneZ2star_Summer12",
        "TTJets_Hadronic_TuneZ2star_ext_Summer12",
        "DYJetsToLL_M50_TuneZ2star_Summer12",
        "T_t-channel_TuneZ2star_Summer12",
        "Tbar_t-channel_TuneZ2star_Summer12",
        "T_tW-channel_TuneZ2star_Summer12",
        "Tbar_tW-channel_TuneZ2star_Summer12",
        "T_s-channel_TuneZ2star_Summer12",
        "Tbar_s-channel_TuneZ2star_Summer12",
        "WW_TuneZ2star_Summer12",
        "WZ_TuneZ2star_Summer12",
        "ZZ_TuneZ2star_Summer12",
        "QCD_Pt20_MuEnriched_TuneZ2star_Summer12"
]    
datasetsData2012QuadJet = [
        "SingleMu_190456-190738_2012A_Jul13",
]
datasetsMC2012QuadJet = [
        "TTJets_TuneZ2star_Summer12",
]
datasets = []
#datasets.extend(datasetsData2011)
#datasets.extend(datasetsMC2011)
#datasets.extend(datasetsData2012)
#datasets.extend(datasetsMC2012)

print
print "Analysis",analysis
print

outputfiles = ""

if analysis == "TauLeg2011":
    datasets.extend(datasetsData2011TauLeg)
    datasets.extend(datasetsMC2011TauLeg)
    outputfiles = "tteffAnalysis-hltpftau-hpspftau.root, tteffAnalysis-hltpftau-hpspftau-highpurity.root"

if analysis == "MetLeg2011":
    datasets.extend(datasetsData2011MetLeg)
    datasets.extend(datasetsMC2011MetLeg)
    outputfiles = "tteffAnalysis-metleg.root"

if analysis == "TauLeg2012":
    datasets.extend(datasetsData2012TauLeg)
    datasets.extend(datasetsMC2012TauLeg)
#    outputfiles = "tteffAnalysis-hltpftau-hpspftau.root, tteffAnalysis-hltpftaumedium-hpspftau.root, tteffAnalysis-hltpftau-hpspftau-highpurity.root"                                                                                  
    outputfiles = "tteffAnalysis-hltpftau-hpspftau.root, tteffAnalysis-hltpftau-hpspftau-highpurity.root"

if analysis == "MetLeg2012":
    datasets.extend(datasetsData2012MetLeg)
    datasets.extend(datasetsMC2012MetLeg)
    outputfiles = "tteffAnalysis-metleg.root"

if analysis == "MetLegWMuons2012":
    datasets.extend(datasetsData2012MetLegWMuons)
    datasets.extend(datasetsMC2012MetLegWMuons)
    outputfiles = "tteffAnalysis-metleg.root"
                
if analysis == "QuadJet2012":
    datasets.extend(datasetsData2012QuadJet)
    datasets.extend(datasetsMC2012QuadJet)
    outputfiles = "tteffAnalysis-quadjet.root"

if analysis == "MetLegWMuons2012":
    multicrab.extendDatasets("tauembedding_skim_v53_3", datasets)
#        "trigger2012"+"_analysis_wMuons_"+multicrabDatasetsTTEff.skimVersion, datasets)
else:
    multicrab.extendDatasets("trigger"+analysis[:-4]+"_analysis_"+multicrabDatasetsTTEff.skimVersion, datasets)
#multicrab.extendDatasets("triggerMetLeg_analysis_vXXX", datasets)
#multicrab.appendLineAll("GRID.maxtarballsize = 20") 
multicrab.appendLineAll("CMSSW.output_file = "+outputfiles)
multicrab.appendLineAll("CMSSW.skip_TFileService_output = 1")

# Force all jobs go to jade, in some situations this might speed up
# the analysis (e.g. when there are O(1000) Alice jobs queueing, all
# CMS jobs typically go to korundi).
#if not runPatOnTheFly:
#    multicrab.extendBlackWhiteListAll("ce_white_list", ["jade-cms.hip.fi"])


# Genenerate configuration and create the crab tasks
prefix = "multicrab_"+analysis
configOnly=False
multicrab.createTasks(prefix=prefix, configOnly=configOnly, codeRepo="cvs")
