import FWCore.ParameterSet.Config as cms
import PhysicsTools.PatUtils.patPFMETCorrections_cff as patPFMETCorrections

import math

tauVariation = cms.EDProducer("ShiftedPATTauProducer",
    src = cms.InputTag("selectedPatTaus"),
    uncertainty = cms.double(0.03),
    shiftBy = cms.double(+1), # +1/-1 for +-1 sigma variation
)

jetVariation = cms.EDProducer("ShiftedPATJetProducer",
    src = cms.InputTag("selectedPatJetsAK5PF"),
    jetCorrPayloadName = cms.string("AK5PF"),
    jetCorrUncertaintyTag = cms.string('Uncertainty'),
    #jetCorrInputFileName = cms.FileInPath('PhysicsTools/PatUtils/data/JEC11_V12_AK5PF_UncertaintySources.txt'),
    #jetCorrUncertaintyTag = cms.string("SubTotalDataMC"),
    addResidualJES = cms.bool(False),
    jetCorrLabelUpToL3 = cms.string("ak5PFL1FastL2L3"),
    jetCorrLabelUpToL3Res = cms.string("ak5PFL1FastL2L3Residual"),
    shiftBy = cms.double(+1) # +1/-1 for +-1 sigma variation
)

objectVariationToMet = cms.EDProducer("ShiftedParticleMETcorrInputProducer",
    srcOriginal = cms.InputTag("selectedPatTaus"),
    srcShifted = cms.InputTag("selectedPatTausVariated")
)

unclusteredCorrections =  [
    [ 'pfCandMETcorr', [ '' ] ],
    [ 'patPFJetMETtype1p2Corr', [ 'type2', 'offset' ] ],
    [ 'patPFJetMETtype2Corr', [ 'type2' ] ],
]
unclusteredVariation = cms.EDProducer("ShiftedMETcorrInputProducer",
    src = cms.VInputTag(),
    uncertainty = cms.double(0.10),
    shiftBy = cms.double(+1) # +1/-1 for +-1 sigma variation
)

