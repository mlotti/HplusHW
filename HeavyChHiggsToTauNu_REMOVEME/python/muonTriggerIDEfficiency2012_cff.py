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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/muonIDEfficiency2012_pickle.json"),
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
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/muonTriggerEfficiency2012_pickle.json"),
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
