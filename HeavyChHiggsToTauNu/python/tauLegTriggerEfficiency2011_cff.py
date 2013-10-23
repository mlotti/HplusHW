# Generated on Tue Oct 23 09:54:59 2012
# by HiggsAnalysis/TriggerEfficiency/test/plotTauEfficiency.py

import FWCore.ParameterSet.Config as cms

_prototype = cms.untracked.PSet(
    data = cms.FileInPath("NOT_YET_SET"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Fall11_PU_2011AB"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)

def getTauLegEfficiency(isolation, againstElectron):
    return _prototype.clone(
        data = "HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2011_%s_%s.json" % (isolation, againstElectron)
    )



## Below are legacy definitions (although the same files are still in use)

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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2011_byMediumCombinedIsolationDeltaBetaCorr_againstElectronMedium.json"),
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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2011_byMediumCombinedIsolationDeltaBetaCorr_againstElectronMVA.json"),
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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2011_byLooseCombinedIsolationDeltaBetaCorr_againstElectronMVA.json"),
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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2011_byLooseCombinedIsolationDeltaBetaCorr_againstElectronMedium.json"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Fall11_PU_2011AB"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)


# Generated on Fri Dec 14 15:09:47 2012
# by HiggsAnalysis/TriggerEfficiency/test/PythonWriter.py

tauLegEfficiency_HIG11019_byTightIsolation_againstElectronMedium = cms.untracked.PSet(
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

    # Offline selection: PFTauPt > 20 && abs(PFTauEta) < 2.1&& 1/PFTauInvPt > 20&& PFTauProng == 1&& againstMuonTight > 0.5&& MuonTauInvMass < 80&& againstElectronMedium > 0.5&& byTightIsolation
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2011_HIG11019_byTightIsolation_againstElectronMedium.json"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Fall11_PU_2011A"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)
