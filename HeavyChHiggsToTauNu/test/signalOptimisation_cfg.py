import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataVersion import DataVersion

#dataVersion = "35X"
#dataVersion = "35Xredigi"
#dataVersion = "36X"
#dataVersion = "36Xspring10"
#dataVersion = "37X"
dataVersion = "38X"
#dataVersion = "data" # this is for collision data 

options = getOptions()
if options.dataVersion != "":
    dataVersion = options.dataVersion

print "Assuming data is ", dataVersion
dataVersion = DataVersion(dataVersion) # convert string to object

process = cms.Process("HChSignalOptimisation")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(200) )

process.source = cms.Source('PoolSource',
    duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
    fileNames = cms.untracked.vstring(
	#"rfio:/castor/cern.ch/user/s/slehti/HiggsAnalysisData/pattuple_2_1_GhW_TTToHpmToTauNu_M-100_7TeV-pythia6-tauola_Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v6.root"
	#"rfio:/castor/cern.ch/user/s/slehti/HiggsAnalysisData/pattuple_1_1_AcP_TTToHplusBWB_M-100_7TeV-pythia6-tauola_Fall10_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_1b.root"
        # For testing in lxplus
        dataVersion.getAnalysisDefaultFileCastor()
        # For testing in jade
        #dataVersion.getAnalysisDefaultFileMadhatter()
        #dataVersion.getAnalysisDefaultFileMadhatterDcap()
  )
)
if options.doPat != 0:
    process.source.fileNames = cms.untracked.vstring(dataVersion.getPatDefaultFileMadhatter())


################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.categories.append("EventCounts")
process.MessageLogger.cerr.FwkReport.reportEvery = 500

# Uncomment the following in order to print the counters at the end of
# the job (note that if many other modules are being run in the same
# job, their INFO messages are printed too)
#process.MessageLogger.cerr.threshold = cms.untracked.string("INFO")
process.TFileService.fileName = "histograms.root"

from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataSelection import addDataSelection, dataSelectionCounters
from HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalTrigger import getSignalTrigger
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import *
process.patSequence = cms.Sequence()
if options.doPat != 0:
    print "Running PAT on the fly"

    process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
    process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())
    print "GlobalTag="+dataVersion.getGlobalTag()

    # Jet trigger (for cleaning of tau->HLT matching
    jetTrigger = "HLT_Jet30U"
    trigger = options.trigger
    if len(trigger) == 0:
        trigger = getSignalTrigger(dataVersion)

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


# Signal optimisations module
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalOptimisationParameters_cff as param
process.signalOptimisation = cms.EDProducer("HPlusSignalOptimisationProducer",
    trigger = param.trigger,
#    TriggerMETEmulation = param.TriggerMETEmulation,
    GlobalElectronVeto = param.GlobalElectronVeto,
    GlobalMuonVeto = param.GlobalMuonVeto,
    tauSelection = param.tauSelection,
    useFactorizedTauID = param.useFactorizedTauID,
    jetSelection = param.jetSelection,
    MET = param.MET,
    bTagging = param.bTagging,
    fakeMETVeto = param.fakeMETVeto,
    transverseMassCut = param.transverseMassCut,
    EvtTopology = param.EvtTopology
)

print "Cut on HLT MET: ", process.signalOptimisation.trigger.hltMetCut
print "TauSelection algorithm:", process.signalOptimisation.tauSelection.selection
print "TauSelection src:", process.signalOptimisation.tauSelection.src
print "TauSelection factorization used:", process.signalOptimisation.useFactorizedTauID

#if dataVersion.isMC() and dataVersion.is38X():
#    process.trigger.trigger = "HLT_SingleIsoTau20_Trk5_MET20"

# Counter analyzer (in order to produce compatible root file with the
# python approach)
process.signalOptimisationCounters = cms.EDAnalyzer("HPlusEventCountAnalyzer",
    counterNames = cms.untracked.InputTag("signalOptimisation", "counterNames"),
    counterInstances = cms.untracked.InputTag("signalOptimisation", "counterInstances"),
    printMainCounter = cms.untracked.bool(True),
    printSubCounters = cms.untracked.bool(False),
    printAvailableCounters = cms.untracked.bool(False),
)
if len(additionalCounters) > 0:
    process.signalOptimisationCounters.counters = cms.untracked.VInputTag([cms.InputTag(c) for c in additionalCounters])

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.PickEventsDumper_cfi")
process.signalOptimisationPath = cms.Path(
    process.patSequence * # supposed to be empty, unless "doPat=1" command line argument is given
    process.signalOptimisation *
    process.signalOptimisationCounters 
#    process.PickEvents
)

# An example how to create an array of analyzers to do the same
# analysis by varying a single parameter. It is significantly more
# efficienct to run many analyzers in single crab job than to run many
# crab jobs with a single analyzer.
#
#
# def setTauPt(m, val):
#     m.tauSelection.ptCut = val
# from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addAnalysisArray
# addAnalysisArray(process, "signalOptimisationTauPt", process.signalOptimisation, setTauPt,
#                  [10, 20, 30, 40, 50])

def setTauSelection(m, val):
    m.tauSelection = val
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addAnalysisArray
addAnalysisArray(process, "signalOptimisation", process.signalOptimisation, setTauSelection,
		 [param.tauSelectionShrinkingConeCutBased,
		  param.tauSelectionShrinkingConeTaNCBased,
		  param.tauSelectionCaloTauCutBased,
		  param.tauSelectionHPSTauBased],
		 names = ["TauSelectionShrinkingConeCutBased",
		  "TauSelectionShrinkingConeTaNCBased",
		  "TauSelectionCaloTauCutBased",
		  "TauSelectionHPSTauBased"],
                 preSequence = process.patSequence,
                 additionalCounters = additionalCounters)


# Print tau discriminators from one tau from one event
process.tauDiscriminatorPrint = cms.EDAnalyzer("HPlusTauDiscriminatorPrintAnalyzer",
    src = process.signalOptimisation.tauSelection.src
)
#process.tauDiscriminatorPrintPath = cms.Path(
#    process.patSequence *
#    process.tauDiscriminatorPrint
#)

################################################################################

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('output.root'),
    outputCommands = cms.untracked.vstring(
        "keep *_*_*_HChSignalOptimisation",
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

