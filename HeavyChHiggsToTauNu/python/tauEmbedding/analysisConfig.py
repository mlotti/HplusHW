import FWCore.ParameterSet.Config as cms

muonFunctions = cms.PSet(
    dB = cms.string("dB()"),

    trackIso = cms.string("trackIso()"),
    caloIso = cms.string("caloIso()"),

    chargedHadronIso = cms.string("chargedHadronIso()"),
    neutralHadronIso = cms.string("neutralHadronIso()"),
    photonIso = cms.string("photonIso()"),
    puChargedHadronIso = cms.string("puChargedHadronIso()"),
        
    chargedHadronIso_01to04 = cms.string("userFloat('embeddingStep_pfChargedHadrons')"),
    neutralHadronIso_01to04 = cms.string("userFloat('embeddingStep_pfNeutralHadrons')"),
    photonIso_01to04 = cms.string("userFloat('embeddingStep_pfPhotons')"),
    puChargedHadronIso_01to04 = cms.string("userFloat('embeddingStep_pfPUChargedHadrons')"),

#     chargedHadronIsoEmb_01to04 = cms.string("userFloat('iso01to04_pfChargedHadrons')"),
#     neutralHadronIsoEmb_01to04 = cms.string("userFloat('iso01to04_pfNeutralHadrons')"),
#     photonIsoEmb_01to04 = cms.string("userFloat('iso01to04_pfPhotons')"),
#     puChargedHadronIsoEmb_01to04 = cms.string("userFloat('iso01to04_pfPUChargedHadrons')"),

#     chargedHadronIsoEmb_01to03 = cms.string("userFloat('iso01to03_pfChargedHadrons')"),
#     neutralHadronIsoEmb_01to03 = cms.string("userFloat('iso01to03_pfNeutralHadrons')"),
#     photonIsoEmb_01to03 = cms.string("userFloat('iso01to03_pfPhotons')"),
#     puChargedHadronIsoEmb_01to03 = cms.string("userFloat('iso01to03_pfPUChargedHadrons')"),

#     tauTightIc04Iso = cms.string("userInt('byTightIc04ChargedOccupancy')+userInt('by%TightIc04GammaOccupancy')"),
)

electronFunctions = cms.PSet(
    superClusterEta = cms.string("? superCluster().isNonnull() ? superCluster().eta() : -1e20")
)

jetFunctions = cms.PSet(
    # btag
    tche = cms.string("bDiscriminator('trackCountingHighEffBJetTags')"),
    csv = cms.string("bDiscriminator('combinedSecondaryVertexBJetTags')"),
    # beta
    beta = cms.string("userFloat('Beta')"),
    betaStar = cms.string("userFloat('BetaStar')"),
)

def puID(name):
    return cms.PSet(
        mvaSrc = cms.InputTag("puJetMva", "%sDiscriminant" % name),
        flagSrc = cms.InputTag("puJetMva", "%sId" % name),
    )
jetPileupIDs = cms.PSet(
    fullId = puID("full"),
    cutbased = puID("cutbased"),
    simpleId = puID("simple"),
    philv1 = puID("philv1"),
)

tauFunctions = cms.PSet()
_tauIds = [
    "decayModeFinding",
    "againstMuonLoose", "againstMuonTight", "againstMuonTight2",
    "againstElectronLoose", "againstElectronMedium", "againstElectronTight", "againstElectronMVA", "againstElectronTightMVA3", "againstElectronVTightMVA3",
#    "byVLooseIsolation", "byLooseIsolation", "byMediumIsolation", "byTightIsolation",
    "byLooseCombinedIsolationDeltaBetaCorr", "byMediumCombinedIsolationDeltaBetaCorr", "byTightCombinedIsolationDeltaBetaCorr",
    "byLooseCombinedIsolationDeltaBetaCorr3Hits", "byMediumCombinedIsolationDeltaBetaCorr3Hits", "byTightCombinedIsolationDeltaBetaCorr3Hits",
    ]
for name in _tauIds:
    setattr(tauFunctions, name, cms.string("tauID('%s')"%name))

mets = cms.PSet(
    caloMet_p4 = cms.InputTag("met"),
    caloMetNoHF_p4 = cms.InputTag("metNoHF"),
    pfMet_p4 = cms.InputTag("pfMet"),
)
