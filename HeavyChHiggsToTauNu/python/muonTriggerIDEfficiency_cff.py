import FWCore.ParameterSet.Config as cms

# Efficiencies for muon pT > 41, by Sami 20121003-160154
efficiency_pt41 = cms.untracked.PSet(
    dataParameters = cms.PSet(
        # PSet names are only documentary
        Run2011A_Mu20 = cms.PSet(
            firstRun = cms.uint32(160431),
            lastRun = cms.uint32(163261),
            efficiency = cms.double(0.882968),
            uncertainty = cms.double(0.003007)
        ),
        Run2011A_Mu24 = cms.PSet(
            firstRun = cms.uint32(163270),
            lastRun = cms.uint32(163869),
            efficiency = cms.double(0.891375),
            uncertainty = cms.double(0.001517)
        ),
        Run2011A_Mu30 = cms.PSet(
            firstRun = cms.uint32(165088),
            lastRun = cms.uint32(166150),
            efficiency = cms.double(0.904915),
            uncertainty = cms.double(0.000522)
        ),
        Run2011A_Mu40 = cms.PSet(
            firstRun = cms.uint32(166161),
            lastRun = cms.uint32(173198),
            efficiency = cms.double(0.877395),
            uncertainty = cms.double(0.000522)
        ),
        Run2011A_Mu40_eta2p1 = cms.PSet(
            firstRun = cms.uint32(173693),
            lastRun = cms.uint32(177452),
            efficiency = cms.double(0.867646),
            uncertainty = cms.double(0.001347)
        ),
        Run2011B_Mu40_eta2p1 = cms.PSet(
            firstRun = cms.uint32(177453),
            lastRun = cms.uint32(180371),
            efficiency = cms.double(0.957712),
            uncertainty = cms.double(0.000252)
        ),
    ),
    mcParameters = cms.PSet(
        efficiency = cms.double(0.888241),
        uncertainty = cms.double(0.000187),
    ),
    mode = cms.string("disabled") # # efficiency, disabled
)

efficiency = efficiency_pt41
