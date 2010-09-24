import FWCore.ParameterSet.Config as cms
import copy

from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoCleaning
from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection
from PhysicsTools.PatAlgos.tools.cmsswVersionTools import run36xOn35xInput
from PhysicsTools.PatAlgos.tools.tauTools import switchToPFTauFixedCone
from PhysicsTools.PatAlgos.tools.metTools import addTcMET, addPfMET
from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
from PhysicsTools.PatAlgos.tools.coreTools import removeMCMatching
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTrigger_cfi as HChTrigger
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTaus_cfi as HChTaus
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTausCont_cfi as HChTausCont

# Assumes that process.out is the output module
#
#
# process      cms.Process object
# dataVersion  Version of the input data (needed for the trigger info process name) 
def addPat(process, dataVersion):
    out = None
    outdict = process.outputModules_()
    if outdict.has_key("out"):
        out = outdict["out"]

    # Tau Discriminators
    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.ChargedHiggsTauIDDiscrimination_cfi")


    # PAT Layer 0+1
    process.load("PhysicsTools.PatAlgos.patSequences_cff")

    process.hplusPatSequence = cms.Sequence(
        process.hplusTauDiscriminationSequence *
        process.patDefaultSequence
    )

    # Remove MC stuff if we have collision data (has to be done any add*Collection!)
    if dataVersion == "data":
        removeMCMatching(process, ["All"])

    # Jets
    process.patJets.jetSource = cms.InputTag("ak5CaloJets")
    process.patJets.trackAssociationSource = cms.InputTag("ak5JetTracksAssociatorAtVertex")
    process.patJets.addJetID = False

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
    if out != None:
        out.outputCommands.append("keep *_selectedPatJetsAK5JPT_*_*")

    #### needed for CMSSW35x data
    if dataVersion in ["35X", "35Xredigi"]: 
        process.load("RecoJets.Configuration.GenJetParticles_cff")
        process.load("RecoJets.Configuration.RecoGenJets_cff")
        ## creating JPT jets
        process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
        process.load('RecoJets.Configuration.RecoJPTJets_cff')

        run36xOn35xInput(process)


    # Taus
    switchToPFTauFixedCone(process)

    process.patTaus.embedLeadTrack = True
    process.patTaus.embedSignalTracks = True
    process.patTaus.embedIsolationTracks = True

    process.patTaus.embedLeadPFCand = True
    process.patTaus.embedLeadPFChargedHadrCand = True
    process.patTaus.embedLeadPFNeutralCand = True

    process.patTaus.embedSignalPFCands = True
    process.patTaus.embedSignalPFChargedHadrCands = True
    process.patTaus.embedSignalPFNeutralHadrCands = True
    process.patTaus.embedSignalPFGammaCands = True

    process.patTaus.embedIsolationPFCands = True
    process.patTaus.embedIsolationPFChargedHadrCands = True
    process.patTaus.embedIsolationPFNeutralHadrCands = True
    process.patTaus.embedIsolationPFGammaCands = True

    process.patTaus.tauIDSources = HChTaus.tauIDSources("fixedConePFTau")

    # Continuous tau discriminators
    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.ChargedHiggsTauIDDiscriminationContinuous_cfi")
    process.hplusTauDiscriminationSequence *= process.hplusTauContinuousDiscriminationSequence
    HChTausCont.tauIDSourcesCont(process.patTaus.tauIDSources,"fixedConePFTau")    

    process.patPFTauProducerFixedCone = copy.deepcopy(process.patTaus)
    process.hplusPatSequence *= process.patPFTauProducerFixedCone

    # Preselections of objects
#    process.selectedPatJets.cut='pt > 10 & abs(eta) < 2.4 & associatedTracks().size() > 0'
#    process.selectedPatMuons.cut='pt > 10 & abs(eta) < 2.4 & isGlobalMuon() & !track().isNull()'
#    process.selectedPatElectrons.cut='pt > 10 & abs(eta) < 2.4 & !gsfTrack().isNull()'
#    process.selectedPatTaus.cut=('pt > 10 & abs(eta) < 2.4'+
#                                 '& tauID("leadingTrackFinding") > 0.5 & tauID("leadingPionPtCut") > 0.5'+
#                                 '& tauID("byIsolationUsingLeadingPion") > 0.5'+
#                                 '& tauID("againstMuon") > 0.5 & tauID("againstElectron") > 0.5')

    # Add PAT default event content
    if out != None:
        out.outputCommands.extend(patEventContentNoCleaning)
	out.outputCommands.extend(["drop *_selectedPatTaus_*_*",
                                   "drop *_cleanPatTaus_*_*",
                                   "drop *_patTaus_*_*",
                                   "keep *_patPFTauProducerFixedCone_*_*"])

    # MET
    addTcMET(process, 'TC')
    addPfMET(process, 'PF')
    if out != None:
        out.outputCommands.extend(["keep *_patMETsPF_*_*", "keep *_patMETsTC_*_*"])


    # Trigger
    switchOnTrigger(process)
    HChTrigger.customise(process, dataVersion)

    # Build sequence
    seq = cms.Sequence()
    if dataVersion in ["35X", "35Xredigi"]: 
        process.hplusJptSequence = cms.Sequence(
            process.genJetParticles *
            process.ak5GenJets *
            process.recoJPTJets
        )
        seq *= process.hplusJptSequence

#    process.hplusPatSequence = cms.Sequence(
#	process.hplusTauDiscriminationSequence *
#        process.patDefaultSequence
#    )
    seq *= process.hplusPatSequence

    return seq
    
