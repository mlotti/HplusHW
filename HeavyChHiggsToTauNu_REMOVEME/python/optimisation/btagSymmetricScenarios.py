from HiggsAnalysis.HeavyChHiggsToTauNu.OptimisationScheme import HPlusOptimisationScheme, Scenario

# There must be 'optimisation' object
optimisation = HPlusOptimisationScheme()

_N = [1, 2]
_leadingDiscr = [("T", 0.898), ("M", 0.679), ("L", 0.244)]
_subLeadingDiscr = _leadingDiscr[1:]

scenarios = []
_subScen = []

# Symmetric cuts for at least 1 b jet
for leadName,leadCut in _leadingDiscr:
    scenarios.append(Scenario("N1discr"+leadName,
                              jetNumber = 1,
                              jetNumberCutDirection = "GEQ",
                              leadingDiscriminatorCut = leadCut))


# Symmetric cuts for at least 1 b jet
for leadName,leadCut in _leadingDiscr:
    if leadName in ["L","M"]:
        scenarios.append(Scenario("N2discr"+leadName,
                                  jetNumber = 2,
                                  jetNumberCutDirection = "GEQ",
                                  leadingDiscriminatorCut = leadCut))

scenarios.extend(_subScen)

optimisation.addBTagVariations(scenarios)
