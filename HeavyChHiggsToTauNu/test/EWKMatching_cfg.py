import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

################################################################################
# Configuration

# Select the version of the data (needed only for interactice running,
# overridden automatically from multicrab
dataVersion="44XmcS6"     # Fall11 MC
#dataVersion="44Xdata"    # Run2011 08Nov and 19Nov ReRecos

# Set the data scenario for vertex/pileup weighting
# options: Run2011A, Run2011B, Run2011AB
puweight = "Run2011AB"

##########
# Flags for additional signal analysis modules

# Apply summer PAS style cuts
doSummerPAS = False # Rtau>0, MET>70

# Scan against electron discriminators
doAgainstElectronScan = False

# Disable Rtau
doRtau0 = False # Rtau>0, MET>50

# Perform b tagging scanning
doBTagScan = False


# fill tree for btagging eff study
doBTagTree = False

    
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

# Apply beta cut for jets to reject PU jets
betaCutForJets = 0.2 # Disable by setting to 0.0; if you want to enable, set to 0.2

######### 
#Flags for options in the signal analysis

# Keep / Ignore prescaling for data (suppresses greatly error messages 
# in datasets with or-function of triggers)
doPrescalesForData = False

# Tree filling
doFillTree = False

# Set level of how many histograms are stored to files
# options are: 'Vital' (least histograms), 'Informative', 'Debug' (all histograms)
myHistogramAmbientLevel = "Debug"

# Apply trigger scale factor or not
applyTriggerScaleFactor = True

PF2PATVersion = "PFlow" # For normal PF2PAT
#PF2PATVersion = "PFlowChs" # For PF2PAT with CHS

### Systematic uncertainty flags ###
# Running of systematic variations is controlled by the global flag
# (below), or the individual flags
doSystematics = False

# Perform the signal analysis with the JES variations in addition to
# the "golden" analysis
doJESVariation = False

# Perform the signal analysis with the PU weight variations
# https://twiki.cern.ch/twiki/bin/view/CMS/PileupSystematicErrors
doPUWeightVariation = False

# Do variations for optimisation
# Note: Keep number of variations below 200 to keep file sizes reasonable
# Note: Currently it is not possible to vary the tau selection -related variables, because only one JES and MET producer is made (tau selection influences type I MET correction and JES)

doOptimisation = False

from HiggsAnalysis.HeavyChHiggsToTauNu.OptimisationScheme import HPlusOptimisationScheme
myOptimisation = HPlusOptimisationScheme()
#myOptimisation.addTauPtVariation([40.0, 50.0])
#myOptimisation.addTauIsolationVariation([])
#myOptimisation.addTauIsolationContinuousVariation([])
#myOptimisation.addRtauVariation([0.0, 0.7])
#myOptimisation.addJetNumberSelectionVariation(["GEQ3", "GEQ4"])
#myOptimisation.addJetEtVariation([20.0, 30.0])
#myOptimisation.addJetBetaVariation(["GT0.0","GT0.5","GT0.7"])
#myOptimisation.addMETSelectionVariation([50.0, 60.0, 70.0])
#myOptimisation.addBJetLeadingDiscriminatorVariation([0.898, 0.679])
#myOptimisation.addBJetSubLeadingDiscriminatorVariation([0.679, 0.244])
#myOptimisation.addBJetEtVariation([])
#myOptimisation.addBJetNumberVariation(["GEQ1", "GEQ2"])
#myOptimisation.addDeltaPhiVariation([180.0,160.0,140.0])
#myOptimisation.addTopRecoVariation(["None","chi"]) # Valid options: None, chi, std, Wselection
myOptimisation.disableMaxVariations()
if doOptimisation:
    doSystematics = True # Make sure that systematics are run
    doFillTree = False # Make sure that tree filling is disabled or root file size explodes
    myHistogramAmbientLevel = "Vital" # Set histogram level to least histograms to reduce output file sizes

################################################################################

# Command line arguments (options) and DataVersion object
options, dataVersion = getOptionsDataVersion(dataVersion)

# These are needed for running against tau embedding samples, can be
# given also from command line
options.doPat=1
options.tauEmbeddingInput=1

