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
        src = cms.InputTag("selectedPatJetsAK4PFCHSNew"),#updatedPatJetsUpdatedJEC"),
#        src = cms.InputTag("selectedPatJetsForMetT1T2SmearCorr"),
#        src = cms.InputTag("cleanedPatJets"),
#        src = cms.InputTag("patJetsReapplyJEC"),
	systVariations = cms.bool(True),
        srcJESup   = cms.InputTag("shiftedPatJetEnUp"),
	srcJESdown = cms.InputTag("shiftedPatJetEnDown"),
        srcJERup   = cms.InputTag("shiftedPatSmearedJetResUp"),
        srcJERdown = cms.InputTag("shiftedPatSmearedJetResDown"),
#        jecPayload = JECpayloadAK4PFchs.payload,

        discriminators = cms.vstring( #https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation80X
            "pfCombinedInclusiveSecondaryVertexV2BJetTags",
            "pfCombinedMVAV2BJetTags", 
            "pfCombinedCvsLJetTags", 
            "pfCombinedCvsBJetTags"
        ),
        userFloats = cms.vstring(
#            "pileupJetId:fullDiscriminant",
            "QGTaggerAK4PFCHSNew:qgLikelihood",
            "QGTaggerAK4PFCHSNew:ptD",
            "QGTaggerAK4PFCHSNew:axis2",
        ),       
        userInts = cms.vstring(
            "QGTaggerAK4PFCHSNew:mult",
        ),
    ),
#    cms.PSet(
#        branchname = cms.untracked.string("JetsPuppi"),
##        src = cms.InputTag("patJetsReapplyJECPuppi"), # made from ak4PFJets
#        src        = cms.InputTag("updatedPatJetsUpdatedJECPuppi"),
#        srcJESup   = cms.InputTag("shiftedPatJetEnUp"),
#        srcJESdown = cms.InputTag("shiftedPatJetEnDown"),
#        srcJERup   = cms.InputTag("shiftedPatJetResUp"),
#        srcJERdown = cms.InputTag("shiftedPatJetResDown"),
##        jecPayload = JECpayloadAK4PFPuppi.payload,
#        discriminators = cms.vstring(
#            "pfCombinedInclusiveSecondaryVertexV2BJetTags",
#            "pfCombinedMVAV2BJetTags", 
#            "pfCombinedCvsLJetTags", 
#            "pfCombinedCvsBJetTags"
#         ),
#        userFloats = cms.vstring(
##           "pileupJetId:fullDiscriminant"
#        ),
#    )
)


JetsNoSysVariations = cms.VPSet()
for i in range(len(Jets)):
    pset = Jets[i].clone()
    pset.systVariations = cms.bool(False)
    JetsNoSysVariations.append(pset)

