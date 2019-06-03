import FWCore.ParameterSet.Config as cms

skim = cms.EDFilter("JetTriggersSkim",
    Verbose        = cms.bool(False),
                    TriggerResults = cms.InputTag("TriggerResults::HLT"),
                    HLTPaths       = cms.vstring("HLT_IsoMu24_v", 
        
                                                 ),
                    # Vertex
    VertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices"),
    # Jets (https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetID#Recommendations_for_13_TeV_data)
    JetCollection  = cms.InputTag("slimmedJets"),
    JetUserFloats  = cms.vstring(
	"pileupJetId:fullDiscriminant", #currently disabled
    ),
    JetEtCut       = cms.double(20.0),
    JetEtaCut      = cms.double(2.4),
    NJets          = cms.int32(0),
    # Electrons (https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2)
    ElectronCollection    = cms.InputTag("slimmedElectrons"),
    ElectronID            = cms.string("cutBasedElectronID-Spring15-25ns-V1-standalone-veto"), #8X: "cutBasedElectronID-Summer16-80X-V1-veto"
    ElectronRhoSource     = cms.InputTag("fixedGridRhoFastjetCentralCalo"), #7X: "fixedGridRhoFastjetAll" (for PU mitigation in isolation)
    ElectronRelIsoEA      = cms.double(0.15), #Loose iso synced with H+->tau+ nu
    ElectronPtCut         = cms.double(15.0),
    ElectronEtaCut        = cms.double(2.5),
    ElectronNCut          = cms.int32(0),
    # Muons (https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2)
    MuonCollection    = cms.InputTag("slimmedMuons"),
    MuonID            = cms.string("Loose"),
    MuonRelIso04      = cms.double(0.15), #Loose iso synced with H+->tau+ nu
    MuonPtCut         = cms.double(26.0),
    MuonEtaCut        = cms.double(2.5),
    MuonNCut          = cms.int32(1),
   )
