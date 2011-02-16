import FWCore.ParameterSet.Config as cms

from patTuple_cfg import *

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#        'rfio:/castor/cern.ch/user/s/slehti/HiggsAnalysisData/test_H120_100_1_08t_RAW_RECO.root'
	'file:/tmp/slehti/test_H120_100_1_08t_RAW_RECO.root'
    )
)

process.load('Configuration/StandardSequences/EndOfProcess_cff')
process.load("HiggsAnalysis.Validation.MomentumValidation_cfi")

process.validatePatHPSTau = process.MomentumValidation.clone()
process.validatePatHPSTau.src = cms.InputTag("patTausHpsPFTau")

process.validatePatHPSTauTriggerMatch = process.MomentumValidation.clone()
process.validatePatHPSTauTriggerMatch.src = cms.InputTag("selectedPatTausHpsPFTauTauTriggerMatched")

process.validateTriggerTaus = process.MomentumValidation.clone()
process.validateTriggerTaus.src = cms.InputTag("patTrigger")


process.out.fileName = cms.untracked.string('output.root')
process.out.outputCommands.append('keep *_*_*_HChPatTuple')

process.path    = cms.Path(
    process.collisionDataSelection * # this is supposed to be empty for MC
    process.s
    * process.triggerMatchingSequence
    * process.validatePatHPSTau
    * process.validatePatHPSTauTriggerMatch
    * process.validateTriggerTaus
    * process.endOfProcess
)
