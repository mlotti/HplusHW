## \package crosssection
# Background and signal cross sections
#
# All cross sections are in pb

########################################
# Background cross section table

## Cross section of a single process (physical dataset)
class CrossSection:
    ## Constructor
    #
    # \parma name              Name of the process
    # \param energyDictionary  Dictionary of energy -> cross section (energy as string in TeV, cross section as float in pb)
    def __init__(self, name, energyDictionary):
        self.name = name
        for key, value in energyDictionary.iteritems():
            setattr(self, key, value)

    ## Get cross section
    #
    # \param energy  Energy as string in TeV
    def get(self, energy):
        try:
            return getattr(self, energy)
        except AttributeError:
            raise Exception("No cross section set for process %s for energy %s" % (self.name, energy))

## List of CrossSection objects
class CrossSectionList:
    def __init__(self, *args):
        self.crossSections = {}
        for a in args:
            self.crossSections[a.name] = a

    def crossSection(self, name, energy):
        for key, obj in self.crossSections.iteritems():
            if name[:len(key)] == key:
                return obj.get(energy)
        return None

# Cross sections from
# [1] PREP
# [2] https://twiki.cern.ch/twiki/bin/view/CMS/ReProcessingSummer2011
# [3] from https://twiki.cern.ch/twiki/bin/view/CMS/CrossSections_3XSeries
# [4] https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSections
# [5] https://twiki.cern.ch/twiki/bin/view/CMS/SingleTopMC2011
# [6] https://twiki.cern.ch/twiki/bin/view/CMS/SingleTopSigma

backgroundCrossSections = CrossSectionList(
    CrossSection("QCD_Pt30to50", {
            "7": 5.312e+07, # [2]
            }),
    CrossSection("QCD_Pt50to80", {
            "7": 6.359e+06, # [2]
            }),
    CrossSection("QCD_Pt80to120", {
            "7": 7.843e+05, # [2]
            }),
    CrossSection("QCD_Pt120to170", {
            "7": 1.151e+05, # [2]
            }),
    CrossSection("QCD_Pt170to300", {
            "7": 2.426e+04, # [2]
            }),
    CrossSection("QCD_Pt300to470", {
            "7": 1.168e+03, # [2]
            }),
    CrossSection("QCD_Pt20_MuEnriched", {
            "7": 296600000.*0.0002855 # [2]
            }),
    CrossSection("WW", {
            "7": 43.0, # [3]
            }),
    CrossSection("WZ", {
            "7": 18.2, # [3]
            }),
    CrossSection("ZZ", {
            "7": 5.9, # [3]
            }),
    CrossSection("TTJets", {
            "7": 165.0, # [3,4], approx. NNLO
            }),
    CrossSection("WJets", {
            "7": 31314.0, # [2], NNLO
            }),
    CrossSection("DYJetsToLL_M50", {
            "7": 3048.0, # [4], NNLO
            }),
    CrossSection("DYJetsToLL_M10to50", {
            "7": 9611.0, # [1]
            }),
    CrossSection("T_t-channel", {
            "7": 41.92, # [5,6]
            }),
    CrossSection("Tbar_t-channel", {
            "7": 22.65, # [5,6]
            }),
    CrossSection("T_tW-channel", {
            "7": 7.87, # [5,6]
            }),
    CrossSection("Tbar_tW-channel", {
            "7": 7.87, # [5,6]
            }),
    CrossSection("T_s-channel", {
            "7": 3.19, # [5,6]
            }),
    CrossSection("Tbar_s-channel", {
            "7": 1.44, # [5,6]
            }),
)

def setBackgroundCrossSections(datasets):
    for dset in datasets.getMCDatasets():
        value = backgroundCrossSections.crossSection(dset.getName(), dset.getEnergy())
        if value is not None:
            dset.setCrossSection(value)
            print "Setting %s cross section to %f pb" % (dset.getName(), value)
#        else:
#            print "Warning: no cross section for dataset %s with energy %s TeV (see python/tools/crosssection.py)" % (dset.getName(), dset.getEnergy())


########################################
# Signal cross section table

import BRdataInterface as br

## Default value of MSSM mu parameter
defaultMu = 200

## Mapping of WH dataset names to mass points
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

## Mapping of HH dataset names to mass points
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

## WH, H->tau nu MSSM cross section
#
# \param mass     H+ mass
# \param tanbeta  tanbeta parameter
# \param mu       mu parameter
# \param energy     sqrt(s) in TeV as string
def whTauNuCrossSectionMSSM(mass, tanbeta, mu, energy):
    br_tH = br.getBR_top2bHp(mass, tanbeta, mu)
    br_Htaunu = br.getBR_Hp2tau(mass, tanbeta, mu)
    return whTauNuCrossSection(br_tH, br_Htaunu, energy)

