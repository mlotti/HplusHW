# Generated on Wed May 29 18:05:46 2013
# by HiggsAnalysis/TriggerEfficiency/test/PythonWriter.py

import FWCore.ParameterSet.Config as cms

def triggerBin(pt, efficiency, uncertainty):
    return cms.PSet(
        pt = cms.double(pt),
        efficiency = cms.double(efficiency),
        uncertainty = cms.double(uncertainty)
    )

# FIXME, temporary fix for changed met leg naming 3105103/SL
metLegEfficiency = metLegEfficiency_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronMediumMVA3


metLegEfficiency_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronMediumMVA3 = cms.untracked.PSet(
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

    # Offline selection: (Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5) >= 1&&Sum$(PFJetPt > 0&& PFJetPUIDtight) >= 3+Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5 && PFTauJetMinDR < 0.5))&& hPlusGlobalElectronVetoFilter > 0.5 && hPlusGlobalMuonVetoFilter > 0.5

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0833333333333, 0.079785592313),
                triggerBin(30.0, 0.0, 0.0),
                triggerBin(40.0, 0.333333333333, 0.272165526976),
                triggerBin(50.0, 0.5, 0.353553390593),
                triggerBin(60.0, 0.0, 0.0),
                triggerBin(70.0, 1.0, 0.0),
                triggerBin(80.0, 0.0, 1.0),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0300751879699, 0.0148097384742),
                triggerBin(30.0, 0.0752688172043, 0.0273573371576),
                triggerBin(40.0, 0.162790697674, 0.0562985989385),
                triggerBin(50.0, 0.194444444444, 0.0659620687443),
                triggerBin(60.0, 0.363636363636, 0.145040733676),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 0.75, 0.216506350946),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.333333333333, 0.272165526976),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0412371134021, 0.0142757479231),
                triggerBin(30.0, 0.0833333333333, 0.0252304196175),
                triggerBin(40.0, 0.0506329113924, 0.0246672076884),
                triggerBin(50.0, 0.166666666667, 0.062112999375),
                triggerBin(60.0, 0.333333333333, 0.111111111111),
                triggerBin(70.0, 0.5, 0.144337567297),
                triggerBin(80.0, 0.25, 0.216506350946),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.75, 0.216506350946),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.041095890411, 0.0134141985368),
                triggerBin(30.0, 0.0700636942675, 0.0203715133022),
                triggerBin(40.0, 0.10989010989, 0.0327853950395),
                triggerBin(50.0, 0.117647058824, 0.0451155875792),
                triggerBin(60.0, 0.25, 0.0968245836552),
                triggerBin(70.0, 0.142857142857, 0.132260014253),
                triggerBin(80.0, 0.428571428571, 0.187043905917),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0344827586207, 0.0151529439449),
                triggerBin(30.0, 0.07, 0.0255147016443),
                triggerBin(40.0, 0.173913043478, 0.0558856162537),
                triggerBin(50.0, 0.210526315789, 0.066134827625),
                triggerBin(60.0, 0.333333333333, 0.136082763488),
                triggerBin(70.0, 0.666666666667, 0.272165526976),
                triggerBin(80.0, 0.75, 0.216506350946),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.5, 0.25),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0383480825959, 0.0104299188373),
                triggerBin(30.0, 0.0772727272727, 0.0180027337435),
                triggerBin(40.0, 0.096, 0.0263490417283),
                triggerBin(50.0, 0.189189189189, 0.0455294142944),
                triggerBin(60.0, 0.333333333333, 0.0860662965824),
                triggerBin(70.0, 0.533333333333, 0.128812237744),
                triggerBin(80.0, 0.5, 0.176776695297),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.6, 0.219089023002),
                triggerBin(140.0, 0.75, 0.216506350946),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0394265232975, 0.00823839169829),
                triggerBin(30.0, 0.0742705570292, 0.0135045371477),
                triggerBin(40.0, 0.101851851852, 0.0205793464567),
                triggerBin(50.0, 0.16, 0.0327902424511),
                triggerBin(60.0, 0.3, 0.0648074069841),
                triggerBin(70.0, 0.409090909091, 0.104823561107),
                triggerBin(80.0, 0.466666666667, 0.128812237744),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.75, 0.153093108924),
                triggerBin(140.0, 0.75, 0.216506350946),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0976163450624, 0.00447181599647),
                triggerBin(30.0, 0.132600919775, 0.00542091173789),
                triggerBin(40.0, 0.180893682589, 0.00675732002082),
                triggerBin(50.0, 0.227564102564, 0.00839190987544),
                triggerBin(60.0, 0.308406647116, 0.0102102048488),
                triggerBin(70.0, 0.380141010576, 0.01176627614),
                triggerBin(80.0, 0.545869947276, 0.00933455413271),
                triggerBin(100.0, 0.766698024459, 0.00917254286911),
                triggerBin(120.0, 0.894138755981, 0.00752406987026),
                triggerBin(140.0, 0.965034965035, 0.0054309461383),
                triggerBin(160.0, 0.994764397906, 0.0026109391715),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0976163450624, 0.00447181599647),
                triggerBin(30.0, 0.132600919775, 0.00542091173789),
                triggerBin(40.0, 0.180893682589, 0.00675732002082),
                triggerBin(50.0, 0.227564102564, 0.00839190987544),
                triggerBin(60.0, 0.308406647116, 0.0102102048488),
                triggerBin(70.0, 0.380141010576, 0.01176627614),
                triggerBin(80.0, 0.545869947276, 0.00933455413271),
                triggerBin(100.0, 0.766698024459, 0.00917254286911),
                triggerBin(120.0, 0.894138755981, 0.00752406987026),
                triggerBin(140.0, 0.965034965035, 0.0054309461383),
                triggerBin(160.0, 0.994764397906, 0.0026109391715),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0976163450624, 0.00447181599647),
                triggerBin(30.0, 0.132600919775, 0.00542091173789),
                triggerBin(40.0, 0.180893682589, 0.00675732002082),
                triggerBin(50.0, 0.227564102564, 0.00839190987544),
                triggerBin(60.0, 0.308406647116, 0.0102102048488),
                triggerBin(70.0, 0.380141010576, 0.01176627614),
                triggerBin(80.0, 0.545869947276, 0.00933455413271),
                triggerBin(100.0, 0.766698024459, 0.00917254286911),
                triggerBin(120.0, 0.894138755981, 0.00752406987026),
                triggerBin(140.0, 0.965034965035, 0.0054309461383),
                triggerBin(160.0, 0.994764397906, 0.0026109391715),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0976163450624, 0.00447181599647),
                triggerBin(30.0, 0.132600919775, 0.00542091173789),
                triggerBin(40.0, 0.180893682589, 0.00675732002082),
                triggerBin(50.0, 0.227564102564, 0.00839190987544),
                triggerBin(60.0, 0.308406647116, 0.0102102048488),
                triggerBin(70.0, 0.380141010576, 0.01176627614),
                triggerBin(80.0, 0.545869947276, 0.00933455413271),
                triggerBin(100.0, 0.766698024459, 0.00917254286911),
                triggerBin(120.0, 0.894138755981, 0.00752406987026),
                triggerBin(140.0, 0.965034965035, 0.0054309461383),
                triggerBin(160.0, 0.994764397906, 0.0026109391715),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0976163450624, 0.00447181599647),
                triggerBin(30.0, 0.132600919775, 0.00542091173789),
                triggerBin(40.0, 0.180893682589, 0.00675732002082),
                triggerBin(50.0, 0.227564102564, 0.00839190987544),
                triggerBin(60.0, 0.308406647116, 0.0102102048488),
                triggerBin(70.0, 0.380141010576, 0.01176627614),
                triggerBin(80.0, 0.545869947276, 0.00933455413271),
                triggerBin(100.0, 0.766698024459, 0.00917254286911),
                triggerBin(120.0, 0.894138755981, 0.00752406987026),
                triggerBin(140.0, 0.965034965035, 0.0054309461383),
                triggerBin(160.0, 0.994764397906, 0.0026109391715),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0976163450624, 0.00447181599647),
                triggerBin(30.0, 0.132600919775, 0.00542091173789),
                triggerBin(40.0, 0.180893682589, 0.00675732002082),
                triggerBin(50.0, 0.227564102564, 0.00839190987544),
                triggerBin(60.0, 0.308406647116, 0.0102102048488),
                triggerBin(70.0, 0.380141010576, 0.01176627614),
                triggerBin(80.0, 0.545869947276, 0.00933455413271),
                triggerBin(100.0, 0.766698024459, 0.00917254286911),
                triggerBin(120.0, 0.894138755981, 0.00752406987026),
                triggerBin(140.0, 0.965034965035, 0.0054309461383),
                triggerBin(160.0, 0.994764397906, 0.0026109391715),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0976163450624, 0.00447181599647),
                triggerBin(30.0, 0.132600919775, 0.00542091173789),
                triggerBin(40.0, 0.180893682589, 0.00675732002082),
                triggerBin(50.0, 0.227564102564, 0.00839190987544),
                triggerBin(60.0, 0.308406647116, 0.0102102048488),
                triggerBin(70.0, 0.380141010576, 0.01176627614),
                triggerBin(80.0, 0.545869947276, 0.00933455413271),
                triggerBin(100.0, 0.766698024459, 0.00917254286911),
                triggerBin(120.0, 0.894138755981, 0.00752406987026),
                triggerBin(140.0, 0.965034965035, 0.0054309461383),
                triggerBin(160.0, 0.994764397906, 0.0026109391715),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0976163450624, 0.00447181599647),
                triggerBin(30.0, 0.132600919775, 0.00542091173789),
                triggerBin(40.0, 0.180893682589, 0.00675732002082),
                triggerBin(50.0, 0.227564102564, 0.00839190987544),
                triggerBin(60.0, 0.308406647116, 0.0102102048488),
                triggerBin(70.0, 0.380141010576, 0.01176627614),
                triggerBin(80.0, 0.545869947276, 0.00933455413271),
                triggerBin(100.0, 0.766698024459, 0.00917254286911),
                triggerBin(120.0, 0.894138755981, 0.00752406987026),
                triggerBin(140.0, 0.965034965035, 0.0054309461383),
                triggerBin(160.0, 0.994764397906, 0.0026109391715),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012A"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

metLegEfficiency_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronMediumMVA3 = cms.untracked.PSet(
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

    # Offline selection: (Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5) >= 1&&Sum$(PFJetPt > 0&& PFJetPUIDtight) >= 3+Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5 && PFTauJetMinDR < 0.5))&& hPlusGlobalElectronVetoFilter > 0.5 && hPlusGlobalMuonVetoFilter > 0.5

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.125, 0.116926793337),
                triggerBin(30.0, 0.0, 0.0),
                triggerBin(40.0, 0.5, 0.353553390593),
                triggerBin(50.0, 0.5, 0.353553390593),
                triggerBin(60.0, 0.0, 1.0),
                triggerBin(70.0, 1.0, 0.0),
                triggerBin(80.0, 0.0, 1.0),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0348837209302, 0.019785726281),
                triggerBin(30.0, 0.125, 0.0441941738242),
                triggerBin(40.0, 0.136363636364, 0.0731650049984),
                triggerBin(50.0, 0.166666666667, 0.0878410461158),
                triggerBin(60.0, 0.25, 0.153093108924),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.333333333333, 0.272165526976),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.051724137931, 0.0205629293764),
                triggerBin(30.0, 0.0757575757576, 0.0325712192794),
                triggerBin(40.0, 0.0681818181818, 0.0379991201606),
                triggerBin(50.0, 0.173913043478, 0.0790341964475),
                triggerBin(60.0, 0.333333333333, 0.136082763488),
                triggerBin(70.0, 0.5, 0.158113883008),
                triggerBin(80.0, 0.333333333333, 0.272165526976),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.03125, 0.0153789216289),
                triggerBin(30.0, 0.0348837209302, 0.019785726281),
                triggerBin(40.0, 0.127659574468, 0.0486766595111),
                triggerBin(50.0, 0.2, 0.08),
                triggerBin(60.0, 0.272727272727, 0.134281626523),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 0.25, 0.216506350946),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0425531914894, 0.0208189810549),
                triggerBin(30.0, 0.116666666667, 0.0414438486701),
                triggerBin(40.0, 0.166666666667, 0.0760725774313),
                triggerBin(50.0, 0.2, 0.0894427191),
                triggerBin(60.0, 0.25, 0.153093108924),
                triggerBin(70.0, 0.666666666667, 0.272165526976),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.5, 0.25),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.047619047619, 0.0146955571392),
                triggerBin(30.0, 0.0952380952381, 0.0261509355888),
                triggerBin(40.0, 0.102941176471, 0.0368511095406),
                triggerBin(50.0, 0.186046511628, 0.0593439339074),
                triggerBin(60.0, 0.3, 0.10246950766),
                triggerBin(70.0, 0.538461538462, 0.138264159119),
                triggerBin(80.0, 0.6, 0.219089023002),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.6, 0.219089023002),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0414201183432, 0.0108383076011),
                triggerBin(30.0, 0.0707547169811, 0.0176106323756),
                triggerBin(40.0, 0.113043478261, 0.0295273860036),
                triggerBin(50.0, 0.191176470588, 0.0476858635609),
                triggerBin(60.0, 0.290322580645, 0.0815248586297),
                triggerBin(70.0, 0.411764705882, 0.119364624987),
                triggerBin(80.0, 0.444444444444, 0.165634665),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.75, 0.153093108924),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0981023988543, 0.00562837417416),
                triggerBin(30.0, 0.127725856698, 0.00658670786463),
                triggerBin(40.0, 0.172568354998, 0.00800012656363),
                triggerBin(50.0, 0.227091633466, 0.00999490546027),
                triggerBin(60.0, 0.302263648469, 0.0118495994101),
                triggerBin(70.0, 0.368924302789, 0.0136203258469),
                triggerBin(80.0, 0.552127162225, 0.0107520562187),
                triggerBin(100.0, 0.764173703257, 0.0104255721179),
                triggerBin(120.0, 0.893893129771, 0.00850900745547),
                triggerBin(140.0, 0.962585034014, 0.00639010416086),
                triggerBin(160.0, 0.993421052632, 0.00327863519121),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0981023988543, 0.00562837417416),
                triggerBin(30.0, 0.127725856698, 0.00658670786463),
                triggerBin(40.0, 0.172568354998, 0.00800012656363),
                triggerBin(50.0, 0.227091633466, 0.00999490546027),
                triggerBin(60.0, 0.302263648469, 0.0118495994101),
                triggerBin(70.0, 0.368924302789, 0.0136203258469),
                triggerBin(80.0, 0.552127162225, 0.0107520562187),
                triggerBin(100.0, 0.764173703257, 0.0104255721179),
                triggerBin(120.0, 0.893893129771, 0.00850900745547),
                triggerBin(140.0, 0.962585034014, 0.00639010416086),
                triggerBin(160.0, 0.993421052632, 0.00327863519121),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0981023988543, 0.00562837417416),
                triggerBin(30.0, 0.127725856698, 0.00658670786463),
                triggerBin(40.0, 0.172568354998, 0.00800012656363),
                triggerBin(50.0, 0.227091633466, 0.00999490546027),
                triggerBin(60.0, 0.302263648469, 0.0118495994101),
                triggerBin(70.0, 0.368924302789, 0.0136203258469),
                triggerBin(80.0, 0.552127162225, 0.0107520562187),
                triggerBin(100.0, 0.764173703257, 0.0104255721179),
                triggerBin(120.0, 0.893893129771, 0.00850900745547),
                triggerBin(140.0, 0.962585034014, 0.00639010416086),
                triggerBin(160.0, 0.993421052632, 0.00327863519121),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0981023988543, 0.00562837417416),
                triggerBin(30.0, 0.127725856698, 0.00658670786463),
                triggerBin(40.0, 0.172568354998, 0.00800012656363),
                triggerBin(50.0, 0.227091633466, 0.00999490546027),
                triggerBin(60.0, 0.302263648469, 0.0118495994101),
                triggerBin(70.0, 0.368924302789, 0.0136203258469),
                triggerBin(80.0, 0.552127162225, 0.0107520562187),
                triggerBin(100.0, 0.764173703257, 0.0104255721179),
                triggerBin(120.0, 0.893893129771, 0.00850900745547),
                triggerBin(140.0, 0.962585034014, 0.00639010416086),
                triggerBin(160.0, 0.993421052632, 0.00327863519121),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0981023988543, 0.00562837417416),
                triggerBin(30.0, 0.127725856698, 0.00658670786463),
                triggerBin(40.0, 0.172568354998, 0.00800012656363),
                triggerBin(50.0, 0.227091633466, 0.00999490546027),
                triggerBin(60.0, 0.302263648469, 0.0118495994101),
                triggerBin(70.0, 0.368924302789, 0.0136203258469),
                triggerBin(80.0, 0.552127162225, 0.0107520562187),
                triggerBin(100.0, 0.764173703257, 0.0104255721179),
                triggerBin(120.0, 0.893893129771, 0.00850900745547),
                triggerBin(140.0, 0.962585034014, 0.00639010416086),
                triggerBin(160.0, 0.993421052632, 0.00327863519121),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0981023988543, 0.00562837417416),
                triggerBin(30.0, 0.127725856698, 0.00658670786463),
                triggerBin(40.0, 0.172568354998, 0.00800012656363),
                triggerBin(50.0, 0.227091633466, 0.00999490546027),
                triggerBin(60.0, 0.302263648469, 0.0118495994101),
                triggerBin(70.0, 0.368924302789, 0.0136203258469),
                triggerBin(80.0, 0.552127162225, 0.0107520562187),
                triggerBin(100.0, 0.764173703257, 0.0104255721179),
                triggerBin(120.0, 0.893893129771, 0.00850900745547),
                triggerBin(140.0, 0.962585034014, 0.00639010416086),
                triggerBin(160.0, 0.993421052632, 0.00327863519121),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0981023988543, 0.00562837417416),
                triggerBin(30.0, 0.127725856698, 0.00658670786463),
                triggerBin(40.0, 0.172568354998, 0.00800012656363),
                triggerBin(50.0, 0.227091633466, 0.00999490546027),
                triggerBin(60.0, 0.302263648469, 0.0118495994101),
                triggerBin(70.0, 0.368924302789, 0.0136203258469),
                triggerBin(80.0, 0.552127162225, 0.0107520562187),
                triggerBin(100.0, 0.764173703257, 0.0104255721179),
                triggerBin(120.0, 0.893893129771, 0.00850900745547),
                triggerBin(140.0, 0.962585034014, 0.00639010416086),
                triggerBin(160.0, 0.993421052632, 0.00327863519121),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0981023988543, 0.00562837417416),
                triggerBin(30.0, 0.127725856698, 0.00658670786463),
                triggerBin(40.0, 0.172568354998, 0.00800012656363),
                triggerBin(50.0, 0.227091633466, 0.00999490546027),
                triggerBin(60.0, 0.302263648469, 0.0118495994101),
                triggerBin(70.0, 0.368924302789, 0.0136203258469),
                triggerBin(80.0, 0.552127162225, 0.0107520562187),
                triggerBin(100.0, 0.764173703257, 0.0104255721179),
                triggerBin(120.0, 0.893893129771, 0.00850900745547),
                triggerBin(140.0, 0.962585034014, 0.00639010416086),
                triggerBin(160.0, 0.993421052632, 0.00327863519121),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012A"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

