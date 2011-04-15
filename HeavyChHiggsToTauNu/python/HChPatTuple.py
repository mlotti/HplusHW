import FWCore.ParameterSet.Config as cms
import copy

from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection, switchJetCollection
from PhysicsTools.PatAlgos.tools.cmsswVersionTools import run36xOn35xInput
import PhysicsTools.PatAlgos.tools.tauTools as tauTools
from PhysicsTools.PatAlgos.tools.metTools import addTcMET, addPfMET
from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
from PhysicsTools.PatAlgos.tools.coreTools import restrictInputToAOD, removeSpecificPATObjects, removeCleaning, runOnData
import PhysicsTools.PatAlgos.tools.pfTools as pfTools
from PhysicsTools.PatAlgos.patEventContent_cff import patTriggerStandAloneEventContent
import HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationForChargedHiggsContinuous as HChPFTauDiscriminatorsCont
import HiggsAnalysis.HeavyChHiggsToTauNu.CaloRecoTauDiscriminationForChargedHiggsContinuous as HChCaloTauDiscriminatorsCont
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTaus_cfi as HChTaus
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTausCont_cfi as HChTausCont
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTausTest_cfi as HChTausTest
import HiggsAnalysis.HeavyChHiggsToTauNu.PFTauTestDiscrimination as PFTauTestDiscrimination
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTriggerMatching as HChTriggerMatching
import HiggsAnalysis.HeavyChHiggsToTauNu.HChDataSelection as HChDataSelection
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelectionPF_cff as MuonSelection

# Assumes that process.out is the output module
#
#
# process      cms.Process object
# dataVersion  Version of the input data (needed for the trigger info process name) 
def addPat(process, dataVersion, doPatTrigger=True, doPatTaus=True, doHChTauDiscriminators=True, doPatMET=True, doPatElectronID=True,
           doPatCalo=True, doBTagging=True, doPatMuonPFIsolation=False, doPatTauIsoDeposits=False,
           doTauHLTMatching=True, matchingTauTrigger=None, matchingJetTrigger=None,
           includeTracksPFCands=True):
    out = None
    outdict = process.outputModules_()
    if outdict.has_key("out"):
        out = outdict["out"]

    outputCommands = []

    if includeTracksPFCands:
        outputCommands.extend([
                "keep *_generalTracks_*_*",
                "keep *_particleFlow_*_*",

                # required for PF2PAT
                "keep *_electronGsfTracks_*_*",
                "keep *_gsfElectrons_*_*",
                "keep *_gsfElectronCores_*_*",
                "keep *_eid*_*_*",
                "keep recoSuperClusters_*_*_*", # I don't know which one is required
                "keep *_hfEMClusters_*_*",
#                "keep *_photons_*_*",
                "keep *_globalMuons_*_*",
                "keep *_standAloneMuons_*_*",
                "keep *_muons_*_*",
                "keep *_offlineBeamSpot_*_*",
                "keep *_genMetTrue_*_*",
                ])

    # Tau Discriminators
    process.hplusPatTauSequence = cms.Sequence()
    if doPatTaus:
        process.hplusPatTauSequence = addPFTausAndDiscriminators(process, dataVersion, doPatCalo, doHChTauDiscriminators)

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
    if includeTracksPFCands:
        process.patTaus.embedLeadTrack = False
        process.patTaus.embedLeadPFCand = False
        process.patTaus.embedLeadPFChargedHadrCand = False
        process.patTaus.embedLeadPFNeutralCand = False
    else:
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
        if doHChTauDiscriminators:
            for idSources in [tauTools.classicTauIDSources, tauTools.hpsTauIDSources, tauTools.hpsTancTauIDSources]:
                idSources.extend(HChTaus.HChTauIDSources)
                idSources.extend(HChTausCont.HChTauIDSourcesCont)
            for idSources in [tauTools.classicPFTauIDSources, tauTools.hpsTauIDSources, tauTools.hpsTancTauIDSources]:
                idSources.extend(HChTausTest.TestTauIDSources)

        if doPatCalo:
            tauTools.addTauCollection(process,cms.InputTag('caloRecoTauProducer'),
                             algoLabel = "caloReco",
                             typeLabel = "Tau")
            process.patTausCaloRecoTau.embedLeadPFCand = False
            process.patTausCaloRecoTau.embedLeadPFChargedHadrCand = False
            process.patTausCaloRecoTau.embedLeadPFNeutralCand = False
    
        tauTools.addTauCollection(process,cms.InputTag('shrinkingConePFTauProducer'),
                         algoLabel = "shrinkingCone",
                         typeLabel = "PFTau")
        # Disable isoDeposits like this until the problem with doPFIsoDeposits is fixed 
        if not doPatTauIsoDeposits:
            process.patTausShrinkingConePFTau.isoDeposits = cms.PSet()

        tauTools.addTauCollection(process,cms.InputTag('hpsPFTauProducer'),
                         algoLabel = "hps",
                         typeLabel = "PFTau")
        if not doPatTauIsoDeposits:
            process.patTausHpsPFTau.isoDeposits = cms.PSet()

        tauTools.addTauCollection(process,cms.InputTag('hpsTancTaus'),
                                  algoLabel = "hpsTanc",
                                  typeLabel = "PFTau")
        if not doPatTauIsoDeposits:
            process.patTausHpsTancPFTau.isoDeposits = cms.PSet()
        # Disable discriminators which are not in AOD
