import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

################################################################################
# Configuration

# Select the version of the data (needed only for interactice running,
# overridden automatically from multicrab
dataVersion="44XmcS6"     # Fall11 MC
#dataVersion="44Xdata"    # Run2011 08Nov and 19Nov ReRecos

# Set the data scenario for vertex/pileup weighting
# options: Run2011A, Run2011B, Run2011A+B
puweight = "Run2011A+B"

##########
# Flags for additional signal analysis modules

# Apply summer PAS style cuts
doSummerPAS = False # Rtau>0, MET>70

# Scan against electron discriminators
doAgainstElectronScan = False

# Disable Rtau
doRtau0 = False # Rtau>0, MET>50

# Perform b tagging scanning
doBTagScan = False


# fill tree for btagging eff study
doBTagTree = False

    
# Perform Rtau scanning
doRtauScan = False

# Make MET resolution histograms
doMETResolution = False

# With tau embedding input, tighten the muon selection
tauEmbeddingFinalizeMuonSelection = True
# With tau embedding input, do the muon selection scan
doTauEmbeddingMuonSelectionScan = False
# Do tau id scan for tau embedding normalisation (no tau embedding input required)
doTauEmbeddingTauSelectionScan = False
# Do embedding-like preselection for signal analysis
doTauEmbeddingLikePreselection = False

# Apply beta cut for jets to reject PU jets
betaCutForJets = 0.2 # Disable by setting to 0.0; if you want to enable, set to 0.2

######### 
#Flags for options in the signal analysis

# Keep / Ignore prescaling for data (suppresses greatly error messages 
# in datasets with or-function of triggers)
doPrescalesForData = False

# Tree filling
doFillTree = False

# Set level of how many histograms are stored to files
# options are: 'Vital' (least histograms), 'Informative', 'Debug' (all histograms)
myHistogramAmbientLevel = "Debug"

# Apply trigger scale factor or not

applyTriggerScaleFactor = True

PF2PATVersion = "PFlow" # For normal PF2PAT
#PF2PATVersion = "PFlowChs" # For PF2PAT with CHS

### Systematic uncertainty flags ###
# Running of systematic variations is controlled by the global flag
# (below), or the individual flags
doSystematics = False

# Perform the signal analysis with the JES variations in addition to
# the "golden" analysis
doJESVariation = False

# Perform the signal analysis with the PU weight variations
# https://twiki.cern.ch/twiki/bin/view/CMS/PileupSystematicErrors
doPUWeightVariation = False

# Do variations for optimisation
# Note: Keep number of variations below 200 to keep file sizes reasonable
# Note: Currently it is not possible to vary the tau selection -related variables, because only one JES and MET producer is made (tau selection influences type I MET correction and JES)

doOptimisation = False

from HiggsAnalysis.HeavyChHiggsToTauNu.OptimisationScheme import HPlusOptimisationScheme
myOptimisation = HPlusOptimisationScheme()
#myOptimisation.addTauPtVariation([40.0, 50.0])
#myOptimisation.addTauIsolationVariation([])
#myOptimisation.addTauIsolationContinuousVariation([])
#myOptimisation.addRtauVariation([0.0, 0.7])
#myOptimisation.addJetNumberSelectionVariation(["GEQ3", "GEQ4"])
#myOptimisation.addJetEtVariation([20.0, 30.0])
#myOptimisation.addJetBetaVariation(["GT0.0","GT0.5","GT0.7"])
myOptimisation.addMETSelectionVariation([50.0, 60.0, 70.0])
#myOptimisation.addBJetLeadingDiscriminatorVariation([0.898, 0.679])
#myOptimisation.addBJetSubLeadingDiscriminatorVariation([0.679, 0.244])
#myOptimisation.addBJetEtVariation([])
#myOptimisation.addBJetNumberVariation(["GEQ1", "GEQ2"])
#myOptimisation.addDeltaPhiVariation([180.0,160.0,140.0])
#myOptimisation.addTopRecoVariation(["None","chi"]) # Valid options: None, chi, std, Wselection
myOptimisation.disableMaxVariations()
if doOptimisation:
    doSystematics = True # Make sure that systematics are run
    doFillTree = False # Make sure that tree filling is disabled or root file size explodes
    myHistogramAmbientLevel = "Vital" # Set histogram level to least histograms to reduce output file sizes

