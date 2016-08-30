lumiMask = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON.txt" # ICHEP dataset 271036-276811

#================================================================================================ 
# Class Definition
#================================================================================================ 
class Dataset:
    def __init__(self, url, dbs="global", dataVersion="80Xmc", dasQuery="", lumiMask=lumiMask):
        self.URL = url
        self.DBS = dbs
        self.dataVersion = dataVersion
        self.lumiMask = lumiMask
        self.DASquery = dasQuery

    def isData(self):
        if "data" in self.dataVersion:
            return True
        return False

#================================================================================================
# 76X: https://cmsweb.cern.ch/das/request?instance=prod%2Fglobal&view=list&input=dataset%3D%2F%2A%2F%2ARunIIFall15MiniAODv2-PU25nsData2015v1%2A%2F%2A&idx=50&limit=50
#================================================================================================
datasetsTauData76x = []
datasetsTauData76x.append(Dataset('/Tau/Run2015C_25ns-16Dec2015-v1/MINIAOD',dataVersion="76Xdata"))
datasetsTauData76x.append(Dataset('/Tau/Run2015D-16Dec2015-v1/MINIAOD',dataVersion="76Xdata"))


datasetsMuonData76x = []
#datasetsMuonData76x.append(Dataset('/SingleMuon/Run2015D-05Oct2015-v1/MINIAOD',dataVersion="76Xdata"))
#datasetsMuonData76x.append(Dataset('/SingleMuon/Run2015D-PromptReco-v4/MINIAOD',dataVersion="76Xdata"))
datasetsMuonData76x.append(Dataset('/SingleMuon/Run2015D-16Dec2015-v1/MINIAOD',dataVersion="76Xdata"))


datasetsMiniAODv2_TT76x = []
#datasetsMiniAODv2_TT76x.append(Dataset('/TT_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
#datasetsMiniAODv2_TT76x.append(Dataset('/TT_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM'))
#datasetsMiniAODv2_TT76x.append(Dataset('/TT_TuneCUETP8M1_13TeV-powheg-pythia8-evtgen/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_TT76x.append(Dataset('/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext3-v1/MINIAODSIM'))
datasetsMiniAODv2_TT76x.append(Dataset('/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext4-v1/MINIAODSIM'))


