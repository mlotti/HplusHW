import FWCore.ParameterSet.Config as cms

process = cms.Process("COUNTANALYZER")

isData = False
#isData = True

process.load("FWCore.MessageService.MessageLogger_cfi")
#process.MessageLogger.cerr.FwkReport.reportEvery = 100 # print the event number for every 100th event

process.maxEvents = cms.untracked.PSet(
        input = cms.untracked.int32(-1)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'file:output.root'
    )
)

process.countAnalyzer = cms.EDAnalyzer("HPlusEventCountAnalyzer"
)

process.p = cms.Path(
    process.countAnalyzer
)

