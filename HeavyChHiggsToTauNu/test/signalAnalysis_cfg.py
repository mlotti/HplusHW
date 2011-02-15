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
process = cms.Process("HChSignalAnalysis")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
#       "rfio:/castor/cern.ch/user/w/wendland/test_pattuplev9_signalM120.root"
	"rfio:/castor/cern.ch/user/w/wendland/test_pattuple_v9_qcd120170.root"
        # For testing in lxplus
#       "file:/tmp/kinnunen/pattuple_9_1_KJi.root"
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
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPatOnTheFly
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion)

# Add configuration information to histograms.root
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addConfigInfo
process.infoPath = addConfigInfo(process, options)


################################################################################
# The "golden" version of the signal analysis

import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
# change to non-matched taus
#param.tauSelectionCaloTauCutBased.src = "selectedPatTausCaloRecoTauTau"
#param.tauSelectionShrinkingConeCutBased.src = "selectedPatTausShrinkingConePFTauTau"
#param.tauSelectionShrinkingConeTaNCBased.src = "selectedPatTausShrinkingConePFTauTau"
#param.tauSelectionHPSTauBased.src = "selectedPatTausHpsPFTauTau"
#param.tauSelectionCombinedHPSTaNCTauBased.src = "selectedPatTausHpsTancPFTauTau"

param.overrideTriggerFromOptions(options)
# Set tau selection mode to 'standard' or 'factorized'
param.setAllTauSelectionOperatingMode('standard')
#param.setAllTauSelectionOperatingMode('factorized')

param.setTauIDFactorizationMap(options) # Set Tau ID factorization map

from HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.signalAnalysis import customiseParamForTauEmbedding
if options.tauEmbeddingInput != 0:
    customiseParamForTauEmbedding(param)

# Prescale weight, do not uncomment unless you know what you're doing!
#process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HPlusPrescaleWeightProducer_cfi")
#process.hplusPrescaleWeightProducer.prescaleWeightTriggerResults.setProcessName(dataVersion.getTriggerProcess())
#process.hplusPrescaleWeightProducer.prescaleWeightHltPaths = param.trigger.triggers.value()
#process.commonSequence *= process.hplusPrescaleWeightProducer



# Signal analysis module for the "golden analysis"
process.signalAnalysis = cms.EDFilter("HPlusSignalAnalysisProducer",
#    prescaleSource = cms.untracked.InputTag("hplusPrescaleWeightProducer"),
    trigger = param.trigger,
####    TriggerTauMETEmulation = param.TriggerTauMETEmulation, OBSOLETE?
    GlobalElectronVeto = param.GlobalElectronVeto,
    GlobalMuonVeto = param.GlobalMuonVeto,
    # Change default tau algorithm here as needed         
    tauSelection = param.tauSelectionHPSTauBased,
    jetSelection = param.jetSelection,
    MET = param.MET,
    bTagging = param.bTagging,
    fakeMETVeto = param.fakeMETVeto,
#    forwardJetVeto = param.forwardJetVeto,
    transverseMassCut = param.transverseMassCut,
    EvtTopology = param.EvtTopology,
    TriggerEmulationEfficiency = param.TriggerEmulationEfficiency
)

    #myFactorizationMapName = getTauIDFactorizationMap() 

process.signalAnalysis.MET.METCut = 70.
#process.signalAnalysis.fakeMETVeto.maxDeltaPhi = 5.
process.signalAnalysis.bTagging.discriminatorCut = 2.0



print "Trigger:", process.signalAnalysis.trigger
print "Cut on HLT MET (check histogram Trigger_HLT_MET for minimum value): ", process.signalAnalysis.trigger.hltMetCut
print "TauSelection algorithm:", process.signalAnalysis.tauSelection.selection
print "TauSelection src:", process.signalAnalysis.tauSelection.src
print "TauSelection operating mode:", process.signalAnalysis.tauSelection.operatingMode
print "TauSelection factorization source:", process.signalAnalysis.tauSelection.factorization.factorizationTables.factorizationSourceName

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


################################################################################
# The signal analysis with different tau ID algorithms
#
# Run the analysis for the different tau ID algorithms at the same job
# as the golden analysis. It is significantly more efficiency to run
# many analyses in a single job compared to many jobs (this avoids
# some of the I/O and grid overhead). The fragment below creates the
# following histogram directories
# signalAnalysisTauSelectionShrinkingConeCutBased
# signalAnalysisTauSelectionShrinkingConeTaNCBased
# signalAnalysisTauSelectionCaloTauCutBased
# signalAnalysisTauSelectionHPSTauBased
# signalAnalysisTauSelectionCombinedHPSTaNCBased
#
# The corresponding Counter directories have "Counters" postfix, and
# cms.Paths "Path" postfix. The paths are run independently of each
# other. It is important to give the process.commonSequence for the
# function, so that it will be run before the analysis module in the
# Path. Then, in case PAT is run on the fly, the framework runs the
# analysis module after PAT (and runs PAT only once).
if doAllTauIds:
    param.addTauIdAnalyses(process, "signalAnalysis", process.signalAnalysis, process.commonSequence, additionalCounters)
        
    
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
if doJESVariation:
    # In principle here could be more than two JES variation analyses
    s = "%02d" % int(JESVariation*100)
    addJESVariationAnalysis(process, "signalAnalysis", "JESPlus"+s, process.signalAnalysis, additionalCounters, JESVariation)
    addJESVariationAnalysis(process, "signalAnalysis", "JESMinus"+s, process.signalAnalysis, additionalCounters, -JESVariation)


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

