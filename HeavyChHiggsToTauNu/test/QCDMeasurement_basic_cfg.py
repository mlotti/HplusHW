import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

################################################################################
# Configuration

# Select the version of the data (needed only for interactice running,
dataVersion="44XmcS6"     # Fall11 MC
#dataVersion="44Xdata"    # Run2011 08Nov and 19Nov ReRecos

# Set the data scenario for vertex/pileup weighting
# options: Run2011A, Run2011B, Run2011A+B
puweight = "Run2011A+B"

# Apply beta cut for jets to reject PU jets
betaCutForJets = 0.7 # Disable by setting to 0.0; if you want to enable, set to 0.2

##########
# Flags for additional signal analysis modules
# Perform the signal analysis with all tau ID algorithms in addition
# to the "golden" analysis

# Perform the signal analysis with the JES variations in addition to
# the "golden" analysis
doSystematics = False

# Tree filling
doFillTree = False

# Set level of how many histograms are stored to files
# options are: 'Vital' (least histograms), 'Informative', 'Debug' (all histograms)
myHistogramAmbientLevel = "Debug"

applyTriggerScaleFactor = True

PF2PATVersion = "PFlow" # For normal PF2PAT
#PF2PATVersion = "PFlowChs" # For PF2PAT with CHS

# Enable/disable prescales for data
doPrescalesForData = False

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
myOptimisation.addJetEtVariation([20.0, 30.0])
#myOptimisation.addJetBetaVariation(["GT0.0","GT0.5","GT0.7"])
#myOptimisation.addMETSelectionVariation([50.0, 60.0, 70.0])
#myOptimisation.addBJetLeadingDiscriminatorVariation([0.898, 0.679])
#myOptimisation.addBJetSubLeadingDiscriminatorVariation([0.679, 0.244])
#myOptimisation.addBJetEtVariation([])
myOptimisation.addBJetNumberVariation(["GEQ1", "GEQ2"])
myOptimisation.addDeltaPhiVariation([180.0,160.0,140.0])
#myOptimisation.addTopRecoVatiation(["None"]) # Valid options: None, chi, std, Wselection
myOptimisation.disableMaxVariations()
if doOptimisation:
    doSystematics = True # Make sure that systematics are run
    doFillTree = False # Make sure that tree filling is disabled or root file size explodes
    myHistogramAmbientLevel = "Vital" # Set histogram level to least histograms to reduce output file sizes
    # FIXME add here "light' mode running


################################################################################

# Command line arguments (options) and DataVersion object
options, dataVersion = getOptionsDataVersion(dataVersion)

################################################################################
# Define the process
process = cms.Process("HChQCDMeasurementMethodBasic")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(500) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source('PoolSource',
    duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
    fileNames = cms.untracked.vstring(
    #"file:/media/disk/attikis/PATTuples/v18/pattuple_v18_Run2011A_PromptReco_v4_AOD_166374_9_1_jHG.root"
    #"file:/media/disk/attikis/PATTuples/v18/pattuple_v18_TTJets_TuneZ2_Summer11_9_1_bfN.root"
    #
    #"rfio:/castor/cern.ch/user/a/attikis/pattuples/testing/v18/pattuple_v18_Run2011A_PromptReco_v4_AOD_166374_9_1_jHG.root"
    #"rfio:/castor/cern.ch/user/a/attikis/pattuples/testing/v18/pattuple_v18_TTJets_TuneZ2_Summer11_9_1_bfN.root"
    #
    # dataVersion.getAnalysisDefaultFileCastor()
    # For testing in jade
    dataVersion.getAnalysisDefaultFileMadhatter()
    #dataVersion.getAnalysisDefaultFileMadhatterDcap()
    )
)

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())
print "GlobalTag="+dataVersion.getGlobalTag()

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")

# Uncomment the following in order to print the counters at the end of
# the job (note that if many other modules are being run in the same
# job, their INFO messages are printed too)
#process.MessageLogger.cerr.threshold = cms.untracked.string("INFO") #tmp
#process.MessageLogger.cerr.FwkReport.reportEvery = 1000

