from HiggsAnalysis.HeavyChHiggsToTauNu.OptimisationScheme import HPlusOptimisationScheme

# Note: Keep number of variations below 200 to keep file sizes reasonable
# Note: Currently it is not possible to vary the tau selection -related variables, because only one JES and MET producer is made (tau selection influences type I MET correction and JES)

# There must be 'optimisation' object
optimisation = HPlusOptimisationScheme()
#optimisation.printOptions() # Uncomment to find out the implemented methods

optimisation.addTopRecoVariation(["None","chi","Wselection","Bselection"]) # Valid options: None, chi, std, Wselection, Bselection
#optimisation.addTopRecoVariation(["chi"])
#optimisation.addTopRecoVariation(["None","chi","Bselection"])