################################################################################
# Define the process
process = cms.Process("HChEWKMatching")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(200) )

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
#    "rfio:/castor/cern.ch/user/a/attikis/pattuples/testing/v18/pattuple_v18_TTJets_TuneZ2_Summer11_9_1_bfN.root"
#    "file:/tmp/slehti/TTJets_TuneZ2_Summer11_pattuple_266_1_at8.root"
    # For testing in lxplus
    #dataVersion.getAnalysisDefaultFileCastor()
    # For testing in jade
    #dataVersion.getAnalysisDefaultFileMadhatter()
    #dataVersion.getAnalysisDefaultFileMadhatterDcap()
    "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/TTJets_TuneZ2_Fall11/TTJets_TuneZ2_7TeV-madgraph-tauola/Tauembedding_embedding_v44_2_TTJets_TuneZ2_Fall11/c7fbae985f4002d5d76ea04408a27e38/embedded_9_1_PTD.root"
    #"file:/mnt/flustre/wendland/embedded_latest.root"
    )
)

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())
if options.tauEmbeddingInput != 0:
    process.GlobalTag.globaltag = "START44_V13::All"
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

if dataVersion.isData():
    process.HBHENoiseSequence = cms.Sequence()
    process.commonSequence.replace(process.HBHENoiseFilter, process.HBHENoiseSequence*process.HBHENoiseFilter)
    import HiggsAnalysis.HeavyChHiggsToTauNu.HChDataSelection as DataSelection
    DataSelection.addHBHENoiseFilterResultProducer(process, process.HBHENoiseSequence)

################################################################################
# The "golden" version of the signal analysis
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
param.overrideTriggerFromOptions(options)
param.trigger.triggerSrc.setProcessName(dataVersion.getTriggerProcess())
# Set tau selection mode to 'standard'
param.setAllTauSelectionOperatingMode('standard')
#param.setAllTauSelectionOperatingMode('tauCandidateSelectionOnly')

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
if len(options.puWeightEra) > 0:
    puweight = options.puWeightEra
param.setPileupWeight(dataVersion, process=process, commonSequence=process.commonSequence, pset=param.vertexWeight, psetReader=param.pileupWeightReader, era=puweight) # Reweight by true PU distribution
param.setDataTriggerEfficiency(dataVersion, era=puweight)
print "PU weight era =",puweight

#param.trigger.selectionType = "disabled"

import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as tauEmbeddingCustomisations
if options.tauEmbeddingInput != 0:
    #tauEmbeddingCustomisations.addMuonIsolationEmbeddingForSignalAnalysis(process, process.commonSequence)
    tauEmbeddingCustomisations.setCaloMetSum(process, process.commonSequence, options, dataVersion)
    tauEmbeddingCustomisations.customiseParamForTauEmbedding(param, options, dataVersion)
    if dataVersion.isMC():
        process.muonTriggerFixSequence = cms.Sequence()
        additionalCounters.extend(tauEmbeddingCustomisations.addMuonTriggerFix(process, dataVersion, process.muonTriggerFixSequence, options))
        process.commonSequence.replace(process.patSequence, process.muonTriggerFixSequence*process.patSequence)
    if tauEmbeddingFinalizeMuonSelection:
        #applyIsolation = not doTauEmbeddingMuonSelectionScan
        applyIsolation = False
        additionalCounters.extend(tauEmbeddingCustomisations.addFinalMuonSelection(process, process.commonSequence, param,
                                                                                   enableIsolation=applyIsolation))
    #process.muonFinalSelectionElectronVetoFilter.GlobalElectronVeto.ElectronCollectionName = cms.untracked.InputTag("selectedPatElectronsPFlow","","MUONSKIM")

# Signal analysis module for the "golden analysis"
process.signalAnalysis = cms.EDFilter("HPlusEWKMatchingFilter",
    histogramAmbientLevel = param.histogramAmbientLevel,
    trigger = param.trigger.clone(),
    triggerEfficiencyScaleFactor = param.triggerEfficiencyScaleFactor.clone(),
    primaryVertexSelection = param.primaryVertexSelection.clone(),
    GlobalElectronVeto = param.GlobalElectronVeto.clone(),
    GlobalMuonVeto = param.GlobalMuonVeto.clone(),
    jetSelection = param.jetSelection.clone(),
    MET = param.MET.clone(),
    bTagging = param.bTagging.clone(),
    deltaPhiTauMET = param.deltaPhiTauMET,
    prescaleWeightReader = param.prescaleWeightReader.clone(),
    vertexWeight = param.vertexWeight.clone(),
    pileupWeightReader = param.pileupWeightReader.clone(),
    eventCounter = param.eventCounter.clone(),
)
#process.signalAnalysis.GlobalElectronVeto.ElectronCollectionName.setProcessName("")
process.signalAnalysis.histogramAmbientLevel = myHistogramAmbientLevel
process.signalAnalysis.MET.type1Src = cms.untracked.InputTag("")
process.signalAnalysis.MET.type2Src = cms.untracked.InputTag("")
#process.signalAnalysis.MET.rawSrc = cms.untracked.InputTag("pfMET","","EMBEDDING")
process.signalAnalysis.MET.select = "raw"