#        del process.patTausHpsTancPFTau.tauIDSources.againstCaloMuon
#        del process.patTausHpsTancPFTau.tauIDSources.byHPSvloose

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
            process.hplusPatSequence *= process.VisibleTaus
            outputCommands.append("keep *_VisibleTaus_*_*")

    else:
        # FIXME: this is broken at the moment
        #removeSpecificPATObjects(process, ["Taus"], outputInProcess= out != None)
        process.patDefaultSequence.remove(process.patTaus)
        process.patDefaultSequence.remove(process.selectedPatTaus)

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
        outputCommands.extend(["keep *_patMETsTC_*_*", "keep *_patMETsPF_*_*"])
    else:
        # FIXME: This is broken at the moment...
        #removeSpecificPATObjects(process, ["METs"], outputInProcess= out != None)
        #process.patDefaultSequen
        process.patDefaultSequence.remove(process.patMETs)
        del process.patMETs


    # Muons
    # In order to calculate the transverse impact parameter w.r.t.
    # beam spot instead of primary vertex, see
    # https://twiki.cern.ch/twiki/bin/view/CMS/WorkBookPATExampleTopQuarks
    process.patMuons.usePV = False
    if includeTracksPFCands:
        process.patMuons.embedTrack = False
    else:
        process.patMuons.embedTrack = True

    if doPatMuonPFIsolation:
        addPFMuonIsolation(process, process.patMuons, verbose=True)

    # Electrons
    # In order to calculate the transverse impact parameter w.r.t.
    # beam spot instead of primary vertex, see
    process.patElectrons.usePV = False
    if includeTracksPFCands:
        process.patElectrons.embedTrack = False
    else:
        process.patElectrons.embedTrack = True

    # Electron ID, see
    # https://twiki.cern.ch/twiki/bin/view/CMS/SimpleCutBasedEleID
    if doPatElectronID:
        process.load("ElectroWeakAnalysis.WENu.simpleEleIdSequence_cff")
        process.patDefaultSequence.replace(process.patElectrons, (
            process.simpleEleIdSequence *
            process.patElectronIsolation *
            process.patElectrons
        ))
                                           
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


