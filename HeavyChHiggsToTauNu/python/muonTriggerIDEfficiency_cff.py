import FWCore.ParameterSet.Config as cms

# Efficiencies for muon pT > 41, by Sami 20121003-160154
efficiency_pt41 = cms.untracked.PSet(
    dataParameters = cms.PSet(
        # PSet names are only documentary
        Run2011A_Mu20 = cms.PSet(
            firstRun = cms.uint32(160431),
            lastRun = cms.uint32(163261),
            luminosity = cms.double(46.969999999999999),
            efficiency = cms.double(0.882968),
            uncertainty = cms.double(0.003007)
        ),
        Run2011A_Mu24 = cms.PSet(
            firstRun = cms.uint32(163270),
            lastRun = cms.uint32(163869),
            luminosity = cms.double(168.66399999999999),
            efficiency = cms.double(0.891375),
            uncertainty = cms.double(0.001517)
        ),
        Run2011A_Mu30 = cms.PSet(
            firstRun = cms.uint32(165088),
            lastRun = cms.uint32(166150),
            luminosity = cms.double(238.51400000000001),
            efficiency = cms.double(0.904915),
            uncertainty = cms.double(0.000522)
        ),
        Run2011A_Mu40 = cms.PSet(
            firstRun = cms.uint32(166161),
            lastRun = cms.uint32(173198),
            luminosity = cms.double(1590.5),
            efficiency = cms.double(0.877395),
            uncertainty = cms.double(0.000522)
        ),
        Run2011A_Mu40_eta2p1 = cms.PSet(
            firstRun = cms.uint32(173236),
            lastRun = cms.uint32(177452),
            luminosity = cms.double(264.44299999999998),
            efficiency = cms.double(0.867646),
            uncertainty = cms.double(0.001347)
        ),
        Run2011B_Mu40_eta2p1 = cms.PSet(
            firstRun = cms.uint32(177453),
            lastRun = cms.uint32(180371),
            luminosity = cms.double(2740.0),
            efficiency = cms.double(0.957712),
            uncertainty = cms.double(0.000252)
        ),
    ),
    mcParameters = cms.PSet(
        Fall11_2012AB = cms.PSet(
            efficiency = cms.double(0.888241),
            uncertainty = cms.double(0.000187),
        ),
    ),
    dataSelect = cms.vstring(
        "Run2011A_Mu20",
        "Run2011A_Mu24",
        "Run2011A_Mu30",
        "Run2011A_Mu40",
        "Run2011A_Mu40_eta2p1",
        "Run2011B_Mu40_eta2p1",
    ),
    mcSelect = cms.string("Fall11_2012AB"),
    mode = cms.untracked.string("disabled"), # # efficiency, disabled
    type = cms.untracked.string("constant"),
    muonSrc = cms.InputTag("NOT_SET"),
)

efficiency = efficiency_pt41
