import FWCore.ParameterSet.Config as cms

process = cms.Process("MomValTest")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
	'rfio:/castor/cern.ch/user/s/slehti/HiggsAnalysisData/test_H120_100_1_08t_RAW_RECO.root'
    )
)

process.load('Configuration/StandardSequences/EndOfProcess_cff')
process.load("HiggsAnalysis.Validation.MomentumValidation_cfi")

ANALYSISEventContent = cms.PSet(
    outputCommands = cms.untracked.vstring('keep *_*_*_MomValTest')
)


process.out = cms.OutputModule("PoolOutputModule",
#    verbose = cms.untracked.bool(False),
    fileName = cms.untracked.string('output.root'),
    outputCommands = ANALYSISEventContent.outputCommands
)

process.p = cms.Path(
    process.MomentumValidation+
    process.endOfProcess+
    process.out
)
