# Generated on Thu Oct  3 17:39:29 2013
# by HiggsAnalysis/TriggerEfficiency/test/PythonWriter.py

import FWCore.ParameterSet.Config as cms

def triggerBin(pt, efficiency, uncertaintyPlus, uncertaintyMinus):
    return cms.PSet(
        pt = cms.double(pt),
        efficiency = cms.double(efficiency),
        uncertaintyPlus = cms.double(uncertaintyPlus),
        uncertaintyMinus = cms.double(uncertaintyMinus)
    )


tauLegEfficiency_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronMediumMVA3 = cms.untracked.PSet(
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012lowPurity_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronMediumMVA3.json"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

tauLegEfficiency_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronMediumMVA3 = cms.untracked.PSet(
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012lowPurity_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronMediumMVA3.json"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

tauLegEfficiency_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronMediumMVA3 = cms.untracked.PSet(
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012lowPurity_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronMediumMVA3.json"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

tauLegEfficiency_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronMediumMVA3 = cms.untracked.PSet(
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012lowPurity_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronMediumMVA3.json"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

tauLegEfficiency_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronMediumMVA3 = cms.untracked.PSet(
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012lowPurity_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronMediumMVA3.json"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

tauLegEfficiency_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronMediumMVA3 = cms.untracked.PSet(
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012lowPurity_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronMediumMVA3.json"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

tauLegEfficiency_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012lowPurity_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronTightMVA3.json"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

tauLegEfficiency_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012lowPurity_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronTightMVA3.json"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

tauLegEfficiency_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012lowPurity_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronTightMVA3.json"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

tauLegEfficiency_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012lowPurity_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronTightMVA3.json"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

tauLegEfficiency_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012lowPurity_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronTightMVA3.json"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

tauLegEfficiency_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012lowPurity_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronTightMVA3.json"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

tauLegEfficiency_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronVTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012lowPurity_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronVTightMVA3.json"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

tauLegEfficiency_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronVTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012lowPurity_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronVTightMVA3.json"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

tauLegEfficiency_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronVTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012lowPurity_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronVTightMVA3.json"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

tauLegEfficiency_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronVTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012lowPurity_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronVTightMVA3.json"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

tauLegEfficiency_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronVTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012lowPurity_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronVTightMVA3.json"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

tauLegEfficiency_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronVTightMVA3 = cms.untracked.PSet(
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012lowPurity_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronVTightMVA3.json"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

# if __name__ == "__main__":
#     import HiggsAnalysis.HeavyChHiggsToTauNu.HChTools as tools

#     sets = [
#        "byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronMediumMVA3",
#        "byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronMediumMVA3",
#        "byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronMediumMVA3",
#        "byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronMediumMVA3",
#        "byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronMediumMVA3",
#        "byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronMediumMVA3",
#        "byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronTightMVA3",
#        "byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronTightMVA3",
#        "byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronTightMVA3",
#        "byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronTightMVA3",
#        "byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronTightMVA3",
#        "byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronTightMVA3",
#        "byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronVTightMVA3",
#        "byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronVTightMVA3",
#        "byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronVTightMVA3",
#        "byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronVTightMVA3",
#        "byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronVTightMVA3",
#        "byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronVTightMVA3"
#         ]
#     for s in sets:
#         dst = "data/tauLegTriggerEfficiency2012lowPurity_%s.json"%s
#         tools.dumpPSetAsJson(globals()["tauLegEfficiency_"+s], dst)
#         print "Created", dst
