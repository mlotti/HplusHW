# Generated on Wed Jun 20 15:47:00 2012
# by HiggsAnalysis/TriggerEfficiency/test/plotTauEfficiency.py

import FWCore.ParameterSet.Config as cms

def triggerBin(pt, efficiency, uncertainty):
    return cms.PSet(
        pt = cms.double(pt),
        efficiency = cms.double(efficiency),
        uncertainty = cms.double(uncertainty)
    )

tauLegEfficiency_byVLooseCombinedIsolationDeltaBetaCorr_againstElectronMedium = cms.untracked.PSet(
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
                triggerBin(80.0, 1.0, 0.36887757085), # Copied the previous bin numbers
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

tauLegEfficiency_byMediumCombinedIsolationDeltaBetaCorr_againstElectronMedium = cms.untracked.PSet(
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
                triggerBin(80.0, 1.0, 0.36887757085), # Copied the previous bin numbers
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

tauLegEfficiency_byLooseCombinedIsolationDeltaBetaCorr_againstElectronMedium = cms.untracked.PSet(
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
                triggerBin(80.0, 1.0, 0.36887757085), # Copied the previous bin numbers
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

tauLegEfficiency_byLooseCombinedIsolationDeltaBetaCorr_againstElectronMVA = cms.untracked.PSet(
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
                triggerBin(20.0, 0.0142348754448, 0.00694517561518),
                triggerBin(30.0, 0.119363395225, 0.019106704754),
                triggerBin(40.0, 0.575221238938, 0.0514078196324),
                triggerBin(50.0, 0.875, 0.141688278764),
                triggerBin(60.0, 0.875, 0.23225032014),
                triggerBin(80.0, 1.0, 0.308024223477),
            ),
        ),
        # L1_Jet52_Central + HLT_IsoPFTau35_Trk20_MET60 (Run2011A)
        runs_170826_173198 = cms.PSet(
            firstRun = cms.uint32(170826),
            lastRun = cms.uint32(173198),
            luminosity = cms.double(870.119), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0, 0.010175770947),
                triggerBin(30.0, 0.163120567376, 0.0372344233293),
                triggerBin(40.0, 0.552631578947, 0.0939923284761),
                triggerBin(50.0, 0.714285714286, 0.259937875571),
                triggerBin(60.0, 1.0, 0.308024223477),
                triggerBin(80.0, 0.5, 0.41724846474),
            ),
        ),
        # L1_Jet52_Central + HLT_MediumIsoPFTau35_Trk20_MET60 (Run2011A)
        runs_173236_173692 = cms.PSet(
            firstRun = cms.uint32(173236),
            lastRun = cms.uint32(173692),
            luminosity = cms.double(265.715), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0, 0.0292573651783),
                triggerBin(30.0, 0.142857142857, 0.0755708996607),
                triggerBin(40.0, 0.5, 0.176478356266),
                triggerBin(50.0, 1.0, 0.458641675296),
                triggerBin(60.0, 1.0, 0.36887757085),
                triggerBin(80.0, 1.0, 0.36887757085), # Copied the previous bin numbers
            ),
        ),
        # L1_Jet52_Central + HLT_MediumIsoPFTau35_Trk20_MET60 (Run2011B)
        runs_175860_180252 = cms.PSet(
            firstRun = cms.uint32(175860),
            lastRun = cms.uint32(180252),
            luminosity = cms.double(2762), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0307692307692, 0.0236599606596),
                triggerBin(30.0, 0.258278145695, 0.0405552109037),
                triggerBin(40.0, 0.645161290323, 0.0708590062758),
                triggerBin(50.0, 0.818181818182, 0.1914016948),
                triggerBin(60.0, 1.0, 0.26422943474),
                triggerBin(80.0, 1.0, 0.601684479424),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Fall11= cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0269687162891, 0.00343412830059),
                triggerBin(30.0, 0.206305955625, 0.00829425556335),
                triggerBin(40.0, 0.642781875659, 0.0162288861525),
                triggerBin(50.0, 0.918604651163, 0.0265329784454),
                triggerBin(60.0, 0.971830985915, 0.0359480441867),
                triggerBin(80.0, 1.0, 0.0972223406286),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Fall11"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

tauLegEfficiency_byMediumCombinedIsolationDeltaBetaCorr_againstElectronMVA = cms.untracked.PSet(
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
                triggerBin(20.0, 0.0142348754448, 0.00694517561518),
                triggerBin(30.0, 0.119363395225, 0.019106704754),
                triggerBin(40.0, 0.575221238938, 0.0514078196324),
                triggerBin(50.0, 0.875, 0.141688278764),
                triggerBin(60.0, 0.875, 0.23225032014),
                triggerBin(80.0, 1.0, 0.308024223477),
            ),
        ),
        # L1_Jet52_Central + HLT_IsoPFTau35_Trk20_MET60 (Run2011A)
        runs_170826_173198 = cms.PSet(
            firstRun = cms.uint32(170826),
            lastRun = cms.uint32(173198),
            luminosity = cms.double(870.119), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0, 0.010175770947),
                triggerBin(30.0, 0.163120567376, 0.0372344233293),
                triggerBin(40.0, 0.552631578947, 0.0939923284761),
                triggerBin(50.0, 0.714285714286, 0.259937875571),
                triggerBin(60.0, 1.0, 0.308024223477),
                triggerBin(80.0, 0.5, 0.41724846474),
            ),
        ),
        # L1_Jet52_Central + HLT_MediumIsoPFTau35_Trk20_MET60 (Run2011A)
        runs_173236_173692 = cms.PSet(
            firstRun = cms.uint32(173236),
            lastRun = cms.uint32(173692),
            luminosity = cms.double(265.715), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0, 0.0292573651783),
                triggerBin(30.0, 0.142857142857, 0.0755708996607),
                triggerBin(40.0, 0.5, 0.176478356266),
                triggerBin(50.0, 1.0, 0.458641675296),
                triggerBin(60.0, 1.0, 0.36887757085),
                triggerBin(80.0, 1.0, 0.36887757085), # Copied the previous bin numbers
            ),
        ),
        # L1_Jet52_Central + HLT_MediumIsoPFTau35_Trk20_MET60 (Run2011B)
        runs_175860_180252 = cms.PSet(
            firstRun = cms.uint32(175860),
            lastRun = cms.uint32(180252),
            luminosity = cms.double(2762), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0307692307692, 0.0236599606596),
                triggerBin(30.0, 0.258278145695, 0.0405552109037),
                triggerBin(40.0, 0.645161290323, 0.0708590062758),
                triggerBin(50.0, 0.818181818182, 0.1914016948),
                triggerBin(60.0, 1.0, 0.26422943474),
                triggerBin(80.0, 1.0, 0.601684479424),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Fall11= cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0269687162891, 0.00343412830059),
                triggerBin(30.0, 0.206305955625, 0.00829425556335),
                triggerBin(40.0, 0.642781875659, 0.0162288861525),
                triggerBin(50.0, 0.918604651163, 0.0265329784454),
                triggerBin(60.0, 0.971830985915, 0.0359480441867),
                triggerBin(80.0, 1.0, 0.0972223406286),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Fall11"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

tauLegEfficiency = tauLegEfficiency_byMediumCombinedIsolationDeltaBetaCorr_againstElectronMedium
