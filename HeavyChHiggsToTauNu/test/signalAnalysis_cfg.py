import FWCore.ParameterSet.Config as cms

process = cms.Process("HChSignalAnalysis")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.GlobalTag.globaltag = cms.string('GR10_P_V6::All') # GR10_P_V6::All
process.GlobalTag.globaltag = cms.string("START36_V10::All")

process.source = cms.Source('PoolSource',
  duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
  fileNames = cms.untracked.vstring(
       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/FA6E6683-C844-DF11-A2D8-0018F3D0961E.root',
       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/D0E1C289-C744-DF11-B84C-00261894389F.root',
       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/A24BB684-C544-DF11-81ED-00261894391D.root',
       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/284100C7-4E45-DF11-9AF9-0018F3D09710.root',
       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/06A4E187-C644-DF11-BC3E-0018F3D096AA.root'
  )
)

################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")

# PAT Layer 0+1
process.load("PhysicsTools.PatAlgos.patSequences_cff")

from PhysicsTools.PatAlgos.tools.metTools import *
addTcMET(process, 'TC')
addPfMET(process, 'PF')

from PhysicsTools.PatAlgos.tools.jetTools import *
addJetCollection(process,cms.InputTag('JetPlusTrackZSPCorJetAntiKt5'),
                 'AK5', 'JPT',
                 doJTA        = True,
                 doBTagging   = True,
                 jetCorrLabel = ('AK5','JPT'),
                 doType1MET   = False,
                 doL1Cleaning = False,
                 doL1Counters = True,
                 genJetCollection = cms.InputTag("ak5GenJets"),
                 doJetID      = False
                 )

####from PhysicsTools.PatAlgos.tools.coreTools import *
####removeMCMatching(process)

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChMETs_cfi")

################################################################################

process.s = cms.Sequence (
    process.patDefaultSequence *
#  process.HPlusHLTTrigger *
#  process.HPlusGlobalElectronVeto *
#  process.HPlusGlobalMuonVeto *
    process.HChMETs
#  process.HPlusJetSelection
)
process.path    = cms.Path(process.s)

################################################################################

process.out = cms.OutputModule("PoolOutputModule",
#    process.heavyChHiggsToTauNuEventSelection,
    fileName = cms.untracked.string('HPlusOut.root'),
    outputCommands = cms.untracked.vstring(
#        "keep *"
       "drop *",
	"keep *_*_*_HChSignalAnalysis"
#       "keep *_HPlus*_*_HPLUS"
    )
)
process.outpath = cms.EndPath(process.out)
