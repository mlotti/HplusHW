# All cross sections are in pb

ttCrossSection = 165.0

# Calculated by Ritva with FeynHiggs 2.7.3, from e-mail 2010-10-06
hplusBranchRatio = [
    [ # tan(beta) = 10
        (0.02436, 0.938), # M=80 (81 actually)
        (0.02139, 0.969), # M=90
        (0.01799, 0.979), # M=100
        (0.01124, 0.986), # M=120
        (0.00526, 0.988), # M=140
        (0.00108, 0.989)  # M=160
    ],
    [ # tan(beta) = 20
        (0.06077 ,  0.958 ), # M=82
        (0.05420 ,  0.972 ),
        (0.04569 ,  0.977 ),
        (0.02854 ,  0.982 ),
        (0.01318 ,  0.984 ),
        (0.002501,  0.9857)
    ],
    [ # tan(beta) = 30
        (0.1110  , 0.967), # M=86
        (0.1049  , 0.972),
        (0.08913 , 0.977),
        (0.05646 , 0.981),
        (0.02628 , 0.983),
        (0.004897, 0.985)
    ],
    [ # tan(beta) = 40
        (0, 0), # No meaningful value for M<90
        (0.16296, 0.971),
        (0.13972, 0.977),
        (0.09024, 0.981),
        (0.04271, 0.983),
        (0.00798, 0.985)
    ]
]

hplusMassIndex = {80: 0,
                  90: 1,
                  100: 2,
                  120: 3,
                  140: 4,
                  160: 5}

hplusTanBetaIndex = {10: 0,
                     20: 1,
                     30: 2,
                     40: 3}

hplusDatasetMass = {
    "TTbar_Htaunu_M80":    80,
    "TTToHpmToTauNu_M90":  90,
    "TTToHpmToTauNu_M100": 100,
    "TTToHpmToTauNu_M120": 120,
    "TTbar_Htaunu_M140":   140,
    "TTbar_Htaunu_M160":   160}

def hplusTauNuBRs(mass, tanbeta):
    if not mass in hplusMassIndex:
        raise Exception("Mass %s is not in the table, valid values are %s" % (str(mass), ", ".join([str(x) for x in hplusMassIndex.keys()])))
    if not tanbeta in hplusTanBetaIndex:
        raise Exception("Tan(beta) %s not in the table, valild values are %s" % (str(tanbeta), ", ".join([str(x) for x in hplusTanBetaIndex.keys()])))

    return hplusBranchRatio[hplusTanBetaIndex[tanbeta]][hplusMassIndex[mass]]

def hplusTauNuCrossSection(mass, tanbeta):
    (tHBR, HtaunuBR) = hplusTauNuBRs(mass, tanbeta)

    return 2 * ttCrossSection * tHBR * (1-tHBR) * HtaunuBR


def setHplusCrossSections(datasets, tanbeta):
    for name, mass in hplusDatasetMass.iteritems():
        if not datasets.hasDataset(name):
            continue

        datasets.getDataset(name).setCrossSection(hplusTauNuCrossSection(mass, tanbeta))

def printHplusCrossSections():
    print "ttbar cross section %f pb" % ttCrossSection
    print
    tanbetas = hplusTanBetaIndex.keys()
    tanbetas.sort()
    masses = hplusMassIndex.keys()
    masses.sort()
    for tanbeta in tanbetas:
        print "="*68
        print "tan(beta) = %d" % tanbeta
        print "H+ M (GeV) | BR(t->bH+) | BR(H+->taunu) | sigma(tt->tbH+->tbtaunu) |"
        for mass in masses:
            BR = hplusTauNuBRs(mass, tanbeta)
            print "%10d | %10f | %13f | %24f |" % (mass, BR[0], BR[1], hplusTauNuCrossSection(mass, tanbeta))


if __name__ == "__main__":
    printHplusCrossSections()
