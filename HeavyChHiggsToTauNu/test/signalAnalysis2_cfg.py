import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions
import copy

dataVersion = "35X"
#dataVersion = "36X"
#dataVersion = "37X"

options = getOptions()
if options.dataVersion != "":
    dataVersion = options.dataVersion

print "Assuming data is ", dataVersion

triggerProcess = "HLT"
triggerProcessMap = {"35X": "HLT",
                     "35Xredigi": "REDIGI",
                     "36X": "REDIGI36X",
                     "37X": "REDIGI37X"}
if dataVersion in triggerProcessMap:
    triggerProcess = triggerProcessMap[dataVersion]


process = cms.Process("HChSignalAnalysis")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string("START38_V9::All")

process.source = cms.Source('PoolSource',
    duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
#    skipEvents = cms.untracked.uint32(500),
    fileNames = cms.untracked.vstring(
    "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_3_8_X/TTbar_Htaunu_M80/TTbar_Htaunu_M80/Spring10_START3X_V26_S09_v1_GEN-SIM-RECO-pattuple_test5/744fc999107787b3f27dc1fe1e804784/pattuple_4_1_pCt.root"

#        "file:pattuple-1000.root"
  )
)

################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.categories.append("EventCounts")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.cerr.threshold = cms.untracked.string("INFO")
process.TFileService.fileName = "histograms.root"

process.signalAnalysis = cms.EDProducer("HPlusSignalAnalysisProducer",
    trigger = cms.untracked.PSet(
        src = cms.untracked.InputTag("patTriggerEvent"),
        trigger = cms.untracked.string("HLT_SingleLooseIsoTau20")
    ),
    tauSelection = cms.untracked.PSet(
        src = cms.untracked.InputTag("selectedPatTaus"),
        ptCut = cms.untracked.double(20),
        etaCut = cms.untracked.double(2.4),
        leadingTrackPtCut = cms.untracked.double(10)
    ),
    jetSelection = cms.untracked.PSet(
        src = cms.untracked.InputTag("selectedPatJets"),
#        src = cms.untracked.InputTag("selectedPatJetsAK5JPT"),
        cleanTauDR = cms.untracked.double(0.5),
        ptCut = cms.untracked.double(20),
        etaCut = cms.untracked.double(2.4),
        minNumber = cms.untracked.uint32(3)
    ),
    bTagging = cms.untracked.PSet(
        discriminator = cms.untracked.string("trackCountingHighEffBJetTags"),
        discriminatorCut = cms.untracked.double(1.5),
        minNumber = cms.untracked.uint32(1)
    ),
    MET = cms.untracked.PSet(
        src = cms.untracked.InputTag("patMETs"),
#        src = cms.untracked.InputTag("patMETsPF"),
#        src = cms.untracked.InputTag("patMETsTC"),
        METCut = cms.untracked.double(40)
    )
)
process.path = cms.Path(process.signalAnalysis)

# Counter analyzer (in order to produce compatible root file with the
# python approach)
process.counters = cms.EDAnalyzer("HPlusEventCountAnalyzer",
    counterNames = cms.untracked.InputTag("signalAnalysis", "counterNames"),
    counterInstances = cms.untracked.InputTag("signalAnalysis", "counterInstances")
)
process.counterPath = cms.Path(process.counters)


################################################################################

process.out = cms.OutputModule("PoolOutputModule",
#    SelectEvents = cms.untracked.PSet(
#        SelectEvents = cms.vstring("path")
#    ),
    fileName = cms.untracked.string('output.root'),
    outputCommands = cms.untracked.vstring(
        "keep *_*_*_HChSignalAnalysis"
#	"drop *",
#        "keep edmMergeableCounter_*_*_*"
    )
)
process.outpath = cms.EndPath(process.out)

process.schedule = cms.Schedule(
    process.path,
    process.counterPath
#    ,process.outpath
)
