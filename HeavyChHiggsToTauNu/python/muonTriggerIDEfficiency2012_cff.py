import FWCore.ParameterSet.Config as cms

def triggerBin(eta, eff, unc):
    return cms.PSet(
        eta = cms.double(eta),
        efficiency = cms.double(eff),
        uncertainty = cms.double(unc),
    )

# Taken from https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffs
# file MuonEfficiencies_Run2012ReReco_53X.pkl
efficiency_ID_pickle = cms.untracked.PSet(
    dataParameters = cms.PSet(
        Run2012ABCD = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19749.225000),
            bins = cms.VPSet(
                 triggerBin(-3.0, 0.0, 0.0), # dummy
                 triggerBin(-2.4, 0.932968, 0.000588),
                 triggerBin(-2.1, 0.923644, 0.000357),
                 triggerBin(-1.6, 0.969156, 0.000291),
                 triggerBin(-1.2, 0.960308, 0.000318),
                 triggerBin(-0.9, 0.963095, 0.000288),
                 triggerBin(-0.6, 0.976934, 0.000253),
                 triggerBin(-0.3, 0.878590, 0.000694),
                 triggerBin(-0.2, 0.962047, 0.000249),
                 triggerBin(0.2, 0.868187, 0.000712),
                 triggerBin(0.3, 0.975727, 0.000254),
                 triggerBin(0.6, 0.961412, 0.000290),
                 triggerBin(0.9, 0.957564, 0.000324),
                 triggerBin(1.2, 0.960502, 0.000305),
                 triggerBin(1.6, 0.944208, 0.000320),
                 triggerBin(2.1, 0.943711, 0.000563),
                 triggerBin(2.4, 0.0, 0.0), # dummy
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Run2012ABCD = cms.PSet(
            bins = cms.VPSet(
                 triggerBin(-3.0, 1.0, 0.0), # dummy
                 triggerBin(-2.4, 0.942784, 0.000548),
                 triggerBin(-2.1, 0.933558, 0.000384),
                 triggerBin(-1.6, 0.971095, 0.000280),
                 triggerBin(-1.2, 0.967008, 0.000319),
                 triggerBin(-0.9, 0.968150, 0.000298),
                 triggerBin(-0.6, 0.981670, 0.000229),
                 triggerBin(-0.3, 0.892512, 0.000860),
                 triggerBin(-0.2, 0.969659, 0.000246),
                 triggerBin(0.2, 0.882265, 0.000893),
                 triggerBin(0.3, 0.980292, 0.000236),
                 triggerBin(0.6, 0.967934, 0.000299),
                 triggerBin(0.9, 0.964380, 0.000331),
                 triggerBin(1.2, 0.960570, 0.000321),
                 triggerBin(1.6, 0.946971, 0.000348),
                 triggerBin(2.1, 0.942928, 0.000550),
                 triggerBin(2.4, 1.0, 0.0), # dummy
            ),
        ),
    ),
    dataSelect = cms.vstring(
        "Run2012ABCD",
    ),
    mcSelect = cms.string("Run2012ABCD"),
    mode = cms.untracked.string("disabled"),
    type = cms.untracked.string("binned"),
    muonSrc = cms.InputTag("NOT_SET"),
)

# Taken from https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffs
# file SingleMuonTriggerEfficiencies_eta2p1_Run2012ABCD_v5trees.pkl
efficiency_trigger_pickle = cms.untracked.PSet(
    dataParameters = cms.PSet(
        Run2012ABCD = cms.PSet(
            firstRun = cms.uint32(190456),
            lastRun = cms.uint32(208686),
            luminosity = cms.double(19749.225000),
            bins = cms.VPSet(
                 triggerBin(-3.0, 0.0, 0.0), # dummy
                 triggerBin(-2.1, 0.797967, 0.000941),
                 triggerBin(-1.6, 0.846791, 0.000755),
                 triggerBin(-1.2, 0.848933, 0.000793),
                 triggerBin(-0.9, 0.942568, 0.000487),
                 triggerBin(-0.6, 0.960470, 0.000394),
                 triggerBin(-0.3, 0.888114, 0.001131),
                 triggerBin(-0.2, 0.957171, 0.000355),
                 triggerBin(0.2, 0.908570, 0.001045),
                 triggerBin(0.3, 0.958715, 0.000394),
                 triggerBin(0.6, 0.944297, 0.000484),
                 triggerBin(0.9, 0.845280, 0.000796),
                 triggerBin(1.2, 0.818594, 0.000814),
                 triggerBin(1.6, 0.853188, 0.000816),
                 triggerBin(2.1, 0.0, 0.0), # dummy
            ),
        ),
    ),
    mcParameters = cms.PSet(
        Run2012ABCD = cms.PSet(
            bins = cms.VPSet(
                 triggerBin(-3.0, 1.0, 0.0), # dummy
                 triggerBin(-2.1, 0.802335, 0.001338),
                 triggerBin(-1.6, 0.856032, 0.001069),
                 triggerBin(-1.2, 0.881732, 0.001037),
                 triggerBin(-0.9, 0.959692, 0.000623),
                 triggerBin(-0.6, 0.971532, 0.000488),
                 triggerBin(-0.3, 0.936382, 0.001320),
                 triggerBin(-0.2, 0.969508, 0.000441),
                 triggerBin(0.2, 0.941777, 0.001258),
                 triggerBin(0.3, 0.973530, 0.000492),
                 triggerBin(0.6, 0.959105, 0.000616),
                 triggerBin(0.9, 0.879057, 0.001055),
                 triggerBin(1.2, 0.846500, 0.001106),
                 triggerBin(1.6, 0.840889, 0.001210),
                 triggerBin(2.1, 1.0, 0.0), # dummy
            ),
        ),
    ),
    dataSelect = cms.vstring(
        "Run2012ABCD",
    ),
    mcSelect = cms.string("Run2012ABCD"),
    mode = cms.untracked.string("disabled"),
    type = cms.untracked.string("binned"),
    muonSrc = cms.InputTag("NOT_SET"),
)


efficiency_ID = efficiency_ID_pickle
efficiency_trigger = efficiency_trigger_pickle
