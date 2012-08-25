import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.HChTools as HChTools
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as HChSignalAnalysisParameters
import HiggsAnalysis.HeavyChHiggsToTauNu.HChGlobalElectronVetoFilter_cfi as ElectronVeto
import HiggsAnalysis.HeavyChHiggsToTauNu.HChGlobalMuonVetoFilter_cfi as MuonVeto

PF2PATVersion = "PFlow"
#PF2PATVersion = "PFlowChs"

allPatMuons = "selectedPatMuons"+PF2PATVersion
tauEmbeddingMuons = "tauEmbeddingMuons"

allPatTaus = "patTaus"+PF2PATVersion

jetSelection = "pt() > 30 && abs(eta()) < 2.4"
jetSelection += "&& numberOfDaughters() > 1 && chargedEmEnergyFraction() < 0.99"
jetSelection += "&& neutralHadronEnergyFraction() < 0.99 && neutralEmEnergyFraction < 0.99"
jetSelection += "&& chargedHadronEnergyFraction() > 0 && chargedMultiplicity() > 0"
jetSelection += "&& userFloat('Beta') > 0.2"

def customiseParamForTauEmbedding(param, options, dataVersion):
    # Change the triggers to muon
    param.trigger.triggers = [
        "HLT_Mu9",
        "HLT_Mu15_v1",
        "HLT_Mu20_v1",
        ]
    param.trigger.hltMetCut = -1 # disable
#    param.trigger.caloMetSelection.src = cms.untracked.InputTag("met", "", dataVersion.getRecoProcess())
    param.trigger.caloMetSelection.src = options.tauEmbeddingCaloMet
    param.trigger.caloMetSelection.metEmulationCut = -1#60.0

    tauTrigger = options.tauEmbeddingTauTrigger
    if len(tauTrigger) == 0:
        tauTrigger = "HLT_IsoPFTau35_Trk20_EPS"

    param.trigger.selectionType = "disabled"
    param.triggerEfficiencyScaleFactor.mode = "disabled"

    # Use PatJets and PFMet directly
    param.changeJetCollection(moduleLabel="selectedPatJets"+PF2PATVersion) # these are really AK5PF
    #param.MET.rawSrc = "pfMet" # no PAT object at the moment

    # Use the muons where the original muon is removed in global muon veto
    param.GlobalMuonVeto.MuonCollectionName.setModuleLabel("selectedPatMuonsEmbeddingMuonCleaned")
    param.GlobalElectronVeto.ElectronCollectionName.setProcessName("MUONSKIM")

    # Use the taus matched to the original muon in tau selections
    # Notice that only the version corresponding to PF2PATVersion is produced
    replacePostfix = "TauEmbeddingMuonMatched"
    def replaceTauSrc(mod):
        mod.src.setModuleLabel(mod.src.getModuleLabel().replace("TriggerMatched"+PF2PATVersion, replacePostfix))
    param.forEachTauSelection(replaceTauSrc)

    # Set the analyzer
    param.tree.tauEmbeddingInput = cms.untracked.bool(True)
    param.tree.tauEmbedding = cms.untracked.PSet(
        muonSrc = cms.InputTag(tauEmbeddingMuons),
        muonFunctions = cms.PSet(),
        genParticleOriginalSrc = cms.InputTag("genParticles", "", dataVersion.getTriggerProcess()),
        metSrc = cms.InputTag("pfMet", "", dataVersion.getRecoProcess()),
        caloMetNoHFSrc = cms.InputTag("caloMetNoHFSum"),
        caloMetSrc = cms.InputTag("caloMetSum"),
    )
    import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonAnalysis as muonAnalysis
    muonIsolations = ["trackIso", "caloIso", "pfChargedIso", "pfNeutralIso", "pfGammaIso", "tauTightIc04ChargedIso", "tauTightIc04GammaIso"]
    for name in muonIsolations:
        setattr(param.tree.tauEmbedding.muonFunctions, name, cms.string(muonAnalysis.isolations[name]))
    

