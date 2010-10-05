import FWCore.ParameterSet.Config as cms

process = cms.Process("COUNTANALYZER")

isData = False
#isData = True

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.categories.append("EventCounts")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000 # print the event number for every 100th event

process.maxEvents = cms.untracked.PSet(
        input = cms.untracked.int32(-1)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'file:output.root'
    )
)

process.countAnalyzer = cms.EDAnalyzer("HPlusEventCountAnalyzer",
    counters = cms.untracked.VInputTag(
       cms.InputTag("countAll"),
       cms.InputTag("countTauPtCut"),
       cms.InputTag("countTauEtaCut"),
       cms.InputTag("countTauLeadTrkPtCut"),
       cms.InputTag("countJetPtCut"),
       cms.InputTag("countMETCut")
    )
)

process.p = cms.Path(
    process.countAnalyzer
)

