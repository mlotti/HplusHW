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
import HiggsAnalysis.HeavyChHiggsToTauNu.HChMcSelection as HChMcSelection
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTools as HChTools
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelectionPF_cff as MuonSelection
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.RemoveSoftMuonVisitor as RemoveSoftMuonVisitor

tauPreSelection = "pt() > 15"
#tauPreSelection = ""

jetPreSelection = "pt() > 10"
#jetPreSelection = ""

##################################################
#
# PAT on the fly
#
def addPatOnTheFly(process, options, dataVersion,
                   doPlainPat=True, doPF2PAT=False,
                   plainPatArgs={}, pf2patArgs={},
                   doMcPreselection=False):
    def setPatArg(args, name, value):
        if name in args:
            print "Overriding PAT arg '%s' from '%s' to '%s'" % (name, str(args[name]), str(value))
        args[name] = value
    def setPatArgs(args, d):
        for name, value in d.iteritems():
            setPatArg(args, name, value)

    counters = []
    if dataVersion.isData():
        counters.extend(HChDataSelection.dataSelectionCounters[:])
    
    if options.tauEmbeddingInput != 0:
        import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.PFEmbeddingSource_cff as PFEmbeddingSource
        counters.extend(MuonSelection.muonSelectionCounters[:])
        counters.extend(PFEmbeddingSource.muonSelectionCounters)
    elif dataVersion.isMC() and doMcPreselection:
        counters = HChMcSelection.mcSelectionCounters[:]
    
    if options.doPat == 0:
        process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex_cfi")
        seq = cms.Sequence(
#            process.goodPrimaryVertices10
        )
        if dataVersion.isMC() and doMcPreselection:
            process.eventPreSelection = HChMcSelection.addMcSelection(process, dataVersion, options.trigger)
            seq *= process.eventPreSelection
        return (seq, counters)

    print "Running PAT on the fly"

    process.eventPreSelection = cms.Sequence()
    if options.tauEmbeddingInput != 0:
        if doPF2PAT or not doPlainPat:
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
            process.eventPreSelection = HChDataSelection.addDataSelection(process, dataVersion, options.trigger)
        elif dataVersion.isMC() and doMcPreselection:
            process.eventPreSelection = HChMcSelection.addMcSelection(process, dataVersion, options.trigger)

        pargs = plainPatArgs.copy()
        pargs2 = pf2patArgs.copy()

        argsList = []
        if doPlainPat:
            argsList.append(pargs)
        if doPF2PAT:
            argsList.append(pargs2)

        for args in argsList:
            if args.get("doTauHLTMatching", True):
                if not "matchingTauTrigger" in args:
                    if options.trigger == "":
                        raise Exception("Command line argument 'trigger' is missing")
                    args["matchingTauTrigger"] = options.trigger
                print "Trigger used for tau matching:", args["matchingTauTrigger"]

        process.patSequence = addPat(process, dataVersion,
                                     doPlainPat=doPlainPat, doPF2PAT=doPF2PAT,
                                     plainPatArgs=pargs, pf2patArgs=pargs2,)
    
    # Add selection of PVs with sumPt > 10
#    process.patSequence *= process.goodPrimaryVertices10

    dataPatSequence = cms.Sequence(
        process.eventPreSelection *
        process.patSequence
    )

    if options.tauEmbeddingInput != 0:
        from HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations import addTauEmbeddingMuonTaus
        process.patMuonTauSequence = addTauEmbeddingMuonTaus(process)
        process.patSequence *= process.patMuonTauSequence
    
    return (dataPatSequence, counters)


