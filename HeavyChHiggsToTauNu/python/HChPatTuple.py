import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoCleaning
from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection
from PhysicsTools.PatAlgos.tools.cmsswVersionTools import run36xOn35xInput
from PhysicsTools.PatAlgos.tools.tauTools import switchToPFTauFixedCone
from PhysicsTools.PatAlgos.tools.metTools import addTcMET, addPfMET
from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTrigger_cfi as HChTrigger

# Assumes that process.out is the output module
#
#
# process      cms.Process object
# dataVersion  Version of the input data (needed for the trigger info process name) 
def addPat(process, dataVersion):
    seq = cms.Sequence()

    out = None
    outdict = process.outputModules_()
    if outdict.has_key("out"):
        out = outdict["out"]

    # PAT Layer 0+1
    process.load("PhysicsTools.PatAlgos.patSequences_cff")

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
    if dataVersion == "35X": 
        process.load("RecoJets.Configuration.GenJetParticles_cff")
        process.load("RecoJets.Configuration.RecoGenJets_cff")
        ## creating JPT jets
        process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
        process.load('RecoJets.Configuration.RecoJPTJets_cff')

        run36xOn35xInput(process)


    # Taus
    #process.patTaus.tauSource = cms.InputTag("fixedConePFTauProducer")
    switchToPFTauFixedCone(process)
    #process.patPFTauProducerFixedCone = copy.deepcopy(process.patTaus)

    process.patTaus.embedLeadTrack = True
    process.patTaus.embedSignalTracks = True
    process.patTaus.embedIsolationTracks = True


    # Preselections of objects
    process.selectedPatJets.cut='pt > 10 & abs(eta) < 2.4 & associatedTracks().size() > 0'
    process.selectedPatMuons.cut='pt > 10 & abs(eta) < 2.4 & isGlobalMuon() & !track().isNull()'
    process.selectedPatElectrons.cut='pt > 10 & abs(eta) < 2.4 & !gsfTrack().isNull()'
    process.selectedPatTaus.cut=('pt > 10 & abs(eta) < 2.4'+
                                 '& tauID("leadingTrackFinding") > 0.5 & tauID("leadingPionPtCut") > 0.5'+
                                 '& tauID("byIsolationUsingLeadingPion") > 0.5'+
                                 '& tauID("againstMuon") > 0.5 & tauID("againstElectron") > 0.5')
    if out != None:
        out.outputCommands.extend(patEventContentNoCleaning)

    # MET
    addTcMET(process, 'TC')
    addPfMET(process, 'PF')
    if out != None:
        out.outputCommands.extend(["keep *_patMETsPF_*_*", "keep *_patMETsTC_*_*"])


    # Trigger
    switchOnTrigger(process)
    HChTrigger.customise(process, dataVersion)

    # Discriminators
    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.ChargedHiggsTauIDDiscrimination_cfi")


    # Build sequence
    seq = cms.Sequence()
    if dataVersion == "35X":
        process.hplusJptSequence = cms.Sequence(
            process.genJetParticles *
            process.ak5GenJets *
            process.recoJPTJets
        )
        seq *= process.hplusJptSequence
    process.hplusPatSequence = cms.Sequence(
	process.hplusTauDiscriminationSequence *
        process.patDefaultSequence
    )
    seq *= process.hplusPatSequence

    return seq
    
