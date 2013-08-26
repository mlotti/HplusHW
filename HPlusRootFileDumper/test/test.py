import FWCore.ParameterSet.Config as cms

process = cms.Process("HPLUS")

# Message logger
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.categories.append("HPlusRootFileDumper")
process.MessageLogger.cerr = cms.untracked.PSet(
  placeholder = cms.untracked.bool(True)
)
process.MessageLogger.cout = cms.untracked.PSet(
  INFO = cms.untracked.PSet(
   #reportEvery = cms.untracked.int32(100), # every 100th only
   #limit = cms.untracked.int32(100)       # or limit to 100 printouts...
  )
)
process.MessageLogger.statistics.append('cout')

# Standard sequences
process.load('Configuration/StandardSequences/Services_cff')
#process.load('Configuration/StandardSequences/RawToDigi_Data_cff')
#process.load('Configuration/StandardSequences/L1Reco_cff')
#process.load('Configuration/StandardSequences/Reconstruction_cff')
#process.load('DQMOffline/Configuration/DQMOffline_cff')
#process.load('Configuration/StandardSequences/EndOfProcess_cff')
#process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')

###############################################################################

# Configuration of the ROOT file dumper
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.source = cms.Source('PoolSource',
  duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
  fileNames = cms.untracked.vstring(
    #'/store/mc/Spring10/TTbar_Htaunu_M140/GEN-SIM-RECO/START3X_V26_S09-v1/0024/EED314DE-DC46-DF11-9646-E41F13181704.root'
    #"rfio:/castor/cern.ch/user/a/attikis/testing/minbias_3_5_x.root")
    #"rfio:/castor/cern.ch/user/a/attikis/testing/summer09_MC_HPlus140.root"
    #'file:datatest500.root'
    #'file:AE250FF9-12C2-DE11-B56B-001E4F3D3147.root',
    # '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/F4C92A98-163C-DF11-9788-0030487C7392.root',
    #        '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/F427D642-173C-DF11-A909-0030487C60AE.root',
    #        '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/E27821C3-0C3C-DF11-9BD9-0030487CD718.root',
    #        '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/D87D5469-2E3C-DF11-A470-000423D99896.root',
    #        '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/B647CAD9-0E3C-DF11-886F-0030487CD716.root',
    #        '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/A860D55E-193C-DF11-BE29-0030487C60AE.root',
    #        '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/9884BC11-0C3C-DF11-8F9C-000423D986C4.root',
    #        '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/92684831-233C-DF11-ABA0-0030487CD16E.root',
    #        '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/90269E76-0D3C-DF11-A1A0-0030487CD840.root',
    #        '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/8CAE3014-133C-DF11-A05D-000423D174FE.root',
           '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/8C51BAC6-1A3C-DF11-A0EE-000423D94A04.root'
    #       '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/8C042B04-2D3C-DF11-939F-0030487CD178.root',
    #       '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/80471A6B-0E3C-DF11-8DCD-0030487C6A66.root',
    #        '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/762824C3-0C3C-DF11-A4FD-0030487CD6D2.root',
    #        '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/6A3533F5-103C-DF11-B3AA-00304879BAB2.root',
    #        '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/4C8979D2-073C-DF11-B97B-000423D6AF24.root',
    #        '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/26C8DED9-0E3C-DF11-9D83-0030487CD7B4.root',
    #        '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/181C44F7-093C-DF11-A9CB-001D09F24FEC.root',
    #        '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/0AA7C390-0F3C-DF11-BD65-000423D998BA.root'
  )
)

# Job will exit if any product is not found in the event
process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring("ProductNotFound")
)

process.TFileService = cms.Service("TFileService",
  fileName = cms.string('HPlusOutInfo.root')
)

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string('GR10_P_V6::All') # GR10_P_V6::All

# Magnetic Field
#process.load("Configuration/StandardSequences/MagneticField_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load('Configuration/StandardSequences/Services_cff')
process.load('Configuration/StandardSequences/Geometry_cff')

# Calo geometry service model
process.load("Geometry.CaloEventSetup.CaloGeometry_cfi")
# Calo topology service model
process.load("Geometry.CaloEventSetup.CaloTopology_cfi")

from RecoTauTag.RecoTau.PFRecoTauProducer_cfi import *

process.load("RecoTracker.TransientTrackingRecHit.TransientTrackingRecHitBuilderWithoutRefit_cfi")
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")   

