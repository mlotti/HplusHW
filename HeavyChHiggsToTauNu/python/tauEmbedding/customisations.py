import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.HChTools as HChTools
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as HChSignalAnalysisParameters

tauEmbeddingMuons = "tauEmbeddingMuons"

def customiseParamForTauEmbedding(param, options, dataVersion):
    # Change the triggers to muon
    param.trigger.triggers = [
        "HLT_Mu9",
        "HLT_Mu15_v1",
        "HLT_Mu20_v1",
        ]
    param.trigger.hltMetCut = -1 # disable
#    param.trigger.caloMetSelection.src = cms.untracked.InputTag("met", "", dataVersion.getRecoProcess())
    param.trigger.caloMetSelection.src = "caloMetSum"
    param.trigger.caloMetSelection.metEmulationCut = -1#60.0

    tauTrigger = options.tauEmbeddingTauTrigger
    if len(tauTrigger) == 0:
        tauTrigger = "HLT_IsoPFTau35_Trk20_EPS"

    param.trigger.selectionType = "disabled"
    param.triggerEfficiencyScaleFactor.mode = "disabled"

    # Use PatJets and PFMet directly
    param.changeJetCollection(moduleLabel="selectedPatJets") # these are really AK5PF
    param.MET.rawSrc = "pfMet" # no PAT object at the moment

    # Use the muons where the original muon is removed in global muon veto
    param.GlobalMuonVeto.MuonCollectionName.setModuleLabel("selectedPatMuonsEmbeddingMuonCleaned")

    # Use the taus matched to the original muon in tau selections
    postfix = "TauEmbeddingMuonMatched"
    #param.setAllTauSelectionSrcSelectedPatTaus()
    def replaceTauSrc(mod):
        mod.src.setModuleLabel(mod.src.getModuleLabel().replace("TauTriggerMatched", postfix))
    param.forEachTauSelection(replaceTauSrc)

    # Remove TCTau
    i = param.tauSelections.index(param.tauSelectionCaloTauCutBased)
    print "Removing %s from the list of tau selections" % param.tauSelectionNames[i]
    del param.tauSelections[i]
    del param.tauSelectionNames[i]

    # Set the analyzer
    param.tree.tauEmbeddingInput = cms.untracked.bool(True)
    param.tree.tauEmbeddingMuonSource = cms.untracked.InputTag(tauEmbeddingMuons)
    param.tree.tauEmbeddingMetSource = cms.untracked.InputTag("pfMet", "", dataVersion.getRecoProcess())
    param.tree.tauEmbeddingCaloMetSource = cms.untracked.InputTag("caloMetSum")

def setCaloMetSum(process, sequence, options, dataVersion):
    name = "caloMetSum"
    m = cms.EDProducer("HPlusCaloMETSumProducer",
                       src = cms.VInputTag(cms.InputTag(options.tauEmbeddingCaloMet, "", dataVersion.getRecoProcess()),
                                           cms.InputTag(options.tauEmbeddingCaloMet, "", "EMBEDDING")
                                           )
                       )
    setattr(process, name, m)
    sequence *= m

def addMuonIsolationEmbeddingForSignalAnalysis(process, sequence, **kwargs):
    global tauEmbeddingMuons
    muons = addMuonIsolationEmbedding(process, sequence, tauEmbeddingMuons, **kwargs)
    tauEmbeddingMuons = muons

