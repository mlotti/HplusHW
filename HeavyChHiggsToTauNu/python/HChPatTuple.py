import FWCore.ParameterSet.Config as cms
import copy

from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection, switchJetCollection
from PhysicsTools.PatAlgos.tools.cmsswVersionTools import run36xOn35xInput
import PhysicsTools.PatAlgos.tools.tauTools as tauTools
from PhysicsTools.PatAlgos.tools.metTools import addTcMET, addPfMET
from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
from PhysicsTools.PatAlgos.tools.coreTools import restrictInputToAOD, removeSpecificPATObjects, removeCleaning, runOnData
import PhysicsTools.PatAlgos.tools.helpers as patHelpers
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
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.RemoveSoftMuonVisitor as RemoveSoftMuonVisitor


##################################################
#
# PAT on the fly
#
def addPatOnTheFly(process, options, dataVersion, jetTrigger=None,
                   doPlainPat=True, doPF2PAT=False, doPF2PATNoPu=False,
                   plainPatArgs={}, pf2patArgs={}, pf2patNoPuArgs={}):
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

        import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.PFEmbeddingSource_cff as PFEmbeddingSource
        counters.extend(PFEmbeddingSource.muonSelectionCounters)

    if options.doPat == 0:
        process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex_cfi")
        seq = cms.Sequence(
#            process.goodPrimaryVertices10
        )
        return (seq, counters)

    print "Running PAT on the fly"

    process.collisionDataSelection = cms.Sequence()
    if options.tauEmbeddingInput != 0:
        if doPF2PAT or doPF2PATNoPU or not doPlainPat:
            raise Exception("Only plainPat can be done for tau embedding input at the moment")

        # Hack to not to crash if something in PAT assumes process.out
        hasOut = hasattr(process, "out")
        if not hasOut:
            process.out = cms.OutputModule("PoolOutputModule",
                fileName = cms.untracked.string('dummy.root'),
                outputCommands = cms.untracked.vstring()
            )
        setPatArgs(plainPatArgs, {"doPatTrigger": False,
                             "doTauHLTMatching": False,
                             "doPatCalo": False,
                             "doBTagging": True,
                             "doPatElectronID": False,
                             "doPatMET": False})

        process.patSequence = addPat(process, dataVersion, plainPatArgs=plainPatArgs)
        # FIXME: this is broken at the moment
        #removeSpecificPATObjects(process, ["Muons", "Electrons", "Photons"], False)
        process.patDefaultSequence.remove(process.patMuons)
        process.patDefaultSequence.remove(process.selectedPatMuons)
        process.patDefaultSequence.remove(process.muonMatch)
        process.patDefaultSequence.remove(process.patElectrons)
        process.patDefaultSequence.remove(process.selectedPatElectrons)
        process.patDefaultSequence.remove(process.electronMatch)
        process.patDefaultSequence.remove(process.patPhotons)
        process.patDefaultSequence.remove(process.selectedPatPhotons)
        process.patDefaultSequence.remove(process.photonMatch)

        # Remove soft muon b tagging discriminators as they are not
        # well defined, cause technical problems and we don't use
        # them.
        process.patJets.discriminatorSources = filter(lambda tag: "softMuon" not in tag.getModuleLabel(), process.patJets.discriminatorSources)
        for seq in [process.btagging, process.btaggingJetTagsAOD, process.btaggingTagInfosAOD]:
            softMuonRemover = RemoveSoftMuonVisitor.RemoveSoftMuonVisitor()
            seq.visit(softMuonRemover)
            softMuonRemover.removeFound(process, seq)

        # Use the merged track collection
        process.ak5PFJetTracksAssociatorAtVertex.tracks.setModuleLabel("tmfTracks")
        process.jetTracksAssociatorAtVertex.tracks.setModuleLabel("tmfTracks")

        # Another part of the PAT process.out hack
        if not hasOut:
            del process.out

        # Add PV selection, if not yet done by PAT