def addPFTausAndDiscriminators(process, dataVersion, doCalo, doDiscriminators):
    process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")
    process.load("RecoTauTag.Configuration.RecoTCTauTag_cff")

    if doDiscriminators:
        # Do these imports here in order to be able to run PAT with
        # doPatTaus=False with 3_9_7 without extra tags
        import RecoTauTag.RecoTau.PFRecoTauDiscriminationForChargedHiggs_cfi as HChPFTauDiscriminators
        import RecoTauTag.RecoTau.CaloRecoTauDiscriminationForChargedHiggs_cfi as HChCaloTauDiscriminators

        tauAlgos = ["shrinkingConePFTau", "hpsPFTau", "hpsTancTaus"]
        HChPFTauDiscriminators.addPFTauDiscriminationSequenceForChargedHiggs(process, tauAlgos)
        HChPFTauDiscriminatorsCont.addPFTauDiscriminationSequenceForChargedHiggsCont(process, tauAlgos)
        PFTauTestDiscrimination.addPFTauTestDiscriminationSequence(process, tauAlgos)

        HChCaloTauDiscriminators.addCaloTauDiscriminationSequenceForChargedHiggs(process)
        HChCaloTauDiscriminatorsCont.addCaloTauDiscriminationSequenceForChargedHiggsCont(process)

    # These are already in 36X AOD, se remove them from the tautagging
    # sequence
    if not dataVersion.is35X():
        process.tautagging.remove(process.jptRecoTauProducer)
        process.tautagging.remove(process.caloRecoTauProducer)
        process.tautagging.remove(process.caloRecoTauDiscriminationAgainstElectron)
        process.tautagging.remove(process.caloRecoTauDiscriminationByIsolation)
        process.tautagging.remove(process.caloRecoTauDiscriminationByLeadingTrackFinding)
        process.tautagging.remove(process.caloRecoTauDiscriminationByLeadingTrackPtCut)
        

    process.hplusHpsTancTauSequence = cms.Sequence()
    sequence = cms.Sequence()

    if doCalo:
        sequence *= process.tautagging

    sequence *= process.PFTau

    if doDiscriminators:
        if doCalo:
            sequence *= (
                process.CaloTauDiscriminationSequenceForChargedHiggs *
                process.CaloTauDiscriminationSequenceForChargedHiggsCont
            )
        sequence *= (
            process.PFTauDiscriminationSequenceForChargedHiggs *
            process.PFTauDiscriminationSequenceForChargedHiggsCont *
            process.PFTauTestDiscriminationSequence
        )

    return sequence




##################################################
#
# PAT on the fly
#
from FWCore.ParameterSet.Modules import _Module
class RemoveSoftMuonVisitor:
    def __init__(self):
        self.found = []

    def enter(self, visitee):
        if isinstance(visitee, _Module) and "softMuon" in visitee.label():
            self.found.append(visitee)

    def leave(self, visitee):
        pass

    def removeFound(self, process, sequence):
        for mod in self.found:
            print "Removing '%s' from sequence '%s' and process" % (mod.label(), sequence.label())
            sequence.remove(mod)
            delattr(process, mod.label())

