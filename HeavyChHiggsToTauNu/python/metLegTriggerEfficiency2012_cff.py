# Generated on Tue Feb 19 17:16:50 2013
# by HiggsAnalysis/TriggerEfficiency/test/PythonWriter.py

import FWCore.ParameterSet.Config as cms

def triggerBin(pt, efficiency, uncertainty):
    return cms.PSet(
        pt = cms.double(pt),
        efficiency = cms.double(efficiency),
        uncertainty = cms.double(uncertainty)
    )


metLegEfficiency = cms.untracked.PSet(
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

    # Offline selection: (Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1) >= 1&&Sum$(PFJetPt > 0) >= 3+Sum$(PFTauPt > 41 && abs(PFTauEta) < 2.1 && PFTauJetMinDR < 0.5))&& PFTau_againstElectronMVA > 0.5 && PFTau_againstMuonTight > 0.5&& PFTau_decayModeFinding > 0.5&& PFTau_byMediumCombinedIsolationDeltaBetaCorr > 0.5&& hPlusGlobalElectronVetoFilter > 0.5 && hPlusGlobalMuonVetoFilter > 0.5

    dataParameters = cms.PSet(
        # Dummy
        runs_190456_208686 = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19296), # 1/pb
            bins = cms.VPSet(
                triggerBin(5.0, 0.00553111250786, 0.000831537337386),
                triggerBin(20.0, 0.0071012381646, 0.00113306352584),
                triggerBin(30.0, 0.00959097320169, 0.00163693152987),
                triggerBin(40.0, 0.0209371884347, 0.00319667874872),
                triggerBin(50.0, 0.0302013422819, 0.00572380925614),
                triggerBin(60.0, 0.0631868131868, 0.0127523150049),
                triggerBin(70.0, 0.124087591241, 0.0281665874611),
                triggerBin(80.0, 0.166666666667, 0.0421974736285),
                triggerBin(100.0, 0.458333333333, 0.101707073027),
                triggerBin(120.0, 0.75, 0.153093108924),
                triggerBin(140.0, 1.0, 0.0),
                triggerBin(160.0, 1.0, 0.0),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Summer12_PU_2012ABCD = cms.PSet(
            bins = cms.VPSet(
                triggerBin(5.0, 0.0202739477504, 0.000949154453197),
                triggerBin(20.0, 0.0294101948225, 0.00123435467047),
                triggerBin(30.0, 0.0442361650051, 0.00158870646195),
                triggerBin(40.0, 0.0647734048897, 0.00212493310619),
                triggerBin(50.0, 0.0943869866452, 0.00292967551687),
                triggerBin(60.0, 0.128743315508, 0.00387243919559),
                triggerBin(70.0, 0.202918454936, 0.00526943662375),
                triggerBin(80.0, 0.335732647815, 0.0053540009426),
                triggerBin(100.0, 0.586761328043, 0.00711555535377),
                triggerBin(120.0, 0.793666340189, 0.00731190471658),
                triggerBin(140.0, 0.911261027504, 0.00647795219876),
                triggerBin(160.0, 0.96925566343, 0.00491012446689),
            ),
        ),
    ),
    dataSelect = cms.vstring(),
    mcSelect = cms.string("Summer12_PU_2012ABCD"),
    mode = cms.untracked.string("disabled") # dataEfficiency, scaleFactor, disabled
)
