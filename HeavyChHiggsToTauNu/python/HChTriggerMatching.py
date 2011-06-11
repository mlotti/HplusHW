import FWCore.ParameterSet.Config as cms

_patTauCollectionsDefault = [
#    "selectedPatTausShrinkingConePFTau",
    "selectedPatTausHpsPFTau",
    "selectedPatTausHpsTancPFTau",
#    "selectedPatTausCaloRecoTau"
    ] # add to the list new sources for patTauCollections, if necessary

def addTauTriggerMatching(process, trigger, postfix="", collections=_patTauCollectionsDefault):
    seq = cms.Sequence()

    if isinstance(trigger, basestring):
        trigger = [trigger]

#    check = cms.EDAnalyzer("HPlusTriggerCheck",
#        src = cms.untracked.InputTag("patTriggerEvent"),
#        pathNames = cms.untracked.vstring(trigger)
#    )
#    setattr(process, postfix+"TriggerCheck", check)
#    seq *= check

    matcherPrototype = cms.EDProducer("PATTriggerMatcherDRLessByR",
        src                   = cms.InputTag("dummy"),
        matched               = cms.InputTag("patTrigger"),
        matchedCuts           = cms.string(" || ".join([ "path('%s', 1, 0)"%path for path in trigger ]) ),
        maxDeltaR             = cms.double(0.4), # start with 0.4; patTrigger pages propose 0.1 or 0.2
        resolveAmbiguities    = cms.bool(True),
        resolveByMatchQuality = cms.bool(False)
    )

    selectorPrototype = cms.EDFilter("PATTauSelector",
        src = cms.InputTag("dummy"),
        cut = cms.string(" || ".join(["!triggerObjectMatchesByPath('%s', 1, 0).empty()"%t for t in trigger])),
    )

    for collection in collections:
        name = collection
#        if "selectedPat" in name:
#            name = getattr(process, collection).src.getModuleLabel()
        print "Matching collection %s to trigger(s) %s" % (name, ",".join(trigger))

        # DeltaR matching between the trigger object and the PAT objects
        matcher = matcherPrototype.clone(
            src = cms.InputTag(name)
        )
        matcherName = collection+postfix+"TriggerMatcher"
        setattr(process, matcherName, matcher)
        seq *= matcher

        # Embed the patTriggerObjectStandAloneedmAssociation to a tau collection
        embedder = cms.EDProducer("PATTriggerMatchTauEmbedder",
            src     = cms.InputTag(name),
            matches = cms.VInputTag(matcherName)
        )
        embedderName = collection+postfix+"TriggerEmbedder"
        setattr(process, embedderName, embedder)
        seq *= embedder

        # Select the PAT objects matching to the trigger object
        selector= selectorPrototype.clone(
            src = cms.InputTag(embedderName)
        )
        selectorName = collection+postfix+"TriggerMatched"
        setattr(process, selectorName, selector)
        seq *= selector

    return seq
    

################################################################################
# Do tau -> HLT tau trigger matching and tau -> HLT jet trigger matching
# Produces:
#   1) a patTauCollection of patTaus matched to the HLT tau trigger and
#   2) a copy of the same collection with the patTau matching to the HLT jet trigger
#      removed (needed to remove trigger bias in QCD backround measurement).
# Yes, I agree that this sounds (and is) a bit compicated :)
def addTauHLTMatching(process, tauTrigger, jetTrigger=None, collections=_patTauCollectionsDefault, postfix=""):
    if tauTrigger == None:
        raise Exception("Tau trigger missing for matching")

    setattr(process, "tauTriggerMatchingSequence"+postfix, addTauTriggerMatching(process, tauTrigger, "Tau", collections=collections))
    setattr(process, "triggerMatchingSequence"+postfix, cms.Sequence(
            getattr(process, "tauTriggerMatchingSequence"+postfix)
    ))

    if jetTrigger != None:
        setattr(process, "jetTriggerMatchingSequence"+postfix, addTauTriggerMatching(process, jetTrigger, "Jet", collections=collections))
        seq = getattr(process, "triggerMatchingSequence"+postfix)
        seq *= getattr(process, "jetTriggerMatchingSequence"+postfix)

        ###########################################################################
        # Remove first tau matching to the jet trigger from the list
        # of tau -> HLT tau trigger matched patTaus
        for collection in _patTauCollectionsDefault:
            patJetTriggerCleanedTauTriggerMatchedTaus = cms.EDProducer("TauHLTMatchJetTriggerRemover",
                tausMatchedToTauTriggerSrc = cms.InputTag(collection+"TauTriggerMatched"),
                tausMatchedToJetTriggerSrc = cms.InputTag(collection+"JetTriggerMatched"),
            )
            patJetTriggerCleanedTauTriggerMatchedTausName = collection+"TauTriggerMatchedAndJetTriggerCleaned"+postfix
            setattr(process, patJetTriggerCleanedTauTriggerMatchedTausName, patJetTriggerCleanedTauTriggerMatchedTaus)
            seq = getattr(process, "triggerMatchingSequence"+postfix)
            seq *= patJetTriggerCleanedTauTriggerMatchedTaus
    
    out = None
    outdict = process.outputModules_()
    if outdict.has_key("out"):
        outdict["out"].outputCommands.extend([
            "keep patTaus_*TauTriggerMatched_*_*",
            "drop *_*TauTriggerMatcher_*_*",
            "drop *_*TauTriggerEmbedder_*_*",
            "drop patTaus_*JetTriggerMatched_*_*",
            "drop *_*JetTriggerMatcher_*_*",
            "drop *_*JetTriggerEmbedder_*_*",
            "keep *_*TauTriggerMatchedAndJetTriggerCleaned_*_*"
        ])

    return getattr(process, "triggerMatchingSequence"+postfix)
