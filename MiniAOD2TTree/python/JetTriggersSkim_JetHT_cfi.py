import FWCore.ParameterSet.Config as cms

skim = cms.EDFilter("Hplus2tbAnalysisSkim",
    Verbose        = cms.bool(False),
    TriggerResults = cms.InputTag("TriggerResults::HLT"),
    HLTPaths       = cms.vstring(
        "HLT_PFHT300_v",
        "HLT_PFHT350_v",
        "HLT_PFHT400_v",                                     
        "HLT_PFHT475_v",
        "HLT_PFHT400_SixJet30",
        "HLT_PFHT450_SixJet40",
        "HLT_PFHT400_SixJet30_DoubleBTagCSV_p056",
        "HLT_PFHT450_SixJet40_BTagCSV_p056",
    ),
    # Jets (https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetID#Recommendations_for_13_TeV_data)
    JetCollection  = cms.InputTag("slimmedJets"),
    JetUserFloats  = cms.vstring(
	"pileupJetId:fullDiscriminant", #currently disabled
    ),
    JetEtCut       = cms.double(20.0),
    JetEtaCut      = cms.double(2.4),
    NJets          = cms.int32(0),
                    
    # PF Candidates
    PackedCandidatesCollection = cms.InputTag("packedPFCandidates"),

    # Vertex
    VertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices"),

    # Electrons (https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2)
    ElectronCollection   = cms.InputTag("slimmedElectrons"),
    ElectronID           = cms.string("cutBasedElectronID-Spring15-25ns-V1-standalone-veto"),
    ElectronMVA          = cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values"),
    ElectronRhoSource    = cms.InputTag("fixedGridRhoFastjetCentralNeutral"),
    ElectronMiniRelIsoEA = cms.double(1.0), # MIT cut is at 0.40. Allow wiggle room
    ElectronPtCut        = cms.double(10.0),
    ElectronEtaCut       = cms.double(2.1),
    ElectronNCut         = cms.int32(0),

    # Muons (https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2)
    MuonCollection   = cms.InputTag("slimmedMuons"),
    MuonID           = cms.string("Loose"),
    MuonMiniRelIsoEA = cms.double(1.0), # MIT cut is at 0.40. Allow wiggle room
    MuonPtCut        = cms.double(10.0),
    MuonEtaCut       = cms.double(2.4),
    MuonNCut         = cms.int32(0),
    
    # Taus
    TauCollection     = cms.InputTag("slimmedTaus"),
    TauDiscriminators = cms.vstring(
        "decayModeFinding",
        "byVLooseIsolationMVArun2v1DBoldDMwLT",
        ),
    TauPtCut  = cms.double(20),
    TauEtaCut = cms.double(2.3),
    TauNCut   = cms.int32(999),

)
