from HiggsAnalysis.HeavyChHiggsToTauNu.OptimisationScheme import HPlusOptimisationScheme

# Note: Keep number of variations below 200 to keep file sizes reasonable
# Note: Currently it is not possible to vary the tau selection -related variables, because only one JES and MET producer is made (tau selection influences type I MET correction and JES)

# There must be 'optimisation' object
optimisation = HPlusOptimisationScheme()
#optimisation.printOptions() # Uncomment to find out the implemented methods
#optimisation.addTauPtVariation([40.0, 50.0, 60.0, 70., 80.])
#optimisation.addTauIsolationVariation([])
#optimisation.addTauIsolationContinuousVariation([])
#optimisation.addRtauVariation([0.0, 0.7, 0.8])
#optimisation.addJetNumberSelectionVariation(["GEQ3", "GEQ4"])
#optimisation.addJetEtVariation([20.0, 30.0])
#optimisation.addJetBetaVariation(["GT0.0","GT0.5","GT0.7"])
#optimisation.addMETSelectionVariation([60.0, 70.0, 80.0, 90.,100.0])

#optimisation.addBJetLeadingDiscriminatorVariation([0.898, 0.679])
#optimisation.addBJetSubLeadingDiscriminatorVariation([0.679, 0.244])
#optimisation.addBJetEtVariation([])
#optimisation.addBJetNumberVariation(["GEQ1", "GEQ2"])
#import btagScenarios # Pick btag scan points
#optimisation.addBTagVariations(btagScenarios.scenarios)

#optimisation.addDeltaPhiVariation([180.0,170.0,160.0,150.0])
optimisation.addTopRecoVariation(["None","chi","std","Wselection","Bselection"]) # Valid options: None, chi, std, Wselection, Bselection


#import invMassScenarios # Pick invariant mass scan points
#optimisation.addInvariantMassVariation(invMassScenarios.scenarios)