## WH, H->tau nu cross section from BRs
#
# \param br_tH      BR(t -> b H+)
# \param br_Htaunu  BR(H+ -> tau nu)
# \param energy     sqrt(s) in TeV as string
def whTauNuCrossSection(br_tH, br_Htaunu, energy):
    ttCrossSection = backgroundCrossSections.crossSection("TTJets", energy)
    return 2 * ttCrossSection * br_tH * (1-br_tH) * br_Htaunu


## HH, H->tau nu MSSM cross section
#
# \param mass     H+ mass
# \param tanbeta  tanbeta parameter
# \param mu       mu parameter
# \param energy     sqrt(s) in TeV as string
def hhTauNuCrossSectionMSSM(mass, tanbeta, mu, energy):
    br_tH = br.getBR_top2bHp(mass, tanbeta, mu)
    br_Htaunu = br.getBR_Hp2tau(mass, tanbeta, mu)
    return hhTauNuCrossSection(br_tH, br_Htaunu, energy)

## HH, H->tau nu cross section from BRs
#
# \param br_tH      BR(t -> b H+)
# \param br_Htaunu  BR(H+ -> tau nu)
# \param energy     sqrt(s) in TeV as string
def hhTauNuCrossSection(br_tH, br_Htaunu, energy):
    ttCrossSection = backgroundCrossSections.crossSection("TTJets", energy)
    return ttCrossSection * br_tH*br_tH * br_Htaunu*br_Htaunu


def _setHplusCrossSectionsHelper(massList, datasets, function):
    for name, mass in massList:
        if not datasets.hasDataset(name):
            continue
        d = datasets.getDataset(name)
        crossSection = function(mass, d.getEnergy())
        datasets.getDataset(name).setCrossSection(crossSection)
        print "Setting %s cross section to %f pb" % (name, crossSection)

def _setHplusCrossSections(datasets, whFunction, hhFunction):
    _setHplusCrossSectionsHelper(whDatasetMass.iteritems(), datasets, whFunction)
    _setHplusCrossSectionsHelper(hhDatasetMass.iteritems(), datasets, hhFunction)

## Set signal dataset cross sections to ttbar cross section
#
# \param datasets  dataset.DatasetManager object
def setHplusCrossSectionsToTop(datasets):
    function = lambda mass, energy: backgroundCrossSections.crossSection("TTJets", energy)
    _setHplusCrossSections(datasets, function, function)

## Set signal dataset cross sections to MSSM cross section
#
# \param datasets  dataset.DatasetManager object
# \param tanbeta   tanbeta parameter
# \param mu        mu parameter
def setHplusCrossSectionsToMSSM(datasets, tanbeta=20, mu=defaultMu):
    _setHplusCrossSections(datasets,
                           lambda mass, energy: whTauNuCrossSectionMSSM(mass, tanbeta, mu, energy),
                           lambda mass, energy: hhTauNuCrossSectionMSSM(mass, tanbeta, mu, energy))

## Set signal dataset cross sections to cross section via BR
#
# \param datasets   dataset.DatasetManager object
# \param br_tH      BR(t -> b H+)
# \param br_Htaunu  BR(H+ -> tau nu)
def setHplusCrossSectionsToBR(datasets, br_tH, br_Htaunu):
    _setHplusCrossSections(datasets,
                           lambda mass, energy: whTauNuCrossSection(br_tH, br_Htaunu, energy),
                           lambda mass, energy: hhTauNuCrossSection(br_tH, br_Htaunu, energy))

## Set signal dataset cross sections to cross section (deprecated, only for compatibility)
def setHplusCrossSections(datasets, tanbeta=20, mu=defaultMu, toTop=False):
    if toTop:
        setHplusCrossSectionsToTop(datasets)
    else:
        setHplusCrossSectionsToMSSM(tanbeta, mu)

## Print H+ cross sections for given tanbeta values
#
# \param tanbetas  List of tanbeta values
# \param mu        Mu parameter
# \param energy    sqrt(s) in TeV as string
def printHplusCrossSections(tanbetas=[10, 20, 30, 40], mu=defaultMu, energy="7"):
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

            print "%10d | %10f | %13f | %24f | %27f |" % (mass, br_tH, br_Htaunu, whTauNuCrossSectionMSSM(mass, tanbeta, mu, energy), hhTauNuCrossSectionMSSM(mass, tanbeta, mu, energy))


if __name__ == "__main__":
    printHplusCrossSections()
