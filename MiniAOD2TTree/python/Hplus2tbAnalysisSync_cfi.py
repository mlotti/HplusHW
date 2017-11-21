import FWCore.ParameterSet.Config as cms

skim = cms.EDFilter("Hplus2tbAnalysisSync",
    Verbose        = cms.bool(False),
    TriggerResults = cms.InputTag("TriggerResults::HLT"),
    HLTPaths       = cms.vstring(
        #"HLT_PFHT450_SixJet40_BTagCSV_p056_v",
    ),
    # Vertex
    VertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices"),
    
    # Jets (https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetID#Recommendations_for_13_TeV_data)
    JetCollection  = cms.InputTag("slimmedJets"),
    JetUserFloats  = cms.vstring(
	"pileupJetId:fullDiscriminant", #currently disabled
    ),
    JetEtCut       = cms.double(40.0),
    JetEtaCut      = cms.double(2.4),
    NJets          = cms.int32(0),

    # AK8 Jets
    #AK8JetCollection = cms.InputTag("slimmedJetsAK4"),
    #AK8JetUserFloats = cms.vstring(
    #    
    #    ),
    #AK8JetEtCut      = cms.double(100),
    #AK8JetEtaCut     = cms.double(2.4),
    
    PackedCandidatesCollection = cms.InputTag("packedPFCandidates"),

    # Taus
    TauCollection  = cms.InputTag("slimmedTaus"),
    TauDiscriminators = cms.vstring(
        "decayModeFinding",
        "byVLooseIsolationMVArun2v1DBoldDMwLT",
    ),
    TauPtCut       = cms.double(20),
    TauEtaCut      = cms.double(2.3),
    TauNCut        = cms.int32(0),

    # Electrons (https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2)
    ElectronCollection    = cms.InputTag("slimmedElectrons"),
    ElectronID            = cms.string("cutBasedElectronID-Spring15-25ns-V1-standalone-veto"),
    ElectronMVA           = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values"),
    ElectronRhoSource     = cms.InputTag("fixedGridRhoFastjetAll"),
    ElectronMiniRelIsoEA  = cms.double(0.40),
    ElectronRelIsoEA      = cms.double(0.15),
    ElectronPtCut         = cms.double(10.0),                                               
    ElectronEtaCut        = cms.double(2.1),
    ElectronNCut          = cms.int32(0),

    # Muons (https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2)
    MuonCollection    = cms.InputTag("slimmedMuons"),
    MuonID            = cms.string("Loose"),
    MuonMiniRelIsoEA  = cms.double(0.40),

    MuonRelIso04      = cms.double(0.15),
    MuonPtCut         = cms.double(10.0),
    MuonEtaCut        = cms.double(2.4),
    MuonNCut          = cms.int32(0),
   )
