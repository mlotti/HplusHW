import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

################################################################################
# Configuration

# Select the version of the data (needed only for interactice running,
# overridden automatically from multicrab
#dataVersion = "39Xredigi" # Winter10 MC
#dataVersion = "39Xdata"   # Run2010 Dec22 ReReco
#dataVersion = "311Xredigi" # Spring11 MC
dataVersion = "41Xdata"   # Run2011 PromptReco


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
options.doPat=1
#options.tauEmbeddingInput=1

################################################################################
# Define the process
process = cms.Process("HChTriggerEfficiency")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
#	"/store/data/Run2011A/Tau/AOD/PromptReco-v1/000/160/445/84CA2525-5750-E011-AEC1-003048D375AA.root"
	"file:/tmp/slehti/84CA2525-5750-E011-AEC1-003048D375AA.root"
    #"file:/afs/cern.ch/user/a/attikis/scratch0/CMSSW_4_1_4/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/pattuple_5_1_g68.root"
    #"file:/media/disk/attikis/PATTuples/3683D553-4C4E-E011-9504-E0CB4E19F9A6.root"
    #"rfio:/castor/cern.ch/user/w/wendland/test_pattuplev9_signalM120.root"
    #"file:/media/disk/attikis/PATTuples/v9_1/test_pattuple_v9_JetMet2010A_86.root"
    #"rfio:/castor/cern.ch/user/w/wendland/test_pattuple_v9_qcd120170.root"
    #"rfio:/castor/cern.ch/user/w/wendland/test_JetData_pattuplev9.root"
    # For testing in lxplus
    #       "file:/tmp/kinnunen/pattuple_9_1_KJi.root"
    # dataVersion.getAnalysisDefaultFileCastor()
    # For testing in jade
    #        dataVersion.getAnalysisDefaultFileMadhatter()
    #dataVersion.getAnalysisDefaultFileMadhatterDcap()
    #      "file:/tmp/kinnunen/pattuple_9_1_KJi.root"
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
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion, plainPatArgs={"doTauHLTMatching":False})


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

param.setTauIDFactorizationMap(options) # Set Tau ID factorization map

# Set tau sources to non-trigger matched tau collections
param.setAllTauSelectionSrcSelectedPatTaus()


# Set the data scenario for trigger efficiencies and vertex weighting
#param.setTriggerVertexFor2010()
param.setTriggerVertexFor2011()

process.load("HiggsAnalysis.TriggerEfficiency.EventFilter_cff")

process.triggerEfficiencyAnalyzer = cms.EDAnalyzer("TriggerEfficiencyAnalyzer", 
    triggerResults      = cms.InputTag("TriggerResults","","HLT"),
    triggerBit		= cms.string("HLT_IsoPFTau35_Trk20_MET45_v4"),
    tauSrc              = param.tauSelection.src,
    metSrc              = param.MET.src
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

