# Generated on Mon Mar 18 15:55:23 2013
# by HiggsAnalysis/TriggerEfficiency/test/PythonWriter.py

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
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(6892), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 1.0, 0.0),
            ),
        ),
        # Run2012D
        runs_202807_208686 = cms.PSet(
            firstRun = cms.uint32(202807),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7274), # 1/pb
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
        # Run2012A+B+C+D
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19296), # 1/pb
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
        # Run2012A+B+C+D
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19296), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0298507462687, 0.00327466366006),
                triggerBin(25.0, 0.0433905146317, 0.00406658859772),
                triggerBin(29.0, 0.0899137358991, 0.00551706231864),
                triggerBin(33.0, 0.4, 0.00941154256627),
                triggerBin(37.0, 0.78747714808, 0.00910762902684),
                triggerBin(41.0, 0.843793584379, 0.0101826695001),
                triggerBin(45.0, 0.822799097065, 0.013768112498),
                triggerBin(50.0, 0.85, 0.0194923139367),
                triggerBin(55.0, 0.816143497758, 0.0296750910554),
                triggerBin(60.0, 0.833333333333, 0.0272294675165),
                triggerBin(70.0, 0.821782178218, 0.0464539610827),
                triggerBin(80.0, 0.811594202899, 0.0591701336487),
                triggerBin(100.0, 0.857142857143, 0.0850949832061),
            ),
        ),
        # Run2012A+B+C
        runs_190456_202585 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(202585),
            luminosity = cms.double(11736), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.03125, 0.00557681828814),
                triggerBin(25.0, 0.0319240724763, 0.00604049212332),
                triggerBin(29.0, 0.077057793345, 0.00872201935563),
                triggerBin(33.0, 0.3815915628, 0.0156307044292),
                triggerBin(37.0, 0.750283768445, 0.0154384370959),
                triggerBin(41.0, 0.824253075571, 0.0174262846041),
                triggerBin(45.0, 0.798270893372, 0.0238748558915),
                triggerBin(50.0, 0.83908045977, 0.0328198640903),
                triggerBin(55.0, 0.780821917808, 0.0592886752617),
                triggerBin(60.0, 0.76, 0.0503802396961),
                triggerBin(70.0, 0.790697674419, 0.0807924269882),
                triggerBin(80.0, 0.821428571429, 0.102762023591),
                triggerBin(100.0, 0.875, 0.141688278764),
            ),
        ),
        # Run2012A+B
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5126), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0297790585975, 0.00625097471723),
                triggerBin(25.0, 0.0315904139434, 0.00688665414707),
                triggerBin(29.0, 0.0899122807018, 0.0104971745993),
                triggerBin(33.0, 0.41155234657, 0.0177722829968),
                triggerBin(37.0, 0.809455587393, 0.0160384113817),
                triggerBin(41.0, 0.857142857143, 0.0189891236775),
                triggerBin(45.0, 0.809338521401, 0.0277092756268),
                triggerBin(50.0, 0.861313868613, 0.0360683123585),
                triggerBin(55.0, 0.848484848485, 0.0575785928796),
                triggerBin(60.0, 0.821428571429, 0.0518678580231),
                triggerBin(70.0, 0.78125, 0.0978124398978),
                triggerBin(80.0, 0.9, 0.116971358051),
                triggerBin(100.0, 0.916666666667, 0.166519597077),
            ),
        ),
        # Run2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(697.308), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0131578947368, 0.0170904558787),
                triggerBin(25.0, 0.016393442623, 0.0212125133111),
                triggerBin(29.0, 0.117647058824, 0.0344372890982),
                triggerBin(33.0, 0.428571428571, 0.0499948122083),
                triggerBin(37.0, 0.773109243697, 0.0449744631853),
                triggerBin(41.0, 0.829787234043, 0.0731720068018),
                triggerBin(45.0, 0.666666666667, 0.0963989814963),
                triggerBin(50.0, 0.85, 0.12471137336),
                triggerBin(55.0, 0.888888888889, 0.211557930346),
                triggerBin(60.0, 0.818181818182, 0.1914016948),
                triggerBin(70.0, 0.5, 0.314698893873),
                triggerBin(80.0, 1.0, 0.458641675296),
                triggerBin(100.0, 0.0, 0.841344746068),
            ),
        ),
        # Run2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4430), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0326209223847, 0.00710669061046),
                triggerBin(25.0, 0.0339195979899, 0.00769948887783),
                triggerBin(29.0, 0.0850515463918, 0.0112292340389),
                triggerBin(33.0, 0.408707865169, 0.0192449073231),
                triggerBin(37.0, 0.816925734024, 0.0175023655728),
                triggerBin(41.0, 0.860526315789, 0.0200949702756),
                triggerBin(45.0, 0.83257918552, 0.0289748752395),
                triggerBin(50.0, 0.863247863248, 0.0394651025737),
                triggerBin(55.0, 0.842105263158, 0.0637264282034),
                triggerBin(60.0, 0.821917808219, 0.0563995455401),
                triggerBin(70.0, 0.821428571429, 0.102762023591),
                triggerBin(80.0, 0.882352941176, 0.134601457887),
                triggerBin(100.0, 1.0, 0.154109706156),
            ),
        ),
        # Run2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(6892), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0369003690037, 0.0153296554325),
                triggerBin(25.0, 0.0373443983402, 0.0165898716156),
                triggerBin(29.0, 0.0695652173913, 0.0210791423028),
                triggerBin(33.0, 0.344339622642, 0.0356942286751),
                triggerBin(37.0, 0.770491803279, 0.0353430479337),
                triggerBin(41.0, 0.880281690141, 0.0337377253056),
                triggerBin(45.0, 0.888888888889, 0.043620757271),
                triggerBin(50.0, 0.837837837838, 0.0842807841643),
                triggerBin(55.0, 0.857142857143, 0.257123832984),
                triggerBin(60.0, 0.625, 0.156048626467),
                triggerBin(70.0, 0.818181818182, 0.1914016948),
                triggerBin(80.0, 0.75, 0.239566802733),
                triggerBin(100.0, 0.75, 0.368402425504),
            ),
        ),
        # Run2012D
        runs_202807_208686 = cms.PSet(
            firstRun = cms.uint32(202807),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7274), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0337268128162, 0.00609533781077),
                triggerBin(25.0, 0.0417052826691, 0.00701284369062),
                triggerBin(29.0, 0.0960144927536, 0.00970465900477),
                triggerBin(33.0, 0.414587332054, 0.0158184836808),
                triggerBin(37.0, 0.810635538262, 0.0151736703235),
                triggerBin(41.0, 0.848722986248, 0.0175833660209),
                triggerBin(45.0, 0.831804281346, 0.0232811941134),
                triggerBin(50.0, 0.850340136054, 0.0354106621131),
                triggerBin(55.0, 0.842105263158, 0.053358948161),
                triggerBin(60.0, 0.89247311828, 0.0423330145355),
                triggerBin(70.0, 0.857142857143, 0.0850949832061),
                triggerBin(80.0, 0.807692307692, 0.109171931537),
                triggerBin(100.0, 0.9, 0.194135389638),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0416666666667, 0.0199072079734),
                triggerBin(25.0, 0.0295358649789, 0.0155465860392),
                triggerBin(29.0, 0.0865384615385, 0.0241318675839),
                triggerBin(33.0, 0.509868421053, 0.0302977490853),
                triggerBin(37.0, 0.886255924171, 0.026237053517),
                triggerBin(41.0, 0.915151515152, 0.0275893900003),
                triggerBin(45.0, 0.858585858586, 0.0440781851327),
                triggerBin(50.0, 0.911764705882, 0.0784415663023),
                triggerBin(55.0, 0.869565217391, 0.11081369682),
                triggerBin(60.0, 0.833333333333, 0.135998901491),
                triggerBin(70.0, 0.857142857143, 0.257123832984),
                triggerBin(80.0, 1.0, 0.308024223477),
                triggerBin(100.0, 0.9, 0.194135389638),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0441176470588, 0.0162517043448),
                triggerBin(25.0, 0.0353260869565, 0.0124571515126),
                triggerBin(29.0, 0.0764331210191, 0.0180860814288),
                triggerBin(33.0, 0.514412416851, 0.0246477998365),
                triggerBin(37.0, 0.88996763754, 0.0207893669048),
                triggerBin(41.0, 0.930735930736, 0.020992329012),
                triggerBin(45.0, 0.848920863309, 0.0366989293981),
                triggerBin(50.0, 0.88, 0.0647939679021),
                triggerBin(55.0, 0.9, 0.0877974084544),
                triggerBin(60.0, 0.833333333333, 0.0970335931041),
                triggerBin(70.0, 0.9, 0.194135389638),
                triggerBin(80.0, 1.0, 0.18499249774),
                triggerBin(100.0, 0.933333333333, 0.13708010169),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.05, 0.0166682485701),
                triggerBin(25.0, 0.0402010050251, 0.0124316960968),
                triggerBin(29.0, 0.0722891566265, 0.0171530381657),
                triggerBin(33.0, 0.523305084746, 0.0240736712428),
                triggerBin(37.0, 0.89751552795, 0.0197980305329),
                triggerBin(41.0, 0.928571428571, 0.0208356133221),
                triggerBin(45.0, 0.847133757962, 0.0342939361459),
                triggerBin(50.0, 0.897959183673, 0.06313660811),
                triggerBin(55.0, 0.9, 0.0877974084544),
                triggerBin(60.0, 0.857142857143, 0.0850949832061),
                triggerBin(70.0, 0.833333333333, 0.179009937646),
                triggerBin(80.0, 0.923076923077, 0.155415375679),
                triggerBin(100.0, 0.9375, 0.129429134796),
            ),
        ),
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0715705765408, 0.0134193895344),
                triggerBin(25.0, 0.0648967551622, 0.0108957303123),
                triggerBin(29.0, 0.0629183400268, 0.0101881363806),
                triggerBin(33.0, 0.535490605428, 0.0166647320717),
                triggerBin(37.0, 0.876273653566, 0.0138668411598),
                triggerBin(41.0, 0.930288461538, 0.014830181176),
                triggerBin(45.0, 0.869822485207, 0.0209528635407),
                triggerBin(50.0, 0.884297520661, 0.0367748729899),
                triggerBin(55.0, 0.905660377358, 0.0587823296232),
                triggerBin(60.0, 0.611111111111, 0.145378985762),
                triggerBin(70.0, 0.971428571429, 0.0626552130481),
                triggerBin(80.0, 0.975, 0.0551515705063),
                triggerBin(100.0, 1.0, 0.0923494906334),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0408163265306, 0.0169075502588),
                triggerBin(25.0, 0.0338983050847, 0.0125786564392),
                triggerBin(29.0, 0.0749063670412, 0.0197697265989),
                triggerBin(33.0, 0.518987341772, 0.0264207846138),
                triggerBin(37.0, 0.905303030303, 0.0216082320093),
                triggerBin(41.0, 0.928571428571, 0.02248197781),
                triggerBin(45.0, 0.829457364341, 0.0397338095199),
                triggerBin(50.0, 0.918918918919, 0.0726264763228),
                triggerBin(55.0, 0.888888888889, 0.0963981300751),
                triggerBin(60.0, 0.891891891892, 0.0772589573026),
                triggerBin(70.0, 0.875, 0.23225032014),
                triggerBin(80.0, 1.0, 0.205567857429),
                triggerBin(100.0, 1.0, 0.115501778685),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0374531835206, 0.0155529770872),
                triggerBin(25.0, 0.0317002881844, 0.0124442684863),
                triggerBin(29.0, 0.0764119601329, 0.01854129013),
                triggerBin(33.0, 0.509174311927, 0.0250803252879),
                triggerBin(37.0, 0.882943143813, 0.0216496486572),
                triggerBin(41.0, 0.929203539823, 0.0214336729972),
                triggerBin(45.0, 0.857142857143, 0.0382482675002),
                triggerBin(50.0, 0.9, 0.0619892518934),
                triggerBin(55.0, 0.9, 0.0877974084544),
                triggerBin(60.0, 0.814814814815, 0.105875016529),
                triggerBin(70.0, 0.888888888889, 0.211557930346),
                triggerBin(80.0, 0.857142857143, 0.257123832984),
                triggerBin(100.0, 0.866666666667, 0.14953714223),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0416666666667, 0.0199072079734),
                triggerBin(25.0, 0.0295358649789, 0.0155465860392),
                triggerBin(29.0, 0.0865384615385, 0.0241318675839),
                triggerBin(33.0, 0.509868421053, 0.0302977490853),
                triggerBin(37.0, 0.886255924171, 0.026237053517),
                triggerBin(41.0, 0.915151515152, 0.0275893900003),
                triggerBin(45.0, 0.858585858586, 0.0440781851327),
                triggerBin(50.0, 0.911764705882, 0.0784415663023),
                triggerBin(55.0, 0.869565217391, 0.11081369682),
                triggerBin(60.0, 0.833333333333, 0.135998901491),
                triggerBin(70.0, 0.857142857143, 0.257123832984),
                triggerBin(80.0, 1.0, 0.308024223477),
                triggerBin(100.0, 0.9, 0.194135389638),
            ),
        ),
        Summer12_PU_2012Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0326086956522, 0.0145376677),
                triggerBin(25.0, 0.0494791666667, 0.0137009677138),
                triggerBin(29.0, 0.0576036866359, 0.0134737942085),
                triggerBin(33.0, 0.473568281938, 0.0245673340105),
                triggerBin(37.0, 0.832891246684, 0.0214672570348),
                triggerBin(41.0, 0.885462555066, 0.0251977518915),
                triggerBin(45.0, 0.854166666667, 0.0355612697361),
                triggerBin(50.0, 0.867647058824, 0.0545661227401),
                triggerBin(55.0, 0.878787878788, 0.0855133855999),
                triggerBin(60.0, 0.863636363636, 0.11509911457),
                triggerBin(70.0, 0.9375, 0.129429134796),
                triggerBin(80.0, 0.846153846154, 0.16803608658),
                triggerBin(100.0, 0.818181818182, 0.1914016948),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
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
        # Run2012A+B+C+D
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19296), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0289367429341, 0.00341238045286),
                triggerBin(25.0, 0.0389413988658, 0.00413554001474),
                triggerBin(29.0, 0.0832408435072, 0.00565834145379),
                triggerBin(33.0, 0.399921197794, 0.00995929980447),
                triggerBin(37.0, 0.808456444218, 0.00929665691871),
                triggerBin(41.0, 0.859784283513, 0.0103092887925),
                triggerBin(45.0, 0.844696969697, 0.0139534762944),
                triggerBin(50.0, 0.860892388451, 0.0200471135021),
                triggerBin(55.0, 0.833333333333, 0.0313506035741),
                triggerBin(60.0, 0.848623853211, 0.0282818721873),
                triggerBin(70.0, 0.818181818182, 0.0506834089307),
                triggerBin(80.0, 0.830769230769, 0.0597642650493),
                triggerBin(100.0, 0.870967741935, 0.0903256568946),
            ),
        ),
        # Run2012A+B+C
        runs_190456_202585 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(202585),
            luminosity = cms.double(11736), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0301760268231, 0.00580687197502),
                triggerBin(25.0, 0.0332355816227, 0.00659795525087),
                triggerBin(29.0, 0.0716360116167, 0.00894993895621),
                triggerBin(33.0, 0.377317339149, 0.0166812631904),
                triggerBin(37.0, 0.769426751592, 0.0160198977746),
                triggerBin(41.0, 0.843629343629, 0.017618143007),
                triggerBin(45.0, 0.816129032258, 0.0246817027226),
                triggerBin(50.0, 0.860759493671, 0.0331957180327),
                triggerBin(55.0, 0.787878787879, 0.06248519847),
                triggerBin(60.0, 0.775280898876, 0.0530783889698),
                triggerBin(70.0, 0.794871794872, 0.0854809640957),
                triggerBin(80.0, 0.851851851852, 0.101731447858),
                triggerBin(100.0, 0.916666666667, 0.166519597077),
            ),
        ),
        # Run2012A+B
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5126), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0285412262156, 0.00650076737962),
                triggerBin(25.0, 0.0324594257179, 0.00754053672132),
                triggerBin(29.0, 0.0839416058394, 0.010819989229),
                triggerBin(33.0, 0.405479452055, 0.0189782464046),
                triggerBin(37.0, 0.828843106181, 0.0163274515538),
                triggerBin(41.0, 0.866666666667, 0.0194954719327),
                triggerBin(45.0, 0.838427947598, 0.0280781028504),
                triggerBin(50.0, 0.879032258065, 0.0367264035175),
                triggerBin(55.0, 0.864406779661, 0.0600495172513),
                triggerBin(60.0, 0.828947368421, 0.0544809662773),
                triggerBin(70.0, 0.758620689655, 0.105613026829),
                triggerBin(80.0, 0.9, 0.116971358051),
                triggerBin(100.0, 0.9, 0.194135389638),
            ),
        ),
        # Run2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(697.308), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0148148148148, 0.0192053120757),
                triggerBin(25.0, 0.020202020202, 0.0260240873214),
                triggerBin(29.0, 0.115702479339, 0.0367748729899),
                triggerBin(33.0, 0.421568627451, 0.0543523892995),
                triggerBin(37.0, 0.798076923077, 0.0471984184233),
                triggerBin(41.0, 0.868421052632, 0.0792158922547),
                triggerBin(45.0, 0.69696969697, 0.100556702757),
                triggerBin(50.0, 0.842105263158, 0.130121162629),
                triggerBin(55.0, 0.875, 0.23225032014),
                triggerBin(60.0, 0.8, 0.205453750763),
                triggerBin(70.0, 0.333333333333, 0.414534706285),
                triggerBin(80.0, 1.0, 0.458641675296),
                triggerBin(100.0, 0.0, 0.841344746068),
            ),
        ),
        # Run2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4430), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0308261405672, 0.00733647052764),
                triggerBin(25.0, 0.034188034188, 0.00831760050497),
                triggerBin(29.0, 0.0784593437946, 0.0115157762126),
                triggerBin(33.0, 0.402866242038, 0.0205125813729),
                triggerBin(37.0, 0.834914611006, 0.0177841275084),
                triggerBin(41.0, 0.866477272727, 0.0206605226432),
                triggerBin(45.0, 0.862244897959, 0.0291707244581),
                triggerBin(50.0, 0.885714285714, 0.0399650544691),
                triggerBin(55.0, 0.862745098039, 0.0660830754776),
                triggerBin(60.0, 0.833333333333, 0.058982956237),
                triggerBin(70.0, 0.807692307692, 0.109171931537),
                triggerBin(80.0, 0.882352941176, 0.134601457887),
                triggerBin(100.0, 1.0, 0.18499249774),
            ),
        ),
        # Run2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(6892), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0364372469636, 0.0161979228841),
                triggerBin(25.0, 0.0405405405405, 0.0179664207031),
                triggerBin(29.0, 0.0663507109005, 0.0218641334224),
                triggerBin(33.0, 0.342245989305, 0.0381748187385),
                triggerBin(37.0, 0.792207792208, 0.0379266786567),
                triggerBin(41.0, 0.90625, 0.0332989673195),
                triggerBin(45.0, 0.888888888889, 0.0466071218355),
                triggerBin(50.0, 0.882352941176, 0.0832913466933),
                triggerBin(55.0, 0.857142857143, 0.257123832984),
                triggerBin(60.0, 0.615384615385, 0.176146427336),
                triggerBin(70.0, 0.9, 0.194135389638),
                triggerBin(80.0, 0.857142857143, 0.257123832984),
                triggerBin(100.0, 1.0, 0.601684479424),
            ),
        ),
        # Run2012D
        runs_202807_208686 = cms.PSet(
            firstRun = cms.uint32(202807),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7274), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0320452403393, 0.00636634374696),
                triggerBin(25.0, 0.0350154479918, 0.00694361940856),
                triggerBin(29.0, 0.0897177419355, 0.0100149466342),
                triggerBin(33.0, 0.41887592789, 0.0166765993851),
                triggerBin(37.0, 0.828282828283, 0.0155385996323),
                triggerBin(41.0, 0.862445414847, 0.0180227554435),
                triggerBin(45.0, 0.855670103093, 0.0236228634785),
                triggerBin(50.0, 0.852713178295, 0.0380625615327),
                triggerBin(55.0, 0.903225806452, 0.0533288493999),
                triggerBin(60.0, 0.9125, 0.0439472300684),
                triggerBin(70.0, 0.833333333333, 0.0970335931041),
                triggerBin(80.0, 0.833333333333, 0.112297423319),
                triggerBin(100.0, 0.9, 0.194135389638),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.046783625731, 0.0222634456645),
                triggerBin(25.0, 0.0208333333333, 0.0161658239383),
                triggerBin(29.0, 0.0864864864865, 0.0258944149192),
                triggerBin(33.0, 0.548148148148, 0.0322655682988),
                triggerBin(37.0, 0.885416666667, 0.0278020255416),
                triggerBin(41.0, 0.911392405063, 0.0287329340748),
                triggerBin(45.0, 0.852631578947, 0.045723547021),
                triggerBin(50.0, 0.878787878788, 0.0855133855999),
                triggerBin(55.0, 0.909090909091, 0.10754400896),
                triggerBin(60.0, 0.714285714286, 0.168877178575),
                triggerBin(70.0, 1.0, 0.26422943474),
                triggerBin(80.0, 1.0, 0.308024223477),
                triggerBin(100.0, 1.0, 0.18499249774),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0413223140496, 0.0171107456738),
                triggerBin(25.0, 0.023178807947, 0.0122616141108),
                triggerBin(29.0, 0.0744680851064, 0.0190964060071),
                triggerBin(33.0, 0.563775510204, 0.0264588666335),
                triggerBin(37.0, 0.89247311828, 0.021872715167),
                triggerBin(41.0, 0.928251121076, 0.0217074709481),
                triggerBin(45.0, 0.844444444444, 0.0376617581814),
                triggerBin(50.0, 0.931818181818, 0.0619005708815),
                triggerBin(55.0, 0.896551724138, 0.0904910256742),
                triggerBin(60.0, 0.789473684211, 0.135427055903),
                triggerBin(70.0, 1.0, 0.18499249774),
                triggerBin(80.0, 0.888888888889, 0.211557930346),
                triggerBin(100.0, 1.0, 0.123222080425),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0481927710843, 0.0177009382591),
                triggerBin(25.0, 0.0243902439024, 0.0118086143055),
                triggerBin(29.0, 0.0735785953177, 0.0183650432926),
                triggerBin(33.0, 0.579852579853, 0.0258676171664),
                triggerBin(37.0, 0.897959183673, 0.0208336487969),
                triggerBin(41.0, 0.926406926407, 0.021434577208),
                triggerBin(45.0, 0.837662337662, 0.0353189924478),
                triggerBin(50.0, 0.93023255814, 0.0632357940699),
                triggerBin(55.0, 0.928571428571, 0.0865437819796),
                triggerBin(60.0, 0.772727272727, 0.124519809699),
                triggerBin(70.0, 1.0, 0.168149186138),
                triggerBin(80.0, 1.0, 0.142229304965),
                triggerBin(100.0, 1.0, 0.115501778685),
            ),
        ),
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0567375886525, 0.0136024705758),
                triggerBin(25.0, 0.0495575221239, 0.0109022967425),
                triggerBin(29.0, 0.0608695652174, 0.0105202432245),
                triggerBin(33.0, 0.578143360752, 0.0176011713114),
                triggerBin(37.0, 0.87323943662, 0.0145593631069),
                triggerBin(41.0, 0.926108374384, 0.0153704547931),
                triggerBin(45.0, 0.868656716418, 0.0211240162466),
                triggerBin(50.0, 0.978021978022, 0.028252856261),
                triggerBin(55.0, 0.923076923077, 0.0566529821386),
                triggerBin(60.0, 0.529411764706, 0.147216225237),
                triggerBin(70.0, 1.0, 0.0527078145683),
                triggerBin(80.0, 0.975, 0.0551515705063),
                triggerBin(100.0, 1.0, 0.10263751542),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.045045045045, 0.0186008898042),
                triggerBin(25.0, 0.0171821305842, 0.0114562721736),
                triggerBin(29.0, 0.0759493670886, 0.0213362911472),
                triggerBin(33.0, 0.579881656805, 0.0285318159378),
                triggerBin(37.0, 0.904166666667, 0.0229484473995),
                triggerBin(41.0, 0.926470588235, 0.0231086736593),
                triggerBin(45.0, 0.832, 0.040299684095),
                triggerBin(50.0, 0.942857142857, 0.0704444114251),
                triggerBin(55.0, 0.92, 0.0959186952466),
                triggerBin(60.0, 0.826086956522, 0.116302557627),
                triggerBin(70.0, 1.0, 0.231260479746),
                triggerBin(80.0, 0.875, 0.23225032014),
                triggerBin(100.0, 1.0, 0.115501778685),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0379746835443, 0.0168618714856),
                triggerBin(25.0, 0.0212014134276, 0.012448604932),
                triggerBin(29.0, 0.0777777777778, 0.019900199409),
                triggerBin(33.0, 0.552631578947, 0.0269313444616),
                triggerBin(37.0, 0.888059701493, 0.0227025007459),
                triggerBin(41.0, 0.926267281106, 0.0222765265351),
                triggerBin(45.0, 0.844262295082, 0.0399937984814),
                triggerBin(50.0, 0.913043478261, 0.063430752713),
                triggerBin(55.0, 0.896551724138, 0.0904910256742),
                triggerBin(60.0, 0.764705882353, 0.147311672312),
                triggerBin(70.0, 1.0, 0.205567857429),
                triggerBin(80.0, 0.857142857143, 0.257123832984),
                triggerBin(100.0, 1.0, 0.132046423994),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.046783625731, 0.0222634456645),
                triggerBin(25.0, 0.0208333333333, 0.0161658239383),
                triggerBin(29.0, 0.0864864864865, 0.0258944149192),
                triggerBin(33.0, 0.548148148148, 0.0322655682988),
                triggerBin(37.0, 0.885416666667, 0.0278020255416),
                triggerBin(41.0, 0.911392405063, 0.0287329340748),
                triggerBin(45.0, 0.852631578947, 0.045723547021),
                triggerBin(50.0, 0.878787878788, 0.0855133855999),
                triggerBin(55.0, 0.909090909091, 0.10754400896),
                triggerBin(60.0, 0.714285714286, 0.168877178575),
                triggerBin(70.0, 1.0, 0.26422943474),
                triggerBin(80.0, 1.0, 0.308024223477),
                triggerBin(100.0, 1.0, 0.18499249774),
            ),
        ),
        Summer12_PU_2012Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0333333333333, 0.0160283955349),
                triggerBin(25.0, 0.034375, 0.0134682451879),
                triggerBin(29.0, 0.0474934036939, 0.0136051062375),
                triggerBin(33.0, 0.489847715736, 0.02644529354),
                triggerBin(37.0, 0.845921450151, 0.0224603271958),
                triggerBin(41.0, 0.899038461538, 0.0254217741473),
                triggerBin(45.0, 0.84962406015, 0.0376133269077),
                triggerBin(50.0, 0.883333333333, 0.0571758165749),
                triggerBin(55.0, 0.9, 0.0877974084544),
                triggerBin(60.0, 0.888888888889, 0.128174449784),
                triggerBin(70.0, 1.0, 0.115501778685),
                triggerBin(80.0, 0.909090909091, 0.179295209474),
                triggerBin(100.0, 1.0, 0.205567857429),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
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
        # Run2012A+B+C+D
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19296), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0289367429341, 0.00341238045286),
                triggerBin(25.0, 0.0389413988658, 0.00413554001474),
                triggerBin(29.0, 0.0832408435072, 0.00565834145379),
                triggerBin(33.0, 0.399921197794, 0.00995929980447),
                triggerBin(37.0, 0.808456444218, 0.00929665691871),
                triggerBin(41.0, 0.859784283513, 0.0103092887925),
                triggerBin(45.0, 0.844696969697, 0.0139534762944),
                triggerBin(50.0, 0.860892388451, 0.0200471135021),
                triggerBin(55.0, 0.833333333333, 0.0313506035741),
                triggerBin(60.0, 0.848623853211, 0.0282818721873),
                triggerBin(70.0, 0.818181818182, 0.0506834089307),
                triggerBin(80.0, 0.830769230769, 0.0597642650493),
                triggerBin(100.0, 0.870967741935, 0.0903256568946),
            ),
        ),
        # Run2012A+B+C
        runs_190456_202585 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(202585),
            luminosity = cms.double(11736), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0301760268231, 0.00580687197502),
                triggerBin(25.0, 0.0332355816227, 0.00659795525087),
                triggerBin(29.0, 0.0716360116167, 0.00894993895621),
                triggerBin(33.0, 0.377317339149, 0.0166812631904),
                triggerBin(37.0, 0.769426751592, 0.0160198977746),
                triggerBin(41.0, 0.843629343629, 0.017618143007),
                triggerBin(45.0, 0.816129032258, 0.0246817027226),
                triggerBin(50.0, 0.860759493671, 0.0331957180327),
                triggerBin(55.0, 0.787878787879, 0.06248519847),
                triggerBin(60.0, 0.775280898876, 0.0530783889698),
                triggerBin(70.0, 0.794871794872, 0.0854809640957),
                triggerBin(80.0, 0.851851851852, 0.101731447858),
                triggerBin(100.0, 0.916666666667, 0.166519597077),
            ),
        ),
        # Run2012A+B
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5126), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0285412262156, 0.00650076737962),
                triggerBin(25.0, 0.0324594257179, 0.00754053672132),
                triggerBin(29.0, 0.0839416058394, 0.010819989229),
                triggerBin(33.0, 0.405479452055, 0.0189782464046),
                triggerBin(37.0, 0.828843106181, 0.0163274515538),
                triggerBin(41.0, 0.866666666667, 0.0194954719327),
                triggerBin(45.0, 0.838427947598, 0.0280781028504),
                triggerBin(50.0, 0.879032258065, 0.0367264035175),
                triggerBin(55.0, 0.864406779661, 0.0600495172513),
                triggerBin(60.0, 0.828947368421, 0.0544809662773),
                triggerBin(70.0, 0.758620689655, 0.105613026829),
                triggerBin(80.0, 0.9, 0.116971358051),
                triggerBin(100.0, 0.9, 0.194135389638),
            ),
        ),
        # Run2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(697.308), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0148148148148, 0.0192053120757),
                triggerBin(25.0, 0.020202020202, 0.0260240873214),
                triggerBin(29.0, 0.115702479339, 0.0367748729899),
                triggerBin(33.0, 0.421568627451, 0.0543523892995),
                triggerBin(37.0, 0.798076923077, 0.0471984184233),
                triggerBin(41.0, 0.868421052632, 0.0792158922547),
                triggerBin(45.0, 0.69696969697, 0.100556702757),
                triggerBin(50.0, 0.842105263158, 0.130121162629),
                triggerBin(55.0, 0.875, 0.23225032014),
                triggerBin(60.0, 0.8, 0.205453750763),
                triggerBin(70.0, 0.333333333333, 0.414534706285),
                triggerBin(80.0, 1.0, 0.458641675296),
                triggerBin(100.0, 0.0, 0.841344746068),
            ),
        ),
        # Run2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4430), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0308261405672, 0.00733647052764),
                triggerBin(25.0, 0.034188034188, 0.00831760050497),
                triggerBin(29.0, 0.0784593437946, 0.0115157762126),
                triggerBin(33.0, 0.402866242038, 0.0205125813729),
                triggerBin(37.0, 0.834914611006, 0.0177841275084),
                triggerBin(41.0, 0.866477272727, 0.0206605226432),
                triggerBin(45.0, 0.862244897959, 0.0291707244581),
                triggerBin(50.0, 0.885714285714, 0.0399650544691),
                triggerBin(55.0, 0.862745098039, 0.0660830754776),
                triggerBin(60.0, 0.833333333333, 0.058982956237),
                triggerBin(70.0, 0.807692307692, 0.109171931537),
                triggerBin(80.0, 0.882352941176, 0.134601457887),
                triggerBin(100.0, 1.0, 0.18499249774),
            ),
        ),
        # Run2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(6892), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0364372469636, 0.0161979228841),
                triggerBin(25.0, 0.0405405405405, 0.0179664207031),
                triggerBin(29.0, 0.0663507109005, 0.0218641334224),
                triggerBin(33.0, 0.342245989305, 0.0381748187385),
                triggerBin(37.0, 0.792207792208, 0.0379266786567),
                triggerBin(41.0, 0.90625, 0.0332989673195),
                triggerBin(45.0, 0.888888888889, 0.0466071218355),
                triggerBin(50.0, 0.882352941176, 0.0832913466933),
                triggerBin(55.0, 0.857142857143, 0.257123832984),
                triggerBin(60.0, 0.615384615385, 0.176146427336),
                triggerBin(70.0, 0.9, 0.194135389638),
                triggerBin(80.0, 0.857142857143, 0.257123832984),
                triggerBin(100.0, 1.0, 0.601684479424),
            ),
        ),
        # Run2012D
        runs_202807_208686 = cms.PSet(
            firstRun = cms.uint32(202807),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7274), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0320452403393, 0.00636634374696),
                triggerBin(25.0, 0.0350154479918, 0.00694361940856),
                triggerBin(29.0, 0.0897177419355, 0.0100149466342),
                triggerBin(33.0, 0.41887592789, 0.0166765993851),
                triggerBin(37.0, 0.828282828283, 0.0155385996323),
                triggerBin(41.0, 0.862445414847, 0.0180227554435),
                triggerBin(45.0, 0.855670103093, 0.0236228634785),
                triggerBin(50.0, 0.852713178295, 0.0380625615327),
                triggerBin(55.0, 0.903225806452, 0.0533288493999),
                triggerBin(60.0, 0.9125, 0.0439472300684),
                triggerBin(70.0, 0.833333333333, 0.0970335931041),
                triggerBin(80.0, 0.833333333333, 0.112297423319),
                triggerBin(100.0, 0.9, 0.194135389638),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.046783625731, 0.0222634456645),
                triggerBin(25.0, 0.0208333333333, 0.0161658239383),
                triggerBin(29.0, 0.0864864864865, 0.0258944149192),
                triggerBin(33.0, 0.548148148148, 0.0322655682988),
                triggerBin(37.0, 0.885416666667, 0.0278020255416),
                triggerBin(41.0, 0.911392405063, 0.0287329340748),
                triggerBin(45.0, 0.852631578947, 0.045723547021),
                triggerBin(50.0, 0.878787878788, 0.0855133855999),
                triggerBin(55.0, 0.909090909091, 0.10754400896),
                triggerBin(60.0, 0.714285714286, 0.168877178575),
                triggerBin(70.0, 1.0, 0.26422943474),
                triggerBin(80.0, 1.0, 0.308024223477),
                triggerBin(100.0, 1.0, 0.18499249774),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0413223140496, 0.0171107456738),
                triggerBin(25.0, 0.023178807947, 0.0122616141108),
                triggerBin(29.0, 0.0744680851064, 0.0190964060071),
                triggerBin(33.0, 0.563775510204, 0.0264588666335),
                triggerBin(37.0, 0.89247311828, 0.021872715167),
                triggerBin(41.0, 0.928251121076, 0.0217074709481),
                triggerBin(45.0, 0.844444444444, 0.0376617581814),
                triggerBin(50.0, 0.931818181818, 0.0619005708815),
                triggerBin(55.0, 0.896551724138, 0.0904910256742),
                triggerBin(60.0, 0.789473684211, 0.135427055903),
                triggerBin(70.0, 1.0, 0.18499249774),
                triggerBin(80.0, 0.888888888889, 0.211557930346),
                triggerBin(100.0, 1.0, 0.123222080425),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0481927710843, 0.0177009382591),
                triggerBin(25.0, 0.0243902439024, 0.0118086143055),
                triggerBin(29.0, 0.0735785953177, 0.0183650432926),
                triggerBin(33.0, 0.579852579853, 0.0258676171664),
                triggerBin(37.0, 0.897959183673, 0.0208336487969),
                triggerBin(41.0, 0.926406926407, 0.021434577208),
                triggerBin(45.0, 0.837662337662, 0.0353189924478),
                triggerBin(50.0, 0.93023255814, 0.0632357940699),
                triggerBin(55.0, 0.928571428571, 0.0865437819796),
                triggerBin(60.0, 0.772727272727, 0.124519809699),
                triggerBin(70.0, 1.0, 0.168149186138),
                triggerBin(80.0, 1.0, 0.142229304965),
                triggerBin(100.0, 1.0, 0.115501778685),
            ),
        ),
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0567375886525, 0.0136024705758),
                triggerBin(25.0, 0.0495575221239, 0.0109022967425),
                triggerBin(29.0, 0.0608695652174, 0.0105202432245),
                triggerBin(33.0, 0.578143360752, 0.0176011713114),
                triggerBin(37.0, 0.87323943662, 0.0145593631069),
                triggerBin(41.0, 0.926108374384, 0.0153704547931),
                triggerBin(45.0, 0.868656716418, 0.0211240162466),
                triggerBin(50.0, 0.978021978022, 0.028252856261),
                triggerBin(55.0, 0.923076923077, 0.0566529821386),
                triggerBin(60.0, 0.529411764706, 0.147216225237),
                triggerBin(70.0, 1.0, 0.0527078145683),
                triggerBin(80.0, 0.975, 0.0551515705063),
                triggerBin(100.0, 1.0, 0.10263751542),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.045045045045, 0.0186008898042),
                triggerBin(25.0, 0.0171821305842, 0.0114562721736),
                triggerBin(29.0, 0.0759493670886, 0.0213362911472),
                triggerBin(33.0, 0.579881656805, 0.0285318159378),
                triggerBin(37.0, 0.904166666667, 0.0229484473995),
                triggerBin(41.0, 0.926470588235, 0.0231086736593),
                triggerBin(45.0, 0.832, 0.040299684095),
                triggerBin(50.0, 0.942857142857, 0.0704444114251),
                triggerBin(55.0, 0.92, 0.0959186952466),
                triggerBin(60.0, 0.826086956522, 0.116302557627),
                triggerBin(70.0, 1.0, 0.231260479746),
                triggerBin(80.0, 0.875, 0.23225032014),
                triggerBin(100.0, 1.0, 0.115501778685),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0379746835443, 0.0168618714856),
                triggerBin(25.0, 0.0212014134276, 0.012448604932),
                triggerBin(29.0, 0.0777777777778, 0.019900199409),
                triggerBin(33.0, 0.552631578947, 0.0269313444616),
                triggerBin(37.0, 0.888059701493, 0.0227025007459),
                triggerBin(41.0, 0.926267281106, 0.0222765265351),
                triggerBin(45.0, 0.844262295082, 0.0399937984814),
                triggerBin(50.0, 0.913043478261, 0.063430752713),
                triggerBin(55.0, 0.896551724138, 0.0904910256742),
                triggerBin(60.0, 0.764705882353, 0.147311672312),
                triggerBin(70.0, 1.0, 0.205567857429),
                triggerBin(80.0, 0.857142857143, 0.257123832984),
                triggerBin(100.0, 1.0, 0.132046423994),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.046783625731, 0.0222634456645),
                triggerBin(25.0, 0.0208333333333, 0.0161658239383),
                triggerBin(29.0, 0.0864864864865, 0.0258944149192),
                triggerBin(33.0, 0.548148148148, 0.0322655682988),
                triggerBin(37.0, 0.885416666667, 0.0278020255416),
                triggerBin(41.0, 0.911392405063, 0.0287329340748),
                triggerBin(45.0, 0.852631578947, 0.045723547021),
                triggerBin(50.0, 0.878787878788, 0.0855133855999),
                triggerBin(55.0, 0.909090909091, 0.10754400896),
                triggerBin(60.0, 0.714285714286, 0.168877178575),
                triggerBin(70.0, 1.0, 0.26422943474),
                triggerBin(80.0, 1.0, 0.308024223477),
                triggerBin(100.0, 1.0, 0.18499249774),
            ),
        ),
        Summer12_PU_2012Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0333333333333, 0.0160283955349),
                triggerBin(25.0, 0.034375, 0.0134682451879),
                triggerBin(29.0, 0.0474934036939, 0.0136051062375),
                triggerBin(33.0, 0.489847715736, 0.02644529354),
                triggerBin(37.0, 0.845921450151, 0.0224603271958),
                triggerBin(41.0, 0.899038461538, 0.0254217741473),
                triggerBin(45.0, 0.84962406015, 0.0376133269077),
                triggerBin(50.0, 0.883333333333, 0.0571758165749),
                triggerBin(55.0, 0.9, 0.0877974084544),
                triggerBin(60.0, 0.888888888889, 0.128174449784),
                triggerBin(70.0, 1.0, 0.115501778685),
                triggerBin(80.0, 0.909090909091, 0.179295209474),
                triggerBin(100.0, 1.0, 0.205567857429),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
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
        # Run2012A+B+C+D
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19296), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0298507462687, 0.00327466366006),
                triggerBin(25.0, 0.0433905146317, 0.00406658859772),
                triggerBin(29.0, 0.0899137358991, 0.00551706231864),
                triggerBin(33.0, 0.4, 0.00941154256627),
                triggerBin(37.0, 0.78747714808, 0.00910762902684),
                triggerBin(41.0, 0.843793584379, 0.0101826695001),
                triggerBin(45.0, 0.822799097065, 0.013768112498),
                triggerBin(50.0, 0.85, 0.0194923139367),
                triggerBin(55.0, 0.816143497758, 0.0296750910554),
                triggerBin(60.0, 0.833333333333, 0.0272294675165),
                triggerBin(70.0, 0.821782178218, 0.0464539610827),
                triggerBin(80.0, 0.811594202899, 0.0591701336487),
                triggerBin(100.0, 0.857142857143, 0.0850949832061),
            ),
        ),
        # Run2012A+B+C
        runs_190456_202585 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(202585),
            luminosity = cms.double(11736), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.03125, 0.00557681828814),
                triggerBin(25.0, 0.0319240724763, 0.00604049212332),
                triggerBin(29.0, 0.077057793345, 0.00872201935563),
                triggerBin(33.0, 0.3815915628, 0.0156307044292),
                triggerBin(37.0, 0.750283768445, 0.0154384370959),
                triggerBin(41.0, 0.824253075571, 0.0174262846041),
                triggerBin(45.0, 0.798270893372, 0.0238748558915),
                triggerBin(50.0, 0.83908045977, 0.0328198640903),
                triggerBin(55.0, 0.780821917808, 0.0592886752617),
                triggerBin(60.0, 0.76, 0.0503802396961),
                triggerBin(70.0, 0.790697674419, 0.0807924269882),
                triggerBin(80.0, 0.821428571429, 0.102762023591),
                triggerBin(100.0, 0.875, 0.141688278764),
            ),
        ),
        # Run2012A+B
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5126), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0297790585975, 0.00625097471723),
                triggerBin(25.0, 0.0315904139434, 0.00688665414707),
                triggerBin(29.0, 0.0899122807018, 0.0104971745993),
                triggerBin(33.0, 0.41155234657, 0.0177722829968),
                triggerBin(37.0, 0.809455587393, 0.0160384113817),
                triggerBin(41.0, 0.857142857143, 0.0189891236775),
                triggerBin(45.0, 0.809338521401, 0.0277092756268),
                triggerBin(50.0, 0.861313868613, 0.0360683123585),
                triggerBin(55.0, 0.848484848485, 0.0575785928796),
                triggerBin(60.0, 0.821428571429, 0.0518678580231),
                triggerBin(70.0, 0.78125, 0.0978124398978),
                triggerBin(80.0, 0.9, 0.116971358051),
                triggerBin(100.0, 0.916666666667, 0.166519597077),
            ),
        ),
        # Run2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(697.308), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0131578947368, 0.0170904558787),
                triggerBin(25.0, 0.016393442623, 0.0212125133111),
                triggerBin(29.0, 0.117647058824, 0.0344372890982),
                triggerBin(33.0, 0.428571428571, 0.0499948122083),
                triggerBin(37.0, 0.773109243697, 0.0449744631853),
                triggerBin(41.0, 0.829787234043, 0.0731720068018),
                triggerBin(45.0, 0.666666666667, 0.0963989814963),
                triggerBin(50.0, 0.85, 0.12471137336),
                triggerBin(55.0, 0.888888888889, 0.211557930346),
                triggerBin(60.0, 0.818181818182, 0.1914016948),
                triggerBin(70.0, 0.5, 0.314698893873),
                triggerBin(80.0, 1.0, 0.458641675296),
                triggerBin(100.0, 0.0, 0.841344746068),
            ),
        ),
        # Run2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4430), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0326209223847, 0.00710669061046),
                triggerBin(25.0, 0.0339195979899, 0.00769948887783),
                triggerBin(29.0, 0.0850515463918, 0.0112292340389),
                triggerBin(33.0, 0.408707865169, 0.0192449073231),
                triggerBin(37.0, 0.816925734024, 0.0175023655728),
                triggerBin(41.0, 0.860526315789, 0.0200949702756),
                triggerBin(45.0, 0.83257918552, 0.0289748752395),
                triggerBin(50.0, 0.863247863248, 0.0394651025737),
                triggerBin(55.0, 0.842105263158, 0.0637264282034),
                triggerBin(60.0, 0.821917808219, 0.0563995455401),
                triggerBin(70.0, 0.821428571429, 0.102762023591),
                triggerBin(80.0, 0.882352941176, 0.134601457887),
                triggerBin(100.0, 1.0, 0.154109706156),
            ),
        ),
        # Run2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(6892), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0369003690037, 0.0153296554325),
                triggerBin(25.0, 0.0373443983402, 0.0165898716156),
                triggerBin(29.0, 0.0695652173913, 0.0210791423028),
                triggerBin(33.0, 0.344339622642, 0.0356942286751),
                triggerBin(37.0, 0.770491803279, 0.0353430479337),
                triggerBin(41.0, 0.880281690141, 0.0337377253056),
                triggerBin(45.0, 0.888888888889, 0.043620757271),
                triggerBin(50.0, 0.837837837838, 0.0842807841643),
                triggerBin(55.0, 0.857142857143, 0.257123832984),
                triggerBin(60.0, 0.625, 0.156048626467),
                triggerBin(70.0, 0.818181818182, 0.1914016948),
                triggerBin(80.0, 0.75, 0.239566802733),
                triggerBin(100.0, 0.75, 0.368402425504),
            ),
        ),
        # Run2012D
        runs_202807_208686 = cms.PSet(
            firstRun = cms.uint32(202807),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7274), # 1/pb
            bins = cms.VPSet(
                triggerBin(20.0, 0.0337268128162, 0.00609533781077),
                triggerBin(25.0, 0.0417052826691, 0.00701284369062),
                triggerBin(29.0, 0.0960144927536, 0.00970465900477),
                triggerBin(33.0, 0.414587332054, 0.0158184836808),
                triggerBin(37.0, 0.810635538262, 0.0151736703235),
                triggerBin(41.0, 0.848722986248, 0.0175833660209),
                triggerBin(45.0, 0.831804281346, 0.0232811941134),
                triggerBin(50.0, 0.850340136054, 0.0354106621131),
                triggerBin(55.0, 0.842105263158, 0.053358948161),
                triggerBin(60.0, 0.89247311828, 0.0423330145355),
                triggerBin(70.0, 0.857142857143, 0.0850949832061),
                triggerBin(80.0, 0.807692307692, 0.109171931537),
                triggerBin(100.0, 0.9, 0.194135389638),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0416666666667, 0.0199072079734),
                triggerBin(25.0, 0.0295358649789, 0.0155465860392),
                triggerBin(29.0, 0.0865384615385, 0.0241318675839),
                triggerBin(33.0, 0.509868421053, 0.0302977490853),
                triggerBin(37.0, 0.886255924171, 0.026237053517),
                triggerBin(41.0, 0.915151515152, 0.0275893900003),
                triggerBin(45.0, 0.858585858586, 0.0440781851327),
                triggerBin(50.0, 0.911764705882, 0.0784415663023),
                triggerBin(55.0, 0.869565217391, 0.11081369682),
                triggerBin(60.0, 0.833333333333, 0.135998901491),
                triggerBin(70.0, 0.857142857143, 0.257123832984),
                triggerBin(80.0, 1.0, 0.308024223477),
                triggerBin(100.0, 0.9, 0.194135389638),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0441176470588, 0.0162517043448),
                triggerBin(25.0, 0.0353260869565, 0.0124571515126),
                triggerBin(29.0, 0.0764331210191, 0.0180860814288),
                triggerBin(33.0, 0.514412416851, 0.0246477998365),
                triggerBin(37.0, 0.88996763754, 0.0207893669048),
                triggerBin(41.0, 0.930735930736, 0.020992329012),
                triggerBin(45.0, 0.848920863309, 0.0366989293981),
                triggerBin(50.0, 0.88, 0.0647939679021),
                triggerBin(55.0, 0.9, 0.0877974084544),
                triggerBin(60.0, 0.833333333333, 0.0970335931041),
                triggerBin(70.0, 0.9, 0.194135389638),
                triggerBin(80.0, 1.0, 0.18499249774),
                triggerBin(100.0, 0.933333333333, 0.13708010169),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.05, 0.0166682485701),
                triggerBin(25.0, 0.0402010050251, 0.0124316960968),
                triggerBin(29.0, 0.0722891566265, 0.0171530381657),
                triggerBin(33.0, 0.523305084746, 0.0240736712428),
                triggerBin(37.0, 0.89751552795, 0.0197980305329),
                triggerBin(41.0, 0.928571428571, 0.0208356133221),
                triggerBin(45.0, 0.847133757962, 0.0342939361459),
                triggerBin(50.0, 0.897959183673, 0.06313660811),
                triggerBin(55.0, 0.9, 0.0877974084544),
                triggerBin(60.0, 0.857142857143, 0.0850949832061),
                triggerBin(70.0, 0.833333333333, 0.179009937646),
                triggerBin(80.0, 0.923076923077, 0.155415375679),
                triggerBin(100.0, 0.9375, 0.129429134796),
            ),
        ),
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0715705765408, 0.0134193895344),
                triggerBin(25.0, 0.0648967551622, 0.0108957303123),
                triggerBin(29.0, 0.0629183400268, 0.0101881363806),
                triggerBin(33.0, 0.535490605428, 0.0166647320717),
                triggerBin(37.0, 0.876273653566, 0.0138668411598),
                triggerBin(41.0, 0.930288461538, 0.014830181176),
                triggerBin(45.0, 0.869822485207, 0.0209528635407),
                triggerBin(50.0, 0.884297520661, 0.0367748729899),
                triggerBin(55.0, 0.905660377358, 0.0587823296232),
                triggerBin(60.0, 0.611111111111, 0.145378985762),
                triggerBin(70.0, 0.971428571429, 0.0626552130481),
                triggerBin(80.0, 0.975, 0.0551515705063),
                triggerBin(100.0, 1.0, 0.0923494906334),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0408163265306, 0.0169075502588),
                triggerBin(25.0, 0.0338983050847, 0.0125786564392),
                triggerBin(29.0, 0.0749063670412, 0.0197697265989),
                triggerBin(33.0, 0.518987341772, 0.0264207846138),
                triggerBin(37.0, 0.905303030303, 0.0216082320093),
                triggerBin(41.0, 0.928571428571, 0.02248197781),
                triggerBin(45.0, 0.829457364341, 0.0397338095199),
                triggerBin(50.0, 0.918918918919, 0.0726264763228),
                triggerBin(55.0, 0.888888888889, 0.0963981300751),
                triggerBin(60.0, 0.891891891892, 0.0772589573026),
                triggerBin(70.0, 0.875, 0.23225032014),
                triggerBin(80.0, 1.0, 0.205567857429),
                triggerBin(100.0, 1.0, 0.115501778685),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0374531835206, 0.0155529770872),
                triggerBin(25.0, 0.0317002881844, 0.0124442684863),
                triggerBin(29.0, 0.0764119601329, 0.01854129013),
                triggerBin(33.0, 0.509174311927, 0.0250803252879),
                triggerBin(37.0, 0.882943143813, 0.0216496486572),
                triggerBin(41.0, 0.929203539823, 0.0214336729972),
                triggerBin(45.0, 0.857142857143, 0.0382482675002),
                triggerBin(50.0, 0.9, 0.0619892518934),
                triggerBin(55.0, 0.9, 0.0877974084544),
                triggerBin(60.0, 0.814814814815, 0.105875016529),
                triggerBin(70.0, 0.888888888889, 0.211557930346),
                triggerBin(80.0, 0.857142857143, 0.257123832984),
                triggerBin(100.0, 0.866666666667, 0.14953714223),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0416666666667, 0.0199072079734),
                triggerBin(25.0, 0.0295358649789, 0.0155465860392),
                triggerBin(29.0, 0.0865384615385, 0.0241318675839),
                triggerBin(33.0, 0.509868421053, 0.0302977490853),
                triggerBin(37.0, 0.886255924171, 0.026237053517),
                triggerBin(41.0, 0.915151515152, 0.0275893900003),
                triggerBin(45.0, 0.858585858586, 0.0440781851327),
                triggerBin(50.0, 0.911764705882, 0.0784415663023),
                triggerBin(55.0, 0.869565217391, 0.11081369682),
                triggerBin(60.0, 0.833333333333, 0.135998901491),
                triggerBin(70.0, 0.857142857143, 0.257123832984),
                triggerBin(80.0, 1.0, 0.308024223477),
                triggerBin(100.0, 0.9, 0.194135389638),
            ),
        ),
        Summer12_PU_2012Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0326086956522, 0.0145376677),
                triggerBin(25.0, 0.0494791666667, 0.0137009677138),
                triggerBin(29.0, 0.0576036866359, 0.0134737942085),
                triggerBin(33.0, 0.473568281938, 0.0245673340105),
                triggerBin(37.0, 0.832891246684, 0.0214672570348),
                triggerBin(41.0, 0.885462555066, 0.0251977518915),
                triggerBin(45.0, 0.854166666667, 0.0355612697361),
                triggerBin(50.0, 0.867647058824, 0.0545661227401),
                triggerBin(55.0, 0.878787878788, 0.0855133855999),
                triggerBin(60.0, 0.863636363636, 0.11509911457),
                triggerBin(70.0, 0.9375, 0.129429134796),
                triggerBin(80.0, 0.846153846154, 0.16803608658),
                triggerBin(100.0, 0.818181818182, 0.1914016948),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)