################################################################################

# Command line arguments (options) and DataVersion object
options, dataVersion = getOptionsDataVersion(dataVersion)

# These are needed for running against tau embedding samples, can be
# given also from command line
#options.doPat=1
#options.tauEmbeddingInput=1

################################################################################
# Define the process
process = cms.Process("HChSignalAnalysis")


#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(20) )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
#    "rfio:/castor/cern.ch/user/a/attikis/pattuples/testing/v18/pattuple_v18_TTJets_TuneZ2_Summer11_9_1_bfN.root"
#    "file:/tmp/slehti/TTJets_TuneZ2_Summer11_pattuple_266_1_at8.root"
    # For testing in lxplus
    #dataVersion.getAnalysisDefaultFileCastor()
    # For testing in jade
#    dataVersion.getAnalysisDefaultFileMadhatter()
    #dataVersion.getAnalysisDefaultFileMadhatterDcap()


     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_34_1_YeG.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_39_1_egt.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_8_1_N9K.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_35_1_qIb.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_29_1_uO4.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_9_1_OVD.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_12_1_epl.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_20_1_X0Q.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_37_1_IVo.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_33_1_Zry.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_7_1_I5X.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_15_1_28m.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_24_1_yX8.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_30_1_EUo.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_25_1_NoY.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_38_1_hgD.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_27_1_vg1.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_19_1_RBQ.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_1_1_de4.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_17_1_LnY.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_44_1_uJn.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_40_1_N6N.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_5_1_Hkv.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_46_1_7Z0.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_49_1_uOC.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_2_1_sW6.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_14_1_jeq.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_6_1_3fp.root",
     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_26_1_RrQ.root"
#     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_18_1_4Fc.root",
#     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_22_1_JnR.root",
#     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_31_1_hNk.root",
#     "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_28_1_c4O.root"
    

     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_34_1_YeG.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_39_1_egt.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_8_1_N9K.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_35_1_qIb.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_29_1_uO4.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_9_1_OVD.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_12_1_epl.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_20_1_X0Q.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_37_1_IVo.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_33_1_Zry.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_7_1_I5X.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_15_1_28m.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_24_1_yX8.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_30_1_EUo.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_25_1_NoY.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_38_1_hgD.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_27_1_vg1.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_19_1_RBQ.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_1_1_de4.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_17_1_LnY.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_44_1_uJn.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_40_1_N6N.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_5_1_Hkv.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_46_1_7Z0.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_49_1_uOC.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_2_1_sW6.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_14_1_jeq.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_6_1_3fp.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_26_1_RrQ.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_18_1_4Fc.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_22_1_JnR.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_31_1_hNk.root",
     #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_28_1_c4O.root"


    #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/Tau_173236-173692_2011A_Nov08/Tau/Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_Tau_173236-173692_2011A_Nov08//d7b7dcb6c55f2b2177021b8423a82913/pattuple_10_1_9l2.root",
    #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/Tau_175860-180252_2011B_Nov19/Tau/Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3_test2_Tau_175860-180252_2011B_Nov19//28e7e0ab56ad4146eca1efa805cd10f4/pattuple_100_1_jnU.root",
#    "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTToHplusBWB_M120_Fall11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_TTToHplusBWB_M120_Fall11/867f8948ab405c5cced92453543fca46/pattuple_5_1_Hkv.root"

#    "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/Tau_160431-167913_2011A_Nov08/Tau/Fall11_START44_V9B_v1_AODSIM-pattuple_v25b_nojetskim_Tau_160431-167913_2011A_Nov08/6a35806d4ee51a0fcded80eb169c9c26/pattuple_1_1_63v.root"
    )
)

