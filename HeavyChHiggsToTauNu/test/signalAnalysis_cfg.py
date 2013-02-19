import FWCore.ParameterSet.Config as cms

# Select the version of the data (needed only for interactice running,
# overridden automatically from multicrab
dataVersion="44XmcS6"     # Fall11 MC
#dataVersion="44Xdata"    # Run2011 08Nov and 19Nov ReRecos

dataEras = [
    "Run2011AB", # This is the one for pickEvents, and for counter printout in CMSSW job
    "Run2011A",
    "Run2011B",
]


# Note: Keep number of variations below 200 to keep file sizes reasonable

from HiggsAnalysis.HeavyChHiggsToTauNu.OptimisationScheme import HPlusOptimisationScheme
myOptimisation = HPlusOptimisationScheme()

#myOptimisation.addTauPtVariation([40.0, 50.0, 60.0, 70., 80.])
#myOptimisation.addTauIsolationVariation([])
#myOptimisation.addTauIsolationContinuousVariation([])
#myOptimisation.addRtauVariation([0.0, 0.7, 0.8])
#myOptimisation.addJetNumberSelectionVariation(["GEQ3", "GEQ4"])
#myOptimisation.addJetEtVariation([20.0, 30.0])
#myOptimisation.addJetBetaVariation(["GT0.0","GT0.5","GT0.7"])
#myOptimisation.addMETSelectionVariation([60.0, 70.0, 80.0, 90.,100.0])
#myOptimisation.addBJetLeadingDiscriminatorVariation([0.898, 0.679])
#myOptimisation.addBJetSubLeadingDiscriminatorVariation([0.679, 0.244])
#myOptimisation.addBJetEtVariation([])
#myOptimisation.addBJetNumberVariation(["GEQ1", "GEQ2"])
#myOptimisation.addDeltaPhiVariation([180.0,170.0,160.0,150.0])
#myOptimisation.addTopRecoVariation(["None","chi"]) # Valid options: None, chi, std, Wselection
#myOptimisation.disableMaxVariations()

def customize(signalAnalysis):
    # Apply beta cut for jets to reject PU jets
    signalAnalysis.jetSelection.betaCut = 0.2 # Disable by setting to 0.0; if you want to enable, set to 0.2
#    signalAnalysis.tauSelection.ptCut = 80.0 #
#    signalAnalysis.MET.METCut = 100.0 

from HiggsAnalysis.HeavyChHiggsToTauNu.AnalysisConfiguration import ConfigBuilder
builder = ConfigBuilder(dataVersion, dataEras,
                        maxEvents=-1, # default is -1
                        customizeLightAnalysis=customize,
                        #doHeavyAnalysis=True,
                        #customizeHeavyAnalysis=customize,
                        #doAgainstElectronScan=True,
                        #doSystematics=True,
                        #histogramAmbientLevel = "Vital",
                        #doOptimisation=True, optimisationScheme=myOptimisation
                        )

process = builder.buildSignalAnalysis()

# Doesn't work:
# prefix_TTToHplusBWB_M-120 = "root://madhatter.csc.fi:8443/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4/a7cc08c191a8794be9ec81f73dbf125a/"

#if builder.options.tauEmbeddingInput != 0:
    # process.source.fileNames = [
    #         "root://madhatter.csc.fi:8443/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4/a7cc08c191a8794be9ec81f73dbf125a/pattuple_5_2_D2c.root",
    #         "root://madhatter.csc.fi:8443/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4/a7cc08c191a8794be9ec81f73dbf125a/pattuple_4_2_90j.root",
    #         "root://madhatter.csc.fi:8443/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4/a7cc08c191a8794be9ec81f73dbf125a/pattuple_2_2_i1O.root",
    #         "root://madhatter.csc.fi:8443/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4/a7cc08c191a8794be9ec81f73dbf125a/pattuple_3_2_f6k.root"
    #         ]

process.source.fileNames = [
        "root://madhatter.csc.fi:1094/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4/a7cc08c191a8794be9ec81f73dbf125a/pattuple_5_2_D2c.root",
#         "root://madhatter.csc.fi:8443/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4/a7cc08c191a8794be9ec81f73dbf125a/pattuple_4_2_90j.root",
#             "root://madhatter.csc.fi:8443/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4/a7cc08c191a8794be9ec81f73dbf125a/pattuple_2_2_i1O.root",
#         "root://madhatter.csc.fi:8443/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4/a7cc08c191a8794be9ec81f73dbf125a/pattuple_3_2_f6k.root",
#         "root://madhatter.csc.fi:8443/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4/a7cc08c191a8794be9ec81f73dbf125a/pattuple_5_2_D2c.root"
    ]
    
# process.maxEvents.input = 500



#     if builder.dataVersion.isMC():
#         process.source.fileNames = [
# #            "root://madhatter.csc.fi:1094/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4/f16be938188c46248667b60f0c9e7452/pattuple_490_1_kHI.root"
# #            "file:/afs/cern.ch/work/s/strichte/data/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4/pattuple_7_1_ozc.root"
#             #prefix_TTToHplusBWB_M-120+"pattuple_5_2_D2c.root",
#             "root://madhatter.csc.fi:8443/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4/a7cc08c191a8794be9ec81f73dbf125a/pattuple_4_2_90j.root",
#             "root://madhatter.csc.fi:8443/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4/a7cc08c191a8794be9ec81f73dbf125a/pattuple_2_2_i1O.root",
#             "root://madhatter.csc.fi:8443/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4/a7cc08c191a8794be9ec81f73dbf125a/pattuple_3_2_f6k.root",
#             "root://madhatter.csc.fi:8443/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4/a7cc08c191a8794be9ec81f73dbf125a/pattuple_5_2_D2c.root",
#             #prefix_TTToHplusBWB_M-120+"pattuple_2_2_i1O.root",
#             #prefix_TTToHplusBWB_M-120+"pattuple_3_2_f6k.root",
# #            "root://madhatter.csc.fi:8443/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4/a7cc08c191a8794be9ec81f73dbf125a/pattuple_3_2_f6k.root"
#             ]
#     else:
#         # HLT_Mu40_eta2p1_v1
#         process.source.fileNames = [
# #             "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/SingleMu_Mu_173693-177452_2011B_Nov19/SingleMu/Run2011B_19Nov2011_v1_AOD_173693_tauembedding_embedding_v44_4_2_seed0/a55cb9805ad247805760f23e605c41e5/embedded_9_1_ccy.root",
# #             "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/SingleMu_Mu_173693-177452_2011B_Nov19/SingleMu/Run2011B_19Nov2011_v1_AOD_173693_tauembedding_embedding_v44_4_2_seed0/a55cb9805ad247805760f23e605c41e5/embedded_99_1_Wje.root",
# #             "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/SingleMu_Mu_173693-177452_2011B_Nov19/SingleMu/Run2011B_19Nov2011_v1_AOD_173693_tauembedding_embedding_v44_4_2_seed0/a55cb9805ad247805760f23e605c41e5/embedded_98_1_Qmf.root",
#             ]
        
#         #     process.source.fileNames = [
#         #         "file:/mnt/flustre/mkortela/data/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_pattuple_v44_4/pattuple_7_1_ozc.root"
#         #         ]




#f = open("configDump.py", "w")
#f.write(process.dumpPython())
#f.close()
