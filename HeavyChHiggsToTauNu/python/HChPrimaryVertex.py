import FWCore.ParameterSet.Config as cms


def addPrimaryVertexSelection(process, sequence, srcProcess="", postfix=""):
    m = cms.EDProducer("HPlusFirstVertexSelector",
        src = cms.InputTag("offlinePrimaryVertices", "", srcProcess)
    )
    setattr(process, "firstPrimaryVertex"+postfix, m)
    sequence *= m

    import HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex_cfi as pv
    m = pv.goodPrimaryVertices.clone(
        src = cms.InputTag("firstPrimaryVertex"+postfix)
    )
    setattr(process, "selectedPrimaryVertex"+postfix, m)
    sequence *= m

    m = pv.goodPrimaryVertices.clone()
    setattr(process, "goodPrimaryVertices"+postfix, m)
    sequence *= m

#    process.selectedPrimaryVertexFilter = cms.EDFilter("VertexCountFilter",
#                                                       src = cms.InputTag("selectedPrimaryVertex"),
#                                                       minNumber = cms.uint32(1),
#                                                       maxNumber = cms.uint32(999)
#                                                       )
#    sequence *= process.selectedPrimaryVertexFilter
    