# Add the PAT sequences as requested
def addPat(process, dataVersion,
           doPlainPat=True, doPF2PAT=False,
           plainPatArgs={}, pf2patArgs={},
           includePFCands=False):
    process.pf2patSequence = cms.Sequence()
    process.plainPatSequence = cms.Sequence()

    # Select good primary vertices
    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex_cfi")
    process.offlinePrimaryVerticesSumPt = cms.EDProducer("HPlusVertexViewSumPtComputer",
        src = cms.InputTag("offlinePrimaryVertices")
    )

    # Run various PATs
    if doPF2PAT:
        process.pf2patSequence = addPF2PAT(process, dataVersion, **pf2patArgs)
    if doPlainPat:
        process.plainPatSequence = addPlainPat(process, dataVersion, includePFCands=includePFCands, **plainPatArgs)

    # Adjust event conent
    outdict = process.outputModules_()
    if outdict.has_key("out"):
        out = outdict["out"]
        out.outputCommands.extend([
 #               "keep *_goodPrimaryVertices*_*_*",
                "keep *_offlinePrimaryVerticesSumPt_*_*",
                "keep *_offlineBeamSpot_*_*",
                ])

        if includePFCands:
            out.outputCommands.extend([
                    "keep *_particleFlow_*_*",
                    "keep *_generalTracks_*_*",
                    ])

    # PAT function must be added last (PF2PAT requires unmodified
    # patDefaultSequence), but run first (we use some stuff produced
    # with plain PAT in PF2PAT)
    sequence = cms.Sequence(
#        process.goodPrimaryVertices *
#        process.goodPrimaryVertices10 *
        process.offlinePrimaryVerticesSumPt *
        process.plainPatSequence *
        process.pf2patSequence
    )

    return sequence

def myRemoveCleaning(process, postfix=""):
    modulesInSequence = getattr(process, "patDefaultSequence"+postfix).moduleNames()
    for module in [
        "cleanPatMuons",
        "cleanPatElectrons",
        "cleanPatPhotons",
        "cleanPatTaus",
        "cleanPatTausHpsTancPFTau",
        "cleanPatTausHpsPFTau",
        "cleanPatTausShrinkingConePFTau",
        "cleanPatTausCaloRecoTau",
        "cleanPatJets",
        "cleanPatCandidateSummary",
        "countPatElectrons",
        "countPatMuons",
        "countPatTaus",
        "countPatLeptons",
        "countPatPhotons",
        "countPatJets",
        "countPatJetsAK5PF",
        "countPatJetsAK5JPT",
        "countPatPFParticlesPFlow",
        ]:
        if hasattr(process, module+postfix) and module+postfix in modulesInSequence:
            getattr(process, "patDefaultSequence"+postfix).remove(getattr(process, module+postfix))

# Assumes that process.out is the output module
#
#
# process      cms.Process object
# dataVersion  Version of the input data (needed for the trigger info process name) 
def addPlainPat(process, dataVersion, doPatTrigger=True, doPatTaus=True, doHChTauDiscriminators=True, doPatMET=True, doPatElectronID=True,
                doPatCalo=True, doBTagging=True, doPatMuonPFIsolation=False, doPatTauIsoDeposits=False,
                doTauHLTMatching=True, matchingTauTrigger=None, matchingJetTrigger=None,
                includePFCands=False):
    out = None
    outdict = process.outputModules_()
    if outdict.has_key("out"):
        out = outdict["out"]

    outputCommands = []

    # Tau Discriminators
    process.hplusPatTauSequence = cms.Sequence()
    if doPatTaus:
        process.hplusPatTauSequence = addPFTausAndDiscriminators(process, dataVersion, doPatCalo, doHChTauDiscriminators)

    # PAT Layer 0+1
    process.load("PhysicsTools.PatAlgos.patSequences_cff")

    sequence = cms.Sequence(
        process.hplusPatTauSequence
    )

    # Restrict input to AOD
    restrictInputToAOD(process, ["All"])

    # Remove MC stuff if we have collision data (has to be done any add*Collection!)
    # This also adds the L2L3Residual JEC correction to the process.patJetCorrFactors
    if dataVersion.isData():
        runOnData(process, outputInProcess = out!=None)

    # Jets
    # Produce kt6 rho for L1Fastjet
    process.load('RecoJets.Configuration.RecoPFJets_cff')
    process.kt6PFJets.doRhoFastjet = True
    process.ak5PFJets.doAreaFastjet = True
    process.ak5PFJetSequence = cms.Sequence(process.kt6PFJets * process.ak5PFJets)
   
    # Set defaults
    process.patJets.jetSource = cms.InputTag("ak5CaloJets")
    process.patJets.trackAssociationSource = cms.InputTag("ak5JetTracksAssociatorAtVertex")
    setPatJetDefaults(process.patJets)
    setPatJetCorrDefaults(process.patJetCorrFactors, dataVersion)
    process.patDefaultSequence.replace(process.patJetCorrFactors,
                                       process.ak5PFJetSequence*process.patJetCorrFactors)
    process.selectedPatJets.cut = jetPreSelection

    # The default JEC to be embedded to pat::Jets are L2Relative,
    # L3Absolute, L5Flavor and L7Parton. The default JEC to be applied
    # is L2L3Residual, or L3Absolute, or Uncorrected (in this order).

    if doPatCalo:
        # Add JPT jets
        # FIXME: Disabled for now until the JEC for JPT works again (with the latest JEC)
