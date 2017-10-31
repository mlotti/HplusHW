#lumiMask = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON.txt" # ICHEP dataset 271036-276811
lumiMask = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt"


#================================================================================================ 
# Class Definition
#================================================================================================ 
import os

class Dataset:
    def __init__(self, url, dbs="global", dataVersion="80Xmc", dasQuery="", lumiMask=lumiMask, name=""):
        self.URL = url
        self.DBS = dbs
        self.dataVersion = dataVersion
        if not os.path.dirname(lumiMask):
            lumiMask = os.path.join(os.environ['CMSSW_BASE'],"src/HiggsAnalysis/MiniAOD2TTree/data",lumiMask)
        self.lumiMask = lumiMask
        self.DASquery = dasQuery
	self.name = name

    def isData(self):
        if "data" in self.dataVersion:
            return True
        return False

    def getName(self):
	return self.name


#================================================================================================ 
# Data
#================================================================================================ 
datasetsTauData03Feb = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FTau%2FRun2016*-PromptReco-v2%2FMINIAOD"
datasetsTauData03Feb.append(Dataset('/Tau/Run2016B-03Feb2017_ver2-v2/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_273150-275376_13TeV_PromptReco_Collisions16_JSON_Run2016B.txt"))                          
datasetsTauData03Feb.append(Dataset('/Tau/Run2016C-03Feb2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_275420-276283_13TeV_PromptReco_Collisions16_JSON_Run2016C.txt"))                               
datasetsTauData03Feb.append(Dataset('/Tau/Run2016D-03Feb2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_276315-276437_13TeV_PromptReco_Collisions16_JSON_Run2016D_MET80.txt"))                         
datasetsTauData03Feb.append(Dataset('/Tau/Run2016D-03Feb2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_276453-276811_13TeV_PromptReco_Collisions16_JSON_Run2016D_noMET80.txt"))                       
datasetsTauData03Feb.append(Dataset('/Tau/Run2016E-03Feb2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_276824-277420_13TeV_PromptReco_Collisions16_JSON_Run2016E.txt"))                         
datasetsTauData03Feb.append(Dataset('/Tau/Run2016F-03Feb2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_277816-278800_13TeV_PromptReco_Collisions16_JSON_Run2016F_HIP.txt"))                     
datasetsTauData03Feb.append(Dataset('/Tau/Run2016F-03Feb2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_278801-278808_13TeV_PromptReco_Collisions16_JSON_Run2016F_HIPfixed.txt"))                
datasetsTauData03Feb.append(Dataset('/Tau/Run2016G-03Feb2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_278816-280385_13TeV_PromptReco_Collisions16_JSON_Run2016G.txt"))                         
#datasetsTauData03Feb.append(Dataset('/Tau/Run2016H-PromptReco-v1/MINIAOD', dataVersion="80Xdata2016H", dasQuery=das, lumiMask="Cert_281613-284044_13TeV_PromptReco_Collisions16_JSON_Run2016H.txt"))                  
datasetsTauData03Feb.append(Dataset('/Tau/Run2016H-03Feb2017_ver2-v1/MINIAOD', dataVersion="80Xdata2016H", dasQuery=das, lumiMask="Cert_281613-284044_13TeV_PromptReco_Collisions16_JSON_Run2016H.txt"))               
datasetsTauData03Feb.append(Dataset('/Tau/Run2016H-03Feb2017_ver3-v1/MINIAOD', dataVersion="80Xdata2016H", dasQuery=das, lumiMask="Cert_281613-284044_13TeV_PromptReco_Collisions16_JSON_Run2016H.txt"))
datasetsTauData = datasetsTauData03Feb

datasetsTauData18Apr = []
datasetsTauData18Apr.append(Dataset('/Tau/Run2016B-18Apr2017_ver2-v1/MINIAOD', dataVersion="80Xdata18Apr", dasQuery=das, lumiMask="Cert_273150-275376_13TeV_PromptReco_Collisions16_JSON_Run2016B.txt"))
datasetsTauData18Apr.append(Dataset('/Tau/Run2016C-18Apr2017-v1/MINIAOD', dataVersion="80Xdata18Apr", dasQuery=das, lumiMask="Cert_275420-276283_13TeV_PromptReco_Collisions16_JSON_Run2016C.txt"))
datasetsTauData18Apr.append(Dataset('/Tau/Run2016D-18Apr2017-v1/MINIAOD', dataVersion="80Xdata18Apr", dasQuery=das, lumiMask="Cert_276315-276437_13TeV_PromptReco_Collisions16_JSON_Run2016D_MET80.txt"))
datasetsTauData18Apr.append(Dataset('/Tau/Run2016D-18Apr2017-v1/MINIAOD', dataVersion="80Xdata18Apr", dasQuery=das, lumiMask="Cert_276453-276811_13TeV_PromptReco_Collisions16_JSON_Run2016D_noMET80.txt"))
datasetsTauData18Apr.append(Dataset('/Tau/Run2016E-18Apr2017-v1/MINIAOD', dataVersion="80Xdata18Apr", dasQuery=das, lumiMask="Cert_276824-277420_13TeV_PromptReco_Collisions16_JSON_Run2016E.txt"))
datasetsTauData18Apr.append(Dataset('/Tau/Run2016F-18Apr2017-v1/MINIAOD', dataVersion="80Xdata18Apr", dasQuery=das, lumiMask="Cert_277816-278800_13TeV_PromptReco_Collisions16_JSON_Run2016F_HIP.txt"))
datasetsTauData18Apr.append(Dataset('/Tau/Run2016F-18Apr2017-v1/MINIAOD', dataVersion="80Xdata18Apr", dasQuery=das, lumiMask="Cert_278801-278808_13TeV_PromptReco_Collisions16_JSON_Run2016F_HIPfixed.txt"))
datasetsTauData18Apr.append(Dataset('/Tau/Run2016G-18Apr2017-v1/MINIAOD', dataVersion="80Xdata18Apr", dasQuery=das, lumiMask="Cert_278816-280385_13TeV_PromptReco_Collisions16_JSON_Run2016G.txt"))
datasetsTauData18Apr.append(Dataset('/Tau/Run2016H-18Apr2017-v1/MINIAOD', dataVersion="80Xdata18Apr", dasQuery=das, lumiMask="Cert_281613-284044_13TeV_PromptReco_Collisions16_JSON_Run2016H.txt"))

datasetsTauData07Aug2017 = []
datasetsTauData07Aug2017.append(Dataset('/Tau/Run2016B-07Aug17_ver1-v1/MINIAOD', dataVersion="80Xdata18Apr", dasQuery=das, lumiMask="Cert_273150-275376_13TeV_PromptReco_Collisions16_JSON_Run2016B.txt"))
datasetsTauData07Aug2017.append(Dataset('/Tau/Run2016C-07Aug17-v1/MINIAOD', dataVersion="80Xdata18Apr", dasQuery=das, lumiMask="Cert_275420-276283_13TeV_PromptReco_Collisions16_JSON_Run2016C.txt"))
datasetsTauData07Aug2017.append(Dataset('/Tau/Run2016E-07Aug17-v1/MINIAOD', dataVersion="80Xdata18Apr", dasQuery=das, lumiMask="Cert_276824-277420_13TeV_PromptReco_Collisions16_JSON_Run2016E.txt"))


datasetsJetHTData = []
#das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FJetHT%2FRun2016*-03Feb2017*-v*%2FMINIAOD"
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FJetHT%2FRun2016*-18Apr2017*-v*%2FMINIAOD"
#datasetsJetHTData.append(Dataset('/JetHT/Run2016B-03Feb2017_ver1-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask=""))
datasetsJetHTData.append(Dataset('/JetHT/Run2016B-18Apr2017_ver2-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_273150-275376_13TeV_PromptReco_Collisions16_JSON_Run2016B.txt"))
datasetsJetHTData.append(Dataset('/JetHT/Run2016C-18Apr2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_275420-276283_13TeV_PromptReco_Collisions16_JSON_Run2016C.txt"))
datasetsJetHTData.append(Dataset('/JetHT/Run2016D-18Apr2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_276315-276811_13TeV_PromptReco_Collisions16_JSON_Run2016D.txt"))
datasetsJetHTData.append(Dataset('/JetHT/Run2016E-18Apr2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_276824-277420_13TeV_PromptReco_Collisions16_JSON_Run2016E.txt"))
datasetsJetHTData.append(Dataset('/JetHT/Run2016F-18Apr2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_277816-278800_13TeV_PromptReco_Collisions16_JSON_Run2016F_HIP.txt"))
datasetsJetHTData.append(Dataset('/JetHT/Run2016F-18Apr2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_278801-278808_13TeV_PromptReco_Collisions16_JSON_Run2016F_HIPfixed.txt"))
datasetsJetHTData.append(Dataset('/JetHT/Run2016G-18Apr2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_278816-280385_13TeV_PromptReco_Collisions16_JSON_Run2016G.txt"))
datasetsJetHTData.append(Dataset('/JetHT/Run2016H-18Apr2017-v1/MINIAOD', dataVersion="80Xdata2016H", dasQuery=das, lumiMask="Cert_281613-284044_13TeV_PromptReco_Collisions16_JSON_Run2016H.txt"))


datasetsMuonData03Feb = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FSingleMuon%2FRun2016*-PromptReco-v2%2FMINIAOD"                                                                                                                                                        
datasetsMuonData03Feb.append(Dataset('/SingleMuon/Run2016B-03Feb2017_ver2-v2/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_273150-275376_13TeV_PromptReco_Collisions16_JSON_Run2016B.txt")) # Tau used when SingleMuon same                                                                   
datasetsMuonData03Feb.append(Dataset('/SingleMuon/Run2016C-03Feb2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_275420-276283_13TeV_PromptReco_Collisions16_JSON_Run2016C.txt"))                                                                                                        
datasetsMuonData03Feb.append(Dataset('/SingleMuon/Run2016D-03Feb2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_276315-276811_13TeV_PromptReco_Collisions16_JSON_Run2016D.txt"))                                                                                                 
datasetsMuonData03Feb.append(Dataset('/SingleMuon/Run2016E-03Feb2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_276824-277420_13TeV_PromptReco_Collisions16_JSON_Run2016E.txt"))                                                                                           
datasetsMuonData03Feb.append(Dataset('/SingleMuon/Run2016F-03Feb2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_277816-278800_13TeV_PromptReco_Collisions16_JSON_Run2016F_HIP.txt"))                                                                                              
datasetsMuonData03Feb.append(Dataset('/SingleMuon/Run2016F-03Feb2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_278801-278808_13TeV_PromptReco_Collisions16_JSON_Run2016F_HIPfixed.txt"))                                                                                         
datasetsMuonData03Feb.append(Dataset('/SingleMuon/Run2016G-03Feb2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_278816-280385_13TeV_PromptReco_Collisions16_JSON_Run2016G.txt"))                                                                                                  
#datasetsMuonData03Feb.append(Dataset('/SingleMuon/Run2016H-PromptReco-v1/MINIAOD', dataVersion="80Xdata2016H", dasQuery=das, lumiMask="Cert_281010-281202_13TeV_PromptReco_Collisions16_JSON_Run2016H.txt"))                                                                                           
datasetsMuonData03Feb.append(Dataset('/SingleMuon/Run2016H-03Feb2017_ver2-v1/MINIAOD', dataVersion="80Xdata2016H", dasQuery=das, lumiMask="Cert_281613-284044_13TeV_PromptReco_Collisions16_JSON_Run2016H.txt"))                                                                                        
datasetsMuonData03Feb.append(Dataset('/SingleMuon/Run2016H-03Feb2017_ver3-v1/MINIAOD', dataVersion="80Xdata2016H", dasQuery=das, lumiMask="Cert_281613-284044_13TeV_PromptReco_Collisions16_JSON_Run2016H.txt"))

datasetsMuonData18Apr = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FSingleMuon%2FRun2016*-PromptReco-v2%2FMINIAOD"
datasetsMuonData18Apr.append(Dataset('/SingleMuon/Run2016B-18Apr2017_ver2-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_273150-275376_13TeV_PromptReco_Collisions16_JSON_Run2016B.txt")) # Tau used when SingleMuon same
datasetsMuonData18Apr.append(Dataset('/SingleMuon/Run2016C-18Apr2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_275420-276283_13TeV_PromptReco_Collisions16_JSON_Run2016C.txt"))
datasetsMuonData18Apr.append(Dataset('/SingleMuon/Run2016D-18Apr2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_276315-276811_13TeV_PromptReco_Collisions16_JSON_Run2016D.txt"))
datasetsMuonData18Apr.append(Dataset('/SingleMuon/Run2016E-18Apr2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_276830-277420_13TeV_PromptReco_Collisions16_JSON_Run2016E.txt"))
datasetsMuonData18Apr.append(Dataset('/SingleMuon/Run2016F-18Apr2017-v2/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_277816-278800_13TeV_PromptReco_Collisions16_JSON_Run2016F_HIP.txt"))
datasetsMuonData18Apr.append(Dataset('/SingleMuon/Run2016F-18Apr2017-v2/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_278801-278808_13TeV_PromptReco_Collisions16_JSON_Run2016F_HIPfixed.txt"))
datasetsMuonData18Apr.append(Dataset('/SingleMuon/Run2016G-18Apr2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_278816-280385_13TeV_PromptReco_Collisions16_JSON_Run2016G.txt"))
datasetsMuonData18Apr.append(Dataset('/SingleMuon/Run2016H-18Apr2017-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask="Cert_281613-284044_13TeV_PromptReco_Collisions16_JSON_Run2016H.txt"))


datasetsZeroBiasData = []
das = ""
datasetsZeroBiasData.append(Dataset('/ZeroBias/Run2016G-PromptReco-v1/MINIAOD', dataVersion="80Xdata", dasQuery=das, lumiMask=lumiMask))
datasetsZeroBiasData.append(Dataset('/ZeroBias/Run2016H-PromptReco-v2/MINIAOD', dataVersion="80Xdata2016H", dasQuery=das, lumiMask=lumiMask))
datasetsZeroBiasData.append(Dataset('/ZeroBias/Run2016H-PromptReco-v3/MINIAOD', dataVersion="80Xdata2016H", dasQuery=das, lumiMask=lumiMask))



#================================================================================================ 
# MC-RunIISpring16, reHLT
#================================================================================================ 
datasetsSignalTB_reHLT = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FChargedHiggs_HplusTB_HplusToTB_M-*%2FRunII*16MiniAODv2-*%2FMINIAODSIM"
datasetsSignalTB_reHLT.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-180_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTB_reHLT.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-200_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTB_reHLT.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-220_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTB_reHLT.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-250_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTB_reHLT.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-300_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTB_reHLT.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-350_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTB_reHLT.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-400_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTB_reHLT.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-500_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsSignalTauNu_reHLT = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FChargedHiggs_TTToHplusBWB_HplusToTauNu_M-*%2FRunII*16MiniAODv2-*%2FMINIAODSIM"
#datasetsSignalTauNu_reHLT.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-80_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80XmcReHLT", dasQuery=das))
#datasetsSignalTauNu_reHLT.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-90_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v2/MINIAODSIM', dataVersion="80XmcReHLT", dasQuery=das))
#datasetsSignalTauNu_reHLT.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-100_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80XmcReHLT", dasQuery=das))
#datasetsSignalTauNu_reHLT.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-120_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80XmcReHLT", dasQuery=das))
#datasetsSignalTauNu_reHLT.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-140_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80XmcReHLT", dasQuery=das))
#datasetsSignalTauNu_reHLT.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-150_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80XmcReHLT", dasQuery=das))
#datasetsSignalTauNu_reHLT.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-155_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v2/MINIAODSIM', dataVersion="80XmcReHLT", dasQuery=das))
#datasetsSignalTauNu_reHLT.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-160_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v2/MINIAODSIM', dataVersion="80XmcReHLT", dasQuery=das))
#
#datasetsSignalTauNu_reHLT.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-180_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v2/MINIAODSIM', dataVersion="80XmcReHLT", dasQuery=das))
#datasetsSignalTauNu_reHLT.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-200_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80XmcReHLT", dasQuery=das))
#datasetsSignalTauNu_reHLT.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-220_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80XmcReHLT", dasQuery=das))
#datasetsSignalTauNu_reHLT.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-250_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80XmcReHLT", dasQuery=das))
#datasetsSignalTauNu_reHLT.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-300_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80XmcReHLT", dasQuery=das))
#datasetsSignalTauNu_reHLT.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-350_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80XmcReHLT", dasQuery=das))
#datasetsSignalTauNu_reHLT.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-400_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80XmcReHLT", dasQuery=das))
#datasetsSignalTauNu_reHLT.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-500_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80XmcReHLT", dasQuery=das))
datasetsSignalTauNu_reHLT.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-750_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v2/MINIAODSIM', dataVersion="80XmcReHLT", dasQuery=das, name="ChargedHiggs_HplusTB_HplusToTauNu_M_750_reHLT"))
datasetsSignalTauNu_reHLT.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-800_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80XmcReHLT", dasQuery=das, name="ChargedHiggs_HplusTB_HplusToTauNu_M_800_reHLT"))
datasetsSignalTauNu_reHLT.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-1000_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80XmcReHLT", dasQuery=das, name="ChargedHiggs_HplusTB_HplusToTauNu_M_1000_reHLT"))
datasetsSignalTauNu_reHLT.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-2000_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80XmcReHLT", dasQuery=das, name="ChargedHiggs_HplusTB_HplusToTauNu_M_2000_reHLT"))
datasetsSignalTauNu_reHLT.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-3000_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80XmcReHLT", dasQuery=das, name="ChargedHiggs_HplusTB_HplusToTauNu_M_3000_reHLT"))


datasetsQCDMuEnriched_reHLT = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FQCD_Pt-*_MuEnriched*_TuneCUETP8M1_13TeV_pythia8%2FRunII*16MiniAODv2-*_reHLT_*%2FMINIAODSIM"
datasetsQCDMuEnriched_reHLT.append(Dataset('/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched_reHLT.append(Dataset('/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched_reHLT.append(Dataset('/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched_reHLT.append(Dataset('/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched_reHLT.append(Dataset('/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched_reHLT.append(Dataset('/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched_reHLT.append(Dataset('/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched_reHLT.append(Dataset('/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched_reHLT.append(Dataset('/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched_reHLT.append(Dataset('/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched_reHLT.append(Dataset('/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched_reHLT.append(Dataset('/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched_reHLT.append(Dataset('/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched_reHLT.append(Dataset('/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched_reHLT.append(Dataset('/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched_reHLT.append(Dataset('/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched_reHLT.append(Dataset('/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsTop_reHLT = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FTT_TuneCUETP8M1_13TeV-powheg-pythia8%2FRunII*16MiniAODv2-*%2FMINIAODSIM"
datasetsTop_reHLT.append(Dataset('/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext3-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsTTJets_reHLT = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset+dataset%3D%2FTTJets*%2FRunII*16MiniAODv2-*_reHLT_*%2FMINIAODSIM"
datasetsTTJets_reHLT.append(Dataset('/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsDY_reHLT = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FDY*%2FRunII*16MiniAODv2-*_reHLT_*%2FMINIAODSIM"
datasetsDY_reHLT.append(Dataset('/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsWJets_reHLT = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FWJets*%2FRunII*16MiniAODv2-*_reHLT_*%2FMINIAODSIM"
datasetsWJets_reHLT.append(Dataset('/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsZJetsToQQ_reHLT = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FZJetsToQQ_HT600toInf*%2FRunIISpring16MiniAODv2-*%2F*"
datasetsZJetsToQQ_reHLT.append(Dataset('/ZJetsToQQ_HT600toInf_13TeV-madgraph/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsDiboson_reHLT = []


datasetsDibosonToQQ_reHLT = []


datasetsQCD_reHLT = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FQCD_Pt_*_TuneCUETP8M1_13TeV_pythia8%2FRunII*16MiniAODv2-*_reHLT_*%2FMINIAODSIM"
datasetsQCD_reHLT.append(Dataset('/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_reHLT.append(Dataset('/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_reHLT.append(Dataset('/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_reHLT.append(Dataset('/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_reHLT.append(Dataset('/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_reHLT.append(Dataset('/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_reHLT.append(Dataset('/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_reHLT.append(Dataset('/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_reHLT.append(Dataset('/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_reHLT.append(Dataset('/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_reHLT.append(Dataset('/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_reHLT.append(Dataset('/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_reHLT.append(Dataset('/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_reHLT.append(Dataset('/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_reHLT.append(Dataset('/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


#================================================================================================ 
# MC, PUMoriond17
#================================================================================================ 
datasetsSignalTB = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FChargedHiggs_HplusTB_HplusToTB*%2FRunII*PUMoriond17_80X_mcRun2*%2FMINIAODSIM"
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-180_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' , dataVersion="80Xmc", dasQuery=das))
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-200_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' , dataVersion="80Xmc", dasQuery=das))
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-220_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' , dataVersion="80Xmc", dasQuery=das))
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-250_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' , dataVersion="80Xmc", dasQuery=das))
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-300_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' , dataVersion="80Xmc", dasQuery=das))
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-350_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' , dataVersion="80Xmc", dasQuery=das))
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-400_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' , dataVersion="80Xmc", dasQuery=das))
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-500_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' , dataVersion="80Xmc", dasQuery=das))
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-800_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' , dataVersion="80Xmc", dasQuery=das))
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-1000_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-2000_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-3000_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
# more pending?


datasetsSignalTauNu = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FChargedHiggs_TTToHplusBWB_HplusToTauNu_M-*%2FRunII*16MiniAODv2-*%2FMINIAODSIM"
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-180_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-200_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-220_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-250_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-300_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-400_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-500_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_HeavyMass_M-750_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_HeavyMass_M-1000_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_HeavyMass_M-2000_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_HeavyMass_M-3000_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))

# Intermediate H+
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_IntermediateMassNoNeutral_M-145_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
#datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_IntermediateMassNoNeutral_M-150_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
#datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_IntermediateMassNoNeutral_M-155_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
#datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_IntermediateMassNoNeutral_M-160_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
#datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_IntermediateMassNoNeutral_M-165_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
#datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_IntermediateMassNoNeutral_M-170_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_IntermediateMassNoNeutral_M-175_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
#datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_IntermediateMassNoNeutral_M-180_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
#datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_IntermediateMassNoNeutral_M-190_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))

datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_IntermediateMassWithNeutral_M-145_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v3/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
#datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_IntermediateMassWithNeutral_M-150_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v3/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
#datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_IntermediateMassWithNeutral_M-155_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v3/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
#datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_IntermediateMassWithNeutral_M-160_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v3/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
#datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_IntermediateMassWithNeutral_M-165_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v3/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
#datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_IntermediateMassWithNeutral_M-170_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v3/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_IntermediateMassWithNeutral_M-175_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v3/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
#datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_IntermediateMassWithNeutral_M-180_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v3/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
#datasetsSignalTauNu.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_IntermediateMassWithNeutral_M-190_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v3/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))

# Light H+
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-80_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-90_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-100_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-120_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-140_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-150_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-155_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-160_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
#datasetsSignalTauNu.extend(datasetsSignalTauNu_reHLT)
datasetsSignalTauNu.append(Dataset('/HplusToTauNu_M_200_TuneCUETP8M1_tauola_13TeV_pythia8/amarini-GEN-SIM-71-6edf4b210aa48b81088c0de44a7af6f5/USER', dbs="phys03",dataVersion="80Xmc", dasQuery=das))

datasetsSingleTop = []
das1 = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FST_t-channel_antitop*%2FRunII*PUMoriond17_80X_mcRun2*%2FMINIAODSIM"
das2 = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FST_t-channel_top*%2FRunII*PUMoriond17_80X_mcRun2*%2FMINIAODSIM"
das3 = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FST_tW_antitop_5f_inclusive*%2FRunII*PUMoriond17_80X_mcRun2*%2FMINIAODSIM"
das4 = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FST_tW_top_5f_inclusive*%2FRunII*PUMoriond17_80X_mcRun2*%2FMINIAODSIM"
datasetsSingleTop.append(Dataset('/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das1))
datasetsSingleTop.append(Dataset('/ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das2))
datasetsSingleTop.append(Dataset('/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das3))
datasetsSingleTop.append(Dataset('/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das3))
datasetsSingleTop.append(Dataset('/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das4))
datasetsSingleTop.append(Dataset('/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das4))


datasetsTop = []
das = "https://cmsweb.cern.ch/das/request?instance=prod%2Fglobal&view=list&input=dataset%3D%2FTT_%2A%2FRunII%2APUMoriond17_80X_mcRun2%2A%2FMINIAODSIM&idx=150&limit=150"
datasetsTop.append(Dataset('/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das)) # new tune


datasetsTTJets = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=150&instance=prod%2Fglobal&input=dataset%3D%2FTTJets_HT*%2FRunII*PUMoriond17_80X_mcRun2*%2FMINIAODSIM"
datasetsTTJets.append(Dataset('/TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsTTJets.append(Dataset('/TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsTTJets.append(Dataset('/TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsTTJets.append(Dataset('/TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsDY = []
das = "https://cmsweb.cern.ch/das/request?input=dataset%3D%2FDYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8%2FRunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2%2FMINIAODSIM&instance=prod%2Fglobal"
#datasetsDY.append(Dataset('/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-herwigpp_30M/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das, name="DYJetsToLL_M_50_HERWIGPP"))
datasetsDY.append(Dataset('/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsDYJetsToQQ = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=150&instance=prod%2Fglobal&input=dataset%3D%2FDYJetsToQQ_*%2FRunII*PUMoriond17_80X_mcRun2*%2FMINIAODSIM"
datasetsDYJetsToQQ.append(Dataset('/DYJetsToQQ_HT180_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))

datasetsZprime = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FDY*%2FRunII*16MiniAODv2-*_reHLT_*%2FMINIAODSIM"                                                                                                      
datasetsZprime.append(Dataset('/ZprimeToTauTau_M-500_TuneCUETP8M1_13TeV-pythia8-tauola/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsZprime.append(Dataset('/ZprimeToTauTau_M-1000_TuneCUETP8M1_13TeV-pythia8-tauola/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsZprime.append(Dataset('/ZprimeToTauTau_M-3000_TuneCUETP8M1_13TeV-pythia8-tauola/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsWJets = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=150&instance=prod%2Fglobal&input=dataset%3D%2FWJetsToLNu_Tune*%2FRunII*PUMoriond17_80X_mcRun2*%2FMINIAODSIM"
datasetsWJets.append(Dataset('/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsWJets.append(Dataset('/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))

datasetsWJetsHT = []
datasetsWJetsHT.append(Dataset('/WJetsToLNu_HT-70To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsWJetsHT.append(Dataset('/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsWJetsHT.append(Dataset('/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsWJetsHT.append(Dataset('/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsWJetsHT.append(Dataset('/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsWJetsHT.append(Dataset('/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsWJetsHT.append(Dataset('/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsWJetsHT.append(Dataset('/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsWJetsHT.append(Dataset('/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsWJetsHT.append(Dataset('/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsWJetsHT.append(Dataset('/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsWJetsHT.append(Dataset('/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsWJetsHT.append(Dataset('/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsWJetsHT.append(Dataset('/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsWJetsHT.append(Dataset('/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsWJetsHT.append(Dataset('/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsWJetsHT.append(Dataset('/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsWJetsToQQ = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FWJetsToQQ*%2FRunII*PUMoriond17_80X_mcRun2*%2FMINIAODSIM"
datasetsWJetsToQQ.append(Dataset('/WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsZJetsToQQ = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FZJetsToQQ_HT600toInf*%2FRunIISpring16MiniAODv2-*%2F*"
# datasetsZJetsToQQ.append(Dataset('", dasQuery=das))


datasetsDiboson = []
dasWZ = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FWZ*%2FRunII*PUMoriond17_80X_mcRun2*%2FMINIAODSIM"
datasetsDiboson.append(Dataset('/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=dasWZ))
datasetsDiboson.append(Dataset('/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=dasWZ, name="WZ_ext1"))


datasetsDibosonToQQ = []
dasWZ = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FWZ*%2FRunII*PUMoriond17_80X_mcRun2*%2FMINIAODSIM"
dasWW = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FWWTo4Q*%2FRunII*PUMoriond17_80X_mcRun2*%2FMINIAODSIM"
dasZZ = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FZZTo4Q*%2FRunII*PUMoriond17_80X_mcRun2*%2FMINIAODSIM"
datasetsDibosonToQQ.append(Dataset('/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=dasWZ))
datasetsDibosonToQQ.append(Dataset('/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=dasWZ))
datasetsDibosonToQQ.append(Dataset('/WWTo4Q_13TeV-powheg/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=dasWW))
datasetsDibosonToQQ.append(Dataset('/ZZTo4Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=dasZZ))


datasetsQCD = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=150&instance=prod%2Fglobal&input=dataset%3D%2FQCD_Pt*_*TuneCUETP8M1*%2FRunII*PUMoriond17_80X_mcRun2*%2FMINIAODSIM"
datasetsQCD.append(Dataset('/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD.append(Dataset('/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v3/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsQCDMuEnriched = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FQCD_*MuEnrichedPt5*%2FRunII*PUMoriond17_80X_mcRun2*%2FMINIAODSIM"
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v3/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDMuEnriched.append(Dataset('/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsQCDbEnriched = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FQCD_bEnriched*%2FRunII*PUMoriond17_80X_mcRun2*%2FMINIAODSIM"
datasetsQCDbEnriched.append(Dataset('/QCD_bEnriched_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDbEnriched.append(Dataset('/QCD_bEnriched_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDbEnriched.append(Dataset('/QCD_bEnriched_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDbEnriched.append(Dataset('/QCD_bEnriched_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDbEnriched.append(Dataset('/QCD_bEnriched_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDbEnriched.append(Dataset('/QCD_bEnriched_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCDbEnriched.append(Dataset('/QCD_bEnriched_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsQCD_HT_GenJets5 = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset+dataset%3D%2FQCD_HT*_TuneCUETP8M1_13TeV-madgraphMLM-pythia8%2FRunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1%2FMINIAODSIM"
datasetsQCD_HT_GenJets5.append(Dataset('/QCD_HT1500to2000_GenJets5_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_HT_GenJets5.append(Dataset('/QCD_HT2000toInf_GenJets5_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsQCD_HT_BGenFilter = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset+dataset%3D%2FQCD_HT*_TuneCUETP8M1_13TeV-madgraphMLM-pythia8%2FRunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1%2FMINIAODSIM"
datasetsQCD_HT_BGenFilter.append(Dataset('/QCD_HT1000to1500_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_HT_BGenFilter.append(Dataset('/QCD_HT1500to2000_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsQCD_HT = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FQCD_HT*%2FRunII*PUMoriond17_80X_mcRun2*%2FMINIAODSIM"
datasetsQCD_HT.append(Dataset('/QCD_HT50to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_HT.append(Dataset('/QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_HT.append(Dataset('/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_HT.append(Dataset('/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_HT.append(Dataset('/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_HT.append(Dataset('/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_HT.append(Dataset('/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_HT.append(Dataset('/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsQCD_HT.append(Dataset('/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsTTWJetsToQQ = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FTTWJetsToQQ*%2FRunII*PUMoriond17_80X_mcRun2*%2FMINIAODSIM"
datasetsTTWJetsToQQ.append(Dataset('/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


datasetsTTTT = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FTTTT*%2FRunII*PUMoriond17_80X_mcRun2*%2FMINIAODSIM"
datasetsTTTT.append(Dataset('/TTTT_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsTTTT.append(Dataset('/TTTT_TuneCUETP8M2T4_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das)) # new tune


datasetsTTBB = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FTTBB*%2FRunII*PUMoriond17_80X_mcRun2*%2FMINIAODSIM"
# datasetsTTBB.append(Dataset('', dataVersion="80Xmc", dasQuery=das))


datasetsTTZToQQ = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FTTZToQQ*%2FRunII*PUMoriond17_80X_mcRun2*%2FMINIAODSIM"
datasetsTTZToQQ.append(Dataset('/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dasQuery=das))

datasetsNeutrino = []
datasetsNeutrino.append(Dataset('/SingleNeutrino/RunIIHighPUTrainsMiniAODv2-HighPUTrains_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM', dasQuery=das))

#================================================================================================ 
# MC, Trigger Development
#================================================================================================ 
datasetsSignalTauNu_TRGdev = []
das = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2FChargedHiggs_*%2*%2/RAWAODSIM"
datasetsSignalTauNu_TRGdev.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-80_13TeV_amcatnlo_pythia8/PhaseIFall16MiniAOD-FlatPU28to62HcalNZSRAW_PhaseIFall16_81X_upgrade2017_realistic_v26-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu_TRGdev.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-160_13TeV_amcatnlo_pythia8/PhaseIFall16MiniAOD-FlatPU28to62HcalNZSRAW_PhaseIFall16_81X_upgrade2017_realistic_v26-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu_TRGdev.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-200_13TeV_amcatnlo_pythia8/PhaseIFall16MiniAOD-FlatPU28to62HcalNZSRAW_PhaseIFall16_81X_upgrade2017_realistic_v26-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu_TRGdev.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-500_13TeV_amcatnlo_pythia8/PhaseIFall16MiniAOD-FlatPU28to62HcalNZSRAW_PhaseIFall16_81X_upgrade2017_realistic_v26-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))
datasetsSignalTauNu_TRGdev.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-1000_13TeV_amcatnlo_pythia8/PhaseIFall16MiniAOD-FlatPU28to62HcalNZSRAW_PhaseIFall16_81X_upgrade2017_realistic_v26-v1/MINIAODSIM', dataVersion="80Xmc", dasQuery=das))


#================================================================================================ 
# Dataset Grouping
#================================================================================================ 
tauLegDatasets = []
tauLegDatasets.extend(datasetsMuonData03Feb)
tauLegDatasets.extend(datasetsDY)
tauLegDatasets.extend(datasetsZprime)
# tauLegDatasets.extend(datasetsWJets_reHLT)
# tauLegDatasets.extend(datasetsQCDMuEnriched_reHLT)
# tauLegDatasets.extend(datasetsH125)


metLegDatasets = []
metLegDatasets.extend(datasetsTauData03Feb)
metLegDatasets.extend(datasetsDY)
metLegDatasets.extend(datasetsTop)
metLegDatasets.extend(datasetsSingleTop)
metLegDatasets.extend(datasetsWJets)
metLegDatasets.extend(datasetsQCD)

l1Datasets = []
l1Datasets.extend(datasetsZeroBiasData)
l1Datasets.extend(datasetsNeutrino)
l1Datasets.extend(datasetsQCD)

signalAnalysisDatasets = []
#signalAnalysisDatasets.extend(datasetsTauData)
signalAnalysisDatasets.extend(datasetsTauData03Feb)
signalAnalysisDatasets.extend(datasetsTauData18Apr)
signalAnalysisDatasets.extend(datasetsTauData07Aug2017)
signalAnalysisDatasets.extend(datasetsDY) 
signalAnalysisDatasets.extend(datasetsTop)
signalAnalysisDatasets.extend(datasetsSingleTop)
signalAnalysisDatasets.extend(datasetsWJets)  
signalAnalysisDatasets.extend(datasetsDiboson)
#signalAnalysisDatasets.extend(datasetsQCD)
signalAnalysisDatasets.extend(datasetsSignalTauNu)
#signalAnalysisDatasets.extend(datasetsSignalTB)
####signalAnalysisDatasets.extend(datasetsSignalTauNu_TRGdev)

#signalAnalysisDatasets.extend(datasetsDY_reHLT)
#signalAnalysisDatasets.extend(datasetsTop_reHLT)
#signalAnalysisDatasets.extend(datasetsWJets_reHLT)
#signalAnalysisDatasets.extend(datasetsDiboson_reHLT)
##signalAnalysisDatasets.extend(datasetsQCD_reHLT)
#signalAnalysisDatasets.extend(datasetsSignalTauNu_reHLT)
##signalAnalysisDatasets.extend(datasetsSignalTB_reHLT)


hplus2tbAnalysisDatasets = []
hplus2tbAnalysisDatasets.extend(datasetsJetHTData)
hplus2tbAnalysisDatasets.extend(datasetsSignalTB)
hplus2tbAnalysisDatasets.extend(datasetsTop)
hplus2tbAnalysisDatasets.extend(datasetsSingleTop)
hplus2tbAnalysisDatasets.extend(datasetsDYJetsToQQ)
hplus2tbAnalysisDatasets.extend(datasetsWJetsToQQ)
# hplus2tbAnalysisDatasets.extend(datasetsZJetsToQQ_reHLT) # PUMoriond17?
hplus2tbAnalysisDatasets.extend(datasetsDibosonToQQ)
# hplus2tbAnalysisDatasets.extend(datasetsQCD)
hplus2tbAnalysisDatasets.extend(datasetsQCD_HT)
hplus2tbAnalysisDatasets.extend(datasetsQCDbEnriched)
hplus2tbAnalysisDatasets.extend(datasetsTTWJetsToQQ)  
hplus2tbAnalysisDatasets.extend(datasetsTTTT) 
# hplus2tbAnalysisDatasets.extend(datasetsTTBB) # PUMoriond17?
hplus2tbAnalysisDatasets.extend(datasetsTTZToQQ)
# hplus2tbAnalysisDatasets.extend(datasetsQCDMuEnriched)
# hplus2tbAnalysisDatasets.extend(datasetsQCD_HT_BGenFilter) 
# hplus2tbAnalysisDatasets.extend(datasetsQCD_HT_GenJets5) 
# hplus2tbAnalysisDatasets.extend(datasetsTTJets) #-ve weights


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

        analyses = ["SignalAnalysis", "Hplus2tbAnalysis", "TauLeg", "METLeg", "L1Study", "All"]
        if self.analysis not in analyses:
            raise Exception("Unknown analysis \"%s\". Please select one of the following: \"%s" % (self.analysis, "\", \"".join(analyses) + "\".") )

        self.GroupDict["SignalAnalysis"]   = signalAnalysisDatasets
        self.GroupDict["Hplus2tbAnalysis"] = hplus2tbAnalysisDatasets
        self.GroupDict["TauLeg"]           = tauLegDatasets
        self.GroupDict["METLeg"]           = metLegDatasets
        self.GroupDict["L1Study"]          = l1Datasets
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
