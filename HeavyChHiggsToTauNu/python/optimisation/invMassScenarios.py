from HiggsAnalysis.HeavyChHiggsToTauNu.OptimisationScheme import HPlusOptimisationScheme, Scenario

# There must be 'optimisation' object
optimisation = HPlusOptimisationScheme()

_neutrinoPzSolutionSelectionMethods = ["DeltaEtaMax", "Smaller"]
scenarios = []
for currentPzSelectionMethod in _neutrinoPzSolutionSelectionMethods:
        scenarios.extend([
            Scenario("RecoPZSelection"+currentPzSelectionMethod+"TopInvMassCutNone",
                     topInvMassLowerCut = -1, # negative value means no cut
                     topInvMassUpperCut = -1, # negative value means no cut
                     pzSelectionMethod = currentPzSelectionMethod
                 ),
            Scenario("RecoPZSelection"+currentPzSelectionMethod+"TopInvMassCutLoose",
                     topInvMassLowerCut = 100, # negative value means no cut
                     topInvMassUpperCut = 240, # negative value means no cut
                     pzSelectionMethod = currentPzSelectionMethod
                 ),
            Scenario("RecoPZSelection"+currentPzSelectionMethod+"TopInvMassCutMedium",
                     topInvMassLowerCut = 140, # negative value means no cut
                     topInvMassUpperCut = 200, # negative value means no cut
                     pzSelectionMethod = currentPzSelectionMethod
                 ),
            Scenario("RecoPZSelection"+currentPzSelectionMethod+"TopInvMassCutTight",
                     topInvMassLowerCut = 157, # negative value means no cut
                     topInvMassUpperCut = 187, # negative value means no cut
                     pzSelectionMethod = currentPzSelectionMethod
                 ),
        ])

optimisation.addInvariantMassVariation(scenarios)

