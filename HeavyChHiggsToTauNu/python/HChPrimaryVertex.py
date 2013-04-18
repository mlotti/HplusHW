import FWCore.ParameterSet.Config as cms


def addPrimaryVertexSelection(process, sequence, srcProcess="", postfix="", filter=False):
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

    ret = []
    if filter:
        m = cms.EDProducer("EventCountProducer")
        name = "primaryVertexAllEvents"+postfix
        setattr(process, name, m)
        sequence *= m
        ret.append(name)

        m = cms.EDFilter("VertexCountFilter",
            src = cms.InputTag("selectedPrimaryVertex"+postfix),
            minNumber = cms.uint32(1),
            maxNumber = cms.uint32(999)
        )
        setattr(process, "selectedPrimaryVertexFilter"+postfix, m)
        sequence *= m

        m = cms.EDProducer("EventCountProducer")
        name = "primaryVertexSelected"+postfix
        setattr(process, name, m)
        sequence *= m
        ret.append(name)

    return ret

