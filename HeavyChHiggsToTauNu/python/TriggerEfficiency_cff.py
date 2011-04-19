import FWCore.ParameterSet.Config as cms

# The numbers are not optimized, fit for testing purposes
HLT_SingleIsoTau20_Trk15_MET20 = cms.PSet(
    # par[0]*(TMath::Freq((sqrt(x)-sqrt(par[1]))/(2*par[2])))
    # par[0]=Plateau, par[1]=x when y = 0.5, par[2]=Width
    fakeTauParameters = cms.vdouble([0.79317,35.6938,0.438781]),
    trueTauParameters = cms.vdouble([0.837177,28.9401,0.384818]),
    metParameters     = cms.vdouble([1,38.6373,1.68053]),
)

# The numbers are not optimized, fit for testing purposes
HLT_SingleIsoTau20_Trk15_MET25 = cms.PSet(
    # par[0]*(TMath::Freq((sqrt(x)-sqrt(par[1]))/(2*par[2])))
    # par[0]=Plateau, par[1]=x when y = 0.5, par[2]=Width
    fakeTauParameters = cms.vdouble([0.79317,35.6938,0.438781]),
    trueTauParameters = cms.vdouble([0.837177,28.9401,0.384818]),
    metParameters     = cms.vdouble([1,51.6482,1.48373]),
)

# The numbers are not optimized, fit for testing purposes
HLT_SingleIsoPFTau35_Trk20_MET45 = cms.PSet(
    # par[0]*(TMath::Freq((sqrt(x)-sqrt(par[1]))/(2*par[2])))
    # par[0]=Plateau, par[1]=x when y = 0.5, par[2]=Width
    fakeTauParameters = cms.vdouble([0.54638,41.6775,0.399794]),
    trueTauParameters = cms.vdouble([1,47.1341,0.700911]),
    metParameters     = cms.vdouble([1,75.0429,1.03602]),
)