#        addJetCollection(process, cms.InputTag('JetPlusTrackZSPCorJetAntiKt5'),
#                         'AK5', 'JPT',
#                         doJTA        = True,
#                         doBTagging   = doBTagging,
#                         jetCorrLabel = ('AK5JPT', process.patJetCorrFactors.levels),
#                         doType1MET   = False,
#                         doL1Cleaning = False,
#                         doL1Counters = True,
#                         genJetCollection = cms.InputTag("ak5GenJets"),
#                         doJetID      = True
#        )
    
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
        setPatJetCorrDefaults(process.patJetCorrFactorsAK5PF, dataVersion, True)

    else:
        setPatJetCorrDefaults(process.patJetCorrFactors, dataVersion, True)
        switchJetCollection(process, cms.InputTag('ak5PFJets'),
                            doJTA        = True,
                            doBTagging   = doBTagging,
                            jetCorrLabel = ('AK5PF', process.patJetCorrFactors.levels),
                            doType1MET   = False,
                            genJetCollection = cms.InputTag("ak5GenJets"),
                            doJetID      = True
        )
    
    outputCommands.extend([
            "keep *_selectedPatJets_*_*",
            "keep *_selectedPatJetsAK5JPT_*_*",
            "keep *_selectedPatJetsAK5PF_*_*",
            'drop *_selectedPatJets_pfCandidates_*', ## drop for default patJets which are CaloJets
            'drop *_*PF_caloTowers_*',
            'drop *_*JPT_pfCandidates_*',
            'drop *_*Calo_pfCandidates_*',
            ])

    # Taus

    # Set default PATTauProducer options here, they should be
    # replicated to all added tau collections (and the first call to
    # addTauCollection should replace the default producer modified
    # here)
    setPatTauDefaults(process.patTaus, includePFCands)
    process.selectedPatTaus.cut = tauPreSelection

    if doPatTaus:
        if doHChTauDiscriminators:
            addHChTauDiscriminators()

        # Don't enable TCTau nor shrinking cone tau
        # if doPatCalo:
        #     tauTools.addTauCollection(process,cms.InputTag('caloRecoTauProducer'),
        #                      algoLabel = "caloReco",
        #                      typeLabel = "Tau")
        #     setPatTauDefaults(process.patTausCaloRecoTau, True)
        #     process.patTausCaloRecoTau.embedLeadTrack = not includePFCands
        #     process.patTausCaloRecoTau.embedLeadPFChargedHadrCand = False
    
        # tauTools.addTauCollection(process,cms.InputTag('shrinkingConePFTauProducer'),
        #                  algoLabel = "shrinkingCone",
        #                  typeLabel = "PFTau")
        # # Disable isoDeposits like this until the problem with doPFIsoDeposits is fixed 
        # if not doPatTauIsoDeposits:
        #     process.patTausShrinkingConePFTau.isoDeposits = cms.PSet()

        tauTools.addTauCollection(process,cms.InputTag('hpsPFTauProducer'),
                         algoLabel = "hps",
                         typeLabel = "PFTau")
        if not doPatTauIsoDeposits:
            process.patTausHpsPFTau.isoDeposits = cms.PSet()
        addPatTauIsolationEmbedding(process, process.patDefaultSequence, "HpsPFTau")

        tauTools.addTauCollection(process,cms.InputTag('hpsTancTaus'),
                                  algoLabel = "hpsTanc",
                                  typeLabel = "PFTau")
        if not doPatTauIsoDeposits:
            process.patTausHpsTancPFTau.isoDeposits = cms.PSet()
        # Disable discriminators which are not in AOD