# Fragment to run PAT on the fly if requested from command line
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPatOnTheFly
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion)

# Add configuration information to histograms.root
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addConfigInfo
process.infoPath = addConfigInfo(process, options, dataVersion)

################################################################################
# Import default parameter set and make necessary tweaks
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
param.overrideTriggerFromOptions(options)
param.trigger.triggerSrc.setProcessName(dataVersion.getTriggerProcess())
# Set tau selection mode (options: 'tauCandidateSelectionOnly')
# other options (use not recommended here): 'standard'
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
if len(options.puWeightEra) > 0:
    puweight = options.puWeightEra
param.setPileupWeight(dataVersion, process=process, commonSequence=process.commonSequence, pset=param.vertexWeight, psetReader=param.vertexWeightReader, era=puweight) # Reweight by true PU distribution
param.setDataTriggerEfficiency(dataVersion, era=puweight)
print "PU weight era =",puweight

# Overwrite necessary values here


##############################################################################
process.QCDMeasurement = cms.EDFilter("HPlusQCDMeasurementBasicFilter",
    blindAnalysisStatus = param.blindAnalysisStatus,
    histogramAmbientLevel = param.histogramAmbientLevel,
    trigger = param.trigger.clone(),
    triggerEfficiencyScaleFactor = param.triggerEfficiencyScaleFactor.clone(),
    primaryVertexSelection = param.primaryVertexSelection.clone(),
    GlobalElectronVeto = param.GlobalElectronVeto.clone(),
    GlobalMuonVeto = param.GlobalMuonVeto.clone(),
    tauSelection = param.tauSelectionHPSMediumTauBased.clone(),
    vetoTauSelection = param.vetoTauSelection.clone(),
    jetSelection = param.jetSelection.clone(),
    MET = param.MET.clone(),
    bTagging = param.bTagging.clone(),
    fakeMETVeto = param.fakeMETVeto.clone(),
    jetTauInvMass = param.jetTauInvMass.clone(),
    deltaPhiTauMET = param.deltaPhiTauMET,
    topReconstruction = param.topReconstruction,
    topSelection = param.topSelection.clone(),
    bjetSelection = param.bjetSelection.clone(),
    topChiSelection = param.topChiSelection.clone(),
    topWithBSelection = param.topWithBSelection.clone(),
    topWithWSelection = param.topWithWSelection.clone(),
    forwardJetVeto = param.forwardJetVeto.clone(),
    EvtTopology = param.EvtTopology.clone(),
    vertexWeight = param.vertexWeight.clone(),
    vertexWeightReader = param.vertexWeightReader.clone(),
    GenParticleAnalysis = param.GenParticleAnalysis.clone(),
    Tree = param.tree.clone(),
    eventCounter = param.eventCounter.clone(),
    factorisationTauPtBinLowEdges = cms.untracked.vdouble(40., 50., 60., 70., 80., 100., 120., 150.),
    factorisationTauEtaBinLowEdges = cms.untracked.vdouble(-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0), # probably need to constrain to -1.5, 1.5, i.e. endcap-, barrel, endcap+
    factorisationNVerticesBinLowEdges = cms.untracked.vint32(5, 10, 15, 20, 25, 30),
    factorisationTransverseMassRange = cms.untracked.vdouble(40., 0., 400.),
    factorisationFullMassRange = cms.untracked.vdouble(50., 0., 500.),
)
if not doFillTree:
    process.QCDMeasurement.Tree.fill = cms.untracked.bool(False)
process.QCDMeasurement.histogramAmbientLevel = myHistogramAmbientLevel

