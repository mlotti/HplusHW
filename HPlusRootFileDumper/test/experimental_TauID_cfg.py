import FWCore.ParameterSet.Config as cms

process = cms.Process("tauID")

# Message logger
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.categories.append("HPlusRootFileDumper")
process.MessageLogger.cerr = cms.untracked.PSet(
  placeholder = cms.untracked.bool(True)
)
process.MessageLogger.cout = cms.untracked.PSet(
  INFO = cms.untracked.PSet(
#   reportEvery = cms.untracked.int32(100), # every 100th only
   #limit = cms.untracked.int32(100)       # or limit to 100 printouts...
  )
)
process.MessageLogger.statistics.append('cout')


process.load('Configuration/StandardSequences/Services_cff')

# Standard sequences
process.load('Configuration/StandardSequences/RawToDigi_Data_cff')
process.load('Configuration/StandardSequences/L1Reco_cff')
process.load('Configuration/StandardSequences/Reconstruction_cff')
process.load('DQMOffline/Configuration/DQMOffline_cff')
process.load('Configuration/StandardSequences/EndOfProcess_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.load('Configuration/EventContent/EventContent_cff')

# Global tag - is this necessary, what does it do?
process.GlobalTag.globaltag = cms.string('GR09_R_34X_V2::All')

# Hplus skimming
process.load("HiggsAnalysis.Skimming.heavyChHiggsToTauNu_SkimPaths_cff")


# Jet ET corrections (included in 3_6_0)
#process.load('JetMETCorrections.Configuration.DefaultJEC_cff')

# Calo tau producer
process.load('RecoTauTag/RecoTau/CaloRecoTauTagInfoProducer_cfi')
process.caloRecoTauTagInfoProducer.CaloJetTracksAssociatorProducer = cms.InputTag('ak5JetTracksAssociatorAtVertex')
process.caloRecoTauTagInfoProducer.tkQuality = cms.string('highPurity')

#process.load('RecoTauTag/Configuration/python/RecoTauTag_cff')

# Choose techical bits 40 and coincidence with BPTX (0)
process.load('L1TriggerConfig.L1GtConfigProducers.L1GtTriggerMaskTechTrigConfig_cff')
process.load('HLTrigger/HLTfilters/hltLevel1GTSeed_cfi')
process.hltLevel1GTSeed.L1TechTriggerSeeding = cms.bool(True)
process.hltLevel1GTSeed.L1SeedsLogicalExpression = cms.string('0 AND 40 AND NOT (36 OR 37 OR 38 OR 39)')
# HLT
process.hltHighLevel = cms.EDFilter("HLTHighLevel",
     TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
      HLTPaths = cms.vstring('HLT_PhysicsDeclared'),           # provide list of HLT paths (or patterns) you want
 #    HLTPaths = cms.vstring('HLT_MinBiasBSC'),           # provide list of HLT paths (or patterns) you want
     eventSetupPathsKey = cms.string(''), # not empty => use read paths from AlCaRecoTriggerBitsRcd via this key
     andOr = cms.bool(True),             # how to deal with multiple triggers: True (OR) accept if ANY is true, False (AND) accept if ALL are true
     throw = cms.bool(True)    # throw exception on unknown path names
)
# remove monster events
process.monster = cms.EDFilter(
    "FilterOutScraping",
    applyfilter = cms.untracked.bool(True),
    debugOn = cms.untracked.bool(True),
    numtrack = cms.untracked.uint32(10),
    thresh = cms.untracked.double(0.2)
    )


#process.options = cms.untracked.PSet(
#     SkipEvent = cms.untracked.vstring('Unknown',
#         'ProductNotFound',
#         'DictionaryNotFound',
#         'InsertFailure',
#         'Configuration',
#         'LogicError',
#         'UnimplementedFeature',
#         'InvalidReference',
#         'NullPointerError',
#         'NoProductSpecified',
#         'EventTimeout',
#         'EventCorruption',
#         'ModuleFailure',
#         'ScheduleExecutionFailure',
#         'EventProcessorFailure',
#         'FileInPathError',
#         'FatalRootError',
#         'NotFound')
#)
###############################################################################


# Configuration of the ROOT file dumper
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(20) )

process.source = cms.Source("PoolSource",
  #duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
  fileNames = cms.untracked.vstring(
    'file:AE250FF9-12C2-DE11-B56B-001E4F3D3147.root'
    #'file:PYTHIA6_Tauola_TTbar_WtoTauNu_7TeV_cff_py_RAW2DIGI_RECO_990.root',
    #'file:PYTHIA6_Tauola_TTbar_WtoTauNu_7TeV_cff_py_RAW2DIGI_RECO_999.root'
  )
)

# Job will exit if any product is not found in the event
process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring("ProductNotFound")
)

process.TFileService = cms.Service("TFileService",
  fileName = cms.string('HPlusRootFileDumper.root')
)
	
from RecoTauTag.RecoTau.PFRecoTauProducer_cfi import *

process.HPlusTauIDRootFileDumper = cms.EDAnalyzer('HPlusTauIDRootFileDumper',
  #tauCollectionName       = cms.InputTag("shrinkingConePFTauProducer"),
  tauCollectionName       = cms.InputTag("caloRecoTauProducer"),
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
#      calojets         = cms.string('ak5CaloJets'),
#      jetsID           = cms.string('ak5JetID'),
#      jetExtender      = cms.string('ak5JetExtender')
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

process.p = cms.Path(
    process.hltLevel1GTSeed *
    process.hltHighLevel *
    process.monster *
    process.tautagging *
    process.HPlusTauIDRootFileDumper)

################################################################################
process.load("HiggsAnalysis.Skimming.heavyChHiggsToTauNu_SkimPaths_cff")
process.load("HiggsAnalysis.Skimming.heavyChHiggsToTauNu_EventContent_cff")
process.heavyChHiggsToTauNuHLTFilter.HLTPaths = ['HLT_Jet30']
process.heavyChHiggsToTauNuFilter.minNumberOfJets = cms.int32(4)

process.out = cms.OutputModule("PoolOutputModule",
    process.heavyChHiggsToTauNuEventSelection,
    fileName = cms.untracked.string('HPlusOut.root'),
    outputCommands = cms.untracked.vstring(
        "drop *",
        "keep *_HPlus*_*_HPLUS"
    )
)
################################################################################
process.e = cms.EndPath(process.out)
