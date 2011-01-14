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
options.register("printPaths",
                 0,
                 options.multiplicity.singleton,
                 options.varType.int,
                 "Print HLT paths")
options = getOptions(options)

hltProcess = "HLT"
if options.dataVersion != "":
    hltProcess = DataVersion(options.dataVersion).getTriggerProcess()
if options.hltProcess != "":
    hltProcess = options.hltProcess

print "Using HLT process name", hltProcess

process = cms.Process("HLTTABLEANALYZER")
maxEv = -1
if options.printPaths != 0:
    maxEv = 10
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(maxEv) )
process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring("ProductNotFound")
)

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(options.inputFiles)
)
if options.printPaths == 0:
    process.source.processingMode = cms.untracked.string("Runs")

#process.load("FWCore.MessageService.MessageLogger_cfi")
#process.MessageLogger.categories = cms.untracked.vstring("HLTTableInfo")
#del process.MessageLogger.statistics
process.MessageLogger = cms.Service("MessageLogger",
    categories = cms.untracked.vstring("HLTTableInfo"),
    destinations = cms.untracked.vstring("cout"),
    cout = cms.untracked.PSet(
        threshold = cms.untracked.string("DEBUG"),
        default = cms.untracked.PSet(limit = cms.untracked.int32(0)),
        HLTTableInfo = cms.untracked.PSet(limit = cms.untracked.int32(100)),
    )
)

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HPlusHLTTableAnalyzer_cfi")
process.hltTableAnalyzer.hltProcessName = hltProcess

process.path = cms.Path(process.hltTableAnalyzer)

if options.printPaths != 0:
    process.load("HLTrigger.HLTanalyzers.hlTrigReport_cfi")
    process.hlTrigReport.HLTriggerResults.setProcessName(hltProcess)
    process.path *= process.hlTrigReport

    process.MessageLogger.categories.append("HLTrigReport")
    process.MessageLogger.cout.HLTrigReport = cms.untracked.PSet(limit = cms.untracked.int32(1000000))


print process.dumpPython()
