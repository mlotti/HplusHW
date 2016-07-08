import FWCore.ParameterSet.Config as cms

_patTauCollectionsDefault = [
    "patTaus"
#    "patTausShrinkingConePFTau",
#    "patTausHpsPFTau",
#    "patTausHpsTancPFTau",
#    "patTausCaloRecoTau"
    ] # add to the list new sources for patTauCollections, if necessary

tauPathLastFilter = {
    # 2011
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

    # 2012
    "HLT_LooseIsoPFTau35_Trk20_Prong1_v2":       "hltPFTau35TrackPt20LooseIsoProng2",
    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v2": "hltPFTau35TrackPt20LooseIsoProng2",
    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET75_v2": "hltPFTau35TrackPt20LooseIsoProng2",

    "HLT_LooseIsoPFTau35_Trk20_Prong1_v3":       "hltPFTau35TrackPt20LooseIsoProng2",
    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v3": "hltPFTau35TrackPt20LooseIsoProng2",
    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET75_v3": "hltPFTau35TrackPt20LooseIsoProng2",

    "HLT_LooseIsoPFTau35_Trk20_Prong1_v4":       "hltPFTau35TrackPt20LooseIsoProng2",
    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v4": "hltPFTau35TrackPt20LooseIsoProng2",
    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET75_v4": "hltPFTau35TrackPt20LooseIsoProng2",

    "HLT_LooseIsoPFTau35_Trk20_Prong1_v6":       "hltPFTau35TrackPt20LooseIsoProng2",
    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v6": "hltPFTau35TrackPt20LooseIsoProng2",
    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET75_v6": "hltPFTau35TrackPt20LooseIsoProng2",

    "HLT_LooseIsoPFTau35_Trk20_Prong1_v7":       "hltPFTau35TrackPt20LooseIsoProng2",
    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v7": "hltPFTau35TrackPt20LooseIsoProng2",
    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET75_v7": "hltPFTau35TrackPt20LooseIsoProng2",

    "HLT_LooseIsoPFTau35_Trk20_Prong1_v9":       "hltPFTau35TrackPt20LooseIsoProng2",
    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v9": "hltPFTau35TrackPt20LooseIsoProng2",
    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET75_v9": "hltPFTau35TrackPt20LooseIsoProng2",

    "HLT_LooseIsoPFTau35_Trk20_Prong1_v10":       "hltPFTau35TrackPt20LooseIsoProng2",
    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET70_v10": "hltPFTau35TrackPt20LooseIsoProng2",
    "HLT_LooseIsoPFTau35_Trk20_Prong1_MET75_v10": "hltPFTau35TrackPt20LooseIsoProng2",
    }

muPathLastFilter = {
    # 2011
    "HLT_Mu20_v1": "hltSingleMu20L3Filtered20",
    "HLT_Mu24_v2": "hltSingleMu24L3Filtered24",
    "HLT_Mu30_v3": "hltSingleMu30L3Filtered30",
    "HLT_Mu40_v1": "hltSingleMu40L3Filtered40",
    "HLT_Mu40_v2": "hltSingleMu40L3Filtered40",
    "HLT_Mu40_v3": "hltSingleMu40L3Filtered40",
    "HLT_Mu40_v5": "hltSingleMu40L2QualL3Filtered40",
    "HLT_Mu40_eta2p1_v1": "hltL3fL1sMu16Eta2p1L1f0L2f16QL3Filtered40",
    "HLT_Mu40_eta2p1_v4": "hltL3fL1sMu16Eta2p1L1f0L2f16QL3Filtered40",
    "HLT_Mu40_eta2p1_v5": "hltL3fL1sMu16Eta2p1L1f0L2f16QL3Filtered40",

    # 2012
    "HLT_Mu40_eta2p1_v9":  "hltL3fL1sMu16Eta2p1L1f0L2f16QL3Filtered40Q",
    "HLT_Mu40_eta2p1_v10": "hltL3fL1sMu16Eta2p1L1f0L2f16QL3Filtered40Q",
    "HLT_Mu40_eta2p1_v11": "hltL3fL1sMu16Eta2p1L1f0L2f16QL3Filtered40Q",
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

    print "Performing trigger matching for taus, tau collection %s, triggers %s" % (taus, ", ".join(trigger))

    module = cms.EDProducer("HPlusTauTriggerMatchSelector",
        src = cms.InputTag(taus),
        patTriggerEventSrc = cms.InputTag("patTriggerEvent"),
        deltaR = cms.double(0.4),
        filterNames = cms.vstring(matched),
        enabled = cms.bool(True)
    )
    return module

def setMuonTriggerMatchingInAnalysis(module, trigger, throw=True):
    if isinstance(trigger, basestring):
        trigger = [trigger]

    matched = []
    for path in trigger:
        if path in muPathLastFilter:
            filt = muPathLastFilter[path]
            matched.append(filt)
        elif throw:
            raise Exception("No filter found for path %s" % path)
    module.deltaR = cms.double(0.1)
    module.filterNames = cms.vstring(matched)
    module.enabled = cms.bool(True)

def createMuonTriggerMatchingInAnalysis(trigger, muons, throw=True):
    module = cms.EDProducer("HPlusMuonTriggerMatchSelector",
        src = cms.InputTag(muons),
        patTriggerEventSrc = cms.InputTag("patTriggerEvent"),
    )
    setMuonTriggerMatchingInAnalysis(module, trigger, throw)
    return module

def triggerMatchingInAnalysis(process, sequence, triggers, param):
    tauTriggers = []
    quadJetTriggers = []
    otherTriggers = []
    for trg in triggers:
        if trg in tauPathLastFilter:
            tauTriggers.append(trg)
        elif "QuadJet" in trg or "QuadPFJet" in trg:
            quadJetTriggers.append(trg)
        else:
            otherTriggers.append(trg)
    
    # Consistenty checks
    if len(otherTriggers) > 0:
        raise Exception("Requested triggers '%s', for which there is no trigger matching support at the moment." % ", ".join(otherTriggers))

    if len(tauTriggers) > 0 and len(quadJetTriggers) > 0:
        raise Exception("You should give only one type of triggers, got %d tau triggers and %d QuadJet triggers" % (len(tauTriggers), len(quadJetTriggers)))

    if len(quadJetTriggers) > 0:
        print "Got QuadJet triggers, for which there is no trigger matching implemented yet!"

    if len(tauTriggers) > 0:
        tauSrc = param.tauSelectionHPSTightTauBased.src.value()
        label = tauSrc.split(":")[0] + "TriggerMatched"
        module = createTauTriggerMatchingInAnalysis(triggers, tauSrc)
        sequence += module

        setattr(process, label, module)
        param.setAllTauSelectionSrc(label)

