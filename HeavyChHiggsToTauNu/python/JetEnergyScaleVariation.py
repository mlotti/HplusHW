import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.JetEnergyScaleVariation_cfi import jesVariation

def addJESVariationAnalysis(process, prefix, name, prototype, additionalCounters, variation, etaVariation, unclusteredEneryVariationForMET, jetVariationMode="all"):
    variationName = name
    analysisName = prefix+name
    countersName = analysisName+"Counters"
    pathName = analysisName+"Path"

    # Construct the JES variation module
    variation = jesVariation.clone(
        tauSrc = cms.InputTag(prototype.tauSelection.src.value()), # from untracked to tracked
        jetSrc = cms.InputTag(prototype.jetSelection.src.value()),
        metSrc = cms.InputTag(prototype.MET.src.value()),
        JESVariation = cms.double(variation),
        JESEtaVariation = cms.double(etaVariation),
        unclusteredMETVariation = cms.double(unclusteredEneryVariationForMET),
        jetVariationMode = jetVariationMode,
    )
    setattr(process, variationName, variation)
    #"JES"+variation+"eta"+etaVariation+"unclusted"+unclusteredEneryVariationForMET)

    # Construct the signal analysis module for this variation
    # Use variated taus, jets and MET
    analysis = prototype.clone()
    analysis.tauSelection.src = variationName
    analysis.jetSelection.src = variationName
    analysis.MET.src = variationName
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
        process.commonSequence *
        variation *
        analysis *
        counters
    )
    setattr(process, pathName, path)
