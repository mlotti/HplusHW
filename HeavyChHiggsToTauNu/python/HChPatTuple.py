import FWCore.ParameterSet.Config as cms
import copy

from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection, switchJetCollection
from PhysicsTools.PatAlgos.tools.cmsswVersionTools import run36xOn35xInput
from PhysicsTools.PatAlgos.tools.tauTools import addTauCollection, classicTauIDSources, classicPFTauIDSources, tancTauIDSources
from PhysicsTools.PatAlgos.tools.metTools import addTcMET, addPfMET
from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
from PhysicsTools.PatAlgos.tools.coreTools import restrictInputToAOD, removeSpecificPATObjects, removeCleaning, runOnData
from PhysicsTools.PatAlgos.patEventContent_cff import patTriggerStandAloneEventContent
import RecoTauTag.RecoTau.PFRecoTauDiscriminationForChargedHiggs_cfi as HChPFTauDiscriminators
import HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationForChargedHiggsContinuous_cfi as HChPFTauDiscriminatorsCont
import RecoTauTag.RecoTau.CaloRecoTauDiscriminationForChargedHiggs_cfi as HChCaloTauDiscriminators
import HiggsAnalysis.HeavyChHiggsToTauNu.CaloRecoTauDiscriminationForChargedHiggsContinuous_cfi as HChCaloTauDiscriminatorsCont
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTaus_cfi as HChTaus
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTausCont_cfi as HChTausCont
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTausTest_cfi as HChTausTest
import HiggsAnalysis.HeavyChHiggsToTauNu.PFTauTestDiscrimination_cfi as PFTauTestDiscrimination
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTriggerMatching as HChTriggerMatching
import HiggsAnalysis.HeavyChHiggsToTauNu.HChDataSelection as HChDataSelection