def addPatOnTheFly(process, options, dataVersion, jetTrigger=None, patArgs={}):
    def setPatArg(args, name, value):
        if name in args:
            print "Overriding PAT arg '%s' from '%s' to '%s'" % (name, str(args[name]), str(value))
        args[name] = value
    def setPatArgs(args, d):
        for name, value in d.iteritems():
            setPatArg(args, name, value)

    counters = []
    if dataVersion.isData() and options.tauEmbeddingInput == 0:
        counters = HChDataSelection.dataSelectionCounters[:]
    if options.tauEmbeddingInput != 0:
        counters = MuonSelection.muonSelectionCounters[:]

    if options.doPat == 0:
        return (cms.Sequence(), counters)

    print "Running PAT on the fly"

    process.collisionDataSelection = cms.Sequence()
    if options.tauEmbeddingInput != 0:

        # Hack to not to crash if something in PAT assumes process.out
        hasOut = hasattr(process, "out")
        if not hasOut:
            process.out = cms.OutputModule("PoolOutputModule",
                fileName = cms.untracked.string('dummy.root'),
                outputCommands = cms.untracked.vstring()
            )
        setPatArgs(patArgs, {"doPatTrigger": False,
                             "doTauHLTMatching": False,
                             "doPatCalo": False,
                             "doBTagging": True,
                             "doPatElectronID": False,
                             "doPatMET": False})

        process.patSequence = addPat(process, dataVersion, **patArgs)
        # FIXME: this is broken at the moment
        #removeSpecificPATObjects(process, ["Muons", "Electrons", "Photons"], False)
        process.patDefaultSequence.remove(process.patMuons)
        process.patDefaultSequence.remove(process.selectedPatMuons)
        process.patDefaultSequence.remove(process.patElectrons)
        process.patDefaultSequence.remove(process.selectedPatElectrons)
        process.patDefaultSequence.remove(process.patPhotons)
        process.patDefaultSequence.remove(process.selectedPatPhotons)

        # Remove soft muon b tagging discriminators as they are not
        # well defined, cause technical problems and we don't use
        # them.
        process.patJets.discriminatorSources = filter(lambda tag: "softMuon" not in tag.getModuleLabel(), process.patJets.discriminatorSources)
        for seq in [process.btagging, process.btaggingJetTagsAOD, process.btaggingTagInfosAOD]:
            softMuonRemover = RemoveSoftMuonVisitor()
            seq.visit(softMuonRemover)
            softMuonRemover.removeFound(process, seq)

        # Use the merged track collection
        process.ak5PFJetTracksAssociatorAtVertex.tracks.setModuleLabel("tmfTracks")
        process.jetTracksAssociatorAtVertex.tracks.setModuleLabel("tmfTracks")

        # Another part of the PAT process.out hack
        if not hasOut:
            del process.out
    else:
        if dataVersion.isData():
            process.collisionDataSelection = HChDataSelection.addDataSelection(process, dataVersion, options.trigger)

        pargs = patArgs.copy()

        if not ("doTauHLTMatching" in patArgs and patArgs["doTauHLTMatching"] == False):
            if options.trigger == "":
                raise Exception("Command line argument 'trigger' is missing")

            print "Trigger used for tau matching:", options.trigger
            pargs["matchingTauTrigger"] = options.trigger
            if jetTrigger != None:
                print "Trigger used for jet matching:", jetTrigger
                pargs["matchingJetTrigger"] = jetTrigger            

        process.patSequence = addPat(process, dataVersion, **pargs)

    dataPatSequence = cms.Sequence(
        process.collisionDataSelection *
        process.patSequence
    )

    if options.tauEmbeddingInput != 0:
        from HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations import addTauEmbeddingMuonTaus
        process.patMuonTauSequence = addTauEmbeddingMuonTaus(process)
        process.patSequence *= process.patMuonTauSequence
    
    return (dataPatSequence, counters)


##################################################
#
# PF2PAT
#
def addPF2PAT(process, dataVersion):
    if hasattr(process, "patDefaultSequence"):
        raise Exception("PAT should not exist before calling addPF2PAT at the moment")

    # Hack to not to crash if something in PAT assumes process.out
    hasOut = hasattr(process, "out")
    if not hasOut:
        process.out = cms.OutputModule("PoolOutputModule",
            fileName = cms.untracked.string('dummy.root'),
            outputCommands = cms.untracked.vstring()
        )

    process.load("PhysicsTools.PatAlgos.patSequences_cff")
    pfTools.usePF2PAT(process, runPF2PAT=True, jetAlgo="AK5", runOnMC=dataVersion.isMC(), postfix="PFlow")

    # Remove photon MC matcher in order to avoid keeping photons in the event content
    process.patDefaultSequencePFlow.remove(process.photonMatchPFlow)

    if not hasOut:
        del process.out

    return process.patPF2PATSequencePFlow

