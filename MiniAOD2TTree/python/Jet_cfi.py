import FWCore.ParameterSet.Config as cms

Jets = cms.VPSet(
    cms.PSet(
        branchname = cms.untracked.string("Jets"),
        src = cms.InputTag("slimmedJets"), # made from ak4PFJetsCHS
        discriminators = cms.vstring(
            "pfJetBProbabilityBJetTags",
            "pfJetProbabilityBJetTags",
            #"trackCountingHighPurBJetTags",
            #"trackCountingHighEffBJetTags",
            #"simpleSecondaryVertexHighEffBJetTags",
            #"simpleSecondaryVertexHighPurBJetTags",
            "pfCombinedSecondaryVertexBJetTags",
            "pfCombinedInclusiveSecondaryVertexBJetTags",
            #"combinedInclusiveSecondaryVertexV2BJetTags", # for 72x
            "pfCombinedInclusiveSecondaryVertexV2BJetTags", # for 74x
            "pfCombinedMVABJetTag",
        ),
        userFloats = cms.vstring(
           "pileupJetId:fullDiscriminant"
        ),
    )
)