metLegEfficiency_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronMediumMVA3 = cms.untracked.PSet(
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

    # Offline selection: (Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) >= 1&&Sum$(PFJetPt > 0&& PFJetPUIDtight) >= 3+Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5 && PFTauJetMinDR < 0.5))&& hPlusGlobalElectronVetoFilter > 0.5 && hPlusGlobalMuonVetoFilter > 0.5

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.142857142857, 0.132260014253),
                triggerBin(30.0, 0.0, 0.0),
                triggerBin(40.0, 0.5, 0.353553390593),
                triggerBin(50.0, 0.5, 0.353553390593),
                triggerBin(60.0, 0.0, 1.0),
                triggerBin(70.0, 1.0, 0.0),
                triggerBin(80.0, 0.0, 1.0),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.038961038961, 0.0220516148963),
                triggerBin(30.0, 0.117647058824, 0.0451155875792),
                triggerBin(40.0, 0.166666666667, 0.0878410461158),
                triggerBin(50.0, 0.142857142857, 0.0935219529583),
                triggerBin(60.0, 0.25, 0.153093108924),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0594059405941, 0.0235209775375),
                triggerBin(30.0, 0.0806451612903, 0.0345807888235),
                triggerBin(40.0, 0.0789473684211, 0.043744076724),
                triggerBin(50.0, 0.210526315789, 0.0935287701725),
                triggerBin(60.0, 0.333333333333, 0.136082763488),
                triggerBin(70.0, 0.444444444444, 0.165634665),
                triggerBin(80.0, 0.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0263157894737, 0.0149921817924),
                triggerBin(30.0, 0.038961038961, 0.0220516148963),
                triggerBin(40.0, 0.130434782609, 0.0496556731061),
                triggerBin(50.0, 0.227272727273, 0.0893460673985),
                triggerBin(60.0, 0.3, 0.144913767462),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 0.25, 0.216506350946),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.047619047619, 0.0232357160226),
                triggerBin(30.0, 0.111111111111, 0.0427666866066),
                triggerBin(40.0, 0.2, 0.0894427191),
                triggerBin(50.0, 0.1875, 0.097578093725),
                triggerBin(60.0, 0.25, 0.153093108924),
                triggerBin(70.0, 0.666666666667, 0.272165526976),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.333333333333, 0.272165526976),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0540540540541, 0.0166249914927),
                triggerBin(30.0, 0.0948275862069, 0.0272021986784),
                triggerBin(40.0, 0.120689655172, 0.0427752067866),
                triggerBin(50.0, 0.2, 0.0676123403783),
                triggerBin(60.0, 0.3, 0.10246950766),
                triggerBin(70.0, 0.5, 0.144337567297),
                triggerBin(80.0, 0.5, 0.25),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.5, 0.25),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0434782608696, 0.0117936411784),
                triggerBin(30.0, 0.0725388601036, 0.0186704407255),
                triggerBin(40.0, 0.125, 0.0324296576039),
                triggerBin(50.0, 0.210526315789, 0.0539988606361),
                triggerBin(60.0, 0.3, 0.0836660026534),
                triggerBin(70.0, 0.375, 0.121030729569),
                triggerBin(80.0, 0.375, 0.17116329922),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.714285714286, 0.170746944191),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0944625407166, 0.00590158735886),
                triggerBin(30.0, 0.129933481153, 0.00708049291219),
                triggerBin(40.0, 0.16874687968, 0.00836843110628),
                triggerBin(50.0, 0.227880330999, 0.0105829717345),
                triggerBin(60.0, 0.303230543319, 0.0124549638306),
                triggerBin(70.0, 0.365300784656, 0.014217641993),
                triggerBin(80.0, 0.548830111902, 0.0112226976303),
                triggerBin(100.0, 0.765060240964, 0.0109685893464),
                triggerBin(120.0, 0.889354568315, 0.00908205216497),
                triggerBin(140.0, 0.96125, 0.00682352891655),
                triggerBin(160.0, 0.994652406417, 0.00307916835595),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0944625407166, 0.00590158735886),
                triggerBin(30.0, 0.129933481153, 0.00708049291219),
                triggerBin(40.0, 0.16874687968, 0.00836843110628),
                triggerBin(50.0, 0.227880330999, 0.0105829717345),
                triggerBin(60.0, 0.303230543319, 0.0124549638306),
                triggerBin(70.0, 0.365300784656, 0.014217641993),
                triggerBin(80.0, 0.548830111902, 0.0112226976303),
                triggerBin(100.0, 0.765060240964, 0.0109685893464),
                triggerBin(120.0, 0.889354568315, 0.00908205216497),
                triggerBin(140.0, 0.96125, 0.00682352891655),
                triggerBin(160.0, 0.994652406417, 0.00307916835595),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0944625407166, 0.00590158735886),
                triggerBin(30.0, 0.129933481153, 0.00708049291219),
                triggerBin(40.0, 0.16874687968, 0.00836843110628),
                triggerBin(50.0, 0.227880330999, 0.0105829717345),
                triggerBin(60.0, 0.303230543319, 0.0124549638306),
                triggerBin(70.0, 0.365300784656, 0.014217641993),
                triggerBin(80.0, 0.548830111902, 0.0112226976303),
                triggerBin(100.0, 0.765060240964, 0.0109685893464),
                triggerBin(120.0, 0.889354568315, 0.00908205216497),
                triggerBin(140.0, 0.96125, 0.00682352891655),
                triggerBin(160.0, 0.994652406417, 0.00307916835595),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0944625407166, 0.00590158735886),
                triggerBin(30.0, 0.129933481153, 0.00708049291219),
                triggerBin(40.0, 0.16874687968, 0.00836843110628),
                triggerBin(50.0, 0.227880330999, 0.0105829717345),
                triggerBin(60.0, 0.303230543319, 0.0124549638306),
                triggerBin(70.0, 0.365300784656, 0.014217641993),
                triggerBin(80.0, 0.548830111902, 0.0112226976303),
                triggerBin(100.0, 0.765060240964, 0.0109685893464),
                triggerBin(120.0, 0.889354568315, 0.00908205216497),
                triggerBin(140.0, 0.96125, 0.00682352891655),
                triggerBin(160.0, 0.994652406417, 0.00307916835595),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0944625407166, 0.00590158735886),
                triggerBin(30.0, 0.129933481153, 0.00708049291219),
                triggerBin(40.0, 0.16874687968, 0.00836843110628),
                triggerBin(50.0, 0.227880330999, 0.0105829717345),
                triggerBin(60.0, 0.303230543319, 0.0124549638306),
                triggerBin(70.0, 0.365300784656, 0.014217641993),
                triggerBin(80.0, 0.548830111902, 0.0112226976303),
                triggerBin(100.0, 0.765060240964, 0.0109685893464),
                triggerBin(120.0, 0.889354568315, 0.00908205216497),
                triggerBin(140.0, 0.96125, 0.00682352891655),
                triggerBin(160.0, 0.994652406417, 0.00307916835595),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0944625407166, 0.00590158735886),
                triggerBin(30.0, 0.129933481153, 0.00708049291219),
                triggerBin(40.0, 0.16874687968, 0.00836843110628),
                triggerBin(50.0, 0.227880330999, 0.0105829717345),
                triggerBin(60.0, 0.303230543319, 0.0124549638306),
                triggerBin(70.0, 0.365300784656, 0.014217641993),
                triggerBin(80.0, 0.548830111902, 0.0112226976303),
                triggerBin(100.0, 0.765060240964, 0.0109685893464),
                triggerBin(120.0, 0.889354568315, 0.00908205216497),
                triggerBin(140.0, 0.96125, 0.00682352891655),
                triggerBin(160.0, 0.994652406417, 0.00307916835595),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0944625407166, 0.00590158735886),
                triggerBin(30.0, 0.129933481153, 0.00708049291219),
                triggerBin(40.0, 0.16874687968, 0.00836843110628),
                triggerBin(50.0, 0.227880330999, 0.0105829717345),
                triggerBin(60.0, 0.303230543319, 0.0124549638306),
                triggerBin(70.0, 0.365300784656, 0.014217641993),
                triggerBin(80.0, 0.548830111902, 0.0112226976303),
                triggerBin(100.0, 0.765060240964, 0.0109685893464),
                triggerBin(120.0, 0.889354568315, 0.00908205216497),
                triggerBin(140.0, 0.96125, 0.00682352891655),
                triggerBin(160.0, 0.994652406417, 0.00307916835595),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0944625407166, 0.00590158735886),
                triggerBin(30.0, 0.129933481153, 0.00708049291219),
                triggerBin(40.0, 0.16874687968, 0.00836843110628),
                triggerBin(50.0, 0.227880330999, 0.0105829717345),
                triggerBin(60.0, 0.303230543319, 0.0124549638306),
                triggerBin(70.0, 0.365300784656, 0.014217641993),
                triggerBin(80.0, 0.548830111902, 0.0112226976303),
                triggerBin(100.0, 0.765060240964, 0.0109685893464),
                triggerBin(120.0, 0.889354568315, 0.00908205216497),
                triggerBin(140.0, 0.96125, 0.00682352891655),
                triggerBin(160.0, 0.994652406417, 0.00307916835595),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012A"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

metLegEfficiency_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronMediumMVA3 = cms.untracked.PSet(
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

    # Offline selection: (Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5) >= 1&&Sum$(PFJetPt > 0&& PFJetPUIDtight) >= 3+Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5 && PFTauJetMinDR < 0.5))&& hPlusGlobalElectronVetoFilter > 0.5 && hPlusGlobalMuonVetoFilter > 0.5

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0833333333333, 0.079785592313),
                triggerBin(30.0, 0.0, 0.0),
                triggerBin(40.0, 0.333333333333, 0.272165526976),
                triggerBin(50.0, 0.5, 0.353553390593),
                triggerBin(60.0, 0.0, 0.0),
                triggerBin(70.0, 1.0, 0.0),
                triggerBin(80.0, 0.0, 1.0),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0300751879699, 0.0148097384742),
                triggerBin(30.0, 0.0752688172043, 0.0273573371576),
                triggerBin(40.0, 0.162790697674, 0.0562985989385),
                triggerBin(50.0, 0.194444444444, 0.0659620687443),
                triggerBin(60.0, 0.363636363636, 0.145040733676),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 0.75, 0.216506350946),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.333333333333, 0.272165526976),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0412371134021, 0.0142757479231),
                triggerBin(30.0, 0.0833333333333, 0.0252304196175),
                triggerBin(40.0, 0.0506329113924, 0.0246672076884),
                triggerBin(50.0, 0.166666666667, 0.062112999375),
                triggerBin(60.0, 0.333333333333, 0.111111111111),
                triggerBin(70.0, 0.5, 0.144337567297),
                triggerBin(80.0, 0.25, 0.216506350946),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.75, 0.216506350946),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.041095890411, 0.0134141985368),
                triggerBin(30.0, 0.0700636942675, 0.0203715133022),
                triggerBin(40.0, 0.10989010989, 0.0327853950395),
                triggerBin(50.0, 0.117647058824, 0.0451155875792),
                triggerBin(60.0, 0.25, 0.0968245836552),
                triggerBin(70.0, 0.142857142857, 0.132260014253),
                triggerBin(80.0, 0.428571428571, 0.187043905917),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0344827586207, 0.0151529439449),
                triggerBin(30.0, 0.07, 0.0255147016443),
                triggerBin(40.0, 0.173913043478, 0.0558856162537),
                triggerBin(50.0, 0.210526315789, 0.066134827625),
                triggerBin(60.0, 0.333333333333, 0.136082763488),
                triggerBin(70.0, 0.666666666667, 0.272165526976),
                triggerBin(80.0, 0.75, 0.216506350946),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.5, 0.25),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0383480825959, 0.0104299188373),
                triggerBin(30.0, 0.0772727272727, 0.0180027337435),
                triggerBin(40.0, 0.096, 0.0263490417283),
                triggerBin(50.0, 0.189189189189, 0.0455294142944),
                triggerBin(60.0, 0.333333333333, 0.0860662965824),
                triggerBin(70.0, 0.533333333333, 0.128812237744),
                triggerBin(80.0, 0.5, 0.176776695297),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.6, 0.219089023002),
                triggerBin(140.0, 0.75, 0.216506350946),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0394265232975, 0.00823839169829),
                triggerBin(30.0, 0.0742705570292, 0.0135045371477),
                triggerBin(40.0, 0.101851851852, 0.0205793464567),
                triggerBin(50.0, 0.16, 0.0327902424511),
                triggerBin(60.0, 0.3, 0.0648074069841),
                triggerBin(70.0, 0.409090909091, 0.104823561107),
                triggerBin(80.0, 0.466666666667, 0.128812237744),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.75, 0.153093108924),
                triggerBin(140.0, 0.75, 0.216506350946),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.097177969959, 0.0044684299997),
                triggerBin(30.0, 0.132205995388, 0.00542168925394),
                triggerBin(40.0, 0.179702048417, 0.00676393708447),
                triggerBin(50.0, 0.22633910592, 0.00839782385202),
                triggerBin(60.0, 0.307125307125, 0.010225933041),
                triggerBin(70.0, 0.378027170703, 0.0117847055394),
                triggerBin(80.0, 0.543555240793, 0.00937310775992),
                triggerBin(100.0, 0.76548463357, 0.0092129498062),
                triggerBin(120.0, 0.894011976048, 0.0075325466557),
                triggerBin(140.0, 0.965004374453, 0.00543561146863),
                triggerBin(160.0, 0.994743758213, 0.00262120477396),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.097177969959, 0.0044684299997),
                triggerBin(30.0, 0.132205995388, 0.00542168925394),
                triggerBin(40.0, 0.179702048417, 0.00676393708447),
                triggerBin(50.0, 0.22633910592, 0.00839782385202),
                triggerBin(60.0, 0.307125307125, 0.010225933041),
                triggerBin(70.0, 0.378027170703, 0.0117847055394),
                triggerBin(80.0, 0.543555240793, 0.00937310775992),
                triggerBin(100.0, 0.76548463357, 0.0092129498062),
                triggerBin(120.0, 0.894011976048, 0.0075325466557),
                triggerBin(140.0, 0.965004374453, 0.00543561146863),
                triggerBin(160.0, 0.994743758213, 0.00262120477396),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.097177969959, 0.0044684299997),
                triggerBin(30.0, 0.132205995388, 0.00542168925394),
                triggerBin(40.0, 0.179702048417, 0.00676393708447),
                triggerBin(50.0, 0.22633910592, 0.00839782385202),
                triggerBin(60.0, 0.307125307125, 0.010225933041),
                triggerBin(70.0, 0.378027170703, 0.0117847055394),
                triggerBin(80.0, 0.543555240793, 0.00937310775992),
                triggerBin(100.0, 0.76548463357, 0.0092129498062),
                triggerBin(120.0, 0.894011976048, 0.0075325466557),
                triggerBin(140.0, 0.965004374453, 0.00543561146863),
                triggerBin(160.0, 0.994743758213, 0.00262120477396),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.097177969959, 0.0044684299997),
                triggerBin(30.0, 0.132205995388, 0.00542168925394),
                triggerBin(40.0, 0.179702048417, 0.00676393708447),
                triggerBin(50.0, 0.22633910592, 0.00839782385202),
                triggerBin(60.0, 0.307125307125, 0.010225933041),
                triggerBin(70.0, 0.378027170703, 0.0117847055394),
                triggerBin(80.0, 0.543555240793, 0.00937310775992),
                triggerBin(100.0, 0.76548463357, 0.0092129498062),
                triggerBin(120.0, 0.894011976048, 0.0075325466557),
                triggerBin(140.0, 0.965004374453, 0.00543561146863),
                triggerBin(160.0, 0.994743758213, 0.00262120477396),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.097177969959, 0.0044684299997),
                triggerBin(30.0, 0.132205995388, 0.00542168925394),
                triggerBin(40.0, 0.179702048417, 0.00676393708447),
                triggerBin(50.0, 0.22633910592, 0.00839782385202),
                triggerBin(60.0, 0.307125307125, 0.010225933041),
                triggerBin(70.0, 0.378027170703, 0.0117847055394),
                triggerBin(80.0, 0.543555240793, 0.00937310775992),
                triggerBin(100.0, 0.76548463357, 0.0092129498062),
                triggerBin(120.0, 0.894011976048, 0.0075325466557),
                triggerBin(140.0, 0.965004374453, 0.00543561146863),
                triggerBin(160.0, 0.994743758213, 0.00262120477396),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.097177969959, 0.0044684299997),
                triggerBin(30.0, 0.132205995388, 0.00542168925394),
                triggerBin(40.0, 0.179702048417, 0.00676393708447),
                triggerBin(50.0, 0.22633910592, 0.00839782385202),
                triggerBin(60.0, 0.307125307125, 0.010225933041),
                triggerBin(70.0, 0.378027170703, 0.0117847055394),
                triggerBin(80.0, 0.543555240793, 0.00937310775992),
                triggerBin(100.0, 0.76548463357, 0.0092129498062),
                triggerBin(120.0, 0.894011976048, 0.0075325466557),
                triggerBin(140.0, 0.965004374453, 0.00543561146863),
                triggerBin(160.0, 0.994743758213, 0.00262120477396),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.097177969959, 0.0044684299997),
                triggerBin(30.0, 0.132205995388, 0.00542168925394),
                triggerBin(40.0, 0.179702048417, 0.00676393708447),
                triggerBin(50.0, 0.22633910592, 0.00839782385202),
                triggerBin(60.0, 0.307125307125, 0.010225933041),
                triggerBin(70.0, 0.378027170703, 0.0117847055394),
                triggerBin(80.0, 0.543555240793, 0.00937310775992),
                triggerBin(100.0, 0.76548463357, 0.0092129498062),
                triggerBin(120.0, 0.894011976048, 0.0075325466557),
                triggerBin(140.0, 0.965004374453, 0.00543561146863),
                triggerBin(160.0, 0.994743758213, 0.00262120477396),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.097177969959, 0.0044684299997),
                triggerBin(30.0, 0.132205995388, 0.00542168925394),
                triggerBin(40.0, 0.179702048417, 0.00676393708447),
                triggerBin(50.0, 0.22633910592, 0.00839782385202),
                triggerBin(60.0, 0.307125307125, 0.010225933041),
                triggerBin(70.0, 0.378027170703, 0.0117847055394),
                triggerBin(80.0, 0.543555240793, 0.00937310775992),
                triggerBin(100.0, 0.76548463357, 0.0092129498062),
                triggerBin(120.0, 0.894011976048, 0.0075325466557),
                triggerBin(140.0, 0.965004374453, 0.00543561146863),
                triggerBin(160.0, 0.994743758213, 0.00262120477396),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012A"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