### The functions below are taken from
### UserCode/PFAnalyses/VBFHTauTau/python/vbfDiTauPATTools.py
### revision 1.7

###################a#################################################
from PhysicsTools.PFCandProducer.Isolation.tools_cfi import isoDepositReplace

def addSelectedPFlowParticle(process,verbose=False):
    if verbose:
        print "[Info] Adding pf-particles (for pf-isolation and pf-seed pat-leptons)"
    process.load("PhysicsTools.PFCandProducer.ParticleSelectors.pfSortByType_cff")
    process.load("PhysicsTools.PFCandProducer.pfNoPileUp_cff")
    process.pfCandidateSelectionByType = cms.Sequence(
        process.pfNoPileUpSequence *
        ( process.pfAllNeutralHadrons +
          process.pfAllChargedHadrons +
          process.pfAllPhotons
          )  +
        process.pfAllMuons +
        process.pfAllElectrons
        )
    process.pfPileUp.Enable = True # enable pile-up filtering
    process.pfPileUp.Vertices = "offlinePrimaryVertices" # use vertices w/o BS
    process.pfAllMuons.src = "particleFlow"
    process.pfAllElectrons.src = "particleFlow"
    
    process.hplusPatSequence.replace(process.hplusPatTauSequence,
                                     process.pfCandidateSelectionByType+
                                     process.hplusPatTauSequence)

