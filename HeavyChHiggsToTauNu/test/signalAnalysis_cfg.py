import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataVersion import DataVersion

################################################################################
# Configuration

# Select the version of the data
#dataVersion = "35X"
#dataVersion = "35Xredigi"
#dataVersion = "36X"
#dataVersion = "36Xspring10"
#dataVersion = "37X"
<<<<<<< HEAD
#dataVersion = "38Xrelval"
dataVersion = "39X"
#dataVersion = "data" # this is for collision data 
=======
#dataVersion = "38X"
dataVersion = "39Xredigi"

##########
# Flags for additional signal analysis modules

# Perform the signal analysis with all tau ID algorithms in addition
# to the "golden" analysis
doAllTauIds = True

# Perform the signal analysis with the JES variations in addition to
# the "golden" analysis
doJESVariation = False

################################################################################
# Common configuration, command line arguments, input file, number of
# events, possible PAT-on-the-fly, configuration histograms
>>>>>>> matti/cmssw397

options = getOptions()
if options.dataVersion != "":
    dataVersion = options.dataVersion

print "Assuming data is ", dataVersion
dataVersion = DataVersion(dataVersion) # convert string to object

process = cms.Process("HChSignalAnalysis")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(20) )

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
	#"rfio:/castor/cern.ch/user/s/slehti/HiggsAnalysisData/pattuple_2_1_GhW_TTToHpmToTauNu_M-100_7TeV-pythia6-tauola_Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v6.root"
	#"rfio:/castor/cern.ch/user/s/slehti/HiggsAnalysisData/pattuple_1_1_AcP_TTToHplusBWB_M-100_7TeV-pythia6-tauola_Fall10_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_1b.root"
        # For testing in lxplus
        dataVersion.getAnalysisDefaultFileCastor()
        # For testing in jade
        #dataVersion.getAnalysisDefaultFileMadhatter()
        #dataVersion.getAnalysisDefaultFileMadhatterDcap()
#        "file:pattuple.root"
    )
)
if options.doPat != 0:
    process.source.fileNames = cms.untracked.vstring(dataVersion.getPatDefaultFileMadhatter())

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())
print "GlobalTag="+dataVersion.getGlobalTag()

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 500

# Uncomment the following in order to print the counters at the end of
# the job (note that if many other modules are being run in the same
# job, their INFO messages are printed too)
#process.MessageLogger.cerr.threshold = cms.untracked.string("INFO")
process.TFileService.fileName = "histograms.root"

# Fragment to run PAT on the fly if requested from command line
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataSelection import addDataSelection, dataSelectionCounters
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import *
process.patSequence = cms.Sequence()
if options.doPat != 0:
    print "Running PAT on the fly"

    # Jet trigger (for cleaning of tau->HLT matching
    jetTrigger = "HLT_Jet30U"
    trigger = options.trigger

    process.collisionDataSelection = cms.Sequence()
    if dataVersion.isData():
        process.collisionDataSelection = addDataSelection(process, dataVersion, trigger)

    print "Trigger used for tau matching: "+trigger
    print "Trigger used for jet matching: "+jetTrigger

    process.patSequence = cms.Sequence(
        process.collisionDataSelection *
        addPat(process, dataVersion, matchingTauTrigger=trigger, matchingJetTrigger=jetTrigger)
    )
additionalCounters = []
if dataVersion.isData():
    additionalCounters = dataSelectionCounters[:]


# Add generator and configuration information to histograms.root
process.genRunInfo = cms.EDAnalyzer("HPlusGenRunInfoAnalyzer",
    src = cms.untracked.InputTag("generator")
)
process.configInfo = cms.EDAnalyzer("HPlusConfigInfoAnalyzer")
if options.crossSection >= 0.:
    process.configInfo.crossSection = cms.untracked.double(options.crossSection)
    print "Dataset cross section has been set to %g pb" % options.crossSection
if options.luminosity >= 0:
    process.configInfo.luminosity = cms.untracked.double(options.luminosity)
    print "Dataset integrated luminosity has been set to %g pb^-1" % options.luminosity