#        if dataVersion.isData():
#            process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex_cfi")
#            process.patSequence *= process.goodPrimaryVertices
    else:
        if dataVersion.isData():
            process.collisionDataSelection = HChDataSelection.addDataSelection(process, dataVersion, options.trigger)

        pargs = plainPatArgs.copy()
        pargs2 = pf2patArgs.copy()
        pargs2NoPu = pf2patNoPuArgs.copy()

        for args in [pargs, pargs2, pargs2NoPu]:
            if args.get("doTauHLTMatching", True):
                if options.trigger == "":
                    raise Exception("Command line argument 'trigger' is missing")
    
                print "Trigger used for tau matching:", options.trigger
                args["matchingTauTrigger"] = options.trigger
                if jetTrigger != None:
                    print "Trigger used for jet matching:", jetTrigger
                    args["matchingJetTrigger"] = jetTrigger

        process.patSequence = addPat(process, dataVersion,
                                     doPlainPat=doPlainPat, doPF2PAT=doPF2PAT, doPF2PATNoPu=doPF2PATNoPu,
                                     plainPatArgs=pargs, pf2patArgs=pargs2, pf2patNoPuArgs=pargs2NoPu)
    
    # Add selection of PVs with sumPt > 10
#    process.patSequence *= process.goodPrimaryVertices10

    dataPatSequence = cms.Sequence(
        process.collisionDataSelection *
        process.patSequence
    )

    if options.tauEmbeddingInput != 0:
        from HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations import addTauEmbeddingMuonTaus
        process.patMuonTauSequence = addTauEmbeddingMuonTaus(process)
        process.patSequence *= process.patMuonTauSequence
    
    return (dataPatSequence, counters)


# Add the PAT sequences as requested
def addPat(process, dataVersion,
           doPlainPat=True, doPF2PAT=False, doPF2PATNoPu=False,
           plainPatArgs={}, pf2patArgs={}, pf2patNoPuArgs={}):
    process.pf2patSequence = cms.Sequence()
    process.pf2patNoPuSequence = cms.Sequence()
    process.plainPatSequence = cms.Sequence()

    if doPF2PAT:
        process.pf2patSequence = addPF2PAT(process, dataVersion, postfix="PFlow", doPFnoPU=False, **pf2patArgs)
    if doPF2PATNoPu:
        process.pf2patNoPuSequence = addPF2PAT(process, dataVersion, **pf2patNoPuArgs)
    if doPlainPat:
        process.plainPatSequence = addPlainPat(process, dataVersion, **plainPatArgs)

    # PAT function must be added last (PF2PAT requires unmodified
    # patDefaultSequence), but run first (we use some stuff produced
    # with plain PAT in PF2PAT)
    sequence = cms.Sequence(
        process.plainPatSequence *
        process.pf2patSequence *
        process.pf2patNoPuSequence
    )
    return sequence

