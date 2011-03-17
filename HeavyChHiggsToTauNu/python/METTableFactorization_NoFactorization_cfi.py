import FWCore.ParameterSet.Config as cms

# Default file for the "no factorization coefficients available" case
# Do not edit unless you are certain about what you are doing

ptDummy = cms.untracked.vdouble( *(
  1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.
) )

METTableFactorizationCoefficients = cms.untracked.PSet(
factorizationSourceName = cms.untracked.string('NoFactorization'),

METTables_Coefficients = ptDummy,
METTables_CoefficientUncertainty = ptDummy,

)