# Assumes that process.out is the output module
#
#
# process      cms.Process object
# dataVersion  Version of the input data (needed for the trigger info process name) 
def addPat(process, dataVersion, doPatTrigger=True, doPatTaus=True, doPatMET=True, doPatElectronID=True,
           doPatCalo=True, doBTagging=True,
           doTauHLTMatching=True, matchingTauTrigger=None, matchingJetTrigger=None):
    out = None
    outdict = process.outputModules_()
    if outdict.has_key("out"):
        out = outdict["out"]

    outputCommands = []

    # Tau Discriminators
    process.hplusPatTauSequence = cms.Sequence()
    if doPatTaus:
	process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")
        process.load("RecoTauTag.Configuration.RecoTCTauTag_cff")
        HChPFTauDiscriminators.addPFTauDiscriminationSequenceForChargedHiggs(process)
        HChPFTauDiscriminatorsCont.addPFTauDiscriminationSequenceForChargedHiggsCont(process)
	PFTauTestDiscrimination.addPFTauTestDiscriminationSequence(process)

        HChCaloTauDiscriminators.addCaloTauDiscriminationSequenceForChargedHiggs(process)
        HChCaloTauDiscriminatorsCont.addCaloTauDiscriminationSequenceForChargedHiggsCont(process)

        # Reconfigure PFRecoTauDiscriminationByInvMass because there is no updated configuration in the CVS
        process.shrinkingConePFTauDiscriminationByInvMass.select = cms.PSet(
            min = process.shrinkingConePFTauDiscriminationByInvMass.invMassMin,
            max = process.shrinkingConePFTauDiscriminationByInvMass.invMassMax
        )

        # Disable PFRecoTauDiscriminationAgainstCaloMuon, requires RECO (there is one removal below related to this)
        process.hpsTancTauSequence.remove(process.hpsTancTausDiscriminationAgainstCaloMuon)

        # These are already in 36X AOD, se remove them from the tautagging
        # sequence
        if not dataVersion.is35X():
            process.tautagging.remove(process.jptRecoTauProducer)
            process.tautagging.remove(process.caloRecoTauProducer)
            process.tautagging.remove(process.caloRecoTauDiscriminationAgainstElectron)
            process.tautagging.remove(process.caloRecoTauDiscriminationByIsolation)
            process.tautagging.remove(process.caloRecoTauDiscriminationByLeadingTrackFinding)
            process.tautagging.remove(process.caloRecoTauDiscriminationByLeadingTrackPtCut)
        

        # Sequence to produce HPS and HPS+TaNC taus. Remove the
        # shrinking cone PFTau and the TaNC classifier from the
        # sequence as they are already produced as a part of standard
        # RECO, and we don't want to reproduce them here (i.e. we
        # prefer the objects in RECO/AOD over reproducing them on the
        # fly).
        process.PFTau.remove(process.ak5PFJetsLegacyTaNCPiZeros)
        process.PFTau.remove(process.produceAndDiscriminateShrinkingConePFTaus)
        process.PFTau.remove(process.produceShrinkingConeDiscriminationByTauNeuralClassifier)

        process.hplusPatTauSequence = cms.Sequence(
            process.tautagging *
            process.PFTauDiscriminationSequenceForChargedHiggs *
            process.PFTauDiscriminationSequenceForChargedHiggsCont *
            process.PFTauTestDiscriminationSequence *
            process.PFTau * # for HPS+TaNC
            process.CaloTauDiscriminationSequenceForChargedHiggs *
            process.CaloTauDiscriminationSequenceForChargedHiggsCont
        )
        if not doPatCalo:
            process.hplusPatTauSequence.remove(process.tautagging)
            process.hplusPatTauSequence.remove(process.CaloTauDiscriminationSequenceForChargedHiggs)
            process.hplusPatTauSequence.remove(process.CaloTauDiscriminationSequenceForChargedHiggsCont)

    # PAT Layer 0+1
    process.load("PhysicsTools.PatAlgos.patSequences_cff")

    process.hplusPatSequence = cms.Sequence(
        process.hplusPatTauSequence *
        process.patDefaultSequence
    )

    # Restrict input to AOD
    restrictInputToAOD(process, ["All"])

    # Remove MC stuff if we have collision data (has to be done any add*Collection!)
    # This also adds the L2L3Residual JEC correction to the process.patJetCorrFactors
    if dataVersion.isData():
        runOnData(process, outputInProcess = out!=None)

    # Jets
    # Set defaults
    process.patJets.jetSource = cms.InputTag("ak5CaloJets")
    process.patJets.trackAssociationSource = cms.InputTag("ak5JetTracksAssociatorAtVertex")
    process.patJets.addJetID = True
    process.patJets.embedCaloTowers = False
    process.patJets.embedPFCandidates = False
    process.patJets.addTagInfos = False

    # The default JEC to be embedded to pat::Jets are L2Relative,
    # L3Absolute, L5Flavor and L7Parton. The call to runOnData above
    # adds the L2L3Residual to the list. The default JEC to be applied
    # is L2L3Residual, or L3Absolute, or Uncorrected (in this order).

    if doPatCalo:
        # Add JPT jets
        addJetCollection(process, cms.InputTag('JetPlusTrackZSPCorJetAntiKt5'),
                         'AK5', 'JPT',
                         doJTA        = True,
                         doBTagging   = doBTagging,
                         jetCorrLabel = ('AK5JPT', process.patJetCorrFactors.levels),
                         doType1MET   = False,
                         doL1Cleaning = False,
                         doL1Counters = True,
                         genJetCollection = cms.InputTag("ak5GenJets"),
                         doJetID      = True
        )
    
        # Add PF jets
        addJetCollection(process, cms.InputTag('ak5PFJets'),
                         'AK5', 'PF',
                         doJTA        = True,
                         doBTagging   = doBTagging,
                         jetCorrLabel = ('AK5PF', process.patJetCorrFactors.levels),
                         doType1MET   = False,
                         doL1Cleaning = False,
                         doL1Counters = True,
                         genJetCollection = cms.InputTag("ak5GenJets"),
                         doJetID      = True
        )

    else:
        switchJetCollection(process, cms.InputTag('ak5PFJets'),
                            doJTA        = True,
                            doBTagging   = doBTagging,
                            jetCorrLabel = ('AK5PF', process.patJetCorrFactors.levels),
                            doType1MET   = False,
                            genJetCollection = cms.InputTag("ak5GenJets"),
                            doJetID      = True
        )
    
    outputCommands.append("keep *_selectedPatJetsAK5JPT_*_*")

    #### needed for CMSSW35x data
    if dataVersion.is35X():
        process.load("RecoJets.Configuration.GenJetParticles_cff")
        process.load("RecoJets.Configuration.RecoGenJets_cff")
        ## creating JPT jets
        process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
        process.load('RecoJets.Configuration.RecoJPTJets_cff')

        run36xOn35xInput(process)


    # Taus

    # Set default PATTauProducer options here, they should be
    # replicated to all added tau collections (and the first call to
    # addTauCollection should replace the default producer modified
    # here)
    process.patTaus.embedLeadTrack = True
    process.patTaus.embedLeadPFCand = True
    process.patTaus.embedLeadPFChargedHadrCand = True
    process.patTaus.embedLeadPFNeutralCand = True

    # There's probably a bug in pat::Tau which in practice prevents
    # the emedding of PFCands. Therefore we keep the PFCandidates
    # collection in the event so that the PFCands can be accessed via
    # edm::Refs. (note: PFCand embedding works, so it is just the
    # collection embedding which doesn't. The PFCand embedding is
    # disabled for consistenty and saving even some disk space.

    # process.patTaus.embedSignalPFCands = True
    # process.patTaus.embedSignalPFChargedHadrCands = True
    # process.patTaus.embedSignalPFNeutralHadrCands = True
    # process.patTaus.embedSignalPFGammaCands = True
    # process.patTaus.embedIsolationPFCands = True
    # process.patTaus.embedIsolationPFChargedHadrCands = True
    # process.patTaus.embedIsolationPFNeutralHadrCands = True
    # process.patTaus.embedIsolationPFGammaCands = True

    if doPatTaus:
        classicTauIDSources.extend( HChTaus.HChTauIDSources )
        classicTauIDSources.extend( HChTausCont.HChTauIDSourcesCont )
	classicPFTauIDSources.extend( HChTausTest.TestTauIDSources )

        if doPatCalo:
            addTauCollection(process,cms.InputTag('caloRecoTauProducer'),
                             algoLabel = "caloReco",
                             typeLabel = "Tau")
            process.patTausCaloRecoTau.embedLeadPFCand = False
            process.patTausCaloRecoTau.embedLeadPFChargedHadrCand = False
            process.patTausCaloRecoTau.embedLeadPFNeutralCand = False
    
        addTauCollection(process,cms.InputTag('shrinkingConePFTauProducer'),
                         algoLabel = "shrinkingCone",
                         typeLabel = "PFTau")
        # Disable isoDeposits like this until the problem with doPFIsoDeposits is fixed 
        process.patTausShrinkingConePFTau.isoDeposits = cms.PSet()

        addTauCollection(process,cms.InputTag('hpsPFTauProducer'),
                         algoLabel = "hps",
                         typeLabel = "PFTau")
        process.patTausHpsPFTau.isoDeposits = cms.PSet()

        addTauCollection(process,cms.InputTag('hpsTancTaus'),
                         algoLabel = "hpsTanc",
                         typeLabel = "PFTau")
        process.patTausHpsTancPFTau.isoDeposits = cms.PSet()
        # Disable againstCaloMuon, requires RECO (there is one removal above related to this) 
        del process.patTausHpsTancPFTau.tauIDSources.againstCaloMuon

        # Add visible taus    
        if dataVersion.isMC():
            process.VisibleTaus = cms.EDProducer("HLTTauMCProducer",
                GenParticles  = cms.untracked.InputTag("genParticles"),
                ptMinTau      = cms.untracked.double(3),
                ptMinMuon     = cms.untracked.double(3),
                ptMinElectron = cms.untracked.double(3),
                BosonID       = cms.untracked.vint32(23),
                EtaMax         = cms.untracked.double(2.5)
            )
            outputCommands.append("keep *_VisibleTaus_*_*")

    else:
        removeSpecificPATObjects(process, ["Taus"], outputInProcess= out != None)

    outputCommands.extend(["drop *_selectedPatTaus_*_*",
                           #"keep *_cleanPatTaus_*_*",
                           #"drop *_cleanPatTaus_*_*",
                           #"keep *_patTaus*_*_*",
                           #"keep *_patPFTauProducerFixedCone_*_*",
                           # keep these until the embedding problem with pat::Tau is fixed
                           #"keep recoPFCandidates_particleFlow_*_*",
                           #"keep recoTracks_generalTracks_*_*"
                           ])

    # MET
    if doPatMET:
        addTcMET(process, 'TC')
        addPfMET(process, 'PF')
        outputCommands.extend(["keep *_patMETsPF_*_*", "keep *_patMETsTC_*_*"])
    else:
        removeSpecificPATObjects(process, ["METs"], outputInProcess= out != None)


    # Muons
    # In order to calculate the transverse impact parameter w.r.t.
    # beam spot instead of primary vertex, see
    # https://twiki.cern.ch/twiki/bin/view/CMS/WorkBookPATExampleTopQuarks
    process.patMuons.usePV = False
    process.patMuons.embedTrack = True

    # Electrons
    # In order to calculate the transverse impact parameter w.r.t.
    # beam spot instead of primary vertex, see
    process.patElectrons.usePV = False
    process.patElectrons.embedTrack = True

    # Electron ID, see
    # https://twiki.cern.ch/twiki/bin/view/CMS/SimpleCutBasedEleID
    if doPatElectronID:
        process.load("ElectroWeakAnalysis.WENu.simpleEleIdSequence_cff")
        process.makePatElectronsIdAndElectrons = cms.Sequence(
            process.simpleEleIdSequence *
            process.patElectronIsolation *
            process.patElectrons
        )
        process.makePatElectrons.replace(process.patElectrons, process.makePatElectronsIdAndElectrons)

        process.patElectrons.electronIDSources.simpleEleId95relIso = cms.InputTag("simpleEleId95relIso")
        process.patElectrons.electronIDSources.simpleEleId90relIso = cms.InputTag("simpleEleId90relIso")
        process.patElectrons.electronIDSources.simpleEleId85relIso = cms.InputTag("simpleEleId85relIso")
        process.patElectrons.electronIDSources.simpleEleId80relIso = cms.InputTag("simpleEleId80relIso")
        process.patElectrons.electronIDSources.simpleEleId70relIso = cms.InputTag("simpleEleId70relIso")
        process.patElectrons.electronIDSources.simpleEleId60relIso = cms.InputTag("simpleEleId60relIso")
        process.patElectrons.electronIDSources.simpleEleId95cIso = cms.InputTag("simpleEleId95cIso")
        process.patElectrons.electronIDSources.simpleEleId90cIso = cms.InputTag("simpleEleId90cIso")
        process.patElectrons.electronIDSources.simpleEleId85cIso = cms.InputTag("simpleEleId85cIso")
        process.patElectrons.electronIDSources.simpleEleId80cIso = cms.InputTag("simpleEleId80cIso")
        process.patElectrons.electronIDSources.simpleEleId70cIso = cms.InputTag("simpleEleId70cIso")
        process.patElectrons.electronIDSources.simpleEleId60cIso = cms.InputTag("simpleEleId60cIso")


    # Select good primary vertices
    # For data this is already ran, see HChDataSelection.py
    if not dataVersion.isData():
        process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex_cfi")
        process.hplusPatSequence *= process.goodPrimaryVertices
    outputCommands.extend(["keep *_goodPrimaryVertices_*_*"])


    # Trigger
    if doPatTrigger:
        outMod= ''
        if out != None:
            outMod  = 'out'
        switchOnTrigger(process, hltProcess=dataVersion.getTriggerProcess(), outputModule=outMod)

        # Keep StandAlone trigger objects for enabling trigger
        # matching in the analysis phase with PAT tools
        outputCommands.extend(patTriggerStandAloneEventContent)


    # Remove cleaning step and set the event content
    if out == None:
        removeCleaning(process, False)
    else:
        backup = process.out.outputCommands[:]
        removeCleaning(process, True)
        backup_pat = process.out.outputCommands[:]
        process.out.outputCommands = backup
        process.out.outputCommands.extend(backup_pat)
        process.out.outputCommands.extend(outputCommands)

    # Build sequence
    seq = cms.Sequence()
    if dataVersion.is35X():
        process.hplusJptSequence = cms.Sequence(
            process.genJetParticles *
            process.ak5GenJets *
            process.recoJPTJets
        )
        seq *= process.hplusJptSequence

    seq *= process.hplusPatSequence

    # Tau+HLT matching
    if doTauHLTMatching:
        seq *= HChTriggerMatching.addTauHLTMatching(process, matchingTauTrigger, matchingJetTrigger)

    return seq


def addPatOnTheFly(process, options, dataVersion, jetTrigger=None):
    counters = []
    if dataVersion.isData():
        counters = HChDataSelection.dataSelectionCounters[:]

    if options.doPat == 0:
        return (cms.Sequence(), counters)

    print "Running PAT on the fly"

    process.collisionDataSelection = cms.Sequence()
    if dataVersion.isData():
        process.collisionDataSelection = HChDataSelection.addDataSelection(process, dataVersion, options.trigger)

    if options.trigger == "":
        raise Exception("Command line argument 'trigger' is missing")

    print "Trigger used for tau matching:", options.trigger
    if jetTrigger != None:
        print "Trigger used for jet matching:", jetTrigger

    process.patSequence = addPat(process, dataVersion, matchingTauTrigger=options.trigger, matchingJetTrigger=jetTrigger)

    dataPatSequence = cms.Sequence(
        process.collisionDataSelection *
        process.patSequence
    )
    
    return (dataPatSequence, counters)
