import FWCore.ParameterSet.Config as cms

topPtWeight = cms.EDProducer("HPlusTopPtWeightProducer",
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopPtReweighting#Eventweight
    TopPtCombined = cms.PSet(
        a = cms.double(0.199),
        b = cms.double(-0.00166)
    ),
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopPtReweighting#Eventweight
    TopPtSeparate = cms.PSet(
        ljets_a = cms.double(0.174),
        ljets_b = cms.double(-0.00137),
        dilepton_a = cms.double(0.222),
        dilepton_b = cms.double(-0.00197),
    ),
    # https://indico.cern.ch/getFile.py/access?contribId=19&sessionId=2&resId=0&materialId=slides&confId=267832, AN-2013-145
    TTH = cms.PSet(
        a = cms.double(1.18246),
        b = cms.double(2.10061e-6),
        c = cms.double(463.312),
        constant = cms.double(0.732),
    ),
    mode = cms.string("TopPtCombined"),

    ttGenEventSrc = cms.InputTag("genEvt"),
    alias = cms.string("topPtWeight"),
    enabled = cms.bool(False),
    variationEnabled = cms.bool(False),
    variationDirection = cms.int32(0),
)
