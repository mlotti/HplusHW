## Package for all systematic uncertainties in the analysis

#######################################
# Shape uncertainties

# These are obtained automatically for each dataset from the SystVar identifier in the analysis module names
# Also, one can take the full list of shapes, since the variations are zero compared to nominal,
# unless the analysis has proceeded to a stage where the selection to be varied has been applied

# Considered shape uncertainties:
# - Tau trg SF uncertainty
# (- MET trg SF uncertainty)
# - fake tau SF uncertainty FIXME to be implemented
# - tau energy scale (TES)
# - jet energy scale (JES)
# - MET (unclustered) energy scale
# - jet energy resolution (JER)
# - btag SF
# - top pT reweight SF uncertainty FIXME to be implemented
# - pileup uncertainty
# - QCD method normalization
# - statistical uncertainties

#######################################
# Scalar uncertainties

# List of considered uncertainties:
# - tau ID uncertainty
# - tau mis-ID uncertainty
# - e/mu reco and ID
# - Embedding specific FIXME: add if necessary
# - cross section uncertainties
# - luminosity

## Helper class for a scalar uncertainty
class ScalarUncertaintyItem:
    def __init__(self, uncertaintyName, *args, **kwargs):
        self._name = uncertaintyName
        self._uncertUp = 0.0
        self._uncertDown = 0.0
        # Handle inputs
        if len(args) == 1:
            # Symmetric uncertainty
            self._uncertUp = args[0]
            self._uncertDown = args[0]
        elif len(args) == 0 and len(kwargs) == 2:
            if not "plus" in kwargs or not "minus" in kwargs:
                raise Exception("Error: You forgot to give plus= and minus= arguments to ScalarUncertaintyItem()!")
            self._uncertUp = kwargs["plus"]
            self._uncertDown = kwargs["minus"]
        else:
            raise Exception("Error: You forgot to give the uncertainty value(s) to ScalarUncertaintyItem()!")

    def getName(self):
        return self._name

    def isAsymmetric(self):
        return abs(self._uncertDown - self._uncertUp) > 0.0001

    def getUncertaintyDown(self):
        return self._uncertDown

    def getUncertaintyUp(self):
        return self._uncertUp

_crossSectionUncertainty = {
    "TTJets": ScalarUncertaintyItem("xsect", plus=0.062, minus=0.053),
    "TTToHplus": ScalarUncertaintyItem("xsect", plus=0.062, minus=0.053),
    "HplusTB": ScalarUncertaintyItem("xsect", plus=0.062, minus=0.053),
    "WJets":  ScalarUncertaintyItem("xsect", 0.05),
    "SingleTop": ScalarUncertaintyItem("xsect", 0.08),
    "DYJetsToLL": ScalarUncertaintyItem("xsect", 0.04),
    "Diboson": ScalarUncertaintyItem("xsect", 0.04),
    "QCD": ScalarUncertaintyItem("xsect", 1.00), # We do not trust the MC QCD, therefore 100 % uncertainty
    "QCD_Pt20_MuEnriched": ScalarUncertaintyItem("xsect", 1.00), # We do not trust the MC QCD, therefore 100 % uncertainty
    "default": ScalarUncertaintyItem("xsect", 0.00),
}

def getCrossSectionUncertainty(datasetName):
    if datasetName in _crossSectionUncertainty:
        return _crossSectionUncertainty[datasetName]
    if "pseudo" in datasetName:
        return _crossSectionUncertainty["default"]
    # Ok, dataset name not found and not in the known list, give a warning message
    print WarningLabel()+"Could not find cross section uncertainty for dataset label: %s!%s"%(datasetName,NormalStyle())
    return _crossSectionUncertainty["default"]

def getLeptonVetoUncertainty(datasetName):
    if "pseudo" in datasetName:
        return ScalarUncertaintyItem("LeptonVeto", 0.00)
    return ScalarUncertaintyItem("LeptonVeto", 0.002)

def getTauIDUncertainty(isGenuineTau=True):
    if isGenuineTau:
        return ScalarUncertaintyItem("tauID", 0.06)
    else:
        return ScalarUncertaintyItem("tauID", 0.00)

def getLuminosityUncertainty():
    return ScalarUncertaintyItem("tauMisID", 0.026)

# Note: if majority of sample is genuine taus, set isGenuineTau=true
def getScalarUncertainties(datasetName, isGenuineTau):
    myList = []
    myList.append(getCrossSectionUncertainty(datasetName))
    myList.append(getLeptonVetoUncertainty(datasetName))
    myList.append(getTauIDUncertainty(isGenuineTau))
    myList.append(getLuminosityUncertainty())
    return myList

