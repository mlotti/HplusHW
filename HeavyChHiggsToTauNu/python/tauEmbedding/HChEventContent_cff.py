import FWCore.ParameterSet.Config as cms

HChEventContent = cms.PSet(
    outputCommands = cms.untracked.vstring(
        "keep edmMergeableCounter_*_*_*", # in lumi block
        "keep *_selectedPatMuons_*_*",
        "keep *_tightMuons*_*_*",
        "keep *_selectedPatPhotons_*_*",
        "keep *_selectedPatElectrons_*_*",
        "keep *_selectedPatJets*_*_*",
        "keep *_goodJets_*_*",
        "keep *_selectedPatTaus*_*_*",
        "keep *_tauEmbeddingMuons_*_*",
        "keep *_patTriggerEvent_*_*",
        "keep *_patTrigger_*_*",
        "keep *_hltL1GtObjectMap_*_*",
        "keep *_l1GtTriggerMenuLite_*_*", # in run block, needed for prescale provider
        "keep recoCaloMETs_*_*_*",
        "keep *_towerMaker_*_*",
        "keep *_electronGsfTracks_*_*",
        "keep recoTracks_*_*_*",
        "keep recoBeamHaloSummary_*_*_*", # keep beam halo summaries
        "keep recoGlobalHaloData_*_*_*",
    )
)
