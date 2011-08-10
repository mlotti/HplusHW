import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

# Run this file on top of the PickEvents AOD files

################################################################################
# Configuration

# Select the version of the data (needed only for interactice running,
# overridden automatically from multicrab
#dataVersion="42Xmc"     # Summer11 MC
dataVersion="42Xdata" # Run2010 Apr21 ReReco, Run2011 May10 ReReco, Run2011 PromptReco


################################################################################

# Command line arguments (options) and DataVersion object
options, dataVersion = getOptionsDataVersion(dataVersion)

# Always run PAT on the fly when running on PickEvents AOD file
options.doPat=1
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
options.trigger = param.singleTauMetTriggerPaths

################################################################################
# Define the process
process = cms.Process("HChSignalAnalysis")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(20) )

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
    "file:pickevents_Tau_Run2011A-May10ReReco-v1_AOD.root",
#    "file:pickevents_Tau_Run2011A-PromptReco-v4_AOD.root",
    )
)

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())
print "GlobalTag="+dataVersion.getGlobalTag()

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")

# Fragment to run PAT on the fly if requested from command line

# Remove the event pre-selection because the input files contain run
# regions with different triggers, and it's easier to just disable the
# triggering here.
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPatOnTheFly
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion)
process.commonSequence.remove(process.eventPreSelection)

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

# Set the triggers for trigger efficiency parametrisation
#param.trigger.triggerTauSelection = param.tauSelectionHPSVeryLooseTauBased.clone( # VeryLoose
param.trigger.triggerTauSelection = param.tauSelectionHPSTightTauBased.clone( # Tight
  rtauCut = cms.untracked.double(0.0) # No rtau cut for trigger tau
)
param.trigger.triggerMETSelection = param.MET.clone(
  METCut = cms.untracked.double(0.0) # No MET cut for trigger MET
)

# Set the data scenario for vertex/pileup weighting
#param.setVertexWeightFor2011() # Reweight by reconstructed vertices
param.setPileupWeightFor2011(dataVersion) # Reweight by true PU distribution 

#param.trigger.selectionType = "disabled"

   
# Signal analysis module for the "golden analysis"
process.signalAnalysis = cms.EDFilter("HPlusSignalAnalysisProducer",
    trigger = param.trigger,
    primaryVertexSelection = param.primaryVertexSelection,
    GlobalElectronVeto = param.GlobalElectronVeto,
    GlobalMuonVeto = param.GlobalMuonVeto,
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
    TriggerEmulationEfficiency = param.TriggerEmulationEfficiency,
    vertexWeight = param.vertexWeight,
    tauEmbedding = param.TauEmbeddingAnalysis,
    GenParticleAnalysis = param.GenParticleAnalysis
)

# Prescale fetching done automatically for data
if dataVersion.isData():
    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HPlusPrescaleWeightProducer_cfi")
    process.hplusPrescaleWeightProducer.prescaleWeightTriggerResults.setProcessName(dataVersion.getTriggerProcess())
    process.hplusPrescaleWeightProducer.prescaleWeightHltPaths = param.trigger.triggers.value()
    process.commonSequence *= process.hplusPrescaleWeightProducer
    process.signalAnalysis.prescaleSource = cms.untracked.InputTag("hplusPrescaleWeightProducer")

# Print output
print "Trigger:", process.signalAnalysis.trigger
print "VertexWeight:",process.signalAnalysis.vertexWeight
print "Cut on HLT MET (check histogram Trigger_HLT_MET for minimum value): ", process.signalAnalysis.trigger.hltMetCut
print "Trigger efficiencies by: ", ", ".join([param.formatEfficiencyTrigger(x) for x in process.signalAnalysis.trigger.triggerEfficiency.selectTriggers])
#print "TauSelection algorithm:", process.signalAnalysis.tauSelection.selection
print "TauSelection algorithm:", process.signalAnalysis.tauSelection.selection
print "TauSelection src:", process.signalAnalysis.tauSelection.src
print "TauSelection operating mode:", process.signalAnalysis.tauSelection.operatingMode

# PickEvent module and the main Path. The picked events are only the
# ones selected by the golden analysis defined above.
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.PickEventsDumper_cfi")
process.signalAnalysisPath = cms.Path(
    process.commonSequence * # supposed to be empty, unless "doPat=1" command line argument is given
    process.signalAnalysis
)

################################################################################

# Define the output module. Note that it is not run if it is not in
# any Path! Hence it is enough to (un)comment the process.outpath
# below to enable/disable the EDM output.
process.out = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring("signalAnalysisPath")
    ),
    fileName = cms.untracked.string('events.root'),
    outputCommands = cms.untracked.vstring(
        "keep *",
        "drop *_*_counterNames_*",
        "drop *_*_counterInstances_*"
#	"drop *",
#	"keep *",
#        "keep edmMergeableCounter_*_*_*"
    )
)

process.outpath = cms.EndPath(process.out)