if options.tauEmbeddingInput != 0:
    if  options.doPat == 0:
        raise Exception("In tau embedding input mode, set also doPat=1")

    process.source.fileNames = [
        #"file:/mnt/flustre/wendland/embedded_latest.root"
        "file:/home/wendland/v25_embed/CMSSW_4_4_4/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/tauEmbedding/embedded.root"
        # For testing data
        #"/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/SingleMu_Mu_160431-163261_2011A_Nov08/SingleMu/Tauembedding_embedding_v44_2_SingleMu_Mu_160431-163261_2011A_Nov08/c7fbae985f4002d5d76ea04408a27e38/embedded_1_1_Lka.root"
        ]
    process.maxEvents.input = 10

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())
if options.tauEmbeddingInput != 0:
    process.GlobalTag.globaltag = "START44_V13::All"
print "GlobalTag="+process.GlobalTag.globaltag.value()

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")

# Uncomment the following in order to print the counters at the end of
# the job (note that if many other modules are being run in the same
# job, their INFO messages are printed too)
#process.MessageLogger.cerr.threshold = cms.untracked.string("INFO")
#process.MessageLogger.cerr.FwkReport.reportEvery = 1
#process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

# Fragment to run PAT on the fly if requested from command line
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPatOnTheFly
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion)

# Add configuration information to histograms.root
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addConfigInfo
process.infoPath = addConfigInfo(process, options, dataVersion)

################################################################################
# The "golden" version of the signal analysis
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
param.overrideTriggerFromOptions(options)
param.trigger.triggerSrc.setProcessName(dataVersion.getTriggerProcess())
# Set tau selection mode to 'standard'
param.setAllTauSelectionOperatingMode('standard')
#
#param.setAllTauSelectionOperatingMode('tauCandidateSelectionOnly')

# Set tau sources to trigger matched tau collections
#param.setAllTauSelectionSrcSelectedPatTaus()
param.setAllTauSelectionSrcSelectedPatTausTriggerMatched()

# Switch to PF2PAT objects
#param.changeCollectionsToPF2PAT()
param.changeCollectionsToPF2PAT(postfix=PF2PATVersion)

# Trigger with scale factors (at the moment hard coded)
if applyTriggerScaleFactor and dataVersion.isMC():
    param.triggerEfficiencyScaleFactor.mode = "scaleFactor"

# Set the data scenario for vertex/pileup weighting
if len(options.puWeightEra) > 0:
    puweight = options.puWeightEra
param.setPileupWeight(dataVersion, process=process, commonSequence=process.commonSequence, pset=param.vertexWeight, psetReader=param.vertexWeightReader, era=puweight) # Reweight by true PU distribution
param.setDataTriggerEfficiency(dataVersion, era=puweight)
print "PU weight era =",puweight

#param.trigger.selectionType = "disabled"

import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as tauEmbeddingCustomisations
if options.tauEmbeddingInput != 0:
    #tauEmbeddingCustomisations.addMuonIsolationEmbeddingForSignalAnalysis(process, process.commonSequence)
    tauEmbeddingCustomisations.setCaloMetSum(process, process.commonSequence, options, dataVersion)
    tauEmbeddingCustomisations.customiseParamForTauEmbedding(param, options, dataVersion)
    if dataVersion.isMC():
        process.muonTriggerFixSequence = cms.Sequence()
        additionalCounters.extend(tauEmbeddingCustomisations.addMuonTriggerFix(process, dataVersion, process.muonTriggerFixSequence, options))
        process.commonSequence.replace(process.patSequence, process.muonTriggerFixSequence*process.patSequence)
    if tauEmbeddingFinalizeMuonSelection:
        #applyIsolation = not doTauEmbeddingMuonSelectionScan
        applyIsolation = False
        additionalCounters.extend(tauEmbeddingCustomisations.addFinalMuonSelection(process, process.commonSequence, param,
                                                                                   enableIsolation=applyIsolation))
if doBTagTree:
    param.tree.fillNonIsoLeptonVars = cms.untracked.bool(True)
    param.setAllTauSelectionOperatingMode('tauCandidateSelectionOnly')
    param.MET.METCut = cms.untracked.double(0.0)
    param.bTagging.discriminatorCut = cms.untracked.double(-999)
    param.GlobalMuonVeto.MuonPtCut = cms.untracked.double(999)

