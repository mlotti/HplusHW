import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataVersion import DataVersion
import FWCore.ParameterSet.VarParsing as VarParsing

dataVersion = "36X"
#dataVersion = "36Xspring10"
#dataVersion = "37X"
#dataVersion = "38X"
#dataVersion = "data" # this is for collision data 

options = getOptions()
if options.dataVersion != "":
    dataVersion = options.dataVersion
options.doPat=1

print "Assuming data is ", dataVersion
dataVersion = DataVersion(dataVersion) # convert string to object

process = cms.Process("MUONNTUPLE")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        #dataVersion.getPatDefaultFileCastor()
        #dataVersion.getPatDefaultFileMadhatter()
        "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_3_8_X/DYJetsToLL_PU/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Fall10_E7TeV_ProbDist_2010Data_BX156_START38_V12_v1_GEN-SIM-RECO_tauembedding_skim_v5/f0f5761dbef0a56e664c9bfa3bb2c570/skim_10_1_SCv.root"
    )
)

################################################################################

trigger = options.trigger
if len(trigger) == 0:
    trigger = "HLT_Mu9"

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 5000
del process.TFileService

# Output module
process.out = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring("path")
    ),
    fileName = cms.untracked.string('ntuple.root'),
    outputCommands = cms.untracked.vstring()
)

process.selectionSequence = cms.Sequence()

from PhysicsTools.PatAlgos.tools.coreTools import removeSpecificPATObjects, removeCleaning
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPat
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataSelection import addDataSelection

if options.doPat != 0:
    process.collisionDataSelection = cms.Sequence()
    if dataVersion.isData():
        process.collisionDataSelection = addDataSelection(process, dataVersion, trigger)
    
    process.patSequence = addPat(process, dataVersion, doPatTrigger=False, doTauHLTMatching=False,
                                 doPatTaus=False, doPatElectronID=False)
    removeSpecificPATObjects(process, ["Photons"], False)
    removeCleaning(process, False)    
    process.patMuons.embedTrack = False # In order to avoid transient references and generalTracks is available anyway

    process.selectionSequence = cms.Sequence(
        process.collisionDataSelection * 
        process.patSequence
    )

# Override the outputCommands here, since PAT modifies it
process.out.outputCommands = cms.untracked.vstring(
    "drop *",
    "keep edmMergeableCounter_*_*_*", # in lumi block
    "keep *_muonNtp_*_MUONNTUPLE",
    "keep *_metNtp_*_MUONNTUPLE",
    "keep *_jetNtp_*_MUONNTUPLE",
    "keep *_jetIdNtp_*_MUONNTUPLE",
)

#process.load("HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelection_cff")
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelectionPF_cff")
process.selectionSequence *= process.muonSelectionSequence
process.muonTrigger.hltResults.setProcessName(dataVersion.getTriggerProcess())
process.muonTrigger.triggerConditions = cms.vstring(trigger)

process.jetNtp = cms.EDProducer("CandViewNtpProducer",
    src = cms.InputTag("goodJets"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("jet"),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(tag = cms.untracked.string("Pt"), quantity = cms.untracked.string("pt()")),
   )
)
process.goodJetsId = cms.EDFilter("PATJetSelector",
    src = cms.InputTag("goodJets"),
    cut = cms.string("numberOfDaughters() > 1 && chargedEmEnergyFraction() < 0.99 && neutralHadronEnergyFraction() < 0.99 && neutralEmEnergyFraction < 0.99 && chargedHadronEnergyFraction() > 0 && chargedMultiplicity() > 0")
)
process.jetIdNtp = cms.EDProducer("CandViewNtpProducer",
    src = cms.InputTag("goodJetsId"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("jetId"),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(tag = cms.untracked.string("Pt"), quantity = cms.untracked.string("pt()")),
   )
)

process.muonNtp = cms.EDProducer("CandViewNtpProducer",
    src = cms.InputTag("tauEmbeddingMuons"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("muon"),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(tag = cms.untracked.string("Pt"), quantity = cms.untracked.string("pt()")),
        cms.PSet(tag = cms.untracked.string("Eta"), quantity = cms.untracked.string("eta()")),
        cms.PSet(tag = cms.untracked.string("Iso03EmEt"), quantity = cms.untracked.string("isolationR03().emEt")),
        cms.PSet(tag = cms.untracked.string("Iso03HadEt"), quantity = cms.untracked.string("isolationR03().hadEt")), 
        cms.PSet(tag = cms.untracked.string("Iso03SumPt"), quantity = cms.untracked.string("isolationR03().sumPt")),
        cms.PSet(tag = cms.untracked.string("Iso05EmEt"), quantity = cms.untracked.string("isolationR05().emEt")),
        cms.PSet(tag = cms.untracked.string("Iso05HadEt"), quantity = cms.untracked.string("isolationR05().hadEt")), 
        cms.PSet(tag = cms.untracked.string("Iso05SumPt"), quantity = cms.untracked.string("isolationR05().sumPt")),
   )
)

process.metNtp = cms.EDProducer("CandViewNtpProducer",
    src = cms.InputTag("patMETsPF"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("pfmet"),
    eventInfo = cms.untracked.bool(False),
    variables = cms.VPSet(
        cms.PSet(tag = cms.untracked.string("Et"), quantity = cms.untracked.string("et()")),
   )
)

process.path = cms.Path(
    process.selectionSequence *
    process.goodJetsId *
    process.jetNtp *
    process.jetIdNtp *
    process.muonNtp *
    process.metNtp
)
process.endPath = cms.EndPath(
    process.out
)

#process.counters = cms.EDAnalyzer("HPlusEventCountAnalyzer",
#    printMainCounter = cms.untracked.bool(True),
#    printAvailableCounters = cms.untracked.bool(True),
#)
#process.path *= process.counters