metLegEfficiency_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronMediumMVA3 = cms.untracked.PSet(
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

    # Offline selection: (Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5) >= 1&&Sum$(PFJetPt > 0&& PFJetPUIDtight) >= 3+Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5 && PFTauJetMinDR < 0.5))&& hPlusGlobalElectronVetoFilter > 0.5 && hPlusGlobalMuonVetoFilter > 0.5

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.125, 0.116926793337),
                triggerBin(30.0, 0.0, 0.0),
                triggerBin(40.0, 0.5, 0.353553390593),
                triggerBin(50.0, 0.5, 0.353553390593),
                triggerBin(60.0, 0.0, 1.0),
                triggerBin(70.0, 1.0, 0.0),
                triggerBin(80.0, 0.0, 1.0),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0348837209302, 0.019785726281),
                triggerBin(30.0, 0.125, 0.0441941738242),
                triggerBin(40.0, 0.136363636364, 0.0731650049984),
                triggerBin(50.0, 0.166666666667, 0.0878410461158),
                triggerBin(60.0, 0.25, 0.153093108924),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.333333333333, 0.272165526976),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.051724137931, 0.0205629293764),
                triggerBin(30.0, 0.0757575757576, 0.0325712192794),
                triggerBin(40.0, 0.0681818181818, 0.0379991201606),
                triggerBin(50.0, 0.173913043478, 0.0790341964475),
                triggerBin(60.0, 0.333333333333, 0.136082763488),
                triggerBin(70.0, 0.5, 0.158113883008),
                triggerBin(80.0, 0.333333333333, 0.272165526976),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.03125, 0.0153789216289),
                triggerBin(30.0, 0.0348837209302, 0.019785726281),
                triggerBin(40.0, 0.127659574468, 0.0486766595111),
                triggerBin(50.0, 0.2, 0.08),
                triggerBin(60.0, 0.272727272727, 0.134281626523),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 0.25, 0.216506350946),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0425531914894, 0.0208189810549),
                triggerBin(30.0, 0.116666666667, 0.0414438486701),
                triggerBin(40.0, 0.166666666667, 0.0760725774313),
                triggerBin(50.0, 0.2, 0.0894427191),
                triggerBin(60.0, 0.25, 0.153093108924),
                triggerBin(70.0, 0.666666666667, 0.272165526976),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.5, 0.25),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.047619047619, 0.0146955571392),
                triggerBin(30.0, 0.0952380952381, 0.0261509355888),
                triggerBin(40.0, 0.102941176471, 0.0368511095406),
                triggerBin(50.0, 0.186046511628, 0.0593439339074),
                triggerBin(60.0, 0.3, 0.10246950766),
                triggerBin(70.0, 0.538461538462, 0.138264159119),
                triggerBin(80.0, 0.6, 0.219089023002),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.6, 0.219089023002),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0414201183432, 0.0108383076011),
                triggerBin(30.0, 0.0707547169811, 0.0176106323756),
                triggerBin(40.0, 0.113043478261, 0.0295273860036),
                triggerBin(50.0, 0.191176470588, 0.0476858635609),
                triggerBin(60.0, 0.290322580645, 0.0815248586297),
                triggerBin(70.0, 0.411764705882, 0.119364624987),
                triggerBin(80.0, 0.444444444444, 0.165634665),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.75, 0.153093108924),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0979547900969, 0.00563064967065),
                triggerBin(30.0, 0.127002735444, 0.00658230248408),
                triggerBin(40.0, 0.171635049684, 0.00801355162631),
                triggerBin(50.0, 0.225214899713, 0.00999980368462),
                triggerBin(60.0, 0.300938337802, 0.0118744113624),
                triggerBin(70.0, 0.368, 0.013640410551),
                triggerBin(80.0, 0.550164861046, 0.0107968760576),
                triggerBin(100.0, 0.763317191283, 0.010457571859),
                triggerBin(120.0, 0.89373088685, 0.00852124475571),
                triggerBin(140.0, 0.962585034014, 0.00639010416086),
                triggerBin(160.0, 0.993399339934, 0.00328941982122),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0979547900969, 0.00563064967065),
                triggerBin(30.0, 0.127002735444, 0.00658230248408),
                triggerBin(40.0, 0.171635049684, 0.00801355162631),
                triggerBin(50.0, 0.225214899713, 0.00999980368462),
                triggerBin(60.0, 0.300938337802, 0.0118744113624),
                triggerBin(70.0, 0.368, 0.013640410551),
                triggerBin(80.0, 0.550164861046, 0.0107968760576),
                triggerBin(100.0, 0.763317191283, 0.010457571859),
                triggerBin(120.0, 0.89373088685, 0.00852124475571),
                triggerBin(140.0, 0.962585034014, 0.00639010416086),
                triggerBin(160.0, 0.993399339934, 0.00328941982122),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0979547900969, 0.00563064967065),
                triggerBin(30.0, 0.127002735444, 0.00658230248408),
                triggerBin(40.0, 0.171635049684, 0.00801355162631),
                triggerBin(50.0, 0.225214899713, 0.00999980368462),
                triggerBin(60.0, 0.300938337802, 0.0118744113624),
                triggerBin(70.0, 0.368, 0.013640410551),
                triggerBin(80.0, 0.550164861046, 0.0107968760576),
                triggerBin(100.0, 0.763317191283, 0.010457571859),
                triggerBin(120.0, 0.89373088685, 0.00852124475571),
                triggerBin(140.0, 0.962585034014, 0.00639010416086),
                triggerBin(160.0, 0.993399339934, 0.00328941982122),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0979547900969, 0.00563064967065),
                triggerBin(30.0, 0.127002735444, 0.00658230248408),
                triggerBin(40.0, 0.171635049684, 0.00801355162631),
                triggerBin(50.0, 0.225214899713, 0.00999980368462),
                triggerBin(60.0, 0.300938337802, 0.0118744113624),
                triggerBin(70.0, 0.368, 0.013640410551),
                triggerBin(80.0, 0.550164861046, 0.0107968760576),
                triggerBin(100.0, 0.763317191283, 0.010457571859),
                triggerBin(120.0, 0.89373088685, 0.00852124475571),
                triggerBin(140.0, 0.962585034014, 0.00639010416086),
                triggerBin(160.0, 0.993399339934, 0.00328941982122),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0979547900969, 0.00563064967065),
                triggerBin(30.0, 0.127002735444, 0.00658230248408),
                triggerBin(40.0, 0.171635049684, 0.00801355162631),
                triggerBin(50.0, 0.225214899713, 0.00999980368462),
                triggerBin(60.0, 0.300938337802, 0.0118744113624),
                triggerBin(70.0, 0.368, 0.013640410551),
                triggerBin(80.0, 0.550164861046, 0.0107968760576),
                triggerBin(100.0, 0.763317191283, 0.010457571859),
                triggerBin(120.0, 0.89373088685, 0.00852124475571),
                triggerBin(140.0, 0.962585034014, 0.00639010416086),
                triggerBin(160.0, 0.993399339934, 0.00328941982122),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0979547900969, 0.00563064967065),
                triggerBin(30.0, 0.127002735444, 0.00658230248408),
                triggerBin(40.0, 0.171635049684, 0.00801355162631),
                triggerBin(50.0, 0.225214899713, 0.00999980368462),
                triggerBin(60.0, 0.300938337802, 0.0118744113624),
                triggerBin(70.0, 0.368, 0.013640410551),
                triggerBin(80.0, 0.550164861046, 0.0107968760576),
                triggerBin(100.0, 0.763317191283, 0.010457571859),
                triggerBin(120.0, 0.89373088685, 0.00852124475571),
                triggerBin(140.0, 0.962585034014, 0.00639010416086),
                triggerBin(160.0, 0.993399339934, 0.00328941982122),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0979547900969, 0.00563064967065),
                triggerBin(30.0, 0.127002735444, 0.00658230248408),
                triggerBin(40.0, 0.171635049684, 0.00801355162631),
                triggerBin(50.0, 0.225214899713, 0.00999980368462),
                triggerBin(60.0, 0.300938337802, 0.0118744113624),
                triggerBin(70.0, 0.368, 0.013640410551),
                triggerBin(80.0, 0.550164861046, 0.0107968760576),
                triggerBin(100.0, 0.763317191283, 0.010457571859),
                triggerBin(120.0, 0.89373088685, 0.00852124475571),
                triggerBin(140.0, 0.962585034014, 0.00639010416086),
                triggerBin(160.0, 0.993399339934, 0.00328941982122),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0979547900969, 0.00563064967065),
                triggerBin(30.0, 0.127002735444, 0.00658230248408),
                triggerBin(40.0, 0.171635049684, 0.00801355162631),
                triggerBin(50.0, 0.225214899713, 0.00999980368462),
                triggerBin(60.0, 0.300938337802, 0.0118744113624),
                triggerBin(70.0, 0.368, 0.013640410551),
                triggerBin(80.0, 0.550164861046, 0.0107968760576),
                triggerBin(100.0, 0.763317191283, 0.010457571859),
                triggerBin(120.0, 0.89373088685, 0.00852124475571),
                triggerBin(140.0, 0.962585034014, 0.00639010416086),
                triggerBin(160.0, 0.993399339934, 0.00328941982122),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012A"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

metLegEfficiency_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronMediumMVA3 = cms.untracked.PSet(
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

    # Offline selection: (Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) >= 1&&Sum$(PFJetPt > 0&& PFJetPUIDtight) >= 3+Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5 && PFTauJetMinDR < 0.5))&& hPlusGlobalElectronVetoFilter > 0.5 && hPlusGlobalMuonVetoFilter > 0.5

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.142857142857, 0.132260014253),
                triggerBin(30.0, 0.0, 0.0),
                triggerBin(40.0, 0.5, 0.353553390593),
                triggerBin(50.0, 0.5, 0.353553390593),
                triggerBin(60.0, 0.0, 1.0),
                triggerBin(70.0, 1.0, 0.0),
                triggerBin(80.0, 0.0, 1.0),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.038961038961, 0.0220516148963),
                triggerBin(30.0, 0.117647058824, 0.0451155875792),
                triggerBin(40.0, 0.166666666667, 0.0878410461158),
                triggerBin(50.0, 0.142857142857, 0.0935219529583),
                triggerBin(60.0, 0.25, 0.153093108924),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0594059405941, 0.0235209775375),
                triggerBin(30.0, 0.0806451612903, 0.0345807888235),
                triggerBin(40.0, 0.0789473684211, 0.043744076724),
                triggerBin(50.0, 0.210526315789, 0.0935287701725),
                triggerBin(60.0, 0.333333333333, 0.136082763488),
                triggerBin(70.0, 0.444444444444, 0.165634665),
                triggerBin(80.0, 0.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0263157894737, 0.0149921817924),
                triggerBin(30.0, 0.038961038961, 0.0220516148963),
                triggerBin(40.0, 0.130434782609, 0.0496556731061),
                triggerBin(50.0, 0.227272727273, 0.0893460673985),
                triggerBin(60.0, 0.3, 0.144913767462),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 0.25, 0.216506350946),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.047619047619, 0.0232357160226),
                triggerBin(30.0, 0.111111111111, 0.0427666866066),
                triggerBin(40.0, 0.2, 0.0894427191),
                triggerBin(50.0, 0.1875, 0.097578093725),
                triggerBin(60.0, 0.25, 0.153093108924),
                triggerBin(70.0, 0.666666666667, 0.272165526976),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.333333333333, 0.272165526976),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0540540540541, 0.0166249914927),
                triggerBin(30.0, 0.0948275862069, 0.0272021986784),
                triggerBin(40.0, 0.120689655172, 0.0427752067866),
                triggerBin(50.0, 0.2, 0.0676123403783),
                triggerBin(60.0, 0.3, 0.10246950766),
                triggerBin(70.0, 0.5, 0.144337567297),
                triggerBin(80.0, 0.5, 0.25),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.5, 0.25),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0434782608696, 0.0117936411784),
                triggerBin(30.0, 0.0725388601036, 0.0186704407255),
                triggerBin(40.0, 0.125, 0.0324296576039),
                triggerBin(50.0, 0.210526315789, 0.0539988606361),
                triggerBin(60.0, 0.3, 0.0836660026534),
                triggerBin(70.0, 0.375, 0.121030729569),
                triggerBin(80.0, 0.375, 0.17116329922),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.714285714286, 0.170746944191),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.094616639478, 0.00591071175606),
                triggerBin(30.0, 0.129060970182, 0.00707277435961),
                triggerBin(40.0, 0.167589330649, 0.00837901694491),
                triggerBin(50.0, 0.225496476618, 0.0105774292125),
                triggerBin(60.0, 0.30258302583, 0.0124795489768),
                triggerBin(70.0, 0.364273204904, 0.0142401911764),
                triggerBin(80.0, 0.546386468478, 0.0112710488898),
                triggerBin(100.0, 0.764271323036, 0.0109997456415),
                triggerBin(120.0, 0.889168765743, 0.00909635295525),
                triggerBin(140.0, 0.96125, 0.00682352891655),
                triggerBin(160.0, 0.994633273703, 0.00309015533758),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.094616639478, 0.00591071175606),
                triggerBin(30.0, 0.129060970182, 0.00707277435961),
                triggerBin(40.0, 0.167589330649, 0.00837901694491),
                triggerBin(50.0, 0.225496476618, 0.0105774292125),
                triggerBin(60.0, 0.30258302583, 0.0124795489768),
                triggerBin(70.0, 0.364273204904, 0.0142401911764),
                triggerBin(80.0, 0.546386468478, 0.0112710488898),
                triggerBin(100.0, 0.764271323036, 0.0109997456415),
                triggerBin(120.0, 0.889168765743, 0.00909635295525),
                triggerBin(140.0, 0.96125, 0.00682352891655),
                triggerBin(160.0, 0.994633273703, 0.00309015533758),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.094616639478, 0.00591071175606),
                triggerBin(30.0, 0.129060970182, 0.00707277435961),
                triggerBin(40.0, 0.167589330649, 0.00837901694491),
                triggerBin(50.0, 0.225496476618, 0.0105774292125),
                triggerBin(60.0, 0.30258302583, 0.0124795489768),
                triggerBin(70.0, 0.364273204904, 0.0142401911764),
                triggerBin(80.0, 0.546386468478, 0.0112710488898),
                triggerBin(100.0, 0.764271323036, 0.0109997456415),
                triggerBin(120.0, 0.889168765743, 0.00909635295525),
                triggerBin(140.0, 0.96125, 0.00682352891655),
                triggerBin(160.0, 0.994633273703, 0.00309015533758),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.094616639478, 0.00591071175606),
                triggerBin(30.0, 0.129060970182, 0.00707277435961),
                triggerBin(40.0, 0.167589330649, 0.00837901694491),
                triggerBin(50.0, 0.225496476618, 0.0105774292125),
                triggerBin(60.0, 0.30258302583, 0.0124795489768),
                triggerBin(70.0, 0.364273204904, 0.0142401911764),
                triggerBin(80.0, 0.546386468478, 0.0112710488898),
                triggerBin(100.0, 0.764271323036, 0.0109997456415),
                triggerBin(120.0, 0.889168765743, 0.00909635295525),
                triggerBin(140.0, 0.96125, 0.00682352891655),
                triggerBin(160.0, 0.994633273703, 0.00309015533758),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.094616639478, 0.00591071175606),
                triggerBin(30.0, 0.129060970182, 0.00707277435961),
                triggerBin(40.0, 0.167589330649, 0.00837901694491),
                triggerBin(50.0, 0.225496476618, 0.0105774292125),
                triggerBin(60.0, 0.30258302583, 0.0124795489768),
                triggerBin(70.0, 0.364273204904, 0.0142401911764),
                triggerBin(80.0, 0.546386468478, 0.0112710488898),
                triggerBin(100.0, 0.764271323036, 0.0109997456415),
                triggerBin(120.0, 0.889168765743, 0.00909635295525),
                triggerBin(140.0, 0.96125, 0.00682352891655),
                triggerBin(160.0, 0.994633273703, 0.00309015533758),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.094616639478, 0.00591071175606),
                triggerBin(30.0, 0.129060970182, 0.00707277435961),
                triggerBin(40.0, 0.167589330649, 0.00837901694491),
                triggerBin(50.0, 0.225496476618, 0.0105774292125),
                triggerBin(60.0, 0.30258302583, 0.0124795489768),
                triggerBin(70.0, 0.364273204904, 0.0142401911764),
                triggerBin(80.0, 0.546386468478, 0.0112710488898),
                triggerBin(100.0, 0.764271323036, 0.0109997456415),
                triggerBin(120.0, 0.889168765743, 0.00909635295525),
                triggerBin(140.0, 0.96125, 0.00682352891655),
                triggerBin(160.0, 0.994633273703, 0.00309015533758),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.094616639478, 0.00591071175606),
                triggerBin(30.0, 0.129060970182, 0.00707277435961),
                triggerBin(40.0, 0.167589330649, 0.00837901694491),
                triggerBin(50.0, 0.225496476618, 0.0105774292125),
                triggerBin(60.0, 0.30258302583, 0.0124795489768),
                triggerBin(70.0, 0.364273204904, 0.0142401911764),
                triggerBin(80.0, 0.546386468478, 0.0112710488898),
                triggerBin(100.0, 0.764271323036, 0.0109997456415),
                triggerBin(120.0, 0.889168765743, 0.00909635295525),
                triggerBin(140.0, 0.96125, 0.00682352891655),
                triggerBin(160.0, 0.994633273703, 0.00309015533758),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.094616639478, 0.00591071175606),
                triggerBin(30.0, 0.129060970182, 0.00707277435961),
                triggerBin(40.0, 0.167589330649, 0.00837901694491),
                triggerBin(50.0, 0.225496476618, 0.0105774292125),
                triggerBin(60.0, 0.30258302583, 0.0124795489768),
                triggerBin(70.0, 0.364273204904, 0.0142401911764),
                triggerBin(80.0, 0.546386468478, 0.0112710488898),
                triggerBin(100.0, 0.764271323036, 0.0109997456415),
                triggerBin(120.0, 0.889168765743, 0.00909635295525),
                triggerBin(140.0, 0.96125, 0.00682352891655),
                triggerBin(160.0, 0.994633273703, 0.00309015533758),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012A"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

metLegEfficiency_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: (Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5) >= 1&&Sum$(PFJetPt > 0&& PFJetPUIDtight) >= 3+Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5 && PFTauJetMinDR < 0.5))&& hPlusGlobalElectronVetoFilter > 0.5 && hPlusGlobalMuonVetoFilter > 0.5

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0909090909091, 0.0866784172041),
                triggerBin(30.0, 0.0, 0.0),
                triggerBin(40.0, 0.0, 0.0),
                triggerBin(50.0, 0.5, 0.353553390593),
                triggerBin(60.0, 0.0, 1.0),
                triggerBin(70.0, 1.0, 0.0),
                triggerBin(80.0, 0.0, 1.0),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.036036036036, 0.017690390363),
                triggerBin(30.0, 0.0681818181818, 0.0268694355447),
                triggerBin(40.0, 0.125, 0.0522912516584),
                triggerBin(50.0, 0.176470588235, 0.0653786976737),
                triggerBin(60.0, 0.4, 0.154919333848),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 0.75, 0.216506350946),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.333333333333, 0.272165526976),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0280898876404, 0.0123844878174),
                triggerBin(30.0, 0.0660377358491, 0.0241216948646),
                triggerBin(40.0, 0.0588235294118, 0.0285336029454),
                triggerBin(50.0, 0.1, 0.0547722557505),
                triggerBin(60.0, 0.266666666667, 0.114179845144),
                triggerBin(70.0, 0.444444444444, 0.165634665),
                triggerBin(80.0, 0.333333333333, 0.272165526976),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.75, 0.216506350946),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.048128342246, 0.0156519642065),
                triggerBin(30.0, 0.0575539568345, 0.0197541542643),
                triggerBin(40.0, 0.120481927711, 0.0357309276458),
                triggerBin(50.0, 0.139534883721, 0.0528413377526),
                triggerBin(60.0, 0.263157894737, 0.101022617888),
                triggerBin(70.0, 0.166666666667, 0.152145154863),
                triggerBin(80.0, 0.333333333333, 0.19245008973),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0409836065574, 0.0179489144269),
                triggerBin(30.0, 0.0652173913043, 0.0257420488306),
                triggerBin(40.0, 0.121951219512, 0.051104655788),
                triggerBin(50.0, 0.194444444444, 0.0659620687443),
                triggerBin(60.0, 0.4, 0.154919333848),
                triggerBin(70.0, 0.666666666667, 0.272165526976),
                triggerBin(80.0, 0.75, 0.216506350946),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.5, 0.25),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0333333333333, 0.0103637545034),
                triggerBin(30.0, 0.0656565656566, 0.0176019083336),
                triggerBin(40.0, 0.0825688073394, 0.0263621913364),
                triggerBin(50.0, 0.151515151515, 0.044134489773),
                triggerBin(60.0, 0.32, 0.0932952303175),
                triggerBin(70.0, 0.5, 0.144337567297),
                triggerBin(80.0, 0.571428571429, 0.187043905917),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.6, 0.219089023002),
                triggerBin(140.0, 0.75, 0.216506350946),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0390143737166, 0.00877417486016),
                triggerBin(30.0, 0.0623145400593, 0.0131676519108),
                triggerBin(40.0, 0.0989583333333, 0.0215500364459),
                triggerBin(50.0, 0.146788990826, 0.033897035539),
                triggerBin(60.0, 0.295454545455, 0.0687817954616),
                triggerBin(70.0, 0.388888888889, 0.114904385611),
                triggerBin(80.0, 0.461538461538, 0.138264159119),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.75, 0.153093108924),
                triggerBin(140.0, 0.75, 0.216506350946),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0956925457828, 0.00472442772175),
                triggerBin(30.0, 0.129483814523, 0.00573340241621),
                triggerBin(40.0, 0.17982300885, 0.00722548817808),
                triggerBin(50.0, 0.225472547255, 0.00886529550024),
                triggerBin(60.0, 0.305693753455, 0.0108317726278),
                triggerBin(70.0, 0.364713627386, 0.0123504243046),
                triggerBin(80.0, 0.547297297297, 0.00992345436877),
                triggerBin(100.0, 0.761146496815, 0.00982334698933),
                triggerBin(120.0, 0.891838088918, 0.00800061842636),
                triggerBin(140.0, 0.966085271318, 0.00563458656481),
                triggerBin(160.0, 0.997093023256, 0.0020525530863),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0956925457828, 0.00472442772175),
                triggerBin(30.0, 0.129483814523, 0.00573340241621),
                triggerBin(40.0, 0.17982300885, 0.00722548817808),
                triggerBin(50.0, 0.225472547255, 0.00886529550024),
                triggerBin(60.0, 0.305693753455, 0.0108317726278),
                triggerBin(70.0, 0.364713627386, 0.0123504243046),
                triggerBin(80.0, 0.547297297297, 0.00992345436877),
                triggerBin(100.0, 0.761146496815, 0.00982334698933),
                triggerBin(120.0, 0.891838088918, 0.00800061842636),
                triggerBin(140.0, 0.966085271318, 0.00563458656481),
                triggerBin(160.0, 0.997093023256, 0.0020525530863),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0956925457828, 0.00472442772175),
                triggerBin(30.0, 0.129483814523, 0.00573340241621),
                triggerBin(40.0, 0.17982300885, 0.00722548817808),
                triggerBin(50.0, 0.225472547255, 0.00886529550024),
                triggerBin(60.0, 0.305693753455, 0.0108317726278),
                triggerBin(70.0, 0.364713627386, 0.0123504243046),
                triggerBin(80.0, 0.547297297297, 0.00992345436877),
                triggerBin(100.0, 0.761146496815, 0.00982334698933),
                triggerBin(120.0, 0.891838088918, 0.00800061842636),
                triggerBin(140.0, 0.966085271318, 0.00563458656481),
                triggerBin(160.0, 0.997093023256, 0.0020525530863),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0956925457828, 0.00472442772175),
                triggerBin(30.0, 0.129483814523, 0.00573340241621),
                triggerBin(40.0, 0.17982300885, 0.00722548817808),
                triggerBin(50.0, 0.225472547255, 0.00886529550024),
                triggerBin(60.0, 0.305693753455, 0.0108317726278),
                triggerBin(70.0, 0.364713627386, 0.0123504243046),
                triggerBin(80.0, 0.547297297297, 0.00992345436877),
                triggerBin(100.0, 0.761146496815, 0.00982334698933),
                triggerBin(120.0, 0.891838088918, 0.00800061842636),
                triggerBin(140.0, 0.966085271318, 0.00563458656481),
                triggerBin(160.0, 0.997093023256, 0.0020525530863),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0956925457828, 0.00472442772175),
                triggerBin(30.0, 0.129483814523, 0.00573340241621),
                triggerBin(40.0, 0.17982300885, 0.00722548817808),
                triggerBin(50.0, 0.225472547255, 0.00886529550024),
                triggerBin(60.0, 0.305693753455, 0.0108317726278),
                triggerBin(70.0, 0.364713627386, 0.0123504243046),
                triggerBin(80.0, 0.547297297297, 0.00992345436877),
                triggerBin(100.0, 0.761146496815, 0.00982334698933),
                triggerBin(120.0, 0.891838088918, 0.00800061842636),
                triggerBin(140.0, 0.966085271318, 0.00563458656481),
                triggerBin(160.0, 0.997093023256, 0.0020525530863),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0956925457828, 0.00472442772175),
                triggerBin(30.0, 0.129483814523, 0.00573340241621),
                triggerBin(40.0, 0.17982300885, 0.00722548817808),
                triggerBin(50.0, 0.225472547255, 0.00886529550024),
                triggerBin(60.0, 0.305693753455, 0.0108317726278),
                triggerBin(70.0, 0.364713627386, 0.0123504243046),
                triggerBin(80.0, 0.547297297297, 0.00992345436877),
                triggerBin(100.0, 0.761146496815, 0.00982334698933),
                triggerBin(120.0, 0.891838088918, 0.00800061842636),
                triggerBin(140.0, 0.966085271318, 0.00563458656481),
                triggerBin(160.0, 0.997093023256, 0.0020525530863),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0956925457828, 0.00472442772175),
                triggerBin(30.0, 0.129483814523, 0.00573340241621),
                triggerBin(40.0, 0.17982300885, 0.00722548817808),
                triggerBin(50.0, 0.225472547255, 0.00886529550024),
                triggerBin(60.0, 0.305693753455, 0.0108317726278),
                triggerBin(70.0, 0.364713627386, 0.0123504243046),
                triggerBin(80.0, 0.547297297297, 0.00992345436877),
                triggerBin(100.0, 0.761146496815, 0.00982334698933),
                triggerBin(120.0, 0.891838088918, 0.00800061842636),
                triggerBin(140.0, 0.966085271318, 0.00563458656481),
                triggerBin(160.0, 0.997093023256, 0.0020525530863),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0956925457828, 0.00472442772175),
                triggerBin(30.0, 0.129483814523, 0.00573340241621),
                triggerBin(40.0, 0.17982300885, 0.00722548817808),
                triggerBin(50.0, 0.225472547255, 0.00886529550024),
                triggerBin(60.0, 0.305693753455, 0.0108317726278),
                triggerBin(70.0, 0.364713627386, 0.0123504243046),
                triggerBin(80.0, 0.547297297297, 0.00992345436877),
                triggerBin(100.0, 0.761146496815, 0.00982334698933),
                triggerBin(120.0, 0.891838088918, 0.00800061842636),
                triggerBin(140.0, 0.966085271318, 0.00563458656481),
                triggerBin(160.0, 0.997093023256, 0.0020525530863),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012A"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

