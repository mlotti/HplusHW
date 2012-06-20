# the original one
import FWCore.ParameterSet.Config as cms

def triggerBin(pt, efficiency, uncertainty):
    return cms.PSet(
        pt = cms.double(pt),
        efficiency = cms.double(efficiency),
        uncertainty = cms.double(uncertainty)
    )

tauLegEfficiency = cms.untracked.PSet(
    # The selected triggers for the efficiency. If one trigger is
    # given, the parametrization of it is used as it is (i.e.
    # luminosity below is ignored). If multiple triggers are given,
    # their parametrizations are used weighted by the luminosities
    # given below.
    # selectTriggers = cms.VPSet(
    #     cms.PSet(
    #         trigger = cms.string("HLT_IsoPFTau35_Trk20_EPS"),
    #         luminosity = cms.double(0)
    #     ),
    # ),
    # The parameters of the trigger efficiency parametrizations,
    # looked dynamically from TriggerEfficiency_cff.py
    dataParameters = cms.PSet(
        # L1_SingleTauJet52 OR L1_SingleJet68 + HLT_IsoPFTau35_Trk20
        runs_160431_167913 = cms.PSet(
            firstRun = cms.uint32(160431),
            lastRun = cms.uint32(167913),
            luminosity = cms.double(1145.897000), # 1/pb
            bins = cms.VPSet(
                triggerBin(40, 0.515873,  0.04844569),
                triggerBin(50, 0.8571429, 0.1583514),
                triggerBin(60, 0.8571429, 0.2572427),
                triggerBin(80, 0.8571429, 0.2572427)
            ),
        ),
        # L1_Jet52_Central + HLT_IsoPFTau35_Trk20_MET60
        runs_170722_173198 = cms.PSet(
            firstRun = cms.uint32(170722),
            lastRun = cms.uint32(173198),
            luminosity = cms.double(780.396000), # 1/pb
            bins = cms.VPSet(
                triggerBin(40, 0.666667, 0.101509),
                triggerBin(50, 1,        0.369032),
                triggerBin(60, 1,        0.369032),
                triggerBin(80, 1,        0.8415)
            ),
        ),
        # L1_Jet52_Central + HLT_MediumIsoPFTau35_Trk20_MET60 (Run2011A)
        runs_173236_173692 = cms.PSet(
            firstRun = cms.uint32(173236),
            lastRun = cms.uint32(173692),
            luminosity = cms.double(246.527000), # 1/pb
            bins = cms.VPSet(
                triggerBin(40, 0.6, 0.204692),
                triggerBin(50, 1,   0.458818),
                triggerBin(60, 1,   0.369032),
                triggerBin(80, 1,   0.8415)
            ),
        ),
        # L1_Jet52_Central + HLT_MediumIsoPFTau35_Trk20_MET60 (Run2011B)
        runs_175860_180252 = cms.PSet(
        ),
    ),
    mcParameters = cms.PSet(
        Summer11 = cms.PSet(
            bins = cms.VPSet(
                triggerBin(40, 0.6168224, 0.03608822),
                triggerBin(50, 0.8809524, 0.07255525),
                triggerBin(60, 0.8125,    0.1494758),
                triggerBin(80, 1,         0.1682306)
            ),
        ),
        # Placeholder until efficiencies have been measured
        Fall11 = cms.PSet(
        ), 
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer11"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)
