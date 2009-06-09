import FWCore.ParameterSet.Config as cms
import os

def getEnvVar(var, default=None):
    if os.environ.has_key(var):
        return os.environ.get(var)
    else:
        return default

maxEvt = int(getEnvVar("MYMAXEVENTS", -1))
files = getEnvVar("MYINPUTFILES")

summer08 = True

process = cms.Process("test")

#process.Tracer = cms.Service("Tracer")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(maxEvt)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring()
)

if files:
    for file in files.split(" "):
        print "Append file %s to list of input files" % file
        process.source.fileNames.append(file)
else:
#    process.source.fileNames.append("root://madhatter.csc.fi/pnfs/csc.fi/data/cms/Events_matti/muon2tau/TTJets_Fall08_cmssw2117/digi_muon_223/digi_muon_hltskim_402.root")
    process.source.fileNames.append("rfio:/castor/cern.ch/cms/store/relval/CMSSW_2_2_4/RelValTTbar/GEN-SIM-RECO/STARTUP_V8_v1/0000/200EB7E3-90F3-DD11-B1B0-001D09F2432B.root")

#process.load("RecoParticleFlow.Configuration.RecoParticleFlow_cff")
##process.load("RecoBTau.JetTracksAssociator.pfJetTracksAssociator_cfi")
#process.load("RecoTauTag.RecoTau.PFRecoTauTagInfoProducer_cfi")
#process.pfRecoTauTagInfoProducer.ChargedHadrCand_tkminPt = cms.double(0)
#process.pfRecoTauTagInfoProducer.tkminPt = cms.double(0)
#
#process.load("RecoTauTag.RecoTau.PFRecoTauProducer_cfi")
#process.pfRecoTauTagInfoProducer.ChargedHadrCand_tkminPt = cms.double(0)
#process.pfRecoTauTagInfoProducer.tkminPt = cms.double(0)
#process.load("RecoTauTag.RecoTau.PFRecoTauProducer_cfi")
#process.pfRecoTauProducer.ChargedHadrCand_minPt = cms.double(0)
#process.pfRecoTauProducer.NeutrHadrCand_minPt = cms.double(0)
#process.pfRecoTauProducer.GammaCand_minPt = cms.double(0)
#process.pfRecoTauProducer.Track_minPt = cms.double(0)

process.load("RecoTauTag.RecoTau.PFRecoTauDiscriminationByIsolation_cfi")
#process.pftau = cms.Path(
#    process.particleFlowJetCandidates*
#    process.iterativeCone5PFJets*
#    process.pfJetTracksAssociator*
#    process.pfRecoTauTagInfoProducer*
#    process.pfRecoTauProducer
#)

# Message Logger
process.load("FWCore.MessageService.MessageLogger_cfi")
#process.MessageLogger.debugModules = cms.untracked.vstring("*")
#process.MessageLogger.cerr = cms.untracked.PSet(threshold = cms.untracked.string("DEBUG"))


# Magnetic Field
# These are probably the same, but let's be sure
if summer08:
    process.load('Configuration.StandardSequences.MagneticField_38T_cff')
else:
    process.load("Configuration/StandardSequences/MagneticField_cff")

#process.load("RecoJets.JetProducers.iterativeCone5CaloJets_cff")
##process.load("RecoBTau.JetTracksAssociator.jetTracksAssociator_cfi")
#process.load("RecoTauTag.RecoTau.CaloRecoTauTagInfoProducer_cfi")
#process.caloRecoTauTagInfoProducer.tkminPt = 0
#process.load("RecoTauTag.RecoTau.CaloRecoTauProducer_cfi")
#process.caloRecoTauProducer.Track_minPt = 0
#process.load("RecoTauTag.RecoTau.CaloRecoTauDiscriminationByIsolation_cfi")
#process.tau = cms.Path(
#    process.iterativeCone5CaloJets*
#    process.jetTracksAssociator*
#    process.caloRecoTauTagInfoProducer*
#    process.caloRecoTauProducer
#)


