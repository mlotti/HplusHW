import FWCore.ParameterSet.Config as cms

HChEventContent = cms.PSet(
    outputCommands = cms.untracked.vstring(
        "keep edmMergeableCounter_*_*_*", # in lumi block
        "keep *_selectedPatMuons_*_*",
        "keep *_selectedPatPhotons_*_*",
        "keep *_selectedPatElectrons_*_*",
        "keep *_tauEmbeddingMuons_*_*",
        "keep *_patTriggerEvent_*_*",
        "keep *_patTrigger_*_*",
        "keep *_hltL1GtObjectMap_*_*",
    )
)