#if options.tauEmbeddingInput != 0:
#    process.signalAnalysis.tauEmbeddingStatus = True

# process.signalAnalysis.GlobalMuonVeto = param.NonIsolatedMuonVeto
# Change default tau algorithm here if needed
#process.signalAnalysis.tauSelection.tauSelectionHPSTightTauBased # HPS Tight is the default


# Add type 1 MET
#import HiggsAnalysis.HeavyChHiggsToTauNu.HChMetCorrection as MetCorrection
#sequence = MetCorrection.addCorrectedMet(process, process.signalAnalysis, postfix=PF2PATVersion)
#process.commonSequence *= sequence

# Set beta variable for jets
process.signalAnalysis.jetSelection.betaCut = betaCutForJets

# Prescale fetching done automatically for data
if dataVersion.isData() and options.tauEmbeddingInput == 0 and doPrescalesForData:
    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HPlusPrescaleWeightProducer_cfi")
    process.hplusPrescaleWeightProducer.prescaleWeightTriggerResults.setProcessName(dataVersion.getTriggerProcess())
    process.hplusPrescaleWeightProducer.prescaleWeightHltPaths = param.trigger.triggers.value()
    process.commonSequence *= process.hplusPrescaleWeightProducer
    process.signalAnalysis.prescaleWeightReader.weightSrc = "hplusPrescaleWeightProducer"
    process.signalAnalysis.prescaleWeightReader.enabled = True

# Print output
#print "\nAnalysis is blind:", process.signalAnalysis.blindAnalysisStatus, "\n"
print "Histogram level:", process.signalAnalysis.histogramAmbientLevel.value()
print "VertexWeight data distribution:",process.signalAnalysis.vertexWeight.dataPUdistribution.value()
print "VertexWeight mc distribution:",process.signalAnalysis.vertexWeight.mcPUdistribution.value()
print "TauSelection algorithm:", param.tauSelection
print "Beta cut: ", process.signalAnalysis.jetSelection.betaCutSource.value(), process.signalAnalysis.jetSelection.betaCutDirection.value(), process.signalAnalysis.jetSelection.betaCut.value()
print "electrons: ", process.signalAnalysis.GlobalElectronVeto
print "muons: ", process.signalAnalysis.GlobalMuonVeto
print "jets: ", process.signalAnalysis.jetSelection

# Counter analyzer (in order to produce compatible root file with the
# python approach)

process.signalAnalysis.eventCounter.printMainCounter = cms.untracked.bool(True)
#process.signalAnalysis.eventCounter.printSubCounters = cms.untracked.bool(True)

if len(additionalCounters) > 0:
    process.signalAnalysis.eventCounter.counters = cms.untracked.VInputTag([cms.InputTag(c) for c in additionalCounters])

# PickEvent module and the main Path. The picked events are only the
# ones selected by the golden analysis defined above.
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.PickEventsDumper_cfi")
if not doOptimisation:
    if (options.hasMCBJetsFilter != 0):
        print "Adding bjet filter, setting to",options.hasMCBJetsFilter
        process.MCbjetFilter = cms.EDFilter("HPlusMCHasBJetFilter",
            hasBjets = cms.untracked.bool(True)
        )
        if (options.hasMCBJetsFilter == -1):
            process.MCbjetFilter.hasBjets = cms.untracked.bool(False)

        process.signalAnalysisPath = cms.Path(
            process.MCbjetFilter *
            process.commonSequence * # supposed to be empty, unless "doPat=1" command line argument is given
            process.signalAnalysis *
            process.PickEvents
        )
    else:
        process.signalAnalysisPath = cms.Path(
            process.commonSequence * # supposed to be empty, unless "doPat=1" command line argument is given
            process.signalAnalysis *
            process.PickEvents
        )