metLegEfficiency_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: (Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5) >= 1&&Sum$(PFJetPt > 0&& PFJetPUIDtight) >= 3+Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5 && PFTauJetMinDR < 0.5))&& hPlusGlobalElectronVetoFilter > 0.5 && hPlusGlobalMuonVetoFilter > 0.5

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.142857142857, 0.132260014253),
                triggerBin(30.0, 0.0, 0.0),
                triggerBin(40.0, 0.0, 0.0),
                triggerBin(50.0, 0.5, 0.353553390593),
                triggerBin(60.0, 0.0, 1.0),
                triggerBin(70.0, 1.0, 0.0),
                triggerBin(80.0, 0.0, 1.0),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.041095890411, 0.0232340734086),
                triggerBin(30.0, 0.111111111111, 0.0427666866066),
                triggerBin(40.0, 0.142857142857, 0.0763603548321),
                triggerBin(50.0, 0.176470588235, 0.0924594409404),
                triggerBin(60.0, 0.285714285714, 0.170746944191),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.333333333333, 0.272165526976),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0380952380952, 0.0186812844796),
                triggerBin(30.0, 0.0545454545455, 0.0306209221207),
                triggerBin(40.0, 0.0789473684211, 0.043744076724),
                triggerBin(50.0, 0.15, 0.0798435971133),
                triggerBin(60.0, 0.222222222222, 0.138579903214),
                triggerBin(70.0, 0.428571428571, 0.187043905917),
                triggerBin(80.0, 0.5, 0.353553390593),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0373831775701, 0.0183388856062),
                triggerBin(30.0, 0.027397260274, 0.0191055648508),
                triggerBin(40.0, 0.139534883721, 0.0528413377526),
                triggerBin(50.0, 0.227272727273, 0.0893460673985),
                triggerBin(60.0, 0.3, 0.144913767462),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 0.25, 0.216506350946),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.05, 0.024366985862),
                triggerBin(30.0, 0.105263157895, 0.0406488655643),
                triggerBin(40.0, 0.136363636364, 0.0731650049984),
                triggerBin(50.0, 0.210526315789, 0.0935287701725),
                triggerBin(60.0, 0.285714285714, 0.170746944191),
                triggerBin(70.0, 0.666666666667, 0.272165526976),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.5, 0.25),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0432432432432, 0.0149545735853),
                triggerBin(30.0, 0.0803571428571, 0.0256869673127),
                triggerBin(40.0, 0.1, 0.0387298334621),
                triggerBin(50.0, 0.179487179487, 0.0614507373862),
                triggerBin(60.0, 0.25, 0.108253175473),
                triggerBin(70.0, 0.5, 0.158113883008),
                triggerBin(80.0, 0.75, 0.216506350946),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.6, 0.219089023002),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.041095890411, 0.0116170367043),
                triggerBin(30.0, 0.0594594594595, 0.0173865484103),
                triggerBin(40.0, 0.116504854369, 0.0316122554085),
                triggerBin(50.0, 0.196721311475, 0.0508972022624),
                triggerBin(60.0, 0.269230769231, 0.0869892924733),
                triggerBin(70.0, 0.357142857143, 0.128060208143),
                triggerBin(80.0, 0.5, 0.176776695297),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.75, 0.153093108924),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0948905109489, 0.00590154082045),
                triggerBin(30.0, 0.120407259849, 0.00684713734237),
                triggerBin(40.0, 0.16975308642, 0.00851460183924),
                triggerBin(50.0, 0.221086261981, 0.0104898285359),
                triggerBin(60.0, 0.297052154195, 0.0125631337438),
                triggerBin(70.0, 0.355614973262, 0.0142911214866),
                triggerBin(80.0, 0.553372278279, 0.0114566165432),
                triggerBin(100.0, 0.758339006127, 0.011169251709),
                triggerBin(120.0, 0.891047297297, 0.0090551058501),
                triggerBin(140.0, 0.96379525593, 0.00660022703963),
                triggerBin(160.0, 0.996268656716, 0.00263353104176),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0948905109489, 0.00590154082045),
                triggerBin(30.0, 0.120407259849, 0.00684713734237),
                triggerBin(40.0, 0.16975308642, 0.00851460183924),
                triggerBin(50.0, 0.221086261981, 0.0104898285359),
                triggerBin(60.0, 0.297052154195, 0.0125631337438),
                triggerBin(70.0, 0.355614973262, 0.0142911214866),
                triggerBin(80.0, 0.553372278279, 0.0114566165432),
                triggerBin(100.0, 0.758339006127, 0.011169251709),
                triggerBin(120.0, 0.891047297297, 0.0090551058501),
                triggerBin(140.0, 0.96379525593, 0.00660022703963),
                triggerBin(160.0, 0.996268656716, 0.00263353104176),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0948905109489, 0.00590154082045),
                triggerBin(30.0, 0.120407259849, 0.00684713734237),
                triggerBin(40.0, 0.16975308642, 0.00851460183924),
                triggerBin(50.0, 0.221086261981, 0.0104898285359),
                triggerBin(60.0, 0.297052154195, 0.0125631337438),
                triggerBin(70.0, 0.355614973262, 0.0142911214866),
                triggerBin(80.0, 0.553372278279, 0.0114566165432),
                triggerBin(100.0, 0.758339006127, 0.011169251709),
                triggerBin(120.0, 0.891047297297, 0.0090551058501),
                triggerBin(140.0, 0.96379525593, 0.00660022703963),
                triggerBin(160.0, 0.996268656716, 0.00263353104176),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0948905109489, 0.00590154082045),
                triggerBin(30.0, 0.120407259849, 0.00684713734237),
                triggerBin(40.0, 0.16975308642, 0.00851460183924),
                triggerBin(50.0, 0.221086261981, 0.0104898285359),
                triggerBin(60.0, 0.297052154195, 0.0125631337438),
                triggerBin(70.0, 0.355614973262, 0.0142911214866),
                triggerBin(80.0, 0.553372278279, 0.0114566165432),
                triggerBin(100.0, 0.758339006127, 0.011169251709),
                triggerBin(120.0, 0.891047297297, 0.0090551058501),
                triggerBin(140.0, 0.96379525593, 0.00660022703963),
                triggerBin(160.0, 0.996268656716, 0.00263353104176),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0948905109489, 0.00590154082045),
                triggerBin(30.0, 0.120407259849, 0.00684713734237),
                triggerBin(40.0, 0.16975308642, 0.00851460183924),
                triggerBin(50.0, 0.221086261981, 0.0104898285359),
                triggerBin(60.0, 0.297052154195, 0.0125631337438),
                triggerBin(70.0, 0.355614973262, 0.0142911214866),
                triggerBin(80.0, 0.553372278279, 0.0114566165432),
                triggerBin(100.0, 0.758339006127, 0.011169251709),
                triggerBin(120.0, 0.891047297297, 0.0090551058501),
                triggerBin(140.0, 0.96379525593, 0.00660022703963),
                triggerBin(160.0, 0.996268656716, 0.00263353104176),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0948905109489, 0.00590154082045),
                triggerBin(30.0, 0.120407259849, 0.00684713734237),
                triggerBin(40.0, 0.16975308642, 0.00851460183924),
                triggerBin(50.0, 0.221086261981, 0.0104898285359),
                triggerBin(60.0, 0.297052154195, 0.0125631337438),
                triggerBin(70.0, 0.355614973262, 0.0142911214866),
                triggerBin(80.0, 0.553372278279, 0.0114566165432),
                triggerBin(100.0, 0.758339006127, 0.011169251709),
                triggerBin(120.0, 0.891047297297, 0.0090551058501),
                triggerBin(140.0, 0.96379525593, 0.00660022703963),
                triggerBin(160.0, 0.996268656716, 0.00263353104176),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0948905109489, 0.00590154082045),
                triggerBin(30.0, 0.120407259849, 0.00684713734237),
                triggerBin(40.0, 0.16975308642, 0.00851460183924),
                triggerBin(50.0, 0.221086261981, 0.0104898285359),
                triggerBin(60.0, 0.297052154195, 0.0125631337438),
                triggerBin(70.0, 0.355614973262, 0.0142911214866),
                triggerBin(80.0, 0.553372278279, 0.0114566165432),
                triggerBin(100.0, 0.758339006127, 0.011169251709),
                triggerBin(120.0, 0.891047297297, 0.0090551058501),
                triggerBin(140.0, 0.96379525593, 0.00660022703963),
                triggerBin(160.0, 0.996268656716, 0.00263353104176),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0948905109489, 0.00590154082045),
                triggerBin(30.0, 0.120407259849, 0.00684713734237),
                triggerBin(40.0, 0.16975308642, 0.00851460183924),
                triggerBin(50.0, 0.221086261981, 0.0104898285359),
                triggerBin(60.0, 0.297052154195, 0.0125631337438),
                triggerBin(70.0, 0.355614973262, 0.0142911214866),
                triggerBin(80.0, 0.553372278279, 0.0114566165432),
                triggerBin(100.0, 0.758339006127, 0.011169251709),
                triggerBin(120.0, 0.891047297297, 0.0090551058501),
                triggerBin(140.0, 0.96379525593, 0.00660022703963),
                triggerBin(160.0, 0.996268656716, 0.00263353104176),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012A"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

metLegEfficiency_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: (Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) >= 1&&Sum$(PFJetPt > 0&& PFJetPUIDtight) >= 3+Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5 && PFTauJetMinDR < 0.5))&& hPlusGlobalElectronVetoFilter > 0.5 && hPlusGlobalMuonVetoFilter > 0.5

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.166666666667, 0.152145154863),
                triggerBin(30.0, 0.0, 0.0),
                triggerBin(40.0, 0.0, 0.0),
                triggerBin(50.0, 0.5, 0.353553390593),
                triggerBin(60.0, 0.0, 1.0),
                triggerBin(70.0, 1.0, 0.0),
                triggerBin(80.0, 0.0, 1.0),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0454545454545, 0.0256398215826),
                triggerBin(30.0, 0.102040816327, 0.0432431398664),
                triggerBin(40.0, 0.176470588235, 0.0924594409404),
                triggerBin(50.0, 0.153846153846, 0.100068251629),
                triggerBin(60.0, 0.285714285714, 0.170746944191),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0430107526882, 0.0210378123074),
                triggerBin(30.0, 0.0566037735849, 0.0317418200429),
                triggerBin(40.0, 0.0857142857143, 0.047318781212),
                triggerBin(50.0, 0.1875, 0.097578093725),
                triggerBin(60.0, 0.222222222222, 0.138579903214),
                triggerBin(70.0, 0.428571428571, 0.187043905917),
                triggerBin(80.0, 0.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0309278350515, 0.0175778985147),
                triggerBin(30.0, 0.03125, 0.0217490795423),
                triggerBin(40.0, 0.142857142857, 0.0539949247156),
                triggerBin(50.0, 0.263157894737, 0.101022617888),
                triggerBin(60.0, 0.3, 0.144913767462),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 0.25, 0.216506350946),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0555555555556, 0.0269951476613),
                triggerBin(30.0, 0.0961538461538, 0.0408816970575),
                triggerBin(40.0, 0.166666666667, 0.0878410461158),
                triggerBin(50.0, 0.2, 0.103279555899),
                triggerBin(60.0, 0.285714285714, 0.170746944191),
                triggerBin(70.0, 0.666666666667, 0.272165526976),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.333333333333, 0.272165526976),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0484848484848, 0.0167212562875),
                triggerBin(30.0, 0.0761904761905, 0.0258908859729),
                triggerBin(40.0, 0.11320754717, 0.0435221909205),
                triggerBin(50.0, 0.193548387097, 0.0709582814619),
                triggerBin(60.0, 0.25, 0.108253175473),
                triggerBin(70.0, 0.5, 0.158113883008),
                triggerBin(80.0, 0.666666666667, 0.272165526976),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.5, 0.25),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0419847328244, 0.0123902841514),
                triggerBin(30.0, 0.0591715976331, 0.0181496604801),
                triggerBin(40.0, 0.126315789474, 0.0340835059358),
                triggerBin(50.0, 0.22, 0.0585832740635),
                triggerBin(60.0, 0.269230769231, 0.0869892924733),
                triggerBin(70.0, 0.357142857143, 0.128060208143),
                triggerBin(80.0, 0.428571428571, 0.187043905917),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.714285714286, 0.170746944191),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0909930715935, 0.00618100093225),
                triggerBin(30.0, 0.123799898939, 0.00740353097005),
                triggerBin(40.0, 0.16628440367, 0.00891582388659),
                triggerBin(50.0, 0.221586847748, 0.0111037126702),
                triggerBin(60.0, 0.297658862876, 0.0132211085982),
                triggerBin(70.0, 0.355685131195, 0.014923622154),
                triggerBin(80.0, 0.552752293578, 0.0119060060089),
                triggerBin(100.0, 0.758490566038, 0.0117580202181),
                triggerBin(120.0, 0.886216466235, 0.00965821278492),
                triggerBin(140.0, 0.962861072902, 0.00701341092931),
                triggerBin(160.0, 0.99593495935, 0.00286856954767),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0909930715935, 0.00618100093225),
                triggerBin(30.0, 0.123799898939, 0.00740353097005),
                triggerBin(40.0, 0.16628440367, 0.00891582388659),
                triggerBin(50.0, 0.221586847748, 0.0111037126702),
                triggerBin(60.0, 0.297658862876, 0.0132211085982),
                triggerBin(70.0, 0.355685131195, 0.014923622154),
                triggerBin(80.0, 0.552752293578, 0.0119060060089),
                triggerBin(100.0, 0.758490566038, 0.0117580202181),
                triggerBin(120.0, 0.886216466235, 0.00965821278492),
                triggerBin(140.0, 0.962861072902, 0.00701341092931),
                triggerBin(160.0, 0.99593495935, 0.00286856954767),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0909930715935, 0.00618100093225),
                triggerBin(30.0, 0.123799898939, 0.00740353097005),
                triggerBin(40.0, 0.16628440367, 0.00891582388659),
                triggerBin(50.0, 0.221586847748, 0.0111037126702),
                triggerBin(60.0, 0.297658862876, 0.0132211085982),
                triggerBin(70.0, 0.355685131195, 0.014923622154),
                triggerBin(80.0, 0.552752293578, 0.0119060060089),
                triggerBin(100.0, 0.758490566038, 0.0117580202181),
                triggerBin(120.0, 0.886216466235, 0.00965821278492),
                triggerBin(140.0, 0.962861072902, 0.00701341092931),
                triggerBin(160.0, 0.99593495935, 0.00286856954767),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0909930715935, 0.00618100093225),
                triggerBin(30.0, 0.123799898939, 0.00740353097005),
                triggerBin(40.0, 0.16628440367, 0.00891582388659),
                triggerBin(50.0, 0.221586847748, 0.0111037126702),
                triggerBin(60.0, 0.297658862876, 0.0132211085982),
                triggerBin(70.0, 0.355685131195, 0.014923622154),
                triggerBin(80.0, 0.552752293578, 0.0119060060089),
                triggerBin(100.0, 0.758490566038, 0.0117580202181),
                triggerBin(120.0, 0.886216466235, 0.00965821278492),
                triggerBin(140.0, 0.962861072902, 0.00701341092931),
                triggerBin(160.0, 0.99593495935, 0.00286856954767),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0909930715935, 0.00618100093225),
                triggerBin(30.0, 0.123799898939, 0.00740353097005),
                triggerBin(40.0, 0.16628440367, 0.00891582388659),
                triggerBin(50.0, 0.221586847748, 0.0111037126702),
                triggerBin(60.0, 0.297658862876, 0.0132211085982),
                triggerBin(70.0, 0.355685131195, 0.014923622154),
                triggerBin(80.0, 0.552752293578, 0.0119060060089),
                triggerBin(100.0, 0.758490566038, 0.0117580202181),
                triggerBin(120.0, 0.886216466235, 0.00965821278492),
                triggerBin(140.0, 0.962861072902, 0.00701341092931),
                triggerBin(160.0, 0.99593495935, 0.00286856954767),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0909930715935, 0.00618100093225),
                triggerBin(30.0, 0.123799898939, 0.00740353097005),
                triggerBin(40.0, 0.16628440367, 0.00891582388659),
                triggerBin(50.0, 0.221586847748, 0.0111037126702),
                triggerBin(60.0, 0.297658862876, 0.0132211085982),
                triggerBin(70.0, 0.355685131195, 0.014923622154),
                triggerBin(80.0, 0.552752293578, 0.0119060060089),
                triggerBin(100.0, 0.758490566038, 0.0117580202181),
                triggerBin(120.0, 0.886216466235, 0.00965821278492),
                triggerBin(140.0, 0.962861072902, 0.00701341092931),
                triggerBin(160.0, 0.99593495935, 0.00286856954767),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0909930715935, 0.00618100093225),
                triggerBin(30.0, 0.123799898939, 0.00740353097005),
                triggerBin(40.0, 0.16628440367, 0.00891582388659),
                triggerBin(50.0, 0.221586847748, 0.0111037126702),
                triggerBin(60.0, 0.297658862876, 0.0132211085982),
                triggerBin(70.0, 0.355685131195, 0.014923622154),
                triggerBin(80.0, 0.552752293578, 0.0119060060089),
                triggerBin(100.0, 0.758490566038, 0.0117580202181),
                triggerBin(120.0, 0.886216466235, 0.00965821278492),
                triggerBin(140.0, 0.962861072902, 0.00701341092931),
                triggerBin(160.0, 0.99593495935, 0.00286856954767),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0909930715935, 0.00618100093225),
                triggerBin(30.0, 0.123799898939, 0.00740353097005),
                triggerBin(40.0, 0.16628440367, 0.00891582388659),
                triggerBin(50.0, 0.221586847748, 0.0111037126702),
                triggerBin(60.0, 0.297658862876, 0.0132211085982),
                triggerBin(70.0, 0.355685131195, 0.014923622154),
                triggerBin(80.0, 0.552752293578, 0.0119060060089),
                triggerBin(100.0, 0.758490566038, 0.0117580202181),
                triggerBin(120.0, 0.886216466235, 0.00965821278492),
                triggerBin(140.0, 0.962861072902, 0.00701341092931),
                triggerBin(160.0, 0.99593495935, 0.00286856954767),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012A"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

