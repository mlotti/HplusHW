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
import CommonTools.ParticleFlow.TopProjectors.pfNoJet_cfi as pfNoJet
import HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationForChargedHiggs as HChPFTauDiscriminators
import HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationForChargedHiggsContinuous as HChPFTauDiscriminatorsCont
import HiggsAnalysis.HeavyChHiggsToTauNu.CaloRecoTauDiscriminationForChargedHiggsContinuous as HChCaloTauDiscriminatorsCont
import HiggsAnalysis.HeavyChHiggsToTauNu.PFTauTestDiscrimination as PFTauTestDiscrimination
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTriggerMatching as HChTriggerMatching
import HiggsAnalysis.HeavyChHiggsToTauNu.HChDataSelection as HChDataSelection
import HiggsAnalysis.HeavyChHiggsToTauNu.HChMcSelection as HChMcSelection
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTools as HChTools
import HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex as HChPrimaryVertex
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelectionPF_cff as MuonSelection
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.RemoveSoftMuonVisitor as RemoveSoftMuonVisitor
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as tauEmbeddingCustomisations

tauPreSelection = "pt() > 15"
#tauPreSelection = ""

#jetPreSelection = "pt() > 10"
jetPreSelection = ""

##################################################
#
# PAT on the fly
#
def addPatOnTheFly(process, options, dataVersion,
                   doPlainPat=True, doPF2PAT=False,
                   patArgs={},
                   doMcPreselection=False,
                   doTotalKinematicsFilter=False,
                   doHBHENoiseFilter=True, doPhysicsDeclared=False,
                   calculateEventCleaning=False,
                   ):
    if doPlainPat and doPF2PAT:
        raise Exception("Plain PAT and PF2PAT can not coexist!")


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
        seq = cms.Sequence()
    
        if dataVersion.isMC():
            # First apply total kinematics filter
            if doTotalKinematicsFilter:
                import HLTrigger.HLTfilters.hltHighLevel_cfi as hltHighLevel
                process.totalKinematicsFilter = hltHighLevel.hltHighLevel.clone(
                    TriggerResultsTag = cms.InputTag("TriggerResults", "", "HChPatTuple"),
                    HLTPaths = cms.vstring("totalKinematicsFilterPath")
                )
                process.totalKinematicsFilterAllEvents = cms.EDproducer("EventCountProcucer")
                process.totalKinematicsFilterPassed = cms.EDProducer("EventCountProducer")
                seq *= (
                    process.totalKinematicsFilterAllEvents *
                    process.totalKinematicsFilter *
                    process.totalKinematicsFilterPassed
                )
                counters.extend([
                        "totalKinematicsFilterAllEvents",
                        "totalKinematicsFilterPassed"
                        ])                    
    
            # Then apply MC preselection if wanted
            if doMcPreselection:
                process.eventPreSelection = HChMcSelection.addMcSelection(process, dataVersion, options.trigger)
                seq *= process.eventPreSelection
        else:
            if doPhysicsDeclared:
                counters.extend(HChDataSelection.addPhysicsDeclaredBit(process, seq))
            if doHBHENoiseFilter:
                counters.extend(HChDataSelection.addHBHENoiseFilter(process, seq))

        # Add primary vertex selection
        HChPrimaryVertex.addPrimaryVertexSelection(process, seq)

        if options.doTauHLTMatchingInAnalysis != 0:
            process.patTausHpsPFTauTauTriggerMatched = HChTriggerMatching.createTauTriggerMatchingInAnalysis(options.trigger, "selectedPatTausHpsPFTau")
            seq *= process.patTausHpsPFTauTauTriggerMatched
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
                             "doPatElectronID": False})

        process.patSequence = addPat(process, dataVersion, plainPatArgs=plainPatArgs)
        # FIXME: this is broken at the moment
        #removeSpecificPATObjects(process, ["Muons", "Electrons", "Photons"], False)
        process.patDefaultSequence.remove(process.patMuons)
        process.patDefaultSequence.remove(process.selectedPatMuons)
        #process.selectedPatCandidates.remove(process.selectedPatMuons)
        process.patDefaultSequence.remove(process.muonMatch)
        process.patDefaultSequence.remove(process.patElectrons)
        process.patDefaultSequence.remove(process.selectedPatElectrons)
        #process.selectedPatCandidates.remove(process.selectedPatElectrons)
        process.patDefaultSequence.remove(process.electronMatch)
        process.patDefaultSequence.remove(process.patPhotons)
        process.patDefaultSequence.remove(process.selectedPatPhotons)
        #process.selectedPatCandidates.remove(process.selectedPatPhotons)
        process.patDefaultSequence.remove(process.photonMatch)

        del process.patMuons
        del process.selectedPatMuons
        del process.muonMatch
        del process.patElectrons
        del process.selectedPatElectrons
        del process.electronMatch
        del process.patPhotons
        del process.selectedPatPhotons
        del process.photonMatch

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
            process.eventPreSelection = HChDataSelection.addDataSelection(process, dataVersion, options, calculateEventCleaning)

        elif dataVersion.isMC() and doMcPreselection:
            process.eventPreSelection = HChMcSelection.addMcSelection(process, dataVersion, options.trigger)

        pargs = patArgs.copy()

        pargs["calculateEventCleaning"] = calculateEventCleaning
        if pargs.get("doTauHLTMatching", True):
            if not "matchingTauTrigger" in pargs:
                if options.trigger == "":
                    raise Exception("Command line argument 'trigger' is missing")
                pargs["matchingTauTrigger"] = options.trigger
            print "Trigger used for tau matching:", pargs["matchingTauTrigger"]

        process.patSequence = addPat(process, dataVersion,
                                     doPlainPat=doPlainPat, doPF2PAT=doPF2PAT,
                                     patArgs=pargs)
    
    if dataVersion.isData():
        if doPhysicsDeclared:
            counters.extend(HChDataSelection.addPhysicsDeclaredBit(process, seq))
        if doHBHENoiseFilter:
            counters.extend(HChDataSelection.addHBHENoiseFilter(process, process.eventPreSelection))
    elif dataVersion.isMC() and doTotalKinematicsFilter:
        # TotalKinematicsFilter for managing with buggy LHE+Pythia samples
        # https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/1489.html
        # For pattuples, this is implemented in patTuple_cfg.py, and saved in the event via TriggerResults
        process.load("GeneratorInterface.GenFilters.TotalKinematicsFilter_cfi")
        process.totalKinematicsFilter.src.setProcessName(dataVersion.getTriggerProcess())
        process.totalKinematicsFilterAllEvents = cms.EDproducer("EventCountProcucer")
        process.totalKinematicsFilterPassed = cms.EDProducer("EventCountProducer")
        process.eventPreSelection *= (
            process.totalKinematicsFilterAllEvents *
            process.totalKinematicsFilter *
            process.totalKinematicsFilterPassed
        )
        counters.extend([
                "totalKinematicsFilterAllEvents",
                "totalKinematicsFilterPassed"
                ])                    

    HChPrimaryVertex.addPrimaryVertexSelection(process, process.eventPreSelection)
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
           patArgs={},
           includePFCands=False):
    if doPlainPat and doPF2PAT:
        raise Exception("Plain PAT and PF2PAT can not coexist!")

    # Run various PATs
    sequence = None
    if doPF2PAT:
        print "Using PF2PAT"
        sequence = addPF2PAT(process, dataVersion, **patArgs)
    elif doPlainPat:
        print "Using plain PAT"
        sequence = addPlainPat(process, dataVersion, includePFCands=includePFCands, **patArgs)
    else:
        raise Exception("Either plain PAT or PF2PAT must be run!")

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

    # ValueMap of sumPt of vertices
    process.offlinePrimaryVerticesSumPt = cms.EDProducer("HPlusVertexViewSumPtComputer",
        src = cms.InputTag("offlinePrimaryVertices")
    )
    sequence *= process.offlinePrimaryVerticesSumPt
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
        ]:
        if hasattr(process, module+postfix) and module+postfix in modulesInSequence:
            getattr(process, "patDefaultSequence"+postfix).remove(getattr(process, module+postfix))

    removeCounting(process, postfix)