#        del process.patTausHpsTancPFTau.tauIDSources.againstCaloMuon
#        del process.patTausHpsTancPFTau.tauIDSources.byHPSvloose
        addPatTauIsolationEmbedding(process, process.patDefaultSequence, "HpsTancPFTau")

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
            sequence *= process.VisibleTaus
            outputCommands.append("keep *_VisibleTaus_*_*")

    else:
        # FIXME: this is broken at the moment
        #removeSpecificPATObjects(process, ["Taus"], outputInProcess= out != None)
        process.patDefaultSequence.remove(process.patTaus)
        process.patDefaultSequence.remove(process.selectedPatTaus)

    outputCommands.extend(["drop *_selectedPatTaus_*_*",
#                           "keep *_selectedPatTausCaloRecoTau_*_*",
#                           "keep *_selectedPatTausShrinkingConePFTau_*_*",
                           "keep *_selectedPatTausHpsPFTau_*_*",
                           "keep *_selectedPatTausHpsTancPFTau_*_*",
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
        outputCommands.extend([
                "keep *_patMETs_*_*",
                "keep *_patMETsTC_*_*",
                "keep *_patMETsPF_*_*",
                "keep *_genMetTrue_*_*",
        ])
    else:
        # FIXME: This is broken at the moment...
        #removeSpecificPATObjects(process, ["METs"], outputInProcess= out != None)
        #process.patDefaultSequen
        process.patDefaultSequence.remove(process.patMETCorrections)
        process.patDefaultSequence.remove(process.patMETs)
        del process.patMETCorrections
        del process.patMETs

    # Muons
    setPatLeptonDefaults(process.patMuons, includePFCands)
    if doPatMuonPFIsolation:
        addPFMuonIsolation(process, process.patMuons, sequence, verbose=True)

    outputCommands.extend([
            "keep *_selectedPatMuons_*_*"
            ])

    # Electrons
    # In order to calculate the transverse impact parameter w.r.t.
    # beam spot instead of primary vertex, see
    setPatLeptonDefaults(process.patMuons, includePFCands)

    # Electron ID, see
    # https://twiki.cern.ch/twiki/bin/view/CMS/SimpleCutBasedEleID
    if doPatElectronID:
        addPatElectronID(process, process.patElectrons, process.patDefaultSequence)

    outputCommands.extend([
            "keep *_selectedPatElectrons_*_*"
            ])

    # Photons
#    process.patPhotons.embedGenMatch = False
    outputCommands.extend([
            "keep *_selectedPatPhotons_*_*"
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
        myRemoveCleaning(process)
    else:
        backup = out.outputCommands[:]
        myRemoveCleaning(process)
#        backup_pat = out.outputCommands[:]

        # Remove PFParticles here, they are explicitly included when needed
#        backup_pat = filter(lambda n: "selectedPatPFParticles" not in n, backup_pat)

        out.outputCommands = backup
#        out.outputCommands.extend(backup_pat)
        out.outputCommands.extend(outputCommands)

    # Build sequence
    sequence *= process.patDefaultSequence

    # Tau+HLT matching
    if doTauHLTMatching:
        sequence *= HChTriggerMatching.addTauHLTMatching(process, matchingTauTrigger, matchingJetTrigger)

    return sequence

# Helper functions
def fixFlightPath(process, prefix, postfix=""):
    from RecoTauTag.RecoTau.PFRecoTauQualityCuts_cfi import PFTauQualityCuts
    getattr(process, prefix+"DiscriminationByFlightPathSignificance"+postfix).qualityCuts = PFTauQualityCuts

def addPatTauIsolationEmbedding(process, sequence, name):
    import RecoTauTag.Configuration.RecoPFTauTag_cff as RecoPFTauTag

    prevName = "patTaus"+name
    for iso in ["Tight", "Medium", "Loose", "VLoose"]:
        module = cms.EDProducer("HPlusPATTauViewIsolationEmbedder",
            candSrc = cms.InputTag(prevName),
            primaryVertexSrc = cms.InputTag("offlinePrimaryVertices"),
            embedPrefix = cms.string("by"+iso)
        )
        module.qualityCuts = getattr(RecoPFTauTag, "hpsPFTauDiscriminationBy%sIsolation"%iso).qualityCuts.clone()

        newName = "patTaus%sWith%sEmbedded" % (name, iso)
        setattr(process, newName, module)

        prevModule = getattr(process, prevName)
        sequence.replace(prevModule, prevModule*module)
        prevName = newName

    getattr(process, "selectedPatTaus"+name).src = prevName

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

        # Tau bugfixes
        # The quality PSet is missing
        for tauAlgo in ["caloRecoTau"]+tauAlgos:
            fixFlightPath(process, tauAlgo)
            fixFlightPath(process, tauAlgo, "Cont")


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

def patJetCorrLevels(dataVersion, L1FastJet=False):
    levels = []
    if L1FastJet:
        levels.append("L1FastJet")
    else:
        levels.append("L1Offset")
    levels.extend(["L2Relative", "L3Absolute"])
    if dataVersion.isData():
        levels.append("L2L3Residual")
    levels.extend(["L5Flavor", "L7Parton"])
    return levels

def setPatJetCorrDefaults(module, dataVersion, L1FastJet=False):
    module.levels = cms.vstring(patJetCorrLevels(dataVersion, L1FastJet))
    module.useRho = L1FastJet

def setPatTauDefaults(module, includePFCands):
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

    value = not includePFCands
    for a in attrs:
        setattr(module, a, value)
#    module.embedGenMatch = False


def addHChTauDiscriminators():
    if HChTaus.HChTauIDSources[0] in tauTools.classicTauIDSources:
        print "addHChTauDiscriminators called already once, not adding them again"
        return

    for idSources in [tauTools.classicTauIDSources, tauTools.hpsTauIDSources, tauTools.hpsTancTauIDSources]:
        idSources.extend(HChTaus.HChTauIDSources)
        idSources.extend(HChTausCont.HChTauIDSourcesCont)
    for idSources in [tauTools.classicPFTauIDSources, tauTools.hpsTauIDSources, tauTools.hpsTancTauIDSources]:
        idSources.extend(HChTausTest.TestTauIDSources)

def setPatLeptonDefaults(module, includePFCands):
    # In order to calculate the transverse impact parameter w.r.t.
    # beam spot instead of primary vertex, see
    # https://twiki.cern.ch/twiki/bin/view/CMS/WorkBookPATExampleTopQuarks
    module.usePV = False
    module.embedTrack = not includePFCands
#    module.embedGenMatch = False

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
def addPF2PAT(process, dataVersion, postfix="PFlow",
              doTauHLTMatching=True, matchingTauTrigger=None, 
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

    # Jet modifications
    # PhysicsTools/PatExamples/test/patTuple_42x_jec_cfg.py
    jetCorrFactors = patJetCorrLevels(dataVersion, True)
    jetCorrPayload = "AK5PFchs"

    process.load("PhysicsTools.PatAlgos.patSequences_cff")
    pfTools.usePF2PAT(process, runPF2PAT=True, jetAlgo="AK5", jetCorrections=(jetCorrPayload, jetCorrFactors),
                      runOnMC=dataVersion.isMC(), postfix=postfix)

    outputCommands = [
#        "keep *_selectedPatPhotons%s_*_*" % postfix,
#        'keep *_selectedPatElectrons%s_*_*' % postfix, 
        'keep *_selectedPatMuons%s_*_*' % postfix,
        'keep *_selectedPatJets%s*_*_*' % postfix,
        'keep *_selectedPatTaus%s_*_*' % postfix,
        'keep *_selectedPatPFParticles%s_*_*' % postfix,
        'keep *_selectedPatJets%s_pfCandidates_*' % postfix,
        'drop *_*PF_caloTowers_*',
        'drop *_*JPT_pfCandidates_*',
        'drop *_*Calo_pfCandidates_*',
        'keep *_patMETs%s_*_*' % postfix,
        ]

    # Enable PFnoPU
    getattr(process, "pfPileUp"+postfix).Enable = True
    getattr(process, "pfPileUp"+postfix).checkClosestZVertex = False
    getattr(process, "pfPileUp"+postfix).Vertices = "offlinePrimaryVertices"

    # Jet modifications
    # L1FastJet
    # https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#OffsetJEC
    # https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#JetEnCor2011
    # https://hypernews.cern.ch/HyperNews/CMS/get/jes/184.html
    kt6name = "kt6PFJets"+postfix
    process.load('RecoJets.Configuration.RecoPFJets_cff')
    from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
    setattr(process, kt6name, kt4PFJets.clone(
        rParam = 0.6,
        src = 'pfNoElectron'+postfix,
        doRhoFastjet = True,
        doAreaFastJet = cms.bool(True),
    ))
    getattr(process, "patPF2PATSequence"+postfix).replace(
        getattr(process, "pfNoElectron"+postfix),
        getattr(process, "pfNoElectron"+postfix) * getattr(process, kt6name))
    getattr(process, "patJetCorrFactors"+postfix).rho = cms.InputTag(kt6name, "rho")
    getattr(process, "patJetCorrFactors"+postfix).useRho = True

    # ak5PFJets
    getattr(process, "pfJets"+postfix).doAreaFastjet = cms.bool(True)
    getattr(process, "pfJets"+postfix).doRhoFastjet = False
#    getattr(process, "pfJets"+postfix).Vertices = cms.InputTag("goodPrimaryVertices")

    setPatJetDefaults(getattr(process, "patJets"+postfix))


    # Use HPS taus
    # Add and recalculate the discriminators
    addHChTauDiscriminators()
    if not hasattr(process, "hpsPFTauDiscriminationForChargedHiggsByLeadingTrackPtCut"):
        import RecoTauTag.RecoTau.PFRecoTauDiscriminationForChargedHiggs_cfi as HChPFTauDiscriminators
        import RecoTauTag.RecoTau.CaloRecoTauDiscriminationForChargedHiggs_cfi as HChCaloTauDiscriminators

        tauAlgos = ["hpsPFTau"]
#        tauAlgos = ["pfTaus"+postfix]
        HChPFTauDiscriminators.addPFTauDiscriminationSequenceForChargedHiggs(process, tauAlgos)
        HChPFTauDiscriminatorsCont.addPFTauDiscriminationSequenceForChargedHiggsCont(process, tauAlgos)
        PFTauTestDiscrimination.addPFTauTestDiscriminationSequence(process, tauAlgos)

        fixFlightPath(process, tauAlgos[0])
        fixFlightPath(process, tauAlgos[0], "Cont")
    
    patHelpers.cloneProcessingSnippet(process, process.hpsPFTauHplusDiscriminationSequence, postfix)
    patHelpers.cloneProcessingSnippet(process, process.hpsPFTauHplusDiscriminationSequenceCont, postfix)
    patHelpers.cloneProcessingSnippet(process, process.hpsPFTauHplusTestDiscriminationSequence, postfix)

    patTauSeq = cms.Sequence(
        getattr(process, "hpsPFTauHplusDiscriminationSequence"+postfix) *
        getattr(process, "hpsPFTauHplusDiscriminationSequenceCont"+postfix) * 
        getattr(process, "hpsPFTauHplusTestDiscriminationSequence"+postfix)
#        getattr(process, "pfTaus"+postfix+"HplusDiscriminationSequence") *
#        getattr(process, "pfTaus"+postfix+"HplusDiscriminationSequenceCont") * 
#        getattr(process, "pfTaus"+postfix+"HplusTestDiscriminationSequence")
    )
    setattr(process, "hplusPatTauSequence"+postfix, patTauSeq)
    patHelpers.massSearchReplaceParam(patTauSeq, "PFTauProducer", cms.InputTag("hpsPFTauProducer"), cms.InputTag("pfTaus"+postfix))
    patHelpers.massSearchReplaceAnyInputTag(patTauSeq, cms.InputTag("hpsPFTauDiscriminationByDecayModeFinding"), cms.InputTag("hpsPFTauDiscriminationByDecayModeFinding"+postfix))

    pfTools.adaptPFTaus(process, "hpsPFTau", postfix=postfix)

    setPatTauDefaults(getattr(process, "patTaus"+postfix), False)
    addPatTauIsolationEmbedding(process, getattr(process, "patDefaultSequence"+postfix), postfix)
    getattr(process, "selectedPatTaus"+postfix).cut = tauPreSelection

    # The prediscriminant of pfTausBaseDiscriminationByLooseIsolation
    # is missing from the default sequence, but since we don't want to
    # apply any tau selections as a part of PF2PAT anyway, let's just
    # remove this too
    getattr(process, "pfTaus"+postfix).discriminators = cms.VPSet()
#    getattr(process, "pfTauSequence"+postfix).remove(getattr(process, "pfTaus"+postfix))
#    delattr(process, "pfTaus"+postfix)
#    getattr(process, "pfTausBaseSequence"+postfix).remove(getattr(process, "pfTausBaseDiscriminationByLooseIsolation"+postfix))
    

    # Remove the shrinking cone altogether, we don't care about it
#    getattr(process, "patDefaultSequence"+postfix).remove(getattr(process, "patShrinkingConePFTauDiscrimination"+postfix))

    # Override the tau source (this is WRONG in the standard PF2PAT, the expers should know it already)
#    getattr(process, "patTaus"+postfix).tauSource = "hpsPFTauProducer"+postfix
#    patHelpers.massSearchReplaceAnyInputTag(getattr(process, "patHPSPFTauDiscrimination"+postfix),
#                                            cms.InputTag("pfTaus"+postfix),
#                                            cms.InputTag("hpsPFTauProducer"+postfix))
#    getattr(process, "pfNoTau"+postfix).topCollection = cms.InputTag("hpsPFTauProducer"+postfix)

    # Disable iso deposits, they take a LOT of space
    getattr(process, "patTaus"+postfix).isoDeposits = cms.PSet()

    # Disable tau top projection, the taus are identified and removed
    # from jets as a part of the analysis
    getattr(process, "pfNoTau"+postfix).enable = False



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
        getattr(process, "patPF2PATSequence"+postfix)
    )

    if doTauHLTMatching:
        sequence *= HChTriggerMatching.addTauHLTMatching(process, matchingTauTrigger, collections=["selectedPatTaus"+postfix], postfix=postfix)

    return sequence


### The functions below are taken from
### UserCode/PFAnalyses/VBFHTauTau/python/vbfDiTauPATTools.py
### revision 1.7

###################a#################################################
from CommonTools.ParticleFlow.Isolation.tools_cfi import isoDepositReplace

def addSelectedPFlowParticle(process, sequence, verbose=False):
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
    sequence *= process.pfCandidateSelectionByType

# From https://hypernews.cern.ch/HyperNews/CMS/get/muon/638.html
def addPFMuonIsolation(process, module, sequence, verbose=False):
#    if verbose:
#        print "[Info] Adding particle isolation to muon with postfix '"+postfix+"'"

    if not hasattr(process, "pfCandidateSelectionByType"):
        addSelectedPFlowParticle(process, sequence, verbose=verbose)

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
