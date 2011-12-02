import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

################################################################################
# Configuration

# Select the version of the data (needed only for interactice running,
# overridden automatically from multicrab
#dataVersion="42XmcS4"     # Summer11 MC
dataVersion="42Xdata" # Run2010 Apr21 ReReco, Run2011 May10 ReReco, Run2011 PromptReco

################################################################################

# Command line arguments (options) and DataVersion object
options, dataVersion = getOptionsDataVersion(dataVersion)

if not dataVersion.isData():
    raise Exception("This configuration file supports data only")

# These are needed for running against tau embedding samples, can be
# given also from command line
#options.doPat=1
#options.tauEmbeddingInput=1

################################################################################
# Define the process
process = cms.Process("HChSignalAnalysis")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(20) )

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
    "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_2_X/Tau_161119-161119_May10_Wed/Tau/Run2011A_May10ReReco_v1_AOD_161119_pattuple_v17/377a23a99017553e73fe517f9c607b59/pattuple_1_1_fpl.root"
    )
)

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = "START42_V12::All"
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
# Primary vertex selection
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex import addPrimaryVertexSelection
addPrimaryVertexSelection(process, process.commonSequence)

import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
param.overrideTriggerFromOptions(options)
param.trigger.triggerSrc.setProcessName(dataVersion.getTriggerProcess())
# Set tau selection mode to 'standard'
param.setAllTauSelectionOperatingMode('standard')
#param.setAllTauSelectionOperatingMode('tauCandidateSelectionOnly')

# Set tau sources to trigger matched tau collections
#param.setAllTauSelectionSrcSelectedPatTaus()
param.setAllTauSelectionSrcSelectedPatTausTriggerMatched()

# Set the data scenario for vertex/pileup weighting
puweight = "Run2011A"
if len(options.puWeightEra) > 0:
    puweight = options.puWeightEra
param.setPileupWeightFor2011(dataVersion, era=puweight) # Reweight by true PU distribution 
param.setDataTriggerEfficiency(dataVersion, era=puweight)

# Signal analysis module for the "golden analysis"
process.signalAnalysis = cms.EDFilter("HPlusSignalAnalysisFilter",
    trigger = param.trigger,
    triggerEfficiencyScaleFactor = param.triggerEfficiencyScaleFactor,
    primaryVertexSelection = param.primaryVertexSelection,
    GlobalElectronVeto = param.GlobalElectronVeto,
    GlobalMuonVeto = param.GlobalMuonVeto,
#    GlobalMuonVeto = param.NonIsolatedMuonVeto,
    # Change default tau algorithm here as needed
    tauSelection = param.tauSelectionHPSTightTauBased,
    jetSelection = param.jetSelection,
    MET = param.MET,
    bTagging = param.bTagging,
    fakeMETVeto = param.fakeMETVeto,
    jetTauInvMass = param.jetTauInvMass,
    topSelection = param.topSelection,
    forwardJetVeto = param.forwardJetVeto,
    transverseMassCut = param.transverseMassCut,
    EvtTopology = param.EvtTopology,
    vertexWeight = param.vertexWeight,
    GenParticleAnalysis = param.GenParticleAnalysis,
    Tree = param.tree,
)
process.signalAnalysis.tauSelection.src = "selectedPatTausHpsPFTauTauTriggerMatched"

# Print output
print "Trigger:", process.signalAnalysis.trigger
print "Trigger scale factor mode:", process.signalAnalysis.triggerEfficiencyScaleFactor.mode
print "VertexWeight:",process.signalAnalysis.vertexWeight
print "Cut on HLT MET (check histogram Trigger_HLT_MET for minimum value): ", process.signalAnalysis.trigger.hltMetCut
#print "TauSelection algorithm:", process.signalAnalysis.tauSelection.selection
print "TauSelection algorithm:", process.signalAnalysis.tauSelection.selection
print "TauSelection src:", process.signalAnalysis.tauSelection.src
print "TauSelection operating mode:", process.signalAnalysis.tauSelection.operatingMode

# Counter analyzer (in order to produce compatible root file with the
# python approach)
process.signalAnalysisCounters = cms.EDAnalyzer("HPlusEventCountAnalyzer",
    counterNames = cms.untracked.InputTag("signalAnalysis", "counterNames"),
    counterInstances = cms.untracked.InputTag("signalAnalysis", "counterInstances"),
    printMainCounter = cms.untracked.bool(True),
    printSubCounters = cms.untracked.bool(False), # Default False
    printAvailableCounters = cms.untracked.bool(False),
)
if len(additionalCounters) > 0:
    process.signalAnalysisCounters.counters = cms.untracked.VInputTag([cms.InputTag(c) for c in additionalCounters])

# PickEvent module and the main Path. The picked events are only the
# ones selected by the golden analysis defined above.
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.PickEventsDumper_cfi")
process.signalAnalysisPath = cms.Path(
    process.commonSequence * # supposed to be empty, unless "doPat=1" command line argument is given
    process.signalAnalysis *
    process.signalAnalysisCounters *
    process.PickEvents
)
