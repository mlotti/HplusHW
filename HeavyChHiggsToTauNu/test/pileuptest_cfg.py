import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

################################################################################
# Configuration

# Select the version of the data
dataVersion = "39Xredigi"
#dataVersion = "39Xdata"

##########
# Flags for additional signal analysis modules

# Perform the signal analysis with all tau ID algorithms in addition
# to the "golden" analysis
doAllTauIds = True

# Perform the signal analysis with the JES variations in addition to
# the "golden" analysis
doJESVariation = False
JESVariation = 0.05

################################################################################

# Command line arguments (options) and DataVersion object
options, dataVersion = getOptionsDataVersion(dataVersion)

################################################################################
# Define the process
process = cms.Process("HChPileupTest")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        #"rfio:/castor/cern.ch/user/w/wendland/test_pattuplev9_signalM120.root"
        "rfio:/castor/cern.ch/user/w/wendland/TTToHplusBWB_M-120_7TeV-pythia6-tauola_Winte10_39X_testsample.root"
	#"rfio:/castor/cern.ch/user/w/wendland/test_pattuple_v9_qcd120170.root"
        # For testing in lxplus
#        dataVersion.getAnalysisDefaultFileCastor()
        # For testing in jade
        #dataVersion.getAnalysisDefaultFileMadhatter()
        #dataVersion.getAnalysisDefaultFileMadhatterDcap()
#        "file:pattuple.root"
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
options.doPat = 1
options.trigger="HLT_SingleIsoTau20_Trk15_MET20"
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPatOnTheFly
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion)

# Add configuration information to histograms.root
#from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addConfigInfo
#process.infoPath = addConfigInfo(process, options)


################################################################################
# The "golden" version of the signal analysis

#import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
#param.overrideTriggerFromOptions(options)
# Set tau selection mode to 'standard' or 'factorized'
#param.setAllTauSelectionOperatingMode('standard')
#param.setAllTauSelectionOperatingMode('factorized')

#from HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.signalAnalysis import customiseParamForTauEmbedding
#if options.tauEmbeddingInput != 0:
#    customiseParamForTauEmbedding(param)

# Prescale weight, do not uncomment unless you know what you're doing!
#process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HPlusPrescaleWeightProducer_cfi")
#process.hplusPrescaleWeightProducer.prescaleWeightTriggerResults.setProcessName(dataVersion.getTriggerProcess())
#process.hplusPrescaleWeightProducer.prescaleWeightHltPaths = param.trigger.triggers.value()
#process.commonSequence *= process.hplusPrescaleWeightProducer


# Signal analysis module for the "golden analysis"
process.pileup = cms.EDProducer("HPlusPileupFilter",
    vertexCollectionSrc = cms.InputTag("offlinePrimaryVertices"),
    #patCollectionSrc = cms.InputTag("selectedPatTausShrinkingConePFTau"),
    #patCollectionType = cms.string("patTau")
    patCollectionSrc = cms.InputTag("selectedPatJetsAK5PF"),
    patCollectionType = cms.string("patJet")              
)

process.myAnalysisPath = cms.Path(
    process.commonSequence
    * process.pileup
)

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

