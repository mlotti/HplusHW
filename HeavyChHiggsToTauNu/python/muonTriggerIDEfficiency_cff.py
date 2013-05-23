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

def triggerBin(eta, eff, unc):
    return cms.PSet(
        eta = cms.double(eta),
        efficiency = cms.double(eff),
        uncertainty = cms.double(unc),
    )

# Taken from https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffs
# file MuonEfficiencies2011_44X.pkl
efficiency_pickle = cms.untracked.PSet(
    dataParameters = cms.PSet(
        Run2011A = cms.PSet(
            firstRun = cms.uint32(160431),
            lastRun = cms.uint32(173692),
            luminosity = cms.double(2311.2),
            bins = cms.VPSet(
                 triggerBin(-2.4, 0.911081, 0.001876),
                 triggerBin(-2.1, 0.942857, 0.000967),
                 triggerBin(-1.6, 0.966133, 0.000844),
                 triggerBin(-1.2, 0.939815, 0.001071),
                 triggerBin(-0.9, 0.963884, 0.000857),
                 triggerBin(-0.6, 0.978927, 0.000714),
                 triggerBin(-0.3, 0.873086, 0.002150),
                 triggerBin(-0.2, 0.966454, 0.000693),
                 triggerBin(0.2, 0.864344, 0.002202),
                 triggerBin(0.3, 0.977701, 0.000718),
                 triggerBin(0.6, 0.961561, 0.000869),
                 triggerBin(0.9, 0.933412, 0.001093),
                 triggerBin(1.2, 0.961414, 0.000864),
                 triggerBin(1.6, 0.949883, 0.000908),
                 triggerBin(2.1, 0.916387, 0.001793),
            ),
        ),
        Run2011B = cms.PSet(
            firstRun = cms.uint32(175832),
            lastRun = cms.uint32(180252),
            luminosity = cms.double(2739.0),
            bins = cms.VPSet(
                 triggerBin(-2.4, 0.891508, 0.002352),
                 triggerBin(-2.1, 0.898175, 0.001315),
                 triggerBin(-1.6, 0.925534, 0.001254),
                 triggerBin(-1.2, 0.923540, 0.001312),
                 triggerBin(-0.9, 0.962596, 0.001009),
                 triggerBin(-0.6, 0.978776, 0.000850),
                 triggerBin(-0.3, 0.870056, 0.002384),
                 triggerBin(-0.2, 0.964021, 0.000816),
                 triggerBin(0.2, 0.860059, 0.002428),
                 triggerBin(0.3, 0.977243, 0.000861),
                 triggerBin(0.6, 0.957809, 0.001034),
                 triggerBin(0.9, 0.915410, 0.001353),
                 triggerBin(1.2, 0.925162, 0.001233),
                 triggerBin(1.6, 0.909677, 0.001256),
                 triggerBin(2.1, 0.892636, 0.002269),
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Run2011A = cms.PSet(
            bins = cms.VPSet(
                 triggerBin(-2.4, 0.920800, 0.001413),
                 triggerBin(-2.1, 0.955867, 0.000685),
                 triggerBin(-1.6, 0.976668, 0.000522),
                 triggerBin(-1.2, 0.949758, 0.000805),
                 triggerBin(-0.9, 0.966280, 0.000645),
                 triggerBin(-0.6, 0.979079, 0.000499),
                 triggerBin(-0.3, 0.891634, 0.001789),
                 triggerBin(-0.2, 0.969849, 0.000502),
                 triggerBin(0.2, 0.874329, 0.001809),
                 triggerBin(0.3, 0.976563, 0.000522),
                 triggerBin(0.6, 0.963404, 0.000672),
                 triggerBin(0.9, 0.932337, 0.000931),
                 triggerBin(1.2, 0.963423, 0.000652),
                 triggerBin(1.6, 0.947235, 0.000754),
                 triggerBin(2.1, 0.914812, 0.001440),
            ),
        ),
        Run2011B = cms.PSet(
            bins = cms.VPSet(
                 triggerBin(-2.4, 0.921415, 0.001498),
                 triggerBin(-2.1, 0.954864, 0.000724),
                 triggerBin(-1.6, 0.975155, 0.000564),
                 triggerBin(-1.2, 0.949792, 0.000836),
                 triggerBin(-0.9, 0.965575, 0.000672),
                 triggerBin(-0.6, 0.979110, 0.000518),
                 triggerBin(-0.3, 0.889509, 0.001832),
                 triggerBin(-0.2, 0.968433, 0.000530),
                 triggerBin(0.2, 0.873001, 0.002011),
                 triggerBin(0.3, 0.976034, 0.000555),
                 triggerBin(0.6, 0.963312, 0.000684),
                 triggerBin(0.9, 0.928834, 0.000984),
                 triggerBin(1.2, 0.961309, 0.000696),
                 triggerBin(1.6, 0.947041, 0.000778),
                 triggerBin(2.1, 0.915914, 0.001520),
            ),
        ),
    ),
    dataSelect = cms.vstring(
        "Run2011A",
        "Run2011B",
    ),
    mcSelect = cms.string("Run2011A"),
    mode = cms.untracked.string("disabled"),
    type = cms.untracked.string("binned"),
    muonSrc = cms.InputTag("NOT_SET"),
)

#efficiency = efficiency_pt41
efficiency = efficiency_pickle
