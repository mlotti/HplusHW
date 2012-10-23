# Generated on Tue Oct 23 09:54:59 2012
# by HiggsAnalysis/TriggerEfficiency/test/plotTauEfficiency.py

import FWCore.ParameterSet.Config as cms

def triggerBin(pt, efficiency, uncertainty):
    return cms.PSet(
        pt = cms.double(pt),
        efficiency = cms.double(efficiency),
        uncertainty = cms.double(uncertainty)
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

    # Offline selection: PFTauPt > 20 && abs(PFTauEta) < 2.1&& 1/PFTauInvPt > 20&& PFTauProng == 1&& againstMuonTight > 0.5&& MuonTauInvMass < 80&& againstElectronMedium > 0.5&& byMediumCombinedIsolationDeltaBetaCorr > 0.5

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
        runs_170722_173198 = cms.PSet(
            firstRun = cms.uint32(170722),
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
                triggerBin(80.0, 1.0, 0.36887757085), # duplicated bin
            ),
        ),
        # L1_Jet52_Central + HLT_MediumIsoPFTau35_Trk20_MET60 (Run2011B)
        runs_175832_180252 = cms.PSet(
            firstRun = cms.uint32(175832),
            lastRun = cms.uint32(180252),
            luminosity = cms.double(2762), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0434782608696, 0.0226336219951),
                triggerBin(30.0, 0.219251336898, 0.0344868290637),
                triggerBin(40.0, 0.602564102564, 0.0628459275953),
                triggerBin(50.0, 0.846153846154, 0.16803608658),
                triggerBin(60.0, 1.0, 0.205567857429),
                triggerBin(80.0, 1.0, 0.841344746068),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Fall11_PU_2011AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0265151515152, 0.00303527373676),
                triggerBin(30.0, 0.210711994869, 0.00755771530121),
                triggerBin(40.0, 0.628378378378, 0.0145717360692),
                triggerBin(50.0, 0.884773662551, 0.0242677050137),
                triggerBin(60.0, 0.945652173913, 0.0350930146518),
                triggerBin(80.0, 1.0, 0.0595223440639),
            ),
        ),
        Fall11_PU_2011A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0284237726098, 0.00265336632312),
                triggerBin(30.0, 0.208799048751, 0.00645687976437),
                triggerBin(40.0, 0.61118251928, 0.0127487312099),
                triggerBin(50.0, 0.897832817337, 0.0197409075766),
                triggerBin(60.0, 0.935483870968, 0.0302785222487),
                triggerBin(80.0, 1.0, 0.0461088219835),
            ),
        ),
        Fall11_PU_2011B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0233224222586, 0.00346898106523),
                triggerBin(30.0, 0.2138054684, 0.00903435550701),
                triggerBin(40.0, 0.653802497162, 0.0167677178942),
                triggerBin(50.0, 0.865168539326, 0.0306427598316),
                triggerBin(60.0, 0.969696969697, 0.0385739244524),
                triggerBin(80.0, 1.0, 0.0802770559325),
            ),
        ),
        Fall11_PU_2011A_RR1 = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0295683027794, 0.00257436085358),
                triggerBin(30.0, 0.21243748641, 0.00620341657711),
                triggerBin(40.0, 0.609181871689, 0.0121941985103),
                triggerBin(50.0, 0.901408450704, 0.0184601766587),
                triggerBin(60.0, 0.942446043165, 0.027159470536),
                triggerBin(80.0, 1.0, 0.0461088219835),
            ),
        ),
        Fall11_PU_2011A_RR2 = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0272373540856, 0.00269155026795),
                triggerBin(30.0, 0.205160637491, 0.00662475769456),
                triggerBin(40.0, 0.611225188227, 0.0131692805333),
                triggerBin(50.0, 0.893687707641, 0.0208513955068),
                triggerBin(60.0, 0.930434782609, 0.032517962587),
                triggerBin(80.0, 1.0, 0.0461088219835),
            ),
        ),
        Fall11_PU_2011A_RR3 = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0247566063978, 0.00287170998078),
                triggerBin(30.0, 0.198767334361, 0.00725380626745),
                triggerBin(40.0, 0.624691358025, 0.0144025029502),
                triggerBin(50.0, 0.880478087649, 0.0241151722443),
                triggerBin(60.0, 0.931034482759, 0.0389211715295),
                triggerBin(80.0, 1.0, 0.047293062182),
            ),
        ),
        Fall11_PU_Unweighted = cms.PSet(
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
    mcSelect = cms.string("Fall11_PU_2011AB"),
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

    # Offline selection: PFTauPt > 20 && abs(PFTauEta) < 2.1&& 1/PFTauInvPt > 20&& PFTauProng == 1&& againstMuonTight > 0.5&& MuonTauInvMass < 80&& againstElectronMVA > 0.5&& byMediumCombinedIsolationDeltaBetaCorr > 0.5

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
        runs_170722_173198 = cms.PSet(
            firstRun = cms.uint32(170722),
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
                triggerBin(80.0, 1.0, 0.36887757085), # duplicated bin
            ),
        ),
        # L1_Jet52_Central + HLT_MediumIsoPFTau35_Trk20_MET60 (Run2011B)
        runs_175832_180252 = cms.PSet(
            firstRun = cms.uint32(175832),
            lastRun = cms.uint32(180252),
            luminosity = cms.double(2762), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0281690140845, 0.021712186533),
                triggerBin(30.0, 0.238095238095, 0.0374385181485),
                triggerBin(40.0, 0.617647058824, 0.067684108642),
                triggerBin(50.0, 0.833333333333, 0.179009937646),
                triggerBin(60.0, 1.0, 0.231260479746),
                triggerBin(80.0, 1.0, 0.841344746068),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Fall11_PU_2011AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0262449528937, 0.00327149710854),
                triggerBin(30.0, 0.216393442623, 0.00814638269129),
                triggerBin(40.0, 0.644913627639, 0.0154408242279),
                triggerBin(50.0, 0.916256157635, 0.0242177873236),
                triggerBin(60.0, 0.986666666667, 0.0299911821772),
                triggerBin(80.0, 1.0, 0.0879414416486),
            ),
        ),
        Fall11_PU_2011A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0282217782218, 0.00286686989346),
                triggerBin(30.0, 0.218181818182, 0.0070166739555),
                triggerBin(40.0, 0.63226744186, 0.0134563059408),
                triggerBin(50.0, 0.919117647059, 0.0200882676051),
                triggerBin(60.0, 0.961904761905, 0.0290965667789),
                triggerBin(80.0, 1.0, 0.0636357975793),
            ),
        ),
        Fall11_PU_2011B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0229938995777, 0.00372570512537),
                triggerBin(30.0, 0.213852376138, 0.00961892175756),
                triggerBin(40.0, 0.663636363636, 0.0178852234547),
                triggerBin(50.0, 0.91156462585, 0.0300155149441),
                triggerBin(60.0, 1.0, 0.0354546838235),
                triggerBin(80.0, 1.0, 0.132046423994),
            ),
        ),
        Fall11_PU_2011A_RR1 = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.030004580852, 0.00280999135399),
                triggerBin(30.0, 0.224869694713, 0.00677045400563),
                triggerBin(40.0, 0.633643617021, 0.0128431919663),
                triggerBin(50.0, 0.918918918919, 0.0191260372673),
                triggerBin(60.0, 0.957627118644, 0.0276478289972),
                triggerBin(80.0, 1.0, 0.0615104004414),
            ),
        ),
        Fall11_PU_2011A_RR2 = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0270127118644, 0.00290382923081),
                triggerBin(30.0, 0.211832611833, 0.00716997920385),
                triggerBin(40.0, 0.629457364341, 0.013931972476),
                triggerBin(50.0, 0.918287937743, 0.0208506462173),
                triggerBin(60.0, 0.969072164948, 0.02917029971),
                triggerBin(80.0, 1.0, 0.0636357975793),
            ),
        ),
        Fall11_PU_2011A_RR3 = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0231511254019, 0.00302225185297),
                triggerBin(30.0, 0.199579095054, 0.00776777054465),
                triggerBin(40.0, 0.636279069767, 0.0152614224016),
                triggerBin(50.0, 0.924882629108, 0.0226727049488),
                triggerBin(60.0, 0.986111111111, 0.031212006865),
                triggerBin(80.0, 1.0, 0.0683597389517),
            ),
        ),
        Fall11_PU_Unweighted = cms.PSet(
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
    mcSelect = cms.string("Fall11_PU_2011AB"),
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

    # Offline selection: PFTauPt > 20 && abs(PFTauEta) < 2.1&& 1/PFTauInvPt > 20&& PFTauProng == 1&& againstMuonTight > 0.5&& MuonTauInvMass < 80&& againstElectronMVA > 0.5&& byLooseCombinedIsolationDeltaBetaCorr > 0.5

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
        runs_170722_173198 = cms.PSet(
            firstRun = cms.uint32(170722),
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
                triggerBin(80.0, 1.0, 0.36887757085), # duplicated bin
            ),
        ),
        # L1_Jet52_Central + HLT_MediumIsoPFTau35_Trk20_MET60 (Run2011B)
        runs_175832_180252 = cms.PSet(
            firstRun = cms.uint32(175832),
            lastRun = cms.uint32(180252),
            luminosity = cms.double(2762), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0281690140845, 0.021712186533),
                triggerBin(30.0, 0.238095238095, 0.0374385181485),
                triggerBin(40.0, 0.617647058824, 0.067684108642),
                triggerBin(50.0, 0.833333333333, 0.179009937646),
                triggerBin(60.0, 1.0, 0.231260479746),
                triggerBin(80.0, 1.0, 0.841344746068),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Fall11_PU_2011AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0262449528937, 0.00327149710854),
                triggerBin(30.0, 0.216393442623, 0.00814638269129),
                triggerBin(40.0, 0.644913627639, 0.0154408242279),
                triggerBin(50.0, 0.916256157635, 0.0242177873236),
                triggerBin(60.0, 0.986666666667, 0.0299911821772),
                triggerBin(80.0, 1.0, 0.0879414416486),
            ),
        ),
        Fall11_PU_2011A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0282217782218, 0.00286686989346),
                triggerBin(30.0, 0.218181818182, 0.0070166739555),
                triggerBin(40.0, 0.63226744186, 0.0134563059408),
                triggerBin(50.0, 0.919117647059, 0.0200882676051),
                triggerBin(60.0, 0.961904761905, 0.0290965667789),
                triggerBin(80.0, 1.0, 0.0636357975793),
            ),
        ),
        Fall11_PU_2011B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0229938995777, 0.00372570512537),
                triggerBin(30.0, 0.213852376138, 0.00961892175756),
                triggerBin(40.0, 0.663636363636, 0.0178852234547),
                triggerBin(50.0, 0.91156462585, 0.0300155149441),
                triggerBin(60.0, 1.0, 0.0354546838235),
                triggerBin(80.0, 1.0, 0.132046423994),
            ),
        ),
        Fall11_PU_2011A_RR1 = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.030004580852, 0.00280999135399),
                triggerBin(30.0, 0.224869694713, 0.00677045400563),
                triggerBin(40.0, 0.633643617021, 0.0128431919663),
                triggerBin(50.0, 0.918918918919, 0.0191260372673),
                triggerBin(60.0, 0.957627118644, 0.0276478289972),
                triggerBin(80.0, 1.0, 0.0615104004414),
            ),
        ),
        Fall11_PU_2011A_RR2 = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0270127118644, 0.00290382923081),
                triggerBin(30.0, 0.211832611833, 0.00716997920385),
                triggerBin(40.0, 0.629457364341, 0.013931972476),
                triggerBin(50.0, 0.918287937743, 0.0208506462173),
                triggerBin(60.0, 0.969072164948, 0.02917029971),
                triggerBin(80.0, 1.0, 0.0636357975793),
            ),
        ),
        Fall11_PU_2011A_RR3 = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0231511254019, 0.00302225185297),
                triggerBin(30.0, 0.199579095054, 0.00776777054465),
                triggerBin(40.0, 0.636279069767, 0.0152614224016),
                triggerBin(50.0, 0.924882629108, 0.0226727049488),
                triggerBin(60.0, 0.986111111111, 0.031212006865),
                triggerBin(80.0, 1.0, 0.0683597389517),
            ),
        ),
        Fall11_PU_Unweighted = cms.PSet(
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
    mcSelect = cms.string("Fall11_PU_2011AB"),
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

    # Offline selection: PFTauPt > 20 && abs(PFTauEta) < 2.1&& 1/PFTauInvPt > 20&& PFTauProng == 1&& againstMuonTight > 0.5&& MuonTauInvMass < 80&& againstElectronMedium > 0.5&& byLooseCombinedIsolationDeltaBetaCorr > 0.5

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
        runs_170722_173198 = cms.PSet(
            firstRun = cms.uint32(170722),
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
                triggerBin(80.0, 1.0, 0.36887757085), # duplicated bin
            ),
        ),
        # L1_Jet52_Central + HLT_MediumIsoPFTau35_Trk20_MET60 (Run2011B)
        runs_175832_180252 = cms.PSet(
            firstRun = cms.uint32(175832),
            lastRun = cms.uint32(180252),
            luminosity = cms.double(2762), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0434782608696, 0.0226336219951),
                triggerBin(30.0, 0.219251336898, 0.0344868290637),
                triggerBin(40.0, 0.602564102564, 0.0628459275953),
                triggerBin(50.0, 0.846153846154, 0.16803608658),
                triggerBin(60.0, 1.0, 0.205567857429),
                triggerBin(80.0, 1.0, 0.841344746068),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Fall11_PU_2011AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0265151515152, 0.00303527373676),
                triggerBin(30.0, 0.210711994869, 0.00755771530121),
                triggerBin(40.0, 0.628378378378, 0.0145717360692),
                triggerBin(50.0, 0.884773662551, 0.0242677050137),
                triggerBin(60.0, 0.945652173913, 0.0350930146518),
                triggerBin(80.0, 1.0, 0.0595223440639),
            ),
        ),
        Fall11_PU_2011A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0284237726098, 0.00265336632312),
                triggerBin(30.0, 0.208799048751, 0.00645687976437),
                triggerBin(40.0, 0.61118251928, 0.0127487312099),
                triggerBin(50.0, 0.897832817337, 0.0197409075766),
                triggerBin(60.0, 0.935483870968, 0.0302785222487),
                triggerBin(80.0, 1.0, 0.0461088219835),
            ),
        ),
        Fall11_PU_2011B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0233224222586, 0.00346898106523),
                triggerBin(30.0, 0.2138054684, 0.00903435550701),
                triggerBin(40.0, 0.653802497162, 0.0167677178942),
                triggerBin(50.0, 0.865168539326, 0.0306427598316),
                triggerBin(60.0, 0.969696969697, 0.0385739244524),
                triggerBin(80.0, 1.0, 0.0802770559325),
            ),
        ),
        Fall11_PU_2011A_RR1 = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0295683027794, 0.00257436085358),
                triggerBin(30.0, 0.21243748641, 0.00620341657711),
                triggerBin(40.0, 0.609181871689, 0.0121941985103),
                triggerBin(50.0, 0.901408450704, 0.0184601766587),
                triggerBin(60.0, 0.942446043165, 0.027159470536),
                triggerBin(80.0, 1.0, 0.0461088219835),
            ),
        ),
        Fall11_PU_2011A_RR2 = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0272373540856, 0.00269155026795),
                triggerBin(30.0, 0.205160637491, 0.00662475769456),
                triggerBin(40.0, 0.611225188227, 0.0131692805333),
                triggerBin(50.0, 0.893687707641, 0.0208513955068),
                triggerBin(60.0, 0.930434782609, 0.032517962587),
                triggerBin(80.0, 1.0, 0.0461088219835),
            ),
        ),
        Fall11_PU_2011A_RR3 = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0247566063978, 0.00287170998078),
                triggerBin(30.0, 0.198767334361, 0.00725380626745),
                triggerBin(40.0, 0.624691358025, 0.0144025029502),
                triggerBin(50.0, 0.880478087649, 0.0241151722443),
                triggerBin(60.0, 0.931034482759, 0.0389211715295),
                triggerBin(80.0, 1.0, 0.047293062182),
            ),
        ),
        Fall11_PU_Unweighted = cms.PSet(
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
    mcSelect = cms.string("Fall11_PU_2011AB"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)