# Btagging DB
process.load("CondCore.DBCommon.CondDBCommon_cfi")
#MC measurements
process.load ("RecoBTag.PerformanceDB.PoolBTagPerformanceDBMC36X")
process.load ("RecoBTag.PerformanceDB.BTagPerformanceDBMC36X")
#Data measurements
process.load ("RecoBTag.PerformanceDB.BTagPerformanceDB1107")
process.load ("RecoBTag.PerformanceDB.PoolBTagPerformanceDB1107")
#User DB for btag eff
btagDB = 'sqlite_file:../data/DBs/BTAGTCHEL_hplusBtagDB_TTJets.db'
if options.runOnCrab != 0:
    print "BTagDB: Assuming that you are running on CRAB"
    btagDB = "sqlite_file:src/HiggsAnalysis/HeavyChHiggsToTauNu/data/DBs/BTAGTCHEL_hplusBtagDB_TTJets.db"
else:
    print "BTagDB: Assuming that you are not running on CRAB (if you are running on CRAB, add to job parameters in multicrab.cfg runOnCrab=1)"
process.CondDBCommon.connect = btagDB
process.load ("HiggsAnalysis.HeavyChHiggsToTauNu.Pool_BTAGTCHEL_hplusBtagDB_TTJets")
process.load ("HiggsAnalysis.HeavyChHiggsToTauNu.Btag_BTAGTCHEL_hplusBtagDB_TTJets")
param.bTagging.UseBTagDB  = cms.untracked.bool(False)

# Type 1 MET

# Add type 1 MET
import HiggsAnalysis.HeavyChHiggsToTauNu.HChMetCorrection as MetCorrection
sequence = MetCorrection.addCorrectedMet(process, process.QCDMeasurement, postfix=PF2PATVersion)
process.commonSequence *= sequence

# Set beta variable for jets
process.QCDMeasurement.jetSelection.betaCut = betaCutForJets

# Prescale fetching done automatically for data
if dataVersion.isData() and doPrescalesForData:
    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HPlusPrescaleWeightProducer_cfi")
    process.hplusPrescaleWeightProducer.prescaleWeightTriggerResults.setProcessName(dataVersion.getTriggerProcess())
    process.hplusPrescaleWeightProducer.prescaleWeightHltPaths = param.trigger.triggers.value()
    process.commonSequence *= process.hplusPrescaleWeightProducer
    process.QCDMeasurement.prescaleSource = cms.untracked.InputTag("hplusPrescaleWeightProducer")

# Print output
print "\ntree will be filled:", process.QCDMeasurement.Tree.fill.value()
#print "\nVertexWeight:", process.QCDMeasurement.vertexWeight.value()
#print "\nTrigger:", process.QCDMeasurement.trigger
#print "\nPV Selection:", process.QCDMeasurement.primaryVertexSelection
print "Trigger scale factor mode:", process.QCDMeasurement.triggerEfficiencyScaleFactor.mode.value()
print "Trigger scale factor data:", process.QCDMeasurement.triggerEfficiencyScaleFactor.dataSelect.value()
print "Trigger scale factor MC:", process.QCDMeasurement.triggerEfficiencyScaleFactor.mcSelect.value()
print "VertexWeight data distribution:",process.QCDMeasurement.vertexWeight.dataPUdistribution.value()
print "VertexWeight mc distribution:",process.QCDMeasurement.vertexWeight.mcPUdistribution.value()
print "Cut on HLT MET (check histogram Trigger_HLT_MET for minimum value): ", process.QCDMeasurement.trigger.hltMetCut.value()
print "\nTauSelection operating mode:", process.QCDMeasurement.tauSelection.operatingMode.value()
print "TauSelection src:", process.QCDMeasurement.tauSelection.src.value()
print "TauSelection selection:", process.QCDMeasurement.tauSelection.selection.value()
print "TauSelection isolation:", process.QCDMeasurement.tauSelection.isolationDiscriminator.value()
print "TauSelection rtauCut:", process.QCDMeasurement.tauSelection.rtauCut.value()
print "VetoTauSelection src:", process.QCDMeasurement.vetoTauSelection.tauSelection.src.value()

