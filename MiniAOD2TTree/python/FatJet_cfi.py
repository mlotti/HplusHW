#================================================================================================
# Import modules
#================================================================================================
import FWCore.ParameterSet.Config as cms

AK8Jets = cms.PSet(
    branchname = cms.untracked.string("AK8Jets"),
    src        = cms.InputTag("updatedPatJetsAK8PFCHS"),
    systVariations = cms.bool(True),

    discriminators = cms.vstring(
        "pfCombinedInclusiveSecondaryVertexV2BJetTags",
        ),
    userFloats = cms.vstring(
        "NjettinessAK8:tau1",
        "NjettinessAK8:tau2",
        "NjettinessAK8:tau3",
        ),
    userInts = cms.vstring(
        ),
    groomedmasses = cms.vstring(
        "ak8PFJetsCHSPrunedMass",
        "ak8PFJetsCHSSoftDropMass",
        ),
    mcjecPath   = cms.untracked.string("../test/jec/Summer16_23Sep2016V4"),
    datajecPath = cms.untracked.string("../test/jec/Summer16_23Sep2016BCDV4"), 
    rho         = cms.InputTag("fixedGridRhoFastjetAll"),
    vertices    = cms.InputTag("offlineSlimmedPrimaryVertices"),

    # PUPPI related variables from MiniAOD
    fillPuppi = cms.bool(False),
    userFloatsPuppi = cms.vstring(
        "ak8PFJetsPuppiValueMap:pt",
        "ak8PFJetsPuppiValueMap:eta",
        "ak8PFJetsPuppiValueMap:phi",
        "ak8PFJetsPuppiValueMap:mass",
        "ak8PFJetsPuppiValueMap:NjettinessAK8PuppiTau1",
        "ak8PFJetsPuppiValueMap:NjettinessAK8PuppiTau2",
        "ak8PFJetsPuppiValueMap:NjettinessAK8PuppiTau3",
        ),
)

FatJets = cms.VPSet()
FatJets.append(AK8Jets)

FatJetsNoSysVariations = cms.VPSet()
for i in range(len(FatJets)):
    pset = FatJets[i].clone()
    pset.systVariations = cms.bool(False)
    FatJetsNoSysVariations.append(pset)