# Signal analysis module for the "golden analysis"
import HiggsAnalysis.HeavyChHiggsToTauNu.signalAnalysis as signalAnalysis
process.signalAnalysis = signalAnalysis.createEDFilter(param)
if not doFillTree:
    process.signalAnalysis.Tree.fill = cms.untracked.bool(False)
process.signalAnalysis.histogramAmbientLevel = myHistogramAmbientLevel

if options.tauEmbeddingInput != 0:
    process.signalAnalysis.tauEmbeddingStatus = True

# process.signalAnalysis.GlobalMuonVeto = param.NonIsolatedMuonVeto
# Change default tau algorithm here if needed
#process.signalAnalysis.tauSelection.tauSelectionHPSTightTauBased # HPS Tight is the default

# Btagging DB
process.load("CondCore.DBCommon.CondDBCommon_cfi")
#MC measurements 
process.load ("RecoBTag.PerformanceDB.PoolBTagPerformanceDBMC36X")
process.load ("RecoBTag.PerformanceDB.BTagPerformanceDBMC36X")
#Data measurements
process.load ("RecoBTag.PerformanceDB.BTagPerformanceDB1107")
process.load ("RecoBTag.PerformanceDB.PoolBTagPerformanceDB1107")
#User DB for btag eff
btagDB = 'sqlite_file:../data/DBs/BTAGTCHEL_hplusBtagDB_TTJets.db'
if options.runOnCrab != 0:
    print "BTagDB: Assuming that you are running on CRAB"
    btagDB = "sqlite_file:src/HiggsAnalysis/HeavyChHiggsToTauNu/data/DBs/BTAGTCHEL_hplusBtagDB_TTJets.db"
else:
    print "BTagDB: Assuming that you are not running on CRAB (if you are running on CRAB, add to job parameters in multicrab.cfg runOnCrab=1)"
process.CondDBCommon.connect = btagDB
process.load ("HiggsAnalysis.HeavyChHiggsToTauNu.Pool_BTAGTCHEL_hplusBtagDB_TTJets")
process.load ("HiggsAnalysis.HeavyChHiggsToTauNu.Btag_BTAGTCHEL_hplusBtagDB_TTJets")
    
param.bTagging.UseBTagDB  = cms.untracked.bool(False)



# Add type 1 MET
import HiggsAnalysis.HeavyChHiggsToTauNu.HChMetCorrection as MetCorrection
sequence = MetCorrection.addCorrectedMet(process, process.signalAnalysis, postfix=PF2PATVersion)
process.commonSequence *= sequence

# Set beta variable for jets
process.signalAnalysis.jetSelection.betaCut = betaCutForJets

# Prescale fetching done automatically for data
if dataVersion.isData() and options.tauEmbeddingInput == 0 and doPrescalesForData:
    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HPlusPrescaleWeightProducer_cfi")
    process.hplusPrescaleWeightProducer.prescaleWeightTriggerResults.setProcessName(dataVersion.getTriggerProcess())
    process.hplusPrescaleWeightProducer.prescaleWeightHltPaths = param.trigger.triggers.value()
    process.commonSequence *= process.hplusPrescaleWeightProducer
    process.signalAnalysis.prescaleSource = cms.untracked.InputTag("hplusPrescaleWeightProducer")