def addMuonIsolationEmbedding(process, sequence, muons, pfcands="particleFlow", primaryVertex="firstPrimaryVertex", postfix=""):
    import HiggsAnalysis.HeavyChHiggsToTauNu.HChTools as HChTools
    import RecoTauTag.Configuration.RecoPFTauTag_cff as RecoPFTauTag

    tight = cms.EDProducer("HPlusPATMuonViewTauLikeIsolationEmbedder",
        candSrc = cms.InputTag(muons),
        pfCandSrc = cms.InputTag(pfcands),
        vertexSrc = cms.InputTag(primaryVertex),
        embedPrefix = cms.string("byTight"+postfix),
        signalCone = cms.double(0.1),
        isolationCone = cms.double(0.5)
    )
    name = "patMuonsWithTight"+postfix
    setattr(process, name, tight)

    medium = tight.clone(
        candSrc = name,
        embedPrefix = "byMedium"+postfix,
    )
    name = "patMuonsWithMedium"+postfix
    setattr(process, name, medium)

    loose = tight.clone(
        candSrc = name,
        embedPrefix = "byLoose"+postfix,
    )
    name = "patMuonsWithLoose"+postfix
    setattr(process, name, loose)

    vloose = tight.clone(
        candSrc = name,
        embedPrefix = "byVLoose"+postfix,
    )
    name = "patMuonsWithVLoose"+postfix
    setattr(process, name, vloose)

    tight.qualityCuts = RecoPFTauTag.hpsPFTauDiscriminationByTightIsolation.qualityCuts.clone()
    medium.qualityCuts = RecoPFTauTag.hpsPFTauDiscriminationByMediumIsolation.qualityCuts.clone()
    loose.qualityCuts = RecoPFTauTag.hpsPFTauDiscriminationByLooseIsolation.qualityCuts.clone()
    vloose.qualityCuts = RecoPFTauTag.hpsPFTauDiscriminationByVLooseIsolation.qualityCuts.clone()
    #HChTools.insertPSetContentsTo(RecoPFTauTag.hpsPFTauDiscriminationByTightIsolation.qualityCuts.isolationQualityCuts, tight)
    #HChTools.insertPSetContentsTo(RecoPFTauTag.hpsPFTauDiscriminationByMediumIsolation.qualityCuts.isolationQualityCuts, medium)
    #HChTools.insertPSetContentsTo(RecoPFTauTag.hpsPFTauDiscriminationByLooseIsolation.qualityCuts.isolationQualityCuts, loose)
    #HChTools.insertPSetContentsTo(RecoPFTauTag.hpsPFTauDiscriminationByVLooseIsolation.qualityCuts.isolationQualityCuts, vloose)

    sequence *= (tight * medium * loose *vloose)

    #######################
    m = tight.clone(
        candSrc = name,
        embedPrefix = "byTightSc015"+postfix,
        signalCone = 0.15
    )
    name = "patMuonsWithTightSc015"
    setattr(process, name, m)
    sequence *= m

    m = tight.clone(
        candSrc = name,
        embedPrefix = "byTightSc02"+postfix,
        signalCone = 0.2
    )
    name = "patMuonsWithTightSc02"
    setattr(process, name, m)
    sequence *= m

    m = tight.clone(
        candSrc = name,
        embedPrefix = "byTightIc04"+postfix,
        isolationCone = 0.4
    )
    name = "patMuonsWithTightIc04"
    setattr(process, name, m)
    sequence *= m

    m = m.clone(
        candSrc = name,
        embedPrefix = "byTightSc015Ic04"+postfix,
        signalCone = 0.15
    )
    name = "patMuonsWithTightSc015Ic04"
    setattr(process, name, m)
    sequence *= m

    m = m.clone(
        candSrc = name,
        embedPrefix = "byTightSc02Ic04"+postfix,
        signalCone = 0.2
    )
    name = "patMuonsWithTightSc02Ic04"
    setattr(process, name, m)
    sequence *= m

    #######################
    m = tight.clone(
        candSrc = name,
        embedPrefix = "byTightSc0"+postfix,
        signalCone = 0.01
    )
    name = "patMuonsWithTightSc0"+postfix
    setattr(process, name, m)
    sequence *= m

    m = m.clone(
        candSrc = name,
        embedPrefix = "byTightSc0Ic04"+postfix,
        isolationCone = 0.4,
    )
    name = "patMuonsWithTightSc0Ic04"+postfix
    setattr(process, name, m)
    sequence *= m

    m = m.clone(
        candSrc = name,
        embedPrefix = "byTightSc0Ic04Noq",
        #minTrackHits = 0,
        #minTrackPt = 0.0,
        #maxTrackChi2 = 9999.,
        #minTrackPixelHits = 0,
        #minGammaEt = 0.0,
        #maxDeltaZ = 9999.,
    )
    name = "patMuonsWithTightSc0Ic04Noq"+postfix
    setattr(process, name, m)
    sequence *= m

    #######################
    gen = cms.EDProducer("HPlusPATMuonViewGenEmbedder",
        candSrc = cms.InputTag(name),
        genParticleSrc = cms.InputTag("genParticles"),
        embedPrefix = cms.string("gen"),
        maxDR = cms.double(0.5),
        pdgId = cms.uint32(13)
    )
    name = "patMuonsWithGen"
    setattr(process, name, gen)
    sequence *= gen

    import PhysicsTools.PatAlgos.selectionLayer1.muonSelector_cfi as muonSelector
    m = muonSelector.selectedPatMuons.clone(
        src = name
    )
    name = "selectedPatMuonsWithIso"+postfix
    setattr(process, name, m)
    sequence *= m

    return name

