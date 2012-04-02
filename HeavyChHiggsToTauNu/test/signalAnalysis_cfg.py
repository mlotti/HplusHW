import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

################################################################################
# Configuration

# Select the version of the data (needed only for interactice running,
# overridden automatically from multicrab
dataVersion="44XmcS6"     # Fall11 MC
#dataVersion="44Xdata"    # Run2011 08Nov and 19Nov ReRecos
#dataVersion="42Xdata" # Run2010 Apr21 ReReco, Run2011 May10 ReReco, Run2011 PromptReco


##########
# Flags for additional signal analysis modules
# Perform the signal analysis with all tau ID algorithms in addition
# to the "golden" analysis
doAllTauIds = False

# Apply summer PAS style cuts
doSummerPAS = False

# Perform b tagging scanning
doBTagScan = False

# Perform Rtau scanning
doRtauScan = False

# Make MET resolution histograms
doMETResolution = False

# With tau embedding input, tighten the muon selection
tauEmbeddingFinalizeMuonSelection = True
# With tau embedding input, do the muon selection scan
doTauEmbeddingMuonSelectionScan = False
# Do tau id scan for tau embedding normalisation (no tau embedding input required)
doTauEmbeddingTauSelectionScan = False
# Do embedding-like preselection for signal analysis
doTauEmbeddingLikePreselection = False

#########
# Flags for options in the signal analysis

# Keep / Ignore prescaling for data (suppresses greatly error messages 
# in datasets with or-function of triggers)
doPrescalesForData = False

# Tree filling
doFillTree = False

applyTriggerScaleFactor = True


#PF2PATVersion = "PFlow" # For normal PF2PAT
PF2PATVersion = "PFlowChs" # For PF2PAT with CHS

### Systematic uncertainty flags ###
# Running of systematic variations is controlled by the global flag
# (below), or the individual flags
doSystematics = False

# Perform the signal analysis with the JES variations in addition to
# the "golden" analysis
doJESVariation = True
JESVariation = 0.03
JESEtaVariation = 0.02
JESUnclusteredMETVariation = 0.10

# Perform the signal analysis with the PU weight variations
# https://twiki.cern.ch/twiki/bin/view/CMS/PileupSystematicErrors
doPUWeightVariation = False
PUWeightVariation = 0.6


################################################################################

# Command line arguments (options) and DataVersion object
options, dataVersion = getOptionsDataVersion(dataVersion)

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
        "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_2_X/SingleMu_165088-166150_Prompt/SingleMu/PromptReco_v4_AOD_165088_tauembedding_embedding_v13/9a509078f648b588515c15f2e17e813c/embedded_19_1_YAU.root"
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
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
param.overrideTriggerFromOptions(options)
param.trigger.triggerSrc.setProcessName(dataVersion.getTriggerProcess())
# Set tau selection mode to 'standard'
#param.setAllTauSelectionOperatingMode('standard')
param.setAllTauSelectionOperatingMode('tauCandidateSelectionOnly')

# Set tau sources to trigger matched tau collections
#param.setAllTauSelectionSrcSelectedPatTaus()
param.setAllTauSelectionSrcSelectedPatTausTriggerMatched()

# Switch to PF2PAT objects
#param.changeCollectionsToPF2PAT()
param.changeCollectionsToPF2PAT(postfix=PF2PATVersion)


# Trigger with scale factors (at the moment hard coded)
if applyTriggerScaleFactor and dataVersion.isMC():
    param.triggerEfficiencyScaleFactor.mode = "scaleFactor"

# Set the data scenario for vertex/pileup weighting
puweight = "Run2011A"
if len(options.puWeightEra) > 0:
    puweight = options.puWeightEra
param.setPileupWeightFor2011(dataVersion, era=puweight) # Reweight by true PU distribution 
param.setDataTriggerEfficiency(dataVersion, era=puweight)

#param.trigger.selectionType = "disabled"

import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as tauEmbeddingCustomisations
if options.tauEmbeddingInput != 0:
    #tauEmbeddingCustomisations.addMuonIsolationEmbeddingForSignalAnalysis(process, process.commonSequence)
    tauEmbeddingCustomisations.setCaloMetSum(process, process.commonSequence, options, dataVersion)
    tauEmbeddingCustomisations.customiseParamForTauEmbedding(param, options, dataVersion)
    if tauEmbeddingFinalizeMuonSelection:
        applyIsolation = not doTauEmbeddingMuonSelectionScan
        additionalCounters.extend(tauEmbeddingCustomisations.addFinalMuonSelection(process, process.commonSequence, param,
                                                                                   enableIsolation=applyIsolation))
