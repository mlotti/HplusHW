lumiMask = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-275125_13TeV_PromptReco_Collisions16_JSON.txt"


class Dataset :
    def __init__(self,url,dbs="global",dataVersion="80Xmc",lumiMask=lumiMask):
        self.URL = url
        self.DBS = dbs
        self.dataVersion = dataVersion
        self.lumiMask = lumiMask

    def isData(self):
        if "data" in self.dataVersion:
            return True
        return False


datasetsTauData = []
datasetsTauData.append(Dataset('/Tau/Run2016B-PromptReco-v2/MINIAOD',dataVersion="80Xdata"))
datasetsTauData.append(Dataset('/Tau/Run2016C-PromptReco-v2/MINIAOD',dataVersion="80Xdata"))

datasetsJetHTData = []
datasetsJetHTData.append(Dataset('JetHT/Run2016B-PromptReco-v2/MINIAOD',dataVersion="80Xdata"))

datasetsMuonData = []
datasetsMuonData.append(Dataset('/SingleMuon/Run2016B-PromptReco-v2/MINIAOD',dataVersion="80Xdata"))

datasetsTop =[]
datasetsTop.append(Dataset('/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext3-v1/MINIAODSIM'))

datasetsSignalTauNu = []
datasetsSignalTB.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-120_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM'))

datasetsSignalTB = []
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-180_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM'))
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-200_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM'))
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-220_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM'))
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-250_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM'))
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-300_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM'))
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-350_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM'))
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-400_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM'))
datasetsSignalTB.append(Dataset('/ChargedHiggs_HplusTB_HplusToTB_M-500_13TeV_amcatnlo_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM'))
