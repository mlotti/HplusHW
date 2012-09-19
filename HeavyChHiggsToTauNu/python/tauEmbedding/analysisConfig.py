import FWCore.ParameterSet.Config as cms

muonFunctions = cms.PSet(
    dB = cms.string("dB()"),

    trackIso = cms.string("trackIso()"),
    caloIso = cms.string("caloIso()"),

    chargedHadronIso = cms.string("chargedHadronIso()"),
    neutralHadronIso = cms.string("neutralHadronIso()"),
    photonIso = cms.string("photonIso()"),
    puChargedHadronIso = cms.string("puChargedHadronIso()"),
        
    chargedHadronIsoEmb = cms.string("userFloat('ontheflyiso_pfChargedHadrons')"),
    neutralHadronIsoEmb = cms.string("userFloat('ontheflyiso_pfNeutralHadrons')"),
    photonIsoEmb = cms.string("userFloat('ontheflyiso_pfPhotons')"),
    puChargedHadronIsoEmb = cms.string("userFloat('ontheflyiso_pfPUChargedHadrons')"),

    chargedHadronIsoEmb_01to04 = cms.string("userFloat('iso01to04_pfChargedHadrons')"),
    neutralHadronIsoEmb_01to04 = cms.string("userFloat('iso01to04_pfNeutralHadrons')"),
    photonIsoEmb_01to04 = cms.string("userFloat('iso01to04_ontheflyiso_pfPhotons')"),
    puChargedHadronIsoEmb_01to04 = cms.string("userFloat('iso01to04_pfPUChargedHadrons')"),

    chargedHadronIsoEmb_01to03 = cms.string("userFloat('iso01to03_pfChargedHadrons')"),
    neutralHadronIsoEmb_01to03 = cms.string("userFloat('iso01to03_pfNeutralHadrons')"),
    photonIsoEmb_01to03 = cms.string("userFloat('iso01to03_ontheflyiso_pfPhotons')"),
    puChargedHadronIsoEmb_01to03 = cms.string("userFloat('iso01to03_pfPUChargedHadrons')"),

    tauTightIc04Iso = cms.string("userInt('byTightIc04ChargedOccupancy')+userInt('by%TightIc04GammaOccupancy')"),
)

jetFunctions = cms.PSet(
    # btag
    tche = cms.string("bDiscriminator('trackCountingHighEffBJetTags')"),
    csv = cms.string("bDiscriminator('combinedSecondaryVertexBJetTags')"),
    # beta
    beta = cms.string("userFloat('Beta')"),
    betaStar = cms.string("userFloat('BetaStar')"),
)

tauFunctions = cms.PSet()
_tauIds = [
    "decayModeFinding",
    "againstMuonLoose", "againstMuonTight",
    "againstElectronLoose", "againstElectronMedium", "againstElectronTight", "againstElectronMVA",
    "byVLooseIsolation", "byLooseIsolation", "byMediumIsolation", "byTightIsolation",
    "byLooseCombinedIsolationDeltaBetaCorr", "byMediumCombinedIsolationDeltaBetaCorr", "byTightCombinedIsolationDeltaBetaCorr",
    ]
for name in _tauIds:
    setattr(tauFunctions, name, cms.string("tauID('%s')"%name))

mets = cms.PSet(
    caloMet_p4 = cms.InputTag("met"),
    caloMetNoHF_p4 = cms.InputTag("metNoHF"),
    pfMet_p4 = cms.InputTag("pfMet"),
)