# Print output
#print "\nAnalysis is blind:", process.signalAnalysis.blindAnalysisStatus, "\n"
print "Histogram level:", process.signalAnalysis.histogramAmbientLevel.value()
print "Trigger:", process.signalAnalysis.trigger
print "Trigger scale factor mode:", process.signalAnalysis.triggerEfficiencyScaleFactor.mode.value()
print "Trigger scale factor data:", process.signalAnalysis.triggerEfficiencyScaleFactor.dataSelect.value()
print "Trigger scale factor MC:", process.signalAnalysis.triggerEfficiencyScaleFactor.mcSelect.value()
print "VertexWeight data distribution:",process.signalAnalysis.vertexWeight.dataPUdistribution.value()
print "VertexWeight mc distribution:",process.signalAnalysis.vertexWeight.mcPUdistribution.value()
print "Cut on HLT MET (check histogram Trigger_HLT_MET for minimum value): ", process.signalAnalysis.trigger.hltMetCut.value()
#print "TauSelection algorithm:", process.signalAnalysis.tauSelection.selection.value()
print "TauSelection algorithm:", process.signalAnalysis.tauSelection.selection.value()
print "TauSelection src:", process.signalAnalysis.tauSelection.src.value()
print "TauVetoSelection src:", process.signalAnalysis.vetoTauSelection.tauSelection.src.value()
print "TauSelection isolation:", process.signalAnalysis.tauSelection.isolationDiscriminator.value()
print "TauSelection operating mode:", process.signalAnalysis.tauSelection.operatingMode.value()
print "VetoTauSelection src:", process.signalAnalysis.vetoTauSelection.tauSelection.src.value()
print "Beta cut: ", process.signalAnalysis.jetSelection.betaCutSource.value(), process.signalAnalysis.jetSelection.betaCutDirection.value(), process.signalAnalysis.jetSelection.betaCut.value()
print "electrons: ", process.signalAnalysis.GlobalElectronVeto
print "muons: ", process.signalAnalysis.GlobalMuonVeto
print "jets: ", process.signalAnalysis.jetSelection

# Counter analyzer (in order to produce compatible root file with the
# python approach)

process.signalAnalysis.eventCounter.printMainCounter = cms.untracked.bool(True)
#process.signalAnalysis.eventCounter.printSubCounters = cms.untracked.bool(True)

if len(additionalCounters) > 0:
    process.signalAnalysis.eventCounter.counters = cms.untracked.VInputTag([cms.InputTag(c) for c in additionalCounters])

# PickEvent module and the main Path. The picked events are only the
# ones selected by the golden analysis defined above.
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.PickEventsDumper_cfi")
if not doOptimisation:
    process.signalAnalysisPath = cms.Path(
        process.commonSequence * # supposed to be empty, unless "doPat=1" command line argument is given
        process.signalAnalysis *
        process.PickEvents
    )

if doMETResolution:
    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.METResolutionAnalysis_cfi")
    process.signalAnalysisPath += process.metResolutionAnalysis

# Optimisation
variationModuleNames = []
if doOptimisation:
    # Make variation modules
    variationModuleNames.extend(myOptimisation.generateVariations(process,additionalCounters,process.commonSequence,process.signalAnalysis,"signalAnalysis"))


# Summer PAS cuts
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addAnalysis
if doSummerPAS:
    module = process.signalAnalysis.clone()
    module.tauSelection.rtauCut = 0
    module.MET.METCut = 70
    module.jetSelection.EMfractionCut = 999 # disable
    addAnalysis(process, "signalAnalysisRtau0MET70", module,
                preSequence=process.commonSequence,
                additionalCounters=additionalCounters,
                signalAnalysisCounters=True)

if doAgainstElectronScan:
    myTauIsolation = "byMediumCombinedIsolationDeltaBetaCorr"
    moduleL = process.signalAnalysis.clone()
    moduleL.tauSelection.isolationDiscriminator = myTauIsolation
    moduleL.tauSelection.againstElectronDiscriminator = "againstElectronLoose"
    addAnalysis(process, "signalAnalysisAgainstElectronLoose", moduleL,
                preSequence=process.commonSequence,
                additionalCounters=additionalCounters,
                signalAnalysisCounters=True)
    moduleM = process.signalAnalysis.clone()
    moduleM.tauSelection.isolationDiscriminator = myTauIsolation
    moduleM.tauSelection.againstElectronDiscriminator = "againstElectronMedium"
    addAnalysis(process, "signalAnalysisAgainstElectronMedium", moduleM,
                preSequence=process.commonSequence,
                additionalCounters=additionalCounters,
                signalAnalysisCounters=True)
    moduleT = process.signalAnalysis.clone()
    moduleT.tauSelection.isolationDiscriminator = myTauIsolation
    moduleT.tauSelection.againstElectronDiscriminator = "againstElectronTight"
    addAnalysis(process, "signalAnalysisAgainstElectronTight", moduleT,
                preSequence=process.commonSequence,
                additionalCounters=additionalCounters,
                signalAnalysisCounters=True)
    moduleMVA = process.signalAnalysis.clone()
    moduleMVA.tauSelection.isolationDiscriminator = myTauIsolation
    moduleMVA.tauSelection.againstElectronDiscriminator = "againstElectronMVA"
    addAnalysis(process, "signalAnalysisAgainstElectronMVA", moduleMVA,
                preSequence=process.commonSequence,
                additionalCounters=additionalCounters,
                signalAnalysisCounters=True)

