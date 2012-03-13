import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

################################################################################
# Configuration

# Select the version of the data (needed only for interactice running,
# overridden automatically from multicrab
#dataVersion = "39Xredigi" # Winter10 MC
#dataVersion = "39Xdata"   # Run2010 Dec22 ReReco
dataVersion = "311Xredigi" # Spring11 MC
#dataVersion = "41Xdata"   # Run2011 PromptReco


##########
# Flags for additional signal analysis modules

# Perform the signal analysis with all tau ID algorithms in addition
# to the "golden" analysis
doAllTauIds = False

# Perform the signal analysis with the JES variations in addition to
# the "golden" analysis
doJESVariation = True
JESVariation = 0.03
JESEtaVariation = 0.02
JESUnclusteredMETVariation = 0.10

# Do trigger parametrisation for MC and tau embedding
doTriggerParametrisation = False

################################################################################

# Command line arguments (options) and DataVersion object
options, dataVersion = getOptionsDataVersion(dataVersion)

################################################################################
# Define the process
process = cms.Process("HChEWKFakeTauAnalysis")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        #"file:/home/wendland/data/pattuple_176_1_ikP.root",
        #"file:/home/wendland/data/pattuple_30_1_NKD.root",
        #"file:/home/wendland/data/pattuple_37_1_QMe.root"
        "file:/home/wendland/data/pattuple_427_1_BSA.root"
        # For testing in lxplus
#       "file:/tmp/kinnunen/pattuple_9_1_KJi.root"
#        dataVersion.getAnalysisDefaultFileCastor()
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

# Uncomment the following in order to print the counters at the end of
# the job (note that if many other modules are being run in the same
# job, their INFO messages are printed too)
#process.MessageLogger.cerr.threshold = cms.untracked.string("INFO")

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
# Set tau selection mode to 'standard'
param.setAllTauSelectionOperatingMode('standard')

# Set tau sources to trigger matched tau collections
#param.setAllTauSelectionSrcSelectedPatTaus()

# Set the triggers for trigger efficiency parametrisation
#param.trigger.triggerTauSelection = param.tauSelectionHPSVeryLooseTauBased.clone( # VeryLoose
param.trigger.triggerTauSelection = param.tauSelectionHPSTightTauBased.clone( # Tight
  rtauCut = cms.untracked.double(0.0) # No rtau cut for trigger tau
)
param.trigger.triggerMETSelection = param.MET.clone(
  METCut = cms.untracked.double(0.0) # No MET cut for trigger MET
)
if (doTriggerParametrisation and not dataVersion.isData()):
    # 2010 and 2011 scenarios
    #param.setEfficiencyTriggersFor2010()
    param.setEfficiencyTriggersFor2011()
    # Settings for the configuration
    param.trigger.selectionType = cms.untracked.string("byParametrisation")


# Set the triggers for trigger efficiencies
# one trigger
#param.setEfficiencyTrigger("HLT_SingleIsoTau20_Trk15_MET25_v4")
# many triggers, efficiencies weighted by their luminosities
#param.setEfficiencyTriggers([
#        ("HLT_SingleIsoTau20_Trk15_MET25_v3", 16.084022481),
#        ("HLT_SingleIsoTau20_Trk15_MET25_v4", 2.270373344),
#        ])
# many triggers, efficiencies weighted by their luminosities, triggers
# and luminosities taken from the multicrab dataset definitions
#param.setEfficiencyTriggersFromMulticrabDatasets([
#        "BTau_141956-144114_Dec22",
#        "BTau_146428-148058_Dec22",
#    ])


# Signal analysis module for the "golden analysis"
process.EWKFakeTauAnalysis = cms.EDProducer("HPlusEWKFakeTauAnalysisProducer",
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
    topSelection = param.topSelection,                                      
    forwardJetVeto = param.forwardJetVeto,
    transverseMassCut = param.transverseMassCut,
    EvtTopology = param.EvtTopology,
    TriggerEmulationEfficiency = param.TriggerEmulationEfficiency,
    GenParticleAnalysis = param.GenParticleAnalysis                                     
)

# Prescale fetching done automatically for data
if dataVersion.isData():
    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HPlusPrescaleWeightProducer_cfi")
    process.hplusPrescaleWeightProducer.prescaleWeightTriggerResults.setProcessName(dataVersion.getTriggerProcess())
    process.hplusPrescaleWeightProducer.prescaleWeightHltPaths = param.trigger.triggers.value()
    process.commonSequence *= process.hplusPrescaleWeightProducer
    process.EWKFakeTauAnalysis.prescaleSource = cms.untracked.InputTag("hplusPrescaleWeightProducer")

