import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

################################################################################
# Configuration

# Select the version of the data (needed only for interactice running,
# overridden automatically from multicrab
dataVersion = "42Xmc"

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

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
    dataVersion.getAnalysisDefaultFileMadhatter()
    )
)

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())
print "GlobalTag="+dataVersion.getGlobalTag()

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")

# Uncomment the following in order to print the counters at the end of
# the job (note that if many other modules are being run in the same
# job, their INFO messages are printed too)
#process.MessageLogger.cerr.threshold = cms.untracked.string("INFO")

# Fragment to run PAT on the fly if requested from command line
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPatOnTheFly

process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion, plainPatArgs={"doTauHLTMatching":False})

# Add configuration information to histograms.root
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addConfigInfo
process.infoPath = addConfigInfo(process, options, dataVersion)

################################################################################
# Pileup weighting
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
process.pileupWeight = cms.EDProducer("HPlusVertexWeightProducer",
    alias = cms.string("pileupWeight"),
)
puweight = "Run2011A"
if len(options.puWeightEra) > 0:
    puweight = options.puWeightEra
param.setPileupWeightFor2011(dataVersion, era=puweight)
insertPSetContentsTo(param.vertexWeight.clone(), process.pileupWeight)
process.commonSequence *= process.pileupWeight

# Start event selection
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
param.overrideTriggerFromOptions(options)
param.setAllTauSelectionOperatingMode('standard')
param.setAllTauSelectionSrcSelectedPatTaus()

# Primary vertex selection
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex import addPrimaryVertexSelection
addPrimaryVertexSelection(process, process.commonSequence)
process.selectedPrimaryVertexFilter = cms.EDFilter("VertexCountFilter",
    src = cms.InputTag("selectedPrimaryVertex"),
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(999)
)
process.commonSequence *= process.selectedPrimaryVertexFilter

ntuple = cms.EDAnalyzer("TriggerEfficiencyAnalyzer", 
    patTriggerEvent     = cms.InputTag("patTriggerEvent"),
)
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import *
addAnalysis(process, "ntuple", ntuple,
            preSequence=process.commonSequence,
            signalAnalysisCounters=False)


# Replace all event counters with the weighted one
eventCounters = []
for label, module in process.producers_().iteritems():
    if module.type_() == "EventCountProducer":
        eventCounters.append(label)
prototype = cms.EDProducer("HPlusEventCountProducer",
    weightSrc = cms.InputTag("pileupWeight")
)
for label in eventCounters:
    process.globalReplace(label, prototype.clone())



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

