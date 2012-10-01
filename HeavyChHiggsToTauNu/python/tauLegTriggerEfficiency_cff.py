# Generated on Fri Sep 28 14:28:01 2012
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

    # Offline selection: PFTauPt > 20 && abs(PFTauEta) < 2.1&& 1/PFTauInvPt > 20&& PFTauProng == 1&& againstElectronMedium > 0.5 && againstMuonTight > 0.5&& byMediumCombinedIsolationDeltaBetaCorr > 0.5&& MuonTauInvMass < 80

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
		triggerBin(80.0, 1.0, 0.36887757085), # manually added
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
        Fall11= cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0237136465324, 0.00367391569281),
                triggerBin(30.0, 0.210781932977, 0.00937398019393),
                triggerBin(40.0, 0.65418227216, 0.017618864849),
                triggerBin(50.0, 0.864864864865, 0.034181229703),
                triggerBin(60.0, 0.967213114754, 0.0416131309118),
                triggerBin(80.0, 1.0, 0.0923494906334),
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

    # Offline selection: PFTauPt > 20 && abs(PFTauEta) < 2.1&& 1/PFTauInvPt > 20&& PFTauProng == 1&& againstElectronMVA > 0.5 && againstMuonTight > 0.5&& byMediumCombinedIsolationDeltaBetaCorr > 0.5&& MuonTauInvMass < 80    

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
		triggerBin(80.0, 1.0, 0.36887757085), # manually added
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
        Fall11= cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0241397021058, 0.00400224440462),
                triggerBin(30.0, 0.211014176663, 0.00996053457927),
                triggerBin(40.0, 0.660056657224, 0.0187585885406),
                triggerBin(50.0, 0.918699186992, 0.0326665715574),
                triggerBin(60.0, 1.0, 0.0384134220123),
                triggerBin(80.0, 1.0, 0.142229304965),
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

    # Offline selection: PFTauPt > 20 && abs(PFTauEta) < 2.1&& 1/PFTauInvPt > 20&& PFTauProng == 1&& againstElectronMVA > 0.5 && againstMuonTight > 0.5&& byLooseCombinedIsolationDeltaBetaCorr > 0.5&& MuonTauInvMass < 80     

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
		triggerBin(80.0, 1.0, 0.36887757085), # manually added
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
        Fall11= cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0241397021058, 0.00400224440462),
                triggerBin(30.0, 0.211014176663, 0.00996053457927),
                triggerBin(40.0, 0.660056657224, 0.0187585885406),
                triggerBin(50.0, 0.918699186992, 0.0326665715574),
                triggerBin(60.0, 1.0, 0.0384134220123),
                triggerBin(80.0, 1.0, 0.142229304965),
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

    # Offline selection: PFTauPt > 20 && abs(PFTauEta) < 2.1&& 1/PFTauInvPt > 20&& PFTauProng == 1&& againstElectronMedium > 0.5 && againstMuonTight > 0.5&& byLooseCombinedIsolationDeltaBetaCorr > 0.5&& MuonTauInvMass < 80  

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
		triggerBin(80.0, 1.0, 0.36887757085), # manually added
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
        Fall11= cms.PSet(
            bins = cms.VPSet(
                triggerBin(20.0, 0.0237136465324, 0.00367391569281),
                triggerBin(30.0, 0.210781932977, 0.00937398019393),
                triggerBin(40.0, 0.65418227216, 0.017618864849),
                triggerBin(50.0, 0.864864864865, 0.034181229703),
                triggerBin(60.0, 0.967213114754, 0.0416131309118),
                triggerBin(80.0, 1.0, 0.0923494906334),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Fall11"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)