def addJESVariationAnalysis(process, dataVersion, prefix, name, prototype, additionalCounters, variation, etaVariation, unclusteredEnergyVariationForMET, doJetVariation=True, doUnclusteredVariation=True, postfix="PFlow"):
    variationName = name
    tauVariationName = name+"TauVariation"
    jetVariationForRawMetName = name+"JetVariationForRawMet"
    jetVariationName = name+"JetVariation"
    rawMetVariationName = name+"RawMetVariation"
    type1MetVariationName = name+"Type1MetVariation"
    type2MetVariationName = name+"Type2MetVariation"
    sequenceName = name+"VariationSequence"
    analysisName = prefix+name
    countersName = analysisName+"Counters"
    pathName = analysisName+"Path"

    sequence = cms.Sequence()
    setattr(process, sequenceName, sequence)
    def add(n, module):
        setattr(process, n, module)
        seq = getattr(process, sequenceName) # I don't know why accessing 'sequence' doesn't work
        seq *= module
        return n

    objectVariationRaw = []
    objectVariationType1p2 = []

    # Tau variation (for analysis)
    tauv = tauVariation.clone(
        src = prototype.tauSelection.src.value(),
        uncertainty = abs(variation),
        shiftBy = math.copysign(1.0, variation)
    )
    add(tauVariationName, tauv)

    # For tau variation for type I MET, we need the selected tau only
    m = cms.EDFilter("HPlusTauSelectorFilter",
        tauSelection = prototype.tauSelection.clone(),
        filter = cms.bool(False)
    )
    selectedTauName = add(name+"SelectedTauForVariation", m)
    m = tauVariation.clone(
        src = selectedTauName
    )
    selectedVariatedTauName = add(name+"SelectedTauVariated", m)
    metCorr = objectVariationToMet.clone(
        srcOriginal = selectedTauName,
        srcShifted = selectedVariatedTauName
    )
    n = add(tauVariationName+"METCorr", metCorr)
    objectVariationRaw.append(cms.InputTag(n))
    objectVariationType1p2.append(cms.InputTag(n))

    # Jet variation for raw MET
    if doJetVariation:
        # Add the necessary jet corrector services
        # It should be problem to add these multiple times with the same name (i.e. in each function call)
        # FIXME: support for chs!
        process.load("JetMETCorrections.Configuration.JetCorrectionServices_cff")
        process.ak5PFL1Fastjet.srcRho = cms.InputTag("kt6PFJetsPFlow", "rho")
        if "Chs" in postfix:
            jetCorrs = ["ak5PFL1Fastjet", "ak5PFL2Relative", "ak5PFL3Absolute", "ak5PFResidual",
                        "ak5PFL1FastL2L3", "ak5PFL1FastL2L3Residual"]
            for corr in jetCorrs:
                m = getattr(process, corr).clone()
                setattr(process, corr+"Chs", m)
                if hasattr(m, "correctors"):
                    m.correctors = [c+"Chs" for c in m.correctors]
            process.ak5PFL1FastjetChs.srcRho = cms.InputTag("kt6PFJetsPFlow", "rho")

        # The residual JES is needed here
        jetvRaw = jetVariation.clone(
            src = prototype.jetSelection.src.value(),
            addResidualJES = True,
            shiftBy = math.copysign(1.0, variation)
        )
        add(jetVariationForRawMetName, jetvRaw)
        metCorr = objectVariationToMet.clone(
            srcOriginal = jetvRaw.src.value(),
            srcShifted = jetVariationForRawMetName
        )
        n = add(jetVariationForRawMetName+"METCorr", metCorr)
        objectVariationRaw.append(cms.InputTag(n))
    
        # For type I MET and analysis
        jetv = jetVariation.clone(
            src = prototype.jetSelection.src.value(),
            shiftBy = math.copysign(1.0, variation)
        )
        add(jetVariationName, jetv)
        metCorr = objectVariationToMet.clone(
            srcOriginal = jetv.src.value(),
            srcShifted = jetVariationName
        )
        n = add(jetVariationName+"METCorr", metCorr)
        objectVariationType1p2.append(cms.InputTag(n))
    
    # Unclustered energy variations
    # This looks a bit complex, but that's how it is in PAT
    unclusteredVariations = []
    if doUnclusteredVariation:
        for src in unclusteredCorrections:
            m = unclusteredVariation.clone(
                src = [cms.InputTag(src[0]+postfix, instanceLabel) for instanceLabel in src[1]],
                uncertainty = abs(unclusteredEnergyVariationForMET),
                shiftBy = math.copysign(1.0, unclusteredEnergyVariationForMET)
            )
            n = add(name+src[0]+"Variation", m)
            unclusteredVariations.extend([ cms.InputTag(n, instanceLabel) for instanceLabel in src[1]  ])
    
    # Propagate tau, jet and unclustered variation to MET objects. The
    # overlap between one jet and the selected tau is taken care of in
    # METSelection.

    # Raw MET
    metrawv = patPFMETCorrections.patType1CorrectedPFMet.clone(
        src = prototype.MET.rawSrc.value(),
        srcType1Corrections = objectVariationRaw + unclusteredVariations
    )
    add(rawMetVariationName, metrawv)

    # Type I MET
    mettype1v = metrawv.clone(
        src = prototype.MET.type1Src.value(),
        srcType1Corrections = objectVariationType1p2 + unclusteredVariations
    )
    add(type1MetVariationName, mettype1v)

    # Type II MET
    #mettype2v = mettype1v.clone(
    #    src = prototype.MET.type2Src.value()
    #)
    #add(type2MetVariationName, mettype2v)

    # Construct the signal analysis module for this variation
    # Use variated taus, jets and MET
    analysis = prototype.clone()
    analysis.tauSelection.src = tauVariationName
    if doJetVariation:
        analysis.jetSelection.src = jetVariationName
    analysis.MET.rawSrc = rawMetVariationName
    analysis.MET.type1Src = type1MetVariationName
    #analysis.MET.type2Src = type2MetVariationName
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
        sequence *
        analysis *
        counters
    )
    setattr(process, pathName, path)
