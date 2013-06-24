import FWCore.ParameterSet.Config as cms

muons = cms.PSet(
    enabled = cms.bool(True),
    src = cms.InputTag("selectedPatMuons"),
    correctedEnabled = cms.bool(False),
    correctedSrc = cms.InputTag("NOT_SET"),
    tunePEnabled = cms.bool(False),
    functions = cms.PSet(
        dB = cms.string("dB()"),

        chargedHadronIso = cms.string("chargedHadronIso()"),
        neutralHadronIso = cms.string("neutralHadronIso()"),
        photonIso = cms.string("photonIso()"),
        puChargedHadronIso = cms.string("puChargedHadronIso()"),
    ),
    bools = cms.PSet(),
)



jets = cms.PSet(
    enabled = cms.bool(True),
    detailsEnabled = cms.bool(True),
    src = cms.InputTag("selectedPatJets"),
    functions = cms.PSet(
        csv = cms.string("bDiscriminator('combinedSecondaryVertexBJetTags')"),
    ),
    pileupIDs = cms.PSet(),
    floats = cms.PSet(),
    bools = cms.PSet(),
)