def setCaloMetSum(process, sequence, options, dataVersion):
    name = "caloMetNoHFSum"
    m = cms.EDProducer("HPlusCaloMETSumProducer",
                       src = cms.VInputTag(cms.InputTag("metNoHF", "", dataVersion.getRecoProcess()),
                                           cms.InputTag("metNoHF", "", "EMBEDDING")
                                           )
                       )
    setattr(process, name, m)
    sequence *= m

    name = "caloMetSum"
    m = cms.EDProducer("HPlusCaloMETSumProducer",
                       src = cms.VInputTag(cms.InputTag("met", "", dataVersion.getRecoProcess()),
                                           cms.InputTag("met", "", "EMBEDDING")
                                           )
                       )
    setattr(process, name, m)
    sequence *= m

def addMuonIsolationEmbeddingForSignalAnalysis(process, sequence, **kwargs):
    global tauEmbeddingMuons
    muons = addMuonIsolationEmbedding(process, sequence, tauEmbeddingMuons, **kwargs)
    tauEmbeddingMuons = muons

def addMuonIsolationEmbedding(process, sequence, muons, pfcands="particleFlow", primaryVertex="firstPrimaryVertex",postfix=""):
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
    # name = "patMuonsWithTight"+postfix
    # setattr(process, name, tight)
    name = muons

    # medium = tight.clone(
    #     candSrc = name,
    #     embedPrefix = "byMedium",
    # )
    # name = "patMuonsWithMedium"+postfix
    # setattr(process, name, medium)

    # loose = tight.clone(
    #     candSrc = name,
    #     embedPrefix = "byLoose",
    # )
    # name = "patMuonsWithLoose"+postfix
    # setattr(process, name, loose)

    # vloose = tight.clone(
    #     candSrc = name,
    #     embedPrefix = "byVLoose",
    # )
    # name = "patMuonsWithVLoose"+postfix
    # setattr(process, name, vloose)

    tight.qualityCuts = RecoPFTauTag.hpsPFTauDiscriminationByTightIsolation.qualityCuts.clone()
    # medium.qualityCuts = RecoPFTauTag.hpsPFTauDiscriminationByMediumIsolation.qualityCuts.clone()
    # loose.qualityCuts = RecoPFTauTag.hpsPFTauDiscriminationByLooseIsolation.qualityCuts.clone()
    # vloose.qualityCuts = RecoPFTauTag.hpsPFTauDiscriminationByVLooseIsolation.qualityCuts.clone()

    # sequence *= (tight * medium * loose *vloose)

    #######################
    # m = tight.clone(
    #     candSrc = name,
    #     embedPrefix = "byTightSc015",
    #     signalCone = 0.15
    # )
    # name = "patMuonsWithTightSc015"+postfix
    # setattr(process, name, m)
    # sequence *= m

    # m = tight.clone(
    #     candSrc = name,
    #     embedPrefix = "byTightSc02",
    #     signalCone = 0.2
    # )
    # name = "patMuonsWithTightSc02"+postfix
    # setattr(process, name, m)
    # sequence *= m

    ## This is the one used for HIG-11-019 paper
    # I.e. counting in annulus 0.1 < DR < 0.4
    m = tight.clone(
        candSrc = name,
        embedPrefix = "byTightIc04",
        isolationCone = 0.4
    )
    name = "patMuonsWithTightIc04"+postfix
    setattr(process, name, m)
    sequence *= m


    # m = m.clone(
    #     candSrc = name,
    #     embedPrefix = "byTightSc015Ic04",
    #     signalCone = 0.15
    # )
    # name = "patMuonsWithTightSc015Ic04"+postfix
    # setattr(process, name, m)
    # sequence *= m

    # m = m.clone(
    #     candSrc = name,
    #     embedPrefix = "byTightSc02Ic04",
    #     signalCone = 0.2
    # )
    # name = "patMuonsWithTightSc02Ic04"+postfix
    # setattr(process, name, m)
    # sequence *= m

    #######################
    # m = tight.clone(
    #     candSrc = name,
    #     embedPrefix = "byTightSc0",
    #     signalCone = 0.01
    # )
    # name = "patMuonsWithTightSc0"+postfix
    # setattr(process, name, m)
    # sequence *= m

    # m = m.clone(
    #     candSrc = name,
    #     embedPrefix = "byTightSc0Ic04",
    #     isolationCone = 0.4,
    # )
    # name = "patMuonsWithTightSc0Ic04"+postfix
    # setattr(process, name, m)
    # sequence *= m

    # m = m.clone(
    #     candSrc = name,
    #     embedPrefix = "byTightSc0Ic04Noq",
    #     #minTrackHits = 0, #FIXME PFlow added, make sure that correct collection is taken (i.e. not CHS)
    #     #minTrackPt = 0.0,
    #     #maxTrackChi2 = 9999.,
    #     #minTrackPixelHits = 0,
    #     #minGammaEt = 0.0,
    #     #maxDeltaZ = 9999.,
    # )
    # name = "patMuonsWithTightSc0Ic04Noq"+postfix
    # setattr(process, name, m)
    # sequence *= m

    #######################
    # DeltaBeta-based isolation for embedding, for now this configuration is only a guess
    import RecoMuon.MuonIsolation.muonPFIsolationValues_cff as muonPFIsolation
    def construct(isoModule, isoKey, vetos=[]):
        deposit = isoModule.deposits[0]
        pset = cms.PSet(
            embedName = cms.string(isoKey),
            deltaR = deposit.deltaR,
            skipDefaultVeto = deposit.skipDefaultVeto,
            mode = deposit.mode,
            isolationKey = cms.string(isoKey),
            vetos = cms.vstring(deposit.vetos)
        )
        pset.vetos.extend(vetos)
        return pset

    # In 0.1 < DR < 0.4
    isolation = cms.EDProducer("HPlusPATMuonViewIsoDepositIsolationEmbedder",
        src = cms.InputTag(name),
        embedPrefix = cms.string("iso01to04_"),
        deposits = cms.VPSet(
            construct(muonPFIsolation.muPFIsoValueNeutral04, "pfNeutralHadrons", vetos=["ConeVeto(0.1)"]),
            construct(muonPFIsolation.muPFIsoValueChargedAll04, "pfChargedAll",  vetos=["ConeVeto(0.1)"]),
            construct(muonPFIsolation.muPFIsoValuePU04, "pfPUChargedHadrons",    vetos=["ConeVeto(0.1)"]),
            construct(muonPFIsolation.muPFIsoValueGamma04, "pfPhotons",          vetos=["ConeVeto(0.1)"]),
            construct(muonPFIsolation.muPFIsoValueCharged04, "pfChargedHadrons", vetos=["ConeVeto(0.1)"]),
        )
    )
    name = "patMuonsWithIso01to04"+postfix
    setattr(process, name, isolation)
    sequence *= isolation


    # In 0.1 < DR < 0.3
    isolation = cms.EDProducer("HPlusPATMuonViewIsoDepositIsolationEmbedder",
        src = cms.InputTag(name),
        embedPrefix = cms.string("iso01to03_"),
        deposits = cms.VPSet(
            construct(muonPFIsolation.muPFIsoValueNeutral03, "pfNeutralHadrons", vetos=["ConeVeto(0.1)"]),
            construct(muonPFIsolation.muPFIsoValueChargedAll03, "pfChargedAll",  vetos=["ConeVeto(0.1)"]),
            construct(muonPFIsolation.muPFIsoValuePU03, "pfPUChargedHadrons",    vetos=["ConeVeto(0.1)"]),
            construct(muonPFIsolation.muPFIsoValueGamma03, "pfPhotons",          vetos=["ConeVeto(0.1)"]),
            construct(muonPFIsolation.muPFIsoValueCharged03, "pfChargedHadrons", vetos=["ConeVeto(0.1)"]),
        )
    )
    name = "patMuonsWithIso01to03"+postfix
    setattr(process, name, isolation)
    sequence *= isolation


    #######################
    # Abuse the isolation function to embed generator matching
    gen = cms.EDProducer("HPlusPATMuonViewGenEmbedder",
        candSrc = cms.InputTag(name),
        genParticleSrc = cms.InputTag("genParticles"),
        embedPrefix = cms.string("gen"),
        maxDR = cms.double(0.5),
        pdgId = cms.uint32(13)
    )
    name = "patMuonsWithGen"+postfix
    setattr(process, name, gen)
    sequence *= gen

    import PhysicsTools.PatAlgos.selectionLayer1.muonSelector_cfi as muonSelector
    m = muonSelector.selectedPatMuons.clone(
        src = name
    )
    name = "patMuonsWithIso"+postfix
    setattr(process, name, m)
    sequence *= m

    return name

