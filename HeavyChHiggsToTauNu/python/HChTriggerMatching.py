import FWCore.ParameterSet.Config as cms

_patTauCollectionsDefault = [
    "selectedPatTausShrinkingConePFTau",
    "selectedPatTausHpsPFTau",
    "selectedPatTausCaloRecoTau"
    ] # add to the list new sources for patTauCollections, if necessary

def addTauTriggerMatching(process, trigger, postfix="", collections=_patTauCollectionsDefault):
    seq = cms.Sequence()

    if isinstance(trigger, basestring):
        trigger = [trigger]

    matcherPrototype = cms.EDProducer("PATTriggerMatcherDRLessByR",
        src                   = cms.InputTag("dummy"),
        matched               = cms.InputTag("patTrigger"),
        andOr                 = cms.bool(False),
        filterIdsEnum         = cms.vstring('*'),
        filterIds             = cms.vint32(0),
        filterLabels          = cms.vstring('*'),
        pathNames             = cms.vstring(trigger),
        collectionTags        = cms.vstring('*'),
        maxDeltaR             = cms.double(0.4), # start with 0.4; patTrigger pages propose 0.1 or 0.2
        resolveAmbiguities    = cms.bool(True),
        resolveByMatchQuality = cms.bool(False)
    )

    selectorPrototype = cms.EDFilter("PATTauSelector",
        src = cms.InputTag("dummy"),
        cut = cms.string(" || ".join(["!triggerObjectMatchesByPath('%s').empty()"%t for t in trigger])),
    )

    for collection in collections:
        print "Matching collection %s to trigger(s) %s" % (collection, ",".join(trigger))

        # DeltaR matching between the trigger object and the PAT objects
        matcher = matcherPrototype.clone(
            src = cms.InputTag(collection)
        )
        matcherName = collection+postfix+"TriggerMatcher"
        setattr(process, matcherName, matcher)
        seq *= matcher

        # Embed the patTriggerObjectStandAloneedmAssociation to a tau collection
        embedder = cms.EDProducer("PATTriggerMatchTauEmbedder",
            src     = cms.InputTag(collection),
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
    