if doMETResolution:
    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.METResolutionAnalysis_cfi")
    process.signalAnalysisPath += process.metResolutionAnalysis

# Optimisation
variationModuleNames = []
if doOptimisation:
    # Make variation modules
    variationModuleNames.extend(myOptimisation.generateVariations(process,additionalCounters,process.commonSequence,process.signalAnalysis,"signalAnalysis"))


from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addAnalysis

def getSignalAnalysisModuleNames():
    modules = []
    if not doOptimisation:
        modules.append("signalAnalysis")
    if doSummerPAS:
        modules.append("signalAnalysisRtau0MET70")
    if doRtau0:
        modules.append("signalAnalysisRtau0")
    if doOptimisation:
        modules.extend(variationModuleNames)
    return modules

# To have tau embedding like preselection
if doTauEmbeddingLikePreselection:
    # Preselection similar to tau embedding selection (genuine tau+3 jets+lepton vetoes), no tau+MET trigger required
    process.tauEmbeddingLikeSequence = cms.Sequence(process.commonSequence)
    module = process.signalAnalysis.clone()
    counters = additionalCounters[:]
    counters.extend(tauEmbeddingCustomisations.addEmbeddingLikePreselection(process, process.tauEmbeddingLikeSequence, module))
    addAnalysis(process, "signalAnalysisTauEmbeddingLikePreselection", module,
                preSequence=process.tauEmbeddingLikeSequence,
                additionalCounters=counters, signalAnalysisCounters=True)

    # Preselection similar to tau embedding selection (genuine tau+3 jets+lepton vetoes), tau+MET trigger required
    process.tauEmbeddingLikeTriggeredSequence = cms.Sequence(process.commonSequence)
    module = process.signalAnalysis.clone()
    counters = additionalCounters[:]
    counters.extend(tauEmbeddingCustomisations.addEmbeddingLikePreselection(process, process.tauEmbeddingLikeTriggeredSequence, module, prefix="embeddingLikeTriggeredPreselection", disableTrigger=False))
    addAnalysis(process, "signalAnalysisTauEmbeddingLikeTriggeredPreselection", module,
                preSequence=process.tauEmbeddingLikeTriggeredSequence,
                additionalCounters=counters, signalAnalysisCounters=True)    

    process.genuineTauSequence = cms.Sequence(process.commonSequence)
    module = process.signalAnalysis.clone()
    counters = additionalCounters[:]
    counters.extend(tauEmbeddingCustomisations.addGenuineTauPreselection(process, process.genuineTauSequence, module))
    addAnalysis(process, "signalAnalysisGenuineTauPreselection", module,
                preSequence=process.genuineTauSequence,
                additionalCounters=counters, signalAnalysisCounters=True)

    for name in getSignalAnalysisModuleNames():
        module = getattr(process, name).clone()
        module.onlyGenuineTaus = cms.untracked.bool(True)
        addAnalysis(process, name+"GenuineTau", module,
                    preSequence=process.commonSequence,
                    additionalCounters=additionalCounters, signalAnalysisCounters=True)

# With tau embedding input
if options.tauEmbeddingInput:
    prototypes = ["signalAnalysis"]
    if doSummerPAS:
        prototypes.append("signalAnalysisRtau0MET70")
    if doRtau0:
        prototypes.append("signalAnalysisRtau0")

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
def addJESVariation(name, doJetUnclusteredVariation):
    jetVariationMode="all"
    module = getattr(process, name)

    module = module.clone()
    module.Tree.fill = False        
    module.Tree.fillJetEnergyFractions = False # JES variation will make the fractions invalid

    addJESVariationAnalysis(process, dataVersion, name, "TESPlus",  module, additionalCounters, tauVariationSigma=1.0, postfix=PF2PATVersion)
    addJESVariationAnalysis(process, dataVersion, name, "TESMinus", module, additionalCounters, tauVariationSigma=-1.0, postfix=PF2PATVersion)

    if doJetUnclusteredVariation:
        # Do all variations beyond TES
        addJESVariationAnalysis(process, dataVersion, name, "JESPlus",  module, additionalCounters, jetVariationSigma=1.0, postfix=PF2PATVersion)
        addJESVariationAnalysis(process, dataVersion, name, "JESMinus", module, additionalCounters, jetVariationSigma=-1.0, postfix=PF2PATVersion)
        #addJESVariationAnalysis(process, dataVersion, name, "JERPlus",  module, additionalCounters, VariationSigma=1.0, postfix=PF2PATVersion)
        #addJESVariationAnalysis(process, dataVersion, name, "JERMinus", module, additionalCounters, VariationSigma=-1.0, postfix=PF2PATVersion)
        addJESVariationAnalysis(process, dataVersion, name, "METPlus",  module, additionalCounters, unclusteredVariationSigma=1.0, postfix=PF2PATVersion)
        addJESVariationAnalysis(process, dataVersion, name, "METMinus", module, additionalCounters, unclusteredVariationSigma=-1.0, postfix=PF2PATVersion)

