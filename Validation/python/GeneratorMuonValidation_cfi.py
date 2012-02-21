import FWCore.ParameterSet.Config as cms

from HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelectionPF_cff import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.PFEmbeddingSource_cff import *

generatorMuonValidation = cms.EDAnalyzer("MuonValidation",
    src		       = cms.InputTag("genParticles"),
#    RecoMuons           = cms.InputTag("selectedPatMuons"),                                         
    RecoMuons          = cms.InputTag("tauEmbeddingMuons"),
    MCRecoMatchingCone = cms.double(0.2)
)

generatorMuonValidationSequence = cms.Sequence(
    tightMuons *
    tightenedMuons *
    tauEmbeddingMuons *
    generatorMuonValidation
)
