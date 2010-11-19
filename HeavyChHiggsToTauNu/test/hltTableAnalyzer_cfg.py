import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataVersion import DataVersion

options = VarParsing.VarParsing()
options.register('inputFiles',
                 '',
                 options.multiplicity.list,
                 options.varType.string,
                 "Files to process")
options.register("hltProcess",
                 "",
                 options.multiplicity.singleton,
                 options.varType.string,
                 "HLT Process name")
options = getOptions(options)

hltProcess = "HLT"
if options.dataVersion != "":
    hltProcess = DataVersion(options.dataVersion).getTriggerProcess()
if options.hltProcess != "":
    hltProcess = options.hltProcess

print "Using HLT process name", hltProcess

process = cms.Process("HLTTABLEANALYZER")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring("ProductNotFound")
)

process.source = cms.Source('PoolSource',
    duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
    processingMode = cms.untracked.string("Runs"),
    fileNames = cms.untracked.vstring(options.inputFiles)
)

#process.load("FWCore.MessageService.MessageLogger_cfi")
#process.MessageLogger.categories = cms.untracked.vstring("HLTTableInfo")
#del process.MessageLogger.statistics
process.MessageLogger = cms.Service(
    "MessageLogger",
    categories = cms.untracked.vstring("HLTTableInfo"),
    destinations = cms.untracked.vstring("cout"),
    cout = cms.untracked.PSet(
        threshold = cms.untracked.string("INFO"),
        default = cms.untracked.PSet(limit = cms.untracked.int32(0)),
        HLTTableInfo = cms.untracked.PSet(limit = cms.untracked.int32(100))
    )
)

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HPlusHLTTableAnalyzer_cfi")
process.hltTableAnalyzer.hltProcessName = hltProcess
process.path = cms.Path(process.hltTableAnalyzer)

