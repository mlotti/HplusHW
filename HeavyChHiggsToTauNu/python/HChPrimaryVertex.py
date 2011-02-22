import FWCore.ParameterSet.Config as cms


def addPrimaryVertexSelection(process, sequence):
    process.firstPrimaryVertex = cms.EDProducer("HPlusSelectFirstVertex",
        src = cms.InputTag("offlinePrimaryVertices")
    )
    sequence *= process.firstPrimaryVertex

    import HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex_cfi as pv
    process.selectedPrimaryVertex = pv.goodPrimaryVertices.clone(
        src = cms.InputTag("firstPrimaryVertex")
    )
    sequence *= process.selectedPrimaryVertex