def removeCounting(process, postfix=""):
    modulesInSequence = getattr(process, "patDefaultSequence"+postfix).moduleNames()
    for module in [
        "countPatElectrons",
        "countPatMuons",
        "countPatTaus",
        "countPatLeptons",
        "countPatPhotons",
        "countPatJets",
        "countPatJetsAK5PF",
        "countPatJetsAK5JPT",
        "countPatPFParticles",
        ]:
        if hasattr(process, module+postfix) and module+postfix in modulesInSequence:
            getattr(process, "patDefaultSequence"+postfix).remove(getattr(process, module+postfix))

# Assumes that process.out is the output module
#
#
# process      cms.Process object
# dataVersion  Version of the input data (needed for the trigger info process name) 
def addPlainPat(process, dataVersion, doPatTrigger=True, doPatTaus=True, doHChTauDiscriminators=True, doPatMET=True, doPatElectronID=True,
                doPatCalo=True, doBTagging=True, doPatTauIsoDeposits=False,
                doTauHLTMatching=True, matchingTauTrigger=None, matchingJetTrigger=None,
                doMuonHLTMatching=True,
                includePFCands=False,
                calculateEventCleaning=False):
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

    process.plainPatEndSequence = cms.Sequence()

    # Restrict input to AOD
    restrictInputToAOD(process, ["All"])

    # Remove MC stuff if we have collision data (has to be done any add*Collection!)
    # This also adds the L2L3Residual JEC correction to the process.patJetCorrFactors
    if dataVersion.isData():
        o = []
        if out != None:
            o = ["out"]
        runOnData(process, outputModules=o)

    # Tracks (mainly needed for muon efficiency tag&probe studies
    process.generalTracks20eta2p5 = cms.EDFilter(
        "TrackSelector",
        src = cms.InputTag("generalTracks"),
        cut = cms.string("pt > 20 && abs(eta) < 2.5"),
        filter = cms.bool(False)
    )
    sequence *= process.generalTracks20eta2p5
    outputCommands.append("keep *_generalTracks20eta2p5_*_*")

    # PF particle selectors
    addSelectedPFlowParticle(process, sequence)
    addPFCandidatePtSums(process, process.plainPatEndSequence)
    outputCommands.append("keep double_pf*SumPt_*_*")

    # Jets
    # Produce kt6 rho for L1Fastjet
    process.load('RecoJets.Configuration.RecoPFJets_cff')
    process.kt6PFJets.doRhoFastjet = True
    process.ak5PFJets.doAreaFastjet = True
    process.ak5PFJetSequence = cms.Sequence(process.kt6PFJets * process.ak5PFJets)

    # Calculate kt6 rho, maybe only neutrals and PU particles make sense?
    for particle in ["AllNeutralHadrons", "AllPhotons", "AllNeutralHadronsAndPhotons",
#                     "AllChargedHadrons", "AllChargedParticles",
                     "PileUpAllChargedParticles",
#                     "AllChargedHadronsNoChs", "AllChargedParticlesNoChs"
                     ]:
        m = process.kt6PFJets.clone(
            src = "pf"+particle
        )
        setattr(process, "kt6PFJets"+particle, m)
        process.plainPatEndSequence *= m
        outputCommands.append("keep *_kt6PFJets%s_rho_*" % particle)

    # Produce Type 2 MET correction from unclustered PFCandidates
    process.pfCandsNotInJet = pfNoJet.pfNoJet.clone(
        topCollection = cms.InputTag("ak5PFJets"),
        bottomCollection = cms.InputTag("particleFlow")
    )
    process.pfCandMETcorr = cms.EDProducer("PFCandMETcorrInputProducer",
        src = cms.InputTag('pfCandsNotInJet')
    )
    process.plainPatEndSequence *= (process.pfCandsNotInJet*process.pfCandMETcorr)
    outputCommands.append("keep *_pfCandMETcorr_*_*")

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

    betaPrototype = cms.EDProducer("HPlusPATJetViewBetaEmbedder",
        jetSrc = cms.InputTag("patJetsAK5PF"),
        vertexSrc = cms.InputTag("offlinePrimaryVertices"),
        embedPrefix = cms.string("")
    )

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
        process.patJetsAK5PFBetaEmbedded = betaPrototype.clone()
        process.selectedPatJetsAK5PF.src = "patJetsAK5PFBetaEmbedded"
        process.patDefaultSequence.replace(process.selectedPatJetsAK5PF,
                                           process.patJetsAK5PFBetaEmbedded*process.selectedPatJetsAK5PF)

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
        # Continous isolation
        addTauRawDiscriminators(process.patTausHpsPFTau)
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
    addPfMET(process, 'PF')
    if doPatCalo:
        addTcMET(process, 'TC')
    else:
        # FIXME: This is broken at the moment...
        #removeSpecificPATObjects(process, ["METs"], outputInProcess= out != None)
        #process.patDefaultSequen
        process.patDefaultSequence.remove(process.patMETCorrections)
        process.patDefaultSequence.remove(process.patMETs)
        del process.patMETCorrections
        del process.patMETs

    outputCommands.extend([
            "keep *_patMETs_*_*",
            "keep *_patMETsTC_*_*",
            "keep *_patMETsPF_*_*",
            "keep *_genMetTrue_*_*",
            ])

    # Muons
    setPatLeptonDefaults(process.patMuons, includePFCands)
    addPFMuonIsolation(process, process.patMuons)
    process.muonIsolationEmbeddingSequence = cms.Sequence()
    muons = tauEmbeddingCustomisations.addMuonIsolationEmbedding(process, process.muonIsolationEmbeddingSequence, "patMuons")
    process.patDefaultSequence.replace(process.selectedPatMuons,
                                       process.muonIsolationEmbeddingSequence*process.selectedPatMuons)
    process.selectedPatMuons.src = muons

    # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#Cosmic_ID
    process.cosmicCompatibility = cms.EDProducer("HPlusCosmicID",
        src=cms.InputTag("muons", "cosmicsVeto"),
        result = cms.string("cosmicCompatibility")
    )
    process.timeCompatibility = process.cosmicCompatibility.clone(result = 'timeCompatibility')
    process.backToBackCompatibility = process.cosmicCompatibility.clone(result = 'backToBackCompatibility')
    process.overlapCompatibility = process.cosmicCompatibility.clone(result = 'overlapCompatibility')
    sequence *= (
        process.cosmicCompatibility *
        process.timeCompatibility *
        process.backToBackCompatibility *
        process.overlapCompatibility
    )
    for name in ["cosmicCompatibility", 'timeCompatibility','backToBackCompatibility','overlapCompatibility']:
        setattr(process.patMuons.userData.userFloats, name, cms.InputTag(name))

    outputCommands.extend([
            "keep *_selectedPatMuons_*_*"
            ])

    # Electrons
    # In order to calculate the transverse impact parameter w.r.t.
    # beam spot instead of primary vertex, see
    setPatLeptonDefaults(process.patElectrons, includePFCands)
    addPFElectronIsolation(process, process.patElectrons)

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
        process.patTrigger.addL1Algos = cms.bool(False)
        process.patTrigger.l1ExtraMu = cms.InputTag("l1extraParticles")
        process.patTrigger.l1ExtraCenJet = cms.InputTag("l1extraParticles", "Central")
        process.patTrigger.l1ExtraTauJet = cms.InputTag("l1extraParticles", "Tau")
        process.patTrigger.l1ExtraForJet = cms.InputTag("l1extraParticles", "Forward")
        process.patTrigger.l1ExtraETM = cms.InputTag("l1extraParticles", "MET")
        process.patTrigger.l1ExtraHTM = cms.InputTag("l1extraParticles", "MHT")
        # This is the only way for now to reduce the size of PAT trigger objects
        # And yes, there is a typo in the parameter name
        process.patTrigger.exludeCollections = cms.vstring(
            "hltAntiKT5*",
            "hltBLifetime*",
            "hltBSoft*",
            "hltCleanEle*",
            "hltHITIPT*",
            "hltIsolPixelTrack*",
            "hltJet*",
            "hltL1HLTDouble*",
            "hltL1IsoRecoEcal*",
            "hltL1NonIsoRecoEcal*",
            #"hltL2Muon*",
            #"hltL3Muon*",
            #"hltMuTrack*",
            "hltPixel*",
            "hltRecoEcal*",
        )


        # Keep StandAlone trigger objects for enabling trigger
        # matching in the analysis phase with PAT tools
        outputCommands.extend(patTriggerStandAloneEventContent)
        outputCommands.extend([
                "keep patTriggerAlgorithms_patTrigger_*_*", # for L1
                "keep patTriggerConditions_patTrigger_*_*",
                ])

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

    if calculateEventCleaning:
        # Event cleaning steps which require pat objects
        # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#Tracking_failure_filter
        process.load('SandBox.Skims.trackingFailureFilter_cfi')
        process.trackingFailureFilter.taggingMode = True
        process.trackingFailureFilter.JetSource = "selectedPatJetsAK5PF"
        process.trackingFailureFilter.VertexSource = "goodPrimaryVertices"
        sequence *= process.trackingFailureFilter

    # Tau+HLT matching
    if doTauHLTMatching:
        sequence *= HChTriggerMatching.addTauHLTMatching(process, matchingTauTrigger, matchingJetTrigger, outputCommands=outputCommands)
    # Muon+HLT matching
    if doMuonHLTMatching:
        (process.muonTriggerMatchingSequence, muonsWithTrigger) = HChTriggerMatching.addMuonTriggerMatching(process, muons=process.selectedPatMuons.src.value())
        process.selectedPatMuons.src = muonsWithTrigger
        process.patDefaultSequence.remove(process.selectedPatMuons)
        process.patDefaultSequence *= (
            process.muonTriggerMatchingSequence *
            process.selectedPatMuons
        )
        out.outputCommands.append("drop patTriggerObjectStandAlonesedmAssociation_*_*_*")

    # Add the end sequence (to be able to add possible skim sequence between other pat sequences and it
    sequence *= process.plainPatEndSequence

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
        import RecoTauTag.RecoTau.CaloRecoTauDiscriminationForChargedHiggs_cfi as HChCaloTauDiscriminators

        tauAlgos = ["hpsPFTau", "hpsTancTaus"]
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
    if HChPFTauDiscriminators.HChTauIDSources[0] in tauTools.classicTauIDSources:
        print "addHChTauDiscriminators called already once, not adding them again"
        return

    for idSources in [tauTools.classicTauIDSources, tauTools.hpsTauIDSources, tauTools.hpsTancTauIDSources]:
        idSources.extend(HChPFTauDiscriminators.HChTauIDSources)
        idSources.extend(HChPFTauDiscriminatorsCont.HChTauIDSourcesCont)
    for idSources in [tauTools.classicPFTauIDSources, tauTools.hpsTauIDSources, tauTools.hpsTancTauIDSources]:
        idSources.extend(PFTauTestDiscrimination.TestTauIDSources)

