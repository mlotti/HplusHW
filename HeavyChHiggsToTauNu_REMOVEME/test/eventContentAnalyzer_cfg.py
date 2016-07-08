import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing()
options.register('inputFiles',
                 '',
                 options.multiplicity.list,
                 options.varType.string,
                 "Files to process")
options.parseArguments()
process = cms.Process("EVENTCONTENTANALYZER")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )
process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(options.inputFiles)
)

process.MessageLogger = cms.Service("MessageLogger",
    categories = cms.untracked.vstring("HLTTableInfo"),
    destinations = cms.untracked.vstring("cout"),
    cout = cms.untracked.PSet(
        threshold = cms.untracked.string("DEBUG"),
        default = cms.untracked.PSet(limit = cms.untracked.int32(1)),
    )
)

process.analyzer = cms.EDAnalyzer("EventContentAnalyzer")
process.path = cms.Path(process.analyzer)