process.load("RecoBTag.SecondaryVertex.secondaryVertex_cff")
process.btagForPat = cms.Path(process.simpleSecondaryVertexHighEffBJetTags *
                              process.simpleSecondaryVertexHighPurBJetTags)

# PAT Layer 0+1
process.load("PhysicsTools.PatAlgos.patSequences_cff")
from PhysicsTools.PatAlgos.tools.coreTools import *
removeMCMatching(process)

process.HPlusHLTTrigger = cms.EDFilter('HPlusTriggering',
  TriggerResultsName = cms.InputTag("TriggerResults::HLT"),
  TriggersToBeApplied = cms.vstring(
#    "HLT_Jet30"
  ),
  TriggersToBeSaved = cms.vstring(
    #"HLT_Jet30",
    #"HLT_DiJetAve15U_1E31",
    #"HLT_DiJetAve30U_1E31",
    #"HLT_QuadJet30",
    #"HLT_SingleIsoTau30_Trk5",
    #"HLT_Mu15",
    #"HLT_Ele15_SW_L1R",
    #"HLT_Ele15_SW_EleId_L1R",
    #"HLT_MET35",
  ),
  PrintTriggerNames = cms.bool(False)
)

process.HPlusGlobalElectronVeto = cms.EDFilter('HPlusGlobalElectronVeto',
  #ElectronCollectionName = cms.InputTag("patElectrons"),
  ElectronCollectionName = cms.InputTag("cleanPatElectrons"),
  MaxElectronPtCutValue = cms.double(15),
  ElectronIdentificationType = cms.string("NoElectronIdentification"),
  #ElectronIdentificationType = cms.string("RobustElectronIdentification"),
  #ElectronIdentificationType = cms.string("LooseElectronIdentification"),
  #ElectronIdentificationType = cms.string("TightElectronIdentification"),
  IsHistogrammedStatus = cms.bool(True),
  IsAppliedStatus = cms.bool(True)
)

process.HPlusGlobalMuonVeto = cms.EDFilter('HPlusGlobalMuonVeto',
  MuonCollectionName = cms.InputTag("muons"),
  MaxMuonPtCutValue = cms.double(15),
  IsHistogrammedStatus = cms.bool(True),
  IsAppliedStatus = cms.bool(True)
)

#### The PFTauDecayModes are dropped by default from RECO.  You can add them back in on the fly by doing:
process.load("RecoTauTag.Configuration.ShrinkingConePFTaus_cfi")
#### and then adding "process.shrinkingConePFTauDecayModeProducer" to your sequence/path.

