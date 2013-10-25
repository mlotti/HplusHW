from HiggsAnalysis.HeavyChHiggsToTauNu.OptimisationScheme import HPlusOptimisationScheme, Scenario

# There must be 'optimisation' object
optimisation = HPlusOptimisationScheme()

_N = [3, 4]
_pt = [20, 25, 30]

scenarios = []
_subScen = []

for n in _N:
    for pt in _pt:
        scenarios.append(Scenario("N%dpt%d"%(n,pt),
                                  jetNumber = n,
                                  jetNumberCutDirection = "GEQ",
                                  ptCut = pt))

scenarios.extend(_subScen)

optimisation.addJetVariations(scenarios)