process.infoPath = cms.Path(
    process.genRunInfo +
    process.configInfo
)

<<<<<<< HEAD
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param

# Matching of pat::Taus to HLT taus - FIXME: done already in pattuples
#from HiggsAnalysis.HeavyChHiggsToTauNu.HChTriggerMatching import addTauTriggerMatching
#process.triggerMatching = addTauTriggerMatching(process, param.trigger.triggers[:], "Tau")
#process.patSequence *= process.triggerMatching

=======
################################################################################
# The "golden" version of the signal analysis
>>>>>>> matti/cmssw397

import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
# Prescale weight, do not uncomment unless you know what you're doing!
#process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HPlusPrescaleWeightProducer_cfi")
#process.hplusPrescaleWeightProducer.prescaleWeightTriggerResults.setProcessName(dataVersion.getTriggerProcess())
#process.hplusPrescaleWeightProducer.prescaleWeightHltPaths = param.trigger.triggers.value()
#process.patSequence *= process.hplusPrescaleWeightProducer


# Signal analysis module for the "golden analysis"
process.signalAnalysis = cms.EDFilter("HPlusSignalAnalysisProducer",
#    prescaleSource = cms.untracked.InputTag("hplusPrescaleWeightProducer"),
    trigger = param.trigger,
####    TriggerTauMETEmulation = param.TriggerTauMETEmulation,
    GlobalElectronVeto = param.GlobalElectronVeto,
    GlobalMuonVeto = param.GlobalMuonVeto,
    tauSelection = param.tauSelection,
    useFactorizedTauID = param.useFactorizedTauID,
    jetSelection = param.jetSelection,
    MET = param.MET,
    bTagging = param.bTagging,
    fakeMETVeto = param.fakeMETVeto,
    transverseMassCut = param.transverseMassCut,
    EvtTopology = param.EvtTopology,
    TriggerEmulationEfficiency = param.TriggerEmulationEfficiency
)

print "Trigger:", process.signalAnalysis.trigger
print "Cut on HLT MET: ", process.signalAnalysis.trigger.hltMetCut
print "TauSelection algorithm:", process.signalAnalysis.tauSelection.selection
print "TauSelection src:", process.signalAnalysis.tauSelection.src
print "TauSelection factorization used:", process.signalAnalysis.useFactorizedTauID
print "TauSelection factorization source:", process.signalAnalysis.tauSelection.factorization.factorizationTables.factorizationSourceName

# Counter analyzer (in order to produce compatible root file with the
# python approach)
process.signalAnalysisCounters = cms.EDAnalyzer("HPlusEventCountAnalyzer",
    counterNames = cms.untracked.InputTag("signalAnalysis", "counterNames"),
    counterInstances = cms.untracked.InputTag("signalAnalysis", "counterInstances"),
    printMainCounter = cms.untracked.bool(True),
    printSubCounters = cms.untracked.bool(False),
    printAvailableCounters = cms.untracked.bool(False),
)
if len(additionalCounters) > 0:
    process.signalAnalysisCounters.counters = cms.untracked.VInputTag([cms.InputTag(c) for c in additionalCounters])

