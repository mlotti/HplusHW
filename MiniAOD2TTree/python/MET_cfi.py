import FWCore.ParameterSet.Config as cms

METs = cms.VPSet(
    cms.PSet(
        branchname = cms.untracked.string("MET_Type1"),
        src = cms.InputTag("slimmedMETs")
    ),
#    cms.PSet(
#        branchname = cms.untracked.string("MET_Type1_NoHF"),
#        src = cms.InputTag("slimmedMETsNoHF")
#    ),
#    cms.PSet(
#        branchname = cms.untracked.string("MET_Puppi"),
#        src = cms.InputTag("slimmedMETsPuppi")
#    ),
    cms.PSet(
        branchname = cms.untracked.string("MET_Type1_UnclusteredEnDown"),
        src = cms.InputTag("patPFMetT1UnclusteredEnDown")
    ),
    cms.PSet(
        branchname = cms.untracked.string("MET_Type1_UnclusteredEnUp"),
        src = cms.InputTag("patPFMetT1UnclusteredEnUp")
    ),
    cms.PSet(
        branchname = cms.untracked.string("MET_Type1_JetEnDown"),
        src = cms.InputTag("patPFMetT1JetEnDown")
    ),
    cms.PSet(
        branchname = cms.untracked.string("MET_Type1_JetEnUp"),        
        src = cms.InputTag("patPFMetT1JetEnUp")        
    ),
    cms.PSet(
        branchname = cms.untracked.string("MET_Type1_JetResDown"),        
        src = cms.InputTag("patPFMetT1JetResDown")        
    ),
    cms.PSet(
        branchname = cms.untracked.string("MET_Type1_JetResUp"),  
        src = cms.InputTag("patPFMetT1JetResUp")  
    ),
    cms.PSet(
        branchname = cms.untracked.string("MET_Type1_TauEnDown"),        
        src = cms.InputTag("patPFMetT1TauEnDown")        
    ),
    cms.PSet(
        branchname = cms.untracked.string("MET_Type1_TauEnUp"),  
        src = cms.InputTag("patPFMetT1TauEnUp")  
    ),
)

METsNoSysVariations = cms.VPSet()
METsNoSysVariations.append(METs[0])

