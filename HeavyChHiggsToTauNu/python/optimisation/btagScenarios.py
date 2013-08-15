from HiggsAnalysis.HeavyChHiggsToTauNu.OptimisationScheme import HPlusOptimisationScheme, Scenario

# There must be 'optimisation' object
optimisation = HPlusOptimisationScheme()

_N = [1, 2]
_leadingDiscr = [("T", 0.898), ("M", 0.679), ("L", 0.244)]
_subLeadingDiscr = _leadingDiscr[1:]

scenarios = []
_subScen = []
for leadName,leadCut in _leadingDiscr:
    scenarios.append(Scenario("N1discr"+leadName,
                              jetNumber = 1,
                              jetNumberCutDirection = "GEQ",
                              leadingDiscriminatorCut = leadCut))
    for subName,subCut in _subLeadingDiscr:
        if subCut > leadCut:
            continue
        _subScen.append(Scenario("N2discr"+leadName+"subdiscr"+subName,
                                 jetNumber = 2,
                                 jetNumberCutDirection = "GEQ",
                                 leadingDiscriminatorCut = leadCut,
                                 subleadingDiscriminatorCut = subCut))
scenarios.extend(_subScen)

optimisation.addBTagVariations(scenarios)