process.HPlusTauIDRootFileDumper = cms.EDProducer('HPlusTauIDRootFileDumper',
#  tauCollectionName       = cms.InputTag("shrinkingConePFTauProducer"),
  tauCollectionName       = cms.InputTag("fixedConePFTauProducer"),
#  tauCollectionName       = cms.InputTag("caloRecoTauProducer"),
  CaloTaus = cms.VPSet(
    cms.PSet(
      src = cms.InputTag("caloRecoTauProducer", "", "RECO"),
      discriminators = cms.VInputTag(
	cms.InputTag("caloRecoTauDiscriminationAgainstElectron", "", "RECO"),
	cms.InputTag("caloRecoTauDiscriminationByIsolation", "", "RECO"),
	cms.InputTag("caloRecoTauDiscriminationByLeadingTrackFinding", "", "RECO"),
	cms.InputTag("caloRecoTauDiscriminationByLeadingTrackPtCut", "", "RECO")
      ),
      corrections = cms.vstring("TauJetCorrector"),
      calojets         = cms.string('ak5CaloJets'),
      jetsID           = cms.string('ak5JetID'),
      jetExtender      = cms.string('ak5JetExtender')
    )
  ),
  TCTaus = cms.VPSet(
    cms.PSet(
      src = cms.InputTag("tcRecoTauProducer"),
      discriminators = cms.VInputTag(
	cms.InputTag("caloRecoTauDiscriminationAgainstElectron", "", "test"),
	cms.InputTag("caloRecoTauDiscriminationByIsolation", "", "test"),
	cms.InputTag("caloRecoTauDiscriminationByLeadingTrackFinding", "", "test"),
	cms.InputTag("caloRecoTauDiscriminationByLeadingTrackPtCut", "", "test")
      ),
      corrections = cms.vstring()
    )
  ),
  PFTaus = cms.VPSet(
    cms.PSet(
      src            =  cms.InputTag("fixedConePFTauProducer"),
      discriminators = cms.VInputTag(
	cms.InputTag("fixedConePFTauDiscriminationAgainstElectron"),
	cms.InputTag("fixedConePFTauDiscriminationAgainstMuon"),
	cms.InputTag("fixedConePFTauDiscriminationByECALIsolation"),
	cms.InputTag("fixedConePFTauDiscriminationByECALIsolationUsingLeadingPion"),
	cms.InputTag("fixedConePFTauDiscriminationByIsolation"),
	cms.InputTag("fixedConePFTauDiscriminationByIsolationUsingLeadingPion"),
	cms.InputTag("fixedConePFTauDiscriminationByLeadingPionPtCut"),
	cms.InputTag("fixedConePFTauDiscriminationByLeadingTrackFinding"),
	cms.InputTag("fixedConePFTauDiscriminationByLeadingTrackPtCut"),
	cms.InputTag("fixedConePFTauDiscriminationByTrackIsolation"),
	cms.InputTag("fixedConePFTauDiscriminationByTrackIsolationUsingLeadingPion")
      )
    ),
    cms.PSet(
      src            = cms.InputTag("shrinkingConePFTauProducer"),
      discriminators = cms.VInputTag(
	cms.InputTag("shrinkingConePFTauDecayModeIndexProducer"),
	cms.InputTag("shrinkingConePFTauDiscriminationAgainstElectron"),
	cms.InputTag("shrinkingConePFTauDiscriminationAgainstMuon"),
	cms.InputTag("shrinkingConePFTauDiscriminationByECALIsolation"),
	cms.InputTag("shrinkingConePFTauDiscriminationByECALIsolationUsingLeadingPion"),
	cms.InputTag("shrinkingConePFTauDiscriminationByIsolation"),
	cms.InputTag("shrinkingConePFTauDiscriminationByIsolationUsingLeadingPion"),
	cms.InputTag("shrinkingConePFTauDiscriminationByLeadingPionPtCut"),
	cms.InputTag("shrinkingConePFTauDiscriminationByLeadingTrackFinding"),
	cms.InputTag("shrinkingConePFTauDiscriminationByLeadingTrackPtCut"),
	cms.InputTag("shrinkingConePFTauDiscriminationByTaNC"),
	cms.InputTag("shrinkingConePFTauDiscriminationByTaNCfrHalfPercent"),
	cms.InputTag("shrinkingConePFTauDiscriminationByTaNCfrOnePercent"),
	cms.InputTag("shrinkingConePFTauDiscriminationByTaNCfrQuarterPercent"),
	cms.InputTag("shrinkingConePFTauDiscriminationByTaNCfrTenthPercent"),
	cms.InputTag("shrinkingConePFTauDiscriminationByTrackIsolation"),
	cms.InputTag("shrinkingConePFTauDiscriminationByTrackIsolationUsingLeadingPion")
      )
    )
  )
)

################################################################################
process.load("HiggsAnalysis.Skimming.heavyChHiggsToTauNu_SkimPaths_cff")
process.load("HiggsAnalysis.Skimming.heavyChHiggsToTauNu_EventContent_cff")
process.heavyChHiggsToTauNuHLTFilter.HLTPaths = ['HLT_Jet15U']
process.heavyChHiggsToTauNuFilter.minNumberOfJets = cms.int32(0)
process.heavyChHiggsToTauNuHLTFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","HLT")

process.out = cms.OutputModule("PoolOutputModule",
    process.heavyChHiggsToTauNuEventSelection,
    fileName = cms.untracked.string('HPlusOut.root'),
    outputCommands = cms.untracked.vstring(
    	"drop *",
    	"keep *_HPlus*_*_HPLUS"
    )
)
################################################################################

MySelection = cms.Sequence (
  process.HPlusHLTTrigger *
  process.HPlusGlobalElectronVeto *
  process.HPlusGlobalMuonVeto
)

process.mypat = cms.Path(
  process.patDefaultSequence # needed for GlobalMuonVeto on patElectrons  
)

process.p = cms.Path(
  process.shrinkingConePFTauDecayModeProducer *
  MySelection *
  process.HPlusTauIDRootFileDumper
)

process.e = cms.EndPath(process.out)