def addFinalMuonSelection(process, sequence, param, enableIsolation=True, prefix="muonFinalSelection"):
    counters = []

    cname = prefix+"AllEvents"
    m = cms.EDProducer("EventCountProducer")
    setattr(process, cname, m)
    sequence *= m
    counters.append(cname)

    if enableIsolation:
#        counters.extend(addMuonRelativeIsolation(process, sequence, prefix=prefix+"Isolation", cut=0.1))
        import muonAnalysis
        counters.extend(addMuonIsolation(process, sequence, "muonSelectionIsolation", "(%s)==0" % muonAnalysis.isolations["tauTightIc04Iso"]))
    counters.extend(addMuonVeto(process, sequence, param, prefix+"MuonVeto"))
    counters.extend(addElectronVeto(process, sequence, param, prefix+"ElectronVeto"))
    counters.extend(addMuonJetSelection(process, sequence, prefix+"JetSelection"))

    return counters

def addMuonRelativeIsolation(process, sequence, prefix="muonSelectionIsolation", cut=0.1):
    return addMuonIsolation(process, sequence, prefix, "(isolationR03().emEt+isolationR03().hadEt+isolationR03().sumPt)/pt() < %f" % cut)

def addMuonJetSelection(process, sequence, prefix="muonSelectionJetSelection"):
    selector = prefix+"GoodJets"
    filter = prefix+"Filter"
    counter = prefix

    import muonSelectionPF_cff as muonSelection
    from PhysicsTools.PatAlgos.cleaningLayer1.jetCleaner_cfi import cleanPatJets
    m1 = cleanPatJets.clone(
        src = "selectedPatJets",
        preselection = muonSelection.goodJets.cut,
            checkOverlaps = cms.PSet(
                muons = cms.PSet(
                    src                 = cms.InputTag(tauEmbeddingMuons),
                    algorithm           = cms.string("byDeltaR"),
                    preselection        = cms.string(""),
                    deltaR              = cms.double(0.1),
                    checkRecoComponents = cms.bool(False),
                    pairCut             = cms.string(""),
                    requireNoOverlaps   = cms.bool(True),
                )
            )
        )
    m2 = muonSelection.goodJetFilter.clone(src=selector, minNumber=3)
    m3 = cms.EDProducer("EventCountProducer")

    setattr(process, selector, m1)
    setattr(process, filter, m2)
    setattr(process, counter, m3)

    sequence *= (m1 * m2 * m3)

    return [counter]


def addMuonVeto(process, sequence, param, prefix="muonSelectionMuonVeto"):
    filter = prefix+"Filter"
    counter = prefix

    m1 = cms.EDFilter("HPlusGlobalMuonVetoFilter",
        vertexSrc = cms.InputTag("firstPrimaryVertex"),
        GlobalMuonVeto = param.GlobalMuonVeto.clone(
            src = cms.untracked.InputTag("selectedPatMuonsEmbeddingMuonCleaned")
        ),
        filter = cms.bool(True)              
    )
    m2 = cms.EDProducer("EventCountProducer")

    setattr(process, filter, m1)
    setattr(process, counter, m2)

    sequence *= (m1 * m2)

    return [counter]

def addElectronVeto(process, sequence, param, prefix="muonSelectionElectronVeto"):
    filter = prefix+"Filter"
    counter = prefix

    m1 = cms.EDFilter("HPlusGlobalElectronVetoFilter",
        GlobalElectronVeto = param.GlobalElectronVeto.clone(),
        filter = cms.bool(True)
    )
    m2 = cms.EDProducer("EventCountProducer")

    setattr(process, filter, m1)
    setattr(process, counter, m2)

    sequence *= (m1 * m2)

    return [counter]