metLegEfficiency_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: (Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5) >= 1&&Sum$(PFJetPt > 0&& PFJetPUIDtight) >= 3+Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5 && PFTauJetMinDR < 0.5))&& hPlusGlobalElectronVetoFilter > 0.5 && hPlusGlobalMuonVetoFilter > 0.5

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0909090909091, 0.0866784172041),
                triggerBin(30.0, 0.0, 0.0),
                triggerBin(40.0, 0.0, 0.0),
                triggerBin(50.0, 0.5, 0.353553390593),
                triggerBin(60.0, 0.0, 1.0),
                triggerBin(70.0, 1.0, 0.0),
                triggerBin(80.0, 0.0, 1.0),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.036036036036, 0.017690390363),
                triggerBin(30.0, 0.0681818181818, 0.0268694355447),
                triggerBin(40.0, 0.125, 0.0522912516584),
                triggerBin(50.0, 0.176470588235, 0.0653786976737),
                triggerBin(60.0, 0.4, 0.154919333848),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 0.75, 0.216506350946),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.333333333333, 0.272165526976),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0280898876404, 0.0123844878174),
                triggerBin(30.0, 0.0660377358491, 0.0241216948646),
                triggerBin(40.0, 0.0588235294118, 0.0285336029454),
                triggerBin(50.0, 0.1, 0.0547722557505),
                triggerBin(60.0, 0.266666666667, 0.114179845144),
                triggerBin(70.0, 0.444444444444, 0.165634665),
                triggerBin(80.0, 0.333333333333, 0.272165526976),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.75, 0.216506350946),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.048128342246, 0.0156519642065),
                triggerBin(30.0, 0.0575539568345, 0.0197541542643),
                triggerBin(40.0, 0.120481927711, 0.0357309276458),
                triggerBin(50.0, 0.139534883721, 0.0528413377526),
                triggerBin(60.0, 0.263157894737, 0.101022617888),
                triggerBin(70.0, 0.166666666667, 0.152145154863),
                triggerBin(80.0, 0.333333333333, 0.19245008973),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0409836065574, 0.0179489144269),
                triggerBin(30.0, 0.0652173913043, 0.0257420488306),
                triggerBin(40.0, 0.121951219512, 0.051104655788),
                triggerBin(50.0, 0.194444444444, 0.0659620687443),
                triggerBin(60.0, 0.4, 0.154919333848),
                triggerBin(70.0, 0.666666666667, 0.272165526976),
                triggerBin(80.0, 0.75, 0.216506350946),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.5, 0.25),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0333333333333, 0.0103637545034),
                triggerBin(30.0, 0.0656565656566, 0.0176019083336),
                triggerBin(40.0, 0.0825688073394, 0.0263621913364),
                triggerBin(50.0, 0.151515151515, 0.044134489773),
                triggerBin(60.0, 0.32, 0.0932952303175),
                triggerBin(70.0, 0.5, 0.144337567297),
                triggerBin(80.0, 0.571428571429, 0.187043905917),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.6, 0.219089023002),
                triggerBin(140.0, 0.75, 0.216506350946),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0390143737166, 0.00877417486016),
                triggerBin(30.0, 0.0623145400593, 0.0131676519108),
                triggerBin(40.0, 0.0989583333333, 0.0215500364459),
                triggerBin(50.0, 0.146788990826, 0.033897035539),
                triggerBin(60.0, 0.295454545455, 0.0687817954616),
                triggerBin(70.0, 0.388888888889, 0.114904385611),
                triggerBin(80.0, 0.461538461538, 0.138264159119),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.75, 0.153093108924),
                triggerBin(140.0, 0.75, 0.216506350946),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0953981385729, 0.0047234079498),
                triggerBin(30.0, 0.128985083358, 0.00573235384099),
                triggerBin(40.0, 0.178228388474, 0.00721827767243),
                triggerBin(50.0, 0.224231464738, 0.00886792060206),
                triggerBin(60.0, 0.304613674263, 0.0108510606044),
                triggerBin(70.0, 0.362433862434, 0.012362352117),
                triggerBin(80.0, 0.545418167267, 0.00996065067441),
                triggerBin(100.0, 0.76, 0.00986306240475),
                triggerBin(120.0, 0.891694352159, 0.00801060486832),
                triggerBin(140.0, 0.966052376334, 0.00563995570916),
                triggerBin(160.0, 0.997080291971, 0.00206152920855),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0953981385729, 0.0047234079498),
                triggerBin(30.0, 0.128985083358, 0.00573235384099),
                triggerBin(40.0, 0.178228388474, 0.00721827767243),
                triggerBin(50.0, 0.224231464738, 0.00886792060206),
                triggerBin(60.0, 0.304613674263, 0.0108510606044),
                triggerBin(70.0, 0.362433862434, 0.012362352117),
                triggerBin(80.0, 0.545418167267, 0.00996065067441),
                triggerBin(100.0, 0.76, 0.00986306240475),
                triggerBin(120.0, 0.891694352159, 0.00801060486832),
                triggerBin(140.0, 0.966052376334, 0.00563995570916),
                triggerBin(160.0, 0.997080291971, 0.00206152920855),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0953981385729, 0.0047234079498),
                triggerBin(30.0, 0.128985083358, 0.00573235384099),
                triggerBin(40.0, 0.178228388474, 0.00721827767243),
                triggerBin(50.0, 0.224231464738, 0.00886792060206),
                triggerBin(60.0, 0.304613674263, 0.0108510606044),
                triggerBin(70.0, 0.362433862434, 0.012362352117),
                triggerBin(80.0, 0.545418167267, 0.00996065067441),
                triggerBin(100.0, 0.76, 0.00986306240475),
                triggerBin(120.0, 0.891694352159, 0.00801060486832),
                triggerBin(140.0, 0.966052376334, 0.00563995570916),
                triggerBin(160.0, 0.997080291971, 0.00206152920855),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0953981385729, 0.0047234079498),
                triggerBin(30.0, 0.128985083358, 0.00573235384099),
                triggerBin(40.0, 0.178228388474, 0.00721827767243),
                triggerBin(50.0, 0.224231464738, 0.00886792060206),
                triggerBin(60.0, 0.304613674263, 0.0108510606044),
                triggerBin(70.0, 0.362433862434, 0.012362352117),
                triggerBin(80.0, 0.545418167267, 0.00996065067441),
                triggerBin(100.0, 0.76, 0.00986306240475),
                triggerBin(120.0, 0.891694352159, 0.00801060486832),
                triggerBin(140.0, 0.966052376334, 0.00563995570916),
                triggerBin(160.0, 0.997080291971, 0.00206152920855),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0953981385729, 0.0047234079498),
                triggerBin(30.0, 0.128985083358, 0.00573235384099),
                triggerBin(40.0, 0.178228388474, 0.00721827767243),
                triggerBin(50.0, 0.224231464738, 0.00886792060206),
                triggerBin(60.0, 0.304613674263, 0.0108510606044),
                triggerBin(70.0, 0.362433862434, 0.012362352117),
                triggerBin(80.0, 0.545418167267, 0.00996065067441),
                triggerBin(100.0, 0.76, 0.00986306240475),
                triggerBin(120.0, 0.891694352159, 0.00801060486832),
                triggerBin(140.0, 0.966052376334, 0.00563995570916),
                triggerBin(160.0, 0.997080291971, 0.00206152920855),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0953981385729, 0.0047234079498),
                triggerBin(30.0, 0.128985083358, 0.00573235384099),
                triggerBin(40.0, 0.178228388474, 0.00721827767243),
                triggerBin(50.0, 0.224231464738, 0.00886792060206),
                triggerBin(60.0, 0.304613674263, 0.0108510606044),
                triggerBin(70.0, 0.362433862434, 0.012362352117),
                triggerBin(80.0, 0.545418167267, 0.00996065067441),
                triggerBin(100.0, 0.76, 0.00986306240475),
                triggerBin(120.0, 0.891694352159, 0.00801060486832),
                triggerBin(140.0, 0.966052376334, 0.00563995570916),
                triggerBin(160.0, 0.997080291971, 0.00206152920855),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0953981385729, 0.0047234079498),
                triggerBin(30.0, 0.128985083358, 0.00573235384099),
                triggerBin(40.0, 0.178228388474, 0.00721827767243),
                triggerBin(50.0, 0.224231464738, 0.00886792060206),
                triggerBin(60.0, 0.304613674263, 0.0108510606044),
                triggerBin(70.0, 0.362433862434, 0.012362352117),
                triggerBin(80.0, 0.545418167267, 0.00996065067441),
                triggerBin(100.0, 0.76, 0.00986306240475),
                triggerBin(120.0, 0.891694352159, 0.00801060486832),
                triggerBin(140.0, 0.966052376334, 0.00563995570916),
                triggerBin(160.0, 0.997080291971, 0.00206152920855),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0953981385729, 0.0047234079498),
                triggerBin(30.0, 0.128985083358, 0.00573235384099),
                triggerBin(40.0, 0.178228388474, 0.00721827767243),
                triggerBin(50.0, 0.224231464738, 0.00886792060206),
                triggerBin(60.0, 0.304613674263, 0.0108510606044),
                triggerBin(70.0, 0.362433862434, 0.012362352117),
                triggerBin(80.0, 0.545418167267, 0.00996065067441),
                triggerBin(100.0, 0.76, 0.00986306240475),
                triggerBin(120.0, 0.891694352159, 0.00801060486832),
                triggerBin(140.0, 0.966052376334, 0.00563995570916),
                triggerBin(160.0, 0.997080291971, 0.00206152920855),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012A"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

metLegEfficiency_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: (Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5) >= 1&&Sum$(PFJetPt > 0&& PFJetPUIDtight) >= 3+Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5 && PFTauJetMinDR < 0.5))&& hPlusGlobalElectronVetoFilter > 0.5 && hPlusGlobalMuonVetoFilter > 0.5

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.142857142857, 0.132260014253),
                triggerBin(30.0, 0.0, 0.0),
                triggerBin(40.0, 0.0, 0.0),
                triggerBin(50.0, 0.5, 0.353553390593),
                triggerBin(60.0, 0.0, 1.0),
                triggerBin(70.0, 1.0, 0.0),
                triggerBin(80.0, 0.0, 1.0),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.041095890411, 0.0232340734086),
                triggerBin(30.0, 0.111111111111, 0.0427666866066),
                triggerBin(40.0, 0.142857142857, 0.0763603548321),
                triggerBin(50.0, 0.176470588235, 0.0924594409404),
                triggerBin(60.0, 0.285714285714, 0.170746944191),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.333333333333, 0.272165526976),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0380952380952, 0.0186812844796),
                triggerBin(30.0, 0.0545454545455, 0.0306209221207),
                triggerBin(40.0, 0.0789473684211, 0.043744076724),
                triggerBin(50.0, 0.15, 0.0798435971133),
                triggerBin(60.0, 0.222222222222, 0.138579903214),
                triggerBin(70.0, 0.428571428571, 0.187043905917),
                triggerBin(80.0, 0.5, 0.353553390593),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0373831775701, 0.0183388856062),
                triggerBin(30.0, 0.027397260274, 0.0191055648508),
                triggerBin(40.0, 0.139534883721, 0.0528413377526),
                triggerBin(50.0, 0.227272727273, 0.0893460673985),
                triggerBin(60.0, 0.3, 0.144913767462),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 0.25, 0.216506350946),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.05, 0.024366985862),
                triggerBin(30.0, 0.105263157895, 0.0406488655643),
                triggerBin(40.0, 0.136363636364, 0.0731650049984),
                triggerBin(50.0, 0.210526315789, 0.0935287701725),
                triggerBin(60.0, 0.285714285714, 0.170746944191),
                triggerBin(70.0, 0.666666666667, 0.272165526976),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.5, 0.25),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0432432432432, 0.0149545735853),
                triggerBin(30.0, 0.0803571428571, 0.0256869673127),
                triggerBin(40.0, 0.1, 0.0387298334621),
                triggerBin(50.0, 0.179487179487, 0.0614507373862),
                triggerBin(60.0, 0.25, 0.108253175473),
                triggerBin(70.0, 0.5, 0.158113883008),
                triggerBin(80.0, 0.75, 0.216506350946),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.6, 0.219089023002),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.041095890411, 0.0116170367043),
                triggerBin(30.0, 0.0594594594595, 0.0173865484103),
                triggerBin(40.0, 0.116504854369, 0.0316122554085),
                triggerBin(50.0, 0.196721311475, 0.0508972022624),
                triggerBin(60.0, 0.269230769231, 0.0869892924733),
                triggerBin(70.0, 0.357142857143, 0.128060208143),
                triggerBin(80.0, 0.5, 0.176776695297),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.75, 0.153093108924),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0947154471545, 0.00590385127247),
                triggerBin(30.0, 0.119555555556, 0.00683981886347),
                triggerBin(40.0, 0.168475452196, 0.00850874225011),
                triggerBin(50.0, 0.219151670951, 0.0104869920671),
                triggerBin(60.0, 0.29604261796, 0.0125936789945),
                triggerBin(70.0, 0.354203935599, 0.0143038677609),
                triggerBin(80.0, 0.551871657754, 0.0115000425742),
                triggerBin(100.0, 0.757513661202, 0.0112012975651),
                triggerBin(120.0, 0.890862944162, 0.0090694891571),
                triggerBin(140.0, 0.96379525593, 0.00660022703963),
                triggerBin(160.0, 0.996254681648, 0.00264337591385),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0947154471545, 0.00590385127247),
                triggerBin(30.0, 0.119555555556, 0.00683981886347),
                triggerBin(40.0, 0.168475452196, 0.00850874225011),
                triggerBin(50.0, 0.219151670951, 0.0104869920671),
                triggerBin(60.0, 0.29604261796, 0.0125936789945),
                triggerBin(70.0, 0.354203935599, 0.0143038677609),
                triggerBin(80.0, 0.551871657754, 0.0115000425742),
                triggerBin(100.0, 0.757513661202, 0.0112012975651),
                triggerBin(120.0, 0.890862944162, 0.0090694891571),
                triggerBin(140.0, 0.96379525593, 0.00660022703963),
                triggerBin(160.0, 0.996254681648, 0.00264337591385),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0947154471545, 0.00590385127247),
                triggerBin(30.0, 0.119555555556, 0.00683981886347),
                triggerBin(40.0, 0.168475452196, 0.00850874225011),
                triggerBin(50.0, 0.219151670951, 0.0104869920671),
                triggerBin(60.0, 0.29604261796, 0.0125936789945),
                triggerBin(70.0, 0.354203935599, 0.0143038677609),
                triggerBin(80.0, 0.551871657754, 0.0115000425742),
                triggerBin(100.0, 0.757513661202, 0.0112012975651),
                triggerBin(120.0, 0.890862944162, 0.0090694891571),
                triggerBin(140.0, 0.96379525593, 0.00660022703963),
                triggerBin(160.0, 0.996254681648, 0.00264337591385),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0947154471545, 0.00590385127247),
                triggerBin(30.0, 0.119555555556, 0.00683981886347),
                triggerBin(40.0, 0.168475452196, 0.00850874225011),
                triggerBin(50.0, 0.219151670951, 0.0104869920671),
                triggerBin(60.0, 0.29604261796, 0.0125936789945),
                triggerBin(70.0, 0.354203935599, 0.0143038677609),
                triggerBin(80.0, 0.551871657754, 0.0115000425742),
                triggerBin(100.0, 0.757513661202, 0.0112012975651),
                triggerBin(120.0, 0.890862944162, 0.0090694891571),
                triggerBin(140.0, 0.96379525593, 0.00660022703963),
                triggerBin(160.0, 0.996254681648, 0.00264337591385),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0947154471545, 0.00590385127247),
                triggerBin(30.0, 0.119555555556, 0.00683981886347),
                triggerBin(40.0, 0.168475452196, 0.00850874225011),
                triggerBin(50.0, 0.219151670951, 0.0104869920671),
                triggerBin(60.0, 0.29604261796, 0.0125936789945),
                triggerBin(70.0, 0.354203935599, 0.0143038677609),
                triggerBin(80.0, 0.551871657754, 0.0115000425742),
                triggerBin(100.0, 0.757513661202, 0.0112012975651),
                triggerBin(120.0, 0.890862944162, 0.0090694891571),
                triggerBin(140.0, 0.96379525593, 0.00660022703963),
                triggerBin(160.0, 0.996254681648, 0.00264337591385),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0947154471545, 0.00590385127247),
                triggerBin(30.0, 0.119555555556, 0.00683981886347),
                triggerBin(40.0, 0.168475452196, 0.00850874225011),
                triggerBin(50.0, 0.219151670951, 0.0104869920671),
                triggerBin(60.0, 0.29604261796, 0.0125936789945),
                triggerBin(70.0, 0.354203935599, 0.0143038677609),
                triggerBin(80.0, 0.551871657754, 0.0115000425742),
                triggerBin(100.0, 0.757513661202, 0.0112012975651),
                triggerBin(120.0, 0.890862944162, 0.0090694891571),
                triggerBin(140.0, 0.96379525593, 0.00660022703963),
                triggerBin(160.0, 0.996254681648, 0.00264337591385),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0947154471545, 0.00590385127247),
                triggerBin(30.0, 0.119555555556, 0.00683981886347),
                triggerBin(40.0, 0.168475452196, 0.00850874225011),
                triggerBin(50.0, 0.219151670951, 0.0104869920671),
                triggerBin(60.0, 0.29604261796, 0.0125936789945),
                triggerBin(70.0, 0.354203935599, 0.0143038677609),
                triggerBin(80.0, 0.551871657754, 0.0115000425742),
                triggerBin(100.0, 0.757513661202, 0.0112012975651),
                triggerBin(120.0, 0.890862944162, 0.0090694891571),
                triggerBin(140.0, 0.96379525593, 0.00660022703963),
                triggerBin(160.0, 0.996254681648, 0.00264337591385),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0947154471545, 0.00590385127247),
                triggerBin(30.0, 0.119555555556, 0.00683981886347),
                triggerBin(40.0, 0.168475452196, 0.00850874225011),
                triggerBin(50.0, 0.219151670951, 0.0104869920671),
                triggerBin(60.0, 0.29604261796, 0.0125936789945),
                triggerBin(70.0, 0.354203935599, 0.0143038677609),
                triggerBin(80.0, 0.551871657754, 0.0115000425742),
                triggerBin(100.0, 0.757513661202, 0.0112012975651),
                triggerBin(120.0, 0.890862944162, 0.0090694891571),
                triggerBin(140.0, 0.96379525593, 0.00660022703963),
                triggerBin(160.0, 0.996254681648, 0.00264337591385),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012A"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