# XML ideal geometry description
if summer08:
    process.load('Configuration.StandardSequences.GeometryPilot2_cff')
else:
    process.load("Geometry.CMSCommonData.cmsIdealGeometryXML_cfi")
    
# Calo geometry service model
process.load("Geometry.CaloEventSetup.CaloGeometry_cfi")
# Calo topology service model
process.load("Geometry.CaloEventSetup.CaloTopology_cfi")
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")

#
#    include "JetMETCorrections/MCJet/data/MCJetCorrections152.cff"
#    es_prefer MCJetCorrectorMcone5 = MCJetCorrectionService {}
process.load("JetMETCorrections.Configuration.MCJetCorrectionsSpring07_cff")
#process.load("JetMETCorrections.Configuration.MCJetCorrections152_cff")
#MCJetCorrectorMcone5 = cms.ESSource( "MCJetCorrectionService",
#  appendToDataLabel = cms.string( "" ),
#  tagName = cms.string( "CMSSW_152_midpointCone5" ),
#  label = cms.string( "MCJetCorrectorMcone5" )
#)
#MCJetCorrectorIcone5 = cms.ESSource( "MCJetCorrectionService",
#  appendToDataLabel = cms.string( "" ),
#  tagName = cms.string( "CMSSW_152_iterativeCone5" ),
#  label = cms.string( "MCJetCorrectorIcone5" )
#)

process.load("JetMETCorrections.Type1MET.MetMuonCorrections_cff")
process.load("RecoMET.METProducers.CaloMET_cfi")
process.missingEt = cms.Path(process.metNoHF)

process.load("JetMETCorrections.Type1MET.MetType1Corrections_cff")
process.missingEt_type1i = cms.Path(process.corMetType1Icone5)
#process.missingEt_type1m = cms.Path(process.corMetType1Mcone5)

process.corMetType1Icone5NoHF = cms.EDProducer('Type1MET',
    metType = cms.string("CaloMET"),
    inputUncorMetLabel = cms.string("metNoHF"),
    inputUncorJetsLabel = cms.string("iterativeCone5CaloJets"),
    corrector = cms.string("MCJetCorrectorIcone5"),
    jetPTthreshold = cms.double(20.0),
    jetEMfracLimit = cms.double(0.9)
)
process.missingEt_type1i_nohf = cms.Path(process.corMetType1Icone5NoHF)

#process.corMetType1Mcone5NoHF = cms.EDProducer('Type1MET',
#    metType = cms.string("CaloMET"),
#    inputUncorMetLabel = cms.string("metNoHF"),
#    inputUncorJetsLabel = cms.string("midPointCone5CaloJets"),
#    corrector = cms.string("MCJetCorrectorMcone5"),
#    jetPTthreshold = cms.double(20.0),
#    jetEMfracLimit = cms.double(0.9)
#)
#process.missingEt_type1i_nohf = cms.Path(process.corMetType1Mcone5NoHF)

process.load("JetMETCorrections.Type1MET.MetMuonCorrections_cff")
process.missingEt_muons = cms.Path(process.goodMuonsforMETCorrection*process.corMetGlobalMuons) # 2_2_3
#process.missingEt_muons = cms.Path(process.corMetGlobalMuons) # 2_1_12

process.load("JetMETCorrections.Type1MET.TauMetCorrections_cff")
#process.missingEt_tauMet = cms.Path(process.PFJetsCorrCaloJetsDeltaMet)
process.missingEt_tauMet = cms.Path(process.tauMetCorr)

# track corrected MET
process.load("RecoMET.METProducers.TCMET_cfi")
process.tcMET = cms.Path(process.MetMuonCorrections*process.tcMet)

process.load("RecoTracker.TransientTrackingRecHit.TransientTrackingRecHitBuilderWithoutRefit_cfi")

# iterative tracking
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("Configuration.StandardSequences.FakeConditions_cff")