def constructMuonIsolationOnTheFly(inputMuons, embedPrefix="ontheflyiso_"):
    import RecoMuon.MuonIsolation.muonPFIsolationValues_cff as muonPFIsolation
    def construct(isoModule, isoKey, vetos=[]):
        deposit = isoModule.deposits[0]
        pset = cms.PSet(
            embedName = cms.string(isoKey),
            deltaR = deposit.deltaR,
            skipDefaultVeto = deposit.skipDefaultVeto,
            mode = deposit.mode,
            isolationKey = cms.string(isoKey),
            vetos = cms.vstring(deposit.vetos)
        )
        pset.vetos.extend(vetos)
        return pset
    global tauEmbeddingMuons
    module = cms.EDProducer("HPlusPATMuonViewIsoDepositIsolationEmbedder",
        src = cms.InputTag(inputMuons),
        embedPrefix = cms.string(embedPrefix),
        deposits = cms.VPSet(
            construct(muonPFIsolation.muPFIsoValueNeutral03, "pfNeutralHadrons", vetos=["ConeVeto(0.1)"]),
            construct(muonPFIsolation.muPFIsoValueChargedAll03, "pfChargedAll",  vetos=["ConeVeto(0.1)"]),
            construct(muonPFIsolation.muPFIsoValuePU03, "pfPUChargedHadrons",    vetos=["ConeVeto(0.1)", "Threshold(0.5)"]),
            construct(muonPFIsolation.muPFIsoValueGamma03, "pfPhotons",          vetos=["ConeVeto(0.1)", "Threshold(0.8)"]),
            construct(muonPFIsolation.muPFIsoValueCharged03, "pfChargedHadrons", vetos=["ConeVeto(0.1)", "Threshold(0.8)"]),
            #construct(muonPFIsolation.muPFIsoValueNeutral04, "pfNeutralHadrons", vetos=["ConeVeto(0.1)"]),
            #construct(muonPFIsolation.muPFIsoValueChargedAll04, "pfChargedAll",  vetos=["ConeVeto(0.1)"]),
            #construct(muonPFIsolation.muPFIsoValuePU04, "pfPUChargedHadrons",    vetos=["ConeVeto(0.1)", "Threshold(0.5)"]),
            #construct(muonPFIsolation.muPFIsoValueGamma04, "pfPhotons",          vetos=["ConeVeto(0.1)", "Threshold(0.8)"]),
            #construct(muonPFIsolation.muPFIsoValueCharged04, "pfChargedHadrons", vetos=["ConeVeto(0.1)", "Threshold(0.8)"]),
        )
    )
    return module

