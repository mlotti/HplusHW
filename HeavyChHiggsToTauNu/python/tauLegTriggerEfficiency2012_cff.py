# Generated on Thu Oct  3 15:36:17 2013
# by HiggsAnalysis/TriggerEfficiency/test/PythonWriter.py

import FWCore.ParameterSet.Config as cms
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTools as HChTools

eraRunMap = {
    "Run2012A": ["runs_190456_193621"],
    "Run2012B": ["runs_193834_196531"],
#    "Run2012C": ["runs_198022_202585"], # FIXME: temporary fix
    "Run2012C": ["runs_198022_203742"],
    "Run2012D": ["runs_202807_208686"],
    "Run2012AB": ["runs_190456_196531"],
    "Run2012ABC": ["runs_190456_202585"],
    "Run2012ABCD": ["runs_190456_208686"],
}

def setEfficiency(pset, isolation, againstMuon, againstElectron):
    pset.data = HChTools.getEfficiencyJsonFullPath("tau trigger scale factors", "tauLegTriggerEfficiency2012", "%s_%s_%s" % (isolation, againstMuon, againstElectron))

def getRunsForEra(era):
    try:
        return eraRunMap[era]
    except KeyError:
        raise Exception("Unsupported value of era parameter, has value '%s', allowed values are %s" % (era, ", ".join(["'%s'"%e for e in eraRunMap.iterkeys()])))