if doJESVariation or doSystematics:
    doJetUnclusteredVariation = True

    modules = getSignalAnalysisModuleNames()
    if doTauEmbeddingLikePreselection:
        if options.tauEmbeddingInput != 0:
            raise Exception("tauEmbegginInput clashes with doTauEmbeddingLikePreselection")
        modules.extend([n+"GenuineTau" for n in modules])

    if options.tauEmbeddingInput != 0:
        modules = [n+"CaloMet60TEff" for n in modules]
        if dataVersion.isData():
            doJetUnclusteredVariation = False

    # JES variation is relevant for MC, and for tau in embedding
    if dataVersion.isMC() or options.tauEmbeddingInput != 0:
        for name in modules:
            addJESVariation(name, doJetUnclusteredVariation)
    else:
        print "JES variation disabled for data (not meaningful for data)"
    print "Added JES variation for %d modules"%len(modules)

def addPUWeightVariation(name):
    # Up variation
    module = getattr(process, name).clone()
    module.Tree.fill = False
    param.setPileupWeight(dataVersion, process, process.commonSequence, pset=module.vertexWeight, psetReader=module.pileupWeightReader, era=puweight, suffix="up")
    addAnalysis(process, name+"PUWeightPlus", module,
                preSequence=process.commonSequence,
                additionalCounters=additionalCounters,
                signalAnalysisCounters=True)
    # Down variation
    module = module.clone()
    param.setPileupWeight(dataVersion, process, process.commonSequence, pset=module.vertexWeight, psetReader=module.pileupWeightReader, era=puweight, suffix="down")
    addAnalysis(process, name+"PUWeightMinus", module,
                preSequence=process.commonSequence,
                additionalCounters=additionalCounters,
                signalAnalysisCounters=True)

if doPUWeightVariation or doSystematics:
    modules = getSignalAnalysisModuleNames()
    if doTauEmbeddingLikePreselection:
        if options.tauEmbeddingInput != 0:
            raise Exception("tauEmbegginInput clashes with doTauEmbeddingLikePreselection")
        modules.extend([n+"GenuineTau" for n in modules])

    if options.tauEmbeddingInput != 0:
        modules = [n+"CaloMet60TEff" for n in modules]

    # PU weight variation is relevant for MC only
    if dataVersion.isMC():
        for name in modules:
            addPUWeightVariation(name)
    else:
        print "PU weight variation disabled for data (not meaningful for data)"
    print "Added PU weight variation for %d modules"%len(modules)
    


# Signal analysis with various tightened muon selections for tau embedding
if options.tauEmbeddingInput != 0 and doTauEmbeddingMuonSelectionScan:
    tauEmbeddingCustomisations.addMuonIsolationAnalyses(process, "signalAnalysis", process.signalAnalysis, process.commonSequence, additionalCounters)

if doTauEmbeddingTauSelectionScan:
    tauEmbeddingCustomisations.addTauAnalyses(process, "signalAnalysis", process.signalAnalysis, process.commonSequence, additionalCounters)

# Print tau discriminators from one tau from one event. Note that if
# the path below is commented, the discriminators are not printed.
#process.tauDiscriminatorPrint = cms.EDAnalyzer("HPlusTauDiscriminatorPrintAnalyzer",
    #src = process.signalAnalysis.tauSelection.src
#)
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
        "keep *_*_*_HChEWKMatching",
        "drop *_*_counterNames_*",
        "drop *_*_counterInstances_*",
#	"drop *",
	"keep *",
#        "keep edmMergeableCounter_*_*_*"
    )
)

# Uncomment the following line to get also the event output (can be
# useful for debugging purposes)
#process.outpath = cms.EndPath(process.out)

#f = open("configDump.py", "w")
#f.write(process.dumpPython())
#f.close()
