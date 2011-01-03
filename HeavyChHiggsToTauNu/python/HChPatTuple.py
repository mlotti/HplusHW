import FWCore.ParameterSet.Config as cms
import copy

from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection, switchJetCollection
from PhysicsTools.PatAlgos.tools.cmsswVersionTools import run36xOn35xInput
from PhysicsTools.PatAlgos.tools.tauTools import addTauCollection, classicTauIDSources, classicPFTauIDSources, tancTauIDSources
from PhysicsTools.PatAlgos.tools.metTools import addTcMET, addPfMET
from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
from PhysicsTools.PatAlgos.tools.coreTools import removeMCMatching, restrictInputToAOD, removeSpecificPATObjects, removeCleaning
import RecoTauTag.RecoTau.PFRecoTauDiscriminationForChargedHiggs_cfi as HChPFTauDiscriminators
import HiggsAnalysis.HeavyChHiggsToTauNu.PFRecoTauDiscriminationForChargedHiggsContinuous_cfi as HChPFTauDiscriminatorsCont
import RecoTauTag.RecoTau.CaloRecoTauDiscriminationForChargedHiggs_cfi as HChCaloTauDiscriminators
import HiggsAnalysis.HeavyChHiggsToTauNu.CaloRecoTauDiscriminationForChargedHiggsContinuous_cfi as HChCaloTauDiscriminatorsCont
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTaus_cfi as HChTaus
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTausCont_cfi as HChTausCont
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTausTest_cfi as HChTausTest
import HiggsAnalysis.HeavyChHiggsToTauNu.PFTauTestDiscrimination_cfi as PFTauTestDiscrimination

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
        process.load("RecoTauTag.Configuration.RecoTCTauTag_cff")
        HChPFTauDiscriminators.addPFTauDiscriminationSequenceForChargedHiggs(process)
        HChPFTauDiscriminatorsCont.addPFTauDiscriminationSequenceForChargedHiggsCont(process)
	PFTauTestDiscrimination.addPFTauTestDiscriminationSequence(process)

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
        
        process.load("RecoTauTag.Configuration.HPSPFTaus_cfi")

        process.hplusPatTauSequence = cms.Sequence(
            process.tautagging *
            process.PFTauDiscriminationSequenceForChargedHiggs *
            process.PFTauDiscriminationSequenceForChargedHiggsCont *
	    process.PFTauTestDiscriminationSequence *
            process.produceAndDiscriminateHPSPFTaus *
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
    if dataVersion.isData():
        removeMCMatching(process, ["All"], outputInProcess= out!=None)

    # Jets
    corrections = ["L2Relative", "L3Absolute"]
    if dataVersion.isData():
        corrections.append("L2L3Residual")

    # Set defaults
    process.patJets.jetSource = cms.InputTag("ak5CaloJets")
    process.patJets.trackAssociationSource = cms.InputTag("ak5JetTracksAssociatorAtVertex")
    process.patJets.addJetID = True
    process.patJets.embedCaloTowers = False
    process.patJets.embedPFCandidates = False
    process.patJets.addTagInfos = False

    if doPatCalo:
        # Add JPT jets
        addJetCollection(process, cms.InputTag('JetPlusTrackZSPCorJetAntiKt5'),
                         'AK5', 'JPT',
                         doJTA        = True,
                         doBTagging   = doBTagging,
                         jetCorrLabel = ('AK5JPT', cms.vstring(corrections)),
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
                         jetCorrLabel = ('AK5PF', cms.vstring(corrections)),
                         doType1MET   = False,
                         doL1Cleaning = False,
                         doL1Counters = True,
                         genJetCollection = cms.InputTag("ak5GenJets"),
                         doJetID      = True
        )

        # Use switchJetCollection to get the correct JEC for calo jets
        switchJetCollection(process, cms.InputTag('ak5CaloJets'),
                            doJTA        = True,
                            doBTagging   = doBTagging,
                            jetCorrLabel = ('AK5Calo', cms.vstring(corrections)),
                            doType1MET   = False,
                            genJetCollection = cms.InputTag("ak5GenJets"),
                            doJetID      = True
        )
    else:
        switchJetCollection(process, cms.InputTag('ak5PFJets'),
                            doJTA        = True,
                            doBTagging   = doBTagging,
                            jetCorrLabel = ('AK5PF', cms.vstring(corrections)),
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
        seq *= addTauHLTMatching(process, matchingTauTrigger, matchingJetTrigger)

    return seq
    



################################################################################
# Do tau -> HLT tau trigger matching and tau -> HLT jet trigger matching
# Produces:
#   1) a patTauCollection of patTaus matched to the HLT tau trigger and
#   2) a copy of the same collection with the patTau matching to the HLT jet trigger
#      removed (needed to remove trigger bias in QCD backround measurement).
# Yes, I agree that this sounds (and is) a bit compicated :)
def addTauHLTMatching(process, tauTrigger, jetTrigger):
    if tauTrigger == None:
        raise Exception("Tau trigger missing for matching")
    if jetTrigger == None:
        raise Exception("Jet trigger missing for matching")

    patTauCollectionList = [
        "selectedPatTausShrinkingConePFTau",
        "selectedPatTausHpsPFTau",
        "selectedPatTausCaloRecoTau"
        ] # add to the list new sources for patTauCollections, if necessary

    patTauTriggerMatchHplusProtoType = cms.EDProducer("PATTriggerMatcherDRLessByR",
        src                   = cms.InputTag("dummy"),
        matched               = cms.InputTag("patTrigger"),
        andOr                 = cms.bool(False),
        filterIdsEnum         = cms.vstring('*'),
        filterIds             = cms.vint32(0),
        filterLabels          = cms.vstring('*'),
        pathNames             = cms.vstring(tauTrigger),
        collectionTags        = cms.vstring('*'),
        maxDeltaR             = cms.double(0.4), # start with 0.4; patTrigger pages propose 0.1 or 0.2
        resolveAmbiguities    = cms.bool(True),
        resolveByMatchQuality = cms.bool(False)
    )

    patTauEmptyCleanerProtoType = cms.EDFilter("PATTauSelector",
        src = cms.InputTag("dummy"),
        cut = cms.string("!triggerObjectMatchesByPath('"+tauTrigger+"').empty()"),
    )

    process.triggerMatchingSequence = cms.Sequence()

    for patTauCollection in patTauCollectionList:
        ###########################################################################
        # Tau -> HLT tau trigger matching
        print "Matching patTauCollection "+patTauCollection+" to tau trigger "+tauTrigger
        # create DeltaR matcher of trigger objects to a tau collection
        patTauTriggerMatcher = patTauTriggerMatchHplusProtoType.clone(
            src = cms.InputTag(patTauCollection)
        )
        patTauTriggerMatcherName = patTauCollection+"TauTriggerMatcher"
        setattr(process, patTauTriggerMatcherName, patTauTriggerMatcher)
        process.triggerMatchingSequence *= patTauTriggerMatcher
    
        # produce patTriggerObjectStandAloneedmAssociation object
        patTauTriggerEvent = process.patTriggerEvent.clone(
            patTriggerMatches = cms.VInputTag(patTauTriggerMatcherName)
        )
        patTauTriggerEventName = patTauCollection+"TauTriggerEvent"
        setattr(process, patTauTriggerEventName, patTauTriggerEvent)
        process.triggerMatchingSequence *= patTauTriggerEvent
    
        # embed the patTriggerObjectStandAloneedmAssociation to a tau collection
        patTauTriggerEmbedder = cms.EDProducer("PATTriggerMatchTauEmbedder",
            src     = cms.InputTag(patTauCollection),
            matches = cms.VInputTag(patTauTriggerMatcherName)
        )
        patTauTriggerEmbedderName = patTauCollection+"TauTriggerEmbedder"
        setattr(process, patTauTriggerEmbedderName, patTauTriggerEmbedder)
        process.triggerMatchingSequence *= patTauTriggerEmbedder
    
        # clean empty pat taus from the embedded tau collection
        patTausTriggerMatchedAndCleaned = patTauEmptyCleanerProtoType.clone(
            src = cms.InputTag(patTauTriggerEmbedderName)
        )
        patTausTriggerMatchedAndCleanedName = patTauCollection+"TauTriggerMatched"
        setattr(process, patTausTriggerMatchedAndCleanedName, patTausTriggerMatchedAndCleaned)
        process.triggerMatchingSequence *= patTausTriggerMatchedAndCleaned
    
        ###########################################################################
        # Tau -> HLT jet trigger matching
        # (needed for removing the tau candidate matching to jet trigger in QCD bkg measurement)
        print "Matching patTauCollection "+patTauCollection+" to jet trigger "+jetTrigger
        # create DeltaR matcher of trigger objects
        patJetTriggerMatcher = patTauTriggerMatcher.clone(
            pathNames = cms.vstring(jetTrigger)
        )
        patJetTriggerMatcherName = patTauCollection+"JetTriggerMatcher"
        setattr(process, patJetTriggerMatcherName, patJetTriggerMatcher)
        process.triggerMatchingSequence *= patJetTriggerMatcher
    
        # produce patTriggerObjectStandAloneedmAssociation object
        patJetTriggerEvent = process.patTriggerEvent.clone(
            patTriggerMatches = cms.VInputTag(patJetTriggerMatcherName)
        )
        patJetTriggerEventName = patTauCollection+"JetTriggerEvent"
        setattr(process, patJetTriggerEventName, patJetTriggerEvent)
        process.triggerMatchingSequence *= patJetTriggerEvent
    
        # embed the patTriggerObjectStandAloneedmAssociation to a tau collection
        patJetTriggerEmbedder = cms.EDProducer("PATTriggerMatchTauEmbedder",
            src     = cms.InputTag(patTauCollection),
            matches = cms.VInputTag(patJetTriggerMatcherName)
        )
        patJetTriggerEmbedderName = patTauCollection+"JetTriggerEmbedder"
        setattr(process, patJetTriggerEmbedderName, patJetTriggerEmbedder)
        process.triggerMatchingSequence *= patJetTriggerEmbedder
    
        # clean empty pat taus from the embedded tau collection
        patJetTriggerMatchedAndCleaned = patTauEmptyCleanerProtoType.clone(
            src = cms.InputTag(patJetTriggerEmbedderName)
        )
        patJetTriggerMatchedAndCleanedName = patTauCollection+"JetTriggerMatched"
        setattr(process, patJetTriggerMatchedAndCleanedName, patJetTriggerMatchedAndCleaned)
        process.triggerMatchingSequence *= patJetTriggerMatchedAndCleaned
    
        ###########################################################################
        # Remove first tau matching to the jet trigger from the list
        # of tau -> HLT tau trigger matched patTaus
        patJetTriggerCleanedTauTriggerMatchedTaus = cms.EDProducer("TauHLTMatchJetTriggerRemover",
            tausMatchedToTauTriggerSrc = cms.InputTag(patTausTriggerMatchedAndCleanedName),
            tausMatchedToJetTriggerSrc = cms.InputTag(patJetTriggerMatchedAndCleanedName),
        )
        patJetTriggerCleanedTauTriggerMatchedTausName = patTauCollection+"TauTriggerMatchedAndJetTriggerCleaned"
        setattr(process, patJetTriggerCleanedTauTriggerMatchedTausName, patJetTriggerCleanedTauTriggerMatchedTaus)
        process.triggerMatchingSequence *= patJetTriggerCleanedTauTriggerMatchedTaus
    
    out = None
    outdict = process.outputModules_()
    if outdict.has_key("out"):
        outdict["out"].outputCommands.extend([
            "keep patTaus_*TauTriggerMatched_*_*",
            "drop *_*TauTriggerMatcher_*_*",
            "drop *_*TauTriggerEvent_*_*",
            "drop *_*TauTriggerEmbedder_*_*",
            "drop patTaus_*JetTriggerMatched_*_*",
            "drop *_*JetTriggerMatcher_*_*",
            "drop *_*JetTriggerEvent_*_*",
            "drop *_*JetTriggerEmbedder_*_*",
            "keep *_*TauTriggerMatchedAndJetTriggerCleaned_*_*"
        ])

    return process.triggerMatchingSequence
