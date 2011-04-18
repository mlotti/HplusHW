import FWCore.ParameterSet.Config as cms

# The numbers are FAKE!
HLT_SingleIsoTau20_Trk15_MET25_v4 = cms.PSet(
    fakeTauParameters = cms.vdouble([0.9,5.0,0.3]),
    trueTauParameters = cms.vdouble([0.98,5.0,0.3]),
    metParameters = cms.vdouble([0.78,30.,0.5]),
)

# The numbers are FAKE!
HLT_SingleIsoPFTau35_Trk20_MET45 = cms.PSet(
    fakeTauParameters = cms.vdouble([0.54638, 41.6775, 0.399794]),
    trueTauParameters = cms.vdouble([1, 47.1341, 0.700911]),
    metParameters = cms.vdouble([1, 75.0429, 1.03602]),
)

