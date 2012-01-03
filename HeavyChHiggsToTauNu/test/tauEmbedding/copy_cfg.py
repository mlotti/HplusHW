import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing('analysis')
options.maxEvents = -1
options.parseArguments()

process = cms.Process('TAUEMBEDDINGCOPY')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery=5000

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(options.inputFiles)
)
process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string(options.outputFile),
)

process.ep = cms.EndPath(process.output)
