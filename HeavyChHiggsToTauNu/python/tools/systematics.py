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

from math import sqrt

## Helper class for a scalar uncertainty
class ScalarUncertaintyItem:
    def __init__(self, uncertaintyName, *args, **kwargs):
        self._name = uncertaintyName
        self._uncertUp = 0.0 # relative uncertainty squared
        self._uncertDown = 0.0 # relative uncertainty squared
        # Handle inputs
        if len(args) == 1:
            # Symmetric uncertainty
            self._uncertUp = args[0]**2
            self._uncertDown = args[0]**2
        elif len(args) == 0 and len(kwargs) == 2:
            if not "plus" in kwargs or not "minus" in kwargs:
                raise Exception("Error: You forgot to give plus= and minus= arguments to ScalarUncertaintyItem()!")
            self._uncertUp = kwargs["plus"]**2
            self._uncertDown = kwargs["minus"]**2
        else:
            raise Exception("Error: You forgot to give the uncertainty value(s) to ScalarUncertaintyItem()!")

    def add(self,other):
        self._name += "+%s"%other._name
        self._uncertUp += other._uncertUp
        self._uncertDown += other._uncertDown

    def Clone(self):
        return ScalarUncertaintyItem(self.name, self._uncertUp, self._uncertDown)

    def getName(self):
        return self._name

    def isAsymmetric(self):
        return abs(self._uncertDown - self._uncertUp) > 0.0000001

    def getUncertaintySquaredDown(self):
        return self._uncertDown

    def getUncertaintyDown(self):
        return sqrt(self._uncertDown)

    def getUncertaintySquaredUp(self):
        return self._uncertUp

    def getUncertaintyUp(self):
        return sqrt(self._uncertUp)

_crossSectionUncertainty = {
    "TTJets": ScalarUncertaintyItem("xsect", plus=0.062, minus=0.053),
    "TTToHplus": ScalarUncertaintyItem("xsect", plus=0.062, minus=0.053),
    "HplusTB": ScalarUncertaintyItem("xsect", 0.30),
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

# Binning for data-driven control plots and final shapes
# Needed to get systematics right for QCD anti-isol. -> isol. systematics
# Format: list of left bin edges; last entry is maximum value
_dataDrivenCtrlPlotBinning = {
    "Njets": [3,4,5,6,7,8,9,10],
    "ImprovedDeltaPhiCuts": [0,20,40,60,80,100,120,140,160,180,200,220,240,260],
    "MET": [0,10,20,30,40,50,60,70,80,90,100,100,110,120,130,140,150,170,190,220,250,300,400,500],
    "NBjets": [0,1,2,3,4,5,6,7,8],
    "TopMass": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,350,400,500],
    "WMass": [0,10,20,30,40,50,60,70,80,90,100,100,120,130,140,160,180,200,250,300],
    "shapeTransverseMass": [0,20,40,60,80,100,120,140,160,200,250,400],
    "shapeInvariantMass": [0,20,40,60,80,100,120,140,160,200,400],
}

def getBinningForPlot(plotName):
    for plot in _dataDrivenCtrlPlotBinning:
        if plot == plotName[:len(plot)]:
            return _dataDrivenCtrlPlotBinning[plot]
    raise Exception("Cannot find bin specifications for plotname %s! (implemented are: %s)"%(plotName,', '.join(map(str, _dataDrivenCtrlPlotBinning.keys()))))
