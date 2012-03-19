import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.HChTauFilter_cfi as tauFilter
import PhysicsTools.PatUtils.patPFMETCorrections_cff as patPFMETCorrections

def addCorrectedMet(process, dataVersion, tauSelection, jetSelection, metRaw = "patMETsPF", pfCandMETcorrPostfix="", postfix=""):
    sequence = cms.Sequence()

    # First re-do the tau selection
    #
    # Apply a bit looser pt cut here for tau energy scale variation.
    # This way we can produce the type I MET only once for the
    # variations, and just take later into account the variation
    # (instead of doing the tau ID and jet cleaning for each variation)
    m = tauFilter.hPlusTauPtrSelectorFilter.clone(
        tauSelection = tauSelection.clone(),
        filter = cms.bool(False)
    )
    tauName = "selectedPatTausForMetCorr"+postfix
    setattr(process, tauName, m)
    sequence *= m

    # Then clean jet collection from the selected tau
    m = cms.EDProducer("PATJetCleaner",
        src = cms.InputTag(jetSelection.src.value()),
        preselection = cms.string(""),
        checkOverlaps = cms.PSet(
            taus = cms.PSet(
                src                 = cms.InputTag(tauName),
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
    jetName = "selectedPatJetsTauCleaned"+postfix
    setattr(process, jetName, m)
    sequence *= m

    # Then compute the type I correction for MET with the cleaned jets
    # Select jets with |eta| < 4.7
    m = patPFMETCorrections.selectedPatJetsForMETtype1p2Corr.clone(
        src = jetName
    )
    jetsForMETtype1p2 = "selectedPatJetsForMETtype1p2Corr"+postfix
    setattr(process, jetsForMETtype1p2, m)
    sequence *= m

    # Select jets with |eta| > 4.7
    m = patPFMETCorrections.selectedPatJetsForMETtype2Corr.clone(
        src = jetName
    )
    jetsForMETtype2 = "selectedPatJetsForMETtype2Corr"+postfix
    setattr(process, jetsForMETtype2, m)
    sequence *= m

    # Calculate corrections for type 1 and 2 from jets |eta| < 4.7
    m = patPFMETCorrections.patPFJetMETtype1p2Corr.clone(
        src = jetsForMETtype1p2,
        skipMuons = False
    )
    if dataVersion.isData():
        m.jetCorrLabel = "L2L3Residual"
    type1p2Corr = "patPFJetMETtype1p2Corr"+postfix
    setattr(process, type1p2Corr, m)
    sequence *= m

    # Calculate correction for type 2 from jets |eta| > 4.7
    m = patPFMETCorrections.patPFJetMETtype2Corr.clone(
        src = jetsForMETtype2,
        skipMuons = False
    )
    if dataVersion.isData():
        m.jetCorrLabel = "L2L3Residual"
    type2Corr = "patPFJetMETtype2Corr"+postfix
    setattr(process, type2Corr, m)
    sequence *= m

    # Apply type 1 corrections to raw PF MET in PAT
    m = patPFMETCorrections.patType1CorrectedPFMet.clone(
        src = metRaw,
        srcType1Corrections = [cms.InputTag(type1p2Corr, "type1")],
    )
    type1Name = "patType1CorrectedPFMet"+postfix
    setattr(process, type1Name, m)
    sequence *= m

    # Appluy type 1 and type 2 corrections ro raw PF MET in PAT
    m = patPFMETCorrections.patType1p2CorrectedPFMet.clone(
        src = metRaw,
        srcType1Corrections = [cms.InputTag(type1p2Corr, "type1")],
        srcUnclEnergySums = [
            cms.InputTag(type1p2Corr, 'type2' ),
            cms.InputTag(type2Corr,   'type2' ),
            cms.InputTag(type1p2Corr, 'offset'),
            cms.InputTag('pfCandMETcorr'+pfCandMETcorrPostfix),
        ]
    )
    type1p2Name = "patType1p2CorrectedPFMet"+postfix
    setattr(process, type1p2Name, m)
    sequence *= m

    setattr(process, "patMetCorrSequence"+postfix, sequence)

    return (sequence, type1Name, type1p2Name)
