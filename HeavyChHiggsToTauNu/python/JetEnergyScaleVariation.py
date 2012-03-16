import FWCore.ParameterSet.Config as cms
import HiggsAnalysis.HeavyChHiggsToTauNu.HChMetCorrection as MetCorrection

tauVariation = cms.EDProducer("HPlusTauEnergyScaleVariation",
    src = cms.InputTag("selectedPatTaus"),
    energyVariation = cms.double(0.03),
    energyEtaVariation = cms.double(0)
)

jetVariation = cms.EDProducer("HPlusJetEnergyScaleVariation",
    src = cms.InputTag("selectedPatJetsAK5PF"),
    payloadName = cms.string("AK5PF"),
    uncertaintyTag = cms.string("Uncertainty"),
    defaultPlusVariation = cms.bool(True),
    doVariation = cms.bool(True),
    etaBins = cms.VPSet(
    )
)

metVariation = cms.EDProducer("HPlusMetEnergyScaleVariation",
    metSrc = cms.InputTag("patMETsPF"),
    tauSrc = cms.InputTag("tauVariation"),
    jetSrc = cms.InputTag("jetVariation"),
    unclusteredVariation = cms.double(0.1)
)

def addJESVariationAnalysis(process, dataVersion, prefix, name, prototype, additionalCounters, variation, etaVariation, unclusteredEnergyVariationForMET, doJetVariation=True):
    variationName = name
    tauVariationName = name+"TauVariation"
    jetVariationName = name+"JetVariation"
    jetsForMetVariation = name+"JetsForMetVariation"
    rawMetVariationName = name+"RawMetVariation"
    type1MetVariationName = name+"Type1MetVariation"
    type2MetVariationName = name+"Type2MetVariation"
    analysisName = prefix+name
    countersName = analysisName+"Counters"
    pathName = analysisName+"Path"

    # Tau variation
    tauv = tauVariation.clone(
        src = prototype.tauSelection.src.value(),
        energyVariation = variation,
        energyEtaVariation = etaVariation,
    )
    setattr(process, tauVariationName, tauv)

    # Recompute type 1 MET on the basis of variated tau. However, use
    # the non-variated jets, because the jet variation is taken into
    # account in the MET variation. The tau variation is taken into
    # account here, because the variation can change the decision of
    # which tau to select, and that tau is needed for the jet cleaning
    # in the type 1 MET calculation.
    tauSelection = prototype.tauSelection.clone(src=tauVariationName)
    (type1sequence, type1Met, type1p2Met) = MetCorrection.addCorrectedMet(process, dataVersion, tauSelection, prototype.jetSelection, postfix=name)
    tauForMetVariation = "selectedPatTausForMetCorr"+name

    # Jet variation
    jetv = jetVariation.clone(
        src = prototype.jetSelection.src.value(),
        defaultPlusVariation = variation > 0,
        doVariation = doJetVariation,
    )
    setattr(process, jetVariationName, jetv)

    # Select (type I like) jets for MET variation, clean the selected tau from these
    cutstr = process.selectedPatJetsForMETtype1p2Corr.cut.value()
    cutstr += "&& pt() > %f" % process.patPFJetMETtype1p2Corr.type1JetPtThreshold.value()
    jetsForMetv = cms.EDProducer("PATJetCleaner",
        src = cms.InputTag(jetVariationName),
        preselection = cms.string(cutstr),
        checkOverlaps = cms.PSet(
            taus = cms.PSet(
                src                 = cms.InputTag(tauForMetVariation),
                algorithm           = cms.string("byDeltaR"),
                preselection        = cms.string(""),
                deltaR              = cms.double(0.1),
                checkRecoComponents = cms.bool(False),
                pairCut             = cms.string(""),
                requireNoOverlaps   = cms.bool(True),
            )
        ),
        finalCut = cms.string("")
    )
    setattr(process, jetsForMetVariation, jetsForMetv)

    # MET variation
    # Use the same code for now (although this is not according to the
    # latest recipe for raw). Use the selected tau, and cleaned jets
    # passing the type1 selection (both tau and jet inputs should be
    # the variated ones)
    metrawv = metVariation.clone(
        metSrc = prototype.MET.rawSrc.value(),
        tauSrc = tauForMetVariation,
        jetSrc = jetsForMetVariation,
        unclusteredVariation = unclusteredEnergyVariationForMET
    )
    setattr(process, rawMetVariationName, metrawv)

    mettype1v = metVariation.clone(
        metSrc = type1Met,
        tauSrc = tauForMetVariation,
        jetSrc = jetsForMetVariation,
        unclusteredVariation = unclusteredEnergyVariationForMET
    )
    setattr(process, type1MetVariationName, mettype1v)

    mettype2v = metVariation.clone(
        metSrc = type1p2Met,
        tauSrc = tauForMetVariation,
        jetSrc = jetsForMetVariation,
        unclusteredVariation = unclusteredEnergyVariationForMET
    )
    setattr(process, type2MetVariationName, mettype2v)

    # Construct the signal analysis module for this variation
    # Use variated taus, jets and MET
    analysis = prototype.clone()
    analysis.tauSelection.src = tauVariationName
    analysis.jetSelection.src = jetVariationName
    analysis.MET.rawSrc = rawMetVariationName
    analysis.MET.type1Src = type1MetVariationName
    analysis.MET.type2Src = type2MetVariationName
    setattr(process, analysisName, analysis)
    
    # Construct the counters module
    counters = cms.EDAnalyzer("HPlusEventCountAnalyzer",
        counterNames = cms.untracked.InputTag(analysisName, "counterNames"),
        counterInstances = cms.untracked.InputTag(analysisName, "counterInstances")
    )
    if len(additionalCounters) > 0:
        counters.counters = cms.untracked.VInputTag([cms.InputTag(c) for c in additionalCounters])
    setattr(process, countersName, counters)

    # Construct the path
    path = cms.Path(
        process.commonSequence
        * tauv
        * type1sequence
        * jetv
        * jetsForMetv
        * metrawv
        * mettype1v
        * mettype2v
        * analysis
        * counters
    )
    setattr(process, pathName, path)
