#================================================================================================
# Import modules
#================================================================================================
import FWCore.ParameterSet.Config as cms

AK8Jets = cms.PSet(
    branchname = cms.untracked.string("AK8Jets"),
    src        = cms.InputTag("selectedPatJetsAK8PFCHS"),  # OLD: selectedPatJetsAK8PFCHS"
    systVariations = cms.bool(False),

    discriminators = cms.vstring(
        "pfCombinedInclusiveSecondaryVertexV2BJetTags",
        "pfCombinedSecondaryVertexV2BJetTags",
        "pfCombinedMVAV2BJetTags",
        "pfCombinedCvsLJetTags",
        "pfCombinedCvsBJetTags"
        ),
    userFloats = cms.vstring(
        "NjettinessAK8CHS:tau1",
        "NjettinessAK8CHS:tau2",
        "NjettinessAK8CHS:tau3",
        "NjettinessAK8CHS:tau4",
        ),

    userInts = cms.vstring(
        ),
    checkSubjets = cms.bool(True),
    )
   

# AK8 - SoftDrop Subjets
#AK8JetsSoftDrop = cms.PSet(
#    branchname = cms.untracked.string("AK8JetsSoftDrop"),
#    src        = cms.InputTag("packedPatJetsAK8PFCHSSoftDrop"),
#    systVariations = cms.bool(False),
#    discriminators = cms.vstring(
#        "pfCombinedInclusiveSecondaryVertexV2BJetTags",
#        ),
#    userFloats = cms.vstring(
#        ),
#    userInts = cms.vstring(
#        ),
#    checkSubjets = cms.bool(True),
#    ),


FatJets = cms.VPSet()
FatJets.append(AK8Jets)

FatJetsNoSysVariations = cms.VPSet()
for i in range(len(FatJets)):
    pset = FatJets[i].clone()
    pset.systVariations = cms.bool(False)
    FatJetsNoSysVariations.append(pset)
