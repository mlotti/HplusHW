import FWCore.ParameterSet.Config as cms

_patTauCollectionsDefault = [
#    "patTausShrinkingConePFTau",
    "patTausHpsPFTau",
    "patTausHpsTancPFTau",
#    "patTausCaloRecoTau"
    ] # add to the list new sources for patTauCollections, if necessary

tauPathLastFilter = {
    "HLT_IsoPFTau35_Trk20_MET45_v1": "hltFilterSingleIsoPFTau35Trk20MET45LeadTrack20MET45IsolationL1HLTMatched",
    "HLT_IsoPFTau35_Trk20_MET45_v2": "hltFilterSingleIsoPFTau35Trk20MET45LeadTrack20MET45IsolationL1HLTMatched",
    "HLT_IsoPFTau35_Trk20_MET45_v4": "hltFilterSingleIsoPFTau35Trk20MET45LeadTrack20MET45IsolationL1HLTMatched",
    "HLT_IsoPFTau35_Trk20_MET45_v6": "hltFilterSingleIsoPFTau35Trk20MET45LeadTrack20MET45IsolationL1HLTMatched",

    "HLT_IsoPFTau35_Trk20_v2":       "hltFilterSingleIsoPFTau35Trk20LeadTrack20IsolationL1HLTMatched",
    "HLT_IsoPFTau35_Trk20_v3":       "hltFilterSingleIsoPFTau35Trk20LeadTrack20IsolationL1HLTMatched",
    "HLT_IsoPFTau35_Trk20_v4":       "hltFilterSingleIsoPFTau35Trk20LeadTrack20IsolationL1HLTMatched",
    "HLT_IsoPFTau35_Trk20_v6":       "hltFilterSingleIsoPFTau35Trk20LeadTrack20IsolationL1HLTMatched",
    "HLT_MediumIsoPFTau35_Trk20_v1": "hltFilterSingleIsoPFTau35Trk20LeadTrack20IsolationL1HLTMatched",
    "HLT_MediumIsoPFTau35_Trk20_v5": "hltFilterSingleIsoPFTau35Trk20LeadTrack20IsolationL1HLTMatched",
    "HLT_MediumIsoPFTau35_Trk20_v6": "hltFilterSingleIsoPFTau35Trk20LeadTrack20IsolationL1HLTMatched",

    "HLT_IsoPFTau35_Trk20_MET60_v2":       "hltFilterSingleIsoPFTau35Trk20MET60LeadTrack20IsolationL1HLTMatched",
    "HLT_IsoPFTau35_Trk20_MET60_v3":       "hltFilterSingleIsoPFTau35Trk20MET60LeadTrack20IsolationL1HLTMatched",
    "HLT_IsoPFTau35_Trk20_MET60_v4":       "hltFilterSingleIsoPFTau35Trk20MET60LeadTrack20IsolationL1HLTMatched",
    "HLT_IsoPFTau35_Trk20_MET60_v6":       "hltFilterSingleIsoPFTau35Trk20MET60LeadTrack20IsolationL1HLTMatched",
    "HLT_MediumIsoPFTau35_Trk20_MET60_v1": "hltFilterSingleIsoPFTau35Trk20MET60LeadTrack20IsolationL1HLTMatched",
    "HLT_MediumIsoPFTau35_Trk20_MET60_v5": "hltFilterSingleIsoPFTau35Trk20MET60LeadTrack20IsolationL1HLTMatched",
    "HLT_MediumIsoPFTau35_Trk20_MET60_v6": "hltFilterSingleIsoPFTau35Trk20MET60LeadTrack20IsolationL1HLTMatched",

    "HLT_IsoPFTau45_Trk20_MET60_v2":       "hltFilterSingleIsoPFTau45Trk20MET60LeadTrack20IsolationL1HLTMatched",
    "HLT_IsoPFTau45_Trk20_MET60_v3":       "hltFilterSingleIsoPFTau45Trk20MET60LeadTrack20IsolationL1HLTMatched",
    "HLT_IsoPFTau45_Trk20_MET60_v4":       "hltFilterSingleIsoPFTau45Trk20MET60LeadTrack20IsolationL1HLTMatched",

    "HLT_IsoPFTau35_Trk20_MET70_v2":       "hltFilterSingleIsoPFTau35Trk20MET70LeadTrack20IsolationL1HLTMatched",
    "HLT_MediumIsoPFTau35_Trk20_MET70_v1": "hltFilterSingleIsoPFTau35Trk20MET70LeadTrack20IsolationL1HLTMatched",
    "HLT_MediumIsoPFTau35_Trk20_MET70_v5": "hltFilterSingleIsoPFTau35Trk20MET70LeadTrack20IsolationL1HLTMatched",
    "HLT_MediumIsoPFTau35_Trk20_MET70_v6": "hltFilterSingleIsoPFTau35Trk20MET70LeadTrack20IsolationL1HLTMatched",
    }

