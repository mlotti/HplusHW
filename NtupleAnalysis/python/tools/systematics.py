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

import ShellStyles

## Helper class for a scalar uncertainty
class ScalarUncertaintyItem:
    def __init__(self, uncertaintyName, *args, **kwargs):
        self._name = uncertaintyName
        self._uncertUp = 0.0 # relative uncertainty squared
        self._uncertDown = 0.0 # relative uncertainty squared
        # Handle inputs
        if len(args) == 1:
            if isinstance(args[0], ScalarUncertaintyItem):
                self._uncertUp = args[0]._uncertUp
                self._uncertDown = args[0]._uncertDown
            else:
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

    def add(self,other):
        self._name += "+%s"%other._name
        self._uncertUp = sqrt(self._uncertUp**2 + other._uncertUp**2)
        self._uncertDown = sqrt(self._uncertDown**2 + other._uncertDown**2)

    def Clone(self):
        return ScalarUncertaintyItem(self._name, self)

    def scale(self, factor):
        self._uncertUp *= factor
        self._uncertDown *= factor

    def getName(self):
        return self._name

    def isAsymmetric(self):
        return abs(self._uncertDown - self._uncertUp) > 0.0000001

    def getUncertaintySquaredDown(self):
        return self._uncertDown**2

    def getUncertaintyDown(self):
        return self._uncertDown

    def getUncertaintySquaredUp(self):
        return self._uncertUp**2

    def getUncertaintyUp(self):
        return self._uncertUp

    def getUncertaintyMax(self):
        return max([self._uncertUp, self._uncertDown])

