#lumiMask = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON.txt" # ICHEP dataset 271036-276811
#lumiMask = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-277148_13TeV_PromptReco_Collisions16_JSON.txt"
lumiMask = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-279588_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt"

#================================================================================================ 
# Class Definition
#================================================================================================ 
import os

class Dataset:
    def __init__(self, url, dbs="global", dataVersion="80Xmc", dasQuery="", lumiMask=lumiMask):
        self.URL = url
        self.DBS = dbs
        self.dataVersion = dataVersion
        if not os.path.dirname(lumiMask):
            lumiMask = os.path.join(os.environ['CMSSW_BASE'],"src/HiggsAnalysis/MiniAOD2TTree/data",lumiMask)
        self.lumiMask = lumiMask
        self.DASquery = dasQuery

    def isData(self):
        if "data" in self.dataVersion:
            return True
        return False


#================================================================================================ 
# Dataset definition
#================================================================================================ 

datasetsTauData = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FTau%2FRun2016*-PromptReco-v2%2FMINIAOD"
datasetsTauData.append(Dataset('/Tau/Run2016B-PromptReco-v2/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_273150-275376_13TeV_PromptReco_Collisions16_JSON_Tau_Run2016B.txt"))
datasetsTauData.append(Dataset('/Tau/Run2016C-PromptReco-v2/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_275420-276283_13TeV_PromptReco_Collisions16_JSON_Tau_Run2016C.txt"))
datasetsTauData.append(Dataset('/Tau/Run2016D-PromptReco-v2/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_276315-276437_13TeV_PromptReco_Collisions16_JSON_Tau_Run2016D_MET80.txt"))
datasetsTauData.append(Dataset('/Tau/Run2016D-PromptReco-v2/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_276453-276811_13TeV_PromptReco_Collisions16_JSON_Tau_Run2016D_noMET80.txt"))
datasetsTauData.append(Dataset('/Tau/Run2016E-PromptReco-v2/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_277075-277420_13TeV_PromptReco_Collisions16_JSON_NoL1T_Tau_Run2016E.txt"))
datasetsTauData.append(Dataset('/Tau/Run2016F-PromptReco-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_277816-278800_13TeV_PromptReco_Collisions16_JSON_NoL1T_Tau_Run2016F_HIP.txt"))
datasetsTauData.append(Dataset('/Tau/Run2016F-PromptReco-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_278801-278808_13TeV_PromptReco_Collisions16_JSON_NoL1T_Tau_Run2016F_HIPfixed.txt"))
datasetsTauData.append(Dataset('/Tau/Run2016G-PromptReco-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask=lumiMask))

datasetsJetHTData = []
das = "https://cmsweb.cern.ch/das/request?instance=prod%2Fglobal&limit=50&input=dataset%3D%2FJetHT%2FRun2016%2A-PromptReco-v2%2FMINIAOD&view=list"
datasetsJetHTData.append(Dataset('/JetHT/Run2016B-PromptReco-v2/MINIAOD', dataVersion="80Xdata", dasQuery=das))
datasetsJetHTData.append(Dataset('/JetHT/Run2016C-PromptReco-v2/MINIAOD', dataVersion="80Xdata", dasQuery=das))
datasetsJetHTData.append(Dataset('/JetHT/Run2016D-PromptReco-v2/MINIAOD', dataVersion="80Xdata", dasQuery=das))
datasetsJetHTData.append(Dataset('/JetHT/Run2016E-PromptReco-v2/MINIAOD', dataVersion="80Xdata", dasQuery=das))
datasetsJetHTData.append(Dataset('/JetHT/Run2016F-PromptReco-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das))


datasetsMuonData = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FSingleMuon%2FRun2016*-PromptReco-v2%2FMINIAOD"
datasetsMuonData.append(Dataset('/SingleMuon/Run2016B-PromptReco-v2/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_273150-275376_13TeV_PromptReco_Collisions16_JSON_Tau_Run2016B.txt")) # Tau used when SingleMuon same
datasetsMuonData.append(Dataset('/SingleMuon/Run2016C-PromptReco-v2/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_275420-276283_13TeV_PromptReco_Collisions16_JSON_Tau_Run2016C.txt"))
datasetsMuonData.append(Dataset('/SingleMuon/Run2016D-PromptReco-v2/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_276315-276811_13TeV_PromptReco_Collisions16_JSON_SingleMuon_Run2016D.txt"))
datasetsMuonData.append(Dataset('/SingleMuon/Run2016E-PromptReco-v2/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_276830-277420_13TeV_PromptReco_Collisions16_JSON_NoL1T_SingleMuon_Run2016E.txt"))
datasetsMuonData.append(Dataset('/SingleMuon/Run2016F-PromptReco-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_277816-278800_13TeV_PromptReco_Collisions16_JSON_NoL1T_Tau_Run2016F_HIP.txt"))
datasetsMuonData.append(Dataset('/SingleMuon/Run2016F-PromptReco-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_278801-278808_13TeV_PromptReco_Collisions16_JSON_NoL1T_Tau_Run2016F_HIPfixed.txt"))
datasetsMuonData.append(Dataset('/SingleMuon/Run2016G-PromptReco-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask=lumiMask))

datasetsTop = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FTT_TuneCUETP8M1_13TeV-powheg-pythia8%2FRunII*16MiniAODv2-*%2FMINIAODSIM"
datasetsTop.append(Dataset('/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext3-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsTTJets = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset+dataset%3D%2FTTJets*%2FRunII*16MiniAODv2-*_reHLT_*%2FMINIAODSIM"
datasetsTTJets.append(Dataset('/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das)) # less stats && -ve weights


datasetsDY = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FDY*%2FRunII*16MiniAODv2-*_reHLT_*%2FMINIAODSIM"
datasetsDY.append(Dataset('/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsWJets = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FWJets*%2FRunII*16MiniAODv2-*_reHLT_*%2FMINIAODSIM"
datasetsWJets.append(Dataset('/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsWJetsToQQ_noReHLT = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FWJetsToQQ_HT-600ToInf_*%2FRunIISpring16MiniAODv2-*%2F*"
datasetsWJetsToQQ_noReHLT.append(Dataset('/WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsTTWJetsToQQ_noReHLT = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FQCD_Pt_*_TuneCUETP8M1_13TeV_pythia8%2FRunII*16MiniAODv2-*_reHLT_*%2FMINIAODSIM"
datasetsTTWJetsToQQ_noReHLT.append(Dataset('/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsTTBB_noReHLT = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2Fttbb_4FS_ckm_amcatnlo_madspin_pythia8*%2FRunIISpring16MiniAODv2-*%2F*"
datasetsTTBB_noReHLT.append(Dataset('/ttbb_4FS_ckm_amcatnlo_madspin_pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsTTBB_noReHLT.append(Dataset('/ttbb_4FS_ckm_amcatnlo_madspin_pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsTTTT_noReHLT = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FTTTT_TuneCUETP8M1*%2FRunIISpring16MiniAODv2-*%2F*"
datasetsTTTT_noReHLT.append(Dataset('/TTTT_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsTTZToQQ_noReHLT = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FTTZToQQ*%2FRunIISpring16MiniAODv2-*%2F*"
datasetsTTZToQQ_noReHLT.append(Dataset('/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsZJetsToQQ = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FZJetsToQQ_HT600toInf*%2FRunIISpring16MiniAODv2-*%2F*"
datasetsZJetsToQQ.append(Dataset('/ZJetsToQQ_HT600toInf_13TeV-madgraph/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsDiboson = []


datasetsDibosonToQQ_noReHLT = []
das1 = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FWZ_TuneCUETP8M1*%2FRunIISpring16MiniAODv2-*%2F*"
das2 = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FWWTo4Q_13TeV-powheg*%2FRunIISpring16MiniAODv2-*%2F*"
das3 = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FZZTo4Q_13TeV*%2FRunIISpring16MiniAODv2-*%2F*"
datasetsDibosonToQQ_noReHLT.append(Dataset('/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das1))
datasetsDibosonToQQ_noReHLT.append(Dataset('/WWTo4Q_13TeV-powheg/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das2))
datasetsDibosonToQQ_noReHLT.append(Dataset('/ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das3))


datasetsSingleTop_noReHLT = []
das1 = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FST_t-channel_antitop_*_TuneCUETP8M1*%2FRunIISpring16MiniAODv2-*%2F*"
das2 = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FST_t-channel_top_4f_inclusiveDecays_*_TuneCUETP8M1*%2FRunIISpring16MiniAODv2-*%2F*"
das3 = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FST_tW_antitop_5f_inclusiveDecays_*_TuneCUETP8M1*%2FRunIISpring16MiniAODv2-*%2F*"
das4 = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FST_tW_top_5f_inclusiveDecays_*_TuneCUETP8M1*%2FRunIISpring16MiniAODv2-*%2F*"
datasetsSingleTop_noReHLT.append(Dataset('/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das1))
datasetsSingleTop_noReHLT.append(Dataset('/ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das2))
datasetsSingleTop_noReHLT.append(Dataset('/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das3))
datasetsSingleTop_noReHLT.append(Dataset('/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v2/MINIAODSIM', dataVersion="80Xmc", dasQuery=das4))



datasetsQCD = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FQCD_Pt_*_TuneCUETP8M1_13TeV_pythia8%2FRunII*16MiniAODv2-*_reHLT_*%2FMINIAODSIM"
datasetsQCD.append(Dataset('/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsQCDbEnriched_noReHLT = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FQCD_bEnriched_*%2FRunIISpring16MiniAODv2-*%2F*"
datasetsQCDbEnriched_noReHLT.append(Dataset('/QCD_bEnriched_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDbEnriched_noReHLT.append(Dataset('/QCD_bEnriched_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDbEnriched_noReHLT.append(Dataset('/QCD_bEnriched_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDbEnriched_noReHLT.append(Dataset('/QCD_bEnriched_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDbEnriched_noReHLT.append(Dataset('/QCD_bEnriched_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDbEnriched_noReHLT.append(Dataset('/QCD_bEnriched_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDbEnriched_noReHLT.append(Dataset('/QCD_bEnriched_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDbEnriched_noReHLT.append(Dataset('/QCD_bEnriched_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsQCDMuEnriched = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FQCD_Pt-*_MuEnriched*_TuneCUETP8M1_13TeV_pythia8%2FRunII*16MiniAODv2-*_reHLT_*%2FMINIAODSIM"
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsSignalTauNu = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FChargedHiggs_TTToHplusBWB_HplusToTauNu_M-*%2FRunII*16MiniAODv2-*%2FMINIAODSIM"
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-80_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-90_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v2/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-100_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-120_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-140_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-150_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-155_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v2/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-160_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v2/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))

datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-180_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v2/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-200_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-220_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-250_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-300_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-350_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-400_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-500_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-750_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v2/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-800_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-1000_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-2000_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-3000_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))

datasetsSignalTB = []
das = " https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FChargedHiggs_HplusTB_HplusToTB_M-*%2FRunII*16MiniAODv2-*%2FMINIAODSIMa"
#datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-180_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-200_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
#datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-220_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
#datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-250_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-300_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
#datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-350_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
#datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-400_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-500_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsNoReHLT = []
datasetsNoReHLT.append(Dataset('/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsNoReHLT.append(Dataset('/ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsNoReHLT.append(Dataset('/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsNoReHLT.append(Dataset('/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v2/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsNoReHLT.append(Dataset('/WW_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsNoReHLT.append(Dataset('/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsNoReHLT.append(Dataset('/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))



#================================================================================================ 
# Dataset Grouping
#================================================================================================ 
tauLegDatasets = []
tauLegDatasets.extend(datasetsMuonData)
tauLegDatasets.extend(datasetsDY)
# tauLegDatasets.extend(datasetsWJets)
# tauLegDatasets.extend(datasetsQCDMuEnriched)
# tauLegDatasets.extend(datasetsH125)


metLegDatasets = []
metLegDatasets.extend(datasetsTauData)
metLegDatasets.extend(datasetsDY)
metLegDatasets.extend(datasetsTop)
metLegDatasets.extend(datasetsWJets)
metLegDatasets.extend(datasetsQCD)


signalAnalysisDatasets = []
signalAnalysisDatasets.extend(datasetsTauData)
signalAnalysisDatasets.extend(datasetsDY)
signalAnalysisDatasets.extend(datasetsTop)
signalAnalysisDatasets.extend(datasetsWJets)
signalAnalysisDatasets.extend(datasetsDiboson)
#signalAnalysisDatasets.extend(datasetsQCD)
signalAnalysisDatasets.extend(datasetsSignalTauNu)
#signalAnalysisDatasets.extend(datasetsSignalTB)


hplus2tbAnalysisDatasets = []
#hplus2tbAnalysisDatasets.extend(datasetsJetHTData)
hplus2tbAnalysisDatasets.extend(datasetsSignalTB)
#hplus2tbAnalysisDatasets.extend(datasetsQCD)   
hplus2tbAnalysisDatasets.extend(datasetsQCDbEnriched_noReHLT)
# hplus2tbAnalysisDatasets.extend(datasetsTop) # tmp: too large for lxplus
#hplus2tbAnalysisDatasets.extend(datasetsTTJets) #less stas && -ve weights
hplus2tbAnalysisDatasets.extend(datasetsZJetsToQQ)
hplus2tbAnalysisDatasets.extend(datasetsTTWJetsToQQ_noReHLT)  
hplus2tbAnalysisDatasets.extend(datasetsTTTT_noReHLT)  
hplus2tbAnalysisDatasets.extend(datasetsTTZToQQ_noReHLT)
hplus2tbAnalysisDatasets.extend(datasetsWJetsToQQ_noReHLT)
hplus2tbAnalysisDatasets.extend(datasetsDibosonToQQ_noReHLT)
# hplus2tbAnalysisDatasets.extend(datasetsSingleTop_noReHLT) #fixme: commented for space issues
# hplus2tbAnalysisDatasets.extend(datasetsTTBB_noReHLT)# fixme: commented for space issues
#
# hplus2tbAnalysisDatasets.extend(datasetsGGJets)
# hplus2tbAnalysisDatasets.extend(datasetsGJets)
# hplus2tbAnalysisDatasets.extend(datasetsTGJets)
# hplus2tbAnalysisDatasets.extend(datasetsTTGJets)     
# hplus2tbAnalysisDatasets.extend(datasetsTTJets)
# hplus2tbAnalysisDatasets.extend(datasetsTTJetsHT)    
# hplus2tbAnalysisDatasets.extend(datasetsTT)
# hplus2tbAnalysisDatasets.extend(datasetsQCDbGenFilter)
# hplus2tbAnalysisDatasets.extend(datasetsQCDHTBins)
# hplus2tbAnalysisDatasets.extend(datasetsDibosonG)    
# hplus2tbAnalysisDatasets.extend(datasetsWWTo4Q)
# hplus2tbAnalysisDatasets.extend(datasetsDYToQQ)
# hplus2tbAnalysisDatasets.extend(datasetsTriboson) 
# hplus2tbAnalysisDatasets.extend(datasetsWJets)


#================================================================================================ 
# Class Definition
#================================================================================================ 
class DatasetGroup:
    def __init__(self, analysis):
        self.verbose   = False
        self.analysis  = analysis
        self.GroupDict = {}
        self.CreateGroups()

    def SetVerbose(verbose):
        self.verbose = verbose
        return


    def Verbose(self, msg, printHeader=False):
        '''
        Simple print function. If verbose option is enabled prints, otherwise does nothing.
        '''
        if not self.verbose:
            return
        self.Print(msg, printHeader)
        return


    def Print(self, msg, printHeader=True):
        '''
        Simple print function. If verbose option is enabled prints, otherwise does nothing.
        '''
        fName = __file__.split("/")[-1]
        cName = self.__class__.__name__
        name  = fName + ": " + cName
        if printHeader:
                print "=== ", name
        print "\t", msg
        return


    def CreateGroups(self):
        '''
        Create dataset grouping in a dictionary for easy access.
        '''

        analyses = ["SignalAnalysis", "Hplus2tbAnalysis", "TauLeg", "METLeg", "All"]
        if self.analysis not in analyses:
            raise Exception("Unknown analysis \"%s\". Please select one of the following: \"%s" % (self.analysis, "\", \"".join(analyses) + "\".") )

        self.GroupDict["SignalAnalysis"]   = signalAnalysisDatasets
        self.GroupDict["Hplus2tbAnalysis"] = hplus2tbAnalysisDatasets
        self.GroupDict["TauLeg"]           = tauLegDatasets
        self.GroupDict["METLeg"]           = metLegDatasets
        self.GroupDict["All"]              = signalAnalysisDatasets + hplus2tbAnalysisDatasets + metLegDatasets + metLegDatasets
        return


    def GetDatasetList(self):
        '''
        Return the dataset list according to the analysis name. 
        Uses pre-defined dictionary mapping: analysis->dataset list
        '''
        return self.GroupDict[self.analysis]


    def PrintDatasets(self, printHeader=False):
        '''
        Print all datasets for given analysis
        '''
        datasetList = self.GroupDict[self.analysis]

        if printHeader==True:
            self.Print("The datasets for analysis \"%s\" are:\n\t%s" % (self.analysis, "\n\t".join(str(d.URL) for d in datasetList) ), True)
        else:
            self.Print("\n\t".join(str(d.URL) for d in datasetList), False)
        return