def addFinalMuonSelection(process, sequence, param, enableIsolation=True, prefix="muonFinalSelection"):
    counters = []

    cname = prefix+"AllEvents"
    m = cms.EDProducer("EventCountProducer")
    setattr(process, cname, m)
    sequence *= m
    counters.append(cname)

    # FIXME: ugly hack to calculate muon isolation on the fly (this is the wrong place to do it)
    global tauEmbeddingMuons
    isolation = constructMuonIsolationOnTheFly(tauEmbeddingMuons)
    name = "patMuonsUserOnTheFlyIso"+PF2PATVersion
    tauEmbeddingMuons = name
    setattr(process, name, isolation)
    sequence *= isolation
    # FIXME end ugly hack


    # The old counting-tight in 0.1 < DR < 0.4 annulus
    #isoExpr = "(%s)==0" % muonAnalysis.isolations["tauTightIc04Iso"]
    # Medium iso PF tau combined delta beta
    # Obtain delta beta from RecoTauTag/Configuration/python/HPSPFTaus_cff.py
    # FIXME: does it matter if the PU charged hadrons are not calculated in cone 0.8?
    # FIXME: the k-parameter for the PU charged hadrons can be changed (chosen by optimisation)
    #isoExpr = "(userFloat('ontheflyiso_pfChargedHadrons') + max(userFloat('ontheflyiso_pfPhotons')-0.27386*userFloat('ontheflyiso_pfPUChargedHadrons'), 0)) < 1"
    isoExpr = "(userFloat('ontheflyiso_pfChargedHadrons') + max(userFloat('ontheflyiso_pfPhotons')-0.5*userFloat('ontheflyiso_pfPUChargedHadrons'), 0)) < 2"
    #isoExpr = "1==1" # Ugliness squared, we apply the isolation on the fly calculated from the above user floats
    if enableIsolation:
        print "*** Isolation for muon is enabled ***"
