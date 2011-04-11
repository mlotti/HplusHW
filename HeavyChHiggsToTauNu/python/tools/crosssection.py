import BRdataInterface as br

# All cross sections are in pb
ttCrossSection = 165.0

whDatasetMass = {
    # Spring10
    "TTbar_Htaunu_M80":    80,
    "TTToHpmToTauNu_M90":  90,
    "TTToHpmToTauNu_M100": 100,
    "TTToHpmToTauNu_M120": 120,
    "TTbar_Htaunu_M140":   140,
    "TTbar_Htaunu_M160":   160,

    # Winter10
    "TTToHplusBWB_M90_Winter10": 90,
    "TTToHplusBWB_M100_Winter10": 100,
    "TTToHplusBWB_M120_Winter10": 120,
    "TTToHplusBWB_M140_Winter10": 140,
    "TTToHplusBWB_M160_Winter10": 160,

    # Logical names (see plots.py)
    "TTToHplusBWB_M90": 90,
    "TTToHplusBWB_M100": 100,
    "TTToHplusBWB_M120": 120,
    "TTToHplusBWB_M140": 140,
    "TTToHplusBWB_M150": 150,
    "TTToHplusBWB_M155": 155,
    "TTToHplusBWB_M160": 160,

}

hhDatasetMass = {
    "TToHplusBHminusB_M80": 80,
    "TToHplusBHminusB_M100": 100,
    "TToHplusBHminusB_M120": 120,
    "TToHplusBHminusB_M140": 140,
    "TToHplusBHminusB_M150": 150,
    "TToHplusBHminusB_M155": 155,
    "TToHplusBHminusB_M160": 160,
}

def whTauNuCrossSection(mass, tanbeta, mu=200):
    br_tH = br.getBR_top2bHp(mass, tanbeta, mu)
    br_Htaunu = br.getBR_Hp2tau(mass, tanbeta, mu)

    return 2 * ttCrossSection * br_tH * (1-br_tH) * br_Htaunu


def hhTauNuCrossSection(mass, tanbeta, mu=200):
    br_tH = br.getBR_top2bHp(mass, tanbeta, mu)
    br_Htaunu = br.getBR_Hp2tau(mass, tanbeta, mu)

    return ttCrossSection * br_tH*br_tH * br_Htaunu*br_Htaunu


def setHplusCrossSections(datasets, tanbeta, mu=200):
    for name, mass in whMass.iteritems():
        if not datasets.hasDataset(name):
            continue

        crossSection = whTauNuCrossSection(mass, tanbeta, mu)
        datasets.getDataset(name).setCrossSection(crossSection)
        print "Setting %s cross section to %f pb" % (name, crossSection)

    for name, mass in hhMass.iteritems():
        if not datasets.hasDataset(name):
            continue

        crossSection = hhCrossSection(mass, tanbeta, mu)
        datasets.getDataset(name).setCrossSection(crossSection)
        print "Setting %s cross section to %f pb" % (name, crossSection)

def printHplusCrossSections():
    mu = 200

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

            print "%10d | %10f | %13f | %24f | %27f |" % (mass, br_tH, br_Htaunu, whTauNuCrossSection(mass, tanbeta, mu), hhTauNuCrossSection(mass, tanbeta, mu))


if __name__ == "__main__":
    printHplusCrossSections()
