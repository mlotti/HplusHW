#!/usr/bin/env python

# Usage: multicrabcreate.py [multicrab-dir-to-be-resubmitted]
# is resubmitting some crab tasks within the multicrab dir, 
# first remove the crab-dir, then run multicrabcreate.py again 
# with the multicrab as an argument.

import os
import re
import sys
import datetime

#PSET = "miniAODGEN2TTree_cfg.py"
#PSET = "miniAOD2TTree_TauLegSkim_cfg.py"
#PSET = "miniAOD2TTree_METLegSkim_cfg.py"
PSET = "miniAOD2TTree_SignalAnalysisSkim_cfg.py"

lumiMask25ns = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-258714_13TeV_PromptReco_Collisions15_25ns_JSON.txt "
lumiMask50ns = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-255031_13TeV_PromptReco_Collisions15_50ns_JSON_v2.txt"

class Dataset :
    def __init__(self,url,dbs="global",dataVersion="74Xmc",lumiMask=lumiMask25ns):
        self.URL = url
        self.DBS = dbs
	self.dataVersion = dataVersion
	self.lumiMask = lumiMask

    def isData(self):
	if "data" in self.dataVersion:
	    return True
	return False


datasetsTauData = []
#datasetsTauData.append(Dataset('/Tau/Run2015B-23Sep2015-v1/MINIAOD',dataVersion="74Xdata"))
#datasetsTauData.append(Dataset('/Tau/Run2015C-23Sep2015-v1/MINIAOD',dataVersion="74Xdata",lumiMask=lumiMask50ns))
datasetsTauData.append(Dataset('/Tau/Run2015C-23Sep2015-v1/MINIAOD',dataVersion="74Xdata",lumiMask=lumiMask25ns))
datasetsTauData.append(Dataset('/Tau/Run2015D-PromptReco-v3/MINIAOD',dataVersion="74Xdata",lumiMask=lumiMask25ns))

datasetsMuonData = []
#datasetsMuonData.append(Dataset('/SingleMuon/Run2015B-05Aug2015-v1/MINIAOD',dataVersion="74Xdata"))
datasetsMuonData.append(Dataset('/SingleMuon/Run2015C-PromptReco-v1/MINIAOD',dataVersion="74Xdata",lumiMask=lumiMask50ns))
datasetsMuonData.append(Dataset('/SingleMuon/Run2015C-PromptReco-v1/MINIAOD',dataVersion="74Xdata",lumiMask=lumiMask25ns))
datasetsMuonData.append(Dataset('/SingleMuon/Run2015D-PromptReco-v3/MINIAOD',dataVersion="74Xdata",lumiMask=lumiMask25ns))