process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("Configuration.StandardSequences.FakeConditions_cff")
process.load("Configuration.StandardSequences.Simulation_cff")
process.load("Configuration.StandardSequences.MixingNoPileUp_cff")
process.load("Configuration.StandardSequences.VtxSmearedGauss_cff")
process.load("RecoTracker.IterativeTracking.iterativeTk_cff")

process.iterativeTracks = cms.EDProducer('IterativeTrackCollectionProducer')
####process.iterativeTracking = cms.Path(process.iterTracking,process.iterativeTracks)

#process.load("EgammaAnalysis.ElectronIDProducers.cutBasedElectronId_cfi")
#process.load("EgammaAnalysis.ElectronIDProducers.ptdrElectronId_cfi")

process.hPlusAnalysis = cms.EDAnalyzer('OfflineAnalysis',

	HLTSelection = cms.VInputTag(cms.InputTag("HLT1Tau"),cms.InputTag("HLT1MuonIso"),cms.InputTag("HLT1MET"),cms.InputTag("HLT1Tau1MET"),cms.InputTag("HLT1jet"),cms.InputTag("HLT2jet"),cms.InputTag("HLT3jet"),cms.InputTag("HLT4jet")),

        # JetEnergyCorrection = MCJetCorrectorIcone5,MCJetCorrectorMcone5
        # if no corrections, leave {} empty
	JetEnergyCorrection = cms.VInputTag(
		cms.InputTag("MCJetCorrectorIcone5")
#		cms.InputTag("MCJetCorrectorMcone5")
	),

        # b tagging elgorithms
        BTaggingAlgorithms = cms.VInputTag(
                cms.InputTag("trackCountingHighPurBJetTags"),
                cms.InputTag("trackCountingHighEffBJetTags"),
                cms.InputTag("combinedSecondaryVertexBJetTags"),
                cms.InputTag("combinedSecondaryVertexMVABJetTags"),
                cms.InputTag("impactParameterMVABJetTags"),
                cms.InputTag("jetBProbabilityBJetTags"),
                cms.InputTag("jetProbabilityBJetTags"),
                cms.InputTag("simpleSecondaryVertexBJetTags"),
                cms.InputTag("softElectronBJetTags"),
                cms.InputTag("softMuonBJetTags"),
                cms.InputTag("softMuonNoIPBJetTags")
        ),

	METCorrections = cms.VInputTag(
		cms.InputTag("corMetGlobalMuons"),
		cms.InputTag("corMetType1Icone5"),
		cms.InputTag("metNoHF"),
		cms.InputTag("corMetType1Icone5NoHF"),
		cms.InputTag("tauMetCorr")
	),

        #TrackCollection = ctfWithMaterialTracks,iterativeTracks
####	TrackCollection = cms.InputTag("iterativeTracks"),
	TrackCollection = cms.InputTag("generalTracks"),

        #TauJet calibration
	src = cms.InputTag("iterativeCone5CaloJets"),
	tagName = cms.string("IterativeCone0.4_EtScheme_TowerEt0.5_E0.8_Jets871_2x1033PU_tau"),
	TauTriggerType = cms.int32(1),

	# Electron identification
	ReducedBarrelRecHitCollection = cms.InputTag("reducedEcalRecHitsEB"),
	ReducedEndcapRecHitCollection = cms.InputTag("reducedEcalRecHitsEE"),

	ElectronIdLabels = cms.VInputTag(
		cms.InputTag("eidRobustTight"),
		cms.InputTag("eidTight"),
		cms.InputTag("eidLoose"),
		cms.InputTag("eidRobustLoose")
	),

    	# Selection of input variables:
#    	useEoverPIn      = cms.bool(1),
#    	useDeltaEtaIn    = cms.bool(1),
#    	useDeltaPhiIn    = cms.bool(1),
#    	useHoverE        = cms.bool(1),
#    	useE9overE25     = cms.bool(1),
#    	useEoverPOut     = cms.bool(1),
#    	useDeltaPhiOut   = cms.bool(1),
#    	useInvEMinusInvP = cms.bool(0),
#    	useBremFraction  = cms.bool(0),
#    	useSigmaEtaEta   = cms.bool(1),
#    	useSigmaPhiPhi   = cms.bool(1),

#	barrelClusterShapeAssociation = cms.InputTag("hybridSuperClusters","hybridShapeAssoc"),
#	endcapClusterShapeAssociation = cms.InputTag("islandBasicClusters","islandEndcapShapeAssoc"),

#	algo_psets = cms.VPSet(cms.PSet(using PTDR_ID), cms.PSet(using CutBased_ID))
#	VPSet algo_psets = {
#            {using PTDR_ID}, {using CutBased_ID}
#    	}

    	# Electron quality for cut based ID. Can be:
    	# "loose"  - e.g. suitable for H->ZZ->4l
    	# "medium" - intermediate quality
    	# "tight"  - e.g. suitable for H->WW->2l2nu
#	electronQuality = cms.string("loose"),
#
#	looseEleIDCuts = cms.PSet(
#	    EoverPInMax     = cms.vdouble( 1.3,   1.2,   1.3,   999.,  999.,  999.,  999.,  999.  ),
#   	    EoverPInMin     = cms.vdouble( 0.9,   0.9,   0.9,   0.6,   0.9,   0.9,   0.9,   0.7   ),
#    	    deltaEtaIn      = cms.vdouble( 0.004, 0.006, 0.005, 0.007, 0.007, 0.008, 0.007, 0.008 ),
#    	    deltaPhiIn      = cms.vdouble( 0.04,  0.07,  0.04,  0.08,  0.06,  0.07,  0.06,  0.07  ),
#    	    HoverE          = cms.vdouble( 0.06,  0.05,  0.06,  0.14,  0.1,   0.1,   0.1,   0.12  ),
#    	    E9overE25       = cms.vdouble( 0.7,   0.75,  0.8,   0.,    0.85,  0.75,  0.8,   0.    ),
#    	    EoverPOutMax    = cms.vdouble( 2.5,   999.,  999.,  999.,  2.,    999.,  999.,  999.  ),
#    	    EoverPOutMin    = cms.vdouble( 0.6,   1.8,   1.,    0.75,  0.6,   1.5,   1.,    0.8   ),
#    	    deltaPhiOut     = cms.vdouble( 0.011, 999.,  999.,  999.,  0.02,  999.,  999.,  999.  ),
#    	    invEMinusInvP   = cms.vdouble( 0.02,  0.02,  0.02,  0.02,  0.02,  0.02,  0.02,  0.02  ),
#    	    bremFraction    = cms.vdouble( 0.,    0.1,   0.1,   0.1,   0.,    0.2,   0.2,   0.2   ),
#    	    sigmaEtaEtaMax  = cms.vdouble( 0.011, 0.011, 0.011, 0.011, 0.022, 0.022, 0.022, 0.3   ),
#    	    sigmaEtaEtaMin  = cms.vdouble( 0.005, 0.005, 0.005, 0.005, 0.008, 0.008, 0.008, 0.    ),
#    	    sigmaPhiPhiMax  = cms.vdouble( 0.015, 999.,  999.,  999.,  0.02,  999.,  999.,  999.  ),
#    	    sigmaPhiPhiMin  = cms.vdouble( 0.005, 0.,    0.,    0.,    0.,    0.,    0.,    0.    )
#    	)
	
)

# module execution
process.runEDAna = cms.Path(process.hPlusAnalysis)



process.TESTOUT = cms.OutputModule("PoolOutputModule",
#    outputCommands = cms.untracked.vstring(
#        "drop *",
#        "keep recoCaloMETs_*_*_*"
#    ),
    fileName = cms.untracked.string('file:testout.root')
)
#process.outpath = cms.EndPath(process.TESTOUT)
