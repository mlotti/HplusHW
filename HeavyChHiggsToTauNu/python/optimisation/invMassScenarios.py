import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.OptimisationScheme import HPlusOptimisationScheme

# There must be 'optimisation' object
optimisation = HPlusOptimisationScheme()

_neutrinoPzSolutionSelectionMethods = ["DeltaEtaMax", "Smaller"]
values = []
for currentPzSelectionMethod in _neutrinoPzSolutionSelectionMethods:
        values.extend([
                ("RecoPZSelection"+currentPzSelectionMethod+"TopInvMassCutNone",
                 cms.PSet(topInvMassLowerCut = cms.untracked.double(-1), # negative value means no cut
                          topInvMassUpperCut = cms.untracked.double(-1), # negative value means no cut     
                          pzSelectionMethod = cms.untracked.string(currentPzSelectionMethod)
                  )
                ),
                ("RecoPZSelection"+currentPzSelectionMethod+"TopInvMassCutLoose",
                 cms.PSet(topInvMassLowerCut = cms.untracked.double(100), # negative value means no cut
                          topInvMassUpperCut = cms.untracked.double(240), # negative value means no cut
                          pzSelectionMethod = cms.untracked.string(currentPzSelectionMethod)
                  ),
                ),
                ("RecoPZSelection"+currentPzSelectionMethod+"TopInvMassCutMedium",
                 cms.PSet(topInvMassLowerCut = cms.untracked.double(140), # negative value means no cut
                          topInvMassUpperCut = cms.untracked.double(200), # negative value means no cut
                          pzSelectionMethod = cms.untracked.string(currentPzSelectionMethod)
                  ),
                ),
                ("RecoPZSelection"+currentPzSelectionMethod+"TopInvMassCutTight",
                 cms.PSet(topInvMassLowerCut = cms.untracked.double(157), # negative value means no cut
                          topInvMassUpperCut = cms.untracked.double(187), # negative value means no cut
                          pzSelectionMethod = cms.untracked.string(currentPzSelectionMethod)
                  ),
                )
        ])

optimisation.addInvariantMassVariation(values)
