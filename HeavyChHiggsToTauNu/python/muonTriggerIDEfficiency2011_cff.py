import FWCore.ParameterSet.Config as cms

# Efficiencies for muon pT > 41, by Sami 20121003-160154
efficiency_pt41 = cms.untracked.PSet(
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/muonTriggerIDEfficiency2011_pt41.json"),
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
efficiency_ID_pickle = cms.untracked.PSet(
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/muonIDEfficiency2011_reference.json"),
    dataSelect = cms.vstring(
        "Run2011A",
        "Run2011B",
    ),
    mcSelect = cms.string("Run2011A"),
    mode = cms.untracked.string("disabled"),
    type = cms.untracked.string("binned"),
    muonSrc = cms.InputTag("NOT_SET"),
)

# calculate Run2011AB as lumi weighted average
# if True:
#     lumiA = efficiency_ID_pickle.dataParameters.Run2011A.luminosity.value()
#     lumiB = efficiency_ID_pickle.dataParameters.Run2011B.luminosity.value()
#     lumiAB = lumiA+lumiB
#     bins = []
#     for binA, binB in zip(efficiency_ID_pickle.mcParameters.Run2011A.bins, efficiency_ID_pickle.mcParameters.Run2011B.bins):
#         bins.append(cms.PSet(
#                 triggerBin(binA.eta.value(),
#                            (binA.efficiency.value()*lumiA + binB.efficiency.value()*lumiB)/lumiAB,
#                            # assume stat uncertainties fully correlated in MC samples
#                            (binA.uncertainty.value()*lumiA + binB.uncertainty.value()*lumiB)/lumiAB
#                            )))
#     efficiency_ID_pickle.mcParameters.Run2011AB = cms.PSet(bins = cms.VPSet(bins))
#     efficiency_ID_pickle.mcSelect = "Run2011AB"


## Reference trigger efficiencyes for HLT_Mu40
# From https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonHLT#Reference_Efficiencies_for_2011
# Run ranges from https://indico.cern.ch/getFile.py/access?contribId=1&resId=0&materialId=slides&confId=156713
efficiency_trigger_reference = cms.untracked.PSet(
    data = cms.FileInPath("HiggsAnalysis/HeavyChHiggsToTauNu/data/muonTriggerEfficiency2011_reference.json"),
    dataSelect = cms.vstring(
        "lumi1e33",
        "lumi2e33",
        "lumi3e33lowPU",
        "lumi3e33highPU",
        "lumi5e33",
    ),
    mcSelect = cms.string("Fall11"),
    mode = cms.untracked.string("disabled"),
    type = cms.untracked.string("binned"),
    muonSrc = cms.InputTag("NOT_SET"),
)

# Add dummy eta bins in order to avoid exception for ntuples
# def addEtaDummyBins(pset):
#     for ps in [pset.dataParameters, pset.mcParameters]:
#         for name in ps.parameterNames_():
#             bins = getattr(ps, name).bins
#             bins.insert(0, triggerBin(-5.0, 1, 0))
#             bins.append(triggerBin(2.4, 1, 0))
# addEtaDummyBins(efficiency_ID_pickle)
# addEtaDummyBins(efficiency_trigger_reference)

#efficiency = efficiency_pt41
efficiency = efficiency_ID_pickle

efficiency_ID = efficiency_ID_pickle

efficiency_trigger = efficiency_trigger_reference

# if __name__ == "__main__":
#    import HiggsAnalysis.HeavyChHiggsToTauNu.HChTools as tools
#    tools.dumpPSetAsJson(efficiency_pt41)
#    tools.dumpPSetAsJson(efficiency_ID_pickle)
#    tools.dumpPSetAsJson(efficiency_trigger_reference)
