import FWCore.ParameterSet.Config as cms
import HiggsAnalysis.MiniAOD2TTree.tools.git as git #HiggsAnalysis.HeavyChHiggsToTauNu.tools.git as git

process = cms.Process("TTreeDump")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#        'file:miniAOD-prod_PAT_TT_RECO_721_11112014.root'
#	'file:miniAOD-prod_PAT_TT_RECO_740p1_02122014.root'
#	'file:miniAOD-prod_PAT_Hp200_RECO_740p1_09122014.root'
#	'file:miniAOD-prod_PAT_SingleMu_Run2012D_v1_RECO.root'
	'file:PYTHIA6_Tauola_TTbar_H160_taunu_13TeV_cff_py_GEN.root'
    )
)

process.dump = cms.EDFilter('MiniAOD2TTreeFilter',
    OutputFileName = cms.string("miniaod2tree.root"),
    CodeVersion = cms.string(git.getCommitId()),
    EventInfo = cms.PSet(
	PileupSummaryInfoSrc = cms.InputTag("addPileupInfo"),
#	LHESrc = cms.InputTag(""),
	OfflinePrimaryVertexSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
    ),
    Trigger = cms.PSet(
	TriggerResults = cms.InputTag("TriggerResults::HLT"),
	TriggerBits = cms.vstring(
	    "HLT_LooseIsoPFTau50_Trk30_eta2p1_MET120_v1",
#	    "HLT_IsoMu24_IterTrk02_v1"
        ),
	L1Extra = cms.InputTag("l1extraParticles::MET"),
	filter = cms.untracked.bool(False)
    ),
    Taus = cms.VPSet(
        cms.PSet(
            branchname = cms.untracked.string("Taus"),
            src = cms.InputTag("slimmedTaus"),
            discriminators = cms.vstring(
		"againstElectronMedium",
		"againstMuonTight3",
		"decayModeFinding",
		"byLooseCombinedIsolationDeltaBetaCorr3Hits"
	    ),
            filter = cms.untracked.bool(False)
        )
    ),
    Electrons = cms.VPSet(
        cms.PSet(
            branchname = cms.untracked.string("Electrons"),
            src = cms.InputTag("slimmedElectrons"),
            discriminators = cms.vstring()
        )
    ),
    Muons = cms.VPSet(   
        cms.PSet(
            branchname = cms.untracked.string("Muons"),   
            src = cms.InputTag("slimmedMuons"),    
            discriminators = cms.vstring() 
        )   
    ),
    Jets = cms.VPSet(      
        cms.PSet(
            branchname = cms.untracked.string("Jets"),       
            src = cms.InputTag("slimmedJets"),      
            discriminators = cms.vstring(
		"trackCountingHighPurBJetTags",
		"trackCountingHighEffBJetTags"
            )
        )
    ),
    METs = cms.VPSet(
        cms.PSet(
            branchname = cms.untracked.string("MET_Type1"),
            src = cms.InputTag("slimmedMETs")
        ),
        cms.PSet(
            branchname = cms.untracked.string("CaloMET"),
            src = cms.InputTag("patMETCalo")
        )
    )
)

# module execution
process.runEDFilter = cms.Path(process.dump)

