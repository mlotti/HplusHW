import FWCore.ParameterSet.Config as cms

# Prefix all modules/sequences with the base name of the file, first
# letter lowercased (skimGenTau in this case)

# Provide the skimming sequence with the base name + Sequence
# (skimGenTauSequence in this case)

import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as customisations

skimGenTauTaus = cms.EDFilter("GenParticleSelector",
    src = cms.InputTag("genParticles"),
    cut = cms.string(customisations.generatorTauSelection % customisations.generatorTauPt)
)
skimGenTauTausFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("skimGenTauTaus"),
    minNumber = cms.uint32(1)
)
skimGenTauTausCount = cms.EDProducer("EventCountProducer")

skimGenTauSequence = cms.Sequence(
    skimGenTauTaus +
    skimGenTauTausFilter +
    skimGenTauTausCount
)

counters = [
    "skimGenTauTausCount"
]