datasets25ns = []
datasets25ns.append(Dataset('/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
#datasets25ns.append(Dataset('/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-scaleup-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM')) # For Q2 variation
#datasets25ns.append(Dataset('/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-scaledown-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM')) # For Q2 variation
datasets25ns.append(Dataset('/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25ns.append(Dataset('/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25ns.append(Dataset('/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25ns.append(Dataset('/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25ns.append(Dataset('/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25ns.append(Dataset('/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25ns.append(Dataset('/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM'))
datasets25ns.append(Dataset('/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25ns.append(Dataset('/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25ns.append(Dataset('/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25ns.append(Dataset('/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM'))
datasets25ns.append(Dataset('/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM'))
datasets25ns.append(Dataset('/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25ns.append(Dataset('/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25ns.append(Dataset('/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM'))
#datasets25ns.append(Dataset('/WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25ns.append(Dataset('/WW_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25ns.append(Dataset('/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25ns.append(Dataset('/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM'))
datasets25ns.append(Dataset('/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM'))
datasets25ns.append(Dataset('/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM'))
datasets25ns.append(Dataset('/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25ns.append(Dataset('/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25ns.append(Dataset('/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM'))
datasets25ns.append(Dataset('/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25ns.append(Dataset('/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM'))
datasets25ns.append(Dataset('/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM'))
datasets25ns.append(Dataset('/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM'))
datasets25ns.append(Dataset('/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25ns.append(Dataset('/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25ns.append(Dataset('/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25ns.append(Dataset('/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25ns.append(Dataset('/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))

datasets25nsTau = []
datasets25nsTau.append(Dataset('/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))                 
datasets25nsTau.append(Dataset('/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM'))
#datasets25nsTau.append(Dataset('/DYJetsToLL_M-50_13TeV-madgraph-pythia8-tauola_v2/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM'))
#datasets25nsTau.append(Dataset('/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
#datasets25nsDY.append(Dataset('/DYJetsToLL_M-100to200_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
#datasets25nsDY.append(Dataset('/DYJetsToLL_M-200to400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
#datasets25nsDY.append(Dataset('/DYJetsToLL_M-400to500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
#datasets25nsDY.append(Dataset('/DYJetsToLL_M-500to700_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
#datasets25nsDY.append(Dataset('/DYJetsToLL_M-700to800_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
#datasets25nsDY.append(Dataset('/DYJetsToLL_M-800to1000_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
#datasets25nsDY.append(Dataset('/DYJetsToLL_M-1000to1500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
#datasets25nsDY.append(Dataset('/DYJetsToLL_M-1500to2000_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
#datasets25nsDY.append(Dataset('/DYJetsToLL_M-2000to3000_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
#datasets25nsTau.append(Dataset('/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25nsTau.append(Dataset('/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM'))
#datasets25nsTau.append(Dataset('/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
#datasets25nsTau.append(Dataset('/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
#datasets25nsTau.append(Dataset('/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
#datasets25nsTau.append(Dataset('/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM'))
#datasets25nsTau.append(Dataset('/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM'))
#datasets25nsTau.append(Dataset('/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM'))
datasets25nsTau.append(Dataset('/GluGluHToTauTau_M125_13TeV_powheg_pythia8/manzoni-RunIISpring15DR74-AsymptFlat10to50bx25Raw_MCRUN2_74_V9-v1_25ns14e33_HLT_v4p0_L1_v5_1oct15-9aee7f6aa9ee774a3ecb4dd6367feac8/USER',dbs='phys03'))

datasets25nsSignal = []
datasets25nsSignal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-500_13TeV_amcatnlo_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25nsSignal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-400_13TeV_amcatnlo_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25nsSignal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-350_13TeV_amcatnlo_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25nsSignal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-300_13TeV_amcatnlo_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25nsSignal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-250_13TeV_amcatnlo_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25nsSignal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-220_13TeV_amcatnlo_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25nsSignal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-200_13TeV_amcatnlo_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25nsSignal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-180_13TeV_amcatnlo_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM')) 
datasets25nsSignal.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-160_13TeV_amcatnlo_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25nsSignal.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-155_13TeV_amcatnlo_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25nsSignal.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-150_13TeV_amcatnlo_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM')) 
datasets25nsSignal.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-140_13TeV_amcatnlo_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25nsSignal.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-120_13TeV_amcatnlo_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25nsSignal.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-100_13TeV_amcatnlo_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25nsSignal.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-90_13TeV_amcatnlo_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))
datasets25nsSignal.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-80_13TeV_amcatnlo_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'))

datasets50ns = []
datasets50ns.append(Dataset('/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM'))
datasets50ns.append(Dataset('/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM'))
datasets50ns.append(Dataset('/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM'))
datasets50ns.append(Dataset('/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM'))
datasets50ns.append(Dataset('/WW_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM'))
datasets50ns.append(Dataset('/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM'))
datasets50ns.append(Dataset('/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM'))


datasets = []

tauLegDatasets         = []
#tauLegDatasets.append(Dataset('/ZprimeToTauTau_M-1000_Tune4C_13TeV-pythia8/bluj-ZprimeToTauTau_MiniAOD_GRunV47_v2-6b3acb073896b48a28b982ccc80b3330/USER','phys03'))
tauLegDatasets.extend(datasetsMuonData)
#tauLegDatasets.extend(datasets25ns)
tauLegDatasets.extend(datasets25nsTau)
#tauLegDatasets.extend(datasets50ns)
#tauLegDatasets.extend(datasets25nsSignal)

metLegDatasets         = []
#metLegDatasets.append(Dataset('/TT_Tune4C_13TeV-pythia8-tauola/bluj-TTbar_MiniAOD_GRunV47_v2-6b3acb073896b48a28b982ccc80b3330/USER','phys03'))
metLegDatasets.extend(datasetsTauData)
metLegDatasets.extend(datasets25ns)
#metLegDatasets.extend(datasets25nsSignal)

signalAnalysisDatasets = []
signalAnalysisDatasets.extend(datasetsTauData)
signalAnalysisDatasets.extend(datasets25ns)
signalAnalysisDatasets.extend(datasets25nsSignal)

datadataset_re = re.compile("^/(?P<name>\S+?)/(?P<run>Run\S+?)-")
mcdataset_re = re.compile("^/(?P<name>\S+?)/")

version = ""
pwd = os.getcwd()
cmssw_re = re.compile("/CMSSW_(?P<version>\S+?)/")
match = cmssw_re.search(pwd)
if match:
    version = match.group("version")
    version = version.replace("_","")
    version = version.replace("pre","p")
    version = version.replace("patch","p")

analysis = "SignalAnalysis"
leg_re = re.compile("miniAOD2TTree_(?P<leg>\S+)Skim_cfg.py")
match = leg_re.search(PSET)
if match:
    analysis = match.group("leg")

if analysis == "SignalAnalysis":
    datasets = signalAnalysisDatasets
if analysis == "TauLeg":
    datasets = tauLegDatasets
if analysis == "METLeg":
    datasets = metLegDatasets

dirName = "multicrab"
dirName+= "_"+analysis
dirName+= "_v"+version

bx_re = re.compile("\S+(?P<bx>\d\dns)_\S+")
match = bx_re.search(datasets[0].URL)
if match:
    dirName+= "_"+match.group("bx")

time = datetime.datetime.now().strftime("%Y%m%dT%H%M")
dirName+= "_" + time

if len(sys.argv) == 2 and os.path.exists(sys.argv[1]) and os.path.isdir(sys.argv[1]):
    dirName = sys.argv[1]

if not os.path.exists(dirName):
    os.mkdir(dirName)
    os.system("cp %s %s"%(PSET,dirName))

crab_dataset_re = re.compile("config.Data.inputDataset")
crab_requestName_re = re.compile("config.General.requestName")
crab_workArea_re = re.compile("config.General.workArea")
crab_pset_re = re.compile("config.JobType.psetName")
crab_psetParams_re = re.compile("config.JobType.pyCfgParams")
crab_split_re = re.compile("config.Data.splitting")# = 'FileBased'
crab_splitunits_re = re.compile("config.Data.unitsPerJob")

crab_dbs_re = re.compile("config.Data.inputDBS")
tune_re = re.compile("(?P<name>\S+)_Tune")
tev_re = re.compile("(?P<name>\S+)_13TeV")
rr_re = re.compile("Cert_(?P<RunRange>\d+-\d+)_13TeV_PromptReco_Collisions15(?P<BunchSpacing>\S*)_JSON")
#rr_re = re.compile("Cert_(?P<RunRange>\d+-\d+)_13TeV_PromptReco_Collisions15_(?P<BunchSpacing>\d+ns)_JSON_v")

for dataset in datasets:
    match = mcdataset_re.search(dataset.URL)
    if dataset.isData():
	match = datadataset_re.search(dataset.URL)
    if match:
        rName = match.group("name")
	if dataset.isData():
	    rName+= "_"
	    rName+= match.group("run")
#	rName = rName.replace("-","")
	tune_match = tune_re.search(rName)
	if tune_match:
	    rName = tune_match.group("name")
        tev_match = tev_re.search(rName)
        if tev_match:
            rName = tev_match.group("name")

	if dataset.isData():
	    runrangeMatch = rr_re.search(dataset.lumiMask)
	    if runrangeMatch:
		rr = runrangeMatch.group("RunRange")
		rr = rr.replace("-","_")
		bs = runrangeMatch.group("BunchSpacing")
		rName += "_"+rr+bs
#            s = (dataset.URL).split("/")
#            rName = s[1]+"_"+(s[2].split("-")[0].split("_")[0])

        rName = rName.replace("-","")

        outfilepath = os.path.join(dirName,"crabConfig_"+rName+".py")

	if not os.path.exists(os.path.join(dirName,rName)):

            fIN = open("crabConfig.py","r")
            fOUT = open(outfilepath,"w")
            for line in fIN:
                if line[0] == "#":
                    continue
                match = crab_dataset_re.search(line)
                if match:
                    line = "config.Data.inputDataset = '"+dataset.URL+"'\n"
        	match = crab_requestName_re.search(line)
                if match:
                    line = "config.General.requestName = '"+rName+"'\n"
                match = crab_workArea_re.search(line)
                if match:
                    line = "config.General.workArea = '"+dirName+"'\n"
                match = crab_pset_re.search(line)
                if match:
                    line = "config.JobType.psetName = '"+PSET+"'\n"
                match = crab_psetParams_re.search(line)
                if match:
                    line = "config.JobType.pyCfgParams = ['dataVersion="+dataset.dataVersion+"']\n"
                match = crab_dbs_re.search(line)
                if match:
                    line = "config.Data.inputDBS = '"+dataset.DBS+"'\n"
                if dataset.isData():
                    match = crab_split_re.search(line)
                    if match:
                        line = "config.Data.splitting = 'LumiBased'\n"
                        line+= "config.Data.lumiMask = '"+dataset.lumiMask+"'\n"
                    match = crab_splitunits_re.search(line)	
                    if match:
                        line = "config.Data.unitsPerJob = 100\n"

                fOUT.write(line)
            fOUT.close()
            fIN.close()

            cmd = "crab submit -c "+outfilepath
            print cmd
            os.system("crab submit "+outfilepath)
            mv = "mv "+os.path.join(dirName,"crab_"+rName)+" "+os.path.join(dirName,rName)
#            print mv
            os.system(mv)
