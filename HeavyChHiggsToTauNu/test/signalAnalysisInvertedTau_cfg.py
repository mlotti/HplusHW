
import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

################################################################################
# Configuration

# Select the version of the data (needed only for interactice running,
# overridden automatically from multicrab
dataVersion="42XmcS4"     # Summer11 MC
#dataVersion="42Xdata" # Run2010 Apr21 ReReco, Run2011 May10 ReReco, Run2011 PromptReco


##########
# Flags for additional signal analysis modules
# Perform the signal analysis with all tau ID algorithms in addition
# to the "golden" analysis
doAllTauIds = False

# Perform b tagging scanning
doBTagScan = False

# Perform Rtau scanning
doRtauScan = False

# Make MET resolution histograms
doMETResolution = False


# Perform the signal analysis with the JES variations in addition to
# the "golden" analysis
doJESVariation = False
JESVariation = 0.03
JESEtaVariation = 0.02
JESUnclusteredMETVariation = 0.10

# Perform the signal analysis with the PU weight variations
# https://twiki.cern.ch/twiki/bin/view/CMS/PileupSystematicErrors
doPUWeightVariation = False
PUWeightVariation = 0.6

# With tau embedding input, tighten the muon selection
tauEmbeddingFinalizeMuonSelection = True
# With tau embedding input, do the muon selection scan
doTauEmbeddingMuonSelectionScan = False
# Do tau id scan for tau embedding normalisation (no tau embedding input required)
doTauEmbeddingTauSelectionScan = False

applyTriggerScaleFactor = True

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
process = cms.Process("HChSignalAnalysisInvertedTau")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(20) )

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
    # For testing in lxplus
    # dataVersion.getAnalysisDefaultFileCastor()
    # For testing in jade
    dataVersion.getAnalysisDefaultFileMadhatter()
    #dataVersion.getAnalysisDefaultFileMadhatterDcap()
    )
)

if options.tauEmbeddingInput != 0:
    if  options.doPat == 0:
        raise Exception("In tau embedding input mode, set also doPat=1")

    process.source.fileNames = [
        "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_1_X/SingleMu_160431-163261_May10/SingleMu/Run2011A_May10ReReco_v1_AOD_160431_tauembedding_embedding_v11_8_pt40/ac085343fdb44ba8377c1f709923eacd/embedded_RECO_2_1_Jik.root"
        ]
    process.maxEvents.input = 10

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())
if options.tauEmbeddingInput != 0:
    process.GlobalTag.globaltag = "START42_V13::All"
print "GlobalTag="+process.GlobalTag.globaltag.value()

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

###
# MC Filter
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as tauEmbeddingCustomisations
if filterGenTaus:
    additionalCounters.extend(tauEmbeddingCustomisations.addGeneratorTauFilter(process, process.commonSequence, filterInaccessible=filterGenTausInaccessible))

################################################################################
# The "golden" version of the signal analysis
# Primary vertex selection
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex import addPrimaryVertexSelection
addPrimaryVertexSelection(process, process.commonSequence)

import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
param.overrideTriggerFromOptions(options)
param.trigger.triggerSrc.setProcessName(dataVersion.getTriggerProcess())
# Set tau selection mode to 'standard'
#param.setAllTauSelectionOperatingMode('standard')
param.setAllTauSelectionOperatingMode('tauCandidateSelectionOnly')

# Set tau sources to trigger matched tau collections
#param.setAllTauSelectionSrcSelectedPatTaus()
param.setAllTauSelectionSrcSelectedPatTausTriggerMatched()

# Trigger with scale factors (at the moment hard coded)
if applyTriggerScaleFactor and dataVersion.isMC():
    param.triggerEfficiencyScaleFactor.mode = "scaleFactor"

# Set the data scenario for vertex/pileup weighting
#param.setVertexWeightFor2011() # Reweight by reconstructed vertices
param.setPileupWeightFor2011(dataVersion) # Reweight by true PU distribution 

#param.trigger.selectionType = "disabled"

if options.tauEmbeddingInput != 0:
    tauEmbeddingCustomisations.addMuonIsolationEmbeddingForSignalAnalysisInvertedTau(process, process.commonSequence)
    tauEmbeddingCustomisations.setCaloMetSum(process, process.commonSequence, options, dataVersion)
    tauEmbeddingCustomisations.customiseParamForTauEmbedding(param, options, dataVersion)
    if tauEmbeddingFinalizeMuonSelection:
        applyIsolation = not doTauEmbeddingMuonSelectionScan
        additionalCounters.extend(tauEmbeddingCustomisations.addFinalMuonSelection(process, process.commonSequence, param,
                                                                                   enableIsolation=applyIsolation))

# Signal analysis module for the "golden analysis"
process.signalAnalysis = cms.EDFilter("HPlusSignalAnalysisInvertedTauFilter",
    trigger = param.trigger,
    triggerEfficiencyScaleFactor = param.triggerEfficiencyScaleFactor,
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
    vertexWeight = param.vertexWeight,
    GenParticleAnalysis = param.GenParticleAnalysis,
    Tree = param.tree,
)

# Prescale fetching done automatically for data
if dataVersion.isData() and options.tauEmbeddingInput == 0:
    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HPlusPrescaleWeightProducer_cfi")
    process.hplusPrescaleWeightProducer.prescaleWeightTriggerResults.setProcessName(dataVersion.getTriggerProcess())
    process.hplusPrescaleWeightProducer.prescaleWeightHltPaths = param.trigger.triggers.value()
    process.commonSequence *= process.hplusPrescaleWeightProducer
    process.signalAnalysis.prescaleSource = cms.untracked.InputTag("hplusPrescaleWeightProducer")

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