def addTauTriggerMatching(process, trigger, collections, postfix="", outputCommands=None, pathFilterMap=tauPathLastFilter, throw=True):
    seq = cms.Sequence()

    if isinstance(trigger, basestring):
        trigger = [trigger]

#    check = cms.EDAnalyzer("HPlusTriggerCheck",
#        src = cms.untracked.InputTag("patTriggerEvent"),
#        pathNames = cms.untracked.vstring(trigger)
#    )
#    setattr(process, postfix+"TriggerCheck", check)
#    seq *= check

    matched = []
    matched2 = []
    for path in trigger:
        if pathFilterMap != None and path in pathFilterMap:
            filt = pathFilterMap[path]
            matched.append("filter('%s')" % filt)
            matched2.append("!triggerObjectMatchesByFilter('%s').empty()" % filt)
        elif throw:
            raise Exception("No filter found for path %s" % path)
        else:
            matched.append("path('%s', 1, 0)" % path)
            matched2.append("!triggerObjectMatchesByPath('%s', 1, 0).empty()" % path)

    matcherPrototype = cms.EDProducer("PATTriggerMatcherDRLessByR",
        src                   = cms.InputTag("dummy"),
        matched               = cms.InputTag("patTrigger"),
        matchedCuts           = cms.string(" || ".join(matched)),
        maxDeltaR             = cms.double(0.4), # start with 0.4; patTrigger pages propose 0.1 or 0.2
        resolveAmbiguities    = cms.bool(True),
        resolveByMatchQuality = cms.bool(False)
    )

    selectorPrototype = cms.EDFilter("PATTauSelector",
        src = cms.InputTag("dummy"),
        cut = cms.string(" || ".join(matched2)),
    )

    for collection in collections:
        name = collection
        if "selectedPat" in name and hasattr(process, collection):
            name = getattr(process, collection).src.getModuleLabel()
        print "Matching collection %s to trigger(s) %s" % (name, ",".join(trigger))

        # DeltaR matching between the trigger object and the PAT objects
        matcher = matcherPrototype.clone(
            src = cms.InputTag(name)
        )
        matcherName = collection+"TriggerMatcher"+postfix
        setattr(process, matcherName, matcher)
        seq *= matcher

        # Embed the patTriggerObjectStandAloneedmAssociation to a tau collection
        embedder = cms.EDProducer("PATTriggerMatchTauEmbedder",
            src     = cms.InputTag(name),
            matches = cms.VInputTag(matcherName)
        )
        embedderName = collection+"TriggerEmbedder"+postfix
        setattr(process, embedderName, embedder)
        seq *= embedder

        # Select the PAT objects matching to the trigger object
        selector= selectorPrototype.clone(
            src = cms.InputTag(embedderName)
        )
        selectorName = collection+"TriggerMatched"+postfix
        setattr(process, selectorName, selector)
        seq *= selector

        if outputCommands:
            outputCommands.extend([
                    "drop *_%s_*_*" % matcherName,
                    "drop *_%s_*_*" % embedderName,
                    "keep patTaus_%s_*_*" % selectorName,
                    ])

    return seq