def addHChTauDiscriminatorsPF2PAT(process, module, postfix):
    sequence = cms.Sequence()
    
    tauAlgos = ["pfTaus"+postfix]
    sequence *= HChPFTauDiscriminators.addPFTauDiscriminationSequenceForChargedHiggs(process, tauAlgos, postfix)
    sequence *= HChPFTauDiscriminatorsCont.addPFTauDiscriminationSequenceForChargedHiggsCont(process, tauAlgos, postfix)
    sequence *= PFTauTestDiscrimination.addPFTauTestDiscriminationSequence(process, tauAlgos, postfix)

    for idSources in [HChPFTauDiscriminators.HChTauIDSources,
                      HChPFTauDiscriminatorsCont.HChTauIDSourcesCont,
                      PFTauTestDiscrimination.TestTauIDSources]:
        for label, tag in idSources:
            setattr(module.tauIDSources, label, cms.InputTag("pfTaus"+postfix+tag+postfix))

    return sequence

def addTauRawDiscriminators(module, postfix):
    module.tauIDSources.byRawCombinedIsolationDeltaBetaCorr = cms.InputTag("hpsPFTauDiscriminationByRawCombinedIsolationDBSumPtCorr"+postfix)
    module.tauIDSources.byRawChargedIsolationDeltaBetaCorr = cms.InputTag("hpsPFTauDiscriminationByRawChargedIsolationDBSumPtCorr"+postfix)
    module.tauIDSources.byRawGammaIsolationDeltaBetaCorr = cms.InputTag("hpsPFTauDiscriminationByRawGammaIsolationDBSumPtCorr"+postfix)


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
def addPF2PAT(process, dataVersion, doPatTrigger=True, doHChTauDiscriminators=True, doPatMET=True, doPatElectronID=True,
              doBTagging=True, doPatTauIsoDeposits=False,
              doTauHLTMatching=True, matchingTauTrigger=None,
              doMuonHLTMatching=True,
              includePFCands=False,
              calculateEventCleaning=False
              ):
    postfix = "PFlow"

    # Hack to not to crash if something in PAT assumes process.out
    # hasOut = hasattr(process, "out")
    # outputCommands = []
    # outputCommandsBackup = []
    # if hasOut:
    #     outputCommandsBackup = process.out.outputCommands[:]
    # else:
    #     process.out = cms.OutputModule("PoolOutputModule",
    #         fileName = cms.untracked.string('dummy.root'),
    #         outputCommands = cms.untracked.vstring()
    #     )
    out = None
    outdict = process.outputModules_()
    outputCommands = []
    if outdict.has_key("out"):
        out = outdict["out"]
        outputCommands = out.outputCommands[:]

    sequence = cms.Sequence()
    endSequence = cms.Sequence()
    setattr(process, "patEndSequence"+postfix, endSequence)

    # Visible taus
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

    # PAT
    process.load("PhysicsTools.PatAlgos.patSequences_cff")

    ### First PF2PAT, without CHS
    jetCorrFactors = patJetCorrLevels(dataVersion, L1FastJet=True)
    jetCorrPayload = "AK5PF"
    pfTools.usePF2PAT(process, runPF2PAT=True, jetAlgo="AK5", jetCorrections=(jetCorrPayload, jetCorrFactors),
                      runOnMC=dataVersion.isMC(), postfix=postfix)
    outputCommands.extend([
#        "keep *_selectedPatPhotons%s_*_*" % postfix, # isolated photons are not (yet?) produced as part of PF2PAT
        'keep *_selectedPatElectrons%s_*_*' % postfix, 
        'keep *_selectedPatMuons%s_*_*' % postfix,
        'keep *_selectedPatJets%s*_*_*' % postfix,
        'keep *_selectedPatTaus%s_*_*' % postfix,
        'keep *_selectedPatPFParticles%s_*_*' % postfix,
        'keep *_selectedPatJets%s_pfCandidates_*' % postfix,
        'drop *_selectedPatJets%s_caloTowers_*' % postfix,
        'drop *_*JPT_pfCandidates_*',
        'drop *_*Calo_pfCandidates_*',
        'keep *_patMETs%s_*_*' % postfix,
        ])

    ### Disable CHS
    getattr(process, "pfPileUp"+postfix).Enable = False
    # According to JEC recipe (redundant for this non-CHS case, but
    # hopefully this confuses less)
    # https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#JetEnCorPFnoPU
    # There is a separate pfPileUpIso+postfix whith has this True for lepton isolation
    getattr(process, "pfPileUp"+postfix).checkClosestZVertex = False

    ### Muons
    # isolation step in PF2PAT, default is 0.15 (deltabeta corrected)
    #getattr(process, "pfIsolatedMuons"+postfix).isolationCut = 0.15
    setPatLeptonDefaults(getattr(process, "patMuons"+postfix), includePFCands)
    isoSeq = cms.Sequence()
    setattr(process, "muonIsolationEmbeddingSequence"+postfix, isoSeq)
    muons = tauEmbeddingCustomisations.addMuonIsolationEmbedding(process, isoSeq, "patMuons"+postfix, postfix=postfix)
    getattr(process, "patDefaultSequence"+postfix).replace(
        getattr(process, "selectedPatMuons"+postfix),
        isoSeq * getattr(process, "selectedPatMuons"+postfix))
    getattr(process, "selectedPatMuons"+postfix).src = muons

    # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#Cosmic_ID
    proto = cms.EDProducer("HPlusCosmicID",
        src=cms.InputTag("muons", "cosmicsVeto"),
        result = cms.string("cosmicCompatibility")
    )
    for name in ["cosmicCompatibility", 'timeCompatibility','backToBackCompatibility','overlapCompatibility']:
        m = proto.clone(result=name)
        sequence *= m
        setattr(process, name+postfix, m)
        setattr(process.patMuons.userData.userFloats, name, cms.InputTag(name+postfix))

    # HLT Matching
    if doMuonHLTMatching:
        (muHltSequence, muonsWithTrigger) = HChTriggerMatching.addMuonTriggerMatching(process, muons=getattr(process, "selectedPatMuons"+postfix).src.value(), postfix=postfix)
        setattr(process, "muonTriggerMatchingSequence"+postfix, muHltSequence)
        getattr(process, "selectedPatMuons"+postfix).src = muonsWithTrigger
        getattr(process, "patDefaultSequence"+postfix).remove(getattr(process, "selectedPatMuons"+postfix))
        seqTmp = getattr(process, "patDefaultSequence"+postfix) 
        seqTmp *= (
            muHltSequence *
            getattr(process, "selectedPatMuons"+postfix)
        )
        outputCommands.append("drop patTriggerObjectStandAlonesedmAssociation_*_*_*")

    ### Electrons
    # isolation step in PF2PAT, default is 0.2 (deltabeta corrected)
    #getattr(process, "pfIsolatedElectrons"+postfix).isolationCut = 0.2
    # I'm not sure if the electron ID will work as simply as this
    addPatElectronID(process, getattr(process, "patElectrons"+postfix), getattr(process, "patDefaultSequence"+postfix))


    ### Jets
    # Take all jets (we clean jets from tau later in the analysis)
    getattr(process, "pfNoTau"+postfix).enable = False

    # Don't embed PFCandidates
    setPatJetDefaults(getattr(process, "patJets"+postfix))

    # Calculate rho-neutral
    for particle in ["AllNeutralHadrons"]:
        m = getattr(process, "kt6PFJets"+postfix).clone(
            src = "pf"+particle+postfix
        )
        name = "kt6PFJets"+particle+postfix
        setattr(process, name, m)
        endSequence *= m
        outputCommands.append("keep *_%s_rho_*" % name)

    # Embed beta and betastar to pat::Jet
    betaPrototype = cms.EDProducer("HPlusPATJetViewBetaEmbedder",
        jetSrc = cms.InputTag("patJets"+postfix),
        vertexSrc = cms.InputTag("offlinePrimaryVertices"),
        embedPrefix = cms.string("")
    )
    m = betaPrototype.clone()
    name = "patJetsBetaEmbedded"+postfix
    setattr(process, name, m)
    getattr(process, "selectedPatJets"+postfix).src = name
    getattr(process, "patDefaultSequence"+postfix).replace(
        getattr(process, "selectedPatJets"+postfix),
        m * getattr(process, "selectedPatJets"+postfix)
    )

    # jet pre-selection
    getattr(process, "selectedPatJets"+postfix).cut = jetPreSelection



    ### Taus
    # Switch to HPS taus
    pfTools.adaptPFTaus(process, "hpsPFTau", postfix=postfix)
    # Disable the default PFTau selection in PF2PAT (byDecayMode + loose isolation)
    getattr(process, "pfTaus"+postfix).discriminators = []

    # Remove shrinking cone discrimination sequence as unnecessary
    getattr(process, "patDefaultSequence"+postfix).remove(getattr(process, "patShrinkingConePFTauDiscrimination"+postfix))

    # Set objects to embedded to pat::Tau
    setPatTauDefaults(getattr(process, "patTaus"+postfix), includePFCands)
    getattr(process, "selectedPatTaus"+postfix).cut = tauPreSelection

    # Produce HCh discriminators (could we really reduce the number of these?), and add them to pat::Tau producer
    if doHChTauDiscriminators:
        seq = addHChTauDiscriminatorsPF2PAT(process, getattr(process, "patTaus"+postfix), postfix)
        setattr(process, "hplusPatTauSequence"+postfix, seq)
        getattr(process, "patDefaultSequence"+postfix).replace(
            getattr(process, "patTaus"+postfix),
            seq * getattr(process, "patTaus"+postfix)
        )
        # Fix the flight path discriminator
        fixFlightPath(process, "pfTaus"+postfix, postfix)
        fixFlightPath(process, "pfTaus"+postfix, "Cont"+postfix)

    # Add the continuous isolation discriminators
    addTauRawDiscriminators(getattr(process, "patTaus"+postfix), postfix)

    # Remove iso deposits to save disk space
    if not doPatTauIsoDeposits:
        getattr(process, "patTaus"+postfix).isoDeposits = cms.PSet()

    # Trigger matching
    if doTauHLTMatching:
        endSequence *= HChTriggerMatching.addTauHLTMatching(process, matchingTauTrigger, collections=["patTaus"+postfix], postfix=postfix, outputCommands=outputCommands)



    ### MET
    # Produce Type 2 MET correction from unclustered PFCandidates
    m = cms.EDProducer("PFCandMETcorrInputProducer",
        src = cms.InputTag("pfNoJet"+postfix)
    )
    name = "pfCandMETcorr"+postfix
    setattr(process, name, m)
    endSequence *= m
    outputCommands.append("keep *_%s_*_*"%name)
    


    ### Trigger (as the last)
    if doPatTrigger:
        outMod= ''
        if out != None:
            outMod  = 'out'
        switchOnTrigger(process, hltProcess=dataVersion.getTriggerProcess(), outputModule="")
        process.patTrigger.addL1Algos = cms.bool(False)
        process.patTrigger.l1ExtraMu = cms.InputTag("l1extraParticles")
        process.patTrigger.l1ExtraCenJet = cms.InputTag("l1extraParticles", "Central")
        process.patTrigger.l1ExtraTauJet = cms.InputTag("l1extraParticles", "Tau")
        process.patTrigger.l1ExtraForJet = cms.InputTag("l1extraParticles", "Forward")
        process.patTrigger.l1ExtraETM = cms.InputTag("l1extraParticles", "MET")
        process.patTrigger.l1ExtraHTM = cms.InputTag("l1extraParticles", "MHT")
        # This is the only way for now to reduce the size of PAT trigger objects
        # And yes, there is a typo in the parameter name
        process.patTrigger.exludeCollections = cms.vstring(
            "hltAntiKT5*",
            "hltBLifetime*",
            "hltBSoft*",
            "hltCleanEle*",
            "hltHITIPT*",
            "hltIsolPixelTrack*",
            "hltJet*",
            "hltL1HLTDouble*",
            "hltL1IsoRecoEcal*",
            "hltL1NonIsoRecoEcal*",
            #"hltL2Muon*",
            #"hltL3Muon*",
            #"hltMuTrack*",
            "hltPixel*",
            "hltRecoEcal*",
            "hltEle*",
            "hltGetJetsfrom*",
            "hltMuTrackJpsi*",
        )


        # Keep StandAlone trigger objects for enabling trigger
        # matching in the analysis phase with PAT tools
        outputCommands.extend([
                "keep patTriggerAlgorithms_patTrigger_*_*", # for L1
                "keep patTriggerConditions_patTrigger_*_*",
                "keep patTriggerPaths_patTrigger_*_*",
                "keep patTriggerObjects_patTrigger_*_*",
                "keep patTriggerFilters_patTrigger_*_*",
                "keep patTriggerEvent_patTriggerEvent_*_*",
                ])

        sequence *= process.patDefaultSequenceTrigger
        sequence *= process.patDefaultSequenceTriggerEvent

    ### Other customisation
    # Tracks (mainly needed for muon efficiency tag&probe studies
    process.generalTracks20eta2p5 = cms.EDFilter("TrackSelector",
        src = cms.InputTag("generalTracks"),
        cut = cms.string("pt > 20 && abs(eta) < 2.5"),
        filter = cms.bool(False)
    )
    sequence *= process.generalTracks20eta2p5
    outputCommands.append("keep *_generalTracks20eta2p5_*_*")

    ### Remove unclustered PFParticles
    outputCommands.append("drop *_selectedPatPFParticles%s_*_*"%postfix)

    if calculateEventCleaning:
        # Event cleaning steps which require pat objects
        # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#Tracking_failure_filter
        process.load('SandBox.Skims.trackingFailureFilter_cfi')
        m = process.trackingFailureFilter.clone(
            taggingMode = True,
            JetSource = "selectedPatJetsPFlow",
            VertexSource = "goodPrimaryVertices",
        )
        setattr(process, "trackingFailureFilter"+postfix, m)
        endSequence *= m


    # Remove counting filters (what on earth are they for?)
    removeCounting(process, postfix)

    # Adjust output commands
    if out != None:
        out.outputCommands = outputCommands

    ### Construct the sequences
    sequence *= getattr(process, "patPF2PATSequence"+postfix)
    sequence *= endSequence
    return sequence

