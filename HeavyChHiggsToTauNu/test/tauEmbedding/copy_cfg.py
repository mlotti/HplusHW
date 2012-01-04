import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing('analysis')
options.maxEvents = -1

# Just to not to throw whne the parameters are given from command line
# We don't want to import HChOptions, as it wouldn't work via additional_input_files

options.register("crossSection",
                 -1., # default value
                 options.multiplicity.singleton, # singleton or list
                 options.varType.float,          # string, int, or float
                 "Cross section of the dataset (stored to histograms ROOT file)")
options.register("dataVersion",
                 "", # default value
                 options.multiplicity.singleton, # singleton or list
                 options.varType.string,          # string, int, or float
                 "Data version")
options.register("trigger",
                 [],
                 options.multiplicity.list, options.varType.string,
                 "Triggers to use (logical OR if multiple given")

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