def addMuonTriggerMatching(process, muons="patMuons", postfix=""):
    # See MuonAnalysis/MuonAssociators/python/patMuonsWithTrigger_cff.py V01-15-01
    # http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/CMSSW/MuonAnalysis/MuonAssociators/python/patMuonsWithTrigger_cff.py?view=log

    matcherPrototype = cms.EDProducer("PATTriggerMatcherDRDPtLessByR",
        src     = cms.InputTag(muons),
        matched = cms.InputTag("patTrigger"),
        matchedCuts = cms.string(""),
        maxDPtRel = cms.double(0.5),
        maxDeltaR = cms.double(0.5),
        resolveAmbiguities    = cms.bool(True),
        resolveByMatchQuality = cms.bool(True)
    )
    muonMatchHLTL2 = matcherPrototype.clone(
        matchedCuts = cms.string('coll("hltL2MuonCandidates")'),
        maxDeltaR = 0.3, #maxDeltaR Changed accordingly to Zoltan tuning. It was: 1.2
        maxDPtRel = 10.0
    )
    setattr(process, "muonMatchHLTL2"+postfix, muonMatchHLTL2)
    muonMatchHLTL3 = matcherPrototype.clone(
        matchedCuts = cms.string('coll("hltL3MuonCandidates")'),
        maxDeltaR = 0.1, #maxDeltaR Changed accordingly to Zoltan tuning. It was: 0.5
        maxDPtRel = 10.0
    )
    setattr(process, "muonMatchHLTL3"+postfix, muonMatchHLTL3)

    patMuonsWithTrigger = cms.EDProducer("PATTriggerMatchMuonEmbedder",
        src     = cms.InputTag(muons),
        matches = cms.VInputTag(
            cms.InputTag("muonMatchHLTL2"+postfix),
            cms.InputTag("muonMatchHLTL3"+postfix),
        )
    )
    setattr(process, "patMuonsWithTrigger"+postfix, patMuonsWithTrigger)

    sequence = cms.Sequence(
        muonMatchHLTL2 *
        muonMatchHLTL3 *
        patMuonsWithTrigger
    )

    return (sequence, "patMuonsWithTrigger"+postfix)
    

################################################################################
# Do tau -> HLT tau trigger matching and tau -> HLT jet trigger matching
# Produces:
#   1) a patTauCollection of patTaus matched to the HLT tau trigger and
#   2) a copy of the same collection with the patTau matching to the HLT jet trigger
#      removed (needed to remove trigger bias in QCD backround measurement).
# Yes, I agree that this sounds (and is) a bit compicated :)
def addTauHLTMatching(process, tauTrigger, jetTrigger=None, collections=_patTauCollectionsDefault, outputCommands=None, postfix=""):
    if tauTrigger == None:
        raise Exception("Tau trigger missing for matching")

    seq = addTauTriggerMatching(process, tauTrigger, collections=collections, postfix=postfix, outputCommands=outputCommands)
    setattr(process, "tauTriggerMatchingSequence"+postfix, seq)

    if jetTrigger != None:
        raise Exception("Jet trigger matching for taus is not supported anymore")
    
    return seq


def createTauTriggerMatchingInAnalysis(trigger, taus, pathFilterMap=tauPathLastFilter, throw=True):
    if isinstance(trigger, basestring):
        trigger = [trigger]

    matched = []
    for path in trigger:
        if path in pathFilterMap:
            filt = pathFilterMap[path]
            matched.append(filt)
        elif throw:
            raise Exception("No filter found for path %s" % path)

    module = cms.EDProducer("HPlusTauTriggerMatchSelector",
        tauSrc = cms.InputTag(taus),
        patTriggerEventSrc = cms.InputTag("patTriggerEvent"),
        deltaR = cms.double(0.4),
        filterNames = cms.vstring(matched)
    )
    return module