### OLD STUFF

    # Jet modifications
    # PhysicsTools/PatExamples/test/patTuple_42x_jec_cfg.py

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

    process.load("CommonTools.ParticleFlow.pfParticleSelection_cff")
    process.pfAllElectrons.src = "pfNoPileUp" # take electrons from all no-PU candidates instead of pfNoMuon (which apparently doesn't exist without PF2PAT)
    sequence *= process.pfParticleSelectionSequence


    # Create NoChs versions of particle selections, which take the
    # input from particleFlow instead of pfNoPileUp
    process.pfSortByTypeSequenceNoChs = cms.Sequence()
    for particle in ["NeutralHadrons", "ChargedHadrons", "Photons", "ChargedParticles", "NeutralHadronsAndPhotons"]:
        m = getattr(process, "pfAll"+particle).clone()
        m.src = "particleFlow"
        setattr(process, "pfAll"+particle+"NoChs", m)
        process.pfSortByTypeSequenceNoChs *= m
    process.pfParticleSelectionSequence *= process.pfSortByTypeSequenceNoChs

def addPFCandidatePtSums(process, sequence):
    if not hasattr(process, "pfParticleSelectionSequence"):
        raise Exception("addSelectedPFlowParticle() must be called before this one")

    prototype = cms.EDProducer("HPlusCandViewSumPtComputer",
        src = cms.InputTag("")
    )
    colls = ["pfAll" + p for p in ["NeutralHadrons", "ChargedHadrons", "Photons", "ChargedParticles", "NeutralHadronsAndPhotons",
                                   "ChargedHadronsNoChs", "ChargedParticlesNoChs"
                                   ]]
    colls.append("pfPileUpAllChargedParticles")
    for collection in colls:
        m = prototype.clone(src = collection)
        setattr(process, collection+"SumPt", m)
        sequence *= m

