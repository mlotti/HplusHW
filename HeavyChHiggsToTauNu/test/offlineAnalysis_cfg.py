import FWCore.ParameterSet.Config as cms
import os

def getEnvVar(var, default=None):
    if os.environ.has_key(var):
        return os.environ.get(var)
    else:
        return default

maxEvt = int(getEnvVar("MYMAXEVENTS", 10))
files = getEnvVar("MYINPUTFILES")

summer08 = True

process = cms.Process("test")

#process.Tracer = cms.Service("Tracer")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(maxEvt)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#"file:/tmp/slehti/QCD_Pt80_OctX.root"
    "rfio:/castor/cern.ch/user/s/slehti/QCD_Pt80_OctX.root"
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
#process.MessageLogger.debugModules = cms.untracked.vstring("*")
#process.MessageLogger.cerr = cms.untracked.PSet(threshold = cms.untracked.string("DEBUG"))

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.GlobalTag.globaltag = 'IDEAL_31X::All'
#process.GlobalTag.globaltag = 'STARTUP31X_V1::All'
process.GlobalTag.globaltag = 'MC_31X_V3::All'
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

process.hPlusAnalysis = cms.EDAnalyzer('OfflineAnalysis',
        TrackAssociator.TrackAssociatorParameterBlock,
        fileName = cms.string("analysis.root"),

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
                cms.InputTag("jetBProbabilityBJetTags"),
                cms.InputTag("jetProbabilityBJetTags"),
                cms.InputTag("simpleSecondaryVertexBJetTags"),
                cms.InputTag("softElectronByIP3dBJetTags"),
		cms.InputTag("softElectronByPtBJetTags"),
                cms.InputTag("softMuonBJetTags"),
                cms.InputTag("softMuonByIP3dBJetTags"),
		cms.InputTag("softMuonByPtBJetTags")
        ),

	METCollections = cms.VInputTag(
		cms.InputTag("met"),
		cms.InputTag("metHO"),
		cms.InputTag("metNoHFHO"),
		cms.InputTag("metNoHF"),
		cms.InputTag("metOptHO"),
		cms.InputTag("metOptNoHFHO"),
		cms.InputTag("metOptNoHF"),
		cms.InputTag("metOpt"),
		cms.InputTag("corMetGlobalMuons"),
		cms.InputTag("metJESCorIC5CaloJet"),
		cms.InputTag("metJESCorIC5CaloJetMuons"),
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