#        counters.extend(addMuonRelativeIsolation(process, sequence, prefix=prefix+"Isolation", cut=0.1))
        import muonAnalysis
        counters.extend(addMuonIsolation(process, sequence, prefix+"Isolation", isoExpr))
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

    from PhysicsTools.PatAlgos.cleaningLayer1.jetCleaner_cfi import cleanPatJets
    m1 = cleanPatJets.clone(
#        src = "selectedPatJets",
        src = "goodJets"+PF2PATVersion, # we should use the pat::Jets constructed in the 
        preselection = cms.string(jetSelection),
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
    m2 = cms.EDFilter("CandViewCountFilter",
        src = cms.InputTag(selector),
        minNumber = cms.uint32(3)
    )
    m3 = cms.EDProducer("EventCountProducer")

    setattr(process, selector, m1)
    setattr(process, filter, m2)
    setattr(process, counter, m3)

    sequence *= (m1 * m2 * m3)

    return [counter]


def addMuonVeto(process, sequence, param, prefix="muonSelectionMuonVeto"):
    filter = prefix+"Filter"
    counter = prefix

    import HiggsAnalysis.HeavyChHiggsToTauNu.HChGlobalMuonVetoFilter_cfi as muonVetoFilter_cfi
    m1 = muonVetoFilter_cfi.hPlusGlobalMuonVetoFilter.clone(
        vertexSrc = "firstPrimaryVertex"
    )
    m1.GlobalMuonVeto.MuonCollectionName = "selectedPatMuonsEmbeddingMuonCleaned"
    m2 = cms.EDProducer("EventCountProducer")

    setattr(process, filter, m1)
    setattr(process, counter, m2)

    sequence *= (m1 * m2)

    return [counter]

def addElectronVeto(process, sequence, param, prefix="muonSelectionElectronVeto"):
    filter = prefix+"Filter"
    counter = prefix

    import HiggsAnalysis.HeavyChHiggsToTauNu.HChGlobalElectronVetoFilter_cfi as electronVetoFilter_cfi
    m1 = electronVetoFilter_cfi.hPlusGlobalElectronVetoFilter.clone()
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
    


def selectedMuonCleanedMuons(selectedMuon, allMuons=allPatMuons):
    from PhysicsTools.PatAlgos.cleaningLayer1.muonCleaner_cfi import cleanPatMuons
    module = cleanPatMuons.clone(
        src = cms.InputTag(allMuons),
        checkOverlaps = cms.PSet(
            muons = cms.PSet(
                src                 = cms.InputTag(selectedMuon),
                algorithm           = cms.string("byDeltaR"),
                preselection        = cms.string(""),
                deltaR              = cms.double(0.0001),
                checkRecoComponents = cms.bool(False),
                pairCut             = cms.string(""),
                requireNoOverlaps   = cms.bool(True),
            ),
        )
    )
    return module
    

def addTauEmbeddingMuonTaus(process):
    seq = cms.Sequence()

    # Remove the embedding muon from the list of muons, use the rest
    # as an input for the global muon veto
    process.selectedPatMuonsEmbeddingMuonCleaned = selectedMuonCleanedMuons(tauEmbeddingMuons)
    seq *= process.selectedPatMuonsEmbeddingMuonCleaned

    # Select the taus matching to the original muon
    m = cms.EDProducer("HPlusPATTauCandViewDeltaRSelector",
        src = cms.InputTag(allPatTaus),
        refSrc = cms.InputTag(tauEmbeddingMuons),
        deltaR = cms.double(0.1),
    )
    setattr(process, allPatTaus+"TauEmbeddingMuonMatched", m)
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

def addGenuineTauPreselection(process, sequence, param, prefix="genuineTauPreselection"):
    counters = []

    # Create PU weight producer for the counters
    pileupWeight = cms.EDProducer("HPlusVertexWeightProducer",
        alias = cms.string("pileupWeight"),
    )
    HChTools.insertPSetContentsTo(param.vertexWeight.clone(), pileupWeight)
    setattr(process, prefix+"PileupWeight", pileupWeight)

    counterPrototype = cms.EDProducer("HPlusEventCountProducer",
        weightSrc = cms.InputTag(prefix+"PileupWeight")
    )

    allCount = counterPrototype.clone()
    setattr(process, prefix+"AllCount", allCount)
    counters.append(prefix+"AllCount")

    # Generator taus (if you modify this, remember to modify similar in below)
    genTaus = cms.EDFilter("GenParticleSelector",
        src = cms.InputTag("genParticles"),
        cut = cms.string("abs(pdgId()) == 15 && pt() > 40 && abs(eta()) < 2.1")
    )
    genTausName = prefix+"GenTau"
    setattr(process, genTausName, genTaus)

    genTausFilter = cms.EDFilter("CandViewCountFilter",
        src = cms.InputTag(genTausName),
        minNumber = cms.uint32(1),
    )
    setattr(process, prefix+"GenTauFilter", genTausFilter)

    genTausCount = counterPrototype.clone()
    setattr(process, prefix+"GenTauCount", genTausCount)
    counters.append(prefix+"GenTauCount")

    genTauSequence = cms.Sequence(
        pileupWeight *
        allCount *
        genTaus * genTausFilter * genTausCount
    )
    setattr(process, prefix+"Sequence", genTauSequence)
    sequence *= genTauSequence

    return counters


def addEmbeddingLikePreselection(process, sequence, param, prefix="embeddingLikePreselection", disableTrigger=True):
    counters = []

    # Create PU weight producer for the counters
    pileupWeight = cms.EDProducer("HPlusVertexWeightProducer",
        alias = cms.string("pileupWeight"),
    )
    HChTools.insertPSetContentsTo(param.vertexWeight.clone(), pileupWeight)
    setattr(process, prefix+"PileupWeight", pileupWeight)

    counterPrototype = cms.EDProducer("HPlusEventCountProducer",
        weightSrc = cms.InputTag(prefix+"PileupWeight")
    )

    # Disable trigger
    if disableTrigger:
        param.trigger.selectionType = "disabled"
        param.triggerEfficiencyScaleFactor.mode = "disabled"

    allCount = counterPrototype.clone()
    setattr(process, prefix+"AllCount", allCount)
    counters.append(prefix+"AllCount")

    # Primary vertex
    pvFilter = cms.EDFilter("VertexCountFilter",
        src = cms.InputTag("selectedPrimaryVertex"),
        minNumber = cms.uint32(1),
        maxNumber = cms.uint32(999)
    )
    pvFilterCount = counterPrototype.clone()
    setattr(process, prefix+"PrimaryVertex", pvFilter)
    setattr(process, prefix+"PrimaryVertexCount", pvFilterCount)
    counters.append(prefix+"PrimaryVertexCount")

    # Generator taus (if you modify this, remember to modify similar in above)
    genTaus = cms.EDFilter("GenParticleSelector",
        src = cms.InputTag("genParticles"),
        cut = cms.string("abs(pdgId()) == 15 && pt() > 40 && abs(eta()) < 2.1")
    )
    genTausName = prefix+"GenTau"
    setattr(process, genTausName, genTaus)

    genTausFilter = cms.EDFilter("CandViewCountFilter",
        src = cms.InputTag(genTausName),
        minNumber = cms.uint32(1),
    )
    setattr(process, prefix+"GenTauFilter", genTausFilter)

    genTausCount = counterPrototype.clone()
    setattr(process, prefix+"GenTauCount", genTausCount)
    counters.append(prefix+"GenTauCount")

    # Select first generator tau for the jet cleaning and tau selection
    genTauFirst = cms.EDProducer("HPlusFirstCandidateSelector",
        src = cms.InputTag(genTausName)
    )
    genTauFirstName = prefix+"First"
    setattr(process, genTauFirstName, genTauFirst)

    # Tau selection
    genTauReco = cms.EDProducer("HPlusPATTauCandViewDeltaRSelector",
        src = cms.InputTag("selectedPatTausHpsPFTau"), # not trigger matched
        refSrc = cms.InputTag(genTauFirstName),
        deltaR = cms.double(0.5),
    )
    if not disableTrigger:
        genTauReco.src = param.tauSelection.src.value()
    genTauRecoName = prefix+"Reco"
    setattr(process, genTauRecoName, genTauReco)
    param.tauSelection.src = genTauRecoName

    genTauCleanPSet = cms.PSet(
        src                 = cms.InputTag(genTauFirstName),
        algorithm           = cms.string("byDeltaR"),
        preselection        = cms.string(""),
        deltaR              = cms.double(0.5),
        checkRecoComponents = cms.bool(False),
        pairCut             = cms.string(""),
        requireNoOverlaps   = cms.bool(True),
    )

    # Clean the selected generator tau from the electrons and muons
    # for the e/mu veto. We don't want to reject events where the e/mu
    # comes from the tau decay.
    from PhysicsTools.PatAlgos.cleaningLayer1.electronCleaner_cfi import cleanPatElectrons
    from PhysicsTools.PatAlgos.cleaningLayer1.muonCleaner_cfi import cleanPatMuons
    cleanedElectrons = cleanPatElectrons.clone(
        src = cms.InputTag(param.GlobalElectronVeto.ElectronCollectionName.value()),
        checkOverlaps = cms.PSet(
            genTaus = genTauCleanPSet.clone()
        )
    )
    cleanedElectronsName = prefix+"CleanedElectrons"
    param.GlobalElectronVeto.ElectronCollectionName = cleanedElectronsName
    setattr(process, cleanedElectronsName, cleanedElectrons)
    cleanedMuons = cleanPatMuons.clone(
        src = cms.InputTag(param.GlobalMuonVeto.MuonCollectionName.value()),
        checkOverlaps = cms.PSet(
            genTaus = genTauCleanPSet.clone()
        )
    )
    cleanedMuonsName = prefix+"CleanedMuons"
    param.GlobalMuonVeto.MuonCollectionName = cleanedMuonsName
    setattr(process, cleanedMuonsName, cleanedMuons)

    # Electron and muon veto
    eveto = ElectronVeto.hPlusGlobalElectronVetoFilter.clone()
    evetoCount = counterPrototype.clone()
    muveto = MuonVeto.hPlusGlobalMuonVetoFilter.clone() 
    muvetoCount = counterPrototype.clone()
    setattr(process, prefix+"ElectronVeto", eveto)
    setattr(process, prefix+"ElectronVetoCount", evetoCount)
    setattr(process, prefix+"MuonVeto", muveto)
    setattr(process, prefix+"MuonVetoCount", muvetoCount)
    counters.extend([prefix+"ElectronVetoCount", prefix+"MuonVetoCount"])

    # 3 jets
    from PhysicsTools.PatAlgos.cleaningLayer1.jetCleaner_cfi import cleanPatJets
    cleanedJets = cleanPatJets.clone(
        src = cms.InputTag(param.jetSelection.src.value()),
        preselection = cms.string(jetSelection),
        checkOverlaps = cms.PSet(
            genTaus = genTauCleanPSet.clone()
        )
    )
    cleanedJetsName = prefix+"CleanedJets"
    setattr(process, cleanedJetsName, cleanedJets)

    cleanedJetsFilter = cms.EDFilter("CandViewCountFilter",
        src = cms.InputTag(cleanedJetsName),
        minNumber = cms.uint32(3)
    )
    setattr(process, cleanedJetsName+"Filter", cleanedJetsFilter)

    cleanedJetsCount = counterPrototype.clone()
    setattr(process, cleanedJetsName+"Count", cleanedJetsCount)
    counters.append(cleanedJetsName+"Count")

    genTauSequence = cms.Sequence(
        pileupWeight *
        allCount *
        pvFilter * pvFilterCount *
        genTaus * genTausFilter * genTausCount * genTauFirst * genTauReco *
        cleanedElectrons * cleanedMuons *
        eveto * evetoCount *
        muveto * muvetoCount *
        cleanedJets * cleanedJetsFilter * cleanedJetsCount 
    )
    setattr(process, prefix+"Sequence", genTauSequence)
    sequence *= genTauSequence

    return counters
