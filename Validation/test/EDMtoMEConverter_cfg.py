import FWCore.ParameterSet.Config as cms

process = cms.Process("EDMtoMEConvert")
process.load("DQMServices.Examples.test.MessageLogger_cfi")

process.load("Configuration.StandardSequences.EDMtoMEAtJobEnd_cff")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
	"file:output.root"
    )
)

process.p1 = cms.Path(process.EDMtoMEConverter*process.dqmSaver)