if doTauEmbeddingLikePreselection:
    additionalCounters.extend(tauEmbeddingCustomisations.addEmbeddingLikePreselection(process, process.commonSequence, param))

# Signal analysis module for the "golden analysis"
process.signalAnalysis = cms.EDFilter("HPlusSignalAnalysisInvertedTauFilter",
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
    bjetSelection = param.bjetSelection,
    topChiSelection = param.topChiSelection,
    topWithBSelection = param.topWithBSelection,                                     
    forwardJetVeto = param.forwardJetVeto,
    transverseMassCut = param.transverseMassCut,
    EvtTopology = param.EvtTopology,
    vertexWeight = param.vertexWeight,
    GenParticleAnalysis = param.GenParticleAnalysis,
    Tree = param.tree,
)

import HiggsAnalysis.HeavyChHiggsToTauNu.HChMetCorrection as MetCorrection
sequence = MetCorrection.addCorrectedMet(process, process.signalAnalysis)
process.commonSequence *= sequence


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

# Summer PAS cuts
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addAnalysis
if doSummerPAS:
    module = process.signalAnalysis.clone()
    module.tauSelection.rtauCut = 0
    module.MET.METCut = 70
    module.jetSelection.EMfractionCut = 999 # disable
    addAnalysis(process, "signalAnalysisRtau0MET70", module,
                preSequence=process.commonSequence,
                additionalCounters=additionalCounters,
                signalAnalysisCounters=True)


# b tagging testing
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
    prototypes = ["signalAnalysis"]
    if doSummerPAS:
        prototypes.append("signalAnalysisRtau0MET70")

    for name in prototypes:
        module = getattr(process, name).clone()
#        module.Tree.fill = False
        module.trigger.caloMetSelection.metEmulationCut = 60.0
        addAnalysis(process, name+"CaloMet60", module,
                    preSequence=process.commonSequence,
                    additionalCounters=additionalCounters,
                    signalAnalysisCounters=True)

        module = module.clone()
        module.triggerEfficiencyScaleFactor.mode = "efficiency"
        addAnalysis(process, name+"CaloMet60TEff", module,
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
    module = process.signalAnalysis.clone()
    module.Tree.fill = False
    param.addTauIdAnalyses(process, dataVersion, "signalAnalysis", module, process.commonSequence, additionalCounters)

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
def addJESVariation(name, doJetVariation, metVariation):
    jetVariationMode="all"
    module = getattr(process, name)

    module = module.clone()
    module.Tree.fill = False        
    module.Tree.fillJetEnergyFractions = False # JES variation will make the fractions invalid

    JESs = "%02d" % int(JESVariation*100)
    JESe = "%02d" % int(JESEtaVariation*100)
    JESm = "%02d" % int(metVariation*100)
    addJESVariationAnalysis(process, dataVersion, name, "JESPlus"+JESs+"eta"+JESe+"METPlus"+JESm,   module, additionalCounters, JESVariation, JESEtaVariation, metVariation, doJetVariation)
    addJESVariationAnalysis(process, dataVersion, name, "JESMinus"+JESs+"eta"+JESe+"METPlus"+JESm,  module, additionalCounters, -JESVariation, JESEtaVariation, metVariation, doJetVariation)
    addJESVariationAnalysis(process, dataVersion, name, "JESPlus"+JESs+"eta"+JESe+"METMinus"+JESm,  module, additionalCounters, JESVariation, JESEtaVariation, -metVariation, doJetVariation)
    addJESVariationAnalysis(process, dataVersion, name, "JESMinus"+JESs+"eta"+JESe+"METMinus"+JESm, module, additionalCounters, -JESVariation, JESEtaVariation, -metVariation, doJetVariation)

if doJESVariation or doSystematics:
    doJetVariation = True
    module = "signalAnalysis"
    modulePas = "signalAnalysisRtau0MET70"
    if options.tauEmbeddingInput != 0:
        doJetVariation = False
        module = "signalAnalysisCaloMet60TEff"
        modulePas = "signalAnalysisRtau0MET70CaloMet60TEff"
        JESUnclusteredMETVariation=0

    addJESVariation(module, doJetVariation, JESUnclusteredMETVariation)
    if doSummerPAS:
        addJESVariation(modulePas, doJetVariation, JESUnclusteredMETVariation)


if doPUWeightVariation or doSystematics:
    module = process.signalAnalysis.clone()
    module.Tree.fill = False
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

