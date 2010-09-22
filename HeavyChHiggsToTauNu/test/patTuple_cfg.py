import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions

#dataVersion = "35X"
#dataVersion = "35Xredigi"
dataVersion = "36X"
#dataVersion = "36Xspring10"
#dataVersion = "37X"

options = getOptions()
if options.dataVersion != "":
    dataVersion = options.dataVersion

print "Assuming data is ", dataVersion

# Create Process
process = cms.Process("HChPatTuple")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

# Global tag
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.GlobalTag.globaltag = cms.string("START36_V10::All")
process.GlobalTag.globaltag = cms.string("START38_V9::All")

# Source
process.source = cms.Source('PoolSource',
  duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
  fileNames = cms.untracked.vstring(
    "/store/mc/Summer10/WJets_7TeV-madgraph-tauola/AODSIM/START36_V9_S09-v1/0046/FEFEE1D1-F17B-DF11-B911-00304867C16A.root"
  )
)

# Load common stuff
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
del process.TFileService

# Output module
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('pattuple.root'),
    outputCommands = cms.untracked.vstring(
        "drop *",
        "keep *_genParticles_*_*",
        "keep GenEventInfoProduct_*_*_*",
        "keep GenRunInfoProduct_*_*_*",
        "keep edmTriggerResults_*_*_*",
        "keep triggerTriggerEvent_*_*_*"
    )
)

# Add PAT sequences
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import *
process.s = addPat(process, dataVersion)

# Create paths
process.path    = cms.Path(process.s)
process.outpath = cms.EndPath(process.out)

