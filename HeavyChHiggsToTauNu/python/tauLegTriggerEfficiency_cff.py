# Generated on Wed Jun 20 15:47:00 2012
# by HiggsAnalysis/TriggerEfficiency/test/plotTauEfficiency.py

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
        # L1_SingleTauJet52 OR L1_SingleJet68 + HLT_IsoPFTau35_Trk20_MET45 (Run2011A)
        runs_160404_167913 = cms.PSet(
            firstRun = cms.uint32(160404),
            lastRun = cms.uint32(167913),
            luminosity = cms.double(1197), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0121028744327, 0.00591448641849),
                triggerBin(30.0, 0.120649651972, 0.0177887502724),
                triggerBin(40.0, 0.523076923077, 0.0476461275869),
                triggerBin(50.0, 0.875, 0.141688278764),
                triggerBin(60.0, 0.833333333333, 0.179009937646),
                triggerBin(80.0, 1.0, 0.231260479746),
            ),
        ),
        # L1_Jet52_Central + HLT_IsoPFTau35_Trk20_MET60 (Run2011A)
        runs_170826_173198 = cms.PSet(
            firstRun = cms.uint32(170826),
            lastRun = cms.uint32(173198),
            luminosity = cms.double(870.119), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0, 0.00840949412431),
                triggerBin(30.0, 0.15625, 0.0341454601593),
                triggerBin(40.0, 0.558139534884, 0.0877457601959),
                triggerBin(50.0, 0.75, 0.239566802733),
                triggerBin(60.0, 1.0, 0.26422943474),
                triggerBin(80.0, 0.333333333333, 0.414534706285),
            ),
        ),
        # L1_Jet52_Central + HLT_MediumIsoPFTau35_Trk20_MET60 (Run2011A)
        runs_173236_173692 = cms.PSet(
            firstRun = cms.uint32(173236),
            lastRun = cms.uint32(173692),
            luminosity = cms.double(265.715), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0, 0.0249041202257),
                triggerBin(30.0, 0.136363636364, 0.0725604176231),
                triggerBin(40.0, 0.5, 0.161982400205),
                triggerBin(50.0, 1.0, 0.458641675296),
                triggerBin(60.0, 1.0, 0.36887757085),
            ),
        ),
        # L1_Jet52_Central + HLT_MediumIsoPFTau35_Trk20_MET60 (Run2011B)
        runs_175860_180252 = cms.PSet(
            firstRun = cms.uint32(175860),
            lastRun = cms.uint32(180252),
            luminosity = cms.double(2762), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.041095890411, 0.0237396611301),
                triggerBin(30.0, 0.238095238095, 0.0374385181485),
                triggerBin(40.0, 0.63768115942, 0.0668315065259),
                triggerBin(50.0, 0.833333333333, 0.179009937646),
                triggerBin(60.0, 1.0, 0.231260479746),
                triggerBin(80.0, 1.0, 0.601684479424),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Fall11= cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0271959987496, 0.00318993292808),
                triggerBin(30.0, 0.201376936317, 0.00771691293665),
                triggerBin(40.0, 0.627541589649, 0.0152743156218),
                triggerBin(50.0, 0.883495145631, 0.0268221704259),
                triggerBin(60.0, 0.954022988506, 0.0348613472767),
                triggerBin(80.0, 1.0, 0.0709947284972),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Fall11"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)