# Assumes that process.out is the output module
#
#
# process      cms.Process object
# dataVersion  Version of the input data (needed for the trigger info process name) 
def addPlainPat(process, dataVersion, doPatTrigger=True, doPatTaus=True, doHChTauDiscriminators=True, doPatMET=True, doPatElectronID=True,
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
    setPatJetDefaults(process.patJets)
    setPatJetCorrDefaults(process.patJetCorrFactors, dataVersion)

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


    # Taus

    # Set default PATTauProducer options here, they should be
    # replicated to all added tau collections (and the first call to
    # addTauCollection should replace the default producer modified
    # here)
    setPatTauDefaults(process.patTaus, includeTracksPFCands)

    if doPatTaus:
        if doHChTauDiscriminators:
            addHChTauDiscriminators()

        if doPatCalo:
            tauTools.addTauCollection(process,cms.InputTag('caloRecoTauProducer'),
                             algoLabel = "caloReco",
                             typeLabel = "Tau")
            setPatTauDefaults(process.patTausCaloRecoTau, True)
            process.patTausCaloRecoTau.embedLeadTrack = not includeTracksPFCands
    
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
        process.patDefaultSequence.remove(process.patMETCorrections)
        process.patDefaultSequence.remove(process.patMETs)
        del process.patMETCorrections
        del process.patMETs

    # Muons
    setPatLeptonDefaults(process.patMuons, includeTracksPFCands)
    if doPatMuonPFIsolation:
        addPFMuonIsolation(process, process.patMuons, verbose=True)

    # Electrons
    # In order to calculate the transverse impact parameter w.r.t.
    # beam spot instead of primary vertex, see
    setPatLeptonDefaults(process.patMuons, includeTracksPFCands)

    # Electron ID, see
    # https://twiki.cern.ch/twiki/bin/view/CMS/SimpleCutBasedEleID
    if doPatElectronID:
        addPatElectronID(process, process.patElectrons, process.patDefaultSequence)

    # Select good primary vertices
    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex_cfi")
    process.offlinePrimaryVerticesSumPt = cms.EDProducer("HPlusVertexViewSumPtComputer",
        src = cms.InputTag("offlinePrimaryVertices")
    )
    process.hplusPatSequence *= (
        process.goodPrimaryVertices *
        process.goodPrimaryVertices10 *
        process.offlinePrimaryVerticesSumPt
    )
    outputCommands.extend([
        "keep *_goodPrimaryVertices*_*_*",
        "keep *_offlinePrimaryVerticesSumPt_*_*",
        ])

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

        # Remove PFParticles here, they are explicitly included when needed
        backup_pat = filter(lambda n: "selectedPatPFParticles" not in n, backup_pat)

        process.out.outputCommands = backup
        process.out.outputCommands.extend(backup_pat)
        process.out.outputCommands.extend(outputCommands)

    # Build sequence
    seq = cms.Sequence(
        process.hplusPatSequence
    )

    # Tau+HLT matching
    if doTauHLTMatching:
        seq *= HChTriggerMatching.addTauHLTMatching(process, matchingTauTrigger, matchingJetTrigger)

    return seq

# Helper functions
def addPFTausAndDiscriminators(process, dataVersion, doCalo, doDiscriminators):
    process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")
    process.load("RecoTauTag.Configuration.RecoTCTauTag_cff")

    if doDiscriminators:
        # Do these imports here in order to be able to run PAT with
        # doPatTaus=False with 3_9_7 without extra tags
        import RecoTauTag.RecoTau.PFRecoTauDiscriminationForChargedHiggs_cfi as HChPFTauDiscriminators
        import RecoTauTag.RecoTau.CaloRecoTauDiscriminationForChargedHiggs_cfi as HChCaloTauDiscriminators

        tauAlgos = ["shrinkingConePFTau", "hpsPFTau", "hpsTancTaus"]
        # to synchronize with addPF2PAT
        #if not hasattr(process, "hpsPFTauDiscriminationForChargedHiggsByLeadingTrackPtCut"):
        #    tauAlgos.append("hpsPFTau")

        HChPFTauDiscriminators.addPFTauDiscriminationSequenceForChargedHiggs(process, tauAlgos)
        HChPFTauDiscriminatorsCont.addPFTauDiscriminationSequenceForChargedHiggsCont(process, tauAlgos)
        PFTauTestDiscrimination.addPFTauTestDiscriminationSequence(process, tauAlgos)

        HChCaloTauDiscriminators.addCaloTauDiscriminationSequenceForChargedHiggs(process)
        HChCaloTauDiscriminatorsCont.addCaloTauDiscriminationSequenceForChargedHiggsCont(process)


    # These are already in 36X AOD, se remove them from the tautagging
    # sequence
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

def setPatJetDefaults(module):
    module.addJetID = True
    module.embedCaloTowers = False
    module.embedPFCandidates = False
    module.addTagInfos = False

def setPatJetCorrDefaults(module, dataVersion, L1FastJet=False):
    module.levels = []
    if L1FastJet:
        module.levels.append("L1FastJet")
    else:
        module.levels.append("L1Offset")
    module.levels.extend(["L2Relative", "L3Absolute"])
#    if dataVersion.isData():
#        module.levels.append("L2L3Residual")
    module.levels.extend(["L5Flavor", "L7Parton"])

def setPatTauDefaults(module, includeTracksPFCands):
    attrs = [
        "embedLeadTrack",
        "embedLeadPFCand",
        "embedLeadPFChargedHadrCand",
        "embedLeadPFNeutralCand",
#        "embedSignalPFCands",
#        "embedSignalPFChargedHadrCands",
#        "embedSignalPFNeutralHadrCands",
#        "embedSignalPFGammaCands",
#        "embedIsolationPFCands",
#        "embedIsolationPFChargedHadrCands",
#        "embedIsolationPFNeutralHadrCands",
#        "embedIsolationPFGammaCands",
        ]

    value = not includeTracksPFCands
    for a in attrs:
        setattr(module, a, value)
    

def addHChTauDiscriminators():
    if HChTaus.HChTauIDSources[0] in tauTools.classicTauIDSources:
        print "addHChTauDiscriminators called already once, not adding them again"
        return

    for idSources in [tauTools.classicTauIDSources, tauTools.hpsTauIDSources, tauTools.hpsTancTauIDSources]:
        idSources.extend(HChTaus.HChTauIDSources)
        idSources.extend(HChTausCont.HChTauIDSourcesCont)
    for idSources in [tauTools.classicPFTauIDSources, tauTools.hpsTauIDSources, tauTools.hpsTancTauIDSources]:
        idSources.extend(HChTausTest.TestTauIDSources)

def setPatLeptonDefaults(module, includeTracksPFCands):
    # In order to calculate the transverse impact parameter w.r.t.
    # beam spot instead of primary vertex, see
    # https://twiki.cern.ch/twiki/bin/view/CMS/WorkBookPATExampleTopQuarks
    module.usePV = False
    module.embedTrack = not includeTracksPFCands

def addPatElectronID(process, module, sequence):
    process.load("ElectroWeakAnalysis.WENu.simpleEleIdSequence_cff")
    sequence.replace(module, (
            process.simpleEleIdSequence *
#            process.patElectronIsolation *
            module
    ))
                                           
    module.electronIDSources.simpleEleId95relIso = cms.InputTag("simpleEleId95relIso")
    module.electronIDSources.simpleEleId90relIso = cms.InputTag("simpleEleId90relIso")
    module.electronIDSources.simpleEleId85relIso = cms.InputTag("simpleEleId85relIso")
    module.electronIDSources.simpleEleId80relIso = cms.InputTag("simpleEleId80relIso")
    module.electronIDSources.simpleEleId70relIso = cms.InputTag("simpleEleId70relIso")
    module.electronIDSources.simpleEleId60relIso = cms.InputTag("simpleEleId60relIso")
    module.electronIDSources.simpleEleId95cIso = cms.InputTag("simpleEleId95cIso")
    module.electronIDSources.simpleEleId90cIso = cms.InputTag("simpleEleId90cIso")
    module.electronIDSources.simpleEleId85cIso = cms.InputTag("simpleEleId85cIso")
    module.electronIDSources.simpleEleId80cIso = cms.InputTag("simpleEleId80cIso")
    module.electronIDSources.simpleEleId70cIso = cms.InputTag("simpleEleId70cIso")
    module.electronIDSources.simpleEleId60cIso = cms.InputTag("simpleEleId60cIso")



##################################################
#
# PF2PAT
#
def addPF2PAT(process, dataVersion, postfix="PFlowNoPU",
              doTauHLTMatching=True, matchingTauTrigger=None, 
              doPFnoPU=True,
              ):
#    if hasattr(process, "patDefaultSequence"):
#        raise Exception("PAT should not exist before calling addPF2PAT at the moment")

    # Hack to not to crash if something in PAT assumes process.out
    hasOut = hasattr(process, "out")
    outputCommands = []
    outputCommandsBackup = []
    if hasOut:
        outputCommandsBackup = process.out.outputCommands[:]
    else:
        process.out = cms.OutputModule("PoolOutputModule",
            fileName = cms.untracked.string('dummy.root'),
            outputCommands = cms.untracked.vstring()
        )

    outputCommands = []

    process.load("PhysicsTools.PatAlgos.patSequences_cff")
    pfTools.usePF2PAT(process, runPF2PAT=True, jetAlgo="AK5", runOnMC=dataVersion.isMC(), postfix=postfix)

    outputCommands = [
#        "keep *_selectedPatPhotons%s_*_*" % postfix,
#        'keep *_selectedPatElectrons%s_*_*' % postfix, 
        'keep *_selectedPatMuons%s_*_*' % postfix,
        'keep *_selectedPatTaus%s_*_*' % postfix,
        'keep *_selectedPatJet%s*_*_*' % postfix,
        'drop *_selectedPatJets%s_pfCandidates_*' % postfix,
        'drop *_*PF_caloTowers_*',
        'drop *_*JPT_pfCandidates_*',
        'drop *_*Calo_pfCandidates_*',
        'keep *_patMETs%s_*_*' % postfix,
        ]
    if doPFnoPU:
        outputCommands.extend([
                'keep *_selectedPatPFParticles%s_*_*' % postfix,
                ])
    else:
        outputCommands.extend([
                'drop *_selectedPatPFParticles%s_*_*' % postfix,
                ])

    pfKt6Sequence = cms.Sequence()
    setattr(process, "pfKt6Sequence"+postfix, pfKt6Sequence)

    # Enable/disable PFnoPU
    getattr(process, "pfPileUp"+postfix).Enable = doPFnoPU

    # Jet modifications
    # L1FastJet
    # https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#OffsetJEC
    # https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#JetEnCor2011
    # https://hypernews.cern.ch/HyperNews/CMS/get/jes/184.html
    doL1Fastjet = True
    if doL1Fastjet:
        kt6name = "kt6PFJets"+postfix

        if doPFnoPU:
            from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
            m = cms.EDFilter("PrimaryVertexObjectFilter",
                filterParams = pvSelector.clone(maxZ = 24.0),
                src = cms.InputTag("offlinePrimaryVertices")
            )
            setattr(process, "goodOfflinePrimaryVerticesForJets"+postfix, m)
            pfKt6Sequence *= m
    
            from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
            setattr(process, kt6name, kt4PFJets.clone(
                rParam = cms.double(0.6),
                src = cms.InputTag('pfNoElectron'+postfix),
                doAreaFastjet = cms.bool(True),
                doRhoFastjet = cms.bool(True),
                voronoiRfact = cms.double(0.9)
            ))
        else:
            process.load('RecoJets.Configuration.RecoPFJets_cff')
            setattr(process, kt6name, process.kt6PFJets.clone(
                    doRhoFastjet = True,
                    Rgo_EtaMax = cms.double(4.5)
            ))
        pfKt6Sequence *= getattr(process, kt6name)
        getattr(process, "patJetCorrFactors"+postfix).rho.setModuleLabel(kt6name)

        # ak5PFJets
        getattr(process, "pfJets"+postfix).doAreaFastjet = True
        getattr(process, "pfJets"+postfix).Rho_EtaMax = cms.double(4.5)

        if doPFnoPU:
            getattr(process, "pfJets"+postfix).Vertices = cms.InputTag("goodOfflinePrimaryVerticesForJets"+postfix)
            getattr(process, "pfJets"+postfix).doRhoFastjet = False

        setPatJetCorrDefaults(getattr(process, "patJetCorrFactors"+postfix), dataVersion, L1FastJet=True)
        # With PFnoPU we need separache "charged hadron subtracted" corrections
        if doPFnoPU:
            getattr(process, "patJetCorrFactors"+postfix).payload = "AK5PFchs"

    setPatJetDefaults(getattr(process, "patJets"+postfix))


    # Use HPS taus
    addHChTauDiscriminators()
    if not hasattr(process, "hpsPFTauDiscriminationForChargedHiggsByLeadingTrackPtCut"):
        import RecoTauTag.RecoTau.PFRecoTauDiscriminationForChargedHiggs_cfi as HChPFTauDiscriminators
        import RecoTauTag.RecoTau.CaloRecoTauDiscriminationForChargedHiggs_cfi as HChCaloTauDiscriminators

        tauAlgos = ["hpsPFTau"]
        HChPFTauDiscriminators.addPFTauDiscriminationSequenceForChargedHiggs(process, tauAlgos)
        HChPFTauDiscriminatorsCont.addPFTauDiscriminationSequenceForChargedHiggsCont(process, tauAlgos)
        PFTauTestDiscrimination.addPFTauTestDiscriminationSequence(process, tauAlgos)
    
    patHelpers.cloneProcessingSnippet(process, process.hpsPFTauHplusDiscriminationSequence, postfix)
    patHelpers.cloneProcessingSnippet(process, process.hpsPFTauHplusDiscriminationSequenceCont, postfix)
    patHelpers.cloneProcessingSnippet(process, process.hpsPFTauHplusTestDiscriminationSequence, postfix)

    patTauSeq = cms.Sequence(
        getattr(process, "hpsPFTauHplusDiscriminationSequence"+postfix) *
        getattr(process, "hpsPFTauHplusDiscriminationSequenceCont"+postfix) * 
        getattr(process, "hpsPFTauHplusTestDiscriminationSequence"+postfix)
    )
    setattr(process, "hplusPatTauSequence"+postfix, patTauSeq)
    patHelpers.massSearchReplaceParam(patTauSeq, "PFTauProducer", cms.InputTag("hpsPFTauProducer"), cms.InputTag("hpsPFTauProducer"+postfix))
    patHelpers.massSearchReplaceAnyInputTag(patTauSeq, cms.InputTag("hpsPFTauDiscriminationByDecayModeFinding"), cms.InputTag("hpsPFTauDiscriminationByDecayModeFinding"+postfix))

    pfTools.adaptPFTaus(process, "hpsPFTau", postfix=postfix)
    setPatTauDefaults(getattr(process, "patTaus"+postfix), False)
    getattr(process, "patTaus"+postfix).tauSource = "hpsPFTauProducer"+postfix
    # Disable iso depositsm, they take a LOT of space
    getattr(process, "patTaus"+postfix).isoDeposits = cms.PSet()

    # Lepton modifications
    setPatLeptonDefaults(getattr(process, "patMuons"+postfix), False)
    #setPatLeptonDefaults(getattr(process, "patElectrons"+postfix), False)
    #addPatElectronID(process, getattr(process, "patElectrons"+postfix), getattr(process, "makePatElectrons"+postfix))

    # PATElectronProducer segfaults, and we don't really need them now
    getattr(process, "patDefaultSequence"+postfix).remove(getattr(process, "makePatElectrons"+postfix))
    getattr(process, "patDefaultSequence"+postfix).remove(getattr(process, "selectedPatElectrons"+postfix))
    getattr(process, "patDefaultSequence"+postfix).remove(getattr(process, "countPatElectrons"+postfix))
    getattr(process, "patDefaultSequence"+postfix).remove(getattr(process, "countPatLeptons"+postfix))

    # Disable muon and electron top projections, needs wider
    # discussion about lepton definitions
    getattr(process, "pfNoMuon"+postfix).enable = False
    getattr(process, "pfNoElectron"+postfix).enable = False

    # Disable tau top projection, the taus are identified separately
    getattr(process, "pfNoTau"+postfix).enable = False

    # Remove photon MC matcher in order to avoid keeping photons in the event content
    #process.patDefaultSequencePFlow.remove(process.photonMatchPFlow)

    if hasOut:
        process.out.outputCommands = outputCommandsBackup
        process.out.outputCommands.extend(outputCommands)
    else:
        del process.out

    getattr(process, "patDefaultSequence"+postfix).replace(
        getattr(process, "patTaus"+postfix),
        patTauSeq *
        getattr(process, "patTaus"+postfix)
    )

    sequence = cms.Sequence(
        getattr(process, "patPF2PATSequence"+postfix) *
        pfKt6Sequence
    )

    if doTauHLTMatching:
        sequence *= HChTriggerMatching.addTauHLTMatching(process, matchingTauTrigger, collections=["selectedPatTaus"+postfix], postfix=postfix)

    return sequence


### The functions below are taken from
### UserCode/PFAnalyses/VBFHTauTau/python/vbfDiTauPATTools.py
### revision 1.7

###################a#################################################
from CommonTools.ParticleFlow.Isolation.tools_cfi import isoDepositReplace

def addSelectedPFlowParticle(process,verbose=False):
    if verbose:
        print "[Info] Adding pf-particles (for pf-isolation and pf-seed pat-leptons)"
    process.load("CommonTools.ParticleFlow.ParticleSelectors.pfSortByType_cff")
    process.load("CommonTools.ParticleFlow.pfNoPileUp_cff")

    # From https://hypernews.cern.ch/HyperNews/CMS/get/muon/638.html
    process.pfPileUpCandidates = cms.EDProducer("TPPFCandidatesOnPFCandidates",
        enable =  cms.bool( True ),
        verbose = cms.untracked.bool( False ),
        name = cms.untracked.string("pileUpCandidates"),
        topCollection = cms.InputTag("pfNoPileUp"),
        bottomCollection = cms.InputTag("particleFlow"),
    )
    process.pfNoPileUpSequence *= process.pfPileUpCandidates

    process.pfCandidateSelectionByType = cms.Sequence(
        process.pfNoPileUpSequence * 
        process.pfAllNeutralHadrons *
        process.pfAllChargedHadrons *
        process.pfAllPhotons *
        process.pfAllMuons *
        process.pfAllElectrons
        )
    process.pfPileUp.Enable = True # enable pile-up filtering
    process.pfPileUp.Vertices = "offlinePrimaryVertices" # use vertices w/o BS
    process.pfAllMuons.src = "particleFlow"
    process.pfAllElectrons.src = "particleFlow"
    
    # From https://hypernews.cern.ch/HyperNews/CMS/get/muon/638.html
    process.pileUpHadrons = cms.EDFilter("PdgIdPFCandidateSelector",
        src = cms.InputTag("pfPileUpCandidates"),
        #Pick if you want  electrons and muons as well 
        pdgId = cms.vint32(211,-211,321,-321,999211,2212,-2212,11,-11,13,-13)
        #pdgId = cms.vint32(211,-211,321,-321,999211,2212,-2212)
    )
    process.pfCandidateSelectionByType *= process.pileUpHadrons

    process.hplusPatSequence.replace(process.hplusPatTauSequence,
                                     process.pfCandidateSelectionByType+
                                     process.hplusPatTauSequence)

# From https://hypernews.cern.ch/HyperNews/CMS/get/muon/638.html
def addPFMuonIsolation(process, module, verbose=False):
#    if verbose:
#        print "[Info] Adding particle isolation to muon with postfix '"+postfix+"'"

    if not hasattr(process, "pfCandidateSelectionByType"):
        addSelectedPFlowParticle(process,verbose=verbose)

    process.muPFIsoDepositAll = isoDepositReplace('muons',"pfNoPileUp")
    process.muPFIsoDepositCharged = isoDepositReplace('muons',"pfAllChargedHadrons")
    process.muPFIsoDepositNeutral = isoDepositReplace('muons',"pfAllNeutralHadrons")
    process.muPFIsoDepositGamma = isoDepositReplace('muons',"pfAllPhotons")
    #For Delta beta methos create an additional one fot charged particles from PV
    process.muPFIsoDepositPU = isoDepositReplace('muons',"pileUpHadrons")

    prototype = cms.EDProducer("CandIsolatorFromDeposits",
        deposits = cms.VPSet(
            cms.PSet(
                src = cms.InputTag("dummy"),
                deltaR = cms.double(0.4),
                weight = cms.string('1'),
                vetos = cms.vstring(""),
                skipDefaultVeto = cms.bool(True),
                mode = cms.string('sum')
            )
        )
    )

    for a in ["All", "Charged", "Neutral", "Gamma", "PU"]:
        m = prototype.clone()
        m.deposits[0].src = "muPFIsoDeposit"+a
        setattr(process, "muPFIsoValue"+a, m)
    process.muPFIsoValueAll.deposits[0].vetos = ['0.001','Threshold(0.5)']
    process.muPFIsoValueCharged.deposits[0].vetos = ['0.0001','Threshold(0.0)']
    process.muPFIsoValueNeutral.deposits[0].vetos = ['0.01','Threshold(0.5)']
    process.muPFIsoValueGamma.deposits[0].vetos = ['0.01','Threshold(0.5)']
    #For delta beta add one that has the same threshold as the neutral ones above
    process.muPFIsoValuePU.deposits[0].vetos = ['0.0001','Threshold(0.5)']
    
    process.patMuonIsolationSequence = cms.Sequence(
        process.muPFIsoDepositAll *
        process.muPFIsoDepositCharged *
        process.muPFIsoDepositNeutral *
        process.muPFIsoDepositGamma *
        process.muPFIsoDepositPU *
        process.muPFIsoValueAll *
        process.muPFIsoValueCharged *
        process.muPFIsoValueNeutral *
        process.muPFIsoValueGamma *
        process.muPFIsoValuePU
    )
    
    module.isoDeposits = cms.PSet(
        particle         = cms.InputTag("muPFIsoDepositAll"),
        pfChargedHadrons = cms.InputTag("muPFIsoDepositCharged"),
        pfNeutralHadrons = cms.InputTag("muPFIsoDepositNeutral"),
        pfPhotons        = cms.InputTag("muPFIsoDepositGamma")
    )

    #as you can see the PU deposit will be accessed by muon.userIso(0)
    module.isolationValues = cms.PSet(
        particle         = cms.InputTag("muPFIsoValueAll"),
        pfChargedHadrons = cms.InputTag("muPFIsoValueCharged"),
        pfNeutralHadrons = cms.InputTag("muPFIsoValueNeutral"),
        pfPhotons        = cms.InputTag("muPFIsoValueGamma"),
        user = cms.VInputTag(
            cms.InputTag("muPFIsoValuePU")
        )
    )

    process.patDefaultSequence.replace(module,
                                       process.patMuonIsolationSequence+module)


### UserCode/PFAnalyses/VBFHTauTau/python/vbfDiTauPATTools.py
### revision 1.7
def addPFMuonIsolationOld(process,module,postfix="",verbose=False):
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
