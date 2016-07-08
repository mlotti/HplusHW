import FWCore.ParameterSet.Config as cms

# Default file for the "no factorization coefficients available" case
# Do not edit unless you are certain about what you are doing

ptDummy = cms.untracked.vdouble( *(
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.
) )

etaDummy = cms.untracked.vdouble( *(
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.
) )

ptVsEtaDummy = cms.untracked.vdouble( *(
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.
) )

tauIDFactorizationCoefficients = cms.untracked.PSet(
factorizationSourceName = cms.untracked.string('NoFactorization'),

tauIDFactorizationByPt_signalAnalysisTauSelectionShrinkingConeCutBased_Coefficients = ptDummy,
tauIDFactorizationByPt_signalAnalysisTauSelectionShrinkingConeCutBased_CoefficientUncertainty = ptDummy,
tauIDFactorizationByEta_signalAnalysisTauSelectionShrinkingConeCutBased_Coefficients = etaDummy,
tauIDFactorizationByEta_signalAnalysisTauSelectionShrinkingConeCutBased_CoefficientUncertainty = etaDummy,
tauIDFactorizationByPtVsEta_signalAnalysisTauSelectionShrinkingConeCutBased_Coefficients = ptVsEtaDummy,
tauIDFactorizationByPtVsEta_signalAnalysisTauSelectionShrinkingConeCutBased_CoefficientUncertainty = ptVsEtaDummy,

tauIDFactorizationByPt_signalAnalysisTauSelectionShrinkingConeTaNCBased_Coefficients = ptDummy,
tauIDFactorizationByPt_signalAnalysisTauSelectionShrinkingConeTaNCBased_CoefficientUncertainty = ptDummy,
tauIDFactorizationByEta_signalAnalysisTauSelectionShrinkingConeTaNCBased_Coefficients = etaDummy,
tauIDFactorizationByEta_signalAnalysisTauSelectionShrinkingConeTaNCBased_CoefficientUncertainty = etaDummy,
tauIDFactorizationByPtVsEta_signalAnalysisTauSelectionShrinkingConeTaNCBased_Coefficients = ptVsEtaDummy,
tauIDFactorizationByPtVsEta_signalAnalysisTauSelectionShrinkingConeTaNCBased_CoefficientUncertainty = ptVsEtaDummy,

tauIDFactorizationByPt_signalAnalysisTauSelectionHPSTauBased_Coefficients = ptDummy,
tauIDFactorizationByPt_signalAnalysisTauSelectionHPSTauBased_CoefficientUncertainty = ptDummy,
tauIDFactorizationByEta_signalAnalysisTauSelectionHPSTauBased_Coefficients = etaDummy,
tauIDFactorizationByEta_signalAnalysisTauSelectionHPSTauBased_CoefficientUncertainty = etaDummy,
tauIDFactorizationByPtVsEta_signalAnalysisTauSelectionHPSTauBased_Coefficients = ptVsEtaDummy,
tauIDFactorizationByPtVsEta_signalAnalysisTauSelectionHPSTauBased_CoefficientUncertainty = ptVsEtaDummy,

tauIDFactorizationByPt_signalAnalysisTauSelectionCaloTauCutBased_Coefficients = ptDummy,
tauIDFactorizationByPt_signalAnalysisTauSelectionCaloTauCutBased_CoefficientUncertainty = ptDummy,
tauIDFactorizationByEta_signalAnalysisTauSelectionCaloTauCutBased_Coefficients = etaDummy,
tauIDFactorizationByEta_signalAnalysisTauSelectionCaloTauCutBased_CoefficientUncertainty = etaDummy,
tauIDFactorizationByPtVsEta_signalAnalysisTauSelectionCaloTauCutBased_Coefficients = ptVsEtaDummy,
tauIDFactorizationByPtVsEta_signalAnalysisTauSelectionCaloTauCutBased_CoefficientUncertainty = ptVsEtaDummy,

tauIDFactorizationByPt_signalAnalysisTauSelectionCombinedHPSTaNCBased_Coefficients = ptDummy,
tauIDFactorizationByPt_signalAnalysisTauSelectionCombinedHPSTaNCBased_CoefficientUncertainty = ptDummy,
tauIDFactorizationByEta_signalAnalysisTauSelectionCombinedHPSTaNCBased_Coefficients = etaDummy,
tauIDFactorizationByEta_signalAnalysisTauSelectionCombinedHPSTaNCBased_CoefficientUncertainty = etaDummy,
tauIDFactorizationByPtVsEta_signalAnalysisTauSelectionCombinedHPSTaNCBased_Coefficients = ptVsEtaDummy,
tauIDFactorizationByPtVsEta_signalAnalysisTauSelectionCombinedHPSTaNCBased_CoefficientUncertainty = ptVsEtaDummy

)
