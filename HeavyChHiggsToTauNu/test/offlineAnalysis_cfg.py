import FWCore.ParameterSet.Config as cms
import os

summer08 = True

process = cms.Process("test")

#process.Tracer = cms.Service("Tracer")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)

# Job will exit if any product is not found in the event
process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring("ProductNotFound")
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'rfio:/castor/cern.ch/user/s/slehti/testData/Ztautau_GEN_SIM_RECO_MC_31X_V2_preproduction_311_v1.root'
    )
)

#if files:
#    for file in files.split(" "):
#        print "Append file %s to list of input files" % file
#        process.source.fileNames.append(file)
#else:
##    process.source.fileNames.append("root://madhatter.csc.fi/pnfs/csc.fi/data/cms/Events_matti/muon2tau/TTJets_Fall08_cmssw2117/digi_muon_223/digi_muon_hltskim_402.root")
#    process.source.fileNames.append("rfio:/castor/cern.ch/cms/store/relval/CMSSW_2_2_4/RelValTTbar/GEN-SIM-RECO/STARTUP_V8_v1/0000/200EB7E3-90F3-DD11-B1B0-001D09F2432B.root")


# Message Logger
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100
#process.MessageLogger.debugModules = cms.untracked.vstring("*")
#process.MessageLogger.cerr = cms.untracked.PSet(threshold = cms.untracked.string("DEBUG"))

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.GlobalTag.globaltag = 'IDEAL_31X::All'
process.GlobalTag.globaltag = 'START3X_V18::All'
#process.GlobalTag.globaltag = 'MC_3XY_V18::All'
#process.GlobalTag.globaltag = cms.string('GR09_R_34X_V2::All')

# Magnetic Field
#process.load("Configuration/StandardSequences/MagneticField_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load('Configuration/StandardSequences/Services_cff')
process.load('Configuration/StandardSequences/Geometry_cff')

from Geometry.CaloEventSetup.CaloTopology_cfi import *
process.load("RecoEgamma.ElectronIdentification.electronIdCutBasedExt_cfi")
from RecoEgamma.ElectronIdentification.electronIdCutBasedExt_cfi import *
process.load("RecoEgamma.ElectronIdentification.electronIdCutBasedClassesExt_cfi")
from RecoEgamma.ElectronIdentification.electronIdCutBasedClassesExt_cfi import *

# Calo geometry service model
process.load("Geometry.CaloEventSetup.CaloGeometry_cfi")
# Calo topology service model
process.load("Geometry.CaloEventSetup.CaloTopology_cfi")
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")

process.load("JetMETCorrections.Configuration.JetCorrectionsHLT_cff")
process.load("JetMETCorrections.Configuration.L2L3Corrections_Summer09_cff")

process.load("JetMETCorrections.Type1MET.MetMuonCorrections_cff")
process.load("RecoMET.METProducers.CaloMET_cfi")
#process.missingEt = cms.Path(process.metNoHF)

process.load("JetMETCorrections.Type1MET.MetType1Corrections_cff")
process.missingEt_type1i = cms.Path(process.metJESCorIC5CaloJet)
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


process.load("JetMETCorrections.Type1MET.MetMuonCorrections_cff")
#process.missingEt_muons = cms.Path(process.corMetGlobalMuons) # 3_2_4

from RecoTauTag.RecoTau.PFRecoTauProducer_cfi import *
process.load("JetMETCorrections.Type1MET.TauMetCorrections_cff")
process.tauMetCorr.InputMETLabel = cms.string('metJESCorIC5CaloJet')
####FIXMEprocess.missingEt_tauMet = cms.Path(process.tauMetCorr)

process.load("RecoTracker.TransientTrackingRecHit.TransientTrackingRecHitBuilderWithoutRefit_cfi")
import TrackingTools.TrackAssociator.default_cfi as TrackAssociator

# PAT Layer 0+1
process.load("PhysicsTools.PatAlgos.patSequences_cff")
process.p = cms.Path(process.patDefaultSequence)


# TCTau
process.load("JetMETCorrections/TauJet/TCTauProducer_cff")
process.runTCTauProducer = cms.Path(
    process.TCTau
)


process.TauMCProducer = cms.EDProducer("HLTTauMCProducer",
        GenParticles  = cms.untracked.InputTag("genParticles"),
        ptMinTau      = cms.untracked.double(3),
        ptMinMuon     = cms.untracked.double(3),
        ptMinElectron = cms.untracked.double(3),
        BosonID       = cms.untracked.vint32(23),
        EtaMax         = cms.untracked.double(2.5)
)
process.visibleTau = cms.Path(process.TauMCProducer)