# b tagging testing
if doBTagScan:
    module = process.signalAnalysis.clone()
#    module.bTagging.discriminator = "trackCountingHighPurBJetTags"
    module.bTagging.discriminatorCut = 2.0
    module.Tree.fill = False
    addAnalysis(process, "signalAnalysisBtaggingTest", module,
                preSequence=process.commonSequence,
                additionalCounters=additionalCounters,
                signalAnalysisCounters=True)

    from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addAnalysis
    module = module.clone()
#    module.bTagging.discriminator = "trackCountingHighPurBJetTags"
    module.bTagging.discriminatorCut = 3.3
    addAnalysis(process, "signalAnalysisBtaggingTest2", module,
                preSequence=process.commonSequence,
                additionalCounters=additionalCounters,
                signalAnalysisCounters=True)

# Rtau testing
if doRtauScan:
    prototype = process.signalAnalysis.clone()
    prototype.Tree.fill = False
    for val in [0.0, 0.7, 0.8]:
        module = prototype.clone()
        module.tauSelection.rtauCut = val
        addAnalysis(process, "signalAnalysisRtau%d"%int(val*100), module,
                    preSequence=process.commonSequence,
                    additionalCounters=additionalCounters,
                    signalAnalysisCounters=True)

# Without Rtau cut (check that Rtau0 case is not covered by doRtauScan
if doRtau0 and not hasattr(process, "signalAnalysisRtau0"):
    module = process.signalAnalysis.clone()
    module.tauSelection.rtauCut = 0
    addAnalysis(process, "signalAnalysisRtau0", module,
                preSequence=process.commonSequence,
                additionalCounters=additionalCounters,
                signalAnalysisCounters=True)

def getSignalAnalysisModuleNames():
    modules = []
    if not doOptimisation:
        modules.append("signalAnalysis")
    if doSummerPAS:
        modules.append("signalAnalysisRtau0MET70")
    if doRtau0:
        modules.append("signalAnalysisRtau0")
    if doOptimisation:
        modules.extend(variationModuleNames)
    return modules

# To have tau embedding like preselection
if doTauEmbeddingLikePreselection:
    # Preselection similar to tau embedding selection (genuine tau+3 jets+lepton vetoes), no tau+MET trigger required
    process.tauEmbeddingLikeSequence = cms.Sequence(process.commonSequence)
    module = process.signalAnalysis.clone()
    counters = additionalCounters[:]
    counters.extend(tauEmbeddingCustomisations.addEmbeddingLikePreselection(process, process.tauEmbeddingLikeSequence, module))
    addAnalysis(process, "signalAnalysisTauEmbeddingLikePreselection", module,
                preSequence=process.tauEmbeddingLikeSequence,
                additionalCounters=counters, signalAnalysisCounters=True)

    # Preselection similar to tau embedding selection (genuine tau+3 jets+lepton vetoes), tau+MET trigger required
    process.tauEmbeddingLikeTriggeredSequence = cms.Sequence(process.commonSequence)
    module = process.signalAnalysis.clone()
    counters = additionalCounters[:]
    counters.extend(tauEmbeddingCustomisations.addEmbeddingLikePreselection(process, process.tauEmbeddingLikeTriggeredSequence, module, prefix="embeddingLikeTriggeredPreselection", disableTrigger=False))
    addAnalysis(process, "signalAnalysisTauEmbeddingLikeTriggeredPreselection", module,
                preSequence=process.tauEmbeddingLikeTriggeredSequence,
                additionalCounters=counters, signalAnalysisCounters=True)    

    process.genuineTauSequence = cms.Sequence(process.commonSequence)
    module = process.signalAnalysis.clone()
    counters = additionalCounters[:]
    counters.extend(tauEmbeddingCustomisations.addGenuineTauPreselection(process, process.genuineTauSequence, module))
    addAnalysis(process, "signalAnalysisGenuineTauPreselection", module,
                preSequence=process.genuineTauSequence,
                additionalCounters=counters, signalAnalysisCounters=True)

    for name in getSignalAnalysisModuleNames():
        module = getattr(process, name).clone()
        module.onlyGenuineTaus = cms.untracked.bool(True)
        addAnalysis(process, name+"GenuineTau", module,
                    preSequence=process.commonSequence,
                    additionalCounters=additionalCounters, signalAnalysisCounters=True)

