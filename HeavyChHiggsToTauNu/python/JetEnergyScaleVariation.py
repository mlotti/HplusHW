import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.JetEnergyScaleVariation_cfi import jesVariation

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
    etaBins = cms.VPSet(
    )
)

metVariation = cms.EDProducer("HPlusMetEnergyScaleVariation",
    metSrc = cms.InputTag("patMETsPF"),
    tauSrc = cms.InputTag("tauVariation"),
    jetSrc = cms.InputTag("jetVariation"),
    unclusteredVariation = cms.double(0.1)
)

def addJESVariationAnalysis(process, prefix, name, prototype, additionalCounters, variation, etaVariation, unclusteredEnergyVariationForMET, jetVariationMode="all"):
    variationName = name
    tauVariationName = name+"TauVariation"
    jetVariationName = name+"JetVariation"
    jetsForMetVariation = name+"JetsForMetVariation"
    rawMetVariationName = name+"RawMetVariation"
    type1MetVariationName = name+"Type1MetVariation"
    analysisName = prefix+name
    countersName = analysisName+"Counters"
    pathName = analysisName+"Path"

    # Construct the JES variation module
    v = jesVariation.clone(
        tauSrc = cms.InputTag(prototype.tauSelection.src.value()), # from untracked to tracked
        jetSrc = cms.InputTag(prototype.jetSelection.src.value()),
        metSrc = cms.InputTag(prototype.MET.rawSrc.value()),
        JESVariation = cms.double(variation),
        JESEtaVariation = cms.double(etaVariation),
        unclusteredMETVariation = cms.double(unclusteredEnergyVariationForMET),
        jetVariationMode = jetVariationMode,
    )
    setattr(process, variationName, v)
    #"JES"+variation+"eta"+etaVariation+"unclusted"+unclusteredEnergyVariationForMET)

    # Tau variation
    tauv = tauVariation.clone(
        src = prototype.tauSelection.src.value(),
        energyVariation = variation,
        energyEtaVariation = etaVariation,
    )
    setattr(process, tauVariationName, tauv)

    # Jet variation
    jetv = jetVariation.clone(
        src = prototype.jetSelection.src.value(),
        defaultPlusVariation = variation > 0,
    )
    setattr(process, jetVariationName, jetv)

    # Select (type I like) jets for MET variation
    cutstr = process.selectedPatJetsForMETtype1p2Corr.cut.value()
    cutstr += "&& pt() > %f" % process.patPFJetMETtype1p2Corr.type1JetPtThreshold.value()
    jetsForMetv = cms.EDFilter("PATJetSelector",
        src = cms.InputTag(jetVariationName),
        cut = cms.string(cutstr)
    )
    setattr(process, jetsForMetVariation, jetsForMetv)

    # MET variation
    metrawv = metVariation.clone(
        metSrc = prototype.MET.rawSrc.value(),
        tauSrc = tauVariationName,
        jetSrc = jetsForMetVariation,
        unclusteredVariation = unclusteredEnergyVariationForMET
    )
    setattr(process, rawMetVariationName, metrawv)

    mettype1v = metVariation.clone(
        metSrc = prototype.MET.type1Src.value(),
        tauSrc = tauVariationName,
        jetSrc = jetsForMetVariation,
        unclusteredVariation = unclusteredEnergyVariationForMET
    )
    setattr(process, type1MetVariationName, mettype1v)

    # Construct the signal analysis module for this variation
    # Use variated taus, jets and MET
    analysis = prototype.clone()
    analysis.tauSelection.src = tauVariationName
    analysis.jetSelection.src = jetVariationName
    analysis.MET.rawSrc = rawMetVariationName
    analysis.MET.type1Src = type1MetVariationName
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
        * v
        * tauv
        * jetv
        * jetsForMetv
        * metrawv
        * analysis
        * counters
    )
    setattr(process, pathName, path)
