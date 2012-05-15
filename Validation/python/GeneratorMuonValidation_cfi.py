import FWCore.ParameterSet.Config as cms

from HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelectionPF import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.PFEmbeddingSource_cff import *

generatorMuonValidation = cms.EDAnalyzer("MuonValidation",
    src		       = cms.InputTag("genParticles"),
#    RecoMuons           = cms.InputTag("selectedPatMuons"),                                         
    RecoMuons          = cms.InputTag("tauEmbeddingMuons"),
    MCRecoMatchingCone = cms.double(0.2)
)

print "########################################################"
print "# WARNING: in Validation/python/GeneratorMuonValidation"
print "# tightenedMuons and tauEmbeddingMuons were removed"
print "# from sequence - fix if necessary!"
print "########################################################"

#tightMuons = getTightMuonsDefinition()

generatorMuonValidationSequence = cms.Sequence(
#    tightMuons *
#    tightenedMuons *
#    tauEmbeddingMuons *
    generatorMuonValidation
)
