# Generated on Wed Nov  7 10:40:07 2012
# by HiggsAnalysis/TriggerEfficiency/test/plotTauEfficiency.py

import FWCore.ParameterSet.Config as cms

def triggerBin(pt, efficiency, uncertainty):
    return cms.PSet(
        pt = cms.double(pt),
        efficiency = cms.double(efficiency),
        uncertainty = cms.double(uncertainty)
    )

tauLegEfficiency_noscalefactors = cms.untracked.PSet(
    dataParameters = cms.PSet(
        # Run2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(697), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 1.0, 0.0),
            ),
        ),
        # Run2012B
        runs_193834_196531 = cms.PSet(
            firstRun = cms.uint32(193834),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4428), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 1.0, 0.0),
            ),
        ),
        # Run2012C
        runs_198022_202585 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(202585),
            luminosity = cms.double(6610), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 1.0, 0.0),
            ),
        ),
        # Run2012A+B
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5126), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 1.0, 0.0),
            ),
        ),
        # Run2012A+B+C
        runs_190456_202585 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(202585),
            luminosity = cms.double(11736), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 1.0, 0.0),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 1.0, 0.0),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 1.0, 0.0),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 1.0, 0.0),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 1.0, 0.0),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 1.0, 0.0),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
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

    # Offline selection: PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstMuonTight > 0.5&& MuonTauInvMass < 80&& PFTau_againstElectronMedium > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr > 0.5

    dataParameters = cms.PSet(
        # Run2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(697), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0261437908497, 0.0126406822336),
                triggerBin(30.0, 0.421383647799, 0.0294751086197),
                triggerBin(40.0, 0.785046728972, 0.0471723344386),
                triggerBin(50.0, 0.862068965517, 0.0956983526631),
                triggerBin(60.0, 0.733333333333, 0.161145049639),
                triggerBin(80.0, 1.0, 0.458641675296),
                triggerBin(100.0, 0.0, 0.841344746068),
                triggerBin(200.0, 0.0, 0.841344746068), # duplicated bin
            ),
        ),
        # Run2012B
        runs_193834_196531 = cms.PSet(
            firstRun = cms.uint32(193834),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4428), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.037493304767, 0.00493036813593),
                triggerBin(30.0, 0.405221339387, 0.0120310028558),
                triggerBin(40.0, 0.846685082873, 0.0145793078104),
                triggerBin(50.0, 0.85632183908, 0.0316837763512),
                triggerBin(60.0, 0.821782178218, 0.0464539610827),
                triggerBin(80.0, 0.882352941176, 0.134601457887),
                triggerBin(100.0, 1.0, 0.154109706156),
                triggerBin(200.0, 1.0, 0.841344746068),
            ),
        ),
        # Run2012C
        runs_198022_202585 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(202585),
            luminosity = cms.double(6610), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.043250327654, 0.00468205542596),
                triggerBin(30.0, 0.400879120879, 0.0105367729812),
                triggerBin(40.0, 0.859556494192, 0.0122133841382),
                triggerBin(50.0, 0.847926267281, 0.0283982969726),
                triggerBin(60.0, 0.815533980583, 0.0463476512865),
                triggerBin(80.0, 0.782608695652, 0.120323537142),
                triggerBin(100.0, 0.769230769231, 0.174723757631),
                triggerBin(200.0, 1.0, 0.841344746068),
            ),
        ),
        # Run2012A+B
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5126), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0358950759319, 0.00444942028415),
                triggerBin(30.0, 0.407692307692, 0.0110578713405),
                triggerBin(40.0, 0.838748495788, 0.0137817101587),
                triggerBin(50.0, 0.857142857143, 0.0289212043136),
                triggerBin(60.0, 0.810344827586, 0.0435534126686),
                triggerBin(80.0, 0.9, 0.116971358051),
                triggerBin(100.0, 0.916666666667, 0.166519597077),
                triggerBin(200.0, 1.0, 0.841344746068),
            ),
        ),
        # Run2012A+B+C
        runs_190456_202585 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(202585),
            luminosity = cms.double(11736), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0396683101748, 0.00314194674417),
                triggerBin(30.0, 0.404133180253, 0.00757236000815),
                triggerBin(40.0, 0.849831271091, 0.0089554971757),
                triggerBin(50.0, 0.852380952381, 0.0193845026464),
                triggerBin(60.0, 0.812785388128, 0.0301446146979),
                triggerBin(80.0, 0.837209302326, 0.0766334033584),
                triggerBin(100.0, 0.84, 0.10854843784),
                triggerBin(200.0, 1.0, 0.601684479424),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0528301886792, 0.0175766612871),
                triggerBin(30.0, 0.448863636364, 0.0280421106358),
                triggerBin(40.0, 0.875862068966, 0.0336977613634),
                triggerBin(50.0, 0.903225806452, 0.0852576401872),
                triggerBin(60.0, 1.0, 0.115501778685),
                triggerBin(80.0, 1.0, 0.26422943474),
                triggerBin(100.0, 0.833333333333, 0.287350389332),
                triggerBin(200.0, 0.833333333333, 0.287350389332), # duplicated bin
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0635451505017, 0.0174290416553),
                triggerBin(30.0, 0.466145833333, 0.0268150926439),
                triggerBin(40.0, 0.869047619048, 0.0314064886584),
                triggerBin(50.0, 0.903225806452, 0.0852576401872),
                triggerBin(60.0, 1.0, 0.0923494906334),
                triggerBin(80.0, 1.0, 0.168149186138),
                triggerBin(100.0, 1.0, 0.26422943474),
                triggerBin(200.0, 1.0, 0.26422943474), # duplicated bin
            ),
        ),
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0815602836879, 0.0105284702399),
                triggerBin(30.0, 0.462975778547, 0.0134847751162),
                triggerBin(40.0, 0.890387858347, 0.0143719556449),
                triggerBin(50.0, 0.876033057851, 0.0375527752685),
                triggerBin(60.0, 1.0, 0.0527078145683),
                triggerBin(80.0, 0.975, 0.0551515705063),
                triggerBin(100.0, 0.833333333333, 0.287350389332),
                triggerBin(200.0, 0.833333333333, 0.287350389332), # duplicated bin
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0516431924883, 0.0199812851664),
                triggerBin(30.0, 0.472222222222, 0.0363305871727),
                triggerBin(40.0, 0.851485148515, 0.0441602263209),
                triggerBin(50.0, 0.941176470588, 0.12258022277),
                triggerBin(60.0, 0.941176470588, 0.12258022277),
                triggerBin(80.0, 1.0, 0.308024223477),
                triggerBin(100.0, 1.0, 0.26422943474),
                triggerBin(200.0, 1.0, 0.26422943474), # duplicated bin
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0416666666667, 0.017248941493),
                triggerBin(30.0, 0.435975609756, 0.0290646868546),
                triggerBin(40.0, 0.8828125, 0.0356789360919),
                triggerBin(50.0, 0.870967741935, 0.0903256568946),
                triggerBin(60.0, 0.916666666667, 0.166519597077),
                triggerBin(80.0, 0.75, 0.368402425504),
                triggerBin(100.0, 0.833333333333, 0.287350389332),
                triggerBin(200.0, 0.833333333333, 0.287350389332), # duplicated bin
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.049504950495, 0.0116408705379),
                triggerBin(30.0, 0.431034482759, 0.0195781276306),
                triggerBin(40.0, 0.887596899225, 0.0232409116684),
                triggerBin(50.0, 0.91935483871, 0.0508738752303),
                triggerBin(60.0, 0.923076923077, 0.0925777957157),
                triggerBin(80.0, 0.777777777778, 0.221429368878),
                triggerBin(100.0, 0.875, 0.23225032014),
                triggerBin(200.0, 0.875, 0.23225032014), # duplicated bin
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABC"),
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

    # Offline selection: PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstMuonTight > 0.5&& MuonTauInvMass < 80&& PFTau_againstElectronMVA > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr > 0.5

    dataParameters = cms.PSet(
        # Run2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(697), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0267175572519, 0.0140943842682),
                triggerBin(30.0, 0.418772563177, 0.0316992998044),
                triggerBin(40.0, 0.827956989247, 0.0483272737625),
                triggerBin(50.0, 0.851851851852, 0.101731447858),
                triggerBin(60.0, 0.692307692308, 0.177171188325),
                triggerBin(80.0, 1.0, 0.458641675296),
                triggerBin(100.0, 0.0, 0.841344746068),
                triggerBin(200.0, 0.0, 0.841344746068), # duplicated bin
            ),
        ),
        # Run2012B
        runs_193834_196531 = cms.PSet(
            firstRun = cms.uint32(193834),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4428), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0351818723912, 0.00509675015801),
                triggerBin(30.0, 0.407219759341, 0.0127371917926),
                triggerBin(40.0, 0.860816944024, 0.0147916268304),
                triggerBin(50.0, 0.878205128205, 0.0320677129323),
                triggerBin(60.0, 0.826086956522, 0.0487813413935),
                triggerBin(80.0, 0.882352941176, 0.134601457887),
                triggerBin(100.0, 1.0, 0.18499249774),
                triggerBin(200.0, 1.0, 0.841344746068),
            ),
        ),
        # Run2012C
        runs_198022_202585 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(202585),
            luminosity = cms.double(6610), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0387221684414, 0.00472534092068),
                triggerBin(30.0, 0.405405405405, 0.0111741015059),
                triggerBin(40.0, 0.8779342723, 0.0122671022308),
                triggerBin(50.0, 0.854271356784, 0.0294428745967),
                triggerBin(60.0, 0.835164835165, 0.0483979551099),
                triggerBin(80.0, 0.809523809524, 0.125184034189),
                triggerBin(100.0, 0.818181818182, 0.1914016948),
                triggerBin(200.0, 1.0, 0.841344746068),
            ),
        ),
        # Run2012A+B
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5126), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0340381640021, 0.00463450761548),
                triggerBin(30.0, 0.408943965517, 0.0117283297034),
                triggerBin(40.0, 0.856763925729, 0.0139146304489),
                triggerBin(50.0, 0.874316939891, 0.0294758382406),
                triggerBin(60.0, 0.809523809524, 0.0462209862101),
                triggerBin(80.0, 0.9, 0.116971358051),
                triggerBin(100.0, 0.9, 0.194135389638),
                triggerBin(200.0, 1.0, 0.841344746068),
            ),
        ),
        # Run2012A+B+C
        runs_190456_202585 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(202585),
            luminosity = cms.double(11736), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.03645443196, 0.00320804524058),
                triggerBin(30.0, 0.407093292213, 0.00802781315525),
                triggerBin(40.0, 0.86799501868, 0.00899465558031),
                triggerBin(50.0, 0.86387434555, 0.0198669137269),
                triggerBin(60.0, 0.821428571429, 0.0316438887059),
                triggerBin(80.0, 0.853658536585, 0.077169526135),
                triggerBin(100.0, 0.857142857143, 0.119718786455),
                triggerBin(200.0, 1.0, 0.601684479424),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0355555555556, 0.0170677719482),
                triggerBin(30.0, 0.453376205788, 0.0299443626527),
                triggerBin(40.0, 0.877697841727, 0.0344007007134),
                triggerBin(50.0, 0.96, 0.0860511873626),
                triggerBin(60.0, 0.933333333333, 0.13708010169),
                triggerBin(80.0, 0.833333333333, 0.287350389332),
                triggerBin(100.0, 1.0, 0.308024223477),
                triggerBin(200.0, 1.0, 0.308024223477), # duplicated bin
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0395256916996, 0.0163885425304),
                triggerBin(30.0, 0.470930232558, 0.0284116833895),
                triggerBin(40.0, 0.872727272727, 0.0314554687838),
                triggerBin(50.0, 1.0, 0.0738408910804),
                triggerBin(60.0, 1.0, 0.0923494906334),
                triggerBin(80.0, 1.0, 0.18499249774),
                triggerBin(100.0, 1.0, 0.26422943474),
                triggerBin(200.0, 1.0, 0.26422943474), # duplicated bin
            ),
        ),
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0587392550143, 0.0103062935268),
                triggerBin(30.0, 0.466666666667, 0.0140488625609),
                triggerBin(40.0, 0.889078498294, 0.0145315210749),
                triggerBin(50.0, 0.978021978022, 0.028252856261),
                triggerBin(60.0, 1.0, 0.0527078145683),
                triggerBin(80.0, 1.0, 0.0461088219835),
                triggerBin(100.0, 1.0, 0.458641675296),
                triggerBin(200.0, 1.0, 0.458641675296), # duplicated bin
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0273224043716, 0.0180603993343),
                triggerBin(30.0, 0.478723404255, 0.0391026762452),
                triggerBin(40.0, 0.857142857143, 0.0444785255553),
                triggerBin(50.0, 0.928571428571, 0.145680517857),
                triggerBin(60.0, 0.941176470588, 0.12258022277),
                triggerBin(80.0, 1.0, 0.36887757085),
                triggerBin(100.0, 1.0, 0.26422943474),
                triggerBin(200.0, 1.0, 0.26422943474), # duplicated bin
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0292682926829, 0.0170724864488),
                triggerBin(30.0, 0.437062937063, 0.0312544531642),
                triggerBin(40.0, 0.883333333333, 0.0370545348233),
                triggerBin(50.0, 0.923076923077, 0.0925777957157),
                triggerBin(60.0, 1.0, 0.154109706156),
                triggerBin(80.0, 0.75, 0.368402425504),
                triggerBin(100.0, 1.0, 0.36887757085),
                triggerBin(200.0, 1.0, 0.36887757085), # duplicated bin
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0327868852459, 0.0110620921044),
                triggerBin(30.0, 0.437603993344, 0.0211578608225),
                triggerBin(40.0, 0.887931034483, 0.0246967331659),
                triggerBin(50.0, 0.942307692308, 0.0529489290724),
                triggerBin(60.0, 0.958333333333, 0.0893854708528),
                triggerBin(80.0, 0.857142857143, 0.257123832984),
                triggerBin(100.0, 1.0, 0.26422943474),
                triggerBin(200.0, 1.0, 0.26422943474), # duplicated bin
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABC"),
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

    # Offline selection: PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstMuonTight > 0.5&& MuonTauInvMass < 80&& PFTau_againstElectronMVA > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr > 0.5

    dataParameters = cms.PSet(
        # Run2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(697), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0267175572519, 0.0140943842682),
                triggerBin(30.0, 0.418772563177, 0.0316992998044),
                triggerBin(40.0, 0.827956989247, 0.0483272737625),
                triggerBin(50.0, 0.851851851852, 0.101731447858),
                triggerBin(60.0, 0.692307692308, 0.177171188325),
                triggerBin(80.0, 1.0, 0.458641675296),
                triggerBin(100.0, 0.0, 0.841344746068),
                triggerBin(200.0, 0.0, 0.841344746068), # duplicated bin
            ),
        ),
        # Run2012B
        runs_193834_196531 = cms.PSet(
            firstRun = cms.uint32(193834),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4428), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0351818723912, 0.00509675015801),
                triggerBin(30.0, 0.407219759341, 0.0127371917926),
                triggerBin(40.0, 0.860816944024, 0.0147916268304),
                triggerBin(50.0, 0.878205128205, 0.0320677129323),
                triggerBin(60.0, 0.826086956522, 0.0487813413935),
                triggerBin(80.0, 0.882352941176, 0.134601457887),
                triggerBin(100.0, 1.0, 0.18499249774),
                triggerBin(200.0, 1.0, 0.841344746068),
            ),
        ),
        # Run2012C
        runs_198022_202585 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(202585),
            luminosity = cms.double(6610), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0387221684414, 0.00472534092068),
                triggerBin(30.0, 0.405405405405, 0.0111741015059),
                triggerBin(40.0, 0.8779342723, 0.0122671022308),
                triggerBin(50.0, 0.854271356784, 0.0294428745967),
                triggerBin(60.0, 0.835164835165, 0.0483979551099),
                triggerBin(80.0, 0.809523809524, 0.125184034189),
                triggerBin(100.0, 0.818181818182, 0.1914016948),
                triggerBin(200.0, 1.0, 0.841344746068),
            ),
        ),
        # Run2012A+B
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5126), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0340381640021, 0.00463450761548),
                triggerBin(30.0, 0.408943965517, 0.0117283297034),
                triggerBin(40.0, 0.856763925729, 0.0139146304489),
                triggerBin(50.0, 0.874316939891, 0.0294758382406),
                triggerBin(60.0, 0.809523809524, 0.0462209862101),
                triggerBin(80.0, 0.9, 0.116971358051),
                triggerBin(100.0, 0.9, 0.194135389638),
                triggerBin(200.0, 1.0, 0.841344746068),
            ),
        ),
        # Run2012A+B+C
        runs_190456_202585 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(202585),
            luminosity = cms.double(11736), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.03645443196, 0.00320804524058),
                triggerBin(30.0, 0.407093292213, 0.00802781315525),
                triggerBin(40.0, 0.86799501868, 0.00899465558031),
                triggerBin(50.0, 0.86387434555, 0.0198669137269),
                triggerBin(60.0, 0.821428571429, 0.0316438887059),
                triggerBin(80.0, 0.853658536585, 0.077169526135),
                triggerBin(100.0, 0.857142857143, 0.119718786455),
                triggerBin(200.0, 1.0, 0.601684479424),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0355555555556, 0.0170677719482),
                triggerBin(30.0, 0.453376205788, 0.0299443626527),
                triggerBin(40.0, 0.877697841727, 0.0344007007134),
                triggerBin(50.0, 0.96, 0.0860511873626),
                triggerBin(60.0, 0.933333333333, 0.13708010169),
                triggerBin(80.0, 0.833333333333, 0.287350389332),
                triggerBin(100.0, 1.0, 0.308024223477),
                triggerBin(200.0, 1.0, 0.308024223477), # duplicated bin
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0395256916996, 0.0163885425304),
                triggerBin(30.0, 0.470930232558, 0.0284116833895),
                triggerBin(40.0, 0.872727272727, 0.0314554687838),
                triggerBin(50.0, 1.0, 0.0738408910804),
                triggerBin(60.0, 1.0, 0.0923494906334),
                triggerBin(80.0, 1.0, 0.18499249774),
                triggerBin(100.0, 1.0, 0.26422943474),
                triggerBin(200.0, 1.0, 0.26422943474), # duplicated bin
            ),
        ),
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0587392550143, 0.0103062935268),
                triggerBin(30.0, 0.466666666667, 0.0140488625609),
                triggerBin(40.0, 0.889078498294, 0.0145315210749),
                triggerBin(50.0, 0.978021978022, 0.028252856261),
                triggerBin(60.0, 1.0, 0.0527078145683),
                triggerBin(80.0, 1.0, 0.0461088219835),
                triggerBin(100.0, 1.0, 0.458641675296),
                triggerBin(200.0, 1.0, 0.458641675296), # duplicated bin
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0273224043716, 0.0180603993343),
                triggerBin(30.0, 0.478723404255, 0.0391026762452),
                triggerBin(40.0, 0.857142857143, 0.0444785255553),
                triggerBin(50.0, 0.928571428571, 0.145680517857),
                triggerBin(60.0, 0.941176470588, 0.12258022277),
                triggerBin(80.0, 1.0, 0.36887757085),
                triggerBin(100.0, 1.0, 0.26422943474),
                triggerBin(200.0, 1.0, 0.26422943474), # duplicated bin
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0292682926829, 0.0170724864488),
                triggerBin(30.0, 0.437062937063, 0.0312544531642),
                triggerBin(40.0, 0.883333333333, 0.0370545348233),
                triggerBin(50.0, 0.923076923077, 0.0925777957157),
                triggerBin(60.0, 1.0, 0.154109706156),
                triggerBin(80.0, 0.75, 0.368402425504),
                triggerBin(100.0, 1.0, 0.36887757085),
                triggerBin(200.0, 1.0, 0.36887757085), # duplicated bin
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0327868852459, 0.0110620921044),
                triggerBin(30.0, 0.437603993344, 0.0211578608225),
                triggerBin(40.0, 0.887931034483, 0.0246967331659),
                triggerBin(50.0, 0.942307692308, 0.0529489290724),
                triggerBin(60.0, 0.958333333333, 0.0893854708528),
                triggerBin(80.0, 0.857142857143, 0.257123832984),
                triggerBin(100.0, 1.0, 0.26422943474),
                triggerBin(200.0, 1.0, 0.26422943474), # duplicated bin
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABC"),
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

    # Offline selection: PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstMuonTight > 0.5&& MuonTauInvMass < 80&& PFTau_againstElectronMedium > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr > 0.5

    dataParameters = cms.PSet(
        # Run2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(697), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0261437908497, 0.0126406822336),
                triggerBin(30.0, 0.421383647799, 0.0294751086197),
                triggerBin(40.0, 0.785046728972, 0.0471723344386),
                triggerBin(50.0, 0.862068965517, 0.0956983526631),
                triggerBin(60.0, 0.733333333333, 0.161145049639),
                triggerBin(80.0, 1.0, 0.458641675296),
                triggerBin(100.0, 0.0, 0.841344746068),
                triggerBin(200.0, 0.0, 0.841344746068), # duplicated bin
            ),
        ),
        # Run2012B
        runs_193834_196531 = cms.PSet(
            firstRun = cms.uint32(193834),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4428), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.037493304767, 0.00493036813593),
                triggerBin(30.0, 0.405221339387, 0.0120310028558),
                triggerBin(40.0, 0.846685082873, 0.0145793078104),
                triggerBin(50.0, 0.85632183908, 0.0316837763512),
                triggerBin(60.0, 0.821782178218, 0.0464539610827),
                triggerBin(80.0, 0.882352941176, 0.134601457887),
                triggerBin(100.0, 1.0, 0.154109706156),
                triggerBin(200.0, 1.0, 0.841344746068),
            ),
        ),
        # Run2012C
        runs_198022_202585 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(202585),
            luminosity = cms.double(6610), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.043250327654, 0.00468205542596),
                triggerBin(30.0, 0.400879120879, 0.0105367729812),
                triggerBin(40.0, 0.859556494192, 0.0122133841382),
                triggerBin(50.0, 0.847926267281, 0.0283982969726),
                triggerBin(60.0, 0.815533980583, 0.0463476512865),
                triggerBin(80.0, 0.782608695652, 0.120323537142),
                triggerBin(100.0, 0.769230769231, 0.174723757631),
                triggerBin(200.0, 1.0, 0.841344746068),
            ),
        ),
        # Run2012A+B
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5126), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0358950759319, 0.00444942028415),
                triggerBin(30.0, 0.407692307692, 0.0110578713405),
                triggerBin(40.0, 0.838748495788, 0.0137817101587),
                triggerBin(50.0, 0.857142857143, 0.0289212043136),
                triggerBin(60.0, 0.810344827586, 0.0435534126686),
                triggerBin(80.0, 0.9, 0.116971358051),
                triggerBin(100.0, 0.916666666667, 0.166519597077),
                triggerBin(200.0, 1.0, 0.841344746068),
            ),
        ),
        # Run2012A+B+C
        runs_190456_202585 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(202585),
            luminosity = cms.double(11736), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0396683101748, 0.00314194674417),
                triggerBin(30.0, 0.404133180253, 0.00757236000815),
                triggerBin(40.0, 0.849831271091, 0.0089554971757),
                triggerBin(50.0, 0.852380952381, 0.0193845026464),
                triggerBin(60.0, 0.812785388128, 0.0301446146979),
                triggerBin(80.0, 0.837209302326, 0.0766334033584),
                triggerBin(100.0, 0.84, 0.10854843784),
                triggerBin(200.0, 1.0, 0.601684479424),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0528301886792, 0.0175766612871),
                triggerBin(30.0, 0.448863636364, 0.0280421106358),
                triggerBin(40.0, 0.875862068966, 0.0336977613634),
                triggerBin(50.0, 0.903225806452, 0.0852576401872),
                triggerBin(60.0, 1.0, 0.115501778685),
                triggerBin(80.0, 1.0, 0.26422943474),
                triggerBin(100.0, 0.833333333333, 0.287350389332),
                triggerBin(200.0, 0.833333333333, 0.287350389332), # duplicated bin
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0635451505017, 0.0174290416553),
                triggerBin(30.0, 0.466145833333, 0.0268150926439),
                triggerBin(40.0, 0.869047619048, 0.0314064886584),
                triggerBin(50.0, 0.903225806452, 0.0852576401872),
                triggerBin(60.0, 1.0, 0.0923494906334),
                triggerBin(80.0, 1.0, 0.168149186138),
                triggerBin(100.0, 1.0, 0.26422943474),
                triggerBin(200.0, 1.0, 0.26422943474), # duplicated bin
            ),
        ),
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0815602836879, 0.0105284702399),
                triggerBin(30.0, 0.462975778547, 0.0134847751162),
                triggerBin(40.0, 0.890387858347, 0.0143719556449),
                triggerBin(50.0, 0.876033057851, 0.0375527752685),
                triggerBin(60.0, 1.0, 0.0527078145683),
                triggerBin(80.0, 0.975, 0.0551515705063),
                triggerBin(100.0, 0.833333333333, 0.287350389332),
                triggerBin(200.0, 0.833333333333, 0.287350389332), # duplicated bin
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0516431924883, 0.0199812851664),
                triggerBin(30.0, 0.472222222222, 0.0363305871727),
                triggerBin(40.0, 0.851485148515, 0.0441602263209),
                triggerBin(50.0, 0.941176470588, 0.12258022277),
                triggerBin(60.0, 0.941176470588, 0.12258022277),
                triggerBin(80.0, 1.0, 0.308024223477),
                triggerBin(100.0, 1.0, 0.26422943474),
                triggerBin(200.0, 1.0, 0.26422943474), # duplicated bin
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0416666666667, 0.017248941493),
                triggerBin(30.0, 0.435975609756, 0.0290646868546),
                triggerBin(40.0, 0.8828125, 0.0356789360919),
                triggerBin(50.0, 0.870967741935, 0.0903256568946),
                triggerBin(60.0, 0.916666666667, 0.166519597077),
                triggerBin(80.0, 0.75, 0.368402425504),
                triggerBin(100.0, 0.833333333333, 0.287350389332),
                triggerBin(200.0, 0.833333333333, 0.287350389332), # duplicated bin
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.049504950495, 0.0116408705379),
                triggerBin(30.0, 0.431034482759, 0.0195781276306),
                triggerBin(40.0, 0.887596899225, 0.0232409116684),
                triggerBin(50.0, 0.91935483871, 0.0508738752303),
                triggerBin(60.0, 0.923076923077, 0.0925777957157),
                triggerBin(80.0, 0.777777777778, 0.221429368878),
                triggerBin(100.0, 0.875, 0.23225032014),
                triggerBin(200.0, 0.875, 0.23225032014), # duplicated bin
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABC"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)