# With tau embedding input
if options.tauEmbeddingInput:
    prototypes = ["signalAnalysis"]
    if doSummerPAS:
        prototypes.append("signalAnalysisRtau0MET70")
    if doRtau0:
        prototypes.append("signalAnalysisRtau0")

    for name in prototypes:
        module = getattr(process, name).clone()
#        module.Tree.fill = False
        module.trigger.caloMetSelection.metEmulationCut = 60.0
        addAnalysis(process, name+"CaloMet60", module,
                    preSequence=process.commonSequence,
                    additionalCounters=additionalCounters,
                    signalAnalysisCounters=True)

        module = module.clone()
        module.triggerEfficiencyScaleFactor.mode = "efficiency"
        addAnalysis(process, name+"CaloMet60TEff", module,
                    preSequence=process.commonSequence,
                    additionalCounters=additionalCounters,
                    signalAnalysisCounters=True)

################################################################################
# The signal analysis with jet energy scale variation
#
# If the flag is true, create two paths for the variation in plus and
# minus, and clone the signal analysis and counter modules to the
# paths. The tau, jet and MET collections to adjust are taken from the
# configuration of the golden analysis. The fragment below creates the
# following histogram directories
# signalAnalysisJESPlus05
# signalAnalysisJESMinus05
from HiggsAnalysis.HeavyChHiggsToTauNu.JetEnergyScaleVariation import addJESVariationAnalysis
def addJESVariation(name, doJetUnclusteredVariation):
    jetVariationMode="all"
    module = getattr(process, name)

    module = module.clone()
    module.Tree.fill = False        
    module.Tree.fillJetEnergyFractions = False # JES variation will make the fractions invalid

    addJESVariationAnalysis(process, dataVersion, name, "TESPlus",  module, additionalCounters, tauVariationSigma=1.0, postfix=PF2PATVersion)
    addJESVariationAnalysis(process, dataVersion, name, "TESMinus", module, additionalCounters, tauVariationSigma=-1.0, postfix=PF2PATVersion)

    if doJetUnclusteredVariation:
        # Do all variations beyond TES
        addJESVariationAnalysis(process, dataVersion, name, "JESPlus",  module, additionalCounters, jetVariationSigma=1.0, postfix=PF2PATVersion)
        addJESVariationAnalysis(process, dataVersion, name, "JESMinus", module, additionalCounters, jetVariationSigma=-1.0, postfix=PF2PATVersion)
        #addJESVariationAnalysis(process, dataVersion, name, "JERPlus",  module, additionalCounters, VariationSigma=1.0, postfix=PF2PATVersion)
        #addJESVariationAnalysis(process, dataVersion, name, "JERMinus", module, additionalCounters, VariationSigma=-1.0, postfix=PF2PATVersion)
        addJESVariationAnalysis(process, dataVersion, name, "METPlus",  module, additionalCounters, unclusteredVariationSigma=1.0, postfix=PF2PATVersion)
        addJESVariationAnalysis(process, dataVersion, name, "METMinus", module, additionalCounters, unclusteredVariationSigma=-1.0, postfix=PF2PATVersion)

