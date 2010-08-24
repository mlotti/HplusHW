import FWCore.ParameterSet.Config as cms

#dataVersion = "35X"
dataVersion = "36X"
#dataVersion = "37X"

process = cms.Process("HChPatTuple")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.GlobalTag.globaltag = cms.string('GR10_P_V6::All') # GR10_P_V6::All
if dataVersion == "37X":
    process.GlobalTag.globaltag = cms.string("START37_V6::All")
else:
    process.GlobalTag.globaltag = cms.string("START36_V10::All")

process.GlobalTag.globaltag = cms.string("START38_V9::All")

process.source = cms.Source('PoolSource',
  duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
  fileNames = cms.untracked.vstring(
    "/store/mc/Summer10/WJets_7TeV-madgraph-tauola/AODSIM/START36_V9_S09-v1/0046/FEFEE1D1-F17B-DF11-B911-00304867C16A.root"
#       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/FA6E6683-C844-DF11-A2D8-0018F3D0961E.root',
#       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/D0E1C289-C744-DF11-B84C-00261894389F.root',
#       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/A24BB684-C544-DF11-81ED-00261894391D.root',
#       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/284100C7-4E45-DF11-9AF9-0018F3D09710.root',
#       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/06A4E187-C644-DF11-BC3E-0018F3D096AA.root'
  )
)
if dataVersion == "35X":
    process.source.fileNames = cms.untracked.vstring(
	"rfio:/castor/cern.ch/user/s/slehti/testData/testHplus_35X.root"
#        '/store/relval/CMSSW_3_5_8/RelValZTT/GEN-SIM-RECO/START3X_V26-v1/0017/86C58057-8F52-DF11-9160-002618FDA28E.root',
#        '/store/relval/CMSSW_3_5_8/RelValZTT/GEN-SIM-RECO/START3X_V26-v1/0016/FC9BCE19-5152-DF11-8EDC-002618FDA204.root',
#        '/store/relval/CMSSW_3_5_8/RelValZTT/GEN-SIM-RECO/START3X_V26-v1/0016/64D9835B-5052-DF11-8343-002618FDA279.root',
#        '/store/relval/CMSSW_3_5_8/RelValZTT/GEN-SIM-RECO/START3X_V26-v1/0016/50C0224A-4F52-DF11-B8A0-002618943906.root',
#        '/store/relval/CMSSW_3_5_8/RelValZTT/GEN-SIM-RECO/START3X_V26-v1/0016/207DFCE2-4F52-DF11-8D25-0018F3D096BA.root'
    )
    


################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
del process.TFileService

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('pattuple.root'),
    outputCommands = cms.untracked.vstring(
        "drop *",
        "keep *_genParticles_*_*",
        "keep GenEventInfoProduct_*_*_*",
        "keep GenRunInfoProduct_*_*_*",
        "keep edmTriggerResults_*_*_*",
        "keep triggerTriggerEvent_*_*_*"
    )
)

# PAT Layer 0+1
process.load("PhysicsTools.PatAlgos.patSequences_cff")
from PhysicsTools.PatAlgos.patEventContent_cff import *


process.patJets.jetSource = cms.InputTag("ak5CaloJets")
process.patJets.trackAssociationSource = cms.InputTag("ak5JetTracksAssociatorAtVertex")
process.patJets.addJetID = False

from PhysicsTools.PatAlgos.tools.tauTools import *
#process.patTaus.tauSource = cms.InputTag("fixedConePFTauProducer")
switchToPFTauFixedCone(process)
#process.patPFTauProducerFixedCone = copy.deepcopy(process.patTaus)

process.selectedPatJets.cut='pt > 10 & abs(eta) < 2.4 & associatedTracks().size() > 0'
process.selectedPatMuons.cut='pt > 10 & abs(eta) < 2.4 & isGlobalMuon() & !track().isNull()'
process.selectedPatElectrons.cut='pt > 10 & abs(eta) < 2.4 & !gsfTrack().isNull()'
process.selectedPatTaus.cut=('pt > 10 & abs(eta) < 2.4'+
                     '& tauID("leadingTrackFinding") > 0.5 & tauID("leadingPionPtCut") > 0.5'+
                     '& tauID("byIsolationUsingLeadingPion") > 0.5'+
                     '& tauID("againstMuon") > 0.5 & tauID("againstElectron") > 0.5')
process.patTaus.embedLeadTrack = True
process.patTaus.embedSignalTracks = True
process.patTaus.embedIsolationTracks = True

process.out.outputCommands.extend(patEventContentNoCleaning)


from PhysicsTools.PatAlgos.tools.metTools import *
addTcMET(process, 'TC')
addPfMET(process, 'PF')
process.out.outputCommands.extend(["keep *_patMETsPF_*_*", "keep *_patMETsTC_*_*"])

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
process.out.outputCommands.append("keep *_selectedPatJetsAK5JPT_*_*")

#### needed for CMSSW35x data
if dataVersion == "35X": 
    process.load("RecoJets.Configuration.GenJetParticles_cff")
    process.load("RecoJets.Configuration.RecoGenJets_cff")
    ## creating JPT jets
    process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
    process.load('RecoJets.Configuration.RecoJPTJets_cff')

    from PhysicsTools.PatAlgos.tools.cmsswVersionTools import *
    run36xOn35xInput(process)


####from PhysicsTools.PatAlgos.tools.coreTools import *
####removeMCMatching(process)

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.ChargedHiggsTauIDDiscrimination_cfi")

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChTriggerObjects_cfi")
#process.patTriggerMatcher += process.tauTriggerMatchHLTSingleLooseIsoTau20
#process.patTriggerMatcher.remove( process.patTriggerMatcherElectron )
#process.patTriggerMatcher.remove( process.patTriggerMatcherMuon )
from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
process.load("PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff")
process.patDefaultSequence += process.patTriggerSequence

# Add the correct trigger
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTrigger_cfi as HChTrigger
HChTrigger.customise(process, dataVersion)
switchOnTrigger(process)


################################################################################
#print process.dumpPython()

process.s = cms.Sequence (
    process.hplusTauDiscriminationSequence *
    process.patDefaultSequence
)
if dataVersion == "35X":
    process.s = cms.Sequence (
        #for 35X
        process.genJetParticles *
        process.ak5GenJets *
        process.recoJPTJets *
        #
	process.hplusTauDiscriminationSequence *
        process.patDefaultSequence
    )

process.path    = cms.Path(process.s)

################################################################################

# process.out = cms.OutputModule("PoolOutputModule",
# #    process.heavyChHiggsToTauNuEventSelection,
# #    SelectEvents = cms.untracked.PSet(
# #        SelectEvents = cms.vstring("path")
# #    ),
#     fileName = cms.untracked.string('pattuple.root'),
#     outputCommands = outputCommands
# #    outputCommands = cms.untracked.vstring(
# #        "keep *"
# #	"drop *"
# #        "keep 
# #	"keep *_*_*_HChPatTuple",
# #	"drop reco*_*_*_HChSignalAnalysis",
# #	"drop pat*_*_*_HChSignalAnalysis"
# #    )
# )



process.outpath = cms.EndPath(process.out)

