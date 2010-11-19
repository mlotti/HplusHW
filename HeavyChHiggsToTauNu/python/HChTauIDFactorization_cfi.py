import FWCore.ParameterSet.Config as cms

tauIDFactorizationParameters = cms.untracked.PSet(
  # Note: do not change name!
  etaBinLowEdges = cms.untracked.vdouble(
    -2.4, -2.2, -2.0, -1.8, -1.6, -1.4, -1.2, -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4
  ),
  
  # Note: do not change name!
  ptBinLowEdges = cms.untracked.vdouble(
    20., 30., 40., 50., 60., 70., 80., 90., 100., 120., 150.
  ),
  
  # import the relevant config file
  factorizationTables = cms.untracked.PSet(),
   
  # The options for choosing the desired factorization table (options: byPt, byEta, byPtVsEta)
  factorizationTableType = cms.untracked.string("byPt")
)

import HiggsAnalysis.HeavyChHiggsToTauNu.FactorizationMapBTau_141950_148864_tctau_factorized_cfi as coefficientSource
tauIDFactorizationParameters.factorizationTables = coefficientSource.tauIDFactorizationCoefficients

#print "TauID factorization source: ",factorizationSourceName
#print "TauID factorization type: ",factorizationTableType