def addMuonSelection(process, postfix="", cut="(isolationR03().emEt+isolationR03().hadEt+isolationR03().sumPt)/pt() < 0.10"):
    body = "muonSelectionAnalysis"+postfix
    counters = []

    allEvents = cms.EDProducer("EventCountProducer")
    setattr(process, body+"AllEvents", allEvents)
    counters.append(body+"AllEvents")

    muons = cms.EDFilter("PATMuonSelector",
        src = cms.InputTag(tauEmbeddingMuons),
        cut = cms.string(cut)
    )
    setattr(process, body+"Muons", muons)

    muonsFilter = cms.EDFilter("CandViewCountFilter",
        src = cms.InputTag(body+"Muons"),
        minNumber = cms.uint32(1)
    )
    setattr(process, body+"MuonsFilter", muonsFilter)

    selected = cms.EDProducer("EventCountProducer")
    setattr(process, body+"Selected", selected)
    counters.append(body+"Selected")

    seq = cms.Sequence(
        allEvents *
        muons *
        muonsFilter *
        selected
    )
    setattr(process, body+"Sequence", seq)
    
    return (seq, counters, body+"Muons")

def addMuonTauIsolation(process, postfix="", discriminator="byTightIsolation"):
    body = "muonSelectionAnalysis"+postfix
    counters = []

    allEvents = cms.EDProducer("EventCountProducer")
    setattr(process, body+"AllEvents", allEvents)
    counters.append(body+"AllEvents")

    muons = cms.EDProducer("HPlusTauIsolationPATMuonRefSelector",
        candSrc = cms.InputTag(tauEmbeddingMuons),
        tauSrc = cms.InputTag("patTausHpsPFTau", "", "MUONSKIM"),
        isolationDiscriminator = cms.string(discriminator),
        againstMuonDiscriminator = cms.string("againstMuonLoose"),
        deltaR = cms.double(0.15),
        minCands = cms.uint32(1)
    )
    setattr(process, body+"Muons", muons)

    muonsFilter = cms.EDFilter(
        "CandViewCountFilter",
        src = cms.InputTag(body+"Muons"),
        minNumber = cms.uint32(1)
    )
    setattr(process, body+"MuonsFilter", muonsFilter)

    selected = cms.EDProducer("EventCountProducer")
    setattr(process, body+"Selected", selected)
    counters.append(body+"Selected")

    seq = cms.Sequence(
        allEvents *
        muons *
        muonsFilter *
        selected
    )
    setattr(process, body+"Sequence", seq)

    return (seq, counters, body+"Muons")

def _signalAnalysisSetMuon(module, muons):
    module.tauEmbedding.originalMuon = cms.untracked.InputTag(muons)

def addMuonIsolation(process, sequence, prefix, isolation):
    selector = prefix+"Selected"
    filter = prefix+"Filter"
    counter = prefix

    # Create modules
    m1 = cms.EDFilter("HPlusCandViewLazyPtrSelector",
        src = cms.InputTag(tauEmbeddingMuons),
        cut = cms.string(isolation)
    )
    m2 = cms.EDFilter("CandViewCountFilter",
        src = cms.InputTag(selector),
        minNumber = cms.uint32(1)
    )
    m3 = cms.EDProducer("EventCountProducer")

    # Add modules to process
    setattr(process, selector, m1)
    setattr(process, filter, m2)
    setattr(process, counter, m3)

    # Add modules to sequence
    sequence *= (m1 * m2 * m3)

    # Return list of counter names
    return [counter]

