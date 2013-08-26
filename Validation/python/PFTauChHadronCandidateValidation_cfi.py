import FWCore.ParameterSet.Config as cms

PFTauValidation = cms.EDAnalyzer('PFTauChHadronCandidateValidation',
    src = cms.InputTag("fixedConePFTauProducer")
)