def addPFMuonIsolation(process,module,postfix="",verbose=False):
    if verbose:
        print "[Info] Adding particle isolation to muon with postfix '"+postfix+"'"

    if not hasattr(process, "pfCandidateSelectionByType"):
        addSelectedPFlowParticle(process,verbose=verbose)
        
    #setup correct src of isolated object
    setattr(process,"isoDepMuonWithCharged"+postfix,
            isoDepositReplace(module.muonSource,
                              'pfAllChargedHadrons'))
    setattr(process,"isoDepMuonWithNeutral"+postfix,
            isoDepositReplace(module.muonSource,
                              'pfAllNeutralHadrons'))
    setattr(process,"isoDepMuonWithPhotons"+postfix,
            isoDepositReplace(module.muonSource,
                              'pfAllPhotons'))

    #compute isolation values form deposits
    process.load("PhysicsTools.PFCandProducer.Isolation.pfMuonIsolationFromDeposits_cff")
    if postfix!="":
        setattr(process,"isoValMuonWithCharged"+postfix,
                process.isoValMuonWithCharged.clone())
        getattr(process,"isoValMuonWithCharged"+postfix).deposits.src="isoDepMuonWithCharged"+postfix
        setattr(process,"isoValMuonWithNeutral"+postfix,
                process.isoValMuonWithNeutral.clone())
        getattr(process,"isoValMuonWithNeutral"+postfix).deposits.src="isoDepMuonWithNeutral"+postfix
        setattr(process,"isoValMuonWithPhotons"+postfix,
                process.isoValMuonWithPhotons.clone())
        getattr(process,"isoValMuonWithPhotons"+postfix).deposits.src="isoDepMuonWithPhotons"+postfix

    # Count and max pts
    for name in ["Charged", "Neutral", "Photons"]:
        prototype = getattr(process, "isoValMuonWith"+name+postfix)

        m = prototype.clone()
        m.deposits[0].mode = "count"
        setattr(process, "isoValCountMuonWith"+name+postfix, m)

        m = prototype.clone()
        m.deposits[0].mode = "max"
        m.deposits[0].vetos = []
        setattr(process, "isoValMaxMuonWith"+name+postfix, m)

    # Use the 0.5 min value for pt with charged cands in order to be similar with HpsTight
    for name in ["isoValCountMuonWithCharged", "isoValMaxMuonWithCharged"]:
        m = getattr(process, name+postfix).clone()
        m.deposits[0].vetos = ["Threshold(0.5)"]
        setattr(process, name+"Tight"+postfix, m)
    

    setattr(process,"patMuonIsolationFromDepositsSequence"+postfix,
            cms.Sequence(getattr(process,"isoValMuonWithCharged"+postfix) +
                         getattr(process,"isoValMuonWithNeutral"+postfix) +
                         getattr(process,"isoValMuonWithPhotons"+postfix) +
                         getattr(process,"isoValCountMuonWithCharged"+postfix) +
                         getattr(process,"isoValCountMuonWithNeutral"+postfix) +
                         getattr(process,"isoValCountMuonWithPhotons"+postfix) +                         
                         getattr(process,"isoValMaxMuonWithCharged"+postfix) +
                         getattr(process,"isoValMaxMuonWithNeutral"+postfix) +
                         getattr(process,"isoValMaxMuonWithPhotons"+postfix) +                  
                         getattr(process,"isoValCountMuonWithChargedTight"+postfix) +
                         getattr(process,"isoValMaxMuonWithChargedTight"+postfix) 
            )
    )

    setattr(process,"patMuonIsoDepositsSequence"+postfix,
            cms.Sequence(getattr(process,"isoDepMuonWithCharged"+postfix) +
                         getattr(process,"isoDepMuonWithNeutral"+postfix) +
                         getattr(process,"isoDepMuonWithPhotons"+postfix)
            )
    )
    setattr(process,"patMuonIsolationSequence"+postfix,
            cms.Sequence(getattr(process,"patMuonIsoDepositsSequence"+postfix) +
                         getattr(process,"patMuonIsolationFromDepositsSequence"+postfix)
            )
    )

    # The possible values for the keys are predefined...
    module.isoDeposits = cms.PSet(
        pfChargedHadrons = cms.InputTag("isoDepMuonWithCharged"+postfix),
        pfNeutralHadrons = cms.InputTag("isoDepMuonWithNeutral"+postfix),
        pfPhotons = cms.InputTag("isoDepMuonWithPhotons"+postfix)
    )
    module.isolationValues = cms.PSet(
        pfChargedHadrons = cms.InputTag("isoValMuonWithCharged"+postfix),
        pfNeutralHadrons = cms.InputTag("isoValMuonWithNeutral"+postfix),
        pfPhotons = cms.InputTag("isoValMuonWithPhotons"+postfix),
        # Only 5 slots available *sigh*
        user = cms.VInputTag(
                cms.InputTag("isoValCountMuonWithChargedTight"+postfix),
                cms.InputTag("isoValMaxMuonWithChargedTight"+postfix),
                cms.InputTag("isoValMaxMuonWithNeutral"+postfix),
                cms.InputTag("isoValCountMuonWithPhotons"+postfix),
                cms.InputTag("isoValMaxMuonWithPhotons"+postfix),
        )
#        pfChargedHadronsCount = cms.InputTag("isoValCountMuonWithCharged"+postfix),
#        pfNeutralHadronsCount = cms.InputTag("isoValCountMuonWithNeutral"+postfix),
#        pfPhotonsCount = cms.InputTag("isoValCountMuonWithPhotons"+postfix),
#        pfChargedHadronsMax = cms.InputTag("isoValMaxMuonWithCharged"+postfix),
#        pfNeutralHadronsMax = cms.InputTag("isoValMaxMuonWithNeutral"+postfix),
#        pfPhotonsMax = cms.InputTag("isoValMaxMuonWithPhotons"+postfix),
#        pfChargedHadronsTightCount = cms.InputTag("isoValCountMuonWithChargedTight"+postfix),
#        pfChargedHadronsTightMax = cms.InputTag("isoValMaxMuonWithChargedTight"+postfix),
    )

    process.patDefaultSequence.replace(module,
                                       getattr(process,"patMuonIsolationSequence"+postfix)+
                                       module
                                       )
