# Generated on Mon Oct  7 16:18:42 2013
# by HiggsAnalysis/TriggerEfficiency/test/PythonWriter.py

import FWCore.ParameterSet.Config as cms

def triggerBin(pt, efficiency, uncertaintyPlus, uncertaintyMinus):
    return cms.PSet(
        pt = cms.double(pt),
        efficiency = cms.double(efficiency),
        uncertaintyPlus = cms.double(uncertaintyPlus),
        uncertaintyMinus = cms.double(uncertaintyMinus)
    )


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

    # Used input: multicrab_MetLeg2012_130517_110812

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.05, 0.048733971724),
                triggerBin(20.0, 0.0833333333333, 0.166519597077, 0.0690403141434),
                triggerBin(30.0, 0.0, 0.231260479746, 0.0),
                triggerBin(40.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(50.0, 0.5, 0.41724846474, 0.41724846474),
                triggerBin(60.0, 0.0, 0.841344746068, 0.0),
                triggerBin(70.0, 1.0, 0.0, 0.601684479424),
                triggerBin(80.0, 0.0, 1.0, 0.0),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.025641025641, 0.0113190475827),
                triggerBin(20.0, 0.0300751879699, 0.0231409974237, 0.0143389657932),
                triggerBin(30.0, 0.0752688172043, 0.0381876650234, 0.0273417817938),
                triggerBin(40.0, 0.162790697674, 0.0766334033584, 0.058017338737),
                triggerBin(50.0, 0.194444444444, 0.0889424939268, 0.068790877801),
                triggerBin(60.0, 0.363636363636, 0.195231028387, 0.164761960702),
                triggerBin(70.0, 0.0, 0.841344746068, 0.0),
                triggerBin(80.0, 0.75, 0.207730893696, 0.368402425504),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.028, 0.0104337912573),
                triggerBin(20.0, 0.0412371134021, 0.0197085261874, 0.0141451834179),
                triggerBin(30.0, 0.0833333333333, 0.0334310228604, 0.025385131148),
                triggerBin(40.0, 0.0506329113924, 0.0382257148326, 0.0240761892777),
                triggerBin(50.0, 0.166666666667, 0.0862612860187, 0.0640469271296),
                triggerBin(60.0, 0.333333333333, 0.145567823704, 0.123318223606),
                triggerBin(70.0, 0.5, 0.176478356266, 0.176478356266),
                triggerBin(80.0, 0.25, 0.368402425504, 0.207730893696),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.75, 0.207730893696, 0.368402425504),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.025641025641, 0.00956634122401),
                triggerBin(20.0, 0.041095890411, 0.01820490664, 0.0133158433994),
                triggerBin(30.0, 0.0700636942675, 0.0267414944195, 0.0204350521541),
                triggerBin(40.0, 0.10989010989, 0.0431829785367, 0.0332466549201),
                triggerBin(50.0, 0.117647058824, 0.0636560481649, 0.0456587756637),
                triggerBin(60.0, 0.25, 0.133747879731, 0.103407053241),
                triggerBin(70.0, 0.142857142857, 0.257123832984, 0.118480071045),
                triggerBin(80.0, 0.428571428571, 0.247840988275, 0.222487613116),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.458641675296),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0, 0.458641675296),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0279069767442, 0.0112328789395),
                triggerBin(20.0, 0.0344827586207, 0.0226536450207, 0.014815011728),
                triggerBin(30.0, 0.07, 0.0356680906999, 0.025455689305),
                triggerBin(40.0, 0.173913043478, 0.0745206943475, 0.0578399488833),
                triggerBin(50.0, 0.210526315789, 0.0873003831507, 0.0693657511201),
                triggerBin(60.0, 0.333333333333, 0.185994488221, 0.151856070435),
                triggerBin(70.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(80.0, 0.75, 0.207730893696, 0.368402425504),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.5, 0.314698893873, 0.314698893873),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0279569892473, 0.00764471790369),
                triggerBin(20.0, 0.0383480825959, 0.0134940973628, 0.0103909602007),
                triggerBin(30.0, 0.0772727272727, 0.0224483946638, 0.0181326003294),
                triggerBin(40.0, 0.096, 0.0340404621712, 0.0266345527184),
                triggerBin(50.0, 0.189189189189, 0.0567879423569, 0.0472277746216),
                triggerBin(60.0, 0.333333333333, 0.107317780779, 0.0943571124254),
                triggerBin(70.0, 0.533333333333, 0.152935340154, 0.158270494867),
                triggerBin(80.0, 0.5, 0.220457375638, 0.220457375638),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.6, 0.25334762525, 0.303366136254),
                triggerBin(140.0, 0.75, 0.207730893696, 0.368402425504),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0271002710027, 0.0059771296637),
                triggerBin(20.0, 0.0394265232975, 0.0100667987371, 0.00823822711329),
                triggerBin(30.0, 0.0742705570292, 0.0160784942603, 0.0136020483313),
                triggerBin(40.0, 0.101851851852, 0.0249340403831, 0.0208446594972),
                triggerBin(50.0, 0.16, 0.0397352655668, 0.0336632266047),
                triggerBin(60.0, 0.3, 0.078587256674, 0.0694765089311),
                triggerBin(70.0, 0.409090909091, 0.129031169349, 0.119289306437),
                triggerBin(80.0, 0.466666666667, 0.158270494867, 0.152935340154),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.75, 0.159659347816, 0.239566802733),
                triggerBin(140.0, 0.75, 0.207730893696, 0.368402425504),
                triggerBin(160.0, 1.0, 0.0, 0.308024223477),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0763643502159, 0.00372105597962),
                triggerBin(20.0, 0.0871811777813, 0.00228199191187, 0.00228199191187),
                triggerBin(30.0, 0.128852160034, 0.00292659993415, 0.00292659993415),
                triggerBin(40.0, 0.166187784757, 0.0036042438794, 0.0036042438794),
                triggerBin(50.0, 0.216044059208, 0.00451545145919, 0.00451545145919),
                triggerBin(60.0, 0.276622485146, 0.00541167668266, 0.00541167668266),
                triggerBin(70.0, 0.343917270749, 0.00622306624347, 0.00622306624347),
                triggerBin(80.0, 0.523704078309, 0.00506105174214, 0.00506105174214),
                triggerBin(100.0, 0.763320294094, 0.00482839535826, 0.00482839535826),
                triggerBin(120.0, 0.914563367817, 0.00365415910822, 0.00365415910822),
                triggerBin(140.0, 0.976861627289, 0.00235510222917, 0.00235510222917),
                triggerBin(160.0, 0.996597115763, 0.00114953094049, 0.00114953094049),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0763643502159, 0.00372105597962),
                triggerBin(20.0, 0.0884329899925, 0.00248910008655, 0.00248910008655),
                triggerBin(30.0, 0.127806097787, 0.00315301449667, 0.00315301449667),
                triggerBin(40.0, 0.167537065805, 0.00391268290649, 0.00391268290649),
                triggerBin(50.0, 0.2323863913, 0.00506624379368, 0.00506624379368),
                triggerBin(60.0, 0.285262620851, 0.00589109634647, 0.00589109634647),
                triggerBin(70.0, 0.357367342962, 0.00685537541067, 0.00685537541067),
                triggerBin(80.0, 0.529192029783, 0.00557987422492, 0.00557987422492),
                triggerBin(100.0, 0.76024187311, 0.00535697785939, 0.00535697785939),
                triggerBin(120.0, 0.910446088065, 0.00407182948278, 0.00407182948278),
                triggerBin(140.0, 0.973239645224, 0.00275543959499, 0.00275543959499),
                triggerBin(160.0, 0.991454709917, 0.00198655992467, 0.00198655992467),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0763643502159, 0.00372105597962),
                triggerBin(20.0, 0.0883463430767, 0.00256339756501, 0.00256339756501),
                triggerBin(30.0, 0.128061005398, 0.00324740496897, 0.00324740496897),
                triggerBin(40.0, 0.168302716728, 0.00403082952159, 0.00403082952159),
                triggerBin(50.0, 0.226208814316, 0.0051423624608, 0.0051423624608),
                triggerBin(60.0, 0.285368889302, 0.00607545735851, 0.00607545735851),
                triggerBin(70.0, 0.355100922375, 0.00702549385374, 0.00702549385374),
                triggerBin(80.0, 0.530311356729, 0.00570108099484, 0.00570108099484),
                triggerBin(100.0, 0.762283533531, 0.00547232835371, 0.00547232835371),
                triggerBin(120.0, 0.911285028647, 0.00416315041669, 0.00416315041669),
                triggerBin(140.0, 0.973810571676, 0.00280337036779, 0.00280337036779),
                triggerBin(160.0, 0.992982456987, 0.0018552695148, 0.0018552695148),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0763643502159, 0.00372105597962),
                triggerBin(20.0, 0.0899556264169, 0.00289105907104, 0.00289105907104),
                triggerBin(30.0, 0.128531888194, 0.00363187271699, 0.00363187271699),
                triggerBin(40.0, 0.169903014162, 0.00450649575779, 0.00450649575779),
                triggerBin(50.0, 0.22273041632, 0.00569551344999, 0.00569551344999),
                triggerBin(60.0, 0.287534100781, 0.0068019987759, 0.0068019987759),
                triggerBin(70.0, 0.356154835876, 0.00783760098781, 0.00783760098781),
                triggerBin(80.0, 0.5314788127, 0.00633032851605, 0.00633032851605),
                triggerBin(100.0, 0.76385277221, 0.00608890536708, 0.00608890536708),
                triggerBin(120.0, 0.90918953019, 0.00470240474619, 0.00470240474619),
                triggerBin(140.0, 0.97408787779, 0.00312482987571, 0.00312482987571),
                triggerBin(160.0, 0.994532044733, 0.00181841193657, 0.00181841193657),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0763643502159, 0.00372105597962),
                triggerBin(20.0, 0.0882376283282, 0.00245761173161, 0.00245761173161),
                triggerBin(30.0, 0.127968760616, 0.00311911345242, 0.00311911345242),
                triggerBin(40.0, 0.167327074204, 0.00386604377198, 0.00386604377198),
                triggerBin(50.0, 0.229797932098, 0.00498072545268, 0.00498072545268),
                triggerBin(60.0, 0.283925108785, 0.00581859403924, 0.00581859403924),
                triggerBin(70.0, 0.355241061915, 0.00675840958867, 0.00675840958867),
                triggerBin(80.0, 0.528309003559, 0.00549986450823, 0.00549986450823),
                triggerBin(100.0, 0.760736924406, 0.00527481125702, 0.00527481125702),
                triggerBin(120.0, 0.911095949493, 0.00400703607456, 0.00400703607456),
                triggerBin(140.0, 0.973810591698, 0.00269246639979, 0.00269246639979),
                triggerBin(160.0, 0.992269351712, 0.00186563433123, 0.00186563433123),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0763643502159, 0.00372105597962),
                triggerBin(20.0, 0.0882977382138, 0.00251662480434, 0.00251662480434),
                triggerBin(30.0, 0.128019801804, 0.00319076786111, 0.00319076786111),
                triggerBin(40.0, 0.167867514024, 0.00395800711302, 0.00395800711302),
                triggerBin(50.0, 0.227805911303, 0.0050716246767, 0.0050716246767),
                triggerBin(60.0, 0.284723099841, 0.00596179607635, 0.00596179607635),
                triggerBin(70.0, 0.355163406871, 0.00690773894139, 0.00690773894139),
                triggerBin(80.0, 0.529421228992, 0.00561258588045, 0.00561258588045),
                triggerBin(100.0, 0.76159441942, 0.00538540944884, 0.00538540944884),
                triggerBin(120.0, 0.911200733869, 0.00409435608158, 0.00409435608158),
                triggerBin(140.0, 0.973810470031, 0.00275441560353, 0.00275441560353),
                triggerBin(160.0, 0.992663290248, 0.00186180738605, 0.00186180738605),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0763643502159, 0.00372105597962),
                triggerBin(20.0, 0.0899556264169, 0.00289105907104, 0.00289105907104),
                triggerBin(30.0, 0.128531888194, 0.00363187271699, 0.00363187271699),
                triggerBin(40.0, 0.169903014162, 0.00450649575779, 0.00450649575779),
                triggerBin(50.0, 0.22273041632, 0.00569551344999, 0.00569551344999),
                triggerBin(60.0, 0.287534100781, 0.0068019987759, 0.0068019987759),
                triggerBin(70.0, 0.356154835876, 0.00783760098781, 0.00783760098781),
                triggerBin(80.0, 0.5314788127, 0.00633032851605, 0.00633032851605),
                triggerBin(100.0, 0.76385277221, 0.00608890536708, 0.00608890536708),
                triggerBin(120.0, 0.90918953019, 0.00470240474619, 0.00470240474619),
                triggerBin(140.0, 0.97408787779, 0.00312482987571, 0.00312482987571),
                triggerBin(160.0, 0.994532044733, 0.00181841193657, 0.00181841193657),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0763643502159, 0.00372105597962),
                triggerBin(20.0, 0.0976163450624, 0.00467906571331, 0.00449175660999),
                triggerBin(30.0, 0.132600919775, 0.00564454057002, 0.00545240782411),
                triggerBin(40.0, 0.180893682589, 0.00701135308269, 0.00681022853207),
                triggerBin(50.0, 0.227564102564, 0.00870266916269, 0.00847921326292),
                triggerBin(60.0, 0.308406647116, 0.0105481106039, 0.01035639884),
                triggerBin(70.0, 0.380141010576, 0.0121287130172, 0.0119844034236),
                triggerBin(80.0, 0.545869947276, 0.00949218472115, 0.00952503079985),
                triggerBin(100.0, 0.766698024459, 0.00927740244409, 0.0095346551812),
                triggerBin(120.0, 0.894138755981, 0.0075781198477, 0.0080681546908),
                triggerBin(140.0, 0.965034965035, 0.0054362554544, 0.00631433348166),
                triggerBin(160.0, 0.994764397906, 0.00250404257321, 0.00412033031579),
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

    # Used input: multicrab_MetLeg2012_130517_110812

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.111111111111, 0.104756560176),
                triggerBin(20.0, 0.125, 0.23225032014, 0.103637263595),
                triggerBin(30.0, 0.0, 0.36887757085, 0.0),
                triggerBin(40.0, 0.5, 0.41724846474, 0.41724846474),
                triggerBin(50.0, 0.5, 0.41724846474, 0.41724846474),
                triggerBin(60.0, 0.0, 1.0, 0.0),
                triggerBin(70.0, 1.0, 0.0, 0.601684479424),
                triggerBin(80.0, 0.0, 1.0, 0.0),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0336134453782, 0.0165218423464),
                triggerBin(20.0, 0.0348837209302, 0.0327700967741, 0.0189255996623),
                triggerBin(30.0, 0.125, 0.0608241577898, 0.0449271328006),
                triggerBin(40.0, 0.136363636364, 0.11509911457, 0.0732667013517),
                triggerBin(50.0, 0.166666666667, 0.135998901491, 0.0892717907981),
                triggerBin(60.0, 0.25, 0.239566802733, 0.159659347816),
                triggerBin(70.0, 0.0, 0.841344746068, 0.0),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0281690140845, 0.0138847166789),
                triggerBin(20.0, 0.051724137931, 0.0296167889077, 0.0203272293421),
                triggerBin(30.0, 0.0757575757576, 0.0480000082871, 0.032332845254),
                triggerBin(40.0, 0.0681818181818, 0.0619005708815, 0.0368770250397),
                triggerBin(50.0, 0.173913043478, 0.116302557627, 0.081292990613),
                triggerBin(60.0, 0.333333333333, 0.185994488221, 0.151856070435),
                triggerBin(70.0, 0.5, 0.195182116991, 0.195182116991),
                triggerBin(80.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 1.0, 0.0, 0.458641675296),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0225988700565, 0.0111710281883),
                triggerBin(20.0, 0.03125, 0.0240190532641, 0.0148968388901),
                triggerBin(30.0, 0.0348837209302, 0.0327700967741, 0.0189255996623),
                triggerBin(40.0, 0.127659574468, 0.0684613972074, 0.0494467249774),
                triggerBin(50.0, 0.2, 0.112667857843, 0.0835234580544),
                triggerBin(60.0, 0.272727272727, 0.196072358725, 0.144395891738),
                triggerBin(70.0, 0.0, 0.36887757085, 0.0),
                triggerBin(80.0, 0.25, 0.368402425504, 0.207730893696),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.458641675296),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0390625, 0.0171246854656),
                triggerBin(20.0, 0.0425531914894, 0.0323678650094, 0.0202555238052),
                triggerBin(30.0, 0.116666666667, 0.0571758165749, 0.0420083072563),
                triggerBin(40.0, 0.166666666667, 0.112297423319, 0.077988895091),
                triggerBin(50.0, 0.2, 0.130118869123, 0.0931224604655),
                triggerBin(60.0, 0.25, 0.239566802733, 0.159659347816),
                triggerBin(70.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.5, 0.314698893873, 0.314698893873),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0333333333333, 0.0109243564472),
                triggerBin(20.0, 0.047619047619, 0.0196262351462, 0.0146356034049),
                triggerBin(30.0, 0.0952380952381, 0.0337896798256, 0.0264287787198),
                triggerBin(40.0, 0.102941176471, 0.0510395044133, 0.0371760537044),
                triggerBin(50.0, 0.186046511628, 0.0788697532887, 0.0616866743041),
                triggerBin(60.0, 0.3, 0.135910953525, 0.111901660362),
                triggerBin(70.0, 0.538461538462, 0.164847322399, 0.172004084463),
                triggerBin(80.0, 0.6, 0.25334762525, 0.303366136254),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.6, 0.25334762525, 0.303366136254),
                triggerBin(140.0, 1.0, 0.0, 0.458641675296),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0290827740492, 0.00794795237694),
                triggerBin(20.0, 0.0414201183432, 0.0138912736932, 0.010812974964),
                triggerBin(30.0, 0.0707547169811, 0.0222805405079, 0.0177024361083),
                triggerBin(40.0, 0.113043478261, 0.0376688495896, 0.0299925163015),
                triggerBin(50.0, 0.191176470588, 0.0599041554082, 0.0495236647292),
                triggerBin(60.0, 0.290322580645, 0.103897013206, 0.0880517504109),
                triggerBin(70.0, 0.411764705882, 0.149770451815, 0.137360513174),
                triggerBin(80.0, 0.444444444444, 0.213462824948, 0.198267144951),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.75, 0.159659347816, 0.239566802733),
                triggerBin(140.0, 1.0, 0.0, 0.458641675296),
                triggerBin(160.0, 1.0, 0.0, 0.36887757085),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0721966205837, 0.00453639552401),
                triggerBin(20.0, 0.0870130647037, 0.00285656808514, 0.00285656808514),
                triggerBin(30.0, 0.121473594365, 0.00354596374012, 0.00354596374012),
                triggerBin(40.0, 0.16332660628, 0.00433172887266, 0.00433172887266),
                triggerBin(50.0, 0.223233878408, 0.00547111437865, 0.00547111437865),
                triggerBin(60.0, 0.277066075262, 0.00639719366282, 0.00639719366282),
                triggerBin(70.0, 0.338942977902, 0.00723369959291, 0.00723369959291),
                triggerBin(80.0, 0.537963584846, 0.00587336629882, 0.00587336629882),
                triggerBin(100.0, 0.769737193367, 0.00544372854461, 0.00544372854461),
                triggerBin(120.0, 0.914356335564, 0.00414289076173, 0.00414289076173),
                triggerBin(140.0, 0.973581787865, 0.00285188994591, 0.00285188994591),
                triggerBin(160.0, 0.995838899537, 0.001405127284, 0.001405127284),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0721966205837, 0.00453639552401),
                triggerBin(20.0, 0.089394795199, 0.00311838240374, 0.00311838240374),
                triggerBin(30.0, 0.11749590876, 0.00377094722572, 0.00377094722572),
                triggerBin(40.0, 0.164123086101, 0.00470847090037, 0.00470847090037),
                triggerBin(50.0, 0.23921619646, 0.00609214421435, 0.00609214421435),
                triggerBin(60.0, 0.283449651882, 0.00688372845661, 0.00688372845661),
                triggerBin(70.0, 0.356288856327, 0.00797017005238, 0.00797017005238),
                triggerBin(80.0, 0.542362983648, 0.00647648374517, 0.00647648374517),
                triggerBin(100.0, 0.7629548595, 0.00608950021517, 0.00608950021517),
                triggerBin(120.0, 0.906866606183, 0.00471635175422, 0.00471635175422),
                triggerBin(140.0, 0.969138794222, 0.00334515622539, 0.00334515622539),
                triggerBin(160.0, 0.989404086227, 0.00246074496271, 0.00246074496271),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0721966205837, 0.00453639552401),
                triggerBin(20.0, 0.0887460457791, 0.00321127235048, 0.00321127235048),
                triggerBin(30.0, 0.119149138038, 0.0039058840737, 0.0039058840737),
                triggerBin(40.0, 0.164993695752, 0.00484344052482, 0.00484344052482),
                triggerBin(50.0, 0.232364345669, 0.00619655628919, 0.00619655628919),
                triggerBin(60.0, 0.283886300494, 0.0071309373953, 0.0071309373953),
                triggerBin(70.0, 0.352888881063, 0.00818245876936, 0.00818245876936),
                triggerBin(80.0, 0.544123366249, 0.00661207663634, 0.00661207663634),
                triggerBin(100.0, 0.765847948321, 0.00620705248122, 0.00620705248122),
                triggerBin(120.0, 0.90916402733, 0.00477750557001, 0.00477750557001),
                triggerBin(140.0, 0.970070047774, 0.00339214442553, 0.00339214442553),
                triggerBin(160.0, 0.991316475343, 0.00229379698355, 0.00229379698355),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0721966205837, 0.00453639552401),
                triggerBin(20.0, 0.0901927679375, 0.00362680675094, 0.00362680675094),
                triggerBin(30.0, 0.120982378008, 0.00438658524522, 0.00438658524522),
                triggerBin(40.0, 0.165663431933, 0.00539428204231, 0.00539428204231),
                triggerBin(50.0, 0.226983038016, 0.00684509111751, 0.00684509111751),
                triggerBin(60.0, 0.285967129138, 0.00799190666252, 0.00799190666252),
                triggerBin(70.0, 0.351273537832, 0.00911320299781, 0.00911320299781),
                triggerBin(80.0, 0.544564112208, 0.00732738947481, 0.00732738947481),
                triggerBin(100.0, 0.766990570289, 0.00689910061254, 0.00689910061254),
                triggerBin(120.0, 0.907717655348, 0.00536731668361, 0.00536731668361),
                triggerBin(140.0, 0.971190235526, 0.00373588061422, 0.00373588061422),
                triggerBin(160.0, 0.993226460004, 0.00225112979158, 0.00225112979158),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0721966205837, 0.00453639552401),
                triggerBin(20.0, 0.0890261397744, 0.00307862948498, 0.00307862948498),
                triggerBin(30.0, 0.11811209528, 0.00373804795136, 0.00373804795136),
                triggerBin(40.0, 0.163998588696, 0.00465139812423, 0.00465139812423),
                triggerBin(50.0, 0.236709344748, 0.00599658180968, 0.00599658180968),
                triggerBin(60.0, 0.282476682725, 0.00681113659525, 0.00681113659525),
                triggerBin(70.0, 0.353559151587, 0.00785759677876, 0.00785759677876),
                triggerBin(80.0, 0.541655359849, 0.00638344274107, 0.00638344274107),
                triggerBin(100.0, 0.764052228227, 0.00598826453941, 0.00598826453941),
                triggerBin(120.0, 0.908058728684, 0.00462613097243, 0.00462613097243),
                triggerBin(140.0, 0.969836545254, 0.00326784285181, 0.00326784285181),
                triggerBin(160.0, 0.990435356992, 0.0023060789534, 0.0023060789534),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0721966205837, 0.00453639552401),
                triggerBin(20.0, 0.0888715654862, 0.00315262673723, 0.00315262673723),
                triggerBin(30.0, 0.118686240469, 0.0038315970164, 0.0038315970164),
                triggerBin(40.0, 0.164550572123, 0.00475866691166, 0.00475866691166),
                triggerBin(50.0, 0.23430167486, 0.00610903007241, 0.00610903007241),
                triggerBin(60.0, 0.283254197233, 0.00698911198231, 0.00698911198231),
                triggerBin(70.0, 0.353188352456, 0.0080390231697, 0.0080390231697),
                triggerBin(80.0, 0.543026625399, 0.0065115938322, 0.0065115938322),
                triggerBin(100.0, 0.765048156251, 0.00611085334477, 0.00611085334477),
                triggerBin(120.0, 0.908671499914, 0.00471122043063, 0.00471122043063),
                triggerBin(140.0, 0.969965834753, 0.00333743131829, 0.00333743131829),
                triggerBin(160.0, 0.990922282653, 0.00230164086667, 0.00230164086667),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0721966205837, 0.00453639552401),
                triggerBin(20.0, 0.0901927679375, 0.00362680675094, 0.00362680675094),
                triggerBin(30.0, 0.120982378008, 0.00438658524522, 0.00438658524522),
                triggerBin(40.0, 0.165663431933, 0.00539428204231, 0.00539428204231),
                triggerBin(50.0, 0.226983038016, 0.00684509111751, 0.00684509111751),
                triggerBin(60.0, 0.285967129138, 0.00799190666252, 0.00799190666252),
                triggerBin(70.0, 0.351273537832, 0.00911320299781, 0.00911320299781),
                triggerBin(80.0, 0.544564112208, 0.00732738947481, 0.00732738947481),
                triggerBin(100.0, 0.766990570289, 0.00689910061254, 0.00689910061254),
                triggerBin(120.0, 0.907717655348, 0.00536731668361, 0.00536731668361),
                triggerBin(140.0, 0.971190235526, 0.00373588061422, 0.00373588061422),
                triggerBin(160.0, 0.993226460004, 0.00225112979158, 0.00225112979158),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0721966205837, 0.00453639552401),
                triggerBin(20.0, 0.0981023988543, 0.00595598821866, 0.00565910196985),
                triggerBin(30.0, 0.127725856698, 0.00693033433266, 0.00663189543857),
                triggerBin(40.0, 0.172568354998, 0.00837408008484, 0.00807240646212),
                triggerBin(50.0, 0.227091633466, 0.0104369719235, 0.0101175825408),
                triggerBin(60.0, 0.302263648469, 0.0123141002391, 0.012043515336),
                triggerBin(70.0, 0.368924302789, 0.0141206979222, 0.0139058071806),
                triggerBin(80.0, 0.552127162225, 0.0109583129479, 0.0110080980847),
                triggerBin(100.0, 0.764173703257, 0.0105607407406, 0.010888505801),
                triggerBin(120.0, 0.893893129771, 0.00857663776567, 0.00920470974313),
                triggerBin(140.0, 0.962585034014, 0.00639621940683, 0.00753759111279),
                triggerBin(160.0, 0.993421052632, 0.00314599800107, 0.0051712685747),
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

    # Used input: multicrab_MetLeg2012_130517_110812

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.142857142857, 0.132260014253),
                triggerBin(20.0, 0.142857142857, 0.257123832984, 0.118480071045),
                triggerBin(30.0, 0.0, 0.458641675296, 0.0),
                triggerBin(40.0, 0.5, 0.41724846474, 0.41724846474),
                triggerBin(50.0, 0.5, 0.41724846474, 0.41724846474),
                triggerBin(60.0, 0.0, 1.0, 0.0),
                triggerBin(70.0, 1.0, 0.0, 0.601684479424),
                triggerBin(80.0, 0.0, 1.0, 0.0),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0392156862745, 0.0192195305651),
                triggerBin(20.0, 0.038961038961, 0.0364493853816, 0.0211298096514),
                triggerBin(30.0, 0.117647058824, 0.0636560481649, 0.0456587756637),
                triggerBin(40.0, 0.166666666667, 0.135998901491, 0.0892717907981),
                triggerBin(50.0, 0.142857142857, 0.158270654649, 0.0917088958422),
                triggerBin(60.0, 0.25, 0.239566802733, 0.159659347816),
                triggerBin(70.0, 0.0, 0.841344746068, 0.0),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.0, 0.601684479424, 0.0),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0327868852459, 0.016122457965),
                triggerBin(20.0, 0.0594059405941, 0.0337974107057, 0.0233130483776),
                triggerBin(30.0, 0.0806451612903, 0.0508738752303, 0.0343911806251),
                triggerBin(40.0, 0.0789473684211, 0.0708737003562, 0.0426562617902),
                triggerBin(50.0, 0.210526315789, 0.135427055903, 0.0978662361907),
                triggerBin(60.0, 0.333333333333, 0.185994488221, 0.151856070435),
                triggerBin(70.0, 0.444444444444, 0.213462824948, 0.198267144951),
                triggerBin(80.0, 0.0, 0.601684479424, 0.0),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 1.0, 0.0, 0.601684479424),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.025974025974, 0.0128172408109),
                triggerBin(20.0, 0.0263157894737, 0.0249359369637, 0.0142883223082),
                triggerBin(30.0, 0.038961038961, 0.0364493853816, 0.0211298096514),
                triggerBin(40.0, 0.130434782609, 0.0697762494647, 0.0504937771347),
                triggerBin(50.0, 0.227272727273, 0.124519809699, 0.0944237146768),
                triggerBin(60.0, 0.3, 0.20826248199, 0.158328098893),
                triggerBin(70.0, 0.0, 0.36887757085, 0.0),
                triggerBin(80.0, 0.25, 0.368402425504, 0.207730893696),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.458641675296),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.045871559633, 0.0200383484757),
                triggerBin(20.0, 0.047619047619, 0.0360513607022, 0.0226519839091),
                triggerBin(30.0, 0.111111111111, 0.060467252805, 0.0431774157972),
                triggerBin(40.0, 0.2, 0.130118869123, 0.0931224604655),
                triggerBin(50.0, 0.1875, 0.149398565056, 0.100212028831),
                triggerBin(60.0, 0.25, 0.239566802733, 0.159659347816),
                triggerBin(70.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.038961038961, 0.0127315057964),
                triggerBin(20.0, 0.0540540540541, 0.0221717569697, 0.0165871352054),
                triggerBin(30.0, 0.0948275862069, 0.0355229928616, 0.0274768938321),
                triggerBin(40.0, 0.120689655172, 0.0589443821995, 0.0434188250899),
                triggerBin(50.0, 0.2, 0.0910146087326, 0.0706631844333),
                triggerBin(60.0, 0.3, 0.135910953525, 0.111901660362),
                triggerBin(70.0, 0.5, 0.176478356266, 0.176478356266),
                triggerBin(80.0, 0.5, 0.314698893873, 0.314698893873),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.5, 0.314698893873, 0.314698893873),
                triggerBin(140.0, 1.0, 0.0, 0.601684479424),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0337662337662, 0.00920559897717),
                triggerBin(20.0, 0.0434782608696, 0.0152440228034, 0.011764633588),
                triggerBin(30.0, 0.0725388601036, 0.0237975497686, 0.0187699741391),
                triggerBin(40.0, 0.125, 0.0412759820659, 0.0330480156249),
                triggerBin(50.0, 0.210526315789, 0.0681226444959, 0.0564551889986),
                triggerBin(60.0, 0.3, 0.106340064496, 0.090716398418),
                triggerBin(70.0, 0.375, 0.156048626467, 0.137247055387),
                triggerBin(80.0, 0.375, 0.234946487636, 0.196075614151),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.714285714286, 0.182129028008, 0.259937875571),
                triggerBin(140.0, 1.0, 0.0, 0.601684479424),
                triggerBin(160.0, 1.0, 0.0, 0.36887757085),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0691582256374, 0.00474186493714),
                triggerBin(20.0, 0.082409864081, 0.00298282790675, 0.00298282790675),
                triggerBin(30.0, 0.12083882578, 0.00377730633292, 0.00377730633292),
                triggerBin(40.0, 0.154158218475, 0.00444137175394, 0.00444137175394),
                triggerBin(50.0, 0.221011435788, 0.00574453479917, 0.00574453479917),
                triggerBin(60.0, 0.281086324981, 0.00669161308503, 0.00669161308503),
                triggerBin(70.0, 0.34147130097, 0.00758830398163, 0.00758830398163),
                triggerBin(80.0, 0.536075096901, 0.00609462696848, 0.00609462696848),
                triggerBin(100.0, 0.767623748914, 0.00574490911073, 0.00574490911073),
                triggerBin(120.0, 0.911522775937, 0.00437987242337, 0.00437987242337),
                triggerBin(140.0, 0.971994144684, 0.00305964371804, 0.00305964371804),
                triggerBin(160.0, 0.995783365055, 0.00148434334414, 0.00148434334414),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0691582256374, 0.00474186493714),
                triggerBin(20.0, 0.0841225488835, 0.0032535010159, 0.0032535010159),
                triggerBin(30.0, 0.119664968853, 0.00408123612114, 0.00408123612114),
                triggerBin(40.0, 0.155169594727, 0.0048577372528, 0.0048577372528),
                triggerBin(50.0, 0.237645151042, 0.00640313604653, 0.00640313604653),
                triggerBin(60.0, 0.283586019176, 0.00718081806944, 0.00718081806944),
                triggerBin(70.0, 0.357220638786, 0.00833383079917, 0.00833383079917),
                triggerBin(80.0, 0.541011594213, 0.00672539177225, 0.00672539177225),
                triggerBin(100.0, 0.763829290199, 0.00643068522916, 0.00643068522916),
                triggerBin(120.0, 0.907638820905, 0.00488958412153, 0.00488958412153),
                triggerBin(140.0, 0.966650555532, 0.00364827905709, 0.00364827905709),
                triggerBin(160.0, 0.989195524172, 0.00259496749859, 0.00259496749859),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0691582256374, 0.00474186493714),
                triggerBin(20.0, 0.0838647673732, 0.00335150778945, 0.00335150778945),
                triggerBin(30.0, 0.120500510435, 0.0042055368834, 0.0042055368834),
                triggerBin(40.0, 0.156345224826, 0.00499477253101, 0.00499477253101),
                triggerBin(50.0, 0.230978967621, 0.00651951050553, 0.00651951050553),
                triggerBin(60.0, 0.285613302439, 0.00744896584162, 0.00744896584162),
                triggerBin(70.0, 0.353757275256, 0.0085580576524, 0.0085580576524),
                triggerBin(80.0, 0.542376753402, 0.00686438180822, 0.00686438180822),
                triggerBin(100.0, 0.766171695787, 0.00655063375701, 0.00655063375701),
                triggerBin(120.0, 0.908715534614, 0.00498439177134, 0.00498439177134),
                triggerBin(140.0, 0.967998435679, 0.0036710885465, 0.0036710885465),
                triggerBin(160.0, 0.991301660494, 0.00240313469173, 0.00240313469173),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0691582256374, 0.00474186493714),
                triggerBin(20.0, 0.0860120637857, 0.0037966553385, 0.0037966553385),
                triggerBin(30.0, 0.121907430973, 0.00470566063354, 0.00470566063354),
                triggerBin(40.0, 0.15780653497, 0.00556955212978, 0.00556955212978),
                triggerBin(50.0, 0.225478230755, 0.0072080533046, 0.0072080533046),
                triggerBin(60.0, 0.288857344986, 0.00836292522532, 0.00836292522532),
                triggerBin(70.0, 0.350937069288, 0.00953195853217, 0.00953195853217),
                triggerBin(80.0, 0.542142995123, 0.00761607663038, 0.00761607663038),
                triggerBin(100.0, 0.766739106673, 0.00727722166674, 0.00727722166674),
                triggerBin(120.0, 0.905405368383, 0.005660094712, 0.005660094712),
                triggerBin(140.0, 0.969429945489, 0.0040231022137, 0.0040231022137),
                triggerBin(160.0, 0.99366070065, 0.00227847640118, 0.00227847640118),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0691582256374, 0.00474186493714),
                triggerBin(20.0, 0.0838565282201, 0.00321238976703, 0.00321238976703),
                triggerBin(30.0, 0.119848606779, 0.00403556634888, 0.00403556634888),
                triggerBin(40.0, 0.155010026376, 0.00479416074552, 0.00479416074552),
                triggerBin(50.0, 0.235037450592, 0.00630180467136, 0.00630180467136),
                triggerBin(60.0, 0.283204018511, 0.00710793894114, 0.00710793894114),
                triggerBin(70.0, 0.354750576414, 0.00822019464076, 0.00822019464076),
                triggerBin(80.0, 0.540216472412, 0.00662800219802, 0.00662800219802),
                triggerBin(100.0, 0.764449270833, 0.00632288176208, 0.00632288176208),
                triggerBin(120.0, 0.908255198369, 0.00481021391534, 0.00481021391534),
                triggerBin(140.0, 0.967500311537, 0.00355490634646, 0.00355490634646),
                triggerBin(160.0, 0.990243065392, 0.00243425598035, 0.00243425598035),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0691582256374, 0.00474186493714),
                triggerBin(20.0, 0.0838610858187, 0.00328998389855, 0.00328998389855),
                triggerBin(30.0, 0.120209979227, 0.00413045516098, 0.00413045516098),
                triggerBin(40.0, 0.155750998729, 0.00490619557519, 0.00490619557519),
                triggerBin(50.0, 0.232790127331, 0.0064240979556, 0.0064240979556),
                triggerBin(60.0, 0.284533054546, 0.00729763703382, 0.00729763703382),
                triggerBin(70.0, 0.354201010102, 0.0084089133964, 0.0084089133964),
                triggerBin(80.0, 0.541417109918, 0.00676050271751, 0.00676050271751),
                triggerBin(100.0, 0.765404884308, 0.00645053530693, 0.00645053530693),
                triggerBin(120.0, 0.908510721239, 0.00490781592535, 0.00490781592535),
                triggerBin(140.0, 0.967776208617, 0.00362025161235, 0.00362025161235),
                triggerBin(160.0, 0.990827170506, 0.00242017195354, 0.00242017195354),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0691582256374, 0.00474186493714),
                triggerBin(20.0, 0.0860120637857, 0.0037966553385, 0.0037966553385),
                triggerBin(30.0, 0.121907430973, 0.00470566063354, 0.00470566063354),
                triggerBin(40.0, 0.15780653497, 0.00556955212978, 0.00556955212978),
                triggerBin(50.0, 0.225478230755, 0.0072080533046, 0.0072080533046),
                triggerBin(60.0, 0.288857344986, 0.00836292522532, 0.00836292522532),
                triggerBin(70.0, 0.350937069288, 0.00953195853217, 0.00953195853217),
                triggerBin(80.0, 0.542142995123, 0.00761607663038, 0.00761607663038),
                triggerBin(100.0, 0.766739106673, 0.00727722166674, 0.00727722166674),
                triggerBin(120.0, 0.905405368383, 0.005660094712, 0.005660094712),
                triggerBin(140.0, 0.969429945489, 0.0040231022137, 0.0040231022137),
                triggerBin(160.0, 0.99366070065, 0.00227847640118, 0.00227847640118),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0691582256374, 0.00474186493714),
                triggerBin(20.0, 0.0944625407166, 0.00627620251486, 0.00593464191002),
                triggerBin(30.0, 0.129933481153, 0.00747102540866, 0.00713261247368),
                triggerBin(40.0, 0.16874687968, 0.00878719203443, 0.00844666721391),
                triggerBin(50.0, 0.227880330999, 0.0110769669526, 0.0107202554409),
                triggerBin(60.0, 0.303230543319, 0.0129664476268, 0.0126691218359),
                triggerBin(70.0, 0.365300784656, 0.0147682758989, 0.0145263317607),
                triggerBin(80.0, 0.548830111902, 0.0114486629442, 0.0114994474126),
                triggerBin(100.0, 0.765060240964, 0.0111175628133, 0.0114830760252),
                triggerBin(120.0, 0.889354568315, 0.00915963013916, 0.00984216290523),
                triggerBin(140.0, 0.96125, 0.00683052891516, 0.00808848752627),
                triggerBin(160.0, 0.994652406417, 0.00290896961209, 0.00517433891575),
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

    # Used input: multicrab_MetLeg2012_130517_110812

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.05, 0.048733971724),
                triggerBin(20.0, 0.0833333333333, 0.166519597077, 0.0690403141434),
                triggerBin(30.0, 0.0, 0.231260479746, 0.0),
                triggerBin(40.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(50.0, 0.5, 0.41724846474, 0.41724846474),
                triggerBin(60.0, 0.0, 0.841344746068, 0.0),
                triggerBin(70.0, 1.0, 0.0, 0.601684479424),
                triggerBin(80.0, 0.0, 1.0, 0.0),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.025641025641, 0.0113190475827),
                triggerBin(20.0, 0.0300751879699, 0.0231409974237, 0.0143389657932),
                triggerBin(30.0, 0.0752688172043, 0.0381876650234, 0.0273417817938),
                triggerBin(40.0, 0.162790697674, 0.0766334033584, 0.058017338737),
                triggerBin(50.0, 0.194444444444, 0.0889424939268, 0.068790877801),
                triggerBin(60.0, 0.363636363636, 0.195231028387, 0.164761960702),
                triggerBin(70.0, 0.0, 0.841344746068, 0.0),
                triggerBin(80.0, 0.75, 0.207730893696, 0.368402425504),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.028, 0.0104337912573),
                triggerBin(20.0, 0.0412371134021, 0.0197085261874, 0.0141451834179),
                triggerBin(30.0, 0.0833333333333, 0.0334310228604, 0.025385131148),
                triggerBin(40.0, 0.0506329113924, 0.0382257148326, 0.0240761892777),
                triggerBin(50.0, 0.166666666667, 0.0862612860187, 0.0640469271296),
                triggerBin(60.0, 0.333333333333, 0.145567823704, 0.123318223606),
                triggerBin(70.0, 0.5, 0.176478356266, 0.176478356266),
                triggerBin(80.0, 0.25, 0.368402425504, 0.207730893696),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.75, 0.207730893696, 0.368402425504),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.025641025641, 0.00956634122401),
                triggerBin(20.0, 0.041095890411, 0.01820490664, 0.0133158433994),
                triggerBin(30.0, 0.0700636942675, 0.0267414944195, 0.0204350521541),
                triggerBin(40.0, 0.10989010989, 0.0431829785367, 0.0332466549201),
                triggerBin(50.0, 0.117647058824, 0.0636560481649, 0.0456587756637),
                triggerBin(60.0, 0.25, 0.133747879731, 0.103407053241),
                triggerBin(70.0, 0.142857142857, 0.257123832984, 0.118480071045),
                triggerBin(80.0, 0.428571428571, 0.247840988275, 0.222487613116),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.458641675296),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0, 0.458641675296),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0279069767442, 0.0112328789395),
                triggerBin(20.0, 0.0344827586207, 0.0226536450207, 0.014815011728),
                triggerBin(30.0, 0.07, 0.0356680906999, 0.025455689305),
                triggerBin(40.0, 0.173913043478, 0.0745206943475, 0.0578399488833),
                triggerBin(50.0, 0.210526315789, 0.0873003831507, 0.0693657511201),
                triggerBin(60.0, 0.333333333333, 0.185994488221, 0.151856070435),
                triggerBin(70.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(80.0, 0.75, 0.207730893696, 0.368402425504),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.5, 0.314698893873, 0.314698893873),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0279569892473, 0.00764471790369),
                triggerBin(20.0, 0.0383480825959, 0.0134940973628, 0.0103909602007),
                triggerBin(30.0, 0.0772727272727, 0.0224483946638, 0.0181326003294),
                triggerBin(40.0, 0.096, 0.0340404621712, 0.0266345527184),
                triggerBin(50.0, 0.189189189189, 0.0567879423569, 0.0472277746216),
                triggerBin(60.0, 0.333333333333, 0.107317780779, 0.0943571124254),
                triggerBin(70.0, 0.533333333333, 0.152935340154, 0.158270494867),
                triggerBin(80.0, 0.5, 0.220457375638, 0.220457375638),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.6, 0.25334762525, 0.303366136254),
                triggerBin(140.0, 0.75, 0.207730893696, 0.368402425504),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0271002710027, 0.0059771296637),
                triggerBin(20.0, 0.0394265232975, 0.0100667987371, 0.00823822711329),
                triggerBin(30.0, 0.0742705570292, 0.0160784942603, 0.0136020483313),
                triggerBin(40.0, 0.101851851852, 0.0249340403831, 0.0208446594972),
                triggerBin(50.0, 0.16, 0.0397352655668, 0.0336632266047),
                triggerBin(60.0, 0.3, 0.078587256674, 0.0694765089311),
                triggerBin(70.0, 0.409090909091, 0.129031169349, 0.119289306437),
                triggerBin(80.0, 0.466666666667, 0.158270494867, 0.152935340154),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.75, 0.159659347816, 0.239566802733),
                triggerBin(140.0, 0.75, 0.207730893696, 0.368402425504),
                triggerBin(160.0, 1.0, 0.0, 0.308024223477),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0763629206849, 0.00372578120498),
                triggerBin(20.0, 0.086849046471, 0.00227994818723, 0.00227994818723),
                triggerBin(30.0, 0.128196261245, 0.00292606606509, 0.00292606606509),
                triggerBin(40.0, 0.16534022829, 0.00361012492157, 0.00361012492157),
                triggerBin(50.0, 0.215870144724, 0.00452873908221, 0.00452873908221),
                triggerBin(60.0, 0.275581785603, 0.00541540846105, 0.00541540846105),
                triggerBin(70.0, 0.342116363233, 0.00622776726595, 0.00622776726595),
                triggerBin(80.0, 0.519557959812, 0.00508493712337, 0.00508493712337),
                triggerBin(100.0, 0.762160694887, 0.0048483618294, 0.0048483618294),
                triggerBin(120.0, 0.914563284375, 0.00365415914631, 0.00365415914631),
                triggerBin(140.0, 0.976857043611, 0.00235556324503, 0.00235556324503),
                triggerBin(160.0, 0.996570083875, 0.00115864688943, 0.00115864688943),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0763629206849, 0.00372578120498),
                triggerBin(20.0, 0.0881904259827, 0.00248847755748, 0.00248847755748),
                triggerBin(30.0, 0.127508847421, 0.00315719362069, 0.00315719362069),
                triggerBin(40.0, 0.166873011633, 0.00391994545088, 0.00391994545088),
                triggerBin(50.0, 0.232179742322, 0.00507905329911, 0.00507905329911),
                triggerBin(60.0, 0.284415603094, 0.00589514043821, 0.00589514043821),
                triggerBin(70.0, 0.355924836355, 0.00686025291565, 0.00686025291565),
                triggerBin(80.0, 0.525300651215, 0.00560625743107, 0.00560625743107),
                triggerBin(100.0, 0.759187584225, 0.00537680088368, 0.00537680088368),
                triggerBin(120.0, 0.910444317063, 0.00407190174429, 0.00407190174429),
                triggerBin(140.0, 0.973230294226, 0.00275638919936, 0.00275638919936),
                triggerBin(160.0, 0.991404616188, 0.0019981814239, 0.0019981814239),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0763629206849, 0.00372578120498),
                triggerBin(20.0, 0.0880298943427, 0.00256185594626, 0.00256185594626),
                triggerBin(30.0, 0.127679577099, 0.00325026587164, 0.00325026587164),
                triggerBin(40.0, 0.167486042781, 0.00403685803721, 0.00403685803721),
                triggerBin(50.0, 0.226056199519, 0.00515690190965, 0.00515690190965),
                triggerBin(60.0, 0.284454233592, 0.006079975592, 0.006079975592),
                triggerBin(70.0, 0.353549915284, 0.00703091624645, 0.00703091624645),
                triggerBin(80.0, 0.526468838302, 0.00572787732547, 0.00572787732547),
                triggerBin(100.0, 0.761183238255, 0.00549368913961, 0.00549368913961),
                triggerBin(120.0, 0.911280489752, 0.0041633577356, 0.0041633577356),
                triggerBin(140.0, 0.973800361703, 0.00280444856249, 0.00280444856249),
                triggerBin(160.0, 0.992939548134, 0.00186660532983, 0.00186660532983),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0763629206849, 0.00372578120498),
                triggerBin(20.0, 0.0895878838685, 0.00288868750394, 0.00288868750394),
                triggerBin(30.0, 0.128027118414, 0.00363263575549, 0.00363263575549),
                triggerBin(40.0, 0.168967790427, 0.00451226022089, 0.00451226022089),
                triggerBin(50.0, 0.222293744321, 0.00570912147206, 0.00570912147206),
                triggerBin(60.0, 0.286485549926, 0.00680791633483, 0.00680791633483),
                triggerBin(70.0, 0.354497172128, 0.00784445506721, 0.00784445506721),
                triggerBin(80.0, 0.52790478028, 0.00635939463809, 0.00635939463809),
                triggerBin(100.0, 0.762678274365, 0.00611448578321, 0.00611448578321),
                triggerBin(120.0, 0.909174831685, 0.00470312616775, 0.00470312616775),
                triggerBin(140.0, 0.974074736244, 0.00312639356941, 0.00312639356941),
                triggerBin(160.0, 0.994498566745, 0.00182953934934, 0.00182953934934),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0763629206849, 0.00372578120498),
                triggerBin(20.0, 0.0879810124844, 0.002456750992, 0.002456750992),
                triggerBin(30.0, 0.127615854276, 0.00312251321562, 0.00312251321562),
                triggerBin(40.0, 0.166634584295, 0.00387308873371, 0.00387308873371),
                triggerBin(50.0, 0.229598138126, 0.00499365620049, 0.00499365620049),
                triggerBin(60.0, 0.283048740695, 0.00582260460828, 0.00582260460828),
                triggerBin(70.0, 0.353743351897, 0.00676329623413, 0.00676329623413),
                triggerBin(80.0, 0.52437668452, 0.00552586544508, 0.00552586544508),
                triggerBin(100.0, 0.759665724286, 0.00529469691991, 0.00529469691991),
                triggerBin(120.0, 0.911094643643, 0.00400709633811, 0.00400709633811),
                triggerBin(140.0, 0.973802064999, 0.00269333121657, 0.00269333121657),
                triggerBin(160.0, 0.992221402346, 0.00187716057599, 0.00187716057599),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0763629206849, 0.00372578120498),
                triggerBin(20.0, 0.0880080643479, 0.00251539383235, 0.00251539383235),
                triggerBin(30.0, 0.12765109019, 0.00319387597219, 0.00319387597219),
                triggerBin(40.0, 0.167106273086, 0.00396450184866, 0.00396450184866),
                triggerBin(50.0, 0.227632556981, 0.00508544199906, 0.00508544199906),
                triggerBin(60.0, 0.283825560975, 0.00596608478141, 0.00596608478141),
                triggerBin(70.0, 0.353636134039, 0.00691292026561, 0.00691292026561),
                triggerBin(80.0, 0.525538835269, 0.00563903571849, 0.00563903571849),
                triggerBin(100.0, 0.760506926842, 0.00540610972961, 0.00540610972961),
                triggerBin(120.0, 0.911197535768, 0.00409449635804, 0.00409449635804),
                triggerBin(140.0, 0.973800938835, 0.00275539699957, 0.00275539699957),
                triggerBin(160.0, 0.992618118061, 0.00187324276227, 0.00187324276227),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0763629206849, 0.00372578120498),
                triggerBin(20.0, 0.0895878838685, 0.00288868750394, 0.00288868750394),
                triggerBin(30.0, 0.128027118414, 0.00363263575549, 0.00363263575549),
                triggerBin(40.0, 0.168967790427, 0.00451226022089, 0.00451226022089),
                triggerBin(50.0, 0.222293744321, 0.00570912147206, 0.00570912147206),
                triggerBin(60.0, 0.286485549926, 0.00680791633483, 0.00680791633483),
                triggerBin(70.0, 0.354497172128, 0.00784445506721, 0.00784445506721),
                triggerBin(80.0, 0.52790478028, 0.00635939463809, 0.00635939463809),
                triggerBin(100.0, 0.762678274365, 0.00611448578321, 0.00611448578321),
                triggerBin(120.0, 0.909174831685, 0.00470312616775, 0.00470312616775),
                triggerBin(140.0, 0.974074736244, 0.00312639356941, 0.00312639356941),
                triggerBin(160.0, 0.994498566745, 0.00182953934934, 0.00182953934934),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0763629206849, 0.00372578120498),
                triggerBin(20.0, 0.097177969959, 0.00467631212014, 0.0044883143824),
                triggerBin(30.0, 0.132205995388, 0.00564606023587, 0.00545316707397),
                triggerBin(40.0, 0.179702048417, 0.00702018076622, 0.00681683643271),
                triggerBin(50.0, 0.22633910592, 0.00871073176946, 0.00848507236739),
                triggerBin(60.0, 0.307125307125, 0.0105663189042, 0.0103722645972),
                triggerBin(70.0, 0.378027170703, 0.0121503542067, 0.0120027056931),
                triggerBin(80.0, 0.543555240793, 0.00953273632522, 0.00956415869998),
                triggerBin(100.0, 0.76548463357, 0.00931892575874, 0.0095763446401),
                triggerBin(120.0, 0.894011976048, 0.00758673555693, 0.00807720055243),
                triggerBin(140.0, 0.965004374453, 0.00544095048212, 0.00631973950827),
                triggerBin(160.0, 0.994743758213, 0.0025139074707, 0.00413649665585),
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

    # Used input: multicrab_MetLeg2012_130517_110812

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.111111111111, 0.104756560176),
                triggerBin(20.0, 0.125, 0.23225032014, 0.103637263595),
                triggerBin(30.0, 0.0, 0.36887757085, 0.0),
                triggerBin(40.0, 0.5, 0.41724846474, 0.41724846474),
                triggerBin(50.0, 0.5, 0.41724846474, 0.41724846474),
                triggerBin(60.0, 0.0, 1.0, 0.0),
                triggerBin(70.0, 1.0, 0.0, 0.601684479424),
                triggerBin(80.0, 0.0, 1.0, 0.0),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0336134453782, 0.0165218423464),
                triggerBin(20.0, 0.0348837209302, 0.0327700967741, 0.0189255996623),
                triggerBin(30.0, 0.125, 0.0608241577898, 0.0449271328006),
                triggerBin(40.0, 0.136363636364, 0.11509911457, 0.0732667013517),
                triggerBin(50.0, 0.166666666667, 0.135998901491, 0.0892717907981),
                triggerBin(60.0, 0.25, 0.239566802733, 0.159659347816),
                triggerBin(70.0, 0.0, 0.841344746068, 0.0),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0281690140845, 0.0138847166789),
                triggerBin(20.0, 0.051724137931, 0.0296167889077, 0.0203272293421),
                triggerBin(30.0, 0.0757575757576, 0.0480000082871, 0.032332845254),
                triggerBin(40.0, 0.0681818181818, 0.0619005708815, 0.0368770250397),
                triggerBin(50.0, 0.173913043478, 0.116302557627, 0.081292990613),
                triggerBin(60.0, 0.333333333333, 0.185994488221, 0.151856070435),
                triggerBin(70.0, 0.5, 0.195182116991, 0.195182116991),
                triggerBin(80.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 1.0, 0.0, 0.458641675296),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0225988700565, 0.0111710281883),
                triggerBin(20.0, 0.03125, 0.0240190532641, 0.0148968388901),
                triggerBin(30.0, 0.0348837209302, 0.0327700967741, 0.0189255996623),
                triggerBin(40.0, 0.127659574468, 0.0684613972074, 0.0494467249774),
                triggerBin(50.0, 0.2, 0.112667857843, 0.0835234580544),
                triggerBin(60.0, 0.272727272727, 0.196072358725, 0.144395891738),
                triggerBin(70.0, 0.0, 0.36887757085, 0.0),
                triggerBin(80.0, 0.25, 0.368402425504, 0.207730893696),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.458641675296),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0390625, 0.0171246854656),
                triggerBin(20.0, 0.0425531914894, 0.0323678650094, 0.0202555238052),
                triggerBin(30.0, 0.116666666667, 0.0571758165749, 0.0420083072563),
                triggerBin(40.0, 0.166666666667, 0.112297423319, 0.077988895091),
                triggerBin(50.0, 0.2, 0.130118869123, 0.0931224604655),
                triggerBin(60.0, 0.25, 0.239566802733, 0.159659347816),
                triggerBin(70.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.5, 0.314698893873, 0.314698893873),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0333333333333, 0.0109243564472),
                triggerBin(20.0, 0.047619047619, 0.0196262351462, 0.0146356034049),
                triggerBin(30.0, 0.0952380952381, 0.0337896798256, 0.0264287787198),
                triggerBin(40.0, 0.102941176471, 0.0510395044133, 0.0371760537044),
                triggerBin(50.0, 0.186046511628, 0.0788697532887, 0.0616866743041),
                triggerBin(60.0, 0.3, 0.135910953525, 0.111901660362),
                triggerBin(70.0, 0.538461538462, 0.164847322399, 0.172004084463),
                triggerBin(80.0, 0.6, 0.25334762525, 0.303366136254),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.6, 0.25334762525, 0.303366136254),
                triggerBin(140.0, 1.0, 0.0, 0.458641675296),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0290827740492, 0.00794795237694),
                triggerBin(20.0, 0.0414201183432, 0.0138912736932, 0.010812974964),
                triggerBin(30.0, 0.0707547169811, 0.0222805405079, 0.0177024361083),
                triggerBin(40.0, 0.113043478261, 0.0376688495896, 0.0299925163015),
                triggerBin(50.0, 0.191176470588, 0.0599041554082, 0.0495236647292),
                triggerBin(60.0, 0.290322580645, 0.103897013206, 0.0880517504109),
                triggerBin(70.0, 0.411764705882, 0.149770451815, 0.137360513174),
                triggerBin(80.0, 0.444444444444, 0.213462824948, 0.198267144951),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.75, 0.159659347816, 0.239566802733),
                triggerBin(140.0, 1.0, 0.0, 0.458641675296),
                triggerBin(160.0, 1.0, 0.0, 0.36887757085),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.072374499538, 0.00454713640075),
                triggerBin(20.0, 0.0867333030099, 0.00285382783705, 0.00285382783705),
                triggerBin(30.0, 0.120151046056, 0.00353629718356, 0.00353629718356),
                triggerBin(40.0, 0.163270924738, 0.00434651203154, 0.00434651203154),
                triggerBin(50.0, 0.222927940996, 0.00549235095522, 0.00549235095522),
                triggerBin(60.0, 0.277026715951, 0.00640725373174, 0.00640725373174),
                triggerBin(70.0, 0.338437023373, 0.00724007739053, 0.00724007739053),
                triggerBin(80.0, 0.533881707273, 0.00590285916329, 0.00590285916329),
                triggerBin(100.0, 0.769284316335, 0.00545283040122, 0.00545283040122),
                triggerBin(120.0, 0.914356433418, 0.00414289118694, 0.00414289118694),
                triggerBin(140.0, 0.973581787865, 0.00285188994591, 0.00285188994591),
                triggerBin(160.0, 0.995798410136, 0.00141877096841, 0.00141877096841),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.072374499538, 0.00454713640075),
                triggerBin(20.0, 0.0892131880185, 0.00311707051909, 0.00311707051909),
                triggerBin(30.0, 0.11676131561, 0.00377088417107, 0.00377088417107),
                triggerBin(40.0, 0.164111998242, 0.00472481235614, 0.00472481235614),
                triggerBin(50.0, 0.238870536247, 0.00611230167901, 0.00611230167901),
                triggerBin(60.0, 0.283225448219, 0.00689247176109, 0.00689247176109),
                triggerBin(70.0, 0.355839654325, 0.00797599774894, 0.00797599774894),
                triggerBin(80.0, 0.538403396374, 0.00651022511358, 0.00651022511358),
                triggerBin(100.0, 0.762508912046, 0.00609917589068, 0.00609917589068),
                triggerBin(120.0, 0.906864348511, 0.00471646021463, 0.00471646021463),
                triggerBin(140.0, 0.969138794222, 0.00334515622539, 0.00334515622539),
                triggerBin(160.0, 0.98932752257, 0.00247842159782, 0.00247842159782),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.072374499538, 0.00454713640075),
                triggerBin(20.0, 0.0885357399389, 0.00320967663778, 0.00320967663778),
                triggerBin(30.0, 0.118277219594, 0.00390273687692, 0.00390273687692),
                triggerBin(40.0, 0.164857807488, 0.0048582514124, 0.0048582514124),
                triggerBin(50.0, 0.232077569643, 0.00621936469218, 0.00621936469218),
                triggerBin(60.0, 0.283602627947, 0.0071407258357, 0.0071407258357),
                triggerBin(70.0, 0.352402954655, 0.00818915678392, 0.00818915678392),
                triggerBin(80.0, 0.540260525808, 0.00664603503308, 0.00664603503308),
                triggerBin(100.0, 0.765372002271, 0.0062177389847, 0.0062177389847),
                triggerBin(120.0, 0.90915784255, 0.00477781122471, 0.00477781122471),
                triggerBin(140.0, 0.970070047774, 0.00339214442553, 0.00339214442553),
                triggerBin(160.0, 0.991251561872, 0.00231087846988, 0.00231087846988),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.072374499538, 0.00454713640075),
                triggerBin(20.0, 0.0899855978932, 0.00362555901594, 0.00362555901594),
                triggerBin(30.0, 0.119952308899, 0.0043793270228, 0.0043793270228),
                triggerBin(40.0, 0.165285290356, 0.00540767426108, 0.00540767426108),
                triggerBin(50.0, 0.226267599389, 0.00686568367379, 0.00686568367379),
                triggerBin(60.0, 0.285489505168, 0.00800412329095, 0.00800412329095),
                triggerBin(70.0, 0.350725670386, 0.00912160898564, 0.00912160898564),
                triggerBin(80.0, 0.541147603372, 0.00736278577791, 0.00736278577791),
                triggerBin(100.0, 0.766446604771, 0.00691274980343, 0.00691274980343),
                triggerBin(120.0, 0.907698559677, 0.00536837086331, 0.00536837086331),
                triggerBin(140.0, 0.971190235526, 0.00373588061422, 0.00373588061422),
                triggerBin(160.0, 0.993177334655, 0.00226742315083, 0.00226742315083),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.072374499538, 0.00454713640075),
                triggerBin(20.0, 0.0888293360725, 0.00307708420182, 0.00307708420182),
                triggerBin(30.0, 0.117287075478, 0.00373638693492, 0.00373638693492),
                triggerBin(40.0, 0.163980551916, 0.00466749949812, 0.00466749949812),
                triggerBin(50.0, 0.236372245068, 0.00601697939775, 0.00601697939775),
                triggerBin(60.0, 0.28228091172, 0.00682009670138, 0.00682009670138),
                triggerBin(70.0, 0.353102138404, 0.00786354066443, 0.00786354066443),
                triggerBin(80.0, 0.537676021796, 0.00641650753875, 0.00641650753875),
                triggerBin(100.0, 0.763605016696, 0.00599786003845, 0.00599786003845),
                triggerBin(120.0, 0.908056858631, 0.00462622029717, 0.00462622029717),
                triggerBin(140.0, 0.969836545254, 0.00326784285181, 0.00326784285181),
                triggerBin(160.0, 0.990362536609, 0.00232356742393, 0.00232356742393),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.072374499538, 0.00454713640075),
                triggerBin(20.0, 0.0886673205913, 0.00315105322656, 0.00315105322656),
                triggerBin(30.0, 0.117835362736, 0.00382912793053, 0.00382912793053),
                triggerBin(40.0, 0.164467178762, 0.0047740716103, 0.0047740716103),
                triggerBin(50.0, 0.233992925586, 0.00613075634893, 0.00613075634893),
                triggerBin(60.0, 0.283009841588, 0.00699852465873, 0.00699852465873),
                triggerBin(70.0, 0.352715329123, 0.0080453803771, 0.0080453803771),
                triggerBin(80.0, 0.539112155571, 0.00654516442291, 0.00654516442291),
                triggerBin(100.0, 0.764584829972, 0.00612105012396, 0.00612105012396),
                triggerBin(120.0, 0.908667194379, 0.00471142835388, 0.00471142835388),
                triggerBin(140.0, 0.969965834753, 0.00333743131829, 0.00333743131829),
                triggerBin(160.0, 0.990853645508, 0.0023189359264, 0.0023189359264),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.072374499538, 0.00454713640075),
                triggerBin(20.0, 0.0899855978932, 0.00362555901594, 0.00362555901594),
                triggerBin(30.0, 0.119952308899, 0.0043793270228, 0.0043793270228),
                triggerBin(40.0, 0.165285290356, 0.00540767426108, 0.00540767426108),
                triggerBin(50.0, 0.226267599389, 0.00686568367379, 0.00686568367379),
                triggerBin(60.0, 0.285489505168, 0.00800412329095, 0.00800412329095),
                triggerBin(70.0, 0.350725670386, 0.00912160898564, 0.00912160898564),
                triggerBin(80.0, 0.541147603372, 0.00736278577791, 0.00736278577791),
                triggerBin(100.0, 0.766446604771, 0.00691274980343, 0.00691274980343),
                triggerBin(120.0, 0.907698559677, 0.00536837086331, 0.00536837086331),
                triggerBin(140.0, 0.971190235526, 0.00373588061422, 0.00373588061422),
                triggerBin(160.0, 0.993177334655, 0.00226742315083, 0.00226742315083),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.072374499538, 0.00454713640075),
                triggerBin(20.0, 0.0979547900969, 0.00595903411243, 0.00566138351002),
                triggerBin(30.0, 0.127002735444, 0.00692745550911, 0.00662734936174),
                triggerBin(40.0, 0.171635049684, 0.00839084111443, 0.00808593544265),
                triggerBin(50.0, 0.225214899713, 0.0104460579845, 0.0101222042304),
                triggerBin(60.0, 0.300938337802, 0.0123429542333, 0.0120686963013),
                triggerBin(70.0, 0.368, 0.0141435475327, 0.0139262606791),
                triggerBin(80.0, 0.550164861046, 0.0110056169998, 0.0110538924204),
                triggerBin(100.0, 0.763317191283, 0.0105937471632, 0.0109216408099),
                triggerBin(120.0, 0.89373088685, 0.00858909931289, 0.00921787451751),
                triggerBin(140.0, 0.962585034014, 0.00639621940683, 0.00753759111279),
                triggerBin(160.0, 0.993399339934, 0.00315637224661, 0.00518823409511),
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

    # Used input: multicrab_MetLeg2012_130517_110812

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.142857142857, 0.132260014253),
                triggerBin(20.0, 0.142857142857, 0.257123832984, 0.118480071045),
                triggerBin(30.0, 0.0, 0.458641675296, 0.0),
                triggerBin(40.0, 0.5, 0.41724846474, 0.41724846474),
                triggerBin(50.0, 0.5, 0.41724846474, 0.41724846474),
                triggerBin(60.0, 0.0, 1.0, 0.0),
                triggerBin(70.0, 1.0, 0.0, 0.601684479424),
                triggerBin(80.0, 0.0, 1.0, 0.0),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0392156862745, 0.0192195305651),
                triggerBin(20.0, 0.038961038961, 0.0364493853816, 0.0211298096514),
                triggerBin(30.0, 0.117647058824, 0.0636560481649, 0.0456587756637),
                triggerBin(40.0, 0.166666666667, 0.135998901491, 0.0892717907981),
                triggerBin(50.0, 0.142857142857, 0.158270654649, 0.0917088958422),
                triggerBin(60.0, 0.25, 0.239566802733, 0.159659347816),
                triggerBin(70.0, 0.0, 0.841344746068, 0.0),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.0, 0.601684479424, 0.0),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0327868852459, 0.016122457965),
                triggerBin(20.0, 0.0594059405941, 0.0337974107057, 0.0233130483776),
                triggerBin(30.0, 0.0806451612903, 0.0508738752303, 0.0343911806251),
                triggerBin(40.0, 0.0789473684211, 0.0708737003562, 0.0426562617902),
                triggerBin(50.0, 0.210526315789, 0.135427055903, 0.0978662361907),
                triggerBin(60.0, 0.333333333333, 0.185994488221, 0.151856070435),
                triggerBin(70.0, 0.444444444444, 0.213462824948, 0.198267144951),
                triggerBin(80.0, 0.0, 0.601684479424, 0.0),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 1.0, 0.0, 0.601684479424),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.025974025974, 0.0128172408109),
                triggerBin(20.0, 0.0263157894737, 0.0249359369637, 0.0142883223082),
                triggerBin(30.0, 0.038961038961, 0.0364493853816, 0.0211298096514),
                triggerBin(40.0, 0.130434782609, 0.0697762494647, 0.0504937771347),
                triggerBin(50.0, 0.227272727273, 0.124519809699, 0.0944237146768),
                triggerBin(60.0, 0.3, 0.20826248199, 0.158328098893),
                triggerBin(70.0, 0.0, 0.36887757085, 0.0),
                triggerBin(80.0, 0.25, 0.368402425504, 0.207730893696),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.458641675296),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.045871559633, 0.0200383484757),
                triggerBin(20.0, 0.047619047619, 0.0360513607022, 0.0226519839091),
                triggerBin(30.0, 0.111111111111, 0.060467252805, 0.0431774157972),
                triggerBin(40.0, 0.2, 0.130118869123, 0.0931224604655),
                triggerBin(50.0, 0.1875, 0.149398565056, 0.100212028831),
                triggerBin(60.0, 0.25, 0.239566802733, 0.159659347816),
                triggerBin(70.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.038961038961, 0.0127315057964),
                triggerBin(20.0, 0.0540540540541, 0.0221717569697, 0.0165871352054),
                triggerBin(30.0, 0.0948275862069, 0.0355229928616, 0.0274768938321),
                triggerBin(40.0, 0.120689655172, 0.0589443821995, 0.0434188250899),
                triggerBin(50.0, 0.2, 0.0910146087326, 0.0706631844333),
                triggerBin(60.0, 0.3, 0.135910953525, 0.111901660362),
                triggerBin(70.0, 0.5, 0.176478356266, 0.176478356266),
                triggerBin(80.0, 0.5, 0.314698893873, 0.314698893873),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.5, 0.314698893873, 0.314698893873),
                triggerBin(140.0, 1.0, 0.0, 0.601684479424),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0337662337662, 0.00920559897717),
                triggerBin(20.0, 0.0434782608696, 0.0152440228034, 0.011764633588),
                triggerBin(30.0, 0.0725388601036, 0.0237975497686, 0.0187699741391),
                triggerBin(40.0, 0.125, 0.0412759820659, 0.0330480156249),
                triggerBin(50.0, 0.210526315789, 0.0681226444959, 0.0564551889986),
                triggerBin(60.0, 0.3, 0.106340064496, 0.090716398418),
                triggerBin(70.0, 0.375, 0.156048626467, 0.137247055387),
                triggerBin(80.0, 0.375, 0.234946487636, 0.196075614151),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.714285714286, 0.182129028008, 0.259937875571),
                triggerBin(140.0, 1.0, 0.0, 0.601684479424),
                triggerBin(160.0, 1.0, 0.0, 0.36887757085),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0693277310924, 0.00475305433254),
                triggerBin(20.0, 0.0824632474216, 0.00298467329786, 0.00298467329786),
                triggerBin(30.0, 0.119318835672, 0.00376512126544, 0.00376512126544),
                triggerBin(40.0, 0.153968494618, 0.0044556926938, 0.0044556926938),
                triggerBin(50.0, 0.219975080494, 0.0057539068892, 0.0057539068892),
                triggerBin(60.0, 0.280741938584, 0.0066970213197, 0.0066970213197),
                triggerBin(70.0, 0.340923383865, 0.00759573683042, 0.00759573683042),
                triggerBin(80.0, 0.531651497693, 0.00612732133851, 0.00612732133851),
                triggerBin(100.0, 0.767131161722, 0.0057552391723, 0.0057552391723),
                triggerBin(120.0, 0.911522823732, 0.00437987291046, 0.00437987291046),
                triggerBin(140.0, 0.971994144684, 0.00305964371804, 0.00305964371804),
                triggerBin(160.0, 0.99573807006, 0.00150024260922, 0.00150024260922),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0693277310924, 0.00475305433254),
                triggerBin(20.0, 0.0841791838309, 0.00325559075781, 0.00325559075781),
                triggerBin(30.0, 0.118809302517, 0.00408092845354, 0.00408092845354),
                triggerBin(40.0, 0.155037790413, 0.00487420634661, 0.00487420634661),
                triggerBin(50.0, 0.236640433548, 0.00641259456403, 0.00641259456403),
                triggerBin(60.0, 0.283208332246, 0.00718651637085, 0.00718651637085),
                triggerBin(70.0, 0.356732089744, 0.00834051593702, 0.00834051593702),
                triggerBin(80.0, 0.536645466414, 0.00676258025166, 0.00676258025166),
                triggerBin(100.0, 0.763389271582, 0.00644081049867, 0.00644081049867),
                triggerBin(120.0, 0.907636402831, 0.00488970562157, 0.00488970562157),
                triggerBin(140.0, 0.966650555532, 0.00364827905709, 0.00364827905709),
                triggerBin(160.0, 0.989110461465, 0.00261529430892, 0.00261529430892),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0693277310924, 0.00475305433254),
                triggerBin(20.0, 0.0839310990788, 0.00335403717641, 0.00335403717641),
                triggerBin(30.0, 0.119484067923, 0.00420122163233, 0.00420122163233),
                triggerBin(40.0, 0.156069646702, 0.00500903625768, 0.00500903625768),
                triggerBin(50.0, 0.230001230483, 0.00653045182237, 0.00653045182237),
                triggerBin(60.0, 0.285160503686, 0.00745532383841, 0.00745532383841),
                triggerBin(70.0, 0.353228345753, 0.00856574514267, 0.00856574514267),
                triggerBin(80.0, 0.538123691453, 0.0069017854428, 0.0069017854428),
                triggerBin(100.0, 0.765693403968, 0.00656198378678, 0.00656198378678),
                triggerBin(120.0, 0.908708939154, 0.00498473761398, 0.00498473761398),
                triggerBin(140.0, 0.967998435679, 0.0036710885465, 0.0036710885465),
                triggerBin(160.0, 0.991230278389, 0.00242276855666, 0.00242276855666),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0693277310924, 0.00475305433254),
                triggerBin(20.0, 0.0860960065862, 0.0038001861335, 0.0038001861335),
                triggerBin(30.0, 0.120702647712, 0.00469587255163, 0.00469587255163),
                triggerBin(40.0, 0.157262540464, 0.00558157065989, 0.00558157065989),
                triggerBin(50.0, 0.224093459637, 0.0072161880427, 0.0072161880427),
                triggerBin(60.0, 0.288305474432, 0.00837179599336, 0.00837179599336),
                triggerBin(70.0, 0.350336366608, 0.00954156590724, 0.00954156590724),
                triggerBin(80.0, 0.538306611761, 0.00765481106873, 0.00765481106873),
                triggerBin(100.0, 0.766211805137, 0.00729116474694, 0.00729116474694),
                triggerBin(120.0, 0.905384169349, 0.00566130207265, 0.00566130207265),
                triggerBin(140.0, 0.969429945489, 0.0040231022137, 0.0040231022137),
                triggerBin(160.0, 0.99361026738, 0.00229655394139, 0.00229655394139),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0693277310924, 0.00475305433254),
                triggerBin(20.0, 0.0839126437927, 0.00321444098849, 0.00321444098849),
                triggerBin(30.0, 0.11888913574, 0.00403326148041, 0.00403326148041),
                triggerBin(40.0, 0.154869043244, 0.00481028872318, 0.00481028872318),
                triggerBin(50.0, 0.23402937753, 0.00631129380687, 0.00631129380687),
                triggerBin(60.0, 0.28283146016, 0.00711359485578, 0.00711359485578),
                triggerBin(70.0, 0.354253722287, 0.00822702843564, 0.00822702843564),
                triggerBin(80.0, 0.535840705148, 0.00666447630927, 0.00666447630927),
                triggerBin(100.0, 0.76400054308, 0.00633306685489, 0.00633306685489),
                triggerBin(120.0, 0.908253176962, 0.00481031453936, 0.00481031453936),
                triggerBin(140.0, 0.967500311537, 0.00355490634646, 0.00355490634646),
                triggerBin(160.0, 0.990161773912, 0.00245443662687, 0.00245443662687),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0693277310924, 0.00475305433254),
                triggerBin(20.0, 0.0839228474345, 0.00329229590173, 0.00329229590173),
                triggerBin(30.0, 0.119218986542, 0.0041270536746, 0.0041270536746),
                triggerBin(40.0, 0.155535437775, 0.00492131331177, 0.00492131331177),
                triggerBin(50.0, 0.231799197844, 0.00643438714963, 0.00643438714963),
                triggerBin(60.0, 0.284116062012, 0.00730367315088, 0.00730367315088),
                triggerBin(70.0, 0.353686501464, 0.00841621706425, 0.00841621706425),
                triggerBin(80.0, 0.537109941454, 0.00679750526258, 0.00679750526258),
                triggerBin(100.0, 0.764939591776, 0.0064613627912, 0.0064613627912),
                triggerBin(120.0, 0.908506253938, 0.00490805071575, 0.00490805071575),
                triggerBin(140.0, 0.967776208617, 0.00362025161235, 0.00362025161235),
                triggerBin(160.0, 0.990751300388, 0.00244007537334, 0.00244007537334),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0693277310924, 0.00475305433254),
                triggerBin(20.0, 0.0860960065862, 0.0038001861335, 0.0038001861335),
                triggerBin(30.0, 0.120702647712, 0.00469587255163, 0.00469587255163),
                triggerBin(40.0, 0.157262540464, 0.00558157065989, 0.00558157065989),
                triggerBin(50.0, 0.224093459637, 0.0072161880427, 0.0072161880427),
                triggerBin(60.0, 0.288305474432, 0.00837179599336, 0.00837179599336),
                triggerBin(70.0, 0.350336366608, 0.00954156590724, 0.00954156590724),
                triggerBin(80.0, 0.538306611761, 0.00765481106873, 0.00765481106873),
                triggerBin(100.0, 0.766211805137, 0.00729116474694, 0.00729116474694),
                triggerBin(120.0, 0.905384169349, 0.00566130207265, 0.00566130207265),
                triggerBin(140.0, 0.969429945489, 0.0040231022137, 0.0040231022137),
                triggerBin(160.0, 0.99361026738, 0.00229655394139, 0.00229655394139),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0693277310924, 0.00475305433254),
                triggerBin(20.0, 0.094616639478, 0.00628587040292, 0.00594388178105),
                triggerBin(30.0, 0.129060970182, 0.00746513485543, 0.00712466845594),
                triggerBin(40.0, 0.167589330649, 0.00880179453284, 0.00845726127396),
                triggerBin(50.0, 0.225496476618, 0.0110762215834, 0.0107140074898),
                triggerBin(60.0, 0.30258302583, 0.0129941751903, 0.0126943032605),
                triggerBin(70.0, 0.364273204904, 0.0147941669939, 0.0145492900188),
                triggerBin(80.0, 0.546386468478, 0.0115000151026, 0.011548632541),
                triggerBin(100.0, 0.764271323036, 0.0111497461775, 0.0115154002654),
                triggerBin(120.0, 0.889168765743, 0.00917421314595, 0.0098575683242),
                triggerBin(140.0, 0.96125, 0.00683052891516, 0.00808848752627),
                triggerBin(160.0, 0.994633273703, 0.00291937241779, 0.00519275337642),
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

    # Used input: multicrab_MetLeg2012_130517_110812

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0666666666667, 0.0644061188719),
                triggerBin(20.0, 0.0909090909091, 0.179295209474, 0.0753268806181),
                triggerBin(30.0, 0.0, 0.36887757085, 0.0),
                triggerBin(40.0, 0.0, 0.841344746068, 0.0),
                triggerBin(50.0, 0.5, 0.41724846474, 0.41724846474),
                triggerBin(60.0, 0.0, 1.0, 0.0),
                triggerBin(70.0, 1.0, 0.0, 0.601684479424),
                triggerBin(80.0, 0.0, 1.0, 0.0),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0295857988166, 0.0130339745683),
                triggerBin(20.0, 0.036036036036, 0.0275760676929, 0.0171677750461),
                triggerBin(30.0, 0.0681818181818, 0.0385044118677, 0.0267133636922),
                triggerBin(40.0, 0.125, 0.0757199817448, 0.0529092136612),
                triggerBin(50.0, 0.176470588235, 0.0905039073753, 0.0676761749045),
                triggerBin(60.0, 0.4, 0.204596854236, 0.180009253894),
                triggerBin(70.0, 0.0, 0.841344746068, 0.0),
                triggerBin(80.0, 0.75, 0.207730893696, 0.368402425504),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0272727272727, 0.0109811668572),
                triggerBin(20.0, 0.0280898876404, 0.0185555038223, 0.0120805355016),
                triggerBin(30.0, 0.0660377358491, 0.0337580471231, 0.0240344740711),
                triggerBin(40.0, 0.0588235294118, 0.0440704816426, 0.0279408462558),
                triggerBin(50.0, 0.1, 0.0877974084544, 0.0539221516634),
                triggerBin(60.0, 0.266666666667, 0.161145049639, 0.122866921165),
                triggerBin(70.0, 0.444444444444, 0.213462824948, 0.198267144951),
                triggerBin(80.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.75, 0.207730893696, 0.368402425504),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0277777777778, 0.0103521665625),
                triggerBin(20.0, 0.048128342246, 0.0212069837314, 0.0155690574289),
                triggerBin(30.0, 0.0575539568345, 0.027159470536, 0.0196717116272),
                triggerBin(40.0, 0.120481927711, 0.0469494802123, 0.0363498571828),
                triggerBin(50.0, 0.139534883721, 0.0740357287102, 0.0539183163988),
                triggerBin(60.0, 0.263157894737, 0.138819970242, 0.108565019101),
                triggerBin(70.0, 0.166666666667, 0.287350389332, 0.138284918684),
                triggerBin(80.0, 0.333333333333, 0.282023462085, 0.211935221871),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.458641675296),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0, 0.458641675296),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0326086956522, 0.0130935946463),
                triggerBin(20.0, 0.0409836065574, 0.0267735739173, 0.0175899199367),
                triggerBin(30.0, 0.0652173913043, 0.0369226591417, 0.0255660522893),
                triggerBin(40.0, 0.121951219512, 0.0740833298519, 0.0516458433485),
                triggerBin(50.0, 0.194444444444, 0.0889424939268, 0.068790877801),
                triggerBin(60.0, 0.4, 0.204596854236, 0.180009253894),
                triggerBin(70.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(80.0, 0.75, 0.207730893696, 0.368402425504),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.5, 0.314698893873, 0.314698893873),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.029702970297, 0.00844620482067),
                triggerBin(20.0, 0.0333333333333, 0.0138841638885, 0.0102805804984),
                triggerBin(30.0, 0.0656565656566, 0.0226579362019, 0.0176574860501),
                triggerBin(40.0, 0.0825688073394, 0.0354288055604, 0.0264930657628),
                triggerBin(50.0, 0.151515151515, 0.0575785928796, 0.045333084157),
                triggerBin(60.0, 0.32, 0.119275761539, 0.102271514956),
                triggerBin(70.0, 0.5, 0.176478356266, 0.176478356266),
                triggerBin(80.0, 0.571428571429, 0.222487613116, 0.247840988275),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.6, 0.25334762525, 0.303366136254),
                triggerBin(140.0, 0.75, 0.207730893696, 0.368402425504),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0289634146341, 0.006547729923),
                triggerBin(20.0, 0.0390143737166, 0.0108791884278, 0.00876693170708),
                triggerBin(30.0, 0.0623145400593, 0.0161116856273, 0.0132265720972),
                triggerBin(40.0, 0.0989583333333, 0.0264833985093, 0.0218164532641),
                triggerBin(50.0, 0.146788990826, 0.0420419363152, 0.0347281303945),
                triggerBin(60.0, 0.295454545455, 0.0845305778572, 0.0738629419477),
                triggerBin(70.0, 0.388888888889, 0.145378985762, 0.130640004543),
                triggerBin(80.0, 0.461538461538, 0.172004084463, 0.164847322399),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.75, 0.159659347816, 0.239566802733),
                triggerBin(140.0, 0.75, 0.207730893696, 0.368402425504),
                triggerBin(160.0, 1.0, 0.0, 0.308024223477),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0713801671561, 0.00386948347881),
                triggerBin(20.0, 0.0875347948393, 0.00242999230557, 0.00242999230557),
                triggerBin(30.0, 0.12779593148, 0.00310759677527, 0.00310759677527),
                triggerBin(40.0, 0.165227600488, 0.00384645372189, 0.00384645372189),
                triggerBin(50.0, 0.211110029519, 0.00470708816865, 0.00470708816865),
                triggerBin(60.0, 0.277201538565, 0.00573888334312, 0.00573888334312),
                triggerBin(70.0, 0.325791411684, 0.00644502188738, 0.00644502188738),
                triggerBin(80.0, 0.523612791414, 0.00537055712606, 0.00537055712606),
                triggerBin(100.0, 0.75839578954, 0.00518336461487, 0.00518336461487),
                triggerBin(120.0, 0.908930722014, 0.00393892286999, 0.00393892286999),
                triggerBin(140.0, 0.979188340065, 0.00235849172762, 0.00235849172762),
                triggerBin(160.0, 0.999543254197, 0.000450791419081, 0.000450791419081),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0713801671561, 0.00386948347881),
                triggerBin(20.0, 0.0892449995673, 0.00266251647426, 0.00266251647426),
                triggerBin(30.0, 0.12758383742, 0.00335832080438, 0.00335832080438),
                triggerBin(40.0, 0.166275390355, 0.00418064182559, 0.00418064182559),
                triggerBin(50.0, 0.228873872465, 0.00529582562832, 0.00529582562832),
                triggerBin(60.0, 0.288901025537, 0.00627524168399, 0.00627524168399),
                triggerBin(70.0, 0.343343223578, 0.00713479562286, 0.00713479562286),
                triggerBin(80.0, 0.528346062801, 0.00593822942505, 0.00593822942505),
                triggerBin(100.0, 0.760284645242, 0.0057171104262, 0.0057171104262),
                triggerBin(120.0, 0.908428899151, 0.0043096104885, 0.0043096104885),
                triggerBin(140.0, 0.973993511854, 0.00285943450888, 0.00285943450888),
                triggerBin(160.0, 0.999304052153, 0.000613076748756, 0.000613076748756),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0713801671561, 0.00386948347881),
                triggerBin(20.0, 0.0887523139748, 0.00273347335255, 0.00273347335255),
                triggerBin(30.0, 0.127244419955, 0.00345096186931, 0.00345096186931),
                triggerBin(40.0, 0.167308571867, 0.00430540446948, 0.00430540446948),
                triggerBin(50.0, 0.222487813905, 0.00537521655392, 0.00537521655392),
                triggerBin(60.0, 0.288153344648, 0.00646319046249, 0.00646319046249),
                triggerBin(70.0, 0.34003976937, 0.0073018012087, 0.0073018012087),
                triggerBin(80.0, 0.529952379251, 0.0060614908439, 0.0060614908439),
                triggerBin(100.0, 0.760337731635, 0.00585280838637, 0.00585280838637),
                triggerBin(120.0, 0.907712195552, 0.00444190342626, 0.00444190342626),
                triggerBin(140.0, 0.974774229812, 0.00289967759061, 0.00289967759061),
                triggerBin(160.0, 0.999175585506, 0.000684310614961, 0.000684310614961),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0713801671561, 0.00386948347881),
                triggerBin(20.0, 0.0897868881342, 0.00307337703902, 0.00307337703902),
                triggerBin(30.0, 0.127297667247, 0.00385570897861, 0.00385570897861),
                triggerBin(40.0, 0.168709219182, 0.00481181807443, 0.00481181807443),
                triggerBin(50.0, 0.219166892712, 0.00596153928541, 0.00596153928541),
                triggerBin(60.0, 0.288388849204, 0.00722556979156, 0.00722556979156),
                triggerBin(70.0, 0.339612146918, 0.00814868468622, 0.00814868468622),
                triggerBin(80.0, 0.532092162453, 0.00672254934694, 0.00672254934694),
                triggerBin(100.0, 0.759763379594, 0.00652523413149, 0.00652523413149),
                triggerBin(120.0, 0.904925534039, 0.00503715902753, 0.00503715902753),
                triggerBin(140.0, 0.975164991233, 0.00322663206114, 0.00322663206114),
                triggerBin(160.0, 0.998931958133, 0.000859603064098, 0.000859603064098),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0713801671561, 0.00386948347881),
                triggerBin(20.0, 0.0889770545901, 0.00262698305986, 0.00262698305986),
                triggerBin(30.0, 0.127616894347, 0.00332061873569, 0.00332061873569),
                triggerBin(40.0, 0.166111852907, 0.00413002530854, 0.00413002530854),
                triggerBin(50.0, 0.2260616151, 0.00520438853728, 0.00520438853728),
                triggerBin(60.0, 0.287085979095, 0.00619387997656, 0.00619387997656),
                triggerBin(70.0, 0.340565589642, 0.00702876764563, 0.00702876764563),
                triggerBin(80.0, 0.527580813767, 0.00585034976414, 0.00585034976414),
                triggerBin(100.0, 0.759978484025, 0.0056347379783, 0.0056347379783),
                triggerBin(120.0, 0.908508356094, 0.0042529801003, 0.0042529801003),
                triggerBin(140.0, 0.974809273244, 0.00278108474612, 0.00278108474612),
                triggerBin(160.0, 0.999342410353, 0.00058745655086, 0.00058745655086),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0713801671561, 0.00386948347881),
                triggerBin(20.0, 0.0888527557245, 0.00268648658112, 0.00268648658112),
                triggerBin(30.0, 0.127410624683, 0.0033935099987, 0.0033935099987),
                triggerBin(40.0, 0.166775202563, 0.00422791893808, 0.00422791893808),
                triggerBin(50.0, 0.224078869268, 0.00530043523628, 0.00530043523628),
                triggerBin(60.0, 0.287676008252, 0.00634407890709, 0.00634407890709),
                triggerBin(70.0, 0.340273884274, 0.00718148938302, 0.00718148938302),
                triggerBin(80.0, 0.528898521276, 0.00596867240618, 0.00596867240618),
                triggerBin(100.0, 0.760177998928, 0.00575672238204, 0.00575672238204),
                triggerBin(120.0, 0.908067402972, 0.0043583155395, 0.0043583155395),
                triggerBin(140.0, 0.974789790081, 0.00284726844573, 0.00284726844573),
                triggerBin(160.0, 0.999250144813, 0.000641492334854, 0.000641492334854),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0713801671561, 0.00386948347881),
                triggerBin(20.0, 0.0897868881342, 0.00307337703902, 0.00307337703902),
                triggerBin(30.0, 0.127297667247, 0.00385570897861, 0.00385570897861),
                triggerBin(40.0, 0.168709219182, 0.00481181807443, 0.00481181807443),
                triggerBin(50.0, 0.219166892712, 0.00596153928541, 0.00596153928541),
                triggerBin(60.0, 0.288388849204, 0.00722556979156, 0.00722556979156),
                triggerBin(70.0, 0.339612146918, 0.00814868468622, 0.00814868468622),
                triggerBin(80.0, 0.532092162453, 0.00672254934694, 0.00672254934694),
                triggerBin(100.0, 0.759763379594, 0.00652523413149, 0.00652523413149),
                triggerBin(120.0, 0.904925534039, 0.00503715902753, 0.00503715902753),
                triggerBin(140.0, 0.975164991233, 0.00322663206114, 0.00322663206114),
                triggerBin(160.0, 0.998931958133, 0.000859603064098, 0.000859603064098),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0713801671561, 0.00386948347881),
                triggerBin(20.0, 0.0956925457828, 0.0049606327822, 0.00474640112493),
                triggerBin(30.0, 0.129483814523, 0.00598980060703, 0.00576823280346),
                triggerBin(40.0, 0.17982300885, 0.00751781874278, 0.00728563988648),
                triggerBin(50.0, 0.225472547255, 0.00921544625635, 0.00896214243757),
                triggerBin(60.0, 0.305693753455, 0.0112154901569, 0.0109952605068),
                triggerBin(70.0, 0.364713627386, 0.0127669182855, 0.0125841188304),
                triggerBin(80.0, 0.547297297297, 0.0101009725176, 0.0101393133521),
                triggerBin(100.0, 0.761146496815, 0.00994432928726, 0.0102289543957),
                triggerBin(120.0, 0.891838088918, 0.00806163943347, 0.00860302993962),
                triggerBin(140.0, 0.966085271318, 0.00563756565474, 0.00661806188887),
                triggerBin(160.0, 0.997093023256, 0.00187741885377, 0.0038211848045),
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

    # Used input: multicrab_MetLeg2012_130517_110812

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.142857142857, 0.132260014253),
                triggerBin(20.0, 0.142857142857, 0.257123832984, 0.118480071045),
                triggerBin(30.0, 0.0, 0.458641675296, 0.0),
                triggerBin(40.0, 0.0, 0.841344746068, 0.0),
                triggerBin(50.0, 0.5, 0.41724846474, 0.41724846474),
                triggerBin(60.0, 0.0, 1.0, 0.0),
                triggerBin(70.0, 1.0, 0.0, 0.601684479424),
                triggerBin(80.0, 0.0, 1.0, 0.0),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0388349514563, 0.0190367039454),
                triggerBin(20.0, 0.041095890411, 0.0383632915283, 0.0222832479104),
                triggerBin(30.0, 0.111111111111, 0.060467252805, 0.0431774157972),
                triggerBin(40.0, 0.142857142857, 0.119718786455, 0.0767053610655),
                triggerBin(50.0, 0.176470588235, 0.142402653848, 0.0944266759714),
                triggerBin(60.0, 0.285714285714, 0.259937875571, 0.182129028008),
                triggerBin(70.0, 0.0, 0.841344746068, 0.0),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.024, 0.0136891197672),
                triggerBin(20.0, 0.0380952380952, 0.0290965667789, 0.0181439734408),
                triggerBin(30.0, 0.0545454545455, 0.0502231762716, 0.0295392531338),
                triggerBin(40.0, 0.0789473684211, 0.0708737003562, 0.0426562617902),
                triggerBin(50.0, 0.15, 0.12471137336, 0.0804822604739),
                triggerBin(60.0, 0.222222222222, 0.221429368878, 0.14211823823),
                triggerBin(70.0, 0.428571428571, 0.247840988275, 0.222487613116),
                triggerBin(80.0, 0.5, 0.41724846474, 0.41724846474),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 1.0, 0.0, 0.458641675296),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0243902439024, 0.012045482886),
                triggerBin(20.0, 0.0373831775701, 0.0285714611425, 0.0178064693186),
                triggerBin(30.0, 0.027397260274, 0.0349950540934, 0.0176764535746),
                triggerBin(40.0, 0.139534883721, 0.0740357287102, 0.0539183163988),
                triggerBin(50.0, 0.227272727273, 0.124519809699, 0.0944237146768),
                triggerBin(60.0, 0.3, 0.20826248199, 0.158328098893),
                triggerBin(70.0, 0.0, 0.36887757085, 0.0),
                triggerBin(80.0, 0.25, 0.368402425504, 0.207730893696),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.458641675296),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0454545454545, 0.0198605203978),
                triggerBin(20.0, 0.05, 0.0377701577881, 0.0237772015406),
                triggerBin(30.0, 0.105263157895, 0.0575793515833, 0.0409515011174),
                triggerBin(40.0, 0.136363636364, 0.11509911457, 0.0732667013517),
                triggerBin(50.0, 0.210526315789, 0.135427055903, 0.0978662361907),
                triggerBin(60.0, 0.285714285714, 0.259937875571, 0.182129028008),
                triggerBin(70.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.5, 0.314698893873, 0.314698893873),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0340425531915, 0.0118292205394),
                triggerBin(20.0, 0.0432432432432, 0.0206352522007, 0.0148268522389),
                triggerBin(30.0, 0.0803571428571, 0.0345395679156, 0.0257971733075),
                triggerBin(40.0, 0.1, 0.0549521822688, 0.0389435688158),
                triggerBin(50.0, 0.179487179487, 0.083232543249, 0.0637222991994),
                triggerBin(60.0, 0.25, 0.153966037382, 0.115498745679),
                triggerBin(70.0, 0.5, 0.195182116991, 0.195182116991),
                triggerBin(80.0, 0.75, 0.207730893696, 0.368402425504),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.6, 0.25334762525, 0.303366136254),
                triggerBin(140.0, 1.0, 0.0, 0.458641675296),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0300751879699, 0.00855040649468),
                triggerBin(20.0, 0.041095890411, 0.015171386274, 0.0115726923966),
                triggerBin(30.0, 0.0594594594595, 0.0228734949597, 0.0173900908681),
                triggerBin(40.0, 0.116504854369, 0.0406717229099, 0.032137201422),
                triggerBin(50.0, 0.196721311475, 0.0644002380547, 0.052982621917),
                triggerBin(60.0, 0.269230769231, 0.114603025448, 0.0935066525113),
                triggerBin(70.0, 0.357142857143, 0.169219923607, 0.144430653909),
                triggerBin(80.0, 0.5, 0.220457375638, 0.220457375638),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.75, 0.159659347816, 0.239566802733),
                triggerBin(140.0, 1.0, 0.0, 0.458641675296),
                triggerBin(160.0, 1.0, 0.0, 0.36887757085),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.069537592658, 0.00477898815679),
                triggerBin(20.0, 0.0864158334372, 0.00302200528312, 0.00302200528312),
                triggerBin(30.0, 0.116296761311, 0.00369304873348, 0.00369304873348),
                triggerBin(40.0, 0.158955154441, 0.00455480514529, 0.00455480514529),
                triggerBin(50.0, 0.210055637283, 0.00565278599995, 0.00565278599995),
                triggerBin(60.0, 0.275699626719, 0.00678341673231, 0.00678341673231),
                triggerBin(70.0, 0.326078687777, 0.0074923003167, 0.0074923003167),
                triggerBin(80.0, 0.536860390249, 0.00623418092545, 0.00623418092545),
                triggerBin(100.0, 0.761908758206, 0.00587114191832, 0.00587114191832),
                triggerBin(120.0, 0.906714487996, 0.00450126653197, 0.00450126653197),
                triggerBin(140.0, 0.974576818531, 0.0029464708433, 0.0029464708433),
                triggerBin(160.0, 0.99943173122, 0.000560829232942, 0.000560829232942),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.069537592658, 0.00477898815679),
                triggerBin(20.0, 0.0896620684014, 0.00332347323634, 0.00332347323634),
                triggerBin(30.0, 0.114550324845, 0.0039692576028, 0.0039692576028),
                triggerBin(40.0, 0.160049342997, 0.00497246154723, 0.00497246154723),
                triggerBin(50.0, 0.227888041603, 0.006307593584, 0.006307593584),
                triggerBin(60.0, 0.283737559473, 0.00731187998874, 0.00731187998874),
                triggerBin(70.0, 0.345608068715, 0.00829202699426, 0.00829202699426),
                triggerBin(80.0, 0.54079707064, 0.00687796109166, 0.00687796109166),
                triggerBin(100.0, 0.759198672486, 0.00651865765667, 0.00651865765667),
                triggerBin(120.0, 0.901992060419, 0.00505331328123, 0.00505331328123),
                triggerBin(140.0, 0.968895941402, 0.00352554564848, 0.00352554564848),
                triggerBin(160.0, 0.999109874629, 0.000784018927601, 0.000784018927601),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.069537592658, 0.00477898815679),
                triggerBin(20.0, 0.0884246317624, 0.00340769651436, 0.00340769651436),
                triggerBin(30.0, 0.115079237073, 0.00409090146199, 0.00409090146199),
                triggerBin(40.0, 0.161072981827, 0.0051122253442, 0.0051122253442),
                triggerBin(50.0, 0.221153972019, 0.00642094927523, 0.00642094927523),
                triggerBin(60.0, 0.283730232489, 0.00757000990307, 0.00757000990307),
                triggerBin(70.0, 0.341785185364, 0.00850096196345, 0.00850096196345),
                triggerBin(80.0, 0.542990202644, 0.00702056920227, 0.00702056920227),
                triggerBin(100.0, 0.760535745789, 0.00666338865136, 0.00666338865136),
                triggerBin(120.0, 0.9031132409, 0.00514804136413, 0.00514804136413),
                triggerBin(140.0, 0.970059251853, 0.0035655512699, 0.0035655512699),
                triggerBin(160.0, 0.998953679534, 0.000868408662905, 0.000868408662905),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.069537592658, 0.00477898815679),
                triggerBin(20.0, 0.0890348509697, 0.00383125129605, 0.00383125129605),
                triggerBin(30.0, 0.116007900618, 0.00458016080603, 0.00458016080603),
                triggerBin(40.0, 0.161643047037, 0.00569516054683, 0.00569516054683),
                triggerBin(50.0, 0.216832162363, 0.00710779515533, 0.00710779515533),
                triggerBin(60.0, 0.284154112395, 0.00847909705053, 0.00847909705053),
                triggerBin(70.0, 0.338695415932, 0.00946784985271, 0.00946784985271),
                triggerBin(80.0, 0.544338989208, 0.00778064857573, 0.00778064857573),
                triggerBin(100.0, 0.760448604901, 0.00741759382625, 0.00741759382625),
                triggerBin(120.0, 0.901627049292, 0.00578594450954, 0.00578594450954),
                triggerBin(140.0, 0.971422251711, 0.0039125750901, 0.0039125750901),
                triggerBin(160.0, 0.998647068727, 0.00108880284735, 0.00108880284735),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.069537592658, 0.00477898815679),
                triggerBin(20.0, 0.0891570947765, 0.00327737383637, 0.00327737383637),
                triggerBin(30.0, 0.114822161467, 0.00392806515557, 0.00392806515557),
                triggerBin(40.0, 0.159877299724, 0.00490884332908, 0.00490884332908),
                triggerBin(50.0, 0.225105365185, 0.00620714129306, 0.00620714129306),
                triggerBin(60.0, 0.282512850901, 0.00723296548294, 0.00723296548294),
                triggerBin(70.0, 0.34252552073, 0.00816939156646, 0.00816939156646),
                triggerBin(80.0, 0.540162989621, 0.00677857027865, 0.00677857027865),
                triggerBin(100.0, 0.759636898599, 0.00641788523952, 0.00641788523952),
                triggerBin(120.0, 0.902745554304, 0.00496687212939, 0.00496687212939),
                triggerBin(140.0, 0.969784424485, 0.00343528966004, 0.00343528966004),
                triggerBin(160.0, 0.999162765886, 0.00074787438913, 0.00074787438913),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.069537592658, 0.00477898815679),
                triggerBin(20.0, 0.0887524925807, 0.00335025145547, 0.00335025145547),
                triggerBin(30.0, 0.114964563245, 0.00401899783643, 0.00401899783643),
                triggerBin(40.0, 0.160540781585, 0.00502244569445, 0.00502244569445),
                triggerBin(50.0, 0.222917594833, 0.00632726025508, 0.00632726025508),
                triggerBin(60.0, 0.283184512348, 0.00742057747597, 0.00742057747597),
                triggerBin(70.0, 0.342115809282, 0.00835465542417, 0.00835465542417),
                triggerBin(80.0, 0.541734640589, 0.006914230419, 0.006914230419),
                triggerBin(100.0, 0.760135111031, 0.00655526670023, 0.00655526670023),
                triggerBin(120.0, 0.902949267385, 0.00506837417656, 0.00506837417656),
                triggerBin(140.0, 0.969936364016, 0.00350823112911, 0.00350823112911),
                triggerBin(160.0, 0.999046880089, 0.000815227138645, 0.000815227138645),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.069537592658, 0.00477898815679),
                triggerBin(20.0, 0.0890348509697, 0.00383125129605, 0.00383125129605),
                triggerBin(30.0, 0.116007900618, 0.00458016080603, 0.00458016080603),
                triggerBin(40.0, 0.161643047037, 0.00569516054683, 0.00569516054683),
                triggerBin(50.0, 0.216832162363, 0.00710779515533, 0.00710779515533),
                triggerBin(60.0, 0.284154112395, 0.00847909705053, 0.00847909705053),
                triggerBin(70.0, 0.338695415932, 0.00946784985271, 0.00946784985271),
                triggerBin(80.0, 0.544338989208, 0.00778064857573, 0.00778064857573),
                triggerBin(100.0, 0.760448604901, 0.00741759382625, 0.00741759382625),
                triggerBin(120.0, 0.901627049292, 0.00578594450954, 0.00578594450954),
                triggerBin(140.0, 0.971422251711, 0.0039125750901, 0.0039125750901),
                triggerBin(160.0, 0.998647068727, 0.00108880284735, 0.00108880284735),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.069537592658, 0.00477898815679),
                triggerBin(20.0, 0.0948905109489, 0.00627442551239, 0.00593465459532),
                triggerBin(30.0, 0.120407259849, 0.00724165694566, 0.00689480687188),
                triggerBin(40.0, 0.16975308642, 0.00894556745468, 0.00859564845038),
                triggerBin(50.0, 0.221086261981, 0.0109903454171, 0.0106231897456),
                triggerBin(60.0, 0.297052154195, 0.0130945918882, 0.0127787081678),
                triggerBin(70.0, 0.355614973262, 0.0148629966115, 0.014597745258),
                triggerBin(80.0, 0.553372278279, 0.0116899979066, 0.011747981498),
                triggerBin(100.0, 0.758339006127, 0.0113253596899, 0.0116876509342),
                triggerBin(120.0, 0.891047297297, 0.00913170257673, 0.00982273441786),
                triggerBin(140.0, 0.96379525593, 0.0066028560395, 0.00786963421827),
                triggerBin(160.0, 0.996268656716, 0.00240974151247, 0.00490010828149),
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

    # Used input: multicrab_MetLeg2012_130517_110812

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.2, 0.1788854382),
                triggerBin(20.0, 0.166666666667, 0.287350389332, 0.138284918684),
                triggerBin(30.0, 0.0, 0.458641675296, 0.0),
                triggerBin(40.0, 0.0, 0.841344746068, 0.0),
                triggerBin(50.0, 0.5, 0.41724846474, 0.41724846474),
                triggerBin(60.0, 0.0, 1.0, 0.0),
                triggerBin(70.0, 1.0, 0.0, 0.601684479424),
                triggerBin(80.0, 0.0, 1.0, 0.0),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0449438202247, 0.0219611181558),
                triggerBin(20.0, 0.0454545454545, 0.0422441218236, 0.0246367510149),
                triggerBin(30.0, 0.102040816327, 0.06313660811, 0.0433605078476),
                triggerBin(40.0, 0.176470588235, 0.142402653848, 0.0944266759714),
                triggerBin(50.0, 0.153846153846, 0.16803608658, 0.0987133108909),
                triggerBin(60.0, 0.285714285714, 0.259937875571, 0.182129028008),
                triggerBin(70.0, 0.0, 0.841344746068, 0.0),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.0, 0.601684479424, 0.0),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0285714285714, 0.0162583610844),
                triggerBin(20.0, 0.0430107526882, 0.0327020485265, 0.0204721109128),
                triggerBin(30.0, 0.0566037735849, 0.0520081635621, 0.0306480760549),
                triggerBin(40.0, 0.0857142857143, 0.0764033060045, 0.0462826358375),
                triggerBin(50.0, 0.1875, 0.149398565056, 0.100212028831),
                triggerBin(60.0, 0.222222222222, 0.221429368878, 0.14211823823),
                triggerBin(70.0, 0.428571428571, 0.247840988275, 0.222487613116),
                triggerBin(80.0, 0.0, 0.841344746068, 0.0),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 1.0, 0.0, 0.601684479424),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0283687943262, 0.013981752504),
                triggerBin(20.0, 0.0309278350515, 0.02917029971, 0.0167854408748),
                triggerBin(30.0, 0.03125, 0.0397347958314, 0.0201590096415),
                triggerBin(40.0, 0.142857142857, 0.0755708996607, 0.0551651552867),
                triggerBin(50.0, 0.263157894737, 0.138819970242, 0.108565019101),
                triggerBin(60.0, 0.3, 0.20826248199, 0.158328098893),
                triggerBin(70.0, 0.0, 0.36887757085, 0.0),
                triggerBin(80.0, 0.25, 0.368402425504, 0.207730893696),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.458641675296),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0531914893617, 0.0231466542826),
                triggerBin(20.0, 0.0555555555556, 0.0417497559944, 0.0263999125929),
                triggerBin(30.0, 0.0961538461538, 0.0598141322187, 0.0408993528538),
                triggerBin(40.0, 0.166666666667, 0.135998901491, 0.0892717907981),
                triggerBin(50.0, 0.2, 0.157061286074, 0.10675070638),
                triggerBin(60.0, 0.285714285714, 0.259937875571, 0.182129028008),
                triggerBin(70.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0402010050251, 0.013924578649),
                triggerBin(20.0, 0.0484848484848, 0.0230425188578, 0.0166050238729),
                triggerBin(30.0, 0.0761904761905, 0.0354276947868, 0.0259335520675),
                triggerBin(40.0, 0.11320754717, 0.0614945435373, 0.0439740652089),
                triggerBin(50.0, 0.193548387097, 0.0976717076465, 0.0739582576944),
                triggerBin(60.0, 0.25, 0.153966037382, 0.115498745679),
                triggerBin(70.0, 0.5, 0.195182116991, 0.195182116991),
                triggerBin(80.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.5, 0.314698893873, 0.314698893873),
                triggerBin(140.0, 1.0, 0.0, 0.601684479424),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0352941176471, 0.0100071214211),
                triggerBin(20.0, 0.0419847328244, 0.0163593089914, 0.0123344208872),
                triggerBin(30.0, 0.0591715976331, 0.0241779086556, 0.0181345594478),
                triggerBin(40.0, 0.126315789474, 0.0437638281678, 0.0347456906981),
                triggerBin(50.0, 0.22, 0.0744257803206, 0.0614915858722),
                triggerBin(60.0, 0.269230769231, 0.114603025448, 0.0935066525113),
                triggerBin(70.0, 0.357142857143, 0.169219923607, 0.144430653909),
                triggerBin(80.0, 0.428571428571, 0.247840988275, 0.222487613116),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.714285714286, 0.182129028008, 0.259937875571),
                triggerBin(140.0, 1.0, 0.0, 0.601684479424),
                triggerBin(160.0, 1.0, 0.0, 0.36887757085),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0671731307477, 0.00500543092708),
                triggerBin(20.0, 0.0796752027601, 0.00311042188254, 0.00311042188254),
                triggerBin(30.0, 0.118120402442, 0.00396630530953, 0.00396630530953),
                triggerBin(40.0, 0.147425568524, 0.00463710197644, 0.00463710197644),
                triggerBin(50.0, 0.205914785861, 0.00591137669387, 0.00591137669387),
                triggerBin(60.0, 0.279981158912, 0.00713264437936, 0.00713264437936),
                triggerBin(70.0, 0.3345239887, 0.00787497245909, 0.00787497245909),
                triggerBin(80.0, 0.537454925052, 0.00645481323843, 0.00645481323843),
                triggerBin(100.0, 0.757283629929, 0.00619408539891, 0.00619408539891),
                triggerBin(120.0, 0.903908916427, 0.00474528547003, 0.00474528547003),
                triggerBin(140.0, 0.97313254983, 0.00315774209545, 0.00315774209545),
                triggerBin(160.0, 0.999368363591, 0.000623384597569, 0.000623384597569),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0671731307477, 0.00500543092708),
                triggerBin(20.0, 0.0824264629889, 0.00342459346069, 0.00342459346069),
                triggerBin(30.0, 0.118198949983, 0.00431669390501, 0.00431669390501),
                triggerBin(40.0, 0.148633277572, 0.00509188606913, 0.00509188606913),
                triggerBin(50.0, 0.224625896026, 0.00661407599502, 0.00661407599502),
                triggerBin(60.0, 0.284047454338, 0.00764475076972, 0.00764475076972),
                triggerBin(70.0, 0.350993140176, 0.00868263340175, 0.00868263340175),
                triggerBin(80.0, 0.541428091108, 0.00713213023353, 0.00713213023353),
                triggerBin(100.0, 0.755775760301, 0.00690502071506, 0.00690502071506),
                triggerBin(120.0, 0.903295027036, 0.00522417395742, 0.00522417395742),
                triggerBin(140.0, 0.966328212897, 0.00385555097467, 0.00385555097467),
                triggerBin(160.0, 0.999016995541, 0.000865765721094, 0.000865765721094),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0671731307477, 0.00500543092708),
                triggerBin(20.0, 0.0817577846258, 0.00351478044527, 0.00351478044527),
                triggerBin(30.0, 0.118022575768, 0.00442844619549, 0.00442844619549),
                triggerBin(40.0, 0.150129680338, 0.0052360865289, 0.0052360865289),
                triggerBin(50.0, 0.218138848122, 0.00673908631627, 0.00673908631627),
                triggerBin(60.0, 0.285337421285, 0.00793063844592, 0.00793063844592),
                triggerBin(70.0, 0.347493415247, 0.00890337215602, 0.00890337215602),
                triggerBin(80.0, 0.543424257405, 0.00727459958297, 0.00727459958297),
                triggerBin(100.0, 0.757365485682, 0.00704583123492, 0.00704583123492),
                triggerBin(120.0, 0.903007049294, 0.00535705707482, 0.00535705707482),
                triggerBin(140.0, 0.967981582813, 0.0038647188987, 0.0038647188987),
                triggerBin(160.0, 0.998840177562, 0.000962597077485, 0.000962597077485),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0671731307477, 0.00500543092708),
                triggerBin(20.0, 0.0834368485116, 0.00397373751002, 0.00397373751002),
                triggerBin(30.0, 0.11855627592, 0.00494177185146, 0.00494177185146),
                triggerBin(40.0, 0.152181023807, 0.0058509260066, 0.0058509260066),
                triggerBin(50.0, 0.213791376043, 0.00746560402068, 0.00746560402068),
                triggerBin(60.0, 0.286819080418, 0.00890044274807, 0.00890044274807),
                triggerBin(70.0, 0.343336519412, 0.00991319734091, 0.00991319734091),
                triggerBin(80.0, 0.544211055131, 0.00806762752062, 0.00806762752062),
                triggerBin(100.0, 0.757721490476, 0.00783078101241, 0.00783078101241),
                triggerBin(120.0, 0.899556829103, 0.00608318365347, 0.00608318365347),
                triggerBin(140.0, 0.96972813122, 0.00421398533206, 0.00421398533206),
                triggerBin(160.0, 0.998505353008, 0.00120267137131, 0.00120267137131),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0671731307477, 0.00500543092708),
                triggerBin(20.0, 0.0819968091437, 0.00337643835073, 0.00337643835073),
                triggerBin(30.0, 0.118186627691, 0.00426352148793, 0.00426352148793),
                triggerBin(40.0, 0.148441662629, 0.00502209526029, 0.00502209526029),
                triggerBin(50.0, 0.221703716822, 0.00650616252275, 0.00650616252275),
                triggerBin(60.0, 0.283429344576, 0.00756863273305, 0.00756863273305),
                triggerBin(70.0, 0.348397704892, 0.00855898582936, 0.00855898582936),
                triggerBin(80.0, 0.540786603392, 0.00702735982628, 0.00702735982628),
                triggerBin(100.0, 0.756022438465, 0.00679376830445, 0.00679376830445),
                triggerBin(120.0, 0.903392916866, 0.00515042784948, 0.00515042784948),
                triggerBin(140.0, 0.96740812876, 0.00374524756624, 0.00374524756624),
                triggerBin(160.0, 0.999074407345, 0.000826765681594, 0.000826765681594),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0671731307477, 0.00500543092708),
                triggerBin(20.0, 0.081864630211, 0.00345371804345, 0.00345371804345),
                triggerBin(30.0, 0.118095728317, 0.00435578368535, 0.00435578368535),
                triggerBin(40.0, 0.149378794645, 0.00514157332667, 0.00514157332667),
                triggerBin(50.0, 0.219731537015, 0.00663687245124, 0.00663687245124),
                triggerBin(60.0, 0.284481597541, 0.00776999998514, 0.00776999998514),
                triggerBin(70.0, 0.347896979061, 0.00875145323111, 0.00875145323111),
                triggerBin(80.0, 0.542253245107, 0.00716599902222, 0.00716599902222),
                triggerBin(100.0, 0.756766504277, 0.00693493744708, 0.00693493744708),
                triggerBin(120.0, 0.903178865862, 0.00526592061148, 0.00526592061148),
                triggerBin(140.0, 0.967725647553, 0.00381251408796, 0.00381251408796),
                triggerBin(160.0, 0.998944783181, 0.000902587680916, 0.000902587680916),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0671731307477, 0.00500543092708),
                triggerBin(20.0, 0.0834368485116, 0.00397373751002, 0.00397373751002),
                triggerBin(30.0, 0.11855627592, 0.00494177185146, 0.00494177185146),
                triggerBin(40.0, 0.152181023807, 0.0058509260066, 0.0058509260066),
                triggerBin(50.0, 0.213791376043, 0.00746560402068, 0.00746560402068),
                triggerBin(60.0, 0.286819080418, 0.00890044274807, 0.00890044274807),
                triggerBin(70.0, 0.343336519412, 0.00991319734091, 0.00991319734091),
                triggerBin(80.0, 0.544211055131, 0.00806762752062, 0.00806762752062),
                triggerBin(100.0, 0.757721490476, 0.00783078101241, 0.00783078101241),
                triggerBin(120.0, 0.899556829103, 0.00608318365347, 0.00608318365347),
                triggerBin(140.0, 0.96972813122, 0.00421398533206, 0.00421398533206),
                triggerBin(160.0, 0.998505353008, 0.00120267137131, 0.00120267137131),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0671731307477, 0.00500543092708),
                triggerBin(20.0, 0.0909930715935, 0.0066082613939, 0.00621640429117),
                triggerBin(30.0, 0.123799898939, 0.00785233589165, 0.00745928027462),
                triggerBin(40.0, 0.16628440367, 0.00939860348414, 0.0090037273104),
                triggerBin(50.0, 0.221586847748, 0.011663397801, 0.0112527445037),
                triggerBin(60.0, 0.297658862876, 0.0138084517895, 0.0134595668721),
                triggerBin(70.0, 0.355685131195, 0.0155469694362, 0.0152575138869),
                triggerBin(80.0, 0.552752293578, 0.0121581847279, 0.0122201154543),
                triggerBin(100.0, 0.758490566038, 0.0119304741341, 0.0123329882461),
                triggerBin(120.0, 0.886216466235, 0.00974604324589, 0.0104944261508),
                triggerBin(140.0, 0.962861072902, 0.00701575904016, 0.00841299435296),
                triggerBin(160.0, 0.99593495935, 0.00262521168387, 0.0053362590053),
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

    # Used input: multicrab_MetLeg2012_130517_110812

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0666666666667, 0.0644061188719),
                triggerBin(20.0, 0.0909090909091, 0.179295209474, 0.0753268806181),
                triggerBin(30.0, 0.0, 0.36887757085, 0.0),
                triggerBin(40.0, 0.0, 0.841344746068, 0.0),
                triggerBin(50.0, 0.5, 0.41724846474, 0.41724846474),
                triggerBin(60.0, 0.0, 1.0, 0.0),
                triggerBin(70.0, 1.0, 0.0, 0.601684479424),
                triggerBin(80.0, 0.0, 1.0, 0.0),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0295857988166, 0.0130339745683),
                triggerBin(20.0, 0.036036036036, 0.0275760676929, 0.0171677750461),
                triggerBin(30.0, 0.0681818181818, 0.0385044118677, 0.0267133636922),
                triggerBin(40.0, 0.125, 0.0757199817448, 0.0529092136612),
                triggerBin(50.0, 0.176470588235, 0.0905039073753, 0.0676761749045),
                triggerBin(60.0, 0.4, 0.204596854236, 0.180009253894),
                triggerBin(70.0, 0.0, 0.841344746068, 0.0),
                triggerBin(80.0, 0.75, 0.207730893696, 0.368402425504),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0272727272727, 0.0109811668572),
                triggerBin(20.0, 0.0280898876404, 0.0185555038223, 0.0120805355016),
                triggerBin(30.0, 0.0660377358491, 0.0337580471231, 0.0240344740711),
                triggerBin(40.0, 0.0588235294118, 0.0440704816426, 0.0279408462558),
                triggerBin(50.0, 0.1, 0.0877974084544, 0.0539221516634),
                triggerBin(60.0, 0.266666666667, 0.161145049639, 0.122866921165),
                triggerBin(70.0, 0.444444444444, 0.213462824948, 0.198267144951),
                triggerBin(80.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.75, 0.207730893696, 0.368402425504),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0277777777778, 0.0103521665625),
                triggerBin(20.0, 0.048128342246, 0.0212069837314, 0.0155690574289),
                triggerBin(30.0, 0.0575539568345, 0.027159470536, 0.0196717116272),
                triggerBin(40.0, 0.120481927711, 0.0469494802123, 0.0363498571828),
                triggerBin(50.0, 0.139534883721, 0.0740357287102, 0.0539183163988),
                triggerBin(60.0, 0.263157894737, 0.138819970242, 0.108565019101),
                triggerBin(70.0, 0.166666666667, 0.287350389332, 0.138284918684),
                triggerBin(80.0, 0.333333333333, 0.282023462085, 0.211935221871),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.458641675296),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0, 0.458641675296),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0326086956522, 0.0130935946463),
                triggerBin(20.0, 0.0409836065574, 0.0267735739173, 0.0175899199367),
                triggerBin(30.0, 0.0652173913043, 0.0369226591417, 0.0255660522893),
                triggerBin(40.0, 0.121951219512, 0.0740833298519, 0.0516458433485),
                triggerBin(50.0, 0.194444444444, 0.0889424939268, 0.068790877801),
                triggerBin(60.0, 0.4, 0.204596854236, 0.180009253894),
                triggerBin(70.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(80.0, 0.75, 0.207730893696, 0.368402425504),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.5, 0.314698893873, 0.314698893873),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.029702970297, 0.00844620482067),
                triggerBin(20.0, 0.0333333333333, 0.0138841638885, 0.0102805804984),
                triggerBin(30.0, 0.0656565656566, 0.0226579362019, 0.0176574860501),
                triggerBin(40.0, 0.0825688073394, 0.0354288055604, 0.0264930657628),
                triggerBin(50.0, 0.151515151515, 0.0575785928796, 0.045333084157),
                triggerBin(60.0, 0.32, 0.119275761539, 0.102271514956),
                triggerBin(70.0, 0.5, 0.176478356266, 0.176478356266),
                triggerBin(80.0, 0.571428571429, 0.222487613116, 0.247840988275),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.6, 0.25334762525, 0.303366136254),
                triggerBin(140.0, 0.75, 0.207730893696, 0.368402425504),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0289634146341, 0.006547729923),
                triggerBin(20.0, 0.0390143737166, 0.0108791884278, 0.00876693170708),
                triggerBin(30.0, 0.0623145400593, 0.0161116856273, 0.0132265720972),
                triggerBin(40.0, 0.0989583333333, 0.0264833985093, 0.0218164532641),
                triggerBin(50.0, 0.146788990826, 0.0420419363152, 0.0347281303945),
                triggerBin(60.0, 0.295454545455, 0.0845305778572, 0.0738629419477),
                triggerBin(70.0, 0.388888888889, 0.145378985762, 0.130640004543),
                triggerBin(80.0, 0.461538461538, 0.172004084463, 0.164847322399),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.75, 0.159659347816, 0.239566802733),
                triggerBin(140.0, 0.75, 0.207730893696, 0.368402425504),
                triggerBin(160.0, 1.0, 0.0, 0.308024223477),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0712669683258, 0.00386971030144),
                triggerBin(20.0, 0.0872721238384, 0.00242882205139, 0.00242882205139),
                triggerBin(30.0, 0.126994030451, 0.00310564287951, 0.00310564287951),
                triggerBin(40.0, 0.163781429374, 0.0038435978886, 0.0038435978886),
                triggerBin(50.0, 0.212003208379, 0.00472603752037, 0.00472603752037),
                triggerBin(60.0, 0.276034534619, 0.00574336809577, 0.00574336809577),
                triggerBin(70.0, 0.324853249501, 0.00644469208608, 0.00644469208608),
                triggerBin(80.0, 0.520922745989, 0.00538708524721, 0.00538708524721),
                triggerBin(100.0, 0.757175988723, 0.00520534063343, 0.00520534063343),
                triggerBin(120.0, 0.908930713679, 0.00393892321469, 0.00393892321469),
                triggerBin(140.0, 0.979183753972, 0.00235900592452, 0.00235900592452),
                triggerBin(160.0, 0.999539104712, 0.000454885865248, 0.000454885865248),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0712669683258, 0.00386971030144),
                triggerBin(20.0, 0.0890866621567, 0.00266319131654, 0.00266319131654),
                triggerBin(30.0, 0.127206789864, 0.00336242682648, 0.00336242682648),
                triggerBin(40.0, 0.164951627437, 0.00417674887718, 0.00417674887718),
                triggerBin(50.0, 0.229382701288, 0.00531205308671, 0.00531205308671),
                triggerBin(60.0, 0.287959989946, 0.00628032901457, 0.00628032901457),
                triggerBin(70.0, 0.342502798719, 0.00713531732437, 0.00713531732437),
                triggerBin(80.0, 0.525653167847, 0.00595808145986, 0.00595808145986),
                triggerBin(100.0, 0.759196449456, 0.00573895055714, 0.00573895055714),
                triggerBin(120.0, 0.908426967823, 0.00430969435415, 0.00430969435415),
                triggerBin(140.0, 0.973983449102, 0.00286052613987, 0.00286052613987),
                triggerBin(160.0, 0.999299237065, 0.000617287727595, 0.000617287727595),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0712669683258, 0.00386971030144),
                triggerBin(20.0, 0.088534271484, 0.00273335334984, 0.00273335334984),
                triggerBin(30.0, 0.126764209171, 0.0034532453211, 0.0034532453211),
                triggerBin(40.0, 0.165880920872, 0.00430112113888, 0.00430112113888),
                triggerBin(50.0, 0.223051784108, 0.00539338780521, 0.00539338780521),
                triggerBin(60.0, 0.28713837204, 0.00646880826819, 0.00646880826819),
                triggerBin(70.0, 0.339083711229, 0.00730235984546, 0.00730235984546),
                triggerBin(80.0, 0.527381055957, 0.00608106742176, 0.00608106742176),
                triggerBin(100.0, 0.759203878929, 0.00587611595575, 0.00587611595575),
                triggerBin(120.0, 0.90770700349, 0.00444214589454, 0.00444214589454),
                triggerBin(140.0, 0.974763316572, 0.00290091581789, 0.00290091581789),
                triggerBin(160.0, 0.999169746049, 0.000689155680278, 0.000689155680278),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0712669683258, 0.00386971030144),
                triggerBin(20.0, 0.0895284158136, 0.0030725920564, 0.0030725920564),
                triggerBin(30.0, 0.126673647249, 0.0038552061611, 0.0038552061611),
                triggerBin(40.0, 0.167200982945, 0.00480684409468, 0.00480684409468),
                triggerBin(50.0, 0.219398345112, 0.00597858469902, 0.00597858469902),
                triggerBin(60.0, 0.287227196259, 0.00723276507687, 0.00723276507687),
                triggerBin(70.0, 0.338495693624, 0.00814985718531, 0.00814985718531),
                triggerBin(80.0, 0.52966244886, 0.00674471780861, 0.00674471780861),
                triggerBin(100.0, 0.758562763492, 0.00655265926001, 0.00655265926001),
                triggerBin(120.0, 0.904908664002, 0.00503800586712, 0.00503800586712),
                triggerBin(140.0, 0.975150994228, 0.00322842742029, 0.00322842742029),
                triggerBin(160.0, 0.998924385144, 0.000865660567278, 0.000865660567278),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0712669683258, 0.00386971030144),
                triggerBin(20.0, 0.0888022956662, 0.00262734948653, 0.00262734948653),
                triggerBin(30.0, 0.127173739157, 0.00332372130685, 0.00332372130685),
                triggerBin(40.0, 0.16476915758, 0.00412630434552, 0.00412630434552),
                triggerBin(50.0, 0.226632197052, 0.00522107740962, 0.00522107740962),
                triggerBin(60.0, 0.286110848795, 0.00619889718025, 0.00619889718025),
                triggerBin(70.0, 0.33970985448, 0.00702915655041, 0.00702915655041),
                triggerBin(80.0, 0.52488808566, 0.00586965651865, 0.00586965651865),
                triggerBin(100.0, 0.758869417432, 0.0056566454886, 0.0056566454886),
                triggerBin(120.0, 0.908506771483, 0.00425305005881, 0.00425305005881),
                triggerBin(140.0, 0.974800185049, 0.00278207512424, 0.00278207512424),
                triggerBin(160.0, 0.99933768519, 0.000591676367974, 0.000591676367974),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0712669683258, 0.00386971030144),
                triggerBin(20.0, 0.0886540371781, 0.00268658886937, 0.00268658886937),
                triggerBin(30.0, 0.126946897672, 0.00339616804124, 0.00339616804124),
                triggerBin(40.0, 0.165385357193, 0.00422388740813, 0.00422388740813),
                triggerBin(50.0, 0.224646072111, 0.00531794558929, 0.00531794558929),
                triggerBin(60.0, 0.286678762397, 0.00634942430664, 0.00634942430664),
                triggerBin(70.0, 0.33936256415, 0.00718197166536, 0.00718197166536),
                triggerBin(80.0, 0.526273386145, 0.005988137415, 0.005988137415),
                triggerBin(100.0, 0.759055186221, 0.0057794045812, 0.0057794045812),
                triggerBin(120.0, 0.908063766703, 0.00435847935425, 0.00435847935425),
                triggerBin(140.0, 0.974779692841, 0.00284839408643, 0.00284839408643),
                triggerBin(160.0, 0.999244664192, 0.000646063700318, 0.000646063700318),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0712669683258, 0.00386971030144),
                triggerBin(20.0, 0.0895284158136, 0.0030725920564, 0.0030725920564),
                triggerBin(30.0, 0.126673647249, 0.0038552061611, 0.0038552061611),
                triggerBin(40.0, 0.167200982945, 0.00480684409468, 0.00480684409468),
                triggerBin(50.0, 0.219398345112, 0.00597858469902, 0.00597858469902),
                triggerBin(60.0, 0.287227196259, 0.00723276507687, 0.00723276507687),
                triggerBin(70.0, 0.338495693624, 0.00814985718531, 0.00814985718531),
                triggerBin(80.0, 0.52966244886, 0.00674471780861, 0.00674471780861),
                triggerBin(100.0, 0.758562763492, 0.00655265926001, 0.00655265926001),
                triggerBin(120.0, 0.904908664002, 0.00503800586712, 0.00503800586712),
                triggerBin(140.0, 0.975150994228, 0.00322842742029, 0.00322842742029),
                triggerBin(160.0, 0.998924385144, 0.000865660567278, 0.000865660567278),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0712669683258, 0.00386971030144),
                triggerBin(20.0, 0.0953981385729, 0.00496025114877, 0.00474535018836),
                triggerBin(30.0, 0.128985083358, 0.00598966401697, 0.00576713198533),
                triggerBin(40.0, 0.178228388474, 0.00751267239442, 0.00727814172333),
                triggerBin(50.0, 0.224231464738, 0.00922024929906, 0.00896462359641),
                triggerBin(60.0, 0.304613674263, 0.0112375359242, 0.0110148306241),
                triggerBin(70.0, 0.362433862434, 0.0127823335018, 0.0125955756572),
                triggerBin(80.0, 0.545418167267, 0.0101401332957, 0.0101772034537),
                triggerBin(100.0, 0.76, 0.00998523409443, 0.010269975011),
                triggerBin(120.0, 0.891694352159, 0.00807180022944, 0.00861371275681),
                triggerBin(140.0, 0.966052376334, 0.00564296739725, 0.00662434608339),
                triggerBin(160.0, 0.997080291971, 0.00188564016332, 0.00383786315919),
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

    # Used input: multicrab_MetLeg2012_130517_110812

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.142857142857, 0.132260014253),
                triggerBin(20.0, 0.142857142857, 0.257123832984, 0.118480071045),
                triggerBin(30.0, 0.0, 0.458641675296, 0.0),
                triggerBin(40.0, 0.0, 0.841344746068, 0.0),
                triggerBin(50.0, 0.5, 0.41724846474, 0.41724846474),
                triggerBin(60.0, 0.0, 1.0, 0.0),
                triggerBin(70.0, 1.0, 0.0, 0.601684479424),
                triggerBin(80.0, 0.0, 1.0, 0.0),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0388349514563, 0.0190367039454),
                triggerBin(20.0, 0.041095890411, 0.0383632915283, 0.0222832479104),
                triggerBin(30.0, 0.111111111111, 0.060467252805, 0.0431774157972),
                triggerBin(40.0, 0.142857142857, 0.119718786455, 0.0767053610655),
                triggerBin(50.0, 0.176470588235, 0.142402653848, 0.0944266759714),
                triggerBin(60.0, 0.285714285714, 0.259937875571, 0.182129028008),
                triggerBin(70.0, 0.0, 0.841344746068, 0.0),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.024, 0.0136891197672),
                triggerBin(20.0, 0.0380952380952, 0.0290965667789, 0.0181439734408),
                triggerBin(30.0, 0.0545454545455, 0.0502231762716, 0.0295392531338),
                triggerBin(40.0, 0.0789473684211, 0.0708737003562, 0.0426562617902),
                triggerBin(50.0, 0.15, 0.12471137336, 0.0804822604739),
                triggerBin(60.0, 0.222222222222, 0.221429368878, 0.14211823823),
                triggerBin(70.0, 0.428571428571, 0.247840988275, 0.222487613116),
                triggerBin(80.0, 0.5, 0.41724846474, 0.41724846474),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 1.0, 0.0, 0.458641675296),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0243902439024, 0.012045482886),
                triggerBin(20.0, 0.0373831775701, 0.0285714611425, 0.0178064693186),
                triggerBin(30.0, 0.027397260274, 0.0349950540934, 0.0176764535746),
                triggerBin(40.0, 0.139534883721, 0.0740357287102, 0.0539183163988),
                triggerBin(50.0, 0.227272727273, 0.124519809699, 0.0944237146768),
                triggerBin(60.0, 0.3, 0.20826248199, 0.158328098893),
                triggerBin(70.0, 0.0, 0.36887757085, 0.0),
                triggerBin(80.0, 0.25, 0.368402425504, 0.207730893696),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.458641675296),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0454545454545, 0.0198605203978),
                triggerBin(20.0, 0.05, 0.0377701577881, 0.0237772015406),
                triggerBin(30.0, 0.105263157895, 0.0575793515833, 0.0409515011174),
                triggerBin(40.0, 0.136363636364, 0.11509911457, 0.0732667013517),
                triggerBin(50.0, 0.210526315789, 0.135427055903, 0.0978662361907),
                triggerBin(60.0, 0.285714285714, 0.259937875571, 0.182129028008),
                triggerBin(70.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.5, 0.314698893873, 0.314698893873),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0340425531915, 0.0118292205394),
                triggerBin(20.0, 0.0432432432432, 0.0206352522007, 0.0148268522389),
                triggerBin(30.0, 0.0803571428571, 0.0345395679156, 0.0257971733075),
                triggerBin(40.0, 0.1, 0.0549521822688, 0.0389435688158),
                triggerBin(50.0, 0.179487179487, 0.083232543249, 0.0637222991994),
                triggerBin(60.0, 0.25, 0.153966037382, 0.115498745679),
                triggerBin(70.0, 0.5, 0.195182116991, 0.195182116991),
                triggerBin(80.0, 0.75, 0.207730893696, 0.368402425504),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.6, 0.25334762525, 0.303366136254),
                triggerBin(140.0, 1.0, 0.0, 0.458641675296),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0300751879699, 0.00855040649468),
                triggerBin(20.0, 0.041095890411, 0.015171386274, 0.0115726923966),
                triggerBin(30.0, 0.0594594594595, 0.0228734949597, 0.0173900908681),
                triggerBin(40.0, 0.116504854369, 0.0406717229099, 0.032137201422),
                triggerBin(50.0, 0.196721311475, 0.0644002380547, 0.052982621917),
                triggerBin(60.0, 0.269230769231, 0.114603025448, 0.0935066525113),
                triggerBin(70.0, 0.357142857143, 0.169219923607, 0.144430653909),
                triggerBin(80.0, 0.5, 0.220457375638, 0.220457375638),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.75, 0.159659347816, 0.239566802733),
                triggerBin(140.0, 1.0, 0.0, 0.458641675296),
                triggerBin(160.0, 1.0, 0.0, 0.36887757085),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0696113074205, 0.00478386471276),
                triggerBin(20.0, 0.086100052362, 0.00301868987408, 0.00301868987408),
                triggerBin(30.0, 0.114783073199, 0.00368032589501, 0.00368032589501),
                triggerBin(40.0, 0.158208369448, 0.00455503640297, 0.00455503640297),
                triggerBin(50.0, 0.211214336202, 0.00568279032816, 0.00568279032816),
                triggerBin(60.0, 0.275650319615, 0.0067954117267, 0.0067954117267),
                triggerBin(70.0, 0.325083632782, 0.00749190699937, 0.00749190699937),
                triggerBin(80.0, 0.534777195129, 0.00625020991503, 0.00625020991503),
                triggerBin(100.0, 0.761535789488, 0.00587889958811, 0.00587889958811),
                triggerBin(120.0, 0.906714477085, 0.00450126695481, 0.00450126695481),
                triggerBin(140.0, 0.974576818531, 0.0029464708433, 0.0029464708433),
                triggerBin(160.0, 0.999425294115, 0.00056718023989, 0.00056718023989),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0696113074205, 0.00478386471276),
                triggerBin(20.0, 0.0894565956908, 0.00332190470008, 0.00332190470008),
                triggerBin(30.0, 0.113699588392, 0.00396852621864, 0.00396852621864),
                triggerBin(40.0, 0.159256175846, 0.00497044192998, 0.00497044192998),
                triggerBin(50.0, 0.228493518025, 0.00633244587679, 0.00633244587679),
                triggerBin(60.0, 0.283485900641, 0.00732236654731, 0.00732236654731),
                triggerBin(70.0, 0.344779001955, 0.00829278695574, 0.00829278695574),
                triggerBin(80.0, 0.538461430532, 0.00689989950203, 0.00689989950203),
                triggerBin(100.0, 0.758811199535, 0.00652748027468, 0.00652748027468),
                triggerBin(120.0, 0.901989390996, 0.00505344162261, 0.00505344162261),
                triggerBin(140.0, 0.968895941402, 0.00352554564848, 0.00352554564848),
                triggerBin(160.0, 0.999102174041, 0.000790761081971, 0.000790761081971),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0696113074205, 0.00478386471276),
                triggerBin(20.0, 0.0881865758167, 0.00340575806638, 0.00340575806638),
                triggerBin(30.0, 0.114071021499, 0.00408620650886, 0.00408620650886),
                triggerBin(40.0, 0.160235347314, 0.00511029435392, 0.00511029435392),
                triggerBin(50.0, 0.221824187769, 0.0064488455605, 0.0064488455605),
                triggerBin(60.0, 0.283415031867, 0.00758173403321, 0.00758173403321),
                triggerBin(70.0, 0.340881117935, 0.00850179476697, 0.00850179476697),
                triggerBin(80.0, 0.540821267084, 0.00704174330098, 0.00704174330098),
                triggerBin(100.0, 0.760126199788, 0.00667298277918, 0.00667298277918),
                triggerBin(120.0, 0.903106016319, 0.00514840069608, 0.00514840069608),
                triggerBin(140.0, 0.970059251853, 0.0035655512699, 0.0035655512699),
                triggerBin(160.0, 0.998944512397, 0.000876049911222, 0.000876049911222),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0696113074205, 0.00478386471276),
                triggerBin(20.0, 0.0887990914249, 0.00382966096759, 0.00382966096759),
                triggerBin(30.0, 0.114819795986, 0.00457020628735, 0.00457020628735),
                triggerBin(40.0, 0.160632134454, 0.005691573897, 0.005691573897),
                triggerBin(50.0, 0.217010076326, 0.00713292702824, 0.00713292702824),
                triggerBin(60.0, 0.283628657499, 0.00849368244467, 0.00849368244467),
                triggerBin(70.0, 0.337705620612, 0.00946944817896, 0.00946944817896),
                triggerBin(80.0, 0.542415376134, 0.0078040018275, 0.0078040018275),
                triggerBin(100.0, 0.759965343653, 0.00743019572706, 0.00743019572706),
                triggerBin(120.0, 0.90160480053, 0.0057871868321, 0.0057871868321),
                triggerBin(140.0, 0.971422251711, 0.0039125750901, 0.0039125750901),
                triggerBin(160.0, 0.998635496258, 0.00109804453327, 0.00109804453327),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0696113074205, 0.00478386471276),
                triggerBin(20.0, 0.088934469051, 0.00327551940239, 0.00327551940239),
                triggerBin(30.0, 0.113868503077, 0.00392533011425, 0.00392533011425),
                triggerBin(40.0, 0.159091501353, 0.00490720177719, 0.00490720177719),
                triggerBin(50.0, 0.225798432433, 0.00623283676984, 0.00623283676984),
                triggerBin(60.0, 0.282292245736, 0.00724369764726, 0.00724369764726),
                triggerBin(70.0, 0.341670692405, 0.00816998057373, 0.00816998057373),
                triggerBin(80.0, 0.537867286014, 0.00679951305502, 0.00679951305502),
                triggerBin(100.0, 0.759251828643, 0.00642653744455, 0.00642653744455),
                triggerBin(120.0, 0.902743385932, 0.0049669770933, 0.0049669770933),
                triggerBin(140.0, 0.969784424485, 0.00343528966004, 0.00343528966004),
                triggerBin(160.0, 0.999155155544, 0.000754669589213, 0.000754669589213),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0696113074205, 0.00478386471276),
                triggerBin(20.0, 0.0885213645442, 0.00334835138032, 0.00334835138032),
                triggerBin(30.0, 0.11398069835, 0.00401519449096, 0.00401519449096),
                triggerBin(40.0, 0.15972620119, 0.00502064410783, 0.00502064410783),
                triggerBin(50.0, 0.223598433797, 0.0063541759042, 0.0063541759042),
                triggerBin(60.0, 0.282911661179, 0.00743185156681, 0.00743185156681),
                triggerBin(70.0, 0.341233693958, 0.00835537712538, 0.00835537712538),
                triggerBin(80.0, 0.539509634022, 0.00693531240299, 0.00693531240299),
                triggerBin(100.0, 0.759736461838, 0.00656443718737, 0.00656443718737),
                triggerBin(120.0, 0.902944321811, 0.00506861837206, 0.00506861837206),
                triggerBin(140.0, 0.969936364016, 0.00350823112911, 0.00350823112911),
                triggerBin(160.0, 0.999038345077, 0.000822523833448, 0.000822523833448),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0696113074205, 0.00478386471276),
                triggerBin(20.0, 0.0887990914249, 0.00382966096759, 0.00382966096759),
                triggerBin(30.0, 0.114819795986, 0.00457020628735, 0.00457020628735),
                triggerBin(40.0, 0.160632134454, 0.005691573897, 0.005691573897),
                triggerBin(50.0, 0.217010076326, 0.00713292702824, 0.00713292702824),
                triggerBin(60.0, 0.283628657499, 0.00849368244467, 0.00849368244467),
                triggerBin(70.0, 0.337705620612, 0.00946944817896, 0.00946944817896),
                triggerBin(80.0, 0.542415376134, 0.0078040018275, 0.0078040018275),
                triggerBin(100.0, 0.759965343653, 0.00743019572706, 0.00743019572706),
                triggerBin(120.0, 0.90160480053, 0.0057871868321, 0.0057871868321),
                triggerBin(140.0, 0.971422251711, 0.0039125750901, 0.0039125750901),
                triggerBin(160.0, 0.998635496258, 0.00109804453327, 0.00109804453327),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0696113074205, 0.00478386471276),
                triggerBin(20.0, 0.0947154471545, 0.00627773429203, 0.0059369644741),
                triggerBin(30.0, 0.119555555556, 0.00723634923052, 0.00688727521233),
                triggerBin(40.0, 0.168475452196, 0.00894243556044, 0.00858947412223),
                triggerBin(50.0, 0.219151670951, 0.0109917375758, 0.0106198310578),
                triggerBin(60.0, 0.29604261796, 0.0131295837969, 0.0128099142646),
                triggerBin(70.0, 0.354203935599, 0.0148791018574, 0.0146102786771),
                triggerBin(80.0, 0.551871657754, 0.0117358513796, 0.0117926003772),
                triggerBin(100.0, 0.757513661202, 0.0113584996142, 0.0117208720772),
                triggerBin(120.0, 0.890862944162, 0.00914636731373, 0.00983824462614),
                triggerBin(140.0, 0.96379525593, 0.0066028560395, 0.00786963421827),
                triggerBin(160.0, 0.996254681648, 0.00241876540484, 0.00491838085518),
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

    # Used input: multicrab_MetLeg2012_130517_110812

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.2, 0.1788854382),
                triggerBin(20.0, 0.166666666667, 0.287350389332, 0.138284918684),
                triggerBin(30.0, 0.0, 0.458641675296, 0.0),
                triggerBin(40.0, 0.0, 0.841344746068, 0.0),
                triggerBin(50.0, 0.5, 0.41724846474, 0.41724846474),
                triggerBin(60.0, 0.0, 1.0, 0.0),
                triggerBin(70.0, 1.0, 0.0, 0.601684479424),
                triggerBin(80.0, 0.0, 1.0, 0.0),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0449438202247, 0.0219611181558),
                triggerBin(20.0, 0.0454545454545, 0.0422441218236, 0.0246367510149),
                triggerBin(30.0, 0.102040816327, 0.06313660811, 0.0433605078476),
                triggerBin(40.0, 0.176470588235, 0.142402653848, 0.0944266759714),
                triggerBin(50.0, 0.153846153846, 0.16803608658, 0.0987133108909),
                triggerBin(60.0, 0.285714285714, 0.259937875571, 0.182129028008),
                triggerBin(70.0, 0.0, 0.841344746068, 0.0),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.0, 0.601684479424, 0.0),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0285714285714, 0.0162583610844),
                triggerBin(20.0, 0.0430107526882, 0.0327020485265, 0.0204721109128),
                triggerBin(30.0, 0.0566037735849, 0.0520081635621, 0.0306480760549),
                triggerBin(40.0, 0.0857142857143, 0.0764033060045, 0.0462826358375),
                triggerBin(50.0, 0.1875, 0.149398565056, 0.100212028831),
                triggerBin(60.0, 0.222222222222, 0.221429368878, 0.14211823823),
                triggerBin(70.0, 0.428571428571, 0.247840988275, 0.222487613116),
                triggerBin(80.0, 0.0, 0.841344746068, 0.0),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 1.0, 0.0, 0.601684479424),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0283687943262, 0.013981752504),
                triggerBin(20.0, 0.0309278350515, 0.02917029971, 0.0167854408748),
                triggerBin(30.0, 0.03125, 0.0397347958314, 0.0201590096415),
                triggerBin(40.0, 0.142857142857, 0.0755708996607, 0.0551651552867),
                triggerBin(50.0, 0.263157894737, 0.138819970242, 0.108565019101),
                triggerBin(60.0, 0.3, 0.20826248199, 0.158328098893),
                triggerBin(70.0, 0.0, 0.36887757085, 0.0),
                triggerBin(80.0, 0.25, 0.368402425504, 0.207730893696),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.458641675296),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0531914893617, 0.0231466542826),
                triggerBin(20.0, 0.0555555555556, 0.0417497559944, 0.0263999125929),
                triggerBin(30.0, 0.0961538461538, 0.0598141322187, 0.0408993528538),
                triggerBin(40.0, 0.166666666667, 0.135998901491, 0.0892717907981),
                triggerBin(50.0, 0.2, 0.157061286074, 0.10675070638),
                triggerBin(60.0, 0.285714285714, 0.259937875571, 0.182129028008),
                triggerBin(70.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0402010050251, 0.013924578649),
                triggerBin(20.0, 0.0484848484848, 0.0230425188578, 0.0166050238729),
                triggerBin(30.0, 0.0761904761905, 0.0354276947868, 0.0259335520675),
                triggerBin(40.0, 0.11320754717, 0.0614945435373, 0.0439740652089),
                triggerBin(50.0, 0.193548387097, 0.0976717076465, 0.0739582576944),
                triggerBin(60.0, 0.25, 0.153966037382, 0.115498745679),
                triggerBin(70.0, 0.5, 0.195182116991, 0.195182116991),
                triggerBin(80.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.5, 0.314698893873, 0.314698893873),
                triggerBin(140.0, 1.0, 0.0, 0.601684479424),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0352941176471, 0.0100071214211),
                triggerBin(20.0, 0.0419847328244, 0.0163593089914, 0.0123344208872),
                triggerBin(30.0, 0.0591715976331, 0.0241779086556, 0.0181345594478),
                triggerBin(40.0, 0.126315789474, 0.0437638281678, 0.0347456906981),
                triggerBin(50.0, 0.22, 0.0744257803206, 0.0614915858722),
                triggerBin(60.0, 0.269230769231, 0.114603025448, 0.0935066525113),
                triggerBin(70.0, 0.357142857143, 0.169219923607, 0.144430653909),
                triggerBin(80.0, 0.428571428571, 0.247840988275, 0.222487613116),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.714285714286, 0.182129028008, 0.259937875571),
                triggerBin(140.0, 1.0, 0.0, 0.601684479424),
                triggerBin(160.0, 1.0, 0.0, 0.36887757085),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0672538030424, 0.00501122554997),
                triggerBin(20.0, 0.0797330829264, 0.00311258357597, 0.00311258357597),
                triggerBin(30.0, 0.11639656385, 0.00395102079891, 0.00395102079891),
                triggerBin(40.0, 0.146491491679, 0.00463397735395, 0.00463397735395),
                triggerBin(50.0, 0.206577801619, 0.00593147061217, 0.00593147061217),
                triggerBin(60.0, 0.279585762901, 0.0071391625652, 0.0071391625652),
                triggerBin(70.0, 0.333452214868, 0.00787501093007, 0.00787501093007),
                triggerBin(80.0, 0.535212475037, 0.00647258460946, 0.00647258460946),
                triggerBin(100.0, 0.756881489321, 0.00620269974794, 0.00620269974794),
                triggerBin(120.0, 0.903908904263, 0.00474528604178, 0.00474528604178),
                triggerBin(140.0, 0.97313254983, 0.00315774209545, 0.00315774209545),
                triggerBin(160.0, 0.999360323774, 0.000631279288451, 0.000631279288451),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0672538030424, 0.00501122554997),
                triggerBin(20.0, 0.082489094284, 0.00342707864691, 0.00342707864691),
                triggerBin(30.0, 0.117220600566, 0.00431592824763, 0.00431592824763),
                triggerBin(40.0, 0.147655041438, 0.00508619096282, 0.00508619096282),
                triggerBin(50.0, 0.224738865857, 0.00662939749813, 0.00662939749813),
                triggerBin(60.0, 0.28362092442, 0.00765164106767, 0.00765164106767),
                triggerBin(70.0, 0.350098248677, 0.00868376563875, 0.00868376563875),
                triggerBin(80.0, 0.538826531049, 0.00715613265129, 0.00715613265129),
                triggerBin(100.0, 0.755405429731, 0.00691379823808, 0.00691379823808),
                triggerBin(120.0, 0.903292253426, 0.0052243139122, 0.0052243139122),
                triggerBin(140.0, 0.966328212897, 0.00385555097467, 0.00385555097467),
                triggerBin(160.0, 0.999007595609, 0.000874040451784, 0.000874040451784),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0672538030424, 0.00501122554997),
                triggerBin(20.0, 0.0818305830203, 0.00351777060387, 0.00351777060387),
                triggerBin(30.0, 0.116859501513, 0.00442259826964, 0.00442259826964),
                triggerBin(40.0, 0.149092495237, 0.00523007625156, 0.00523007625156),
                triggerBin(50.0, 0.218299028847, 0.00675659034218, 0.00675659034218),
                triggerBin(60.0, 0.284822796366, 0.00793830030496, 0.00793830030496),
                triggerBin(70.0, 0.346518461013, 0.00890464284883, 0.00890464284883),
                triggerBin(80.0, 0.5410152507, 0.00729773885763, 0.00729773885763),
                triggerBin(100.0, 0.756966520127, 0.00705555860052, 0.00705555860052),
                triggerBin(120.0, 0.90299929751, 0.00535746198341, 0.00535746198341),
                triggerBin(140.0, 0.967981582813, 0.0038647188987, 0.0038647188987),
                triggerBin(160.0, 0.998828792748, 0.000972040387334, 0.000972040387334),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0672538030424, 0.00501122554997),
                triggerBin(20.0, 0.0835285657389, 0.0039779065822, 0.0039779065822),
                triggerBin(30.0, 0.117177738174, 0.00492902659916, 0.00492902659916),
                triggerBin(40.0, 0.15094907762, 0.00584238335574, 0.00584238335574),
                triggerBin(50.0, 0.213485380175, 0.00748021138665, 0.00748021138665),
                triggerBin(60.0, 0.286183520631, 0.00891103112391, 0.00891103112391),
                triggerBin(70.0, 0.342267273239, 0.0099153499611, 0.0099153499611),
                triggerBin(80.0, 0.542002121895, 0.00809280728325, 0.00809280728325),
                triggerBin(100.0, 0.757272315571, 0.00784297461569, 0.00784297461569),
                triggerBin(120.0, 0.899531986584, 0.00608459844025, 0.00608459844025),
                triggerBin(140.0, 0.96972813122, 0.00421398533206, 0.00421398533206),
                triggerBin(160.0, 0.998491409423, 0.00121393064589, 0.00121393064589),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0672538030424, 0.00501122554997),
                triggerBin(20.0, 0.0820586881832, 0.0033788724991, 0.0033788724991),
                triggerBin(30.0, 0.117090948642, 0.00426030199008, 0.00426030199008),
                triggerBin(40.0, 0.14747050359, 0.00501683225166, 0.00501683225166),
                triggerBin(50.0, 0.221902929162, 0.00652223280727, 0.00652223280727),
                triggerBin(60.0, 0.283007535057, 0.00757546788251, 0.00757546788251),
                triggerBin(70.0, 0.347475376342, 0.00855995696104, 0.00855995696104),
                triggerBin(80.0, 0.538242528343, 0.00705030964667, 0.00705030964667),
                triggerBin(100.0, 0.755646794634, 0.00680253696947, 0.00680253696947),
                triggerBin(120.0, 0.903390653968, 0.00515054579842, 0.00515054579842),
                triggerBin(140.0, 0.96740812876, 0.00374524756624, 0.00374524756624),
                triggerBin(160.0, 0.999065097145, 0.000835077925654, 0.000835077925654),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0672538030424, 0.00501122554997),
                triggerBin(20.0, 0.0819325632588, 0.00345645614354, 0.00345645614354),
                triggerBin(30.0, 0.116962635305, 0.00435112839134, 0.00435112839134),
                triggerBin(40.0, 0.148370949863, 0.00513589718395, 0.00513589718395),
                triggerBin(50.0, 0.219909467794, 0.00665373912913, 0.00665373912913),
                triggerBin(60.0, 0.284008453122, 0.00777728275081, 0.00777728275081),
                triggerBin(70.0, 0.346945518269, 0.00875258800374, 0.00875258800374),
                triggerBin(80.0, 0.539784475446, 0.00718906575264, 0.00718906575264),
                triggerBin(100.0, 0.75637787479, 0.0069442340786, 0.0069442340786),
                triggerBin(120.0, 0.903173606018, 0.00526619534348, 0.00526619534348),
                triggerBin(140.0, 0.967725647553, 0.00381251408796, 0.00381251408796),
                triggerBin(160.0, 0.99893412039, 0.000911581118696, 0.000911581118696),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0672538030424, 0.00501122554997),
                triggerBin(20.0, 0.0835285657389, 0.0039779065822, 0.0039779065822),
                triggerBin(30.0, 0.117177738174, 0.00492902659916, 0.00492902659916),
                triggerBin(40.0, 0.15094907762, 0.00584238335574, 0.00584238335574),
                triggerBin(50.0, 0.213485380175, 0.00748021138665, 0.00748021138665),
                triggerBin(60.0, 0.286183520631, 0.00891103112391, 0.00891103112391),
                triggerBin(70.0, 0.342267273239, 0.0099153499611, 0.0099153499611),
                triggerBin(80.0, 0.542002121895, 0.00809280728325, 0.00809280728325),
                triggerBin(100.0, 0.757272315571, 0.00784297461569, 0.00784297461569),
                triggerBin(120.0, 0.899531986584, 0.00608459844025, 0.00608459844025),
                triggerBin(140.0, 0.96972813122, 0.00421398533206, 0.00421398533206),
                triggerBin(160.0, 0.998491409423, 0.00121393064589, 0.00121393064589),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0672538030424, 0.00501122554997),
                triggerBin(20.0, 0.0911614993059, 0.00661983512417, 0.00622741326998),
                triggerBin(30.0, 0.122780314561, 0.00784344415355, 0.00744765087623),
                triggerBin(40.0, 0.164746543779, 0.00938910388007, 0.00899050540508),
                triggerBin(50.0, 0.219266714594, 0.0116583396536, 0.0112417971223),
                triggerBin(60.0, 0.296888141295, 0.0138415386277, 0.0134892241962),
                triggerBin(70.0, 0.354146341463, 0.015565483516, 0.0152717735207),
                triggerBin(80.0, 0.550808314088, 0.0122070998165, 0.0122671657556),
                triggerBin(100.0, 0.757759273278, 0.0119614635754, 0.012364059751),
                triggerBin(120.0, 0.886005560704, 0.00976314699674, 0.0105125108763),
                triggerBin(140.0, 0.962861072902, 0.00701575904016, 0.00841299435296),
                triggerBin(160.0, 0.995918367347, 0.00263592507761, 0.00535793630232),
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

    # Used input: multicrab_MetLeg2012_130517_110812

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0714285714286, 0.0688302936899),
                triggerBin(20.0, 0.0909090909091, 0.179295209474, 0.0753268806181),
                triggerBin(30.0, 0.0, 0.36887757085, 0.0),
                triggerBin(40.0, 0.0, 0.841344746068, 0.0),
                triggerBin(50.0, 1.0, 0.0, 0.841344746068),
                triggerBin(60.0, 0.0, 1.0, 0.0),
                triggerBin(70.0, 1.0, 0.0, 0.601684479424),
                triggerBin(80.0, 0.0, 1.0, 0.0),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0335570469799, 0.014753220915),
                triggerBin(20.0, 0.0388349514563, 0.0296413099588, 0.0184945174852),
                triggerBin(30.0, 0.0609756097561, 0.0391439922963, 0.0260867261305),
                triggerBin(40.0, 0.135135135135, 0.0810851922564, 0.0570987615161),
                triggerBin(50.0, 0.161290322581, 0.0943938992063, 0.0678360239621),
                triggerBin(60.0, 0.4, 0.204596854236, 0.180009253894),
                triggerBin(70.0, 0.0, 0.841344746068, 0.0),
                triggerBin(80.0, 1.0, 0.0, 0.458641675296),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0309278350515, 0.0124294512387),
                triggerBin(20.0, 0.0308641975309, 0.0203396530446, 0.0132679006318),
                triggerBin(30.0, 0.06, 0.0341183623328, 0.0235435867755),
                triggerBin(40.0, 0.0634920634921, 0.0473598474317, 0.0301398055994),
                triggerBin(50.0, 0.12, 0.103114634532, 0.0645799596342),
                triggerBin(60.0, 0.266666666667, 0.161145049639, 0.122866921165),
                triggerBin(70.0, 0.5, 0.220457375638, 0.220457375638),
                triggerBin(80.0, 0.5, 0.41724846474, 0.41724846474),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0215517241379, 0.00953379816409),
                triggerBin(20.0, 0.0487804878049, 0.0231776876734, 0.0167051922328),
                triggerBin(30.0, 0.0578512396694, 0.0297701883604, 0.0210904293882),
                triggerBin(40.0, 0.116883116883, 0.0488003111809, 0.0371884583537),
                triggerBin(50.0, 0.135135135135, 0.0810851922564, 0.0570987615161),
                triggerBin(60.0, 0.263157894737, 0.138819970242, 0.108565019101),
                triggerBin(70.0, 0.166666666667, 0.287350389332, 0.138284918684),
                triggerBin(80.0, 0.2, 0.324250626004, 0.16603930634),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.458641675296),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0, 0.458641675296),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0368098159509, 0.014748370691),
                triggerBin(20.0, 0.0438596491228, 0.0285810165484, 0.0188157050399),
                triggerBin(30.0, 0.0581395348837, 0.0374166301655, 0.024884782787),
                triggerBin(40.0, 0.131578947368, 0.0792158922547, 0.0556305565753),
                triggerBin(50.0, 0.1875, 0.0951654963661, 0.0717391962659),
                triggerBin(60.0, 0.4, 0.204596854236, 0.180009253894),
                triggerBin(70.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(80.0, 1.0, 0.0, 0.458641675296),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.5, 0.314698893873, 0.314698893873),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0336134453782, 0.00953889012623),
                triggerBin(20.0, 0.036231884058, 0.0150593556177, 0.0111667137113),
                triggerBin(30.0, 0.0591397849462, 0.022755891775, 0.0172980263453),
                triggerBin(40.0, 0.0891089108911, 0.0380389959459, 0.0285463037648),
                triggerBin(50.0, 0.157894736842, 0.0637264282034, 0.0497130664879),
                triggerBin(60.0, 0.32, 0.119275761539, 0.102271514956),
                triggerBin(70.0, 0.545454545455, 0.1795821324, 0.189661990926),
                triggerBin(80.0, 0.8, 0.16603930634, 0.324250626004),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.6, 0.25334762525, 0.303366136254),
                triggerBin(140.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0288624787776, 0.00689841842266),
                triggerBin(20.0, 0.0409090909091, 0.0117710975327, 0.00943624491951),
                triggerBin(30.0, 0.0586319218241, 0.0166691379962, 0.0134508692194),
                triggerBin(40.0, 0.101123595506, 0.027909603445, 0.022888738487),
                triggerBin(50.0, 0.148936170213, 0.0461538807695, 0.0376626274674),
                triggerBin(60.0, 0.295454545455, 0.0845305778572, 0.0738629419477),
                triggerBin(70.0, 0.411764705882, 0.149770451815, 0.137360513174),
                triggerBin(80.0, 0.5, 0.195182116991, 0.195182116991),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.75, 0.159659347816, 0.239566802733),
                triggerBin(140.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(160.0, 1.0, 0.0, 0.308024223477),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0688872066616, 0.00402307749313),
                triggerBin(20.0, 0.0827394438411, 0.00249606319107, 0.00249606319107),
                triggerBin(30.0, 0.123611452996, 0.00322960186762, 0.00322960186762),
                triggerBin(40.0, 0.168296413084, 0.00406385834417, 0.00406385834417),
                triggerBin(50.0, 0.216530829892, 0.00494787957763, 0.00494787957763),
                triggerBin(60.0, 0.274549098416, 0.00597383085728, 0.00597383085728),
                triggerBin(70.0, 0.327637365763, 0.00675795366837, 0.00675795366837),
                triggerBin(80.0, 0.519641872363, 0.00562534058236, 0.00562534058236),
                triggerBin(100.0, 0.751412529084, 0.00546556838059, 0.00546556838059),
                triggerBin(120.0, 0.905411308145, 0.00415767374452, 0.00415767374452),
                triggerBin(140.0, 0.977567608497, 0.00258539535321, 0.00258539535321),
                triggerBin(160.0, 0.999502635393, 0.000490841536009, 0.000490841536009),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0688872066616, 0.00402307749313),
                triggerBin(20.0, 0.085244594043, 0.00274100719032, 0.00274100719032),
                triggerBin(30.0, 0.123333351037, 0.00348203334373, 0.00348203334373),
                triggerBin(40.0, 0.165077977168, 0.00436564828633, 0.00436564828633),
                triggerBin(50.0, 0.231768312033, 0.00554097240415, 0.00554097240415),
                triggerBin(60.0, 0.285187636843, 0.00654624082836, 0.00654624082836),
                triggerBin(70.0, 0.344345482171, 0.00747303246352, 0.00747303246352),
                triggerBin(80.0, 0.526516183807, 0.00621088562235, 0.00621088562235),
                triggerBin(100.0, 0.750732946255, 0.00607004620784, 0.00607004620784),
                triggerBin(120.0, 0.904789309483, 0.00454462372109, 0.00454462372109),
                triggerBin(140.0, 0.972319375656, 0.00309391290727, 0.00309391290727),
                triggerBin(160.0, 0.99924151985, 0.000668110345674, 0.000668110345674),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0688872066616, 0.00402307749313),
                triggerBin(20.0, 0.0845135113609, 0.00281290924491, 0.00281290924491),
                triggerBin(30.0, 0.123358248236, 0.00358587625317, 0.00358587625317),
                triggerBin(40.0, 0.167615905669, 0.0045117122353, 0.0045117122353),
                triggerBin(50.0, 0.226063915467, 0.00563140024675, 0.00563140024675),
                triggerBin(60.0, 0.284894918272, 0.00673661070422, 0.00673661070422),
                triggerBin(70.0, 0.340780273066, 0.00764691267927, 0.00764691267927),
                triggerBin(80.0, 0.527298489893, 0.00634305408234, 0.00634305408234),
                triggerBin(100.0, 0.752375094844, 0.00619235404496, 0.00619235404496),
                triggerBin(120.0, 0.904249552872, 0.00468172963405, 0.00468172963405),
                triggerBin(140.0, 0.973184981846, 0.00314221272587, 0.00314221272587),
                triggerBin(160.0, 0.99910334368, 0.000744311161591, 0.000744311161591),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0688872066616, 0.00402307749313),
                triggerBin(20.0, 0.0861829823823, 0.00317689860072, 0.00317689860072),
                triggerBin(30.0, 0.124370874092, 0.0040218974629, 0.0040218974629),
                triggerBin(40.0, 0.17008942036, 0.00505590110264, 0.00505590110264),
                triggerBin(50.0, 0.222617876828, 0.00624519164452, 0.00624519164452),
                triggerBin(60.0, 0.284907539465, 0.00752524416515, 0.00752524416515),
                triggerBin(70.0, 0.340193166806, 0.00853690315292, 0.00853690315292),
                triggerBin(80.0, 0.529786752722, 0.00703652187606, 0.00703652187606),
                triggerBin(100.0, 0.753341509978, 0.00688128822529, 0.00688128822529),
                triggerBin(120.0, 0.901525540457, 0.00531113151363, 0.00531113151363),
                triggerBin(140.0, 0.973960475326, 0.00347444996211, 0.00347444996211),
                triggerBin(160.0, 0.998839458485, 0.000934081151869, 0.000934081151869),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0688872066616, 0.00402307749313),
                triggerBin(20.0, 0.0848538588974, 0.00270355156012, 0.00270355156012),
                triggerBin(30.0, 0.123376487055, 0.00344418802526, 0.00344418802526),
                triggerBin(40.0, 0.165579473372, 0.004320700109, 0.004320700109),
                triggerBin(50.0, 0.229355271283, 0.0054489371777, 0.0054489371777),
                triggerBin(60.0, 0.283528538502, 0.00645907179206, 0.00645907179206),
                triggerBin(70.0, 0.341702852614, 0.00736317888695, 0.00736317888695),
                triggerBin(80.0, 0.525408136252, 0.00612045244883, 0.00612045244883),
                triggerBin(100.0, 0.750842114103, 0.00597590905429, 0.00597590905429),
                triggerBin(120.0, 0.904887292972, 0.00448558739224, 0.00448558739224),
                triggerBin(140.0, 0.973134172491, 0.00301528408249, 0.00301528408249),
                triggerBin(160.0, 0.999283479187, 0.000640083729953, 0.000640083729953),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0688872066616, 0.00402307749313),
                triggerBin(20.0, 0.0846656554313, 0.00276466307709, 0.00276466307709),
                triggerBin(30.0, 0.123366423541, 0.00352332538, 0.00352332538),
                triggerBin(40.0, 0.166708697838, 0.00442724640478, 0.00442724640478),
                triggerBin(50.0, 0.227529339523, 0.00555145525506, 0.00555145525506),
                triggerBin(60.0, 0.284284716855, 0.00661391918936, 0.00661391918936),
                triggerBin(70.0, 0.341191291155, 0.0075219220255, 0.0075219220255),
                triggerBin(80.0, 0.526457916945, 0.00624516791549, 0.00624516791549),
                triggerBin(100.0, 0.751693386987, 0.0060971970463, 0.0060971970463),
                triggerBin(120.0, 0.904533809234, 0.00459498510801, 0.00459498510801),
                triggerBin(140.0, 0.973161873834, 0.00308615388125, 0.00308615388125),
                triggerBin(160.0, 0.999183622297, 0.0006983159164, 0.0006983159164),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0688872066616, 0.00402307749313),
                triggerBin(20.0, 0.0861829823823, 0.00317689860072, 0.00317689860072),
                triggerBin(30.0, 0.124370874092, 0.0040218974629, 0.0040218974629),
                triggerBin(40.0, 0.17008942036, 0.00505590110264, 0.00505590110264),
                triggerBin(50.0, 0.222617876828, 0.00624519164452, 0.00624519164452),
                triggerBin(60.0, 0.284907539465, 0.00752524416515, 0.00752524416515),
                triggerBin(70.0, 0.340193166806, 0.00853690315292, 0.00853690315292),
                triggerBin(80.0, 0.529786752722, 0.00703652187606, 0.00703652187606),
                triggerBin(100.0, 0.753341509978, 0.00688128822529, 0.00688128822529),
                triggerBin(120.0, 0.901525540457, 0.00531113151363, 0.00531113151363),
                triggerBin(140.0, 0.973960475326, 0.00347444996211, 0.00347444996211),
                triggerBin(160.0, 0.998839458485, 0.000934081151869, 0.000934081151869),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0688872066616, 0.00402307749313),
                triggerBin(20.0, 0.0950071326676, 0.0052145275901, 0.00497681274721),
                triggerBin(30.0, 0.129011345219, 0.0063205172473, 0.00607359149764),
                triggerBin(40.0, 0.180372381691, 0.00789292889189, 0.00763866976398),
                triggerBin(50.0, 0.225427872861, 0.00962088905194, 0.00934533354153),
                triggerBin(60.0, 0.301818181818, 0.0117240824372, 0.0114775111722),
                triggerBin(70.0, 0.363702096891, 0.0133938680376, 0.0131913441583),
                triggerBin(80.0, 0.547423126895, 0.0105517320751, 0.0105936564536),
                triggerBin(100.0, 0.758299359348, 0.0104658872818, 0.0107751326903),
                triggerBin(120.0, 0.888332140301, 0.00849463828377, 0.00907397183271),
                triggerBin(140.0, 0.967230443975, 0.0057884091668, 0.00686587464842),
                triggerBin(160.0, 0.996855345912, 0.00203089914731, 0.00413246748141),
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

    # Used input: multicrab_MetLeg2012_130517_110812

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.166666666667, 0.152145154863),
                triggerBin(20.0, 0.142857142857, 0.257123832984, 0.118480071045),
                triggerBin(30.0, 0.0, 0.458641675296, 0.0),
                triggerBin(40.0, 0.0, 0.841344746068, 0.0),
                triggerBin(50.0, 1.0, 0.0, 0.841344746068),
                triggerBin(60.0, 0.0, 1.0, 0.0),
                triggerBin(70.0, 1.0, 0.0, 0.601684479424),
                triggerBin(80.0, 0.0, 1.0, 0.0),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0434782608696, 0.0212612889966),
                triggerBin(20.0, 0.0441176470588, 0.0410575957313, 0.0239150832448),
                triggerBin(30.0, 0.1, 0.0619892518934, 0.0425078913818),
                triggerBin(40.0, 0.166666666667, 0.135998901491, 0.0892717907981),
                triggerBin(50.0, 0.142857142857, 0.158270654649, 0.0917088958422),
                triggerBin(60.0, 0.285714285714, 0.259937875571, 0.182129028008),
                triggerBin(70.0, 0.0, 0.841344746068, 0.0),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0265486725664, 0.0151230470988),
                triggerBin(20.0, 0.0425531914894, 0.0323678650094, 0.0202555238052),
                triggerBin(30.0, 0.0377358490566, 0.0476137480969, 0.0243364286652),
                triggerBin(40.0, 0.0833333333333, 0.074467426805, 0.045007246588),
                triggerBin(50.0, 0.1875, 0.149398565056, 0.100212028831),
                triggerBin(60.0, 0.222222222222, 0.221429368878, 0.14211823823),
                triggerBin(70.0, 0.5, 0.256909620203, 0.256909620203),
                triggerBin(80.0, 1.0, 0.0, 0.841344746068),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 1.0, 0.0, 0.601684479424),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0266666666667, 0.0131543542995),
                triggerBin(20.0, 0.0449438202247, 0.0341106344125, 0.0213868402105),
                triggerBin(30.0, 0.03125, 0.0397347958314, 0.0201590096415),
                triggerBin(40.0, 0.128205128205, 0.0774292319421, 0.0542358310136),
                triggerBin(50.0, 0.2, 0.130118869123, 0.0931224604655),
                triggerBin(60.0, 0.3, 0.20826248199, 0.158328098893),
                triggerBin(70.0, 0.0, 0.36887757085, 0.0),
                triggerBin(80.0, 0.0, 0.458641675296, 0.0),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.458641675296),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0510204081633, 0.0222273333556),
                triggerBin(20.0, 0.0533333333333, 0.0401631110859, 0.0253512991407),
                triggerBin(30.0, 0.0943396226415, 0.0587823296232, 0.0401398467978),
                triggerBin(40.0, 0.157894736842, 0.130121162629, 0.0846498044596),
                triggerBin(50.0, 0.2, 0.157061286074, 0.10675070638),
                triggerBin(60.0, 0.285714285714, 0.259937875571, 0.182129028008),
                triggerBin(70.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.5, 0.314698893873, 0.314698893873),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0379146919431, 0.0131482916696),
                triggerBin(20.0, 0.0473372781065, 0.0225172257675, 0.0162160781563),
                triggerBin(30.0, 0.0660377358491, 0.0337580471231, 0.0240344740711),
                triggerBin(40.0, 0.109090909091, 0.0594733255375, 0.0424090752596),
                triggerBin(50.0, 0.193548387097, 0.0976717076465, 0.0739582576944),
                triggerBin(60.0, 0.25, 0.153966037382, 0.115498745679),
                triggerBin(70.0, 0.555555555556, 0.198267144951, 0.213462824948),
                triggerBin(80.0, 1.0, 0.0, 0.458641675296),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.6, 0.25334762525, 0.303366136254),
                triggerBin(140.0, 1.0, 0.0, 0.601684479424),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0332409972299, 0.00943501366809),
                triggerBin(20.0, 0.046511627907, 0.0171041432239, 0.0130790500734),
                triggerBin(30.0, 0.0529411764706, 0.0232423956989, 0.017106729572),
                triggerBin(40.0, 0.117021276596, 0.0430921905462, 0.0337038808445),
                triggerBin(50.0, 0.196078431373, 0.071771396768, 0.0579382436591),
                triggerBin(60.0, 0.269230769231, 0.114603025448, 0.0935066525113),
                triggerBin(70.0, 0.384615384615, 0.176146427336, 0.154567226396),
                triggerBin(80.0, 0.5, 0.256909620203, 0.256909620203),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.75, 0.159659347816, 0.239566802733),
                triggerBin(140.0, 1.0, 0.0, 0.601684479424),
                triggerBin(160.0, 1.0, 0.0, 0.36887757085),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0675355450237, 0.0049871277901),
                triggerBin(20.0, 0.081452644646, 0.00308933249834, 0.00308933249834),
                triggerBin(30.0, 0.110984028277, 0.00380416045835, 0.00380416045835),
                triggerBin(40.0, 0.162643479085, 0.00483346856279, 0.00483346856279),
                triggerBin(50.0, 0.209771104145, 0.00585293738723, 0.00585293738723),
                triggerBin(60.0, 0.2759936715, 0.00704586003559, 0.00704586003559),
                triggerBin(70.0, 0.334763793693, 0.00792395217606, 0.00792395217606),
                triggerBin(80.0, 0.534999018702, 0.00651472729715, 0.00651472729715),
                triggerBin(100.0, 0.756242373487, 0.00618306789589, 0.00618306789589),
                triggerBin(120.0, 0.904043966325, 0.00471339604533, 0.00471339604533),
                triggerBin(140.0, 0.97244917971, 0.00324486631043, 0.00324486631043),
                triggerBin(160.0, 0.99939077904, 0.000601268730243, 0.000601268730243),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0675355450237, 0.0049871277901),
                triggerBin(20.0, 0.0863441488684, 0.0034303112023, 0.0034303112023),
                triggerBin(30.0, 0.109516449273, 0.00408620156063, 0.00408620156063),
                triggerBin(40.0, 0.159783321511, 0.00520868938875, 0.00520868938875),
                triggerBin(50.0, 0.224584678666, 0.00650977393665, 0.00650977393665),
                triggerBin(60.0, 0.283370318206, 0.00762189804136, 0.00762189804136),
                triggerBin(70.0, 0.354030535693, 0.00873486032707, 0.00873486032707),
                triggerBin(80.0, 0.539558402827, 0.00717242765363, 0.00717242765363),
                triggerBin(100.0, 0.749951243672, 0.00692799317635, 0.00692799317635),
                triggerBin(120.0, 0.898355367245, 0.00531909961262, 0.00531909961262),
                triggerBin(140.0, 0.966343524622, 0.00385590714891, 0.00385590714891),
                triggerBin(160.0, 0.999044661119, 0.000841491072366, 0.000841491072366),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0675355450237, 0.0049871277901),
                triggerBin(20.0, 0.0846772641736, 0.00350945836094, 0.00350945836094),
                triggerBin(30.0, 0.110508247305, 0.00422227873074, 0.00422227873074),
                triggerBin(40.0, 0.162516482535, 0.00537799237448, 0.00537799237448),
                triggerBin(50.0, 0.218919224274, 0.00663588717155, 0.00663588717155),
                triggerBin(60.0, 0.283926116419, 0.00788083679533, 0.00788083679533),
                triggerBin(70.0, 0.349418531862, 0.00895714382016, 0.00895714382016),
                triggerBin(80.0, 0.541216740369, 0.00732955474791, 0.00732955474791),
                triggerBin(100.0, 0.753333032928, 0.00705024323832, 0.00705024323832),
                triggerBin(120.0, 0.899908898918, 0.00540781678338, 0.00540781678338),
                triggerBin(140.0, 0.967692624287, 0.00390287258521, 0.00390287258521),
                triggerBin(160.0, 0.998878932019, 0.000930450783592, 0.000930450783592),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0675355450237, 0.0049871277901),
                triggerBin(20.0, 0.0859870248809, 0.00396416384568, 0.00396416384568),
                triggerBin(30.0, 0.112758902995, 0.00475552156631, 0.00475552156631),
                triggerBin(40.0, 0.164276432546, 0.00600754870337, 0.00600754870337),
                triggerBin(50.0, 0.215645453628, 0.00736175969048, 0.00736175969048),
                triggerBin(60.0, 0.283641613573, 0.00881223818705, 0.00881223818705),
                triggerBin(70.0, 0.34529985984, 0.00997827979456, 0.00997827979456),
                triggerBin(80.0, 0.543116798965, 0.00813159862543, 0.00813159862543),
                triggerBin(100.0, 0.755033769096, 0.00781420094886, 0.00781420094886),
                triggerBin(120.0, 0.898700006373, 0.00607450777369, 0.00607450777369),
                triggerBin(140.0, 0.969442387206, 0.00426318013561, 0.00426318013561),
                triggerBin(160.0, 0.998549175075, 0.001167458524, 0.001167458524),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0675355450237, 0.0049871277901),
                triggerBin(20.0, 0.0855835396954, 0.00337790882698, 0.00337790882698),
                triggerBin(30.0, 0.109744339343, 0.00404415966487, 0.00404415966487),
                triggerBin(40.0, 0.16023090499, 0.00515255795186, 0.00515255795186),
                triggerBin(50.0, 0.2222675077, 0.00640884459797, 0.00640884459797),
                triggerBin(60.0, 0.282238144744, 0.00753542115954, 0.00753542115954),
                triggerBin(70.0, 0.351004491958, 0.00861109882444, 0.00861109882444),
                triggerBin(80.0, 0.538826728369, 0.00707117287943, 0.00707117287943),
                triggerBin(100.0, 0.750975271955, 0.00681087910207, 0.00681087910207),
                triggerBin(120.0, 0.899265661111, 0.00522386009792, 0.00522386009792),
                triggerBin(140.0, 0.967288990036, 0.00376169318062, 0.00376169318062),
                triggerBin(160.0, 0.999101503794, 0.000802573245846, 0.000802573245846),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0675355450237, 0.0049871277901),
                triggerBin(20.0, 0.0850830670492, 0.00345152997215, 0.00345152997215),
                triggerBin(30.0, 0.110167321594, 0.00414348269749, 0.00414348269749),
                triggerBin(40.0, 0.161499757036, 0.00527837242781, 0.00527837242781),
                triggerBin(50.0, 0.220413860863, 0.00653626303274, 0.00653626303274),
                triggerBin(60.0, 0.283170371048, 0.00772779689462, 0.00772779689462),
                triggerBin(70.0, 0.350126506073, 0.00880450771094, 0.00880450771094),
                triggerBin(80.0, 0.540154279068, 0.00721592950466, 0.00721592950466),
                triggerBin(100.0, 0.752283288036, 0.00694514282432, 0.00694514282432),
                triggerBin(120.0, 0.899622764552, 0.00532701257675, 0.00532701257675),
                triggerBin(140.0, 0.967512061395, 0.00384079702681, 0.00384079702681),
                triggerBin(160.0, 0.998978007474, 0.000874105466696, 0.000874105466696),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0675355450237, 0.0049871277901),
                triggerBin(20.0, 0.0859870248809, 0.00396416384568, 0.00396416384568),
                triggerBin(30.0, 0.112758902995, 0.00475552156631, 0.00475552156631),
                triggerBin(40.0, 0.164276432546, 0.00600754870337, 0.00600754870337),
                triggerBin(50.0, 0.215645453628, 0.00736175969048, 0.00736175969048),
                triggerBin(60.0, 0.283641613573, 0.00881223818705, 0.00881223818705),
                triggerBin(70.0, 0.34529985984, 0.00997827979456, 0.00997827979456),
                triggerBin(80.0, 0.543116798965, 0.00813159862543, 0.00813159862543),
                triggerBin(100.0, 0.755033769096, 0.00781420094886, 0.00781420094886),
                triggerBin(120.0, 0.898700006373, 0.00607450777369, 0.00607450777369),
                triggerBin(140.0, 0.969442387206, 0.00426318013561, 0.00426318013561),
                triggerBin(160.0, 0.998549175075, 0.001167458524, 0.001167458524),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0675355450237, 0.0049871277901),
                triggerBin(20.0, 0.0956014362657, 0.00664219642322, 0.00626619413506),
                triggerBin(30.0, 0.121316306483, 0.00767333241216, 0.00728882451693),
                triggerBin(40.0, 0.171637591446, 0.0094153438037, 0.0090342737887),
                triggerBin(50.0, 0.219054242003, 0.0114533883386, 0.0110503536762),
                triggerBin(60.0, 0.295901639344, 0.0136453479655, 0.0133004391334),
                triggerBin(70.0, 0.356862745098, 0.0156280076669, 0.0153383490338),
                triggerBin(80.0, 0.554140127389, 0.0122146900873, 0.0122788834236),
                triggerBin(100.0, 0.755970149254, 0.0119058341521, 0.0122998519526),
                triggerBin(120.0, 0.887773722628, 0.00961964071935, 0.0103607338483),
                triggerBin(140.0, 0.964432284542, 0.0068496508505, 0.00824623627951),
                triggerBin(160.0, 0.995975855131, 0.00259880537061, 0.00528282546359),
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

    # Used input: multicrab_MetLeg2012_130517_110812

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.2, 0.1788854382),
                triggerBin(20.0, 0.166666666667, 0.287350389332, 0.138284918684),
                triggerBin(30.0, 0.0, 0.458641675296, 0.0),
                triggerBin(40.0, 0.0, 0.841344746068, 0.0),
                triggerBin(50.0, 1.0, 0.0, 0.841344746068),
                triggerBin(60.0, 0.0, 1.0, 0.0),
                triggerBin(70.0, 1.0, 0.0, 0.601684479424),
                triggerBin(80.0, 0.0, 1.0, 0.0),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0506329113924, 0.0246672076884),
                triggerBin(20.0, 0.0491803278689, 0.0455330494696, 0.0266469956784),
                triggerBin(30.0, 0.0888888888889, 0.064719960598, 0.042052521739),
                triggerBin(40.0, 0.2, 0.157061286074, 0.10675070638),
                triggerBin(50.0, 0.0909090909091, 0.179295209474, 0.0753268806181),
                triggerBin(60.0, 0.285714285714, 0.259937875571, 0.182129028008),
                triggerBin(70.0, 0.0, 0.841344746068, 0.0),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.0, 0.601684479424, 0.0),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0315789473684, 0.0179419289732),
                triggerBin(20.0, 0.047619047619, 0.0360513607022, 0.0226519839091),
                triggerBin(30.0, 0.0392156862745, 0.0493938932952, 0.0252892452443),
                triggerBin(40.0, 0.0909090909091, 0.0805904491223, 0.049063192669),
                triggerBin(50.0, 0.25, 0.184899566147, 0.132706908337),
                triggerBin(60.0, 0.222222222222, 0.221429368878, 0.14211823823),
                triggerBin(70.0, 0.5, 0.256909620203, 0.256909620203),
                triggerBin(80.0, 0.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 1.0, 0.0, 0.841344746068),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.03125, 0.0153789216289),
                triggerBin(20.0, 0.0375, 0.03513458966, 0.0203401601691),
                triggerBin(30.0, 0.0350877192982, 0.0444119674392, 0.0226310911763),
                triggerBin(40.0, 0.131578947368, 0.0792158922547, 0.0556305565753),
                triggerBin(50.0, 0.235294117647, 0.147311672312, 0.108959165741),
                triggerBin(60.0, 0.3, 0.20826248199, 0.158328098893),
                triggerBin(70.0, 0.0, 0.36887757085, 0.0),
                triggerBin(80.0, 0.0, 0.458641675296, 0.0),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.458641675296),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0595238095238, 0.0258154451793),
                triggerBin(20.0, 0.0597014925373, 0.0446914097028, 0.0283545955351),
                triggerBin(30.0, 0.0833333333333, 0.0609994410026, 0.0394538529141),
                triggerBin(40.0, 0.1875, 0.149398565056, 0.100212028831),
                triggerBin(50.0, 0.166666666667, 0.179009937646, 0.106875367754),
                triggerBin(60.0, 0.285714285714, 0.259937875571, 0.182129028008),
                triggerBin(70.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0446927374302, 0.0154441319064),
                triggerBin(20.0, 0.0529801324503, 0.0250907982925, 0.018126668258),
                triggerBin(30.0, 0.0606060606061, 0.0344454501331, 0.0237787283297),
                triggerBin(40.0, 0.122448979592, 0.06597268204, 0.0474774607725),
                triggerBin(50.0, 0.208333333333, 0.116379172568, 0.086867737525),
                triggerBin(60.0, 0.25, 0.153966037382, 0.115498745679),
                triggerBin(70.0, 0.555555555556, 0.198267144951, 0.213462824948),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.5, 0.314698893873, 0.314698893873),
                triggerBin(140.0, 1.0, 0.0, 0.841344746068),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0390879478827, 0.0110609917346),
                triggerBin(20.0, 0.047619047619, 0.0184786643575, 0.0139696084467),
                triggerBin(30.0, 0.0512820512821, 0.0243188284978, 0.0175522352879),
                triggerBin(40.0, 0.126436781609, 0.0462169137562, 0.0363210989057),
                triggerBin(50.0, 0.219512195122, 0.0839616158399, 0.067970007356),
                triggerBin(60.0, 0.269230769231, 0.114603025448, 0.0935066525113),
                triggerBin(70.0, 0.384615384615, 0.176146427336, 0.154567226396),
                triggerBin(80.0, 0.4, 0.303366136254, 0.25334762525),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.714285714286, 0.182129028008, 0.259937875571),
                triggerBin(140.0, 1.0, 0.0, 0.841344746068),
                triggerBin(160.0, 1.0, 0.0, 0.36887757085),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0663677130045, 0.00527125378313),
                triggerBin(20.0, 0.0765205387126, 0.00319487647594, 0.00319487647594),
                triggerBin(30.0, 0.111601802498, 0.00407090634798, 0.00407090634798),
                triggerBin(40.0, 0.150382572911, 0.00491628093078, 0.00491628093078),
                triggerBin(50.0, 0.204117062657, 0.00611136061157, 0.00611136061157),
                triggerBin(60.0, 0.279387043953, 0.00738685917911, 0.00738685917911),
                triggerBin(70.0, 0.341066971339, 0.00828315913306, 0.00828315913306),
                triggerBin(80.0, 0.537703023128, 0.00674146106578, 0.00674146106578),
                triggerBin(100.0, 0.753058213305, 0.00650519777844, 0.00650519777844),
                triggerBin(120.0, 0.901589328294, 0.00495312989496, 0.00495312989496),
                triggerBin(140.0, 0.97100995209, 0.00346431775987, 0.00346431775987),
                triggerBin(160.0, 0.999318537838, 0.000672502646306, 0.000672502646306),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0663677130045, 0.00527125378313),
                triggerBin(20.0, 0.0804424907522, 0.00354649147749, 0.00354649147749),
                triggerBin(30.0, 0.112188771441, 0.00443788325097, 0.00443788325097),
                triggerBin(40.0, 0.1487218311, 0.00533831272969, 0.00533831272969),
                triggerBin(50.0, 0.219661428569, 0.00681857007949, 0.00681857007949),
                triggerBin(60.0, 0.282535760304, 0.00795734249218, 0.00795734249218),
                triggerBin(70.0, 0.357813030059, 0.0091173488258, 0.0091173488258),
                triggerBin(80.0, 0.541645821851, 0.00743454882215, 0.00743454882215),
                triggerBin(100.0, 0.748346286289, 0.00731189804724, 0.00731189804724),
                triggerBin(120.0, 0.900383460406, 0.00547308598274, 0.00547308598274),
                triggerBin(140.0, 0.963563871883, 0.00421773161356, 0.00421773161356),
                triggerBin(160.0, 0.998939305982, 0.000934153255664, 0.000934153255664),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0663677130045, 0.00527125378313),
                triggerBin(20.0, 0.0794992993759, 0.00363404532676, 0.00363404532676),
                triggerBin(30.0, 0.112456872142, 0.00456083933792, 0.00456083933792),
                triggerBin(40.0, 0.151161492212, 0.0055044768863, 0.0055044768863),
                triggerBin(50.0, 0.214347631511, 0.00695697583213, 0.00695697583213),
                triggerBin(60.0, 0.284424439679, 0.00824033201403, 0.00824033201403),
                triggerBin(70.0, 0.353543266553, 0.00934775927037, 0.00934775927037),
                triggerBin(80.0, 0.543002089115, 0.00759102155208, 0.00759102155208),
                triggerBin(100.0, 0.75197456319, 0.00742891671822, 0.00742891671822),
                triggerBin(120.0, 0.900344925754, 0.0056069424134, 0.0056069424134),
                triggerBin(140.0, 0.965502491622, 0.00422571758814, 0.00422571758814),
                triggerBin(160.0, 0.998750959991, 0.00103659708993, 0.00103659708993),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0663677130045, 0.00527125378313),
                triggerBin(20.0, 0.0816939800224, 0.00412525299278, 0.00412525299278),
                triggerBin(30.0, 0.114486035287, 0.00511973450976, 0.00511973450976),
                triggerBin(40.0, 0.154218754317, 0.00616776629222, 0.00616776629222),
                triggerBin(50.0, 0.211149397474, 0.00772283165263, 0.00772283165263),
                triggerBin(60.0, 0.285145851985, 0.00923043177744, 0.00923043177744),
                triggerBin(70.0, 0.34853827422, 0.0104129475562, 0.0104129475562),
                triggerBin(80.0, 0.544254218945, 0.00842365323873, 0.00842365323873),
                triggerBin(100.0, 0.75395425102, 0.00822604749968, 0.00822604749968),
                triggerBin(120.0, 0.897014605053, 0.00636891194491, 0.00636891194491),
                triggerBin(140.0, 0.967707049046, 0.00458394146922, 0.00458394146922),
                triggerBin(160.0, 0.998390176124, 0.00129522276556, 0.00129522276556),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0663677130045, 0.00527125378313),
                triggerBin(20.0, 0.0798291872028, 0.00349229224861, 0.00349229224861),
                triggerBin(30.0, 0.112096631671, 0.00438208257401, 0.00438208257401),
                triggerBin(40.0, 0.148983893972, 0.00527449261498, 0.00527449261498),
                triggerBin(50.0, 0.217226012371, 0.00670967826874, 0.00670967826874),
                triggerBin(60.0, 0.282052138351, 0.00787195331973, 0.00787195331973),
                triggerBin(70.0, 0.355179783066, 0.00898993085772, 0.00898993085772),
                triggerBin(80.0, 0.541011286076, 0.00732760291088, 0.00732760291088),
                triggerBin(100.0, 0.749120567139, 0.00718444481533, 0.00718444481533),
                triggerBin(120.0, 0.900575971952, 0.0053926765085, 0.0053926765085),
                triggerBin(140.0, 0.964737554318, 0.00409954423546, 0.00409954423546),
                triggerBin(160.0, 0.999001297009, 0.000892037272086, 0.000892037272086),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0663677130045, 0.00527125378313),
                triggerBin(20.0, 0.0796468062726, 0.00357150069182, 0.00357150069182),
                triggerBin(30.0, 0.112296413236, 0.00448195237111, 0.00448195237111),
                triggerBin(40.0, 0.150193205242, 0.00540286451975, 0.00540286451975),
                triggerBin(50.0, 0.215633766775, 0.00684830149687, 0.00684830149687),
                triggerBin(60.0, 0.283362063475, 0.00807701988686, 0.00807701988686),
                triggerBin(70.0, 0.354273479314, 0.00918997466796, 0.00918997466796),
                triggerBin(80.0, 0.542117388349, 0.00747522997488, 0.00747522997488),
                triggerBin(100.0, 0.750704275093, 0.00732170154299, 0.00732170154299),
                triggerBin(120.0, 0.900447906914, 0.00551245958222, 0.00551245958222),
                triggerBin(140.0, 0.96516098183, 0.00417071172546, 0.00417071172546),
                triggerBin(160.0, 0.998862540333, 0.000972807750652, 0.000972807750652),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0663677130045, 0.00527125378313),
                triggerBin(20.0, 0.0816939800224, 0.00412525299278, 0.00412525299278),
                triggerBin(30.0, 0.114486035287, 0.00511973450976, 0.00511973450976),
                triggerBin(40.0, 0.154218754317, 0.00616776629222, 0.00616776629222),
                triggerBin(50.0, 0.211149397474, 0.00772283165263, 0.00772283165263),
                triggerBin(60.0, 0.285145851985, 0.00923043177744, 0.00923043177744),
                triggerBin(70.0, 0.34853827422, 0.0104129475562, 0.0104129475562),
                triggerBin(80.0, 0.544254218945, 0.00842365323873, 0.00842365323873),
                triggerBin(100.0, 0.75395425102, 0.00822604749968, 0.00822604749968),
                triggerBin(120.0, 0.897014605053, 0.00636891194491, 0.00636891194491),
                triggerBin(140.0, 0.967707049046, 0.00458394146922, 0.00458394146922),
                triggerBin(160.0, 0.998390176124, 0.00129522276556, 0.00129522276556),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0663677130045, 0.00527125378313),
                triggerBin(20.0, 0.0917899031107, 0.00699169720001, 0.0065592053661),
                triggerBin(30.0, 0.124649073554, 0.00832566536269, 0.00788917862034),
                triggerBin(40.0, 0.168341708543, 0.0099054018637, 0.00947494879543),
                triggerBin(50.0, 0.218238503507, 0.0121448277718, 0.0116909725155),
                triggerBin(60.0, 0.294918330309, 0.0143766687102, 0.0139923882647),
                triggerBin(70.0, 0.357219251337, 0.0163549792919, 0.0160393514165),
                triggerBin(80.0, 0.553894080997, 0.0126808888154, 0.0127497063967),
                triggerBin(100.0, 0.757650951199, 0.0125129236524, 0.0129532293964),
                triggerBin(120.0, 0.883233532934, 0.0102424232886, 0.0110445290661),
                triggerBin(140.0, 0.962292609351, 0.00739915877272, 0.00893466077509),
                triggerBin(160.0, 0.995604395604, 0.00283865275491, 0.00576797924539),
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

    # Used input: multicrab_MetLeg2012_130517_110812

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0714285714286, 0.0688302936899),
                triggerBin(20.0, 0.0909090909091, 0.179295209474, 0.0753268806181),
                triggerBin(30.0, 0.0, 0.36887757085, 0.0),
                triggerBin(40.0, 0.0, 0.841344746068, 0.0),
                triggerBin(50.0, 1.0, 0.0, 0.841344746068),
                triggerBin(60.0, 0.0, 1.0, 0.0),
                triggerBin(70.0, 1.0, 0.0, 0.601684479424),
                triggerBin(80.0, 0.0, 1.0, 0.0),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0335570469799, 0.014753220915),
                triggerBin(20.0, 0.0388349514563, 0.0296413099588, 0.0184945174852),
                triggerBin(30.0, 0.0609756097561, 0.0391439922963, 0.0260867261305),
                triggerBin(40.0, 0.135135135135, 0.0810851922564, 0.0570987615161),
                triggerBin(50.0, 0.161290322581, 0.0943938992063, 0.0678360239621),
                triggerBin(60.0, 0.4, 0.204596854236, 0.180009253894),
                triggerBin(70.0, 0.0, 0.841344746068, 0.0),
                triggerBin(80.0, 1.0, 0.0, 0.458641675296),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0309278350515, 0.0124294512387),
                triggerBin(20.0, 0.0308641975309, 0.0203396530446, 0.0132679006318),
                triggerBin(30.0, 0.06, 0.0341183623328, 0.0235435867755),
                triggerBin(40.0, 0.0634920634921, 0.0473598474317, 0.0301398055994),
                triggerBin(50.0, 0.12, 0.103114634532, 0.0645799596342),
                triggerBin(60.0, 0.266666666667, 0.161145049639, 0.122866921165),
                triggerBin(70.0, 0.5, 0.220457375638, 0.220457375638),
                triggerBin(80.0, 0.5, 0.41724846474, 0.41724846474),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0215517241379, 0.00953379816409),
                triggerBin(20.0, 0.0487804878049, 0.0231776876734, 0.0167051922328),
                triggerBin(30.0, 0.0578512396694, 0.0297701883604, 0.0210904293882),
                triggerBin(40.0, 0.116883116883, 0.0488003111809, 0.0371884583537),
                triggerBin(50.0, 0.135135135135, 0.0810851922564, 0.0570987615161),
                triggerBin(60.0, 0.263157894737, 0.138819970242, 0.108565019101),
                triggerBin(70.0, 0.166666666667, 0.287350389332, 0.138284918684),
                triggerBin(80.0, 0.2, 0.324250626004, 0.16603930634),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.458641675296),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0, 0.458641675296),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0368098159509, 0.014748370691),
                triggerBin(20.0, 0.0438596491228, 0.0285810165484, 0.0188157050399),
                triggerBin(30.0, 0.0581395348837, 0.0374166301655, 0.024884782787),
                triggerBin(40.0, 0.131578947368, 0.0792158922547, 0.0556305565753),
                triggerBin(50.0, 0.1875, 0.0951654963661, 0.0717391962659),
                triggerBin(60.0, 0.4, 0.204596854236, 0.180009253894),
                triggerBin(70.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(80.0, 1.0, 0.0, 0.458641675296),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.5, 0.314698893873, 0.314698893873),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0336134453782, 0.00953889012623),
                triggerBin(20.0, 0.036231884058, 0.0150593556177, 0.0111667137113),
                triggerBin(30.0, 0.0591397849462, 0.022755891775, 0.0172980263453),
                triggerBin(40.0, 0.0891089108911, 0.0380389959459, 0.0285463037648),
                triggerBin(50.0, 0.157894736842, 0.0637264282034, 0.0497130664879),
                triggerBin(60.0, 0.32, 0.119275761539, 0.102271514956),
                triggerBin(70.0, 0.545454545455, 0.1795821324, 0.189661990926),
                triggerBin(80.0, 0.8, 0.16603930634, 0.324250626004),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.6, 0.25334762525, 0.303366136254),
                triggerBin(140.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0288624787776, 0.00689841842266),
                triggerBin(20.0, 0.0409090909091, 0.0117710975327, 0.00943624491951),
                triggerBin(30.0, 0.0586319218241, 0.0166691379962, 0.0134508692194),
                triggerBin(40.0, 0.101123595506, 0.027909603445, 0.022888738487),
                triggerBin(50.0, 0.148936170213, 0.0461538807695, 0.0376626274674),
                triggerBin(60.0, 0.295454545455, 0.0845305778572, 0.0738629419477),
                triggerBin(70.0, 0.411764705882, 0.149770451815, 0.137360513174),
                triggerBin(80.0, 0.5, 0.195182116991, 0.195182116991),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.75, 0.159659347816, 0.239566802733),
                triggerBin(140.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(160.0, 1.0, 0.0, 0.308024223477),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0687215765538, 0.00402113295289),
                triggerBin(20.0, 0.0824343241069, 0.00249423795213, 0.00249423795213),
                triggerBin(30.0, 0.122494632112, 0.003221688948, 0.003221688948),
                triggerBin(40.0, 0.166964514644, 0.0040594696832, 0.0040594696832),
                triggerBin(50.0, 0.217529318927, 0.00496942939937, 0.00496942939937),
                triggerBin(60.0, 0.273564297288, 0.00597517916718, 0.00597517916718),
                triggerBin(70.0, 0.327320267329, 0.00675786796614, 0.00675786796614),
                triggerBin(80.0, 0.516703636109, 0.00564373986723, 0.00564373986723),
                triggerBin(100.0, 0.751288543409, 0.00546784322895, 0.00546784322895),
                triggerBin(120.0, 0.905411298823, 0.00415767413489, 0.00415767413489),
                triggerBin(140.0, 0.977562088286, 0.00258602427126, 0.00258602427126),
                triggerBin(160.0, 0.999500033664, 0.000493408500769, 0.000493408500769),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0687215765538, 0.00402113295289),
                triggerBin(20.0, 0.0850491375961, 0.00274116673041, 0.00274116673041),
                triggerBin(30.0, 0.122713196991, 0.00348152868117, 0.00348152868117),
                triggerBin(40.0, 0.163961315229, 0.00436108682551, 0.00436108682551),
                triggerBin(50.0, 0.232335004412, 0.00555943136978, 0.00555943136978),
                triggerBin(60.0, 0.284415983365, 0.00654834817329, 0.00654834817329),
                triggerBin(70.0, 0.343907796532, 0.00747326765118, 0.00747326765118),
                triggerBin(80.0, 0.523578737814, 0.00623246589037, 0.00623246589037),
                triggerBin(100.0, 0.750542714778, 0.00607390890239, 0.00607390890239),
                triggerBin(120.0, 0.904787261379, 0.00454471899982, 0.00454471899982),
                triggerBin(140.0, 0.97230765863, 0.00309521346148, 0.00309521346148),
                triggerBin(160.0, 0.999238491762, 0.000670808426214, 0.000670808426214),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0687215765538, 0.00402113295289),
                triggerBin(20.0, 0.0842498284938, 0.00281203596302, 0.00281203596302),
                triggerBin(30.0, 0.122610199852, 0.00358269770135, 0.00358269770135),
                triggerBin(40.0, 0.166430859664, 0.00450701808771, 0.00450701808771),
                triggerBin(50.0, 0.226695406912, 0.00565210299354, 0.00565210299354),
                triggerBin(60.0, 0.284115906705, 0.00673901518115, 0.00673901518115),
                triggerBin(70.0, 0.340253177518, 0.0076471063624, 0.0076471063624),
                triggerBin(80.0, 0.524501647331, 0.00636426886834, 0.00636426886834),
                triggerBin(100.0, 0.752179166199, 0.00619644791154, 0.00619644791154),
                triggerBin(120.0, 0.904243640566, 0.00468200341825, 0.00468200341825),
                triggerBin(140.0, 0.973172055273, 0.00314369591676, 0.00314369591676),
                triggerBin(160.0, 0.999099349553, 0.000747562243148, 0.000747562243148),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0687215765538, 0.00402113295289),
                triggerBin(20.0, 0.0858680627557, 0.00317494113324, 0.00317494113324),
                triggerBin(30.0, 0.123475689251, 0.0040151413447, 0.0040151413447),
                triggerBin(40.0, 0.168929654157, 0.00505145732388, 0.00505145732388),
                triggerBin(50.0, 0.222887750949, 0.00626470333595, 0.00626470333595),
                triggerBin(60.0, 0.284016529621, 0.00752849984224, 0.00752849984224),
                triggerBin(70.0, 0.339469722934, 0.00853717147856, 0.00853717147856),
                triggerBin(80.0, 0.527130380001, 0.00706014334584, 0.00706014334584),
                triggerBin(100.0, 0.753089830436, 0.00688716059435, 0.00688716059435),
                triggerBin(120.0, 0.901506791985, 0.00531209142164, 0.00531209142164),
                triggerBin(140.0, 0.973944224544, 0.00347658929743, 0.00347658929743),
                triggerBin(160.0, 0.998834286339, 0.000938093170826, 0.000938093170826),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0687215765538, 0.00402113295289),
                triggerBin(20.0, 0.0846411819218, 0.00270338182753, 0.00270338182753),
                triggerBin(30.0, 0.122679313405, 0.00344245659363, 0.00344245659363),
                triggerBin(40.0, 0.164428941117, 0.00431615182741, 0.00431615182741),
                triggerBin(50.0, 0.229991167986, 0.00546792402542, 0.00546792402542),
                triggerBin(60.0, 0.282724276836, 0.00646107457142, 0.00646107457142),
                triggerBin(70.0, 0.341283824149, 0.00736334712743, 0.00736334712743),
                triggerBin(80.0, 0.522470310595, 0.00614151749256, 0.00614151749256),
                triggerBin(100.0, 0.750662745614, 0.00597949824845, 0.00597949824845),
                triggerBin(120.0, 0.904885580307, 0.00448566647653, 0.00448566647653),
                triggerBin(140.0, 0.973123470333, 0.00301646865129, 0.00301646865129),
                triggerBin(160.0, 0.999280418942, 0.000642816529209, 0.000642816529209),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0687215765538, 0.00402113295289),
                triggerBin(20.0, 0.0844247824193, 0.00276411186916, 0.00276411186916),
                triggerBin(30.0, 0.122641056762, 0.00352080503877, 0.00352080503877),
                triggerBin(40.0, 0.165538983749, 0.00442261484031, 0.00442261484031),
                triggerBin(50.0, 0.228163114692, 0.00557139262228, 0.00557139262228),
                triggerBin(60.0, 0.283494382449, 0.00661614130743, 0.00661614130743),
                triggerBin(70.0, 0.340712394584, 0.00752210531491, 0.00752210531491),
                triggerBin(80.0, 0.523598483806, 0.00626632554634, 0.00626632554634),
                triggerBin(100.0, 0.751504643496, 0.00610106391426, 0.00610106391426),
                triggerBin(120.0, 0.904529751511, 0.00459517011307, 0.00459517011307),
                triggerBin(140.0, 0.973149904143, 0.00308750120007, 0.00308750120007),
                triggerBin(160.0, 0.999180129031, 0.000701302772636, 0.000701302772636),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0687215765538, 0.00402113295289),
                triggerBin(20.0, 0.0858680627557, 0.00317494113324, 0.00317494113324),
                triggerBin(30.0, 0.123475689251, 0.0040151413447, 0.0040151413447),
                triggerBin(40.0, 0.168929654157, 0.00505145732388, 0.00505145732388),
                triggerBin(50.0, 0.222887750949, 0.00626470333595, 0.00626470333595),
                triggerBin(60.0, 0.284016529621, 0.00752849984224, 0.00752849984224),
                triggerBin(70.0, 0.339469722934, 0.00853717147856, 0.00853717147856),
                triggerBin(80.0, 0.527130380001, 0.00706014334584, 0.00706014334584),
                triggerBin(100.0, 0.753089830436, 0.00688716059435, 0.00688716059435),
                triggerBin(120.0, 0.901506791985, 0.00531209142164, 0.00531209142164),
                triggerBin(140.0, 0.973944224544, 0.00347658929743, 0.00347658929743),
                triggerBin(160.0, 0.998834286339, 0.000938093170826, 0.000938093170826),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0687215765538, 0.00402113295289),
                triggerBin(20.0, 0.0946255002859, 0.00521120632747, 0.00497277265185),
                triggerBin(30.0, 0.12833008447, 0.00631465187088, 0.00606668812704),
                triggerBin(40.0, 0.179447255742, 0.00789248151542, 0.00763656926907),
                triggerBin(50.0, 0.224078624079, 0.00962641715554, 0.00934811425043),
                triggerBin(60.0, 0.301094890511, 0.0117389711758, 0.0114905809053),
                triggerBin(70.0, 0.361393323657, 0.0134029311115, 0.0131962117459),
                triggerBin(80.0, 0.545335658239, 0.0105917844061, 0.0106321277292),
                triggerBin(100.0, 0.757876312719, 0.0104815638909, 0.010790845358),
                triggerBin(120.0, 0.888172043011, 0.00850616856758, 0.00908609525788),
                triggerBin(140.0, 0.967195767196, 0.00579446458572, 0.00687299099842),
                triggerBin(160.0, 0.996845425868, 0.0020373049585, 0.0041454558768),
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

    # Used input: multicrab_MetLeg2012_130517_110812

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.166666666667, 0.152145154863),
                triggerBin(20.0, 0.142857142857, 0.257123832984, 0.118480071045),
                triggerBin(30.0, 0.0, 0.458641675296, 0.0),
                triggerBin(40.0, 0.0, 0.841344746068, 0.0),
                triggerBin(50.0, 1.0, 0.0, 0.841344746068),
                triggerBin(60.0, 0.0, 1.0, 0.0),
                triggerBin(70.0, 1.0, 0.0, 0.601684479424),
                triggerBin(80.0, 0.0, 1.0, 0.0),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0434782608696, 0.0212612889966),
                triggerBin(20.0, 0.0441176470588, 0.0410575957313, 0.0239150832448),
                triggerBin(30.0, 0.1, 0.0619892518934, 0.0425078913818),
                triggerBin(40.0, 0.166666666667, 0.135998901491, 0.0892717907981),
                triggerBin(50.0, 0.142857142857, 0.158270654649, 0.0917088958422),
                triggerBin(60.0, 0.285714285714, 0.259937875571, 0.182129028008),
                triggerBin(70.0, 0.0, 0.841344746068, 0.0),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0265486725664, 0.0151230470988),
                triggerBin(20.0, 0.0425531914894, 0.0323678650094, 0.0202555238052),
                triggerBin(30.0, 0.0377358490566, 0.0476137480969, 0.0243364286652),
                triggerBin(40.0, 0.0833333333333, 0.074467426805, 0.045007246588),
                triggerBin(50.0, 0.1875, 0.149398565056, 0.100212028831),
                triggerBin(60.0, 0.222222222222, 0.221429368878, 0.14211823823),
                triggerBin(70.0, 0.5, 0.256909620203, 0.256909620203),
                triggerBin(80.0, 1.0, 0.0, 0.841344746068),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 1.0, 0.0, 0.601684479424),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0266666666667, 0.0131543542995),
                triggerBin(20.0, 0.0449438202247, 0.0341106344125, 0.0213868402105),
                triggerBin(30.0, 0.03125, 0.0397347958314, 0.0201590096415),
                triggerBin(40.0, 0.128205128205, 0.0774292319421, 0.0542358310136),
                triggerBin(50.0, 0.2, 0.130118869123, 0.0931224604655),
                triggerBin(60.0, 0.3, 0.20826248199, 0.158328098893),
                triggerBin(70.0, 0.0, 0.36887757085, 0.0),
                triggerBin(80.0, 0.0, 0.458641675296, 0.0),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.458641675296),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0510204081633, 0.0222273333556),
                triggerBin(20.0, 0.0533333333333, 0.0401631110859, 0.0253512991407),
                triggerBin(30.0, 0.0943396226415, 0.0587823296232, 0.0401398467978),
                triggerBin(40.0, 0.157894736842, 0.130121162629, 0.0846498044596),
                triggerBin(50.0, 0.2, 0.157061286074, 0.10675070638),
                triggerBin(60.0, 0.285714285714, 0.259937875571, 0.182129028008),
                triggerBin(70.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.5, 0.314698893873, 0.314698893873),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0379146919431, 0.0131482916696),
                triggerBin(20.0, 0.0473372781065, 0.0225172257675, 0.0162160781563),
                triggerBin(30.0, 0.0660377358491, 0.0337580471231, 0.0240344740711),
                triggerBin(40.0, 0.109090909091, 0.0594733255375, 0.0424090752596),
                triggerBin(50.0, 0.193548387097, 0.0976717076465, 0.0739582576944),
                triggerBin(60.0, 0.25, 0.153966037382, 0.115498745679),
                triggerBin(70.0, 0.555555555556, 0.198267144951, 0.213462824948),
                triggerBin(80.0, 1.0, 0.0, 0.458641675296),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.6, 0.25334762525, 0.303366136254),
                triggerBin(140.0, 1.0, 0.0, 0.601684479424),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0332409972299, 0.00943501366809),
                triggerBin(20.0, 0.046511627907, 0.0171041432239, 0.0130790500734),
                triggerBin(30.0, 0.0529411764706, 0.0232423956989, 0.017106729572),
                triggerBin(40.0, 0.117021276596, 0.0430921905462, 0.0337038808445),
                triggerBin(50.0, 0.196078431373, 0.071771396768, 0.0579382436591),
                triggerBin(60.0, 0.269230769231, 0.114603025448, 0.0935066525113),
                triggerBin(70.0, 0.384615384615, 0.176146427336, 0.154567226396),
                triggerBin(80.0, 0.5, 0.256909620203, 0.256909620203),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.75, 0.159659347816, 0.239566802733),
                triggerBin(140.0, 1.0, 0.0, 0.601684479424),
                triggerBin(160.0, 1.0, 0.0, 0.36887757085),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0675889328063, 0.00499092730096),
                triggerBin(20.0, 0.0810920711424, 0.00308487901841, 0.00308487901841),
                triggerBin(30.0, 0.109224241702, 0.00378596256007, 0.00378596256007),
                triggerBin(40.0, 0.162040224964, 0.00483033057041, 0.00483033057041),
                triggerBin(50.0, 0.211013092585, 0.00588629346856, 0.00588629346856),
                triggerBin(60.0, 0.27634978966, 0.00705345910355, 0.00705345910355),
                triggerBin(70.0, 0.334632987335, 0.00792396180521, 0.00792396180521),
                triggerBin(80.0, 0.532763172554, 0.00653238131239, 0.00653238131239),
                triggerBin(100.0, 0.756084688307, 0.00618642261066, 0.00618642261066),
                triggerBin(120.0, 0.90404401685, 0.00471339669314, 0.00471339669314),
                triggerBin(140.0, 0.97244917971, 0.00324486631043, 0.00324486631043),
                triggerBin(160.0, 0.999386797903, 0.000605160696631, 0.000605160696631),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0675889328063, 0.00499092730096),
                triggerBin(20.0, 0.0860960474266, 0.00342762029125, 0.00342762029125),
                triggerBin(30.0, 0.108481872328, 0.00408181211506, 0.00408181211506),
                triggerBin(40.0, 0.159201445519, 0.00520469047415, 0.00520469047415),
                triggerBin(50.0, 0.22521519997, 0.00653731703093, 0.00653731703093),
                triggerBin(60.0, 0.283471866471, 0.00762837204348, 0.00762837204348),
                triggerBin(70.0, 0.353772079755, 0.00873516516486, 0.00873516516486),
                triggerBin(80.0, 0.537033165433, 0.00719567090399, 0.00719567090399),
                triggerBin(100.0, 0.749703215419, 0.00693372070608, 0.00693372070608),
                triggerBin(120.0, 0.898352400464, 0.00531924232594, 0.00531924232594),
                triggerBin(140.0, 0.966343524622, 0.00385590714891, 0.00385590714891),
                triggerBin(160.0, 0.999039739581, 0.000845743892552, 0.000845743892552),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0675889328063, 0.00499092730096),
                triggerBin(20.0, 0.0843902554698, 0.00350616666244, 0.00350616666244),
                triggerBin(30.0, 0.10929718959, 0.00421303594008, 0.00421303594008),
                triggerBin(40.0, 0.161910315298, 0.00537410349119, 0.00537410349119),
                triggerBin(50.0, 0.219624913782, 0.00666686590285, 0.00666686590285),
                triggerBin(60.0, 0.284058976437, 0.00788809794969, 0.00788809794969),
                triggerBin(70.0, 0.349131110578, 0.00895741471273, 0.00895741471273),
                triggerBin(80.0, 0.538884439268, 0.00735192294688, 0.00735192294688),
                triggerBin(100.0, 0.753079188394, 0.00705630947638, 0.00705630947638),
                triggerBin(120.0, 0.899901051618, 0.00540822147914, 0.00540822147914),
                triggerBin(140.0, 0.967692624287, 0.00390287258521, 0.00390287258521),
                triggerBin(160.0, 0.998873111116, 0.000935279222727, 0.000935279222727),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0675889328063, 0.00499092730096),
                triggerBin(20.0, 0.085690243183, 0.00396066096174, 0.00396066096174),
                triggerBin(30.0, 0.111344188892, 0.00473959826159, 0.00473959826159),
                triggerBin(40.0, 0.163588103551, 0.00600278876322, 0.00600278876322),
                triggerBin(50.0, 0.215828868955, 0.0073897217753, 0.0073897217753),
                triggerBin(60.0, 0.28361545275, 0.00882127258299, 0.00882127258299),
                triggerBin(70.0, 0.344894211893, 0.00997859737558, 0.00997859737558),
                triggerBin(80.0, 0.541027863656, 0.0081556570596, 0.0081556570596),
                triggerBin(100.0, 0.75470971142, 0.00782285878337, 0.00782285878337),
                triggerBin(120.0, 0.898675399807, 0.00607590574946, 0.00607590574946),
                triggerBin(140.0, 0.969442387206, 0.00426318013561, 0.00426318013561),
                triggerBin(160.0, 0.998541913018, 0.00117320513246, 0.00117320513246),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0675889328063, 0.00499092730096),
                triggerBin(20.0, 0.0853180222541, 0.00337493496228, 0.00337493496228),
                triggerBin(30.0, 0.108597342131, 0.00403746717209, 0.00403746717209),
                triggerBin(40.0, 0.159645557426, 0.00514869561035, 0.00514869561035),
                triggerBin(50.0, 0.222994762566, 0.00643735081128, 0.00643735081128),
                triggerBin(60.0, 0.282378580452, 0.00754207107977, 0.00754207107977),
                triggerBin(70.0, 0.35076548966, 0.00861133596919, 0.00861133596919),
                triggerBin(80.0, 0.536347290617, 0.00709348032349, 0.00709348032349),
                triggerBin(100.0, 0.750742208493, 0.006816196325, 0.006816196325),
                triggerBin(120.0, 0.899263326814, 0.00522397796154, 0.00522397796154),
                triggerBin(140.0, 0.967288990036, 0.00376169318062, 0.00376169318062),
                triggerBin(160.0, 0.999096760082, 0.000806808606259, 0.000806808606259),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0675889328063, 0.00499092730096),
                triggerBin(20.0, 0.0848057230356, 0.003448383523, 0.003448383523),
                triggerBin(30.0, 0.108984961789, 0.00413540036261, 0.00413540036261),
                triggerBin(40.0, 0.160902811679, 0.00527449198715, 0.00527449198715),
                triggerBin(50.0, 0.221129563505, 0.00656613817287, 0.00656613817287),
                triggerBin(60.0, 0.283306611514, 0.00773478273787, 0.00773478273787),
                triggerBin(70.0, 0.349860777683, 0.0088047646614, 0.0088047646614),
                triggerBin(80.0, 0.537756861492, 0.00723828435456, 0.00723828435456),
                triggerBin(100.0, 0.752038469117, 0.00695087209285, 0.00695087209285),
                triggerBin(120.0, 0.89961735786, 0.00532728735422, 0.00532728735422),
                triggerBin(140.0, 0.967512061395, 0.00384079702681, 0.00384079702681),
                triggerBin(160.0, 0.998972661331, 0.000878675646824, 0.000878675646824),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0675889328063, 0.00499092730096),
                triggerBin(20.0, 0.085690243183, 0.00396066096174, 0.00396066096174),
                triggerBin(30.0, 0.111344188892, 0.00473959826159, 0.00473959826159),
                triggerBin(40.0, 0.163588103551, 0.00600278876322, 0.00600278876322),
                triggerBin(50.0, 0.215828868955, 0.0073897217753, 0.0073897217753),
                triggerBin(60.0, 0.28361545275, 0.00882127258299, 0.00882127258299),
                triggerBin(70.0, 0.344894211893, 0.00997859737558, 0.00997859737558),
                triggerBin(80.0, 0.541027863656, 0.0081556570596, 0.0081556570596),
                triggerBin(100.0, 0.75470971142, 0.00782285878337, 0.00782285878337),
                triggerBin(120.0, 0.898675399807, 0.00607590574946, 0.00607590574946),
                triggerBin(140.0, 0.969442387206, 0.00426318013561, 0.00426318013561),
                triggerBin(160.0, 0.998541913018, 0.00117320513246, 0.00117320513246),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0675889328063, 0.00499092730096),
                triggerBin(20.0, 0.0953237410072, 0.00664058214929, 0.0062636161991),
                triggerBin(30.0, 0.120256283884, 0.00766052437644, 0.00727354000578),
                triggerBin(40.0, 0.170993227991, 0.00941632921258, 0.0090334004341),
                triggerBin(50.0, 0.216934919524, 0.0114544266591, 0.0110457109901),
                triggerBin(60.0, 0.295473251029, 0.0136694535237, 0.0133223729687),
                triggerBin(70.0, 0.355599214145, 0.0156333748225, 0.0153405690432),
                triggerBin(80.0, 0.552447552448, 0.0122599647583, 0.0123225539055),
                triggerBin(100.0, 0.755422587883, 0.011928696635, 0.0123227577593),
                triggerBin(120.0, 0.887568555759, 0.00963630560771, 0.0103783638501),
                triggerBin(140.0, 0.964432284542, 0.0068496508505, 0.00824623627951),
                triggerBin(160.0, 0.995967741935, 0.00260404404935, 0.0052934263943),
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

    # Used input: multicrab_MetLeg2012_130517_110812

    dataParameters = cms.PSet(
        # 2012A
        runs_190456_193621 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(193621),
            luminosity = cms.double(887.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.2, 0.1788854382),
                triggerBin(20.0, 0.166666666667, 0.287350389332, 0.138284918684),
                triggerBin(30.0, 0.0, 0.458641675296, 0.0),
                triggerBin(40.0, 0.0, 0.841344746068, 0.0),
                triggerBin(50.0, 1.0, 0.0, 0.841344746068),
                triggerBin(60.0, 0.0, 1.0, 0.0),
                triggerBin(70.0, 1.0, 0.0, 0.601684479424),
                triggerBin(80.0, 0.0, 1.0, 0.0),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012B
        runs_193833_196531 = cms.PSet(
            firstRun = cms.uint32(193833),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(4440.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0506329113924, 0.0246672076884),
                triggerBin(20.0, 0.0491803278689, 0.0455330494696, 0.0266469956784),
                triggerBin(30.0, 0.0888888888889, 0.064719960598, 0.042052521739),
                triggerBin(40.0, 0.2, 0.157061286074, 0.10675070638),
                triggerBin(50.0, 0.0909090909091, 0.179295209474, 0.0753268806181),
                triggerBin(60.0, 0.285714285714, 0.259937875571, 0.182129028008),
                triggerBin(70.0, 0.0, 0.841344746068, 0.0),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.0, 0.601684479424, 0.0),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012C
        runs_198022_203742 = cms.PSet(
            firstRun = cms.uint32(198022),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(7124.454), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0315789473684, 0.0179419289732),
                triggerBin(20.0, 0.047619047619, 0.0360513607022, 0.0226519839091),
                triggerBin(30.0, 0.0392156862745, 0.0493938932952, 0.0252892452443),
                triggerBin(40.0, 0.0909090909091, 0.0805904491223, 0.049063192669),
                triggerBin(50.0, 0.25, 0.184899566147, 0.132706908337),
                triggerBin(60.0, 0.222222222222, 0.221429368878, 0.14211823823),
                triggerBin(70.0, 0.5, 0.256909620203, 0.256909620203),
                triggerBin(80.0, 0.0, 1.0, 0.0),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 1.0, 0.0, 0.841344746068),
                triggerBin(140.0, 1.0, 0.0, 0.841344746068),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012D
        runs_203777_208686 = cms.PSet(
            firstRun = cms.uint32(203777),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(7318.0), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.03125, 0.0153789216289),
                triggerBin(20.0, 0.0375, 0.03513458966, 0.0203401601691),
                triggerBin(30.0, 0.0350877192982, 0.0444119674392, 0.0226310911763),
                triggerBin(40.0, 0.131578947368, 0.0792158922547, 0.0556305565753),
                triggerBin(50.0, 0.235294117647, 0.147311672312, 0.108959165741),
                triggerBin(60.0, 0.3, 0.20826248199, 0.158328098893),
                triggerBin(70.0, 0.0, 0.36887757085, 0.0),
                triggerBin(80.0, 0.0, 0.458641675296, 0.0),
                triggerBin(100.0, 0.0, 1.0, 0.0),
                triggerBin(120.0, 1.0, 0.0, 0.458641675296),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012AB
        runs_190456_196531 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(196531),
            luminosity = cms.double(5327.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0595238095238, 0.0258154451793),
                triggerBin(20.0, 0.0597014925373, 0.0446914097028, 0.0283545955351),
                triggerBin(30.0, 0.0833333333333, 0.0609994410026, 0.0394538529141),
                triggerBin(40.0, 0.1875, 0.149398565056, 0.100212028831),
                triggerBin(50.0, 0.166666666667, 0.179009937646, 0.106875367754),
                triggerBin(60.0, 0.285714285714, 0.259937875571, 0.182129028008),
                triggerBin(70.0, 0.666666666667, 0.277375360987, 0.414534706285),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.841344746068),
                triggerBin(120.0, 0.333333333333, 0.414534706285, 0.277375360987),
                triggerBin(140.0, 0.0, 1.0, 0.0),
                triggerBin(160.0, 0.0, 1.0, 0.0),
            ),
        ),
        # 2012ABC
        runs_190456_203742 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(203742),
            luminosity = cms.double(12170.501), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0446927374302, 0.0154441319064),
                triggerBin(20.0, 0.0529801324503, 0.0250907982925, 0.018126668258),
                triggerBin(30.0, 0.0606060606061, 0.0344454501331, 0.0237787283297),
                triggerBin(40.0, 0.122448979592, 0.06597268204, 0.0474774607725),
                triggerBin(50.0, 0.208333333333, 0.116379172568, 0.086867737525),
                triggerBin(60.0, 0.25, 0.153966037382, 0.115498745679),
                triggerBin(70.0, 0.555555555556, 0.198267144951, 0.213462824948),
                triggerBin(80.0, 1.0, 0.0, 0.601684479424),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.5, 0.314698893873, 0.314698893873),
                triggerBin(140.0, 1.0, 0.0, 0.841344746068),
                triggerBin(160.0, 1.0, 0.0, 0.601684479424),
            ),
        ),
        # 2012ABCD
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19769.955), # 1/pb
            bins = cms.VPSet(
                triggerBin(0.0, 0.0390879478827, 0.0110609917346),
                triggerBin(20.0, 0.047619047619, 0.0184786643575, 0.0139696084467),
                triggerBin(30.0, 0.0512820512821, 0.0243188284978, 0.0175522352879),
                triggerBin(40.0, 0.126436781609, 0.0462169137562, 0.0363210989057),
                triggerBin(50.0, 0.219512195122, 0.0839616158399, 0.067970007356),
                triggerBin(60.0, 0.269230769231, 0.114603025448, 0.0935066525113),
                triggerBin(70.0, 0.384615384615, 0.176146427336, 0.154567226396),
                triggerBin(80.0, 0.4, 0.303366136254, 0.25334762525),
                triggerBin(100.0, 1.0, 0.0, 0.601684479424),
                triggerBin(120.0, 0.714285714286, 0.182129028008, 0.259937875571),
                triggerBin(140.0, 1.0, 0.0, 0.841344746068),
                triggerBin(160.0, 1.0, 0.0, 0.36887757085),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012A = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0664272890485, 0.00527581727305),
                triggerBin(20.0, 0.0765747952302, 0.00319704787594, 0.00319704787594),
                triggerBin(30.0, 0.109598212162, 0.00404892201197, 0.00404892201197),
                triggerBin(40.0, 0.149694269218, 0.0049115975683, 0.0049115975683),
                triggerBin(50.0, 0.204822008059, 0.00613371909578, 0.00613371909578),
                triggerBin(60.0, 0.279784817509, 0.00739553219786, 0.00739553219786),
                triggerBin(70.0, 0.340926676071, 0.0082832185754, 0.0082832185754),
                triggerBin(80.0, 0.535320080476, 0.00676120386567, 0.00676120386567),
                triggerBin(100.0, 0.752900174749, 0.00650867719214, 0.00650867719214),
                triggerBin(120.0, 0.901589254144, 0.00495313019625, 0.00495313019625),
                triggerBin(140.0, 0.97100995209, 0.00346431775987, 0.00346431775987),
                triggerBin(160.0, 0.99931364464, 0.000677329852762, 0.000677329852762),
            ),
        ),
        Summer12_PU_2012B = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0664272890485, 0.00527581727305),
                triggerBin(20.0, 0.080490886667, 0.00354853173649, 0.00354853173649),
                triggerBin(30.0, 0.111011945974, 0.00443327364473, 0.00443327364473),
                triggerBin(40.0, 0.148056078295, 0.00533264897552, 0.00533264897552),
                triggerBin(50.0, 0.219760533498, 0.00683542056903, 0.00683542056903),
                triggerBin(60.0, 0.28274912142, 0.00796502595868, 0.00796502595868),
                triggerBin(70.0, 0.357534389099, 0.00911775278791, 0.00911775278791),
                triggerBin(80.0, 0.53894244294, 0.00746061180251, 0.00746061180251),
                triggerBin(100.0, 0.748144232857, 0.00731677948289, 0.00731677948289),
                triggerBin(120.0, 0.900380406342, 0.00547324549276, 0.00547324549276),
                triggerBin(140.0, 0.963563871883, 0.00421773161356, 0.00421773161356),
                triggerBin(160.0, 0.998933449536, 0.000939397269751, 0.000939397269751),
            ),
        ),
        Summer12_PU_2012C = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0664272890485, 0.00527581727305),
                triggerBin(20.0, 0.0795565809122, 0.00363655060699, 0.00363655060699),
                triggerBin(30.0, 0.111076003052, 0.00455005372165, 0.00455005372165),
                triggerBin(40.0, 0.150467973425, 0.00549886259846, 0.00549886259846),
                triggerBin(50.0, 0.214501446978, 0.00697631211059, 0.00697631211059),
                triggerBin(60.0, 0.284677142642, 0.00824894411053, 0.00824894411053),
                triggerBin(70.0, 0.353233861277, 0.0093481393338, 0.0093481393338),
                triggerBin(80.0, 0.54050830816, 0.00761601412617, 0.00761601412617),
                triggerBin(100.0, 0.751760079905, 0.00743428160022, 0.00743428160022),
                triggerBin(120.0, 0.900336331751, 0.00560739434878, 0.00560739434878),
                triggerBin(140.0, 0.965502491622, 0.00422571758814, 0.00422571758814),
                triggerBin(160.0, 0.998743730019, 0.00104259357905, 0.00104259357905),
            ),
        ),
        Summer12_PU_2012D = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0664272890485, 0.00527581727305),
                triggerBin(20.0, 0.081759100732, 0.00412839495674, 0.00412839495674),
                triggerBin(30.0, 0.112875483295, 0.00510082016466, 0.00510082016466),
                triggerBin(40.0, 0.153434924269, 0.00616103797536, 0.00616103797536),
                triggerBin(50.0, 0.210804686175, 0.00773888139474, 0.00773888139474),
                triggerBin(60.0, 0.285347885289, 0.00924156280212, 0.00924156280212),
                triggerBin(70.0, 0.348100516732, 0.0104133985004, 0.0104133985004),
                triggerBin(80.0, 0.542017144314, 0.00845049023036, 0.00845049023036),
                triggerBin(100.0, 0.753695815317, 0.00823327578118, 0.00823327578118),
                triggerBin(120.0, 0.89698735262, 0.00637049738713, 0.00637049738713),
                triggerBin(140.0, 0.967707049046, 0.00458394146922, 0.00458394146922),
                triggerBin(160.0, 0.998381501276, 0.0013022482043, 0.0013022482043),
            ),
        ),
        Summer12_PU_2012AB = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0664272890485, 0.00527581727305),
                triggerBin(20.0, 0.0798785519736, 0.00349435807065, 0.00349435807065),
                triggerBin(30.0, 0.110789590373, 0.00437453643904, 0.00437453643904),
                triggerBin(40.0, 0.148314515976, 0.00526898515309, 0.00526898515309),
                triggerBin(50.0, 0.217420338543, 0.00672741077556, 0.00672741077556),
                triggerBin(60.0, 0.282293818623, 0.00787980199535, 0.00787980199535),
                triggerBin(70.0, 0.354922416217, 0.00899026001256, 0.00899026001256),
                triggerBin(80.0, 0.538358900304, 0.00735260411151, 0.00735260411151),
                triggerBin(100.0, 0.748925904776, 0.00718908512911, 0.00718908512911),
                triggerBin(120.0, 0.900573481102, 0.00539280798845, 0.00539280798845),
                triggerBin(140.0, 0.964737554318, 0.00409954423546, 0.00409954423546),
                triggerBin(160.0, 0.998995432833, 0.000897272495918, 0.000897272495918),
            ),
        ),
        Summer12_PU_2012ABC = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0664272890485, 0.00527581727305),
                triggerBin(20.0, 0.0797005479967, 0.00357380620102, 0.00357380620102),
                triggerBin(30.0, 0.110948480274, 0.00447263612833, 0.00447263612833),
                triggerBin(40.0, 0.149510380778, 0.00539729483858, 0.00539729483858),
                triggerBin(50.0, 0.215805958268, 0.00686692302987, 0.00686692302987),
                triggerBin(60.0, 0.283609734762, 0.00808528694138, 0.00808528694138),
                triggerBin(70.0, 0.353987330592, 0.0091903331389, 0.0091903331389),
                triggerBin(80.0, 0.539553467944, 0.00750024142361, 0.00750024142361),
                triggerBin(100.0, 0.750498524496, 0.00732674009315, 0.00732674009315),
                triggerBin(120.0, 0.900442040429, 0.00551276647614, 0.00551276647614),
                triggerBin(140.0, 0.96516098183, 0.00417071172546, 0.00417071172546),
                triggerBin(160.0, 0.998855914107, 0.000978471557764, 0.000978471557764),
            ),
        ),
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0664272890485, 0.00527581727305),
                triggerBin(20.0, 0.081759100732, 0.00412839495674, 0.00412839495674),
                triggerBin(30.0, 0.112875483295, 0.00510082016466, 0.00510082016466),
                triggerBin(40.0, 0.153434924269, 0.00616103797536, 0.00616103797536),
                triggerBin(50.0, 0.210804686175, 0.00773888139474, 0.00773888139474),
                triggerBin(60.0, 0.285347885289, 0.00924156280212, 0.00924156280212),
                triggerBin(70.0, 0.348100516732, 0.0104133985004, 0.0104133985004),
                triggerBin(80.0, 0.542017144314, 0.00845049023036, 0.00845049023036),
                triggerBin(100.0, 0.753695815317, 0.00823327578118, 0.00823327578118),
                triggerBin(120.0, 0.89698735262, 0.00637049738713, 0.00637049738713),
                triggerBin(140.0, 0.967707049046, 0.00458394146922, 0.00458394146922),
                triggerBin(160.0, 0.998381501276, 0.0013022482043, 0.0013022482043),
            ),
        ),
        Summer12_PU_Unweighted = cms.PSet(
            bins = cms.VPSet(
                triggerBin(0.0, 0.0664272890485, 0.00527581727305),
                triggerBin(20.0, 0.0918836140888, 0.00699844650044, 0.00656561181676),
                triggerBin(30.0, 0.123449830891, 0.0083113610363, 0.0078716588633),
                triggerBin(40.0, 0.167611846251, 0.00990606383635, 0.00947325831903),
                triggerBin(50.0, 0.21568627451, 0.0121378765405, 0.0116769263117),
                triggerBin(60.0, 0.295081967213, 0.0144060607732, 0.0140206684983),
                triggerBin(70.0, 0.355841371919, 0.016361264795, 0.0160418879442),
                triggerBin(80.0, 0.552070263488, 0.0127315319161, 0.0127984843127),
                triggerBin(100.0, 0.757249378625, 0.0125307166204, 0.0129710679567),
                triggerBin(120.0, 0.883, 0.0102617913355, 0.0110650154884),
                triggerBin(140.0, 0.962292609351, 0.00739915877272, 0.00893466077509),
                triggerBin(160.0, 0.995594713656, 0.00284490418776, 0.00578061896492),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012A"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)