process.hPlusAnalysis = cms.EDAnalyzer('OfflineAnalysis',
        TrackAssociator.TrackAssociatorParameterBlock,
        fileName = cms.string("analysis.root"),

        # JetEnergyCorrection = MCJetCorrectorIcone5,MCJetCorrectorMcone5
        # if no corrections, leave {} empty
	JetEnergyCorrection = cms.vstring(
		"MCJetCorrectorIcone5"
#		"MCJetCorrectorMcone5"
	),

        # b tagging elgorithms
        BTaggingAlgorithms = cms.vstring(
                "trackCountingHighPurBJetTags",
                "trackCountingHighEffBJetTags",
                "combinedSecondaryVertexBJetTags",
                "combinedSecondaryVertexMVABJetTags",
                "jetBProbabilityBJetTags",
                "jetProbabilityBJetTags",
                "simpleSecondaryVertexBJetTags",
                "softElectronByIP3dBJetTags",
		"softElectronByPtBJetTags",
                "softMuonBJetTags",
                "softMuonByIP3dBJetTags",
		"softMuonByPtBJetTags"
        ),

        Vertices = cms.InputTag("pixelVertices"),
        GsfElectrons = cms.VInputTag(
#                cms.InputTag("gsfElectrons")
        ),
        PATElectrons = cms.VInputTag(
                cms.InputTag("cleanLayer1Electrons")
        ),
#        Photons = cms.VInputTag(
#                cms.InputTag("correctedPhotons")
#        ),
        Muons = cms.VInputTag(
                 cms.InputTag("muons")
        ),
        PATMuons = cms.VInputTag(
#                 cms.InputTag("cleanLauer1Muons")
        ),
        CaloTaus = cms.VPSet(
            cms.PSet(src = cms.InputTag("caloRecoTauProducer"), corrections = cms.vstring("TauJetCorrector"))
        ),
        PFTaus = cms.VInputTag(
                 cms.InputTag("fixedConePFTauProducer"),
                 cms.InputTag("fixedConeHighEffPFTauProducer"),
                 cms.InputTag("shrinkingConePFTauProducer")
        ),
        PATTaus = cms.VInputTag(
#                 cms.InputTag("cleanLayer1Taus")
        ),
	TCTaus = cms.VInputTag(
		 cms.InputTag("tcRecoTauProducer")
	),
        CaloJets = cms.VInputTag(
                 cms.InputTag("iterativeCone5CaloJets")
        ),
        PATJets = cms.VInputTag(
#                 cms.InputTag("cleanLayer1Jets")
        ),
        
	# CaloMET collections, more info: https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMETObjects
	# TCMET and PFMET in separate collections, saved by default
#	METCollections = cms.VInputTag(
#		cms.InputTag("met"),
#		cms.InputTag("metHO"),
#		cms.InputTag("metNoHFHO"),
#		cms.InputTag("metNoHF"),
#		cms.InputTag("metOptHO"),
#		cms.InputTag("metOptNoHFHO"),
#		cms.InputTag("metOptNoHF"),
#		cms.InputTag("metOpt"),
#		cms.InputTag("corMetGlobalMuons"),
#		cms.InputTag("metJESCorIC5CaloJet"),
#		cms.InputTag("metJESCorIC5CaloJetMuons"),
#		cms.InputTag("corMetType1Icone5NoHF"),
#		cms.InputTag("tauMetCorr")
#	),

        #TrackCollection = ctfWithMaterialTracks,iterativeTracks
####	TrackCollection = cms.InputTag("iterativeTracks"),
	TrackCollection = cms.InputTag("generalTracks"),

        MuonReplacementMuons = cms.InputTag("selectedMuons"),

        # MC collections
        GenParticles = cms.InputTag("genParticles"),
	VisibleTaus  = cms.InputTag("TauMCProducer:HadronicTauOneAndThreeProng"),
        MuonReplacementGen = cms.InputTag("DUMMY"),
        GenJets = cms.InputTag("iterativeCone5GenJets"),
        SimHits = cms.InputTag("g4SimHits"),
        
        #TauJet calibration
	src = cms.InputTag("iterativeCone5CaloJets"),
	tagName = cms.string("IterativeCone0.4_EtScheme_TowerEt0.5_E0.8_Jets871_2x1033PU_tau"),
	TauTriggerType = cms.int32(1),

        BarrelBasicClustersSource = cms.InputTag("hybridSuperClusters", "hybridBarrelBasicClusters"),
        EndcapBasicClustersSource = cms.InputTag("multi5x5BasicClusters", "multi5x5EndcapBasicClusters"),

	# Electron identification
	ReducedBarrelRecHitCollection = cms.InputTag("reducedEcalRecHitsEB"),
	ReducedEndcapRecHitCollection = cms.InputTag("reducedEcalRecHitsEE"),

	ElectronIdLabels = cms.VInputTag(
		cms.InputTag("eidRobustTight"),
		cms.InputTag("eidTight"),
		cms.InputTag("eidLoose"),
		cms.InputTag("eidRobustLoose")
	)
)

# module execution
process.runEDAna = cms.Path(process.hPlusAnalysis)


#process.TESTOUT = cms.OutputModule("PoolOutputModule",
#    outputCommands = cms.untracked.vstring(
#        "drop *",
#        "keep patMuons_*_*_*"
#    ),
#    fileName = cms.untracked.string('file:testout.root')
#)
#process.outpath = cms.EndPath(process.TESTOUT)
