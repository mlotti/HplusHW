import FWCore.ParameterSet.Config as cms

# Workaround: use PSets because this module is loaded
#JECpayloadAK4PFchs = cms.PSet(
#    payload = cms.string("AK4PFchs")
#)
#JECpayloadAK4PFPuppi = cms.PSet(
#    payload = cms.string("AK4PFPuppi")
#)

Jets = cms.VPSet(
    cms.PSet(
        branchname = cms.untracked.string("Jets"),
#        src = cms.InputTag("patJetsReapplyJECAK4CHS"), # made from ak4PFJetsCHS
#        src = cms.InputTag("updatedPatJetsUpdatedJEC"),
        src = cms.InputTag("cleanedPatJets"),
        srcJESup   = cms.InputTag("shiftedPatJetEnUp"),
	srcJESdown = cms.InputTag("shiftedPatJetEnDown"),
        srcJERup   = cms.InputTag("shiftedPatJetResUp"),
        srcJERdown = cms.InputTag("shiftedPatJetResDown"),
#        jecPayload = JECpayloadAK4PFchs.payload,

        discriminators = cms.vstring(
            "pfJetBProbabilityBJetTags",
            "pfJetProbabilityBJetTags",
            #"pfCombinedSecondaryVertexBJetTags",
            #"pfCombinedInclusiveSecondaryVertexBJetTags",
            #"combinedInclusiveSecondaryVertexV2BJetTags", # for 72x
            "pfCombinedInclusiveSecondaryVertexV2BJetTags", # for 74x
            "pfCombinedMVABJetTag",
        ),
        userFloats = cms.vstring(
#           "pileupJetId:fullDiscriminant"
        ),
    ),
#    cms.PSet(
#        branchname = cms.untracked.string("JetsPuppi"),
##        src = cms.InputTag("patJetsReapplyJECPuppi"), # made from ak4PFJets
#        src = cms.InputTag("updatedPatJetsUpdatedJECPuppi"),
#        srcJES = cms.InputTag("shiftedPatJetEnDown"),   
#        srcJER = cms.InputTag("shiftedPatJetResDown"),
##        jecPayload = JECpayloadAK4PFPuppi.payload,
#        discriminators = cms.vstring(
#            "pfJetBProbabilityBJetTags",
#            "pfJetProbabilityBJetTags",
#            #"pfCombinedSecondaryVertexBJetTags",
#            #"pfCombinedInclusiveSecondaryVertexBJetTags",
#            #"combinedInclusiveSecondaryVertexV2BJetTags", # for 72x
#            "pfCombinedInclusiveSecondaryVertexV2BJetTags", # for 74x
#            "pfCombinedMVABJetTag", # Does not work
#        ),
#        userFloats = cms.vstring(
##           "pileupJetId:fullDiscriminant"
#        ),
#    )
)
