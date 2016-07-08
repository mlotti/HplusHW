import FWCore.ParameterSet.Config as cms
import PhysicsTools.PatUtils.patPFMETCorrections_cff as patPFMETCorrections
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTauFilter_cfi as TauFilter

def _doCommon(process, prefix, name, prototype, direction, postfix):
    if not postfix in ["", "Chs"]:
        raise Exception("There are several assumptions of standard PAT, or PF2PAT with Chs-postfix-only workflow")

    if direction not in ["Up", "Down"]:
        raise Exception("direction should be 'Up' or 'Down', was '%s'" % direction)

    analysisName = prefix+name
    pathName = analysisName+"Path"

    analysis = prototype.clone()
    setattr(process, analysisName, analysis)
    # Configure the event counter
    analysis.eventCounter.printMainCounter = cms.untracked.bool(False)

    path = cms.Path(
        process.commonSequence *
        analysis
    )
    setattr(process, pathName, path)

    return (analysis, analysisName)

def addJESVariation(process, prefix, name, prototype, direction, postfix=""):
    (analysis, name) = _doCommon(process, prefix, name, prototype, direction, postfix)

    analysis.jetSelection.src = "shiftedPatJetsEn%sForCorrMEt%s" % (direction, postfix)
    analysis.MET.rawSrc = "patPFMetJetEn%s%s" % (direction, postfix)
    analysis.MET.type1Src = "patType1CorrectedPFMetJetEn%s%s" % (direction, postfix)
    analysis.MET.type2Src = "patType1p2CorrectedPFMetJetEn%s%s" % (direction, postfix)

    return name

def addJERVariation(process, prefix, name, prototype, direction, postfix=""):
    (analysis, name) = _doCommon(process, prefix, name, prototype, direction, postfix)

    analysis.jetSelection.src = "smearedPatJetsRes%s%s" % (direction, postfix)
    analysis.MET.rawSrc = "patPFMetJetRes%s%s" % (direction, postfix)
    analysis.MET.type1Src = "patType1CorrectedPFMetJetRes%s%s" % (direction, postfix)
    analysis.MET.type2Src = "patType1p2CorrectedPFMetJetRes%s%s" % (direction, postfix)

    return name

def addUESVariation(process, prefix, name, prototype, direction, postfix=""):
    (analysis, name) = _doCommon(process, prefix, name, prototype, direction, postfix)

    analysis.MET.rawSrc = "patPFMetUnclusteredEn%s%s" % (direction, postfix)
    analysis.MET.type1Src = "patType1CorrectedPFMetUnclusteredEn%s%s" % (direction, postfix)
    analysis.MET.type2Src = "patType1p2CorrectedPFMetUnclusteredEn%s%s" % (direction, postfix)

    return name

tauVariation = cms.EDProducer("ShiftedPATTauProducer",
    src = cms.InputTag("selectedPatTaus"),
    uncertainty = cms.double(0.03),
    shiftBy = cms.double(+1), # +1/-1 for +-1 sigma variation
)
objectVariationToMet = cms.EDProducer("ShiftedParticleMETcorrInputProducer",
    srcOriginal = cms.InputTag("selectedPatTaus"),
    srcShifted = cms.InputTag("selectedPatTausVariated")
)
def addTESVariation(process, prefix, name, prototype, direction, postfix="", histogramAmbientLevel="Systematics"):
    tauVariationName = name+"TauVariation"
    analysisName = prefix+name
    rawMetVariationName = analysisName+"RawMetVariation"
    type1MetVariationName = analysisName+"Type1MetVariation"
    type2MetVariationName = analysisName+"Type2MetVariation"
    sequenceName = analysisName+"VariationSequence"
    analysisName = prefix+name
    pathName = analysisName+"Path"

    sequence = cms.Sequence()
    setattr(process, sequenceName, sequence)
    def add(n, module):
        if not hasattr(process, n):
            setattr(process, n, module)
            mod = module
        else:
            mod = getattr(process, n)
        seq = getattr(process, sequenceName) # I don't know why accessing 'sequence' doesn't work
        seq *= mod
        return n

    # Variation of all tau candidates
    # It is enough to do this once per job (nothing depends on tau ID)
    tauv = tauVariation.clone(
        src = prototype.tauSelection.src.value(),
    )
    if direction == "Up":
        tauv.shiftBy = +1
    elif direction == "Down":
        tauv.shiftBy = -1
    else:
        raise Exception("direction should be 'Up' or 'Down', was '%s'" % direction)
    add(tauVariationName, tauv)

    # To propagate tau variation to type I MET, we need the selected tau only
    # First do the tau ID to get the selected tau, then variate it, and propagate to MET

    # Repeat the procedure for each call of addTESVariation in case
    # tauID parameters have changed (e.g. due to optimization). This
    # could be optimized by inspecting if tauID parameters have really
    # changed. That would be more complex, and it looks like the time
    # penalty of this KISS approach is not that much (couple of
    # percents with full systematics).
    m = TauFilter.hPlusTauSelectorFilter.clone(
        tauSelection = prototype.tauSelection.clone(),
        vertexSrc = prototype.primaryVertexSelection.selectedSrc.value(),
        filter = False,
        histogramAmbientLevel = histogramAmbientLevel
    )
    if histogramAmbientLevel == "Systematics":
        m.eventCounter.enabled = cms.untracked.bool(False)
    selectedTauName = add(analysisName+"SelectedTauForVariation", m)
    m = tauv.clone(
        src = selectedTauName
    )
    selectedVariatedTauName = add(analysisName+"SelectedTauVariated", m)
    metCorr = objectVariationToMet.clone(
        srcOriginal = selectedTauName,
        srcShifted = selectedVariatedTauName
    )
    variationMetCorrection = add(selectedTauName+"METCorr", metCorr)

    # Raw MET
    metrawv = patPFMETCorrections.patType1CorrectedPFMet.clone(
        src = prototype.MET.rawSrc.value(),
        srcType1Corrections = [cms.InputTag(variationMetCorrection)]
    )
    add(rawMetVariationName, metrawv)

    # Type I MET
    mettype1v = metrawv.clone(
        src = prototype.MET.type1Src.value(),
    )
    add(type1MetVariationName, mettype1v)

    # Type II MET
    mettype2v = mettype1v.clone(
        src = prototype.MET.type2Src.value()
    )
    add(type2MetVariationName, mettype2v)

    # Construct the signal analysis module for this variation
    analysis = prototype.clone()
    analysis.tauSelection.src = tauVariationName
    analysis.MET.rawSrc = rawMetVariationName
    analysis.MET.type1Src = type1MetVariationName
    analysis.MET.type2Src = type2MetVariationName
    setattr(process, analysisName, analysis)

    # Configure the event counter
    analysis.eventCounter.printMainCounter = cms.untracked.bool(False)

    # Construct the path
    path = cms.Path(
        process.commonSequence *
        sequence *
        analysis
    )
    setattr(process, pathName, path)

    return analysisName