# From https://hypernews.cern.ch/HyperNews/CMS/get/muon/638.html
def addPFMuonIsolation(process, module):
    if not hasattr(process, "pfParticleSelectionSequence"):
        raise Exception("addSelectedPFlowParticle() must be called before this one")

    process.load("RecoMuon.MuonIsolation.muonPFIsolation_cff")
    process.patDefaultSequence.replace(module, process.muonPFIsolationSequence*module)

    ## Iso deposits
    # Set the muon source to 'muons' from 'muons1st'
    process.muPFIsoDepositCharged.src = "muons"
    process.muPFIsoDepositChargedAll.src = "muons"
    process.muPFIsoDepositNeutral.src = "muons"
    process.muPFIsoDepositGamma.src = "muons"
    process.muPFIsoDepositPU.src = "muons"

    # Without CHS (neutral hadrons and photons are not modified by CHS)
    process.muPFIsoDepositChargedNoChs = isoDepositReplace("muons", "pfAllChargedHadronsNoChs")
    process.muPFIsoDepositChargedAllNoChs = isoDepositReplace("muons", "pfAllChargedParticlesNoChs")
    process.muonPFIsolationDepositsSequence *= (
        process.muPFIsoDepositChargedNoChs *
        process.muPFIsoDepositChargedAllNoChs
    )

    ## Iso values
    # Without CHS (neutral hadrons and photons are not modified by CHS)
    for name in ["Charged", "ChargedAll"]:
        for cone in ["03", "04"]:
            m = getattr(process, "muPFIsoValue%s%s" % (name, cone)).clone()
            m.deposits[0].src = "muPFIsoDeposit%sNoChs" % name
            setattr(process, "muPFIsoValue%sNoChs%s" % (name, cone), m)
            process.muonPFIsolationSequence *= m

    ## Add iso deposits and values to the PATMuonProducer module

    # Example from PhysicsTools/PatAlgos/python/tools/pfTools.py
    # We can't use pfTools directly, because it's only for PF2PAT, but
    # we can get the PF isolation by adding these by ourselves
    module.isoDeposits = cms.PSet(
        pfChargedHadrons   = cms.InputTag("muPFIsoDepositCharged"),
        pfChargedAll       = cms.InputTag("muPFIsoDepositChargedAll"),
        pfPUChargedHadrons = cms.InputTag("muPFIsoDepositPU"),
        pfNeutralHadrons   = cms.InputTag("muPFIsoDepositNeutral"),
        pfPhotons          = cms.InputTag("muPFIsoDepositGamma"),
        user               = cms.VInputTag(
            cms.InputTag("muPFIsoDepositChargedNoChs"),
            cms.InputTag("muPFIsoDepositChargedAllNoChs")
        )
    )

    cone = "04"
    module.isolationValues = cms.PSet(
        pfChargedHadrons   = cms.InputTag("muPFIsoValueCharged"+cone),
        pfChargedAll       = cms.InputTag("muPFIsoValueChargedAll"+cone),
        pfPUChargedHadrons = cms.InputTag("muPFIsoValuePU"+cone),
        pfNeutralHadrons   = cms.InputTag("muPFIsoValueNeutral"+cone),
        pfPhotons          = cms.InputTag("muPFIsoValueGamma"+cone),
        user               = cms.VInputTag(
            cms.InputTag("muPFIsoValueChargedNoChs"+cone),
            cms.InputTag("muPFIsoValueChargedAllNoChs"+cone)
        )
    )