metLegEfficiency_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: (Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) >= 1&&Sum$(PFJetPt > 0&& PFJetPUIDtight) >= 3+Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5 && PFTauJetMinDR < 0.5))&& hPlusGlobalElectronVetoFilter > 0.5 && hPlusGlobalMuonVetoFilter > 0.5

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.166666666667, 0.152145154863),
                triggerBin(30.0, 0.0, 0.0),
                triggerBin(40.0, 0.0, 0.0),
                triggerBin(50.0, 0.5, 0.353553390593),
                triggerBin(60.0, 0.0, 1.0),
                triggerBin(70.0, 1.0, 0.0),
                triggerBin(80.0, 0.0, 1.0),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0454545454545, 0.0256398215826),
                triggerBin(30.0, 0.102040816327, 0.0432431398664),
                triggerBin(40.0, 0.176470588235, 0.0924594409404),
                triggerBin(50.0, 0.153846153846, 0.100068251629),
                triggerBin(60.0, 0.285714285714, 0.170746944191),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0430107526882, 0.0210378123074),
                triggerBin(30.0, 0.0566037735849, 0.0317418200429),
                triggerBin(40.0, 0.0857142857143, 0.047318781212),
                triggerBin(50.0, 0.1875, 0.097578093725),
                triggerBin(60.0, 0.222222222222, 0.138579903214),
                triggerBin(70.0, 0.428571428571, 0.187043905917),
                triggerBin(80.0, 0.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0309278350515, 0.0175778985147),
                triggerBin(30.0, 0.03125, 0.0217490795423),
                triggerBin(40.0, 0.142857142857, 0.0539949247156),
                triggerBin(50.0, 0.263157894737, 0.101022617888),
                triggerBin(60.0, 0.3, 0.144913767462),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 0.25, 0.216506350946),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0555555555556, 0.0269951476613),
                triggerBin(30.0, 0.0961538461538, 0.0408816970575),
                triggerBin(40.0, 0.166666666667, 0.0878410461158),
                triggerBin(50.0, 0.2, 0.103279555899),
                triggerBin(60.0, 0.285714285714, 0.170746944191),
                triggerBin(70.0, 0.666666666667, 0.272165526976),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.333333333333, 0.272165526976),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0484848484848, 0.0167212562875),
                triggerBin(30.0, 0.0761904761905, 0.0258908859729),
                triggerBin(40.0, 0.11320754717, 0.0435221909205),
                triggerBin(50.0, 0.193548387097, 0.0709582814619),
                triggerBin(60.0, 0.25, 0.108253175473),
                triggerBin(70.0, 0.5, 0.158113883008),
                triggerBin(80.0, 0.666666666667, 0.272165526976),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.5, 0.25),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0419847328244, 0.0123902841514),
                triggerBin(30.0, 0.0591715976331, 0.0181496604801),
                triggerBin(40.0, 0.126315789474, 0.0340835059358),
                triggerBin(50.0, 0.22, 0.0585832740635),
                triggerBin(60.0, 0.269230769231, 0.0869892924733),
                triggerBin(70.0, 0.357142857143, 0.128060208143),
                triggerBin(80.0, 0.428571428571, 0.187043905917),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.714285714286, 0.170746944191),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0911614993059, 0.00619186821558),
                triggerBin(30.0, 0.122780314561, 0.00739222612351),
                triggerBin(40.0, 0.164746543779, 0.00890312429278),
                triggerBin(50.0, 0.219266714594, 0.0110936417585),
                triggerBin(60.0, 0.296888141295, 0.013250055869),
                triggerBin(70.0, 0.354146341463, 0.0149381394437),
                triggerBin(80.0, 0.550808314088, 0.0119520432032),
                triggerBin(100.0, 0.757759273278, 0.011787936874),
                triggerBin(120.0, 0.886005560704, 0.0096749634904),
                triggerBin(140.0, 0.962861072902, 0.00701341092931),
                triggerBin(160.0, 0.995918367347, 0.00288025400239),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0911614993059, 0.00619186821558),
                triggerBin(30.0, 0.122780314561, 0.00739222612351),
                triggerBin(40.0, 0.164746543779, 0.00890312429278),
                triggerBin(50.0, 0.219266714594, 0.0110936417585),
                triggerBin(60.0, 0.296888141295, 0.013250055869),
                triggerBin(70.0, 0.354146341463, 0.0149381394437),
                triggerBin(80.0, 0.550808314088, 0.0119520432032),
                triggerBin(100.0, 0.757759273278, 0.011787936874),
                triggerBin(120.0, 0.886005560704, 0.0096749634904),
                triggerBin(140.0, 0.962861072902, 0.00701341092931),
                triggerBin(160.0, 0.995918367347, 0.00288025400239),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0911614993059, 0.00619186821558),
                triggerBin(30.0, 0.122780314561, 0.00739222612351),
                triggerBin(40.0, 0.164746543779, 0.00890312429278),
                triggerBin(50.0, 0.219266714594, 0.0110936417585),
                triggerBin(60.0, 0.296888141295, 0.013250055869),
                triggerBin(70.0, 0.354146341463, 0.0149381394437),
                triggerBin(80.0, 0.550808314088, 0.0119520432032),
                triggerBin(100.0, 0.757759273278, 0.011787936874),
                triggerBin(120.0, 0.886005560704, 0.0096749634904),
                triggerBin(140.0, 0.962861072902, 0.00701341092931),
                triggerBin(160.0, 0.995918367347, 0.00288025400239),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0911614993059, 0.00619186821558),
                triggerBin(30.0, 0.122780314561, 0.00739222612351),
                triggerBin(40.0, 0.164746543779, 0.00890312429278),
                triggerBin(50.0, 0.219266714594, 0.0110936417585),
                triggerBin(60.0, 0.296888141295, 0.013250055869),
                triggerBin(70.0, 0.354146341463, 0.0149381394437),
                triggerBin(80.0, 0.550808314088, 0.0119520432032),
                triggerBin(100.0, 0.757759273278, 0.011787936874),
                triggerBin(120.0, 0.886005560704, 0.0096749634904),
                triggerBin(140.0, 0.962861072902, 0.00701341092931),
                triggerBin(160.0, 0.995918367347, 0.00288025400239),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0911614993059, 0.00619186821558),
                triggerBin(30.0, 0.122780314561, 0.00739222612351),
                triggerBin(40.0, 0.164746543779, 0.00890312429278),
                triggerBin(50.0, 0.219266714594, 0.0110936417585),
                triggerBin(60.0, 0.296888141295, 0.013250055869),
                triggerBin(70.0, 0.354146341463, 0.0149381394437),
                triggerBin(80.0, 0.550808314088, 0.0119520432032),
                triggerBin(100.0, 0.757759273278, 0.011787936874),
                triggerBin(120.0, 0.886005560704, 0.0096749634904),
                triggerBin(140.0, 0.962861072902, 0.00701341092931),
                triggerBin(160.0, 0.995918367347, 0.00288025400239),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0911614993059, 0.00619186821558),
                triggerBin(30.0, 0.122780314561, 0.00739222612351),
                triggerBin(40.0, 0.164746543779, 0.00890312429278),
                triggerBin(50.0, 0.219266714594, 0.0110936417585),
                triggerBin(60.0, 0.296888141295, 0.013250055869),
                triggerBin(70.0, 0.354146341463, 0.0149381394437),
                triggerBin(80.0, 0.550808314088, 0.0119520432032),
                triggerBin(100.0, 0.757759273278, 0.011787936874),
                triggerBin(120.0, 0.886005560704, 0.0096749634904),
                triggerBin(140.0, 0.962861072902, 0.00701341092931),
                triggerBin(160.0, 0.995918367347, 0.00288025400239),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0911614993059, 0.00619186821558),
                triggerBin(30.0, 0.122780314561, 0.00739222612351),
                triggerBin(40.0, 0.164746543779, 0.00890312429278),
                triggerBin(50.0, 0.219266714594, 0.0110936417585),
                triggerBin(60.0, 0.296888141295, 0.013250055869),
                triggerBin(70.0, 0.354146341463, 0.0149381394437),
                triggerBin(80.0, 0.550808314088, 0.0119520432032),
                triggerBin(100.0, 0.757759273278, 0.011787936874),
                triggerBin(120.0, 0.886005560704, 0.0096749634904),
                triggerBin(140.0, 0.962861072902, 0.00701341092931),
                triggerBin(160.0, 0.995918367347, 0.00288025400239),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0911614993059, 0.00619186821558),
                triggerBin(30.0, 0.122780314561, 0.00739222612351),
                triggerBin(40.0, 0.164746543779, 0.00890312429278),
                triggerBin(50.0, 0.219266714594, 0.0110936417585),
                triggerBin(60.0, 0.296888141295, 0.013250055869),
                triggerBin(70.0, 0.354146341463, 0.0149381394437),
                triggerBin(80.0, 0.550808314088, 0.0119520432032),
                triggerBin(100.0, 0.757759273278, 0.011787936874),
                triggerBin(120.0, 0.886005560704, 0.0096749634904),
                triggerBin(140.0, 0.962861072902, 0.00701341092931),
                triggerBin(160.0, 0.995918367347, 0.00288025400239),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012A"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

metLegEfficiency_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronVTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: (Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5) >= 1&&Sum$(PFJetPt > 0&& PFJetPUIDtight) >= 3+Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5 && PFTauJetMinDR < 0.5))&& hPlusGlobalElectronVetoFilter > 0.5 && hPlusGlobalMuonVetoFilter > 0.5

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0909090909091, 0.0866784172041),
                triggerBin(30.0, 0.0, 0.0),
                triggerBin(40.0, 0.0, 0.0),
                triggerBin(50.0, 1.0, 0.0),
                triggerBin(60.0, 0.0, 1.0),
                triggerBin(70.0, 1.0, 0.0),
                triggerBin(80.0, 0.0, 1.0),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0388349514563, 0.0190367039454),
                triggerBin(30.0, 0.0609756097561, 0.0264246708383),
                triggerBin(40.0, 0.135135135135, 0.0562027291795),
                triggerBin(50.0, 0.161290322581, 0.0660585650285),
                triggerBin(60.0, 0.4, 0.154919333848),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.333333333333, 0.272165526976),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0308641975309, 0.0135882117669),
                triggerBin(30.0, 0.06, 0.0237486841741),
                triggerBin(40.0, 0.0634920634921, 0.0307216952878),
                triggerBin(50.0, 0.12, 0.0649923072371),
                triggerBin(60.0, 0.266666666667, 0.114179845144),
                triggerBin(70.0, 0.5, 0.176776695297),
                triggerBin(80.0, 0.5, 0.353553390593),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.666666666667, 0.272165526976),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0487804878049, 0.0168206014463),
                triggerBin(30.0, 0.0578512396694, 0.0212238120087),
                triggerBin(40.0, 0.116883116883, 0.036613363161),
                triggerBin(50.0, 0.135135135135, 0.0562027291795),
                triggerBin(60.0, 0.263157894737, 0.101022617888),
                triggerBin(70.0, 0.166666666667, 0.152145154863),
                triggerBin(80.0, 0.2, 0.1788854382),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0438596491228, 0.0191796630922),
                triggerBin(30.0, 0.0581395348837, 0.0252336360438),
                triggerBin(40.0, 0.131578947368, 0.0548361022017),
                triggerBin(50.0, 0.1875, 0.0689981317682),
                triggerBin(60.0, 0.4, 0.154919333848),
                triggerBin(70.0, 0.666666666667, 0.272165526976),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.5, 0.25),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.036231884058, 0.0112480488865),
                triggerBin(30.0, 0.0591397849462, 0.0172960109116),
                triggerBin(40.0, 0.0891089108911, 0.0283486973684),
                triggerBin(50.0, 0.157894736842, 0.0482980492359),
                triggerBin(60.0, 0.32, 0.0932952303175),
                triggerBin(70.0, 0.545454545455, 0.150131422517),
                triggerBin(80.0, 0.8, 0.1788854382),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.6, 0.219089023002),
                triggerBin(140.0, 0.666666666667, 0.272165526976),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0409090909091, 0.00944307552824),
                triggerBin(30.0, 0.0586319218241, 0.0134084201713),
                triggerBin(40.0, 0.101123595506, 0.0225978041513),
                triggerBin(50.0, 0.148936170213, 0.0367212309473),
                triggerBin(60.0, 0.295454545455, 0.0687817954616),
                triggerBin(70.0, 0.411764705882, 0.119364624987),
                triggerBin(80.0, 0.5, 0.158113883008),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.75, 0.153093108924),
                triggerBin(140.0, 0.666666666667, 0.272165526976),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0950071326676, 0.00495286707585),
                triggerBin(30.0, 0.129011345219, 0.00603521320145),
                triggerBin(40.0, 0.180372381691, 0.00757271923777),
                triggerBin(50.0, 0.225427872861, 0.00924034279464),
                triggerBin(60.0, 0.301818181818, 0.0113009510713),
                triggerBin(70.0, 0.363702096891, 0.0129357632474),
                triggerBin(80.0, 0.547423126895, 0.0103584740603),
                triggerBin(100.0, 0.758299359348, 0.0103317549682),
                triggerBin(120.0, 0.888332140301, 0.00842662331759),
                triggerBin(140.0, 0.967230443975, 0.00578834874628),
                triggerBin(160.0, 0.996855345912, 0.00222010724099),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0950071326676, 0.00495286707585),
                triggerBin(30.0, 0.129011345219, 0.00603521320145),
                triggerBin(40.0, 0.180372381691, 0.00757271923777),
                triggerBin(50.0, 0.225427872861, 0.00924034279464),
                triggerBin(60.0, 0.301818181818, 0.0113009510713),
                triggerBin(70.0, 0.363702096891, 0.0129357632474),
                triggerBin(80.0, 0.547423126895, 0.0103584740603),
                triggerBin(100.0, 0.758299359348, 0.0103317549682),
                triggerBin(120.0, 0.888332140301, 0.00842662331759),
                triggerBin(140.0, 0.967230443975, 0.00578834874628),
                triggerBin(160.0, 0.996855345912, 0.00222010724099),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0950071326676, 0.00495286707585),
                triggerBin(30.0, 0.129011345219, 0.00603521320145),
                triggerBin(40.0, 0.180372381691, 0.00757271923777),
                triggerBin(50.0, 0.225427872861, 0.00924034279464),
                triggerBin(60.0, 0.301818181818, 0.0113009510713),
                triggerBin(70.0, 0.363702096891, 0.0129357632474),
                triggerBin(80.0, 0.547423126895, 0.0103584740603),
                triggerBin(100.0, 0.758299359348, 0.0103317549682),
                triggerBin(120.0, 0.888332140301, 0.00842662331759),
                triggerBin(140.0, 0.967230443975, 0.00578834874628),
                triggerBin(160.0, 0.996855345912, 0.00222010724099),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0950071326676, 0.00495286707585),
                triggerBin(30.0, 0.129011345219, 0.00603521320145),
                triggerBin(40.0, 0.180372381691, 0.00757271923777),
                triggerBin(50.0, 0.225427872861, 0.00924034279464),
                triggerBin(60.0, 0.301818181818, 0.0113009510713),
                triggerBin(70.0, 0.363702096891, 0.0129357632474),
                triggerBin(80.0, 0.547423126895, 0.0103584740603),
                triggerBin(100.0, 0.758299359348, 0.0103317549682),
                triggerBin(120.0, 0.888332140301, 0.00842662331759),
                triggerBin(140.0, 0.967230443975, 0.00578834874628),
                triggerBin(160.0, 0.996855345912, 0.00222010724099),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0950071326676, 0.00495286707585),
                triggerBin(30.0, 0.129011345219, 0.00603521320145),
                triggerBin(40.0, 0.180372381691, 0.00757271923777),
                triggerBin(50.0, 0.225427872861, 0.00924034279464),
                triggerBin(60.0, 0.301818181818, 0.0113009510713),
                triggerBin(70.0, 0.363702096891, 0.0129357632474),
                triggerBin(80.0, 0.547423126895, 0.0103584740603),
                triggerBin(100.0, 0.758299359348, 0.0103317549682),
                triggerBin(120.0, 0.888332140301, 0.00842662331759),
                triggerBin(140.0, 0.967230443975, 0.00578834874628),
                triggerBin(160.0, 0.996855345912, 0.00222010724099),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0950071326676, 0.00495286707585),
                triggerBin(30.0, 0.129011345219, 0.00603521320145),
                triggerBin(40.0, 0.180372381691, 0.00757271923777),
                triggerBin(50.0, 0.225427872861, 0.00924034279464),
                triggerBin(60.0, 0.301818181818, 0.0113009510713),
                triggerBin(70.0, 0.363702096891, 0.0129357632474),
                triggerBin(80.0, 0.547423126895, 0.0103584740603),
                triggerBin(100.0, 0.758299359348, 0.0103317549682),
                triggerBin(120.0, 0.888332140301, 0.00842662331759),
                triggerBin(140.0, 0.967230443975, 0.00578834874628),
                triggerBin(160.0, 0.996855345912, 0.00222010724099),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0950071326676, 0.00495286707585),
                triggerBin(30.0, 0.129011345219, 0.00603521320145),
                triggerBin(40.0, 0.180372381691, 0.00757271923777),
                triggerBin(50.0, 0.225427872861, 0.00924034279464),
                triggerBin(60.0, 0.301818181818, 0.0113009510713),
                triggerBin(70.0, 0.363702096891, 0.0129357632474),
                triggerBin(80.0, 0.547423126895, 0.0103584740603),
                triggerBin(100.0, 0.758299359348, 0.0103317549682),
                triggerBin(120.0, 0.888332140301, 0.00842662331759),
                triggerBin(140.0, 0.967230443975, 0.00578834874628),
                triggerBin(160.0, 0.996855345912, 0.00222010724099),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0950071326676, 0.00495286707585),
                triggerBin(30.0, 0.129011345219, 0.00603521320145),
                triggerBin(40.0, 0.180372381691, 0.00757271923777),
                triggerBin(50.0, 0.225427872861, 0.00924034279464),
                triggerBin(60.0, 0.301818181818, 0.0113009510713),
                triggerBin(70.0, 0.363702096891, 0.0129357632474),
                triggerBin(80.0, 0.547423126895, 0.0103584740603),
                triggerBin(100.0, 0.758299359348, 0.0103317549682),
                triggerBin(120.0, 0.888332140301, 0.00842662331759),
                triggerBin(140.0, 0.967230443975, 0.00578834874628),
                triggerBin(160.0, 0.996855345912, 0.00222010724099),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012A"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

