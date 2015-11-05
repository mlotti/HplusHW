
lumiMask50ns = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-255031_13TeV_PromptReco_Collisions15_50ns_JSON_v2.txt"
lumiMask25ns = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-259891_13TeV_PromptReco_Collisions15_25ns_JSON.txt"
#lumiMask25nsSilver = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-259891_13TeV_PromptReco_Collisions15_25ns_JSON_Silver.txt"

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
datasetsTauData.append(Dataset('/Tau/Run2015D-PromptReco-v4/MINIAOD',dataVersion="74Xdata",lumiMask=lumiMask25ns))
datasetsTauData.append(Dataset('/Tau/Run2015D-PromptReco-v3/MINIAOD',dataVersion="74Xdata",lumiMask=lumiMask25nsSilver))
datasetsTauData.append(Dataset('/Tau/Run2015D-PromptReco-v4/MINIAOD',dataVersion="74Xdata",lumiMask=lumiMask25nsSilver))

datasetsMuonData = []
#datasetsMuonData.append(Dataset('/SingleMuon/Run2015B-05Aug2015-v1/MINIAOD',dataVersion="74Xdata"))                                                                      
datasetsMuonData.append(Dataset('/SingleMuon/Run2015C-PromptReco-v1/MINIAOD',dataVersion="74Xdata",lumiMask=lumiMask50ns))
datasetsMuonData.append(Dataset('/SingleMuon/Run2015C-PromptReco-v1/MINIAOD',dataVersion="74Xdata",lumiMask=lumiMask25ns))
datasetsMuonData.append(Dataset('/SingleMuon/Run2015D-PromptReco-v3/MINIAOD',dataVersion="74Xdata",lumiMask=lumiMask25ns))
datasetsMuonData.append(Dataset('/SingleMuon/Run2015D-PromptReco-v4/MINIAOD',dataVersion="74Xdata",lumiMask=lumiMask25ns))
datasetsMuonData.append(Dataset('/SingleMuon/Run2015D-PromptReco-v3/MINIAOD',dataVersion="74Xdata",lumiMask=lumiMask25nsSilver))
datasetsMuonData.append(Dataset('/SingleMuon/Run2015D-PromptReco-v4/MINIAOD',dataVersion="74Xdata",lumiMask=lumiMask25nsSilver))

datasetsMiniAODv2_Top = []                                                                                                                                                                          
datasetsMiniAODv2_Top.append(Dataset('/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v3/MINIAODSIM'))                                              
#datasetsMiniAODv2_Top.append(Dataset('/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
#datasetsMiniAODv2_Top.append(Dataset('/TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
#datasetsMiniAODv2_Top.append(Dataset('/TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
#datasetsMiniAODv2_Top.append(Dataset('/TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
#datasetsMiniAODv2_Top.append(Dataset('/TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_Top.append(Dataset('/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))    
datasetsMiniAODv2_Top.append(Dataset('/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM'))        
datasetsMiniAODv2_Top.append(Dataset('/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))    
datasetsMiniAODv2_Top.append(Dataset('/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_Top.append(Dataset('/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
                                                                                                                                                                                                    
datasetsMiniAODv2_DY = []                                                                                                                                                                           
datasetsMiniAODv2_DY.append(Dataset('/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))                                  
datasetsMiniAODv2_DY.append(Dataset('/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))                                      
datasetsMiniAODv2_DY.append(Dataset('/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_DY.append(Dataset('/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_DY.append(Dataset('/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM'))
datasetsMiniAODv2_DY.append(Dataset('/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))

datasetsMiniAODv2_Diboson = []
datasetsMiniAODv2_Diboson.append(Dataset('/WW_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_Diboson.append(Dataset('/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_Diboson.append(Dataset('/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
                                                                                                                                                                                                    
datasetsMiniAODv2_WJets = []                                                                                                                                                                        
datasetsMiniAODv2_WJets.append(Dataset('/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))                                        
datasetsMiniAODv2_WJets.append(Dataset('/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_WJets.append(Dataset('/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_WJets.append(Dataset('/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_WJets.append(Dataset('/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_WJets.append(Dataset('/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_WJets.append(Dataset('/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_WJets.append(Dataset('/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
                                                                                                                                                    
datasetsMiniAODv2_QCD = []                                                                                                                          
datasetsMiniAODv2_QCD.append(Dataset('/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))    
datasetsMiniAODv2_QCD.append(Dataset('/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))    
datasetsMiniAODv2_QCD.append(Dataset('/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))   
datasetsMiniAODv2_QCD.append(Dataset('/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))  
datasetsMiniAODv2_QCD.append(Dataset('/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))  
datasetsMiniAODv2_QCD.append(Dataset('/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))  
datasetsMiniAODv2_QCD.append(Dataset('/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))  
datasetsMiniAODv2_QCD.append(Dataset('/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_QCD.append(Dataset('/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM')) 
datasetsMiniAODv2_QCD.append(Dataset('/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_QCD.append(Dataset('/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_QCD.append(Dataset('/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_QCD.append(Dataset('/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_QCD.append(Dataset('/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM')) 
                                                                                                                                                    
datasetsMiniAODv2_QCDMuEnriched = []                                                                                                                
datasetsMiniAODv2_QCDMuEnriched.append(Dataset('/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))                            
datasetsMiniAODv2_QCDMuEnriched.append(Dataset('/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))                           
datasetsMiniAODv2_QCDMuEnriched.append(Dataset('/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))                          
datasetsMiniAODv2_QCDMuEnriched.append(Dataset('/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))                          
datasetsMiniAODv2_QCDMuEnriched.append(Dataset('/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))                          

datasetsMiniAODv2_Signal = []                                                                                                                                                                                                    
datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-80_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-90_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-100_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-120_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-140_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-150_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-155_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_TTToHplusBWB_HplusToTauNu_M-160_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))

datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-180_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-200_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-220_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-250_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-300_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-350_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM'))
datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-400_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-500_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))

#datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-180_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-200_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
#datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-220_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
#datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-250_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
#datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-300_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
#datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-350_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM'))
#datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-400_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
datasetsMiniAODv2_Signal.append(Dataset('/ChargedHiggs_HplusTB_HplusToTauNu_M-500_13TeV_amcatnlo_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'))
                                                                                                                                                                                  
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
