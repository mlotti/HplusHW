from HiggsAnalysis.HeavyChHiggsToTauNu.OptimisationScheme import HPlusOptimisationScheme, Scenario

# There must be 'optimisation' object
optimisation = HPlusOptimisationScheme()

_pt = [50,60,70,80,90]

scenarios = []

for pt in _pt:
    scenarios.append(Scenario("%d"%(pt),
                              METCut = pt))

optimisation.addMETVariations(scenarios)