_crossSectionUncertainty = {
    "TTJets": ScalarUncertaintyItem("xsect", plus=0.0517, minus=0.060), # arxiv:1303.6254
    "TTToHplus": ScalarUncertaintyItem("xsect", plus=0.0517, minus=0.060), # arxiv:1303.6254
    "HplusTB": ScalarUncertaintyItem("xsect", 0.30),
    "WJets":  ScalarUncertaintyItem("xsect", plus=0.0403, minus=0.0371), # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV
    "SingleTop": ScalarUncertaintyItem("xsect", 0.0901), # for tW https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV
    "DYJetsToLL": ScalarUncertaintyItem("xsect", plus=0.0380, minus=0.0360), # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV
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
    print ShellStyles.WarningLabel()+"Could not find cross section uncertainty for dataset label: %s!%s"%(datasetName,ShellStyles.NormalStyle())
    return _crossSectionUncertainty["default"]

# def getLeptonVetoUncertainty(datasetName):
#     if "pseudo" in datasetName:
#         return ScalarUncertaintyItem("LeptonVeto", 0.00)
#     return ScalarUncertaintyItem("LeptonVeto", 0.002)

def getLeptonVetoUncertainty():
     return ScalarUncertaintyItem("LeptonVeto", 0.01)

def getTauIDUncertainty(isGenuineTau=True):
    if isGenuineTau:
        return ScalarUncertaintyItem("tauID", 0.06)
    else:
        return ScalarUncertaintyItem("tauID", 0.00)

def getLuminosityUncertainty():
    return ScalarUncertaintyItem("lumi", 0.026)

def getProbabilisticBtagUncertainty():
    return ScalarUncertaintyItem("probBtag", 0.5)

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
    "WeightedCounters": None,
    "Njets*": [3,4,5,6,7,8,9,10],
    "JetPt_AfterStandardSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,170,190,220,250,300,400,500],
    "JetEta_AfterStandardSelections": [-2.5,-2.2,-2.0,-1.8,-1.6,-1.4,-1.2,-1.0,-0.8,-0.6,-0.4,-0.2,-0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.5],
    "JetPt_AfterAllSelections": [0,20,30,40,60,70,80,90,100,120,150,200,250,300,400,500],
    "JetEta_AfterAllSelections": [-2.5,-2.0,-1.5,-1.0,-0.5,0.0,0.5,1.0,1.5,2.0,2.5],
    "ImprovedDeltaPhiCuts*": [0,20,40,60,80,100,120,140,160,180,200,220,240,260],
    "CollinearAngularCutsMinimum*": [0,20,40,60,80,100,120,140,160,180,200,220,240,260],
    "BackToBackAngularCutsMinimum*": [0,20,40,60,80,100,120,140,160,180,200,220,240,260],
    #"MET": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,170,190,220,250,300,400,500,600,700,800],
    "MET": [0,20,40,60,80,100,120,140,160,200,250,300,400,500,600,700,800],
    "METPhi": [-3.14,-2.75,-2.36,-1.96,-1.57,-1.18,-0.79,-0.39,0.00,0.39,0.79,1.18,1.57,1.96,2.36,2.75,3.14],
    "METPhiMinusTauPhi": [0.00,0.39,0.79,1.18,1.57,1.96,2.36,2.75,3.14],
    "MET_AfterAllSelections": [0,20,40,60,80,100,120,140,160,180,200,250,300,400,500,600,700,800],
    "METPhi_AfterAllSelections": [-3.14,-2.36,-1.57,-0.79,0.00,0.79,1.57,2.36,3.14],
    "METPhiMinusTauPhi_AfterAllSelections": [0.00,0.39,0.79,1.18,1.57,1.96,2.36,2.75,3.14],
    "TauPlusMETPt": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,450,500],
    "TauPlusMETPt_AfterAllSelections": [0,40,80,120,160,200,240,280,320,360,400,450,500],
    "NBjets": [0,1,2,3,4,5,6,7,8],
    "BJetSelection*": [0,1,2,3,4,5,6,7,8],
    "BJetPt": [0,30,50,70,90,110,130,150,200,300,400,500],
    "BJetEta": [-2.5,-2.0,-1.5,-1.0,-0.5,0.0,0.5,1.0,1.5,2.0,2.5],
    "BtagDiscriminator": [-1.0,-0.9,0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
    "NBjets_AfterAllSelections": [0,1,2,3,4,5,6,7,8],
    "BJetPt_AfterAllSelections": [0,20,30,50,70,90,110,130,150,200,300,400,500],
    "BJetEta_AfterAllSelections": [-2.5,-2.0,-1.5,-1.0,-0.5,0.0,0.5,1.0,1.5,2.0,2.5],
    "BtagDiscriminator_AfterAllSelections": [-1.0,-0.9,0.0,0.2,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
    "DeltaPhiTauMet_AfterAllSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180],
    "MinDeltaPhiTauJet": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180],
    "MaxDeltaPhiTauJet": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180],
    "TopMass": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,350,400,500],
    "TopPt": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,350,400,500],
    "WMass": [0,10,20,30,40,50,60,70,80,90,100,100,120,130,140,160,180,200,250,300],
    "WPt": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,350,400,500],
    "TopMass_AfterAllSelections": [0,20,40,60,80,100,150,200,300,500],
    "TopPt_AfterAllSelections": [0,20,40,60,80,100,150,200,300,500],
    "WMass_AfterAllSelections": [0,10,20,30,40,50,60,70,80,90,100,100,120,130,140,160,180,200,250,300],
    "WPt_AfterAllSelections": [0,20,40,60,80,100,150,200,300,500],
    #"shapeTransverseMass": [0,20,40,60,80,100,120,140,160,200,400],
    #"shapeTransverseMass": [0,20,40,60,80,100,120,140,160,200,700],
    "TransverseMass*": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,600,700,800],
    "shapeTransverseMass": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,600,700,800],
    #"shapeTransverseMass": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350,360,370,380,390,400],
    "shapeInvariantMass": [0,20,40,60,80,100,120,140,160,200,400],
    "InvariantMass*": [0,20,40,60,80,100,120,140,160,200,400],
    "SelectedTau_pT_AfterStandardSelections": [0,50,60,70,80,90,100,110,120,130,140,150,170,190,220,250,300,400,500],
    "SelectedTau_eta_AfterStandardSelections": [-2.5,-2.2,-2.0,-1.8,-1.6,-1.4,-1.2,-1.0,-0.8,-0.6,-0.4,-0.2,-0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.5],
    "SelectedTau_phi_AfterStandardSelections": [-3.14,-2.75,-2.36,-1.96,-1.57,-1.18,-0.79,-0.39,0.00,0.39,0.79,1.18,1.57,1.96,2.36,2.75,3.14],
    "SelectedTau_ldgTrkPt_AfterStandardSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,170,190,220,250,300,400,500],
    "SelectedTau_Rtau_AfterStandardSelections": [0.70,0.72,0.74,0.76,0.78,0.80,0.82,0.84,0.86,0.88,0.90,0.92,0.94,0.96,0.98,1.00],
    "SelectedTau_p_AfterStandardSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,170,190,220,250,300,400,500],
    "SelectedTau_LeadingTrackP_AfterStandardSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,170,190,220,250,300,400,500],
    "SelectedTau_DecayMode_AfterStandardSelections": [0,1,2,3,4,5,6,7,8,9,10],
    "SelectedTau_pT_AfterAllSelections": [0,50,60,80,100,150,200,300,400,500],
    "SelectedTau_eta_AfterAllSelections": [-2.5,-2.0,-1.5,-1.0,-0.5,0.0,0.5,1.0,1.5,2.0,2.5],
    "SelectedTau_phi_AfterAllSelections": [-3.14,-2.36,-1.57,-0.79,0.00,0.79,1.57,2.36,3.14],
    "SelectedTau_ldgTrkPt_AfterAllSelections": [0,20,40,50,60,70,80,100,150,200,300],
    "SelectedTau_Rtau_AfterAllSelections": [0.70,0.75,0.80,0.85,0.90,0.95,1.00],
    "SelectedTau_Rtau_FullRange_AfterAllSelections": [0.0, 0.05, 0.1, 0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00],
    "SelectedTau_p_AfterAllSelections": [0,20,40,50,60,70,80,100,150,200,300,500],
    "SelectedTau_LeadingTrackP_AfterAllSelections": [0,41,60,80,100,150,200,300,500],
    "SelectedTau_DecayMode_AfterAllSelections": [0,1,2,3,4,5,6,7,8,9,10],
    "DeltaPhiTauMET_AfterAllSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180],
    "MinDeltaPhiTauJet_AfterAllSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180],
    "MaxDeltaPhiTauJet_AfterAllSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180],
}
# Add EWK fake tau shape definitions
for key in _dataDrivenCtrlPlotBinning.keys():
    if "shape" in key:
        _dataDrivenCtrlPlotBinning[key.replace("shape","shapeEWKFakeTaus")] = _dataDrivenCtrlPlotBinning[key]


def getBinningForPlot(plotName):
    s = plotName.split("/")
    shortName = s[len(s)-1]
    for plot in _dataDrivenCtrlPlotBinning:
        if plot[len(plot)-1] == "*" and plot[:(len(plot)-1)] == shortName[:(len(plot)-1)]:
            return _dataDrivenCtrlPlotBinning[plot]
    if shortName in _dataDrivenCtrlPlotBinning.keys():
        return _dataDrivenCtrlPlotBinning[shortName]
    raise Exception("Cannot find bin specifications for plotname %s! (implemented are: %s)"%(shortName,', '.join(map(str, _dataDrivenCtrlPlotBinning.keys()))))
