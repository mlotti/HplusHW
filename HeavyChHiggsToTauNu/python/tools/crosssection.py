import BRdataInterface as br

# All cross sections are in pb
ttCrossSection = 165.0
defaultMu = 200

whDatasetMass = {
    # Logical names (see plots.py)
    "TTToHplusBWB_M80": 80,
    "TTToHplusBWB_M90": 90,
    "TTToHplusBWB_M100": 100,
    "TTToHplusBWB_M120": 120,
    "TTToHplusBWB_M140": 140,
    "TTToHplusBWB_M150": 150,
    "TTToHplusBWB_M155": 155,
    "TTToHplusBWB_M160": 160,

}

hhDatasetMass = {
    "TTToHplusBHminusB_M80": 80,
    "TTToHplusBHminusB_M90": 90,
    "TTToHplusBHminusB_M100": 100,
    "TTToHplusBHminusB_M120": 120,
    "TTToHplusBHminusB_M140": 140,
    "TTToHplusBHminusB_M150": 150,
    "TTToHplusBHminusB_M155": 155,
    "TTToHplusBHminusB_M160": 160,
}

def whTauNuCrossSectionMSSM(mass, tanbeta, mu):
    br_tH = br.getBR_top2bHp(mass, tanbeta, mu)
    br_Htaunu = br.getBR_Hp2tau(mass, tanbeta, mu)
    return whTauNuCrossSection(br_tH, br_Htaunu)

def whTauNuCrossSection(br_tH, br_Htaunu):
    return 2 * ttCrossSection * br_tH * (1-br_tH) * br_Htaunu


def hhTauNuCrossSectionMSSM(mass, tanbeta, mu):
    br_tH = br.getBR_top2bHp(mass, tanbeta, mu)
    br_Htaunu = br.getBR_Hp2tau(mass, tanbeta, mu)
    return hhTauNuCrossSection(br_tH, br_Htaunu)

def hhTauNuCrossSection(br_tH, br_Htaunu):
    return ttCrossSection * br_tH*br_tH * br_Htaunu*br_Htaunu


def _setHplusCrossSectionsHelper(massList, datasets, function):
    for name, mass in massList:
        if not datasets.hasDataset(name):
            continue
        crossSection = function(mass)
        datasets.getDataset(name).setCrossSection(crossSection)
        print "Setting %s cross section to %f pb" % (name, crossSection)

def _setHplusCrossSections(datasets, whFunction, hhFunction):
    _setHplusCrossSectionsHelper(whDatasetMass.iteritems(), datasets, whFunction)
    _setHplusCrossSectionsHelper(hhDatasetMass.iteritems(), datasets, hhFunction)

def setHplusCrossSectionsToTop(datasets):
    function = lambda mass: ttCrossSection
    _setHplusCrossSections(datasets, function, function)

def setHplusCrossSectionsToMSSM(datasets, tanbeta=20, mu=defaultMu):
    _setHplusCrossSections(datasets,
                           lambda mass: whTauNuCrossSectionMSSM(mass, tanbeta, mu),
                           lambda mass: hhTauNuCrossSectionMSSM(mass, tanbeta, mu))

def setHplusCrossSectionsToBR(datasets, br_tH, br_Htaunu):
    _setHplusCrossSections(datasets,
                           lambda mass: whTauNuCrossSection(br_tH, br_Htaunu),
                           lambda mass: hhTauNuCrossSection(br_tH, br_Htaunu))

def setHplusCrossSections(datasets, tanbeta=20, mu=defaultMu, toTop=False):
    if toTop:
        setHplusCrossSectionsToTop(datasets)
    else:
        setHplusCrossSectionsToMSSM(tanbeta, mu)

def printHplusCrossSections(tanbetas=[10, 20, 30, 40], mu=defaultMu):
    print "ttbar cross section %.1f pb" % ttCrossSection
    print "mu %.1f" % mu
    print
    for tanbeta in [10, 20, 30, 40]:
        print "="*98
        print "tan(beta) = %d" % tanbeta
        print "H+ M (GeV) | BR(t->bH+) | BR(H+->taunu) | sigma(tt->tbH+->tbtaunu) | sigma(tt->bbH+H-->bbtautau) |"
        for mass in [90, 100, 120, 140, 150, 155, 160]:
            br_tH = br.getBR_top2bHp(mass, tanbeta, mu)
            br_Htaunu = br.getBR_Hp2tau(mass, tanbeta, mu)

            print "%10d | %10f | %13f | %24f | %27f |" % (mass, br_tH, br_Htaunu, whTauNuCrossSectionMSSM(mass, tanbeta, mu), hhTauNuCrossSectionMSSM(mass, tanbeta, mu))


if __name__ == "__main__":
    printHplusCrossSections()