# PickEvent module and the main Path. The picked events are only the
# ones selected by the golden analysis defined above.
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.PickEventsDumper_cfi")
process.signalAnalysisPath = cms.Path(
    process.patSequence * # supposed to be empty, unless "doPat=1" command line argument is given
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
# some of the I/O and grid overhead). The fragmen below creates the
# following histogram directories
# signalAnalysisTauSelectionShrinkingConeCutBased
# signalAnalysisTauSelectionShrinkingConeTaNCBased
# signalAnalysisTauSelectionCaloTauCutBased
# signalAnalysisTauSelectionHPSTauBased
#
# The corresponding Counter directories have "Counters" postfix, and
# cms.Paths "Path" postfix. The paths are run independently of each
# other. It is important to give the process.patSequence for the
# function, so that it will be run before the analysis module in the
# Path. Then, in case PAT is run on the fly, the framework runs the
# analysis module after PAT (and runs PAT only once).
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addAnalysisArray
<<<<<<< HEAD
addAnalysisArray(process, "signalAnalysis", process.signalAnalysis, setTauSelection,
		 [param.tauSelectionShrinkingConeCutBased,
		  param.tauSelectionShrinkingConeTaNCBased,
		  param.tauSelectionCaloTauCutBased,
		  param.tauSelectionHPSTauBased,
                  param.tauSelectionCombinedHPSTaNCTauBased],
		 names = ["TauSelectionShrinkingConeCutBased",
		  "TauSelectionShrinkingConeTaNCBased",
		  "TauSelectionCaloTauCutBased",
		  "TauSelectionHPSTauBased",
                  "TauSelectionCombinedHPSTaNCBased"],
                 preSequence = process.patSequence,
                 additionalCounters = additionalCounters)


# Print tau discriminators from one tau from one event
=======
def setTauSelection(module, val):
    module.tauSelection = val
if doAllTauIds:
    addAnalysisArray(process, "signalAnalysis", process.signalAnalysis, setTauSelection,
        values = [param.tauSelectionShrinkingConeCutBased,
                  param.tauSelectionShrinkingConeTaNCBased,
                  param.tauSelectionCaloTauCutBased,
                  param.tauSelectionHPSTauBased],
        names = ["TauSelectionShrinkingConeCutBased",
                 "TauSelectionShrinkingConeTaNCBased",
                 "TauSelectionCaloTauCutBased",
                 "TauSelectionHPSTauBased"],
        preSequence = process.patSequence,
        additionalCounters = additionalCounters)
    
################################################################################
# The signal analysis with jet energy scale variation
#
# If the flag is true, create two paths for the variation in plus and
# minus, and clone the signal analysis and counter modules to the
# paths. The tau, jet and MET collections to adjust are taken from the
# configuration of the golden analysis. 

from HiggsAnalysis.HeavyChHiggsToTauNu.JetEnergyScaleVariation_cfi import jesVariation
def addJESVariation(process, name, variation):
    variationName = name
    analysisName = "signalAnalysis"+name
    countersName = analysisName+"Counters"
    pathName = analysisName+"Path"

    # Construct the JES variation module
    variation = jesVariation.clone(
        tauSrc = cms.InputTag(process.signalAnalysis.tauSelection.src.value()), # from untracked to tracked
        jetSrc = cms.InputTag(process.signalAnalysis.jetSelection.src.value()),
        metSrc = cms.InputTag(process.signalAnalysis.MET.src.value()),
        JESVariation = cms.double(variation)
    )
    setattr(process, variationName, variation)

    # Construct the signal analysis module for this variation
    # Use variated taus, jets and MET
    analysis = process.signalAnalysis.clone()
    analysis.tauSelection.src = cms.untracked.InputTag(variationName)
    analysis.jetSelection.src = cms.untracked.InputTag(variationName)
    analysis.MET.src = cms.untracked.InputTag(variationName)
    setattr(process, analysisName, analysis)
    
    # Construct the counters module
    counters = cms.EDAnalyzer("HPlusEventCountAnalyzer",
        counterNames = cms.untracked.InputTag(analysisName, "counterNames"),
        counterInstances = cms.untracked.InputTag(analysisName, "counterInstances")
    )
    if len(additionalCounters) > 0:
        counters.counters = cms.untracked.VInputTag([cms.InputTag(c) for c in additionalCounters])
    setattr(process, countersName, counters)

    # Construct the path
    path = cms.Path(
        process.patSequence *
        variation *
        analysis *
        counters
    )
    setattr(process, pathName, path)

if doJESVariation:
    # In principle here could be more than two JES variation analyses
    addJESVariation(process, "JESPlus05", 0.05)
    addJESVariation(process, "JESMinus05", -0.05)


# Print tau discriminators from one tau from one event. Note that if
# the path below is commented, the discriminators are not printed.
>>>>>>> matti/cmssw397
process.tauDiscriminatorPrint = cms.EDAnalyzer("HPlusTauDiscriminatorPrintAnalyzer",
    src = process.signalAnalysis.tauSelection.src
)
#process.tauDiscriminatorPrintPath = cms.Path(
#    process.patSequence *
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

