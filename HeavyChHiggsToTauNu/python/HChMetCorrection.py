import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.HChTauFilter_cfi as tauFilter
import PhysicsTools.PatUtils.patPFMETCorrections_cff as patPFMETCorrections

METType1Name = "patType1CorrectedPFMet"

def addCorrectedMet(process, dataVersion, tauSelection, jetSelection):
    sequence = cms.Sequence()

    # First re-do the tau selection
    #
    # Apply a bit looser pt cut here for tau energy scale variation.
    # This way we can produce the type I MET only once for the
    # variations, and just take later into account the variation
    # (instead of doing the tau ID and jet cleaning for each variation)
    process.selectedPatTausForMetCorr = tauFilter.hPlusTauPtrSelectorFilter.clone(
        tauSelection = tauSelection.clone(),
        filter = cms.bool(False)
    )
    process.selectedPatTausForMetCorr.tauSelection.ptCut = tauSelection.ptCut.value()*0.9
    tauName = "selectedPatTausForMetCorr"

    # Then clean jet collection from the selected tau
    process.selectedPatJetsTauCleaned = cms.EDFilter("PATJetSelector",
        src = cms.InputTag(jetSelection.src.value()),
        cut = cms.string(""),
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
        )
    )
    jetName = "selectedPatJetsTauCleaned"
    metName = "patMETsPF"

    # Then compute the type I correction for MET with the cleaned jets
    process.load("PhysicsTools.PatUtils.patPFMETCorrections_cff")
    process.selectedPatJetsForMETtype1p2Corr.src = jetName
    process.selectedPatJetsForMETtype2Corr.src = jetName

    process.patType1CorrectedPFMet.src = metName
    process.patPFJetMETtype1p2Corr.skipMuons = False
    process.patPFJetMETtype2Corr.skipMuons = False
    if dataVersion.isData():
        process.patPFJetMETtype1p2Corr.jetCorrLabel = "L2L3Residual"
        process.patPFJetMETtype2Corr.jetCorrLabel = "L2L3Residual"

    process.patType1p2CorrectedPFMet.src = metName

    sequence = cms.Sequence(
        process.selectedPatTausForMetCorr
        * process.selectedPatJetsTauCleaned
        * process.selectedPatJetsForMETtype1p2Corr
        * process.selectedPatJetsForMETtype2Corr 
        * process.patPFJetMETtype1p2Corr
        * process.patPFJetMETtype2Corr 
        * process.patType1CorrectedPFMet
        # * process.patType1p2CorrectedPFMet # we need more stuff in event in order to calculate type II MET
    )

    return sequence