metLegEfficiency_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronVTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: (Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5) >= 1&&Sum$(PFJetPt > 0&& PFJetPUIDtight) >= 3+Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5 && PFTauJetMinDR < 0.5))&& hPlusGlobalElectronVetoFilter > 0.5 && hPlusGlobalMuonVetoFilter > 0.5

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.142857142857, 0.132260014253),
                triggerBin(30.0, 0.0, 0.0),
                triggerBin(40.0, 0.0, 0.0),
                triggerBin(50.0, 1.0, 0.0),
                triggerBin(60.0, 0.0, 1.0),
                triggerBin(70.0, 1.0, 0.0),
                triggerBin(80.0, 0.0, 1.0),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0441176470588, 0.0249031300527),
                triggerBin(30.0, 0.1, 0.0424264068712),
                triggerBin(40.0, 0.166666666667, 0.0878410461158),
                triggerBin(50.0, 0.142857142857, 0.0935219529583),
                triggerBin(60.0, 0.285714285714, 0.170746944191),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.333333333333, 0.272165526976),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0425531914894, 0.0208189810549),
                triggerBin(30.0, 0.0377358490566, 0.0261749753573),
                triggerBin(40.0, 0.0833333333333, 0.0460642331994),
                triggerBin(50.0, 0.1875, 0.097578093725),
                triggerBin(60.0, 0.222222222222, 0.138579903214),
                triggerBin(70.0, 0.5, 0.204124145232),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0449438202247, 0.0219611181558),
                triggerBin(30.0, 0.03125, 0.0217490795423),
                triggerBin(40.0, 0.128205128205, 0.0535337356629),
                triggerBin(50.0, 0.2, 0.0894427191),
                triggerBin(60.0, 0.3, 0.144913767462),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 0.0, 0.0),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0533333333333, 0.0259458124788),
                triggerBin(30.0, 0.0943396226415, 0.0401505793659),
                triggerBin(40.0, 0.157894736842, 0.083654675183),
                triggerBin(50.0, 0.2, 0.103279555899),
                triggerBin(60.0, 0.285714285714, 0.170746944191),
                triggerBin(70.0, 0.666666666667, 0.272165526976),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.5, 0.25),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0473372781065, 0.0163353285798),
                triggerBin(30.0, 0.0660377358491, 0.0241216948646),
                triggerBin(40.0, 0.109090909091, 0.0420367983048),
                triggerBin(50.0, 0.193548387097, 0.0709582814619),
                triggerBin(60.0, 0.25, 0.108253175473),
                triggerBin(70.0, 0.555555555556, 0.165634665),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.6, 0.219089023002),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.046511627907, 0.0131107826469),
                triggerBin(30.0, 0.0529411764706, 0.0171735789385),
                triggerBin(40.0, 0.117021276596, 0.0331545859316),
                triggerBin(50.0, 0.196078431373, 0.0555951190062),
                triggerBin(60.0, 0.269230769231, 0.0869892924733),
                triggerBin(70.0, 0.384615384615, 0.13493200297),
                triggerBin(80.0, 0.5, 0.204124145232),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.75, 0.153093108924),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0956014362657, 0.00622951946535),
                triggerBin(30.0, 0.121316306483, 0.00723580719943),
                triggerBin(40.0, 0.171637591446, 0.00894484219135),
                triggerBin(50.0, 0.219054242003, 0.0109070379935),
                triggerBin(60.0, 0.295901639344, 0.0130680394499),
                triggerBin(70.0, 0.356862745098, 0.0150003832062),
                triggerBin(80.0, 0.554140127389, 0.0119608715138),
                triggerBin(100.0, 0.755970149254, 0.0117333331362),
                triggerBin(120.0, 0.887773722628, 0.00953439509444),
                triggerBin(140.0, 0.964432284542, 0.00685023021524),
                triggerBin(160.0, 0.995975855131, 0.0028397690016),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0956014362657, 0.00622951946535),
                triggerBin(30.0, 0.121316306483, 0.00723580719943),
                triggerBin(40.0, 0.171637591446, 0.00894484219135),
                triggerBin(50.0, 0.219054242003, 0.0109070379935),
                triggerBin(60.0, 0.295901639344, 0.0130680394499),
                triggerBin(70.0, 0.356862745098, 0.0150003832062),
                triggerBin(80.0, 0.554140127389, 0.0119608715138),
                triggerBin(100.0, 0.755970149254, 0.0117333331362),
                triggerBin(120.0, 0.887773722628, 0.00953439509444),
                triggerBin(140.0, 0.964432284542, 0.00685023021524),
                triggerBin(160.0, 0.995975855131, 0.0028397690016),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0956014362657, 0.00622951946535),
                triggerBin(30.0, 0.121316306483, 0.00723580719943),
                triggerBin(40.0, 0.171637591446, 0.00894484219135),
                triggerBin(50.0, 0.219054242003, 0.0109070379935),
                triggerBin(60.0, 0.295901639344, 0.0130680394499),
                triggerBin(70.0, 0.356862745098, 0.0150003832062),
                triggerBin(80.0, 0.554140127389, 0.0119608715138),
                triggerBin(100.0, 0.755970149254, 0.0117333331362),
                triggerBin(120.0, 0.887773722628, 0.00953439509444),
                triggerBin(140.0, 0.964432284542, 0.00685023021524),
                triggerBin(160.0, 0.995975855131, 0.0028397690016),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0956014362657, 0.00622951946535),
                triggerBin(30.0, 0.121316306483, 0.00723580719943),
                triggerBin(40.0, 0.171637591446, 0.00894484219135),
                triggerBin(50.0, 0.219054242003, 0.0109070379935),
                triggerBin(60.0, 0.295901639344, 0.0130680394499),
                triggerBin(70.0, 0.356862745098, 0.0150003832062),
                triggerBin(80.0, 0.554140127389, 0.0119608715138),
                triggerBin(100.0, 0.755970149254, 0.0117333331362),
                triggerBin(120.0, 0.887773722628, 0.00953439509444),
                triggerBin(140.0, 0.964432284542, 0.00685023021524),
                triggerBin(160.0, 0.995975855131, 0.0028397690016),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0956014362657, 0.00622951946535),
                triggerBin(30.0, 0.121316306483, 0.00723580719943),
                triggerBin(40.0, 0.171637591446, 0.00894484219135),
                triggerBin(50.0, 0.219054242003, 0.0109070379935),
                triggerBin(60.0, 0.295901639344, 0.0130680394499),
                triggerBin(70.0, 0.356862745098, 0.0150003832062),
                triggerBin(80.0, 0.554140127389, 0.0119608715138),
                triggerBin(100.0, 0.755970149254, 0.0117333331362),
                triggerBin(120.0, 0.887773722628, 0.00953439509444),
                triggerBin(140.0, 0.964432284542, 0.00685023021524),
                triggerBin(160.0, 0.995975855131, 0.0028397690016),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0956014362657, 0.00622951946535),
                triggerBin(30.0, 0.121316306483, 0.00723580719943),
                triggerBin(40.0, 0.171637591446, 0.00894484219135),
                triggerBin(50.0, 0.219054242003, 0.0109070379935),
                triggerBin(60.0, 0.295901639344, 0.0130680394499),
                triggerBin(70.0, 0.356862745098, 0.0150003832062),
                triggerBin(80.0, 0.554140127389, 0.0119608715138),
                triggerBin(100.0, 0.755970149254, 0.0117333331362),
                triggerBin(120.0, 0.887773722628, 0.00953439509444),
                triggerBin(140.0, 0.964432284542, 0.00685023021524),
                triggerBin(160.0, 0.995975855131, 0.0028397690016),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0956014362657, 0.00622951946535),
                triggerBin(30.0, 0.121316306483, 0.00723580719943),
                triggerBin(40.0, 0.171637591446, 0.00894484219135),
                triggerBin(50.0, 0.219054242003, 0.0109070379935),
                triggerBin(60.0, 0.295901639344, 0.0130680394499),
                triggerBin(70.0, 0.356862745098, 0.0150003832062),
                triggerBin(80.0, 0.554140127389, 0.0119608715138),
                triggerBin(100.0, 0.755970149254, 0.0117333331362),
                triggerBin(120.0, 0.887773722628, 0.00953439509444),
                triggerBin(140.0, 0.964432284542, 0.00685023021524),
                triggerBin(160.0, 0.995975855131, 0.0028397690016),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0956014362657, 0.00622951946535),
                triggerBin(30.0, 0.121316306483, 0.00723580719943),
                triggerBin(40.0, 0.171637591446, 0.00894484219135),
                triggerBin(50.0, 0.219054242003, 0.0109070379935),
                triggerBin(60.0, 0.295901639344, 0.0130680394499),
                triggerBin(70.0, 0.356862745098, 0.0150003832062),
                triggerBin(80.0, 0.554140127389, 0.0119608715138),
                triggerBin(100.0, 0.755970149254, 0.0117333331362),
                triggerBin(120.0, 0.887773722628, 0.00953439509444),
                triggerBin(140.0, 0.964432284542, 0.00685023021524),
                triggerBin(160.0, 0.995975855131, 0.0028397690016),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012A"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

metLegEfficiency_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronVTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: (Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) >= 1&&Sum$(PFJetPt > 0&& PFJetPUIDtight) >= 3+Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5 && PFTauJetMinDR < 0.5))&& hPlusGlobalElectronVetoFilter > 0.5 && hPlusGlobalMuonVetoFilter > 0.5

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.166666666667, 0.152145154863),
                triggerBin(30.0, 0.0, 0.0),
                triggerBin(40.0, 0.0, 0.0),
                triggerBin(50.0, 1.0, 0.0),
                triggerBin(60.0, 0.0, 1.0),
                triggerBin(70.0, 1.0, 0.0),
                triggerBin(80.0, 0.0, 1.0),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0491803278689, 0.0276872531539),
                triggerBin(30.0, 0.0888888888889, 0.0424231735208),
                triggerBin(40.0, 0.2, 0.103279555899),
                triggerBin(50.0, 0.0909090909091, 0.0866784172041),
                triggerBin(60.0, 0.285714285714, 0.170746944191),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.047619047619, 0.0232357160226),
                triggerBin(30.0, 0.0392156862745, 0.0271805207876),
                triggerBin(40.0, 0.0909090909091, 0.0500438075057),
                triggerBin(50.0, 0.25, 0.125),
                triggerBin(60.0, 0.222222222222, 0.138579903214),
                triggerBin(70.0, 0.5, 0.204124145232),
                triggerBin(80.0, 0.0, 1.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0375, 0.021240806835),
                triggerBin(30.0, 0.0350877192982, 0.0243716009785),
                triggerBin(40.0, 0.131578947368, 0.0548361022017),
                triggerBin(50.0, 0.235294117647, 0.102879368494),
                triggerBin(60.0, 0.3, 0.144913767462),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 0.0, 0.0),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0597014925373, 0.0289459672458),
                triggerBin(30.0, 0.0833333333333, 0.0398927961565),
                triggerBin(40.0, 0.1875, 0.097578093725),
                triggerBin(50.0, 0.166666666667, 0.107582870728),
                triggerBin(60.0, 0.285714285714, 0.170746944191),
                triggerBin(70.0, 0.666666666667, 0.272165526976),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.333333333333, 0.272165526976),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0529801324503, 0.0182283597573),
                triggerBin(30.0, 0.0606060606061, 0.0239808353668),
                triggerBin(40.0, 0.122448979592, 0.0468290915575),
                triggerBin(50.0, 0.208333333333, 0.0828981693494),
                triggerBin(60.0, 0.25, 0.108253175473),
                triggerBin(70.0, 0.555555555556, 0.165634665),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.5, 0.25),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.047619047619, 0.0140116639604),
                triggerBin(30.0, 0.0512820512821, 0.0176599290185),
                triggerBin(40.0, 0.126436781609, 0.0356306922237),
                triggerBin(50.0, 0.219512195122, 0.0646428445316),
                triggerBin(60.0, 0.269230769231, 0.0869892924733),
                triggerBin(70.0, 0.384615384615, 0.13493200297),
                triggerBin(80.0, 0.4, 0.219089023002),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.714285714286, 0.170746944191),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0917899031107, 0.00652006344538),
                triggerBin(30.0, 0.124649073554, 0.00782715016001),
                triggerBin(40.0, 0.168341708543, 0.0093777099168),
                triggerBin(50.0, 0.218238503507, 0.011531598092),
                triggerBin(60.0, 0.294918330309, 0.0137366172708),
                triggerBin(70.0, 0.357219251337, 0.0156708680235),
                triggerBin(80.0, 0.553894080997, 0.012407801486),
                triggerBin(100.0, 0.757650951199, 0.0123237277556),
                triggerBin(120.0, 0.883233532934, 0.0101452553847),
                triggerBin(140.0, 0.962292609351, 0.00739792716261),
                triggerBin(160.0, 0.995604395604, 0.00310132302771),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0917899031107, 0.00652006344538),
                triggerBin(30.0, 0.124649073554, 0.00782715016001),
                triggerBin(40.0, 0.168341708543, 0.0093777099168),
                triggerBin(50.0, 0.218238503507, 0.011531598092),
                triggerBin(60.0, 0.294918330309, 0.0137366172708),
                triggerBin(70.0, 0.357219251337, 0.0156708680235),
                triggerBin(80.0, 0.553894080997, 0.012407801486),
                triggerBin(100.0, 0.757650951199, 0.0123237277556),
                triggerBin(120.0, 0.883233532934, 0.0101452553847),
                triggerBin(140.0, 0.962292609351, 0.00739792716261),
                triggerBin(160.0, 0.995604395604, 0.00310132302771),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0917899031107, 0.00652006344538),
                triggerBin(30.0, 0.124649073554, 0.00782715016001),
                triggerBin(40.0, 0.168341708543, 0.0093777099168),
                triggerBin(50.0, 0.218238503507, 0.011531598092),
                triggerBin(60.0, 0.294918330309, 0.0137366172708),
                triggerBin(70.0, 0.357219251337, 0.0156708680235),
                triggerBin(80.0, 0.553894080997, 0.012407801486),
                triggerBin(100.0, 0.757650951199, 0.0123237277556),
                triggerBin(120.0, 0.883233532934, 0.0101452553847),
                triggerBin(140.0, 0.962292609351, 0.00739792716261),
                triggerBin(160.0, 0.995604395604, 0.00310132302771),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0917899031107, 0.00652006344538),
                triggerBin(30.0, 0.124649073554, 0.00782715016001),
                triggerBin(40.0, 0.168341708543, 0.0093777099168),
                triggerBin(50.0, 0.218238503507, 0.011531598092),
                triggerBin(60.0, 0.294918330309, 0.0137366172708),
                triggerBin(70.0, 0.357219251337, 0.0156708680235),
                triggerBin(80.0, 0.553894080997, 0.012407801486),
                triggerBin(100.0, 0.757650951199, 0.0123237277556),
                triggerBin(120.0, 0.883233532934, 0.0101452553847),
                triggerBin(140.0, 0.962292609351, 0.00739792716261),
                triggerBin(160.0, 0.995604395604, 0.00310132302771),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0917899031107, 0.00652006344538),
                triggerBin(30.0, 0.124649073554, 0.00782715016001),
                triggerBin(40.0, 0.168341708543, 0.0093777099168),
                triggerBin(50.0, 0.218238503507, 0.011531598092),
                triggerBin(60.0, 0.294918330309, 0.0137366172708),
                triggerBin(70.0, 0.357219251337, 0.0156708680235),
                triggerBin(80.0, 0.553894080997, 0.012407801486),
                triggerBin(100.0, 0.757650951199, 0.0123237277556),
                triggerBin(120.0, 0.883233532934, 0.0101452553847),
                triggerBin(140.0, 0.962292609351, 0.00739792716261),
                triggerBin(160.0, 0.995604395604, 0.00310132302771),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0917899031107, 0.00652006344538),
                triggerBin(30.0, 0.124649073554, 0.00782715016001),
                triggerBin(40.0, 0.168341708543, 0.0093777099168),
                triggerBin(50.0, 0.218238503507, 0.011531598092),
                triggerBin(60.0, 0.294918330309, 0.0137366172708),
                triggerBin(70.0, 0.357219251337, 0.0156708680235),
                triggerBin(80.0, 0.553894080997, 0.012407801486),
                triggerBin(100.0, 0.757650951199, 0.0123237277556),
                triggerBin(120.0, 0.883233532934, 0.0101452553847),
                triggerBin(140.0, 0.962292609351, 0.00739792716261),
                triggerBin(160.0, 0.995604395604, 0.00310132302771),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0917899031107, 0.00652006344538),
                triggerBin(30.0, 0.124649073554, 0.00782715016001),
                triggerBin(40.0, 0.168341708543, 0.0093777099168),
                triggerBin(50.0, 0.218238503507, 0.011531598092),
                triggerBin(60.0, 0.294918330309, 0.0137366172708),
                triggerBin(70.0, 0.357219251337, 0.0156708680235),
                triggerBin(80.0, 0.553894080997, 0.012407801486),
                triggerBin(100.0, 0.757650951199, 0.0123237277556),
                triggerBin(120.0, 0.883233532934, 0.0101452553847),
                triggerBin(140.0, 0.962292609351, 0.00739792716261),
                triggerBin(160.0, 0.995604395604, 0.00310132302771),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0917899031107, 0.00652006344538),
                triggerBin(30.0, 0.124649073554, 0.00782715016001),
                triggerBin(40.0, 0.168341708543, 0.0093777099168),
                triggerBin(50.0, 0.218238503507, 0.011531598092),
                triggerBin(60.0, 0.294918330309, 0.0137366172708),
                triggerBin(70.0, 0.357219251337, 0.0156708680235),
                triggerBin(80.0, 0.553894080997, 0.012407801486),
                triggerBin(100.0, 0.757650951199, 0.0123237277556),
                triggerBin(120.0, 0.883233532934, 0.0101452553847),
                triggerBin(140.0, 0.962292609351, 0.00739792716261),
                triggerBin(160.0, 0.995604395604, 0.00310132302771),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012A"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

metLegEfficiency_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronVTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: (Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5) >= 1&&Sum$(PFJetPt > 0&& PFJetPUIDtight) >= 3+Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5 && PFTauJetMinDR < 0.5))&& hPlusGlobalElectronVetoFilter > 0.5 && hPlusGlobalMuonVetoFilter > 0.5

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0909090909091, 0.0866784172041),
                triggerBin(30.0, 0.0, 0.0),
                triggerBin(40.0, 0.0, 0.0),
                triggerBin(50.0, 1.0, 0.0),
                triggerBin(60.0, 0.0, 1.0),
                triggerBin(70.0, 1.0, 0.0),
                triggerBin(80.0, 0.0, 1.0),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0388349514563, 0.0190367039454),
                triggerBin(30.0, 0.0609756097561, 0.0264246708383),
                triggerBin(40.0, 0.135135135135, 0.0562027291795),
                triggerBin(50.0, 0.161290322581, 0.0660585650285),
                triggerBin(60.0, 0.4, 0.154919333848),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.333333333333, 0.272165526976),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0308641975309, 0.0135882117669),
                triggerBin(30.0, 0.06, 0.0237486841741),
                triggerBin(40.0, 0.0634920634921, 0.0307216952878),
                triggerBin(50.0, 0.12, 0.0649923072371),
                triggerBin(60.0, 0.266666666667, 0.114179845144),
                triggerBin(70.0, 0.5, 0.176776695297),
                triggerBin(80.0, 0.5, 0.353553390593),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.666666666667, 0.272165526976),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0487804878049, 0.0168206014463),
                triggerBin(30.0, 0.0578512396694, 0.0212238120087),
                triggerBin(40.0, 0.116883116883, 0.036613363161),
                triggerBin(50.0, 0.135135135135, 0.0562027291795),
                triggerBin(60.0, 0.263157894737, 0.101022617888),
                triggerBin(70.0, 0.166666666667, 0.152145154863),
                triggerBin(80.0, 0.2, 0.1788854382),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0438596491228, 0.0191796630922),
                triggerBin(30.0, 0.0581395348837, 0.0252336360438),
                triggerBin(40.0, 0.131578947368, 0.0548361022017),
                triggerBin(50.0, 0.1875, 0.0689981317682),
                triggerBin(60.0, 0.4, 0.154919333848),
                triggerBin(70.0, 0.666666666667, 0.272165526976),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.5, 0.25),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.036231884058, 0.0112480488865),
                triggerBin(30.0, 0.0591397849462, 0.0172960109116),
                triggerBin(40.0, 0.0891089108911, 0.0283486973684),
                triggerBin(50.0, 0.157894736842, 0.0482980492359),
                triggerBin(60.0, 0.32, 0.0932952303175),
                triggerBin(70.0, 0.545454545455, 0.150131422517),
                triggerBin(80.0, 0.8, 0.1788854382),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.6, 0.219089023002),
                triggerBin(140.0, 0.666666666667, 0.272165526976),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0409090909091, 0.00944307552824),
                triggerBin(30.0, 0.0586319218241, 0.0134084201713),
                triggerBin(40.0, 0.101123595506, 0.0225978041513),
                triggerBin(50.0, 0.148936170213, 0.0367212309473),
                triggerBin(60.0, 0.295454545455, 0.0687817954616),
                triggerBin(70.0, 0.411764705882, 0.119364624987),
                triggerBin(80.0, 0.5, 0.158113883008),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.75, 0.153093108924),
                triggerBin(140.0, 0.666666666667, 0.272165526976),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0946255002859, 0.0049488959266),
                triggerBin(30.0, 0.12833008447, 0.00602845413216),
                triggerBin(40.0, 0.179447255742, 0.00757076227831),
                triggerBin(50.0, 0.224078624079, 0.00924329611136),
                triggerBin(60.0, 0.301094890511, 0.0113138363877),
                triggerBin(70.0, 0.361393323657, 0.0129414274228),
                triggerBin(80.0, 0.545335658239, 0.0103963451363),
                triggerBin(100.0, 0.757876312719, 0.0103469511216),
                triggerBin(120.0, 0.888172043011, 0.0084379440422),
                triggerBin(140.0, 0.967195767196, 0.00579437011147),
                triggerBin(160.0, 0.996845425868, 0.00222709965247),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0946255002859, 0.0049488959266),
                triggerBin(30.0, 0.12833008447, 0.00602845413216),
                triggerBin(40.0, 0.179447255742, 0.00757076227831),
                triggerBin(50.0, 0.224078624079, 0.00924329611136),
                triggerBin(60.0, 0.301094890511, 0.0113138363877),
                triggerBin(70.0, 0.361393323657, 0.0129414274228),
                triggerBin(80.0, 0.545335658239, 0.0103963451363),
                triggerBin(100.0, 0.757876312719, 0.0103469511216),
                triggerBin(120.0, 0.888172043011, 0.0084379440422),
                triggerBin(140.0, 0.967195767196, 0.00579437011147),
                triggerBin(160.0, 0.996845425868, 0.00222709965247),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0946255002859, 0.0049488959266),
                triggerBin(30.0, 0.12833008447, 0.00602845413216),
                triggerBin(40.0, 0.179447255742, 0.00757076227831),
                triggerBin(50.0, 0.224078624079, 0.00924329611136),
                triggerBin(60.0, 0.301094890511, 0.0113138363877),
                triggerBin(70.0, 0.361393323657, 0.0129414274228),
                triggerBin(80.0, 0.545335658239, 0.0103963451363),
                triggerBin(100.0, 0.757876312719, 0.0103469511216),
                triggerBin(120.0, 0.888172043011, 0.0084379440422),
                triggerBin(140.0, 0.967195767196, 0.00579437011147),
                triggerBin(160.0, 0.996845425868, 0.00222709965247),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0946255002859, 0.0049488959266),
                triggerBin(30.0, 0.12833008447, 0.00602845413216),
                triggerBin(40.0, 0.179447255742, 0.00757076227831),
                triggerBin(50.0, 0.224078624079, 0.00924329611136),
                triggerBin(60.0, 0.301094890511, 0.0113138363877),
                triggerBin(70.0, 0.361393323657, 0.0129414274228),
                triggerBin(80.0, 0.545335658239, 0.0103963451363),
                triggerBin(100.0, 0.757876312719, 0.0103469511216),
                triggerBin(120.0, 0.888172043011, 0.0084379440422),
                triggerBin(140.0, 0.967195767196, 0.00579437011147),
                triggerBin(160.0, 0.996845425868, 0.00222709965247),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0946255002859, 0.0049488959266),
                triggerBin(30.0, 0.12833008447, 0.00602845413216),
                triggerBin(40.0, 0.179447255742, 0.00757076227831),
                triggerBin(50.0, 0.224078624079, 0.00924329611136),
                triggerBin(60.0, 0.301094890511, 0.0113138363877),
                triggerBin(70.0, 0.361393323657, 0.0129414274228),
                triggerBin(80.0, 0.545335658239, 0.0103963451363),
                triggerBin(100.0, 0.757876312719, 0.0103469511216),
                triggerBin(120.0, 0.888172043011, 0.0084379440422),
                triggerBin(140.0, 0.967195767196, 0.00579437011147),
                triggerBin(160.0, 0.996845425868, 0.00222709965247),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0946255002859, 0.0049488959266),
                triggerBin(30.0, 0.12833008447, 0.00602845413216),
                triggerBin(40.0, 0.179447255742, 0.00757076227831),
                triggerBin(50.0, 0.224078624079, 0.00924329611136),
                triggerBin(60.0, 0.301094890511, 0.0113138363877),
                triggerBin(70.0, 0.361393323657, 0.0129414274228),
                triggerBin(80.0, 0.545335658239, 0.0103963451363),
                triggerBin(100.0, 0.757876312719, 0.0103469511216),
                triggerBin(120.0, 0.888172043011, 0.0084379440422),
                triggerBin(140.0, 0.967195767196, 0.00579437011147),
                triggerBin(160.0, 0.996845425868, 0.00222709965247),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0946255002859, 0.0049488959266),
                triggerBin(30.0, 0.12833008447, 0.00602845413216),
                triggerBin(40.0, 0.179447255742, 0.00757076227831),
                triggerBin(50.0, 0.224078624079, 0.00924329611136),
                triggerBin(60.0, 0.301094890511, 0.0113138363877),
                triggerBin(70.0, 0.361393323657, 0.0129414274228),
                triggerBin(80.0, 0.545335658239, 0.0103963451363),
                triggerBin(100.0, 0.757876312719, 0.0103469511216),
                triggerBin(120.0, 0.888172043011, 0.0084379440422),
                triggerBin(140.0, 0.967195767196, 0.00579437011147),
                triggerBin(160.0, 0.996845425868, 0.00222709965247),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0946255002859, 0.0049488959266),
                triggerBin(30.0, 0.12833008447, 0.00602845413216),
                triggerBin(40.0, 0.179447255742, 0.00757076227831),
                triggerBin(50.0, 0.224078624079, 0.00924329611136),
                triggerBin(60.0, 0.301094890511, 0.0113138363877),
                triggerBin(70.0, 0.361393323657, 0.0129414274228),
                triggerBin(80.0, 0.545335658239, 0.0103963451363),
                triggerBin(100.0, 0.757876312719, 0.0103469511216),
                triggerBin(120.0, 0.888172043011, 0.0084379440422),
                triggerBin(140.0, 0.967195767196, 0.00579437011147),
                triggerBin(160.0, 0.996845425868, 0.00222709965247),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012A"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

