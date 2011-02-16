import FWCore.ParameterSet.Config as cms

process = cms.Process("Validation")

dataVersion = "39Xredigi"

# Command line arguments (options) and DataVersion object
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion
options, dataVersion = getOptionsDataVersion(dataVersion)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#        'rfio:/castor/cern.ch/user/s/slehti/HiggsAnalysisData/test_H120_100_1_08t_RAW_RECO.root'
#	'file:/tmp/slehti/test_H120_100_1_08t_RAW_RECO.root'
	dataVersion.getAnalysisDefaultFileCastor()
    )
)

process.load('Configuration/StandardSequences/EndOfProcess_cff')
process.load("HiggsAnalysis.Validation.TauMomentumValidation_cff")

ANALYSISEventContent = cms.PSet(
    outputCommands = cms.untracked.vstring('keep *_*_*_Validation')
)

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('output.root'),
    outputCommands = ANALYSISEventContent.outputCommands
)

process.p = cms.Path(
    process.TauMomentumValidation+
    process.endOfProcess+
    process.out
)