# Counter analyzer (in order to produce compatible root file with the
# python approach)
process.QCDMeasurement.eventCounter.printMainCounter = cms.untracked.bool(True)
#process.QCDMeasurement.eventCounter.printMainCounter = cms.untracked.bool(False)
if len(additionalCounters) > 0:
    process.QCDMeasurement.eventCounter.counters = cms.untracked.VInputTag([cms.InputTag(c) for c in additionalCounters])

# PickEvent module and the main Path. The picked events are only the
# ones selected by the golden analysis defined above.
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.PickEventsDumper_cfi")
if not doOptimisation:
    process.QCDMeasurementPath = cms.Path(
        process.commonSequence * # supposed to be empty, unless "doPat=1" command line argument is given
        process.QCDMeasurement *
        process.PickEvents
    )

# Optimisation
variationModuleNames = []
if doOptimisation:
    # Make variation modules
    variationModuleNames.extend(myOptimisation.generateVariations(process,additionalCounters,process.commonSequence,process.QCDMeasurement,"QCDMeasurement"))

def getQCDMeasurementModuleNames():
    modules = []
    if not doOptimisation:
        modules.append("QCDMeasurement")
    if doOptimisation:
        modules.extend(variationModuleNames)
    return modules

################################################################################
# The QCD measurement with jet energy scale variation
#
# If the flag is true, create two paths for the variation in plus and
# minus, and clone the QCD measurement and counter modules to the
# paths. The tau, jet and MET collections to adjust are taken from the
# configuration of the golden analysis. The fragment below creates
# additional directories with suffix JES...
from HiggsAnalysis.HeavyChHiggsToTauNu.JetEnergyScaleVariation import addJESVariationAnalysis
def addJESVariation(name, doJetUnclusteredVariation):
    print "fixme"
    # FIXME: copy new code from signal analysis

# Print tau discriminators from one tau from one event. Note that if
# the path below is commented, the discriminators are not printed.
process.tauDiscriminatorPrint = cms.EDAnalyzer("HPlusTauDiscriminatorPrintAnalyzer",
    src = process.QCDMeasurement.tauSelection.src
)
#process.tauDiscriminatorPrintPath = cms.Path(
#    process.patSequence *
#    process.tauDiscriminatorPrint
#)

# PU weight variation
# Adds two directories (up and down)
def addPUWeightVariation(name):
    # Up variation
    module = getattr(process, name).clone()
    module.Tree.fill = False
    param.setPileupWeight(dataVersion, process, process.commonSequence, pset=module.vertexWeight, psetReader=module.vertexWeightReader, era=puweight, suffix="up")
    addAnalysis(process, name+"PUWeightPlus", module,
                preSequence=process.commonSequence,
                additionalCounters=additionalCounters,
                signalAnalysisCounters=True)
    # Down variation
    module = module.clone()
    param.setPileupWeight(dataVersion, process, process.commonSequence, pset=module.vertexWeight, psetReader=module.vertexWeightReader, era=puweight, suffix="down")
    addAnalysis(process, name+"PUWeightMinus", module,
                preSequence=process.commonSequence,
                additionalCounters=additionalCounters,
                signalAnalysisCounters=True)

if doSystematics:
    doJetUnclusteredVariation = True
    modules = getSignalAnalysisModuleNames()

    # JES variation is relevant for MC only
    if dataVersion.isMC():
        for name in modules:
            addJESVariation(name, doJetUnclusteredVariation)
    else:
        print "JES variation disabled for data (not meaningful for data)"
    print "Added JES variation for %d modules"%len(modules)
    # PU weight variation is relevant for MC only
    if dataVersion.isMC():
        for name in modules:
            addPUWeightVariation(name)
    else:
        print "PU weight variation disabled for data (not meaningful for data)"
    print "Added PU weight variation for %d modules"%len(modules)

################################################################################
#for QCD control plots
process.out = cms.OutputModule("PoolOutputModule",
                                fileName = cms.untracked.string('output.root'),
                                outputCommands = cms.untracked.vstring(
    "keep *_*_*_HChQCDMeasurement",
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

