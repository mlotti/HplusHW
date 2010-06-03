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
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(20) )

process.source = cms.Source('PoolSource',
  duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
  fileNames = cms.untracked.vstring(
    #'file:datatest500.root'
     'file:AE250FF9-12C2-DE11-B56B-001E4F3D3147.root',
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
    #       '/store/data/Commissioning10/MinimumBias/RECO/v7/000/132/440/8C51BAC6-1A3C-DF11-A0EE-000423D94A04.root',
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
	
from RecoTauTag.RecoTau.PFRecoTauProducer_cfi import *

process.HPlusHLTTrigger = cms.EDFilter('HPlusTriggering',
  TriggersToBeApplied = cms.vstring(
    #"HLT_Jet15U"
    "HLT_Jet30U"
    #"HLT_DiJetAve15U_8E29"
    #"HLT_QuadJet15U"
  ),
  TriggersToBeSaved = cms.vstring(
    "HLT_Jet30U",
    "HLT_DiJetAve15U_8E29",
    "HLT_QuadJet15U"
  ),
  PrintTriggerNames = cms.bool(False)
)

process.HPlusGlobalMuonVeto = cms.EDFilter('HPlusGlobalMuonVeto',
  MuonCollectionName = cms.InputTag("muons"),
  MaxMuonPtCutValue = cms.double(15),
  IsHistogrammedStatus = cms.bool(True)
)

process.HPlusTauIDRootFileDumper = cms.EDProducer('HPlusTauIDRootFileDumper',
  tauCollectionName       = cms.InputTag("shrinkingConePFTauProducer"),
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

process.out = cms.OutputModule("PoolOutputModule",
  fileName = cms.untracked.string('HPlusOut.root'),
  outputCommands = cms.untracked.vstring(
    "drop *",
    "keep *_*_*_HPLUS"
  )
)
################################################################################

MySelection = cms.Sequence (
  process.HPlusHLTTrigger *
  process.HPlusGlobalMuonVeto
)

process.p = cms.Path(
  MySelection *
  process.HPlusTauIDRootFileDumper
)

process.e = cms.EndPath(process.out)