## Below are legacy definitions (although the same files are still in use)

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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1&& sqrt(2*(sqrt(MuonPt*TMath::Cos(MuonPhi)*MuonPt*TMath::Cos(MuonPhi)+MuonPt*TMath::Sin(MuonPhi)*MuonPt*TMath::Sin(MuonPhi)+MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta))))*sqrt(PFTauPt*TMath::Cos(PFTauPhi)*PFTauPt*TMath::Cos(PFTauPhi)+PFTauPt*TMath::Sin(PFTauPhi)*PFTauPt*TMath::Sin(PFTauPhi)+PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))-MuonPt*TMath::Cos(MuonPhi)*PFTauPt*TMath::Cos(PFTauPhi)-MuonPt*TMath::Sin(MuonPhi)*PFTauPt*TMath::Sin(PFTauPhi)-MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))) < 80&& sqrt( 2 * MuonPt * PFMET_ET * (1-cos(MuonPhi-PFMET_phi)) ) < 40

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronMediumMVA3.json"),
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1&& sqrt(2*(sqrt(MuonPt*TMath::Cos(MuonPhi)*MuonPt*TMath::Cos(MuonPhi)+MuonPt*TMath::Sin(MuonPhi)*MuonPt*TMath::Sin(MuonPhi)+MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta))))*sqrt(PFTauPt*TMath::Cos(PFTauPhi)*PFTauPt*TMath::Cos(PFTauPhi)+PFTauPt*TMath::Sin(PFTauPhi)*PFTauPt*TMath::Sin(PFTauPhi)+PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))-MuonPt*TMath::Cos(MuonPhi)*PFTauPt*TMath::Cos(PFTauPhi)-MuonPt*TMath::Sin(MuonPhi)*PFTauPt*TMath::Sin(PFTauPhi)-MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))) < 80&& sqrt( 2 * MuonPt * PFMET_ET * (1-cos(MuonPhi-PFMET_phi)) ) < 40

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronMediumMVA3.json"),
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1&& sqrt(2*(sqrt(MuonPt*TMath::Cos(MuonPhi)*MuonPt*TMath::Cos(MuonPhi)+MuonPt*TMath::Sin(MuonPhi)*MuonPt*TMath::Sin(MuonPhi)+MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta))))*sqrt(PFTauPt*TMath::Cos(PFTauPhi)*PFTauPt*TMath::Cos(PFTauPhi)+PFTauPt*TMath::Sin(PFTauPhi)*PFTauPt*TMath::Sin(PFTauPhi)+PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))-MuonPt*TMath::Cos(MuonPhi)*PFTauPt*TMath::Cos(PFTauPhi)-MuonPt*TMath::Sin(MuonPhi)*PFTauPt*TMath::Sin(PFTauPhi)-MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))) < 80&& sqrt( 2 * MuonPt * PFMET_ET * (1-cos(MuonPhi-PFMET_phi)) ) < 40

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronMediumMVA3.json"),
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1&& sqrt(2*(sqrt(MuonPt*TMath::Cos(MuonPhi)*MuonPt*TMath::Cos(MuonPhi)+MuonPt*TMath::Sin(MuonPhi)*MuonPt*TMath::Sin(MuonPhi)+MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta))))*sqrt(PFTauPt*TMath::Cos(PFTauPhi)*PFTauPt*TMath::Cos(PFTauPhi)+PFTauPt*TMath::Sin(PFTauPhi)*PFTauPt*TMath::Sin(PFTauPhi)+PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))-MuonPt*TMath::Cos(MuonPhi)*PFTauPt*TMath::Cos(PFTauPhi)-MuonPt*TMath::Sin(MuonPhi)*PFTauPt*TMath::Sin(PFTauPhi)-MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))) < 80&& sqrt( 2 * MuonPt * PFMET_ET * (1-cos(MuonPhi-PFMET_phi)) ) < 40

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronMediumMVA3.json"),
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1&& sqrt(2*(sqrt(MuonPt*TMath::Cos(MuonPhi)*MuonPt*TMath::Cos(MuonPhi)+MuonPt*TMath::Sin(MuonPhi)*MuonPt*TMath::Sin(MuonPhi)+MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta))))*sqrt(PFTauPt*TMath::Cos(PFTauPhi)*PFTauPt*TMath::Cos(PFTauPhi)+PFTauPt*TMath::Sin(PFTauPhi)*PFTauPt*TMath::Sin(PFTauPhi)+PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))-MuonPt*TMath::Cos(MuonPhi)*PFTauPt*TMath::Cos(PFTauPhi)-MuonPt*TMath::Sin(MuonPhi)*PFTauPt*TMath::Sin(PFTauPhi)-MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))) < 80&& sqrt( 2 * MuonPt * PFMET_ET * (1-cos(MuonPhi-PFMET_phi)) ) < 40

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronMediumMVA3.json"),
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronMediumMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1&& sqrt(2*(sqrt(MuonPt*TMath::Cos(MuonPhi)*MuonPt*TMath::Cos(MuonPhi)+MuonPt*TMath::Sin(MuonPhi)*MuonPt*TMath::Sin(MuonPhi)+MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta))))*sqrt(PFTauPt*TMath::Cos(PFTauPhi)*PFTauPt*TMath::Cos(PFTauPhi)+PFTauPt*TMath::Sin(PFTauPhi)*PFTauPt*TMath::Sin(PFTauPhi)+PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))-MuonPt*TMath::Cos(MuonPhi)*PFTauPt*TMath::Cos(PFTauPhi)-MuonPt*TMath::Sin(MuonPhi)*PFTauPt*TMath::Sin(PFTauPhi)-MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))) < 80&& sqrt( 2 * MuonPt * PFMET_ET * (1-cos(MuonPhi-PFMET_phi)) ) < 40

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronMediumMVA3.json"),
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1&& sqrt(2*(sqrt(MuonPt*TMath::Cos(MuonPhi)*MuonPt*TMath::Cos(MuonPhi)+MuonPt*TMath::Sin(MuonPhi)*MuonPt*TMath::Sin(MuonPhi)+MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta))))*sqrt(PFTauPt*TMath::Cos(PFTauPhi)*PFTauPt*TMath::Cos(PFTauPhi)+PFTauPt*TMath::Sin(PFTauPhi)*PFTauPt*TMath::Sin(PFTauPhi)+PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))-MuonPt*TMath::Cos(MuonPhi)*PFTauPt*TMath::Cos(PFTauPhi)-MuonPt*TMath::Sin(MuonPhi)*PFTauPt*TMath::Sin(PFTauPhi)-MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))) < 80&& sqrt( 2 * MuonPt * PFMET_ET * (1-cos(MuonPhi-PFMET_phi)) ) < 40

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronTightMVA3.json"),
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1&& sqrt(2*(sqrt(MuonPt*TMath::Cos(MuonPhi)*MuonPt*TMath::Cos(MuonPhi)+MuonPt*TMath::Sin(MuonPhi)*MuonPt*TMath::Sin(MuonPhi)+MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta))))*sqrt(PFTauPt*TMath::Cos(PFTauPhi)*PFTauPt*TMath::Cos(PFTauPhi)+PFTauPt*TMath::Sin(PFTauPhi)*PFTauPt*TMath::Sin(PFTauPhi)+PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))-MuonPt*TMath::Cos(MuonPhi)*PFTauPt*TMath::Cos(PFTauPhi)-MuonPt*TMath::Sin(MuonPhi)*PFTauPt*TMath::Sin(PFTauPhi)-MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))) < 80&& sqrt( 2 * MuonPt * PFMET_ET * (1-cos(MuonPhi-PFMET_phi)) ) < 40

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronTightMVA3.json"),
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1&& sqrt(2*(sqrt(MuonPt*TMath::Cos(MuonPhi)*MuonPt*TMath::Cos(MuonPhi)+MuonPt*TMath::Sin(MuonPhi)*MuonPt*TMath::Sin(MuonPhi)+MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta))))*sqrt(PFTauPt*TMath::Cos(PFTauPhi)*PFTauPt*TMath::Cos(PFTauPhi)+PFTauPt*TMath::Sin(PFTauPhi)*PFTauPt*TMath::Sin(PFTauPhi)+PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))-MuonPt*TMath::Cos(MuonPhi)*PFTauPt*TMath::Cos(PFTauPhi)-MuonPt*TMath::Sin(MuonPhi)*PFTauPt*TMath::Sin(PFTauPhi)-MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))) < 80&& sqrt( 2 * MuonPt * PFMET_ET * (1-cos(MuonPhi-PFMET_phi)) ) < 40

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronTightMVA3.json"),
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1&& sqrt(2*(sqrt(MuonPt*TMath::Cos(MuonPhi)*MuonPt*TMath::Cos(MuonPhi)+MuonPt*TMath::Sin(MuonPhi)*MuonPt*TMath::Sin(MuonPhi)+MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta))))*sqrt(PFTauPt*TMath::Cos(PFTauPhi)*PFTauPt*TMath::Cos(PFTauPhi)+PFTauPt*TMath::Sin(PFTauPhi)*PFTauPt*TMath::Sin(PFTauPhi)+PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))-MuonPt*TMath::Cos(MuonPhi)*PFTauPt*TMath::Cos(PFTauPhi)-MuonPt*TMath::Sin(MuonPhi)*PFTauPt*TMath::Sin(PFTauPhi)-MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))) < 80&& sqrt( 2 * MuonPt * PFMET_ET * (1-cos(MuonPhi-PFMET_phi)) ) < 40

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronTightMVA3.json"),
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1&& sqrt(2*(sqrt(MuonPt*TMath::Cos(MuonPhi)*MuonPt*TMath::Cos(MuonPhi)+MuonPt*TMath::Sin(MuonPhi)*MuonPt*TMath::Sin(MuonPhi)+MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta))))*sqrt(PFTauPt*TMath::Cos(PFTauPhi)*PFTauPt*TMath::Cos(PFTauPhi)+PFTauPt*TMath::Sin(PFTauPhi)*PFTauPt*TMath::Sin(PFTauPhi)+PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))-MuonPt*TMath::Cos(MuonPhi)*PFTauPt*TMath::Cos(PFTauPhi)-MuonPt*TMath::Sin(MuonPhi)*PFTauPt*TMath::Sin(PFTauPhi)-MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))) < 80&& sqrt( 2 * MuonPt * PFMET_ET * (1-cos(MuonPhi-PFMET_phi)) ) < 40

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronTightMVA3.json"),
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1&& sqrt(2*(sqrt(MuonPt*TMath::Cos(MuonPhi)*MuonPt*TMath::Cos(MuonPhi)+MuonPt*TMath::Sin(MuonPhi)*MuonPt*TMath::Sin(MuonPhi)+MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta))))*sqrt(PFTauPt*TMath::Cos(PFTauPhi)*PFTauPt*TMath::Cos(PFTauPhi)+PFTauPt*TMath::Sin(PFTauPhi)*PFTauPt*TMath::Sin(PFTauPhi)+PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))-MuonPt*TMath::Cos(MuonPhi)*PFTauPt*TMath::Cos(PFTauPhi)-MuonPt*TMath::Sin(MuonPhi)*PFTauPt*TMath::Sin(PFTauPhi)-MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))) < 80&& sqrt( 2 * MuonPt * PFMET_ET * (1-cos(MuonPhi-PFMET_phi)) ) < 40

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronTightMVA3.json"),
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1&& sqrt(2*(sqrt(MuonPt*TMath::Cos(MuonPhi)*MuonPt*TMath::Cos(MuonPhi)+MuonPt*TMath::Sin(MuonPhi)*MuonPt*TMath::Sin(MuonPhi)+MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta))))*sqrt(PFTauPt*TMath::Cos(PFTauPhi)*PFTauPt*TMath::Cos(PFTauPhi)+PFTauPt*TMath::Sin(PFTauPhi)*PFTauPt*TMath::Sin(PFTauPhi)+PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))-MuonPt*TMath::Cos(MuonPhi)*PFTauPt*TMath::Cos(PFTauPhi)-MuonPt*TMath::Sin(MuonPhi)*PFTauPt*TMath::Sin(PFTauPhi)-MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))) < 80&& sqrt( 2 * MuonPt * PFMET_ET * (1-cos(MuonPhi-PFMET_phi)) ) < 40

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronVTightMVA3.json"),
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1&& sqrt(2*(sqrt(MuonPt*TMath::Cos(MuonPhi)*MuonPt*TMath::Cos(MuonPhi)+MuonPt*TMath::Sin(MuonPhi)*MuonPt*TMath::Sin(MuonPhi)+MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta))))*sqrt(PFTauPt*TMath::Cos(PFTauPhi)*PFTauPt*TMath::Cos(PFTauPhi)+PFTauPt*TMath::Sin(PFTauPhi)*PFTauPt*TMath::Sin(PFTauPhi)+PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))-MuonPt*TMath::Cos(MuonPhi)*PFTauPt*TMath::Cos(PFTauPhi)-MuonPt*TMath::Sin(MuonPhi)*PFTauPt*TMath::Sin(PFTauPhi)-MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))) < 80&& sqrt( 2 * MuonPt * PFMET_ET * (1-cos(MuonPhi-PFMET_phi)) ) < 40

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronVTightMVA3.json"),
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonMedium2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1&& sqrt(2*(sqrt(MuonPt*TMath::Cos(MuonPhi)*MuonPt*TMath::Cos(MuonPhi)+MuonPt*TMath::Sin(MuonPhi)*MuonPt*TMath::Sin(MuonPhi)+MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta))))*sqrt(PFTauPt*TMath::Cos(PFTauPhi)*PFTauPt*TMath::Cos(PFTauPhi)+PFTauPt*TMath::Sin(PFTauPhi)*PFTauPt*TMath::Sin(PFTauPhi)+PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))-MuonPt*TMath::Cos(MuonPhi)*PFTauPt*TMath::Cos(PFTauPhi)-MuonPt*TMath::Sin(MuonPhi)*PFTauPt*TMath::Sin(PFTauPhi)-MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))) < 80&& sqrt( 2 * MuonPt * PFMET_ET * (1-cos(MuonPhi-PFMET_phi)) ) < 40

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronVTightMVA3.json"),
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byLooseCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1&& sqrt(2*(sqrt(MuonPt*TMath::Cos(MuonPhi)*MuonPt*TMath::Cos(MuonPhi)+MuonPt*TMath::Sin(MuonPhi)*MuonPt*TMath::Sin(MuonPhi)+MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta))))*sqrt(PFTauPt*TMath::Cos(PFTauPhi)*PFTauPt*TMath::Cos(PFTauPhi)+PFTauPt*TMath::Sin(PFTauPhi)*PFTauPt*TMath::Sin(PFTauPhi)+PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))-MuonPt*TMath::Cos(MuonPhi)*PFTauPt*TMath::Cos(PFTauPhi)-MuonPt*TMath::Sin(MuonPhi)*PFTauPt*TMath::Sin(PFTauPhi)-MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))) < 80&& sqrt( 2 * MuonPt * PFMET_ET * (1-cos(MuonPhi-PFMET_phi)) ) < 40

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronVTightMVA3.json"),
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1&& sqrt(2*(sqrt(MuonPt*TMath::Cos(MuonPhi)*MuonPt*TMath::Cos(MuonPhi)+MuonPt*TMath::Sin(MuonPhi)*MuonPt*TMath::Sin(MuonPhi)+MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta))))*sqrt(PFTauPt*TMath::Cos(PFTauPhi)*PFTauPt*TMath::Cos(PFTauPhi)+PFTauPt*TMath::Sin(PFTauPhi)*PFTauPt*TMath::Sin(PFTauPhi)+PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))-MuonPt*TMath::Cos(MuonPhi)*PFTauPt*TMath::Cos(PFTauPhi)-MuonPt*TMath::Sin(MuonPhi)*PFTauPt*TMath::Sin(PFTauPhi)-MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))) < 80&& sqrt( 2 * MuonPt * PFMET_ET * (1-cos(MuonPhi-PFMET_phi)) ) < 40

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronVTightMVA3.json"),
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

    # Offline selection: Sum$(PFTauPt > 20 && abs(PFTauEta) < 2.1&& PFTauLeadChargedHadrCandPt > 20&& PFTauProng == 1&& PFTau_againstElectronVTightMVA3 > 0.5&& PFTau_againstMuonTight2 > 0.5&& PFTau_byTightCombinedIsolationDeltaBetaCorr3Hits > 0.5) == 1 && Sum$(MuonPt > 15&& MuonIsGlobalMuon) == 1&& sqrt(2*(sqrt(MuonPt*TMath::Cos(MuonPhi)*MuonPt*TMath::Cos(MuonPhi)+MuonPt*TMath::Sin(MuonPhi)*MuonPt*TMath::Sin(MuonPhi)+MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta))))*sqrt(PFTauPt*TMath::Cos(PFTauPhi)*PFTauPt*TMath::Cos(PFTauPhi)+PFTauPt*TMath::Sin(PFTauPhi)*PFTauPt*TMath::Sin(PFTauPhi)+PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))-MuonPt*TMath::Cos(MuonPhi)*PFTauPt*TMath::Cos(PFTauPhi)-MuonPt*TMath::Sin(MuonPhi)*PFTauPt*TMath::Sin(PFTauPhi)-MuonPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-MuonEta)))*PFTauPt/TMath::Tan(2.0*TMath::ATan(TMath::Exp(-PFTauEta))))) < 80&& sqrt( 2 * MuonPt * PFMET_ET * (1-cos(MuonPhi-PFMET_phi)) ) < 40

    # Used input: multicrab_TauLeg2012_130603_104257
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/tauLegTriggerEfficiency2012_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronVTightMVA3.json"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)
