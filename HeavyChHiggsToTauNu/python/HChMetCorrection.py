import FWCore.ParameterSet.Config as cms

import HiggsAnalysis.HeavyChHiggsToTauNu.HChTauFilter_cfi as tauFilter
import PhysicsTools.PatUtils.patPFMETCorrections_cff as patPFMETCorrections

# Note that the Type I and II MET produced here are calculated with
# all jets. In order to take into account the selected tau further
# correction is needed (implemented in METSelection.cc) (the hadronic
# jet corresponding to the tau should not be included in type I
# correction)
def addCorrectedMet(process, signalAnalysis, postfix=""):
    sequence = cms.Sequence()

    # For jets |eta| < 4.7
    # 'type1'   difference corrected - L1-corrected jet energy for jets of (corrected) Pt > 10 GeV
    # 'type2'   unclustered energy due to jets of (corrected) Pt < 10 GeV (calculated with uncorrected pt)
    # 'offset'  offset energy, i.e. sum of energy attributed to pile-up/underlying event
    #           calculated for pt>10 jets, as difference L1-corrected - uncorrected
    # See JetMETCorrections/Type1MET/interface/PFJetMETcorrInputProducerT.h for more details
    type1p2Corr = "patPFJetMETtype1p2Corr"+postfix

    # For jets |eta| > 4.7
    # Only 'type2' is relevant
    type2Corr = "patPFJetMETtype2Corr"+postfix

    # Unclustered energy due to unclustered PFCandidates
    pfCandCorr = "pfCandMETcorr"+postfix


    # Apply type 1 corrections to raw PF MET in PAT
    m = patPFMETCorrections.patType1CorrectedPFMet.clone(
        src = signalAnalysis.MET.rawSrc.value(),
        srcType1Corrections = [cms.InputTag(type1p2Corr, "type1")],
    )
    type1Name = "patType1CorrectedPFMet"+postfix
    setattr(process, type1Name, m)
    sequence *= m

    # Apply type 1 and type 2 corrections to raw PF MET in PAT
    m = patPFMETCorrections.patType1p2CorrectedPFMet.clone(
        src = signalAnalysis.MET.rawSrc.value(),
        srcType1Corrections = [cms.InputTag(type1p2Corr, "type1")],
        srcUnclEnergySums = [
            cms.InputTag(type1p2Corr, 'type2' ),
            cms.InputTag(type2Corr,   'type2' ),
            cms.InputTag(type1p2Corr, 'offset'),
            cms.InputTag(pfCandCorr),
        ]
    )
    type1p2Name = "patType1p2CorrectedPFMet"+postfix
    setattr(process, type1p2Name, m)
    sequence *= m

    if m.type2CorrFormula.value() != "A":
        raise Exception("Assumption that Type II MET correction formula would be constant failed. METSelection.cc should be modified accordingly")
    if m.type2CorrParameter.A.value() != signalAnalysis.MET.type2ScaleFactor.value():
        raise Exception("Correction factor for type II MET differ in signalAnalysis.MET.type2ScaleFactor (%f) and %s (%f)" % (signalAnalysis.MET.type2ScaleFactor.value(), type1p2Name, m.type2CorrParameter.A.value()))

    setattr(process, "patMetCorrSequence"+postfix, sequence)

    signalAnalysis.MET.type1Src = type1Name
    signalAnalysis.MET.type2Src = type1p2Name


    return sequence