datasetsMiniAODv2_Top76x = []
datasetsMiniAODv2_Top76x.extend(datasetsMiniAODv2_TT76x)
datasetsMiniAODv2_Top76x.append(Dataset('/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_Top76x.append(Dataset('/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_Top76x.append(Dataset('/ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_Top76x.append(Dataset('/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_Top76x.append(Dataset('/ST_s-channel_4f_InclusiveDecays_13TeV-amcatnlo-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))


datasetsMiniAODv2_DY76x = []
datasetsMiniAODv2_DY76x.append(Dataset('/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
#datasetsMiniAODv2_DY76x.append(Dataset('/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
#datasetsMiniAODv2_DY76x.append(Dataset('/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
#datasetsMiniAODv2_DY76x.append(Dataset('/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))


datasetsMiniAODv2_H12576x = []
datasetsMiniAODv2_H12576x.append(Dataset('/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))


datasetsMiniAODv2_Diboson76x = []
datasetsMiniAODv2_Diboson76x.append(Dataset('/WW_TuneCUETP8M1_13TeV-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_Diboson76x.append(Dataset('/WZ_TuneCUETP8M1_13TeV-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_Diboson76x.append(Dataset('/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))


datasetsMiniAODv2_WJets76x = []
datasetsMiniAODv2_WJets76x.append(Dataset('/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
#datasetsMiniAODv2_WJets76x.append(Dataset('/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
#datasetsMiniAODv2_WJets76x.append(Dataset('/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
#datasetsMiniAODv2_WJets76x.append(Dataset('/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
#datasetsMiniAODv2_WJets76x.append(Dataset('/WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))


datasetsMiniAODv2_WZJets76x = []
datasetsMiniAODv2_WZJets76x.append(Dataset('/WZJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))


datasetsMiniAODv2_QCD76x = []                                                                                                                          
datasetsMiniAODv2_QCD76x.append(Dataset('/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))    
datasetsMiniAODv2_QCD76x.append(Dataset('/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCD76x.append(Dataset('/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))   
datasetsMiniAODv2_QCD76x.append(Dataset('/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))  
datasetsMiniAODv2_QCD76x.append(Dataset('/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))  
datasetsMiniAODv2_QCD76x.append(Dataset('/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))  
datasetsMiniAODv2_QCD76x.append(Dataset('/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))  
datasetsMiniAODv2_QCD76x.append(Dataset('/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCD76x.append(Dataset('/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM')) 
datasetsMiniAODv2_QCD76x.append(Dataset('/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCD76x.append(Dataset('/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCD76x.append(Dataset('/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCD76x.append(Dataset('/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCD76x.append(Dataset('/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM')) 
                                                                                                                                                    

datasetsMiniAODv2_QCDMuEnriched76x = []
datasetsMiniAODv2_QCDMuEnriched76x.append(Dataset('/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDMuEnriched76x.append(Dataset('/QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDMuEnriched76x.append(Dataset('/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDMuEnriched76x.append(Dataset('/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDMuEnriched76x.append(Dataset('/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDMuEnriched76x.append(Dataset('/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDMuEnriched76x.append(Dataset('/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDMuEnriched76x.append(Dataset('/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDMuEnriched76x.append(Dataset('/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDMuEnriched76x.append(Dataset('/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDMuEnriched76x.append(Dataset('/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v3/MINIAODSIM'))
datasetsMiniAODv2_QCDMuEnriched76x.append(Dataset('/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDMuEnriched76x.append(Dataset('/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v3/MINIAODSIM'))



datasetsMiniAODv2_SignalTauNu76x = []
datasetsMiniAODv2_SignalTauNu76x.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-80_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTauNu76x.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-90_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTauNu76x.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-100_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTauNu76x.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-120_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v7/MINIAODSIM'))
datasetsMiniAODv2_SignalTauNu76x.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-140_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v3/MINIAODSIM'))
datasetsMiniAODv2_SignalTauNu76x.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-150_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTauNu76x.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-155_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTauNu76x.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-160_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))

datasetsMiniAODv2_SignalTauNu76x.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-180_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTauNu76x.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-200_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTauNu76x.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-220_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTauNu76x.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-250_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTauNu76x.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-300_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTauNu76x.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-350_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTauNu76x.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-400_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTauNu76x.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-500_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTauNu76x.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-750_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTauNu76x.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-800_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTauNu76x.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-1000_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTauNu76x.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-2000_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTauNu76x.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-3000_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))

#================================================================================================ 
# Dataset definition
#================================================================================================ 

datasetsMiniAODv2_SignalTB76x = []
datasetsMiniAODv2_SignalTB76x.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauB_M-180_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTB76x.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauB_M-200_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTB76x.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauB_M-220_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTB76x.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauB_M-250_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTB76x.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauB_M-300_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTB76x.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauB_M-350_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTB76x.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauB_M-400_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_SignalTB76x.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauB_M-500_13TeV_amcatnlo_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))

datasetsMiniAODv2_DYToQQ76x = []
datasetsMiniAODv2_DYToQQ76x.append(Dataset('/DYJetsToQQ_HT180_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
#DYJetsToTauTau ?


datasetsMiniAODv2_QCDbGenFilter76x = []
datasetsMiniAODv2_QCDbGenFilter76x.append(Dataset('/QCD_HT100to200_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDbGenFilter76x.append(Dataset('/QCD_HT200to300_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDbGenFilter76x.append(Dataset('/QCD_HT300to500_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDbGenFilter76x.append(Dataset('/QCD_HT500to700_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDbGenFilter76x.append(Dataset('/QCD_HT700to1000_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDbGenFilter76x.append(Dataset('/QCD_HT1000to1500_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDbGenFilter76x.append(Dataset('/QCD_HT1500to2000_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDbGenFilter76x.append(Dataset('/QCD_HT2000toInf_BGenFilter_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))


datasetsMiniAODv2_QCDHTBins76x = []
datasetsMiniAODv2_QCDHTBins76x.append(Dataset('/QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDHTBins76x.append(Dataset('/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDHTBins76x.append(Dataset('/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v3/MINIAODSIM'))
datasetsMiniAODv2_QCDHTBins76x.append(Dataset('/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDHTBins76x.append(Dataset('/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDHTBins76x.append(Dataset('/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDHTBins76x.append(Dataset('/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDHTBins76x.append(Dataset('/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDHTBins76x.append(Dataset('/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDHTBins76x.append(Dataset('/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDHTBins76x.append(Dataset('/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDHTBins76x.append(Dataset('/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDHTBins76x.append(Dataset('/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDHTBins76x.append(Dataset('/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDHTBins76x.append(Dataset('/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM'))


datasetsMiniAODv2_QCDbEnriched76X = []
datasetsMiniAODv2_QCDbEnriched76X.append(Dataset('/QCD_bEnriched_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDbEnriched76X.append(Dataset('/QCD_bEnriched_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDbEnriched76X.append(Dataset('/QCD_bEnriched_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_QCDbEnriched76X.append(Dataset('/QCD_bEnriched_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))


datasetsMiniAODv2_GGJets76x = []
datasetsMiniAODv2_GGJets76x.append(Dataset('/GGJets_M-60To200_Pt-50_13TeV-sherpa/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_GGJets76x.append(Dataset('/GGJets_M-200To500_Pt-50_13TeV-sherpa/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_GGJets76x.append(Dataset('/GGJets_M-1000To2000_Pt-50_13TeV-sherpa/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_GGJets76x.append(Dataset('/GGJets_M-2000To4000_Pt-50_13TeV-sherpa/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_GGJets76x.append(Dataset('/GGJets_M-4000To6000_Pt-50_13TeV-sherpa/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_GGJets76x.append(Dataset('/GGJets_M-6000To8000_Pt-50_13TeV-sherpa/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_GGJets76x.append(Dataset('/GGJets_M-8000To13000_Pt-50_13TeV-sherpa/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))


datasetsMiniAODv2_GJets76x = []
datasetsMiniAODv2_GJets76x.append(Dataset('/GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_GJets76x.append(Dataset('/GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_GJets76x.append(Dataset('/GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_GJets76x.append(Dataset('/GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v3/MINIAODSIM'))
datasetsMiniAODv2_GJets76x.append(Dataset('/GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))


datasetsMiniAODv2_TGJets76x = []
datasetsMiniAODv2_TGJets76x.append(Dataset('/TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_TGJets76x.append(Dataset('/TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM'))


datasetsMiniAODv2_TTGJets76x = []
datasetsMiniAODv2_TTGJets76x.append(Dataset('/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))


datasetsMiniAODv2_TTJets76x = []
datasetsMiniAODv2_TTJets76x.append(Dataset('/TTJets_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM'))
datasetsMiniAODv2_TTJets76x.append(Dataset('/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_TTJets76x.append(Dataset('/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_reHLT_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_TTJets76x.append(Dataset('/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))


datasetsMiniAODv2_TTJetsHT76x = []
datasetsMiniAODv2_TTJetsHT76x.append(Dataset('/TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_TTJetsHT76x.append(Dataset('/TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM'))
datasetsMiniAODv2_TTJetsHT76x.append(Dataset('/TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_TTJetsHT76x.append(Dataset('/TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM'))
datasetsMiniAODv2_TTJetsHT76x.append(Dataset('/TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_TTJetsHT76x.append(Dataset('/TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM'))
datasetsMiniAODv2_TTJetsHT76x.append(Dataset('/TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'))
datasetsMiniAODv2_TTJetsHT76x.append(Dataset('/TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM'))



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
# hplus2tbAnalysisDatasets.extend(datasetsDYToQQ)
hplus2tbAnalysisDatasets.extend(datasetsQCD)   
## hplus2tbAnalysisDatasets.extend(datasetsQCDbEnriched)
## hplus2tbAnalysisDatasets.extend(datasetsQCDbGenFilter)
## hplus2tbAnalysisDatasets.extend(datasetsQCDHTBins)
hplus2tbAnalysisDatasets.extend(datasetsTop)
## h plus2tbAnalysisDatasets.extend(datasetsTT)
## hplus2tbAnalysisDatasets.extend(datasetsGGJets)
## hplus2tbAnalysisDatasets.extend(datasetsGJets)
## hplus2tbAnalysisDatasets.extend(datasetsTGJets)
## hplus2tbAnalysisDatasets.extend(datasetsTTGJets)     
## hplus2tbAnalysisDatasets.extend(datasetsTTJets)
## hplus2tbAnalysisDatasets.extend(datasetsTTJetsHT)    
# hplus2tbAnalysisDatasets.extend(datasetsTTWJets)
# hplus2tbAnalysisDatasets.extend(datasetsTTZJets)
# hplus2tbAnalysisDatasets.extend(datasetsTTWJetsToQQ)  
# hplus2tbAnalysisDatasets.extend(datasetsTTTT)  
# hplus2tbAnalysisDatasets.extend(datasetsTTZToQQ)
# hplus2tbAnalysisDatasets.extend(datasetsWJetsToQQ)    
# hplus2tbAnalysisDatasets.extend(datasetsZJetsToQQ)    
# hplus2tbAnalysisDatasets.extend(datasetsDiboson) #    
## hplus2tbAnalysisDatasets.extend(datasetsDibosonG)    
## hplus2tbAnalysisDatasets.extend(datasetsWWTo4Q)
## hplus2tbAnalysisDatasets.extend(datasetsZZTo4Q)
# hplus2tbAnalysisDatasets.extend(datasetsttbb)  
# hplus2tbAnalysisDatasets.extend(datasetsTriboson) 


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

        analyses = ["SignalAnalysis", "Hplus2tbAnalysis", "TauLeg", "METLeg"]
        if self.analysis not in analyses:
            raise Exception("Unknown analysis \"%s\". Please select one of the following:\n" % ("\n".join(analyses) ) )

        self.GroupDict["SignalAnalysis"]   = signalAnalysisDatasets
        self.GroupDict["Hplus2tbAnalysis"] = hplus2tbAnalysisDatasets
        self.GroupDict["TauLeg"]           = tauLegDatasets
        self.GroupDict["METLeg"]           = metLegDatasets
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