if doJESVariation or doSystematics:
    doJetUnclusteredVariation = True

    modules = getSignalAnalysisModuleNames()
    if doTauEmbeddingLikePreselection:
        if options.tauEmbeddingInput != 0:
            raise Exception("tauEmbegginInput clashes with doTauEmbeddingLikePreselection")
        modules.extend([n+"GenuineTau" for n in modules])

    if options.tauEmbeddingInput != 0:
        modules = [n+"CaloMet60TEff" for n in modules]
        if dataVersion.isData():
            doJetUnclusteredVariation = False

    # JES variation is relevant for MC, and for tau in embedding
    if dataVersion.isMC() or options.tauEmbeddingInput != 0:
        for name in modules:
            addJESVariation(name, doJetUnclusteredVariation)
    else:
        print "JES variation disabled for data (not meaningful for data)"
    print "Added JES variation for %d modules"%len(modules)

def addPUWeightVariation(name):
    # Up variation
    module = getattr(process, name).clone()
    module.Tree.fill = False
    param.setPileupWeight(dataVersion, process, process.commonSequence, pset=module.vertexWeight, psetReader=module.vertexWeightReader, era=puweight, suffix="up")
    addAnalysis(process, name+"PUWeightPlus", module,
                preSequence=process.commonSequence,
                additionalCounters=additionalCounters,
                signalAnalysisCounters=True)
    # Down variation
    module = module.clone()
    param.setPileupWeight(dataVersion, process, process.commonSequence, pset=module.vertexWeight, psetReader=module.vertexWeightReader, era=puweight, suffix="down")
    addAnalysis(process, name+"PUWeightMinus", module,
                preSequence=process.commonSequence,
                additionalCounters=additionalCounters,
                signalAnalysisCounters=True)

if doPUWeightVariation or doSystematics:
    modules = getSignalAnalysisModuleNames()
    if doTauEmbeddingLikePreselection:
        if options.tauEmbeddingInput != 0:
            raise Exception("tauEmbegginInput clashes with doTauEmbeddingLikePreselection")
        modules.extend([n+"GenuineTau" for n in modules])

    if options.tauEmbeddingInput != 0:
        modules = [n+"CaloMet60TEff" for n in modules]

    # PU weight variation is relevant for MC only
    if dataVersion.isMC():
        for name in modules:
            addPUWeightVariation(name)
    else:
        print "PU weight variation disabled for data (not meaningful for data)"
    print "Added PU weight variation for %d modules"%len(modules)
    


# Signal analysis with various tightened muon selections for tau embedding
if options.tauEmbeddingInput != 0 and doTauEmbeddingMuonSelectionScan:
    tauEmbeddingCustomisations.addMuonIsolationAnalyses(process, "signalAnalysis", process.signalAnalysis, process.commonSequence, additionalCounters)

if doTauEmbeddingTauSelectionScan:
    tauEmbeddingCustomisations.addTauAnalyses(process, "signalAnalysis", process.signalAnalysis, process.commonSequence, additionalCounters)

# Print tau discriminators from one tau from one event. Note that if
# the path below is commented, the discriminators are not printed.
process.tauDiscriminatorPrint = cms.EDAnalyzer("HPlusTauDiscriminatorPrintAnalyzer",
    src = process.signalAnalysis.tauSelection.src
)
#process.tauDiscriminatorPrintPath = cms.Path(
#    process.commonSequence *
#    process.tauDiscriminatorPrint
#)

################################################################################

# Define the output module. Note that it is not run if it is not in
# any Path! Hence it is enough to (un)comment the process.outpath
# below to enable/disable the EDM output.
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('output.root'),
    outputCommands = cms.untracked.vstring(
        "keep *_*_*_HChSignalAnalysis",
        "drop *_*_counterNames_*",
        "drop *_*_counterInstances_*"
#	"drop *",
#	"keep *",
#        "keep edmMergeableCounter_*_*_*"
    )
)

# Uncomment the following line to get also the event output (can be
# useful for debugging purposes)
#process.outpath = cms.EndPath(process.out)

#f = open("configDump.py", "w")
#f.write(process.dumpPython())
#f.close()