if doMETResolution:
    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.METResolutionAnalysis_cfi")
    process.signalAnalysisPath += process.metResolutionAnalysis

# b tagging testing
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addAnalysis
if doBTagScan:
    module = process.signalAnalysis.clone()
#    module.bTagging.discriminator = "trackCountingHighPurBJetTags"
    module.bTagging.discriminatorCut = 2.0
    module.Tree.fill = False
    addAnalysis(process, "signalAnalysisBtaggingTest", module,
                preSequence=process.commonSequence,
                additionalCounters=additionalCounters,
                signalAnalysisCounters=True)

    from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addAnalysis
    module = module.clone()
#    module.bTagging.discriminator = "trackCountingHighPurBJetTags"
    module.bTagging.discriminatorCut = 3.3
    addAnalysis(process, "signalAnalysisBtaggingTest2", module,
                preSequence=process.commonSequence,
                additionalCounters=additionalCounters,
                signalAnalysisCounters=True)

# Rtau testing
if doRtauScan:
    prototype = process.signalAnalysis.clone()
    prototype.Tree.fill = False
    for val in [0.0, 0.7, 0.8]:
        module = prototype.clone()
        module.tauSelection.rtauCut = val
        addAnalysis(process, "signalAnalysisRtau%d"%int(val*100), module,
                    preSequence=process.commonSequence,
                    additionalCounters=additionalCounters,
                    signalAnalysisCounters=True)

if options.tauEmbeddingInput:
    module = process.signalAnalysis.clone()
    module.Tree.fill = False
    module.trigger.caloMetSelection.metEmulationCut = 60.0
    addAnalysis(process, "signalAnalysisCaloMet60", module,
                preSequence=process.commonSequence,
                additionalCounters=additionalCounters,
                signalAnalysisCounters=True)

    module = module.clone()
    module.trigger.selectionType = "byParametrisation"
    addAnalysis(process, "signalAnalysisCaloMet60TEff", module,
                preSequence=process.commonSequence,
                additionalCounters=additionalCounters,
                signalAnalysisCounters=True)


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
# signalAnalysisTauSelectionHPSTightTauBased
# signalAnalysisTauSelectionCombinedHPSTaNCBased
#
# The corresponding Counter directories have "Counters" postfix, and
# cms.Paths "Path" postfix. The paths are run independently of each
# other. It is important to give the process.commonSequence for the
# function, so that it will be run before the analysis module in the
# Path. Then, in case PAT is run on the fly, the framework runs the
# analysis module after PAT (and runs PAT only once).
if doAllTauIds:
    module = process.signalAnalysis()
    module.Tree.fill = False
    param.addTauIdAnalyses(process, "signalAnalysis", module, process.commonSequence, additionalCounters)

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
    # Exceptions for tau embedding
    jetVariationMode="all"
    name = "signalAnalysis"
    module = process.signalAnalysis
    if options.tauEmbeddingInput != 0:
        JESUnclusteredMETVariation=0
        jetVariationMode="onlyTauMatching"
        name = "signalAnalysisCaloMet60TEff"
        module = process.signalAnalysisCaloMet60TEff
    module = module.clone()
    module.Tree.fill = False        

    JESs = "%02d" % int(JESVariation*100)
    JESe = "%02d" % int(JESEtaVariation*100)
    JESm = "%02d" % int(JESUnclusteredMETVariation*100)
    addJESVariationAnalysis(process, name, "JESPlus"+JESs+"eta"+JESe+"METPlus"+JESm,   module, additionalCounters, JESVariation, JESEtaVariation, JESUnclusteredMETVariation, jetVariationMode)
    addJESVariationAnalysis(process, name, "JESMinus"+JESs+"eta"+JESe+"METPlus"+JESm,  module, additionalCounters, -JESVariation, JESEtaVariation, JESUnclusteredMETVariation, jetVariationMode)
    addJESVariationAnalysis(process, name, "JESPlus"+JESs+"eta"+JESe+"METMinus"+JESm,  module, additionalCounters, JESVariation, JESEtaVariation, -JESUnclusteredMETVariation, jetVariationMode)
    addJESVariationAnalysis(process, name, "JESMinus"+JESs+"eta"+JESe+"METMinus"+JESm, module, additionalCounters, -JESVariation, JESEtaVariation, -JESUnclusteredMETVariation, jetVariationMode)

if doPUWeightVariation:
    module = process.signalAnalysis.clone()
    module.vertexWeight.shiftMean = True
    module.vertexWeight.shiftMeanAmount = PUWeightVariation
    addAnalysis(process, "signalAnalysisPUWeightPlus", module,
                preSequence=process.commonSequence,
                additionalCounters=additionalCounters,
                signalAnalysisCounters=True)

    module = module.clone()
    module.vertexWeight.shiftMeanAmount = -PUWeightVariation
    addAnalysis(process, "signalAnalysisPUWeightMinus", module,
                preSequence=process.commonSequence,
                additionalCounters=additionalCounters,
                signalAnalysisCounters=True)


# Signal analysis with various tightened muon selections for tau embedding
if options.tauEmbeddingInput != 0 and doTauEmbeddingMuonSelectionScan:
    tauEmbeddingCustomisations.addMuonIsolationAnalyses(process, "signalAnalysis", process.signalAnalysis, process.commonSequence, additionalCounters)

if doTauEmbeddingTauSelectionScan:
    tauEmbeddingCustomisations.addTauAnalyses(process, "signalAnalysis", process.signalAnalysis, process.commonSequence, additionalCounters)

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
        "keep *_*_*_HChSignalAnalysisInvertedTau",
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

