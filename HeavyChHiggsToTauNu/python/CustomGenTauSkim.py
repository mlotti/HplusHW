import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as customisations

def customize(process):
    process.skimGenTauTausCountAll = cms.EDProducer("EventCountProducer")
    
    process.skimGenTauTaus = cms.EDFilter("GenParticleSelector",
        src = cms.InputTag("genParticles"),
        cut = cms.string(customisations.generatorTauSelection % customisations.generatorTauPt)
    )
    process.skimGenTauTausFilter = cms.EDFilter("CandViewCountFilter",
        src = cms.InputTag("skimGenTauTaus"),
        minNumber = cms.uint32(1)
    )
    process.skimGenTauTausCount = cms.EDProducer("EventCountProducer")

    process.eventPreSelection += (
        process.skimGenTauTausCountAll +
        process.skimGenTauTaus +
        process.skimGenTauTausFilter +
        process.skimGenTauTausCount
    )

def getCountersPrepend():
    return [
        "skimGenTauTausCountAll",
        "skimGenTauTausCount"
        ]