def addMuonIsolationAnalyses(process, prefix, prototype, commonSequence, additionalCounters, modify=_signalAnalysisSetMuon, signalAnalysisCounters=True):
    import muonAnalysis

    detRelIso = muonAnalysis.isolations["sumIsoRel"]
    pfRelIso = muonAnalysis.isolations["pfSumIsoRel"]

    isolations = [
        ("RelIso05", detRelIso+" < 0.05"),
        ("RelIso10", detRelIso+" < 0.10"),
        ("RelIso15", detRelIso+" < 0.15"),
#        ("RelIso20", detRelIso+" < 0.20"),
        ("RelIso25", detRelIso+" < 0.25"),
        ("RelIso50", detRelIso+" < 0.50"),

        ("PfRelIso05", pfRelIso+" < 0.05"),
        ("PfRelIso10", pfRelIso+" < 0.10"),
        ("PfRelIso15", pfRelIso+" < 0.15"),
#        ("PfRelIso20", pfRelIso+" < 0.20"),
        ("PfRelIso25", pfRelIso+" < 0.25"),
        ("PfRelIso50", pfRelIso+" < 0.50"),

        ("IsoTauLikeVLoose", muonAnalysis.isolations["tauVLooseIso"]+" == 0"),
        ("IsoTauLikeLoose",  muonAnalysis.isolations["tauLooseIso"] +" == 0"),
        ("IsoTauLikeMedium", muonAnalysis.isolations["tauMediumIso"]+" == 0"),
        ("IsoTauLikeTight",  muonAnalysis.isolations["tauTightIso"] +" == 0"),
        ("IsoTauLikeTightSc015", muonAnalysis.isolations["tauTightSc015Iso"] +" == 0" ),
        ("IsoTauLikeTightSc02", muonAnalysis.isolations["tauTightSc02Iso"] +" == 0" ),

        ("IsoTauLikeTightIc04",  muonAnalysis.isolations["tauTightIc04Iso"] +" == 0"),
        ("IsoTauLikeTightSc015Ic04", muonAnalysis.isolations["tauTightSc015Ic04Iso"] +" == 0" ),
        ("IsoTauLikeTightSc02Ic04", muonAnalysis.isolations["tauTightSc02Ic04Iso"] +" == 0" ),


        ("IsoTauLikeTightSumPtRel10",  muonAnalysis.isolations["tauTightIso"] +" < 0.1"),
        ("IsoTauLikeTightSumPtRel15",  muonAnalysis.isolations["tauTightIso"] +" < 0.15"),

        ("IsoTauLikeTightSc0SumPtRel10",  muonAnalysis.isolations["tauTightSc0SumPtIsoRel"] +" < 0.1"),
        ("IsoTauLikeTightSc0SumPtRel15",  muonAnalysis.isolations["tauTightSc0SumPtIsoRel"] +" < 0.15"),

        ("IsoTauLikeTightSc0Ic04SumPtRel10",  muonAnalysis.isolations["tauTightSc0Ic04SumPtIsoRel"] +" < 0.1"),
        ("IsoTauLikeTightSc0Ic04SumPtRel15",  muonAnalysis.isolations["tauTightSc0Ic04SumPtIsoRel"] +" < 0.15"),

        ("IsoTauLikeTightSc0Ic04NoqSumPtRel10",  muonAnalysis.isolations["tauTightSc0Ic04NoqSumPtIsoRel"] +" < 0.1"),
        ("IsoTauLikeTightSc0Ic04NoqSumPtRel10",  muonAnalysis.isolations["tauTightSc0Ic04NoqSumPtIsoRel"] +" < 0.15"),

        ]

    tauIsolations = [
#        "VLoose",
#        "Loose",
#        "Medium",
#        "Tight"
        ]

    for name, cut in isolations:
        (sequence, counters, muons) = addMuonSelection(process, name, cut)
        cseq = cms.Sequence(commonSequence*sequence)
        setattr(process, prefix+name+"CommonSequence", cseq)

        module = prototype.clone()
        modify(module, muons)

        HChTools.addAnalysis(process, prefix+name, module, cseq, additionalCounters+counters, signalAnalysisCounters)

    for name in tauIsolations:
        (sequence, counters, muons) = addMuonTauIsolation(process, "IsoTau"+name, "by%sIsolation"%name)
        cseq = cms.Sequence(commonSequence*sequence)
        setattr(process, prefix+"IsoTau"+name+"CommonSequence", cseq)

        module = prototype.clone()
        modify(module, muons)

        HChTools.addAnalysis(process, prefix+"IsoTau"+name, module, cseq, additionalCounters+counters, signalAnalysisCounters)


