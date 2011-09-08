import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

################################################################################
# Configuration

# Select the version of the data (needed only for interactice running,
# overridden automatically from multicrab
dataVersion = "42Xdata"


##########
# Flags for additional signal analysis modules
# Perform the signal analysis with all tau ID algorithms in addition
# to the "golden" analysis
doAllTauIds = True

# Perform b tagging scanning
doBTagScan = False

# Perform the signal analysis with the JES variations in addition to
# the "golden" analysis
doJESVariation = False
JESVariation = 0.03
JESEtaVariation = 0.02
JESUnclusteredMETVariation = 0.10

# With tau embedding input, tighten the muon selection
tauEmbeddingFinalizeMuonSelection = True
# With tau embedding input, do the muon selection scan
doTauEmbeddingMuonSelectionScan = False
# Do tau id scan for tau embedding normalisation (no tau embedding input required)
doTauEmbeddingTauSelectionScan = False

filterGenTaus = False
filterGenTausInaccessible = False

################################################################################

# Command line arguments (options) and DataVersion object
options, dataVersion = getOptionsDataVersion(dataVersion)

# These are needed for running against tau embedding samples, can be
# given also from command line
#options.doPat=1
#options.tauEmbeddingInput=1

################################################################################
# Define the process
process = cms.Process("HChTriggerEfficiency")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
    # dataVersion.getAnalysisDefaultFileCastor()
    #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_2_X/Tau_Control_165970-166164_DCS/Tau/Run2011A_PromptReco_v4_AOD_Control_165970_pattuple_v12_1/4f228cbdccbe253fb8fc10a07a3c6bf1/pattuple_3_1_LBC.root"
    #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_2_X/Tau_Single_167078-167784_Prompt/Tau/Run2011A_PromptReco_v4_AOD_Single_167078_pattuple_v17/5ac48e003cbdad1c6c78ae464438a5c1/pattuple_15_15D_Gdh.root"
    "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_2_X/Tau_Single_167078-167784_Prompt/Tau/Run2011A_PromptReco_v4_AOD_Single_167078_pattuple_v17_1/5ac48e003cbdad1c6c78ae464438a5c1/pattuple_13_1_Fem.root"
    )
)

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())
print "GlobalTag="+dataVersion.getGlobalTag()

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.TFileService.fileName = cms.string("efficiencyTree.root")


# Uncomment the following in order to print the counters at the end of
# the job (note that if many other modules are being run in the same
# job, their INFO messages are printed too)
#process.MessageLogger.cerr.threshold = cms.untracked.string("INFO")

# Fragment to run PAT on the fly if requested from command line
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPatOnTheFly
if options.trigger == "": 
    options.trigger = "HLT_IsoPFTau35_Trk20_v4"
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion, plainPatArgs={"doTauHLTMatching":False})

if options.doPat != 0:
    process.patDefaultSequence.remove(process.patElectrons)
    process.patDefaultSequence.remove(process.selectedPatElectrons)
    process.patDefaultSequence.remove(process.electronMatch)
    process.patDefaultSequence.remove(process.cleanPatElectrons)
    process.patDefaultSequence.remove(process.cleanPatPhotons)
    process.patDefaultSequence.remove(process.cleanPatTaus)
    process.patDefaultSequence.remove(process.cleanPatTausHpsTancPFTau)
    process.patDefaultSequence.remove(process.cleanPatTausHpsPFTau)
    process.patDefaultSequence.remove(process.cleanPatTausShrinkingConePFTau)
    process.patDefaultSequence.remove(process.cleanPatTausCaloRecoTau)
    process.patDefaultSequence.remove(process.cleanPatJets)
    process.patDefaultSequence.remove(process.countPatElectrons)
    process.patDefaultSequence.remove(process.countPatLeptons)


    process.commonSequence.remove(process.collisionDataSelection)
    del process.collisionDataSelection

# Add configuration information to histograms.root
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addConfigInfo
process.infoPath = addConfigInfo(process, options, dataVersion)


################################################################################
# The "golden" version of the signal analysis

# Primary vertex selection
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex import addPrimaryVertexSelection
addPrimaryVertexSelection(process, process.commonSequence)

import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
param.overrideTriggerFromOptions(options)
# Set tau selection mode to 'standard' or 'factorized'
param.setAllTauSelectionOperatingMode('standard')
#param.setAllTauSelectionOperatingMode('factorized')

#param.setTauIDFactorizationMap(options) # Set Tau ID factorization map

# Set tau sources to non-trigger matched tau collections
param.setAllTauSelectionSrcSelectedPatTaus()


# Set the data scenario for trigger efficiencies and vertex weighting
#param.setTriggerVertexFor2010()
#param.setTriggerVertexFor2011()

process.load("HiggsAnalysis.TriggerEfficiency.EventFilter_cff")
process.eventFilter.remove(process.metSelectionFilter)

process.tauSelectionFilter.filter = False
process.eVetoFilter.filter = False
process.muVetoFilter.filter = False
process.jetSelectionFilter.jetSelection.ptCut = 30
process.jetSelectionFilter.filter = False
process.btagSelectionFilter.filter = False
process.btagSelectionFilter.throw = False

triggerBit = {
    "HLT_IsoPFTau35_Trk20_v2": "HLT_IsoPFTau35_Trk20_MET60_v2",
    "HLT_IsoPFTau35_Trk20_v3": "HLT_IsoPFTau35_Trk20_MET60_v3",
    "HLT_IsoPFTau35_Trk20_v4": "HLT_IsoPFTau35_Trk20_MET60_v4"
    }

process.triggerEfficiencyAnalyzer = cms.EDAnalyzer("TriggerEfficiencyAnalyzer", 
    triggerResults      = cms.InputTag("TriggerResults","","HLT"),
#    triggerBit		= cms.string("HLT_IsoPFTau35_Trk20_MET45_v4"),
#    triggerBit		= cms.string("HLT_IsoPFTau35_Trk20_MET60_v2"),
    triggerBit		= cms.string(triggerBit[options.trigger]),
#    tauSrc              = param.tauSelection.src,
    tauSrc              = cms.untracked.InputTag("selectedPatTausHpsPFTauTauTriggerMatched"),
    metSrc              = param.MET.src,
    caloMetSrc          = cms.untracked.InputTag("patMETs"),
    caloMetNoHFSrc      = cms.untracked.InputTag("metNoHF"),
    bools = cms.PSet(
        TauIDPassed = cms.InputTag("tauSelectionFilter"),
        ElectronVetoPassed = cms.InputTag("eVetoFilter"),
        MuonVetoPassed = cms.InputTag("muVetoFilter"),
        JetSelectionPassed = cms.InputTag("jetSelectionFilter"),
        BTaggingPassed = cms.InputTag("btagSelectionFilter"),
    )
)


process.triggerEfficiencyPath = cms.Path(
    process.commonSequence * # supposed to be empty, unless "doPat=1" command line argument is given
    process.eventFilter *
    process.triggerEfficiencyAnalyzer
)



################################################################################

# Define the output module. Note that it is not run if it is not in
# any Path! Hence it is enough to (un)comment the process.outpath
# below to enable/disable the EDM output.
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('output.root'),
    outputCommands = cms.untracked.vstring(
	"keep *_*_*_HChTriggerEfficiency"
#        "keep *_*_*_HChSignalAnalysis",
#        "drop *_*_counterNames_*",
#        "drop *_*_counterInstances_*"
#	"drop *",
#	"keep *",
#        "keep edmMergeableCounter_*_*_*"
    )
)

# Uncomment the following line to get also the event output (can be
# useful for debugging purposes)
#process.outpath = cms.EndPath(process.out)