def addPFElectronIsolation(process, module):
    if not hasattr(process, "pfParticleSelectionSequence"):
        raise Exception("addSelectedPFlowParticle() must be called before this one")
    
    process.load("CommonTools.ParticleFlow.Isolation.pfElectronIsolation_cff")
    process.patDefaultSequence.replace(module, process.pfElectronIsolationSequence*module)

    ## Iso deposits
    # Set the electron source to 'gsfElectrons'
    process.elPFIsoDepositCharged.src = "gsfElectrons"
    process.elPFIsoDepositChargedAll.src = "gsfElectrons"
    process.elPFIsoDepositNeutral.src = "gsfElectrons"
    process.elPFIsoDepositGamma.src = "gsfElectrons"
    process.elPFIsoDepositPU.src = "gsfElectrons"

    # Without CHS (neutral hadrons and photons are not modified by CHS)
    process.elPFIsoDepositChargedNoChs = isoDepositReplace("gsfElectrons", "pfAllChargedHadronsNoChs")
    process.elPFIsoDepositChargedAllNoChs = isoDepositReplace("gsfElectrons", "pfAllChargedParticlesNoChs")
    process.electronPFIsolationDepositsSequence *= (
        process.elPFIsoDepositChargedNoChs *
        process.elPFIsoDepositChargedAllNoChs
    )

    ## Iso values
    # Without CHS (neutral hadrons and photons are not modified by CHS)
    for name in ["Charged", "ChargedAll"]:
        for cone in ["03", "04"]:
            m = getattr(process, "elPFIsoValue%s%s" % (name, cone)).clone()
            m.deposits[0].src = "elPFIsoDeposit%sNoChs" % name
            setattr(process, "elPFIsoValue%sNoChs%s" % (name, cone), m)
            process.pfElectronIsolationSequence *= m

    ## Add iso deposits and values to the PATElectronProducer module

    # Example from PhysicsTools/PatAlgos/python/tools/pfTools.py
    # We can't use pfTools directly, because it's only for PF2PAT, but
    # we can get the PF isolation by adding these by ourselves
    module.isoDeposits = cms.PSet(
        pfChargedHadrons   = cms.InputTag("elPFIsoDepositCharged"),
        pfChargedAll       = cms.InputTag("elPFIsoDepositChargedAll"),
        pfPUChargedHadrons = cms.InputTag("elPFIsoDepositPU"),
        pfNeutralHadrons   = cms.InputTag("elPFIsoDepositNeutral"),
        pfPhotons          = cms.InputTag("elPFIsoDepositGamma"),
        user               = cms.VInputTag(
            cms.InputTag("elPFIsoDepositChargedNoChs"),
            cms.InputTag("elPFIsoDepositChargedAllNoChs")
        )
    )

    cone = "04"
    module.isolationValues = cms.PSet(
        pfChargedHadrons   = cms.InputTag("elPFIsoValueCharged"+cone),
        pfChargedAll       = cms.InputTag("elPFIsoValueChargedAll"+cone),
        pfPUChargedHadrons = cms.InputTag("elPFIsoValuePU"+cone),
        pfNeutralHadrons   = cms.InputTag("elPFIsoValueNeutral"+cone),
        pfPhotons          = cms.InputTag("elPFIsoValueGamma"+cone),
        user               = cms.VInputTag(
            cms.InputTag("elPFIsoValueChargedNoChs"+cone),
            cms.InputTag("elPFIsoValueChargedAllNoChs"+cone)
        )
    )
