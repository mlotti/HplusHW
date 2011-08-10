import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing()
options.register('inputFiles',
                 '',
                 options.multiplicity.list,
                 options.varType.string,
                 "Files to process")
options.register("outputFile",
                 "",
                 options.multiplicity.singleton,
                 options.varType.string,
                 "Print HLT paths")
options.parseArguments()

inputFiles = []
for name in options.inputFiles:
    if name[0:6] != "/store" and not ":/" in name:
        inputFiles.append("file:"+name)
        print name

print inputFiles

process = cms.Process("NTUPLEMERGE")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

#process.options = cms.untracked.PSet(
#      fileMode = cms.untracked.string('FULLMERGE')
#)

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 10000

process.source = cms.Source('PoolSource',
#  noEventSort = cms.untracked.bool(True),
  fileNames = cms.untracked.vstring(inputFiles)
)

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string(options.outputFile)
)

process.outpath = cms.EndPath(process.out)