# Print output
print "Trigger:", process.EWKFakeTauAnalysis.trigger
print "Cut on HLT MET (check histogram Trigger_HLT_MET for minimum value): ", process.EWKFakeTauAnalysis.trigger.hltMetCut
print "Trigger efficiencies by: ", ", ".join([param.formatEfficiencyTrigger(x) for x in process.EWKFakeTauAnalysis.trigger.triggerEfficiency.selectTriggers])
print "TauSelection algorithm:", process.EWKFakeTauAnalysis.tauSelection.selection
print "TauSelection src:", process.EWKFakeTauAnalysis.tauSelection.src
print "TauSelection operating mode:", process.EWKFakeTauAnalysis.tauSelection.operatingMode

# Counter analyzer (in order to produce compatible root file with the
# python approach)
process.EWKFakeTauAnalysisCounters = cms.EDAnalyzer("HPlusEventCountAnalyzer",
    counterNames = cms.untracked.InputTag("EWKFakeTauAnalysis", "counterNames"),
    counterInstances = cms.untracked.InputTag("EWKFakeTauAnalysis", "counterInstances"),
    printMainCounter = cms.untracked.bool(True),
    printSubCounters = cms.untracked.bool(False), # Default False
    printAvailableCounters = cms.untracked.bool(False),
)
if len(additionalCounters) > 0:
    process.EWKFakeTauAnalysisCounters.counters = cms.untracked.VInputTag([cms.InputTag(c) for c in additionalCounters])

# PickEvent module and the main Path. The picked events are only the
# ones selected by the golden analysis defined above.
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.PickEventsDumper_cfi")
process.EWKFakeTauAnalysisPath = cms.Path(
    process.commonSequence * # supposed to be empty, unless "doPat=1" command line argument is given
    process.EWKFakeTauAnalysis *
    process.EWKFakeTauAnalysisCounters *
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
# EWKFakeTauAnalysisTauSelectionShrinkingConeCutBased
# EWKFakeTauAnalysisTauSelectionShrinkingConeTaNCBased
# EWKFakeTauAnalysisTauSelectionCaloTauCutBased
# EWKFakeTauAnalysisTauSelectionHPSTightTauBased
# EWKFakeTauAnalysisTauSelectionCombinedHPSTaNCBased
#
# The corresponding Counter directories have "Counters" postfix, and
# cms.Paths "Path" postfix. The paths are run independently of each
# other. It is important to give the process.commonSequence for the
# function, so that it will be run before the analysis module in the
# Path. Then, in case PAT is run on the fly, the framework runs the
# analysis module after PAT (and runs PAT only once).
if doAllTauIds:
    param.addTauIdAnalyses(process, "EWKFakeTauAnalysis", process.EWKFakeTauAnalysis, process.commonSequence, additionalCounters)

################################################################################
# The signal analysis with jet energy scale variation
#
# If the flag is true, create two paths for the variation in plus and
# minus, and clone the signal analysis and counter modules to the
# paths. The tau, jet and MET collections to adjust are taken from the
# configuration of the golden analysis. The fragment below creates the
# following histogram directories
# EWKFakeTauAnalysisJESPlus05
# EWKFakeTauAnalysisJESMinus05
from HiggsAnalysis.HeavyChHiggsToTauNu.JetEnergyScaleVariation import addJESVariationAnalysis
if doJESVariation:
    # In principle here could be more than two JES variation analyses
    JESs = "%02d" % int(JESVariation*100)
    JESe = "%02d" % int(JESEtaVariation*100)
    JESm = "%02d" % int(JESUnclusteredMETVariation*100)
    addJESVariationAnalysis(process, "EWKFakeTauAnalysis", "JESPlus"+JESs+"eta"+JESe+"METPlus"+JESm, process.EWKFakeTauAnalysis, additionalCounters, JESVariation, JESEtaVariation, JESUnclusteredMETVariation)
    addJESVariationAnalysis(process, "EWKFakeTauAnalysis", "JESMinus"+JESs+"eta"+JESe+"METPlus"+JESm, process.EWKFakeTauAnalysis, additionalCounters, -JESVariation, JESEtaVariation, JESUnclusteredMETVariation)
    addJESVariationAnalysis(process, "EWKFakeTauAnalysis", "JESPlus"+JESs+"eta"+JESe+"METMinus"+JESm, process.EWKFakeTauAnalysis, additionalCounters, JESVariation, JESEtaVariation, -JESUnclusteredMETVariation)
    addJESVariationAnalysis(process, "EWKFakeTauAnalysis", "JESMinus"+JESs+"eta"+JESe+"METMinus"+JESm, process.EWKFakeTauAnalysis, additionalCounters, -JESVariation, JESEtaVariation, -JESUnclusteredMETVariation)

# Print tau discriminators from one tau from one event. Note that if
# the path below is commented, the discriminators are not printed.
process.tauDiscriminatorPrint = cms.EDAnalyzer("HPlusTauDiscriminatorPrintAnalyzer",
    src = process.EWKFakeTauAnalysis.tauSelection.src
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
        "keep *_*_*_HChEWKFakeTauAnalysis",
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

