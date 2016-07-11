# Generated on Mon Oct  7 16:18:42 2013
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
    pset.data = HChTools.getEfficiencyJsonFullPath("met trigger scale factors", "metLegTriggerEfficiency2012", "%s_%s_%s" % (isolation, againstMuon, againstElectron))

def getRunsForEra(era):
    try:
        return eraRunMap[era]
    except KeyError:
        raise Exception("Unsupported value of era parameter, has value '%s', allowed values are %s" % (era, ", ".join(["'%s'"%e for e in eraRunMap.iterkeys()])))

## Below are legacy definitions (although the same files are still in use)

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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/metLegTriggerEfficiency2012_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronMediumMVA3.json"),
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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/metLegTriggerEfficiency2012_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronMediumMVA3.json"),
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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/metLegTriggerEfficiency2012_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronMediumMVA3.json"),
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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/metLegTriggerEfficiency2012_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronMediumMVA3.json"),
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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/metLegTriggerEfficiency2012_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronMediumMVA3.json"),
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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/metLegTriggerEfficiency2012_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronMediumMVA3.json"),
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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/metLegTriggerEfficiency2012_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronTightMVA3.json"),
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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/metLegTriggerEfficiency2012_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronTightMVA3.json"),
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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/metLegTriggerEfficiency2012_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronTightMVA3.json"),
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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/metLegTriggerEfficiency2012_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronTightMVA3.json"),
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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/metLegTriggerEfficiency2012_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronTightMVA3.json"),
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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/metLegTriggerEfficiency2012_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronTightMVA3.json"),
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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/metLegTriggerEfficiency2012_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronVTightMVA3.json"),
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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/metLegTriggerEfficiency2012_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronVTightMVA3.json"),
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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/metLegTriggerEfficiency2012_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonMedium2_againstElectronVTightMVA3.json"),
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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/metLegTriggerEfficiency2012_byLooseCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronVTightMVA3.json"),
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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/metLegTriggerEfficiency2012_byMediumCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronVTightMVA3.json"),
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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/metLegTriggerEfficiency2012_byTightCombinedIsolationDeltaBetaCorr3Hits_againstMuonTight2_againstElectronVTightMVA3.json"),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012A"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)