def addTauAnalyses(process, prefix, prototype, commonSequence, additionalCounters):
    def disableRtau(module):
        return module.clone(rtauCut = -1)

    values = [
        HChSignalAnalysisParameters.tauSelectionHPSLooseTauBased,
        disableRtau(HChSignalAnalysisParameters.tauSelectionHPSLooseTauBased),
        disableRtau(HChSignalAnalysisParameters.tauSelectionHPSMediumTauBased),
        disableRtau(HChSignalAnalysisParameters.tauSelectionHPSTauBased),
        disableRtau(HChSignalAnalysisParameters.tauSelectionShrinkingConeCutBased),
        ]
    names = [
        "TauSelectionHPSLooseTauBased",
        "TauSelectionHPSLooseTauNoRtauBased",
        "TauSelectionHPSMediumTauNoRtauBased",
        "TauSelectionHPSTightTauNoRtauBased",
        "TauSelectionShrinkingConeCutNoRtauBased",
        ]

    HChTools.addAnalysisArray(process, prefix, prototype, HChSignalAnalysisParameters.setTauSelection,
                              values=values, names=names,
                              preSequence=commonSequence, additionalCounters=additionalCounters)
    


def addTauEmbeddingMuonTaus(process):
    seq = cms.Sequence()

    # Remove the embedding muon from the list of muons, use the rest
    # as an input for the global muon veto
    from PhysicsTools.PatAlgos.cleaningLayer1.muonCleaner_cfi import cleanPatMuons
    process.selectedPatMuonsEmbeddingMuonCleaned = cleanPatMuons.clone(
        src = cms.InputTag("selectedPatMuons"),
        checkOverlaps = cms.PSet(
            muons = cms.PSet(
                src                 = cms.InputTag(tauEmbeddingMuons),
                algorithm           = cms.string("byDeltaR"),
                preselection        = cms.string(""),
                deltaR              = cms.double(0.1),
                checkRecoComponents = cms.bool(False),
                pairCut             = cms.string(""),
                requireNoOverlaps   = cms.bool(True),
            ),
        )
    )
    seq *= process.selectedPatMuonsEmbeddingMuonCleaned

    # Select the taus matching to the original muon
    prototype = cms.EDProducer("HPlusPATTauCandViewDeltaRSelector",
        src = cms.InputTag("dummy"),
        refSrc = cms.InputTag(tauEmbeddingMuons),
        deltaR = cms.double(0.1),
    )

    for tau in ["patTausHpsPFTau", "patTausHpsTancPFTau"]:
        m = prototype.clone(
            src = tau
        )
        setattr(process, tau+"TauEmbeddingMuonMatched", m)
        seq *= m

    return seq

    
def addGeneratorTauFilter(process, sequence, filterInaccessible=False, prefix="generatorTaus"):
    counters = []

    allCount = cms.EDProducer("EventCountProducer")
    setattr(process, prefix+"AllCount", allCount)
    counters.append(prefix+"AllCount")

    genTaus = cms.EDFilter("GenParticleSelector",
        src = cms.InputTag("genParticles"),
        cut = cms.string("abs(pdgId()) == 15")
    )
    genTausName = prefix
    setattr(process, genTausName, genTaus)

    genTausFilter = cms.EDFilter("CandViewCountFilter",
        src = cms.InputTag(genTausName),
        minNumber = cms.uint32(1),
    )
    setattr(process, prefix+"Filter", genTausFilter)

    genTausCount = cms.EDProducer("EventCountProducer")
    setattr(process, prefix+"Count", genTausCount)
    counters.append(prefix+"Count")

    genTauSequence = cms.Sequence(
        allCount *
        genTaus *
        genTausFilter *
        genTausCount
    )
    setattr(process, prefix+"Sequence", genTauSequence)

    if filterInaccessible:
        genTausAccessible =  cms.EDFilter("GenParticleSelector",
            src = cms.InputTag("genParticles"),
            cut = cms.string("abs(pdgId()) == 15 && pt() > 40 && abs(eta()) < 2.1")
        )
        name = prefix+"Accessible"
        setattr(process, genTausAccessible, name)

        genTausInaccessibleFilter = cms.EDFilter("PATCandViewCountFilter",
            src = cms.InputTag(name),
            minNumber = cms.uint32(0),
            maxNumber = cms.uint32(0),
        )
        setattr(process, prefix+"InaccessibleFilter", genTausInaccessibleFilter)

        genTausInaccessibleCount = cms.EDProducer("EventCountProducer")
        name = prefix+"InaccessibleCount"
        setattr(process, name, genTausInaccessibleCount)
        counters.append(name)

        genTauSequence *= (
            genTausAccessible *
            genTausInaccessibleFilter *
            genTausInaccessibleCount
        )

    sequence *= genTauSequence

    return counters