metLegEfficiency_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronVTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: (Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5) >= 1&&Sum$(PFJetPt > 0&& PFJetPUIDtight) >= 3+Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5 && PFTauJetMinDR < 0.5))&& hPlusGlobalElectronVetoFilter > 0.5 && hPlusGlobalMuonVetoFilter > 0.5

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.142857142857, 0.132260014253),
                triggerBin(30.0, 0.0, 0.0),
                triggerBin(40.0, 0.0, 0.0),
                triggerBin(50.0, 1.0, 0.0),
                triggerBin(60.0, 0.0, 1.0),
                triggerBin(70.0, 1.0, 0.0),
                triggerBin(80.0, 0.0, 1.0),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0441176470588, 0.0249031300527),
                triggerBin(30.0, 0.1, 0.0424264068712),
                triggerBin(40.0, 0.166666666667, 0.0878410461158),
                triggerBin(50.0, 0.142857142857, 0.0935219529583),
                triggerBin(60.0, 0.285714285714, 0.170746944191),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.333333333333, 0.272165526976),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0425531914894, 0.0208189810549),
                triggerBin(30.0, 0.0377358490566, 0.0261749753573),
                triggerBin(40.0, 0.0833333333333, 0.0460642331994),
                triggerBin(50.0, 0.1875, 0.097578093725),
                triggerBin(60.0, 0.222222222222, 0.138579903214),
                triggerBin(70.0, 0.5, 0.204124145232),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0449438202247, 0.0219611181558),
                triggerBin(30.0, 0.03125, 0.0217490795423),
                triggerBin(40.0, 0.128205128205, 0.0535337356629),
                triggerBin(50.0, 0.2, 0.0894427191),
                triggerBin(60.0, 0.3, 0.144913767462),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 0.0, 0.0),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0533333333333, 0.0259458124788),
                triggerBin(30.0, 0.0943396226415, 0.0401505793659),
                triggerBin(40.0, 0.157894736842, 0.083654675183),
                triggerBin(50.0, 0.2, 0.103279555899),
                triggerBin(60.0, 0.285714285714, 0.170746944191),
                triggerBin(70.0, 0.666666666667, 0.272165526976),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.5, 0.25),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0473372781065, 0.0163353285798),
                triggerBin(30.0, 0.0660377358491, 0.0241216948646),
                triggerBin(40.0, 0.109090909091, 0.0420367983048),
                triggerBin(50.0, 0.193548387097, 0.0709582814619),
                triggerBin(60.0, 0.25, 0.108253175473),
                triggerBin(70.0, 0.555555555556, 0.165634665),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.6, 0.219089023002),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.046511627907, 0.0131107826469),
                triggerBin(30.0, 0.0529411764706, 0.0171735789385),
                triggerBin(40.0, 0.117021276596, 0.0331545859316),
                triggerBin(50.0, 0.196078431373, 0.0555951190062),
                triggerBin(60.0, 0.269230769231, 0.0869892924733),
                triggerBin(70.0, 0.384615384615, 0.13493200297),
                triggerBin(80.0, 0.5, 0.204124145232),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.75, 0.153093108924),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0953237410072, 0.00622701259712),
                triggerBin(30.0, 0.120256283884, 0.00722089371869),
                triggerBin(40.0, 0.170993227991, 0.00894409978575),
                triggerBin(50.0, 0.216934919524, 0.0109030385341),
                triggerBin(60.0, 0.295473251029, 0.0130893984984),
                triggerBin(70.0, 0.355599214145, 0.015003222085),
                triggerBin(80.0, 0.552447552448, 0.0120035264399),
                triggerBin(100.0, 0.755422587883, 0.0117554011075),
                triggerBin(120.0, 0.887568555759, 0.00955072164292),
                triggerBin(140.0, 0.964432284542, 0.00685023021524),
                triggerBin(160.0, 0.995967741935, 0.00284548275264),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0953237410072, 0.00622701259712),
                triggerBin(30.0, 0.120256283884, 0.00722089371869),
                triggerBin(40.0, 0.170993227991, 0.00894409978575),
                triggerBin(50.0, 0.216934919524, 0.0109030385341),
                triggerBin(60.0, 0.295473251029, 0.0130893984984),
                triggerBin(70.0, 0.355599214145, 0.015003222085),
                triggerBin(80.0, 0.552447552448, 0.0120035264399),
                triggerBin(100.0, 0.755422587883, 0.0117554011075),
                triggerBin(120.0, 0.887568555759, 0.00955072164292),
                triggerBin(140.0, 0.964432284542, 0.00685023021524),
                triggerBin(160.0, 0.995967741935, 0.00284548275264),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0953237410072, 0.00622701259712),
                triggerBin(30.0, 0.120256283884, 0.00722089371869),
                triggerBin(40.0, 0.170993227991, 0.00894409978575),
                triggerBin(50.0, 0.216934919524, 0.0109030385341),
                triggerBin(60.0, 0.295473251029, 0.0130893984984),
                triggerBin(70.0, 0.355599214145, 0.015003222085),
                triggerBin(80.0, 0.552447552448, 0.0120035264399),
                triggerBin(100.0, 0.755422587883, 0.0117554011075),
                triggerBin(120.0, 0.887568555759, 0.00955072164292),
                triggerBin(140.0, 0.964432284542, 0.00685023021524),
                triggerBin(160.0, 0.995967741935, 0.00284548275264),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0953237410072, 0.00622701259712),
                triggerBin(30.0, 0.120256283884, 0.00722089371869),
                triggerBin(40.0, 0.170993227991, 0.00894409978575),
                triggerBin(50.0, 0.216934919524, 0.0109030385341),
                triggerBin(60.0, 0.295473251029, 0.0130893984984),
                triggerBin(70.0, 0.355599214145, 0.015003222085),
                triggerBin(80.0, 0.552447552448, 0.0120035264399),
                triggerBin(100.0, 0.755422587883, 0.0117554011075),
                triggerBin(120.0, 0.887568555759, 0.00955072164292),
                triggerBin(140.0, 0.964432284542, 0.00685023021524),
                triggerBin(160.0, 0.995967741935, 0.00284548275264),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0953237410072, 0.00622701259712),
                triggerBin(30.0, 0.120256283884, 0.00722089371869),
                triggerBin(40.0, 0.170993227991, 0.00894409978575),
                triggerBin(50.0, 0.216934919524, 0.0109030385341),
                triggerBin(60.0, 0.295473251029, 0.0130893984984),
                triggerBin(70.0, 0.355599214145, 0.015003222085),
                triggerBin(80.0, 0.552447552448, 0.0120035264399),
                triggerBin(100.0, 0.755422587883, 0.0117554011075),
                triggerBin(120.0, 0.887568555759, 0.00955072164292),
                triggerBin(140.0, 0.964432284542, 0.00685023021524),
                triggerBin(160.0, 0.995967741935, 0.00284548275264),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0953237410072, 0.00622701259712),
                triggerBin(30.0, 0.120256283884, 0.00722089371869),
                triggerBin(40.0, 0.170993227991, 0.00894409978575),
                triggerBin(50.0, 0.216934919524, 0.0109030385341),
                triggerBin(60.0, 0.295473251029, 0.0130893984984),
                triggerBin(70.0, 0.355599214145, 0.015003222085),
                triggerBin(80.0, 0.552447552448, 0.0120035264399),
                triggerBin(100.0, 0.755422587883, 0.0117554011075),
                triggerBin(120.0, 0.887568555759, 0.00955072164292),
                triggerBin(140.0, 0.964432284542, 0.00685023021524),
                triggerBin(160.0, 0.995967741935, 0.00284548275264),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0953237410072, 0.00622701259712),
                triggerBin(30.0, 0.120256283884, 0.00722089371869),
                triggerBin(40.0, 0.170993227991, 0.00894409978575),
                triggerBin(50.0, 0.216934919524, 0.0109030385341),
                triggerBin(60.0, 0.295473251029, 0.0130893984984),
                triggerBin(70.0, 0.355599214145, 0.015003222085),
                triggerBin(80.0, 0.552447552448, 0.0120035264399),
                triggerBin(100.0, 0.755422587883, 0.0117554011075),
                triggerBin(120.0, 0.887568555759, 0.00955072164292),
                triggerBin(140.0, 0.964432284542, 0.00685023021524),
                triggerBin(160.0, 0.995967741935, 0.00284548275264),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0953237410072, 0.00622701259712),
                triggerBin(30.0, 0.120256283884, 0.00722089371869),
                triggerBin(40.0, 0.170993227991, 0.00894409978575),
                triggerBin(50.0, 0.216934919524, 0.0109030385341),
                triggerBin(60.0, 0.295473251029, 0.0130893984984),
                triggerBin(70.0, 0.355599214145, 0.015003222085),
                triggerBin(80.0, 0.552447552448, 0.0120035264399),
                triggerBin(100.0, 0.755422587883, 0.0117554011075),
                triggerBin(120.0, 0.887568555759, 0.00955072164292),
                triggerBin(140.0, 0.964432284542, 0.00685023021524),
                triggerBin(160.0, 0.995967741935, 0.00284548275264),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012A"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

metLegEfficiency_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronVTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: (Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) >= 1&&Sum$(PFJetPt > 0&& PFJetPUIDtight) >= 3+Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_decayModeFinding > 0.5&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5 && PFTauJetMinDR < 0.5))&& hPlusGlobalElectronVetoFilter > 0.5 && hPlusGlobalMuonVetoFilter > 0.5

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.166666666667, 0.152145154863),
                triggerBin(30.0, 0.0, 0.0),
                triggerBin(40.0, 0.0, 0.0),
                triggerBin(50.0, 1.0, 0.0),
                triggerBin(60.0, 0.0, 1.0),
                triggerBin(70.0, 1.0, 0.0),
                triggerBin(80.0, 0.0, 1.0),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0491803278689, 0.0276872531539),
                triggerBin(30.0, 0.0888888888889, 0.0424231735208),
                triggerBin(40.0, 0.2, 0.103279555899),
                triggerBin(50.0, 0.0909090909091, 0.0866784172041),
                triggerBin(60.0, 0.285714285714, 0.170746944191),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.047619047619, 0.0232357160226),
                triggerBin(30.0, 0.0392156862745, 0.0271805207876),
                triggerBin(40.0, 0.0909090909091, 0.0500438075057),
                triggerBin(50.0, 0.25, 0.125),
                triggerBin(60.0, 0.222222222222, 0.138579903214),
                triggerBin(70.0, 0.5, 0.204124145232),
                triggerBin(80.0, 0.0, 1.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0375, 0.021240806835),
                triggerBin(30.0, 0.0350877192982, 0.0243716009785),
                triggerBin(40.0, 0.131578947368, 0.0548361022017),
                triggerBin(50.0, 0.235294117647, 0.102879368494),
                triggerBin(60.0, 0.3, 0.144913767462),
                triggerBin(70.0, 0.0, 0.0),
                triggerBin(80.0, 0.0, 0.0),
                triggerBin(100.0, 0.0, 1.0),
                triggerBin(120.0, 1.0, 0.0),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0597014925373, 0.0289459672458),
                triggerBin(30.0, 0.0833333333333, 0.0398927961565),
                triggerBin(40.0, 0.1875, 0.097578093725),
                triggerBin(50.0, 0.166666666667, 0.107582870728),
                triggerBin(60.0, 0.285714285714, 0.170746944191),
                triggerBin(70.0, 0.666666666667, 0.272165526976),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.333333333333, 0.272165526976),
                triggerBin(140.0, 0.0, 1.0),
                triggerBin(160.0, 0.0, 1.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0529801324503, 0.0182283597573),
                triggerBin(30.0, 0.0606060606061, 0.0239808353668),
                triggerBin(40.0, 0.122448979592, 0.0468290915575),
                triggerBin(50.0, 0.208333333333, 0.0828981693494),
                triggerBin(60.0, 0.25, 0.108253175473),
                triggerBin(70.0, 0.555555555556, 0.165634665),
                triggerBin(80.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.5, 0.25),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.047619047619, 0.0140116639604),
                triggerBin(30.0, 0.0512820512821, 0.0176599290185),
                triggerBin(40.0, 0.126436781609, 0.0356306922237),
                triggerBin(50.0, 0.219512195122, 0.0646428445316),
                triggerBin(60.0, 0.269230769231, 0.0869892924733),
                triggerBin(70.0, 0.384615384615, 0.13493200297),
                triggerBin(80.0, 0.4, 0.219089023002),
                triggerBin(100.0, 1.0, 0.0),
                triggerBin(120.0, 0.714285714286, 0.170746944191),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0918836140888, 0.00652638323867),
                triggerBin(30.0, 0.123449830891, 0.0078101042489),
                triggerBin(40.0, 0.167611846251, 0.00937619944848),
                triggerBin(50.0, 0.21568627451, 0.0115186364082),
                triggerBin(60.0, 0.295081967213, 0.0137638355574),
                triggerBin(70.0, 0.355841371919, 0.0156741432736),
                triggerBin(80.0, 0.552070263488, 0.0124554082336),
                triggerBin(100.0, 0.757249378625, 0.0123408764067),
                triggerBin(120.0, 0.883, 0.010164201887),
                triggerBin(140.0, 0.962292609351, 0.00739792716261),
                triggerBin(160.0, 0.995594713656, 0.00310813902274),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0918836140888, 0.00652638323867),
                triggerBin(30.0, 0.123449830891, 0.0078101042489),
                triggerBin(40.0, 0.167611846251, 0.00937619944848),
                triggerBin(50.0, 0.21568627451, 0.0115186364082),
                triggerBin(60.0, 0.295081967213, 0.0137638355574),
                triggerBin(70.0, 0.355841371919, 0.0156741432736),
                triggerBin(80.0, 0.552070263488, 0.0124554082336),
                triggerBin(100.0, 0.757249378625, 0.0123408764067),
                triggerBin(120.0, 0.883, 0.010164201887),
                triggerBin(140.0, 0.962292609351, 0.00739792716261),
                triggerBin(160.0, 0.995594713656, 0.00310813902274),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0918836140888, 0.00652638323867),
                triggerBin(30.0, 0.123449830891, 0.0078101042489),
                triggerBin(40.0, 0.167611846251, 0.00937619944848),
                triggerBin(50.0, 0.21568627451, 0.0115186364082),
                triggerBin(60.0, 0.295081967213, 0.0137638355574),
                triggerBin(70.0, 0.355841371919, 0.0156741432736),
                triggerBin(80.0, 0.552070263488, 0.0124554082336),
                triggerBin(100.0, 0.757249378625, 0.0123408764067),
                triggerBin(120.0, 0.883, 0.010164201887),
                triggerBin(140.0, 0.962292609351, 0.00739792716261),
                triggerBin(160.0, 0.995594713656, 0.00310813902274),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0918836140888, 0.00652638323867),
                triggerBin(30.0, 0.123449830891, 0.0078101042489),
                triggerBin(40.0, 0.167611846251, 0.00937619944848),
                triggerBin(50.0, 0.21568627451, 0.0115186364082),
                triggerBin(60.0, 0.295081967213, 0.0137638355574),
                triggerBin(70.0, 0.355841371919, 0.0156741432736),
                triggerBin(80.0, 0.552070263488, 0.0124554082336),
                triggerBin(100.0, 0.757249378625, 0.0123408764067),
                triggerBin(120.0, 0.883, 0.010164201887),
                triggerBin(140.0, 0.962292609351, 0.00739792716261),
                triggerBin(160.0, 0.995594713656, 0.00310813902274),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0918836140888, 0.00652638323867),
                triggerBin(30.0, 0.123449830891, 0.0078101042489),
                triggerBin(40.0, 0.167611846251, 0.00937619944848),
                triggerBin(50.0, 0.21568627451, 0.0115186364082),
                triggerBin(60.0, 0.295081967213, 0.0137638355574),
                triggerBin(70.0, 0.355841371919, 0.0156741432736),
                triggerBin(80.0, 0.552070263488, 0.0124554082336),
                triggerBin(100.0, 0.757249378625, 0.0123408764067),
                triggerBin(120.0, 0.883, 0.010164201887),
                triggerBin(140.0, 0.962292609351, 0.00739792716261),
                triggerBin(160.0, 0.995594713656, 0.00310813902274),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0918836140888, 0.00652638323867),
                triggerBin(30.0, 0.123449830891, 0.0078101042489),
                triggerBin(40.0, 0.167611846251, 0.00937619944848),
                triggerBin(50.0, 0.21568627451, 0.0115186364082),
                triggerBin(60.0, 0.295081967213, 0.0137638355574),
                triggerBin(70.0, 0.355841371919, 0.0156741432736),
                triggerBin(80.0, 0.552070263488, 0.0124554082336),
                triggerBin(100.0, 0.757249378625, 0.0123408764067),
                triggerBin(120.0, 0.883, 0.010164201887),
                triggerBin(140.0, 0.962292609351, 0.00739792716261),
                triggerBin(160.0, 0.995594713656, 0.00310813902274),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0918836140888, 0.00652638323867),
                triggerBin(30.0, 0.123449830891, 0.0078101042489),
                triggerBin(40.0, 0.167611846251, 0.00937619944848),
                triggerBin(50.0, 0.21568627451, 0.0115186364082),
                triggerBin(60.0, 0.295081967213, 0.0137638355574),
                triggerBin(70.0, 0.355841371919, 0.0156741432736),
                triggerBin(80.0, 0.552070263488, 0.0124554082336),
                triggerBin(100.0, 0.757249378625, 0.0123408764067),
                triggerBin(120.0, 0.883, 0.010164201887),
                triggerBin(140.0, 0.962292609351, 0.00739792716261),
                triggerBin(160.0, 0.995594713656, 0.00310813902274),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0918836140888, 0.00652638323867),
                triggerBin(30.0, 0.123449830891, 0.0078101042489),
                triggerBin(40.0, 0.167611846251, 0.00937619944848),
                triggerBin(50.0, 0.21568627451, 0.0115186364082),
                triggerBin(60.0, 0.295081967213, 0.0137638355574),
                triggerBin(70.0, 0.355841371919, 0.0156741432736),
                triggerBin(80.0, 0.552070263488, 0.0124554082336),
                triggerBin(100.0, 0.757249378625, 0.0123408764067),
                triggerBin(120.0, 0.883, 0.010164201887),
                triggerBin(140.0, 0.962292609351, 0.00739792716261),
                triggerBin(160.0, 0.995594713656, 0.00310813902274),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012A"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)
