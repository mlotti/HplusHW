## Package for fetching systematic uncertainties used in the datacards

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
    # TTJets, based on arxiv:1303.6254 and https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO
    "TTJets_scale": ScalarUncertaintyItem("xsect", plus=19.77/831.76, minus=29.20/831.76),
    "TTJets_pdf": ScalarUncertaintyItem("xsect", 35.06/831.76),
    "TTJets_mass": ScalarUncertaintyItem("xsect", plus=23.18/831.76, minus=22.45/831.76),    
    "TTJets": ScalarUncertaintyItem("xsect", plus=0.062, minus=0.066), # scale, pdf and mass combined (quadratically)

    # Light H+ signal, normalized to TTJets --> use combined TTJets uncertainty
    "TTToHplus": ScalarUncertaintyItem("xsect", plus=0.062, minus=0.066),

    # Heavy H+ signal, what is the effect of this number?
    "HplusTB": ScalarUncertaintyItem("xsect", 0.30),
    
    # Single top, based on http://arxiv.org/abs/1311.0283 and https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec#Single_top_Wt_channel_cross_sect
    "SingleTop_scale":  ScalarUncertaintyItem("xsect", 1.80/71.7),
    "SingleTop_pdf":  ScalarUncertaintyItem("xsect", 3.40/71.7), 

    # W+jets, based on "Total W" on https://twiki.cern.ch/twiki/bin/view/CMS/StandardModelCrossSectionsat13TeVInclusive
    "WJets_scale":  ScalarUncertaintyItem("xsect", plus=165.7/20508.9, minus=88.2/20508.9), 
    "WJets_pdf":  ScalarUncertaintyItem("xsect", 770.9/20508.9),
    
    # DY, based on "Z/a* (50) on https://twiki.cern.ch/twiki/bin/view/CMS/StandardModelCrossSectionsat13TeVInclusive
    "DYJetsToLL_scale": ScalarUncertaintyItem("xsect", plus=13.2/2008.4, minus=7.5/2008.4),
    "DYJetsToLL_pdf": ScalarUncertaintyItem("xsect", 75.0/2008.4), 
    
    # Diboson, values from MIT PAS AN-16-194 (see also https://twiki.cern.ch/twiki/bin/view/CMS/StandardModelCrossSectionsat13TeVInclusive)
    "Diboson_scale": ScalarUncertaintyItem("xsect", 0.032), 
    "Diboson_pdf": ScalarUncertaintyItem("xsect", 0.044),

    # ttW, values from HIG-17-022 which shows consistency with all other systematics defined here (TTJets, SingleTop, WJets, DY, Diboson, ..)
    "TTW_scale": ScalarUncertaintyItem("xsect", plus=0.13, minus=0.12), 
    "TTW_pdf"  : ScalarUncertaintyItem("xsect", 0.02),  # 2%

    # ttZ, values from HIG-17-022 which shows consistency with all other systematics defined here (TTJets, SingleTop, WJets, DY, Diboson, ..)
    "TTZ_scale": ScalarUncertaintyItem("xsect", plus=0.10, minus=0.12), 
    "TTZ_pdf"  : ScalarUncertaintyItem("xsect", 0.03),  # 2%

    # tttt
#    "TTTT_scale": ScalarUncertaintyItem("xsect", plus=0.10, minus=0.12), 
#    "TTTT_pdf"  : ScalarUncertaintyItem("xsect", 0.03),  # 2%
#    "TTTT"      : ScalarUncertaintyItem("xsect", 0.12), # scale and pdf combined (quadratically)
    
    # MC QCD: we do not trust the MC QCD, therefore 100 % uncertainty
    "QCD": ScalarUncertaintyItem("xsect", 1.00),
    "QCD_Pt20_MuEnriched": ScalarUncertaintyItem("xsect", 1.00),
    
    # default: no uncertainty
    "default": ScalarUncertaintyItem("xsect", 0.00),
}

def getCrossSectionUncertainty(uncertName):
    if uncertName in _crossSectionUncertainty:
        return _crossSectionUncertainty[uncertName]
    if "pseudo" in uncertName:
        return _crossSectionUncertainty["default"]
    # Ok, dataset name not found and not in the known list, give a warning message
    print ShellStyles.WarningLabel() + "Could not find cross section uncertainty for dataset label: %s"%uncertName + ShellStyles.NormalStyle()
    return _crossSectionUncertainty["default"]

# def getLeptonVetoUncertainty(uncertName):
#     if "pseudo" in uncertName:
#         return ScalarUncertaintyItem("LeptonVeto", 0.00)
#     return ScalarUncertaintyItem("LeptonVeto", 0.002)

def getLeptonVetoUncertainty():
     return ScalarUncertaintyItem("LeptonVeto", 0.02)

def getTauIDUncertainty(isGenuineTau=True):
    if isGenuineTau:
        return ScalarUncertaintyItem("tauID", 0.06)
    else:
        return ScalarUncertaintyItem("tauID", 0.00)

def getLuminosityUncertainty(year="2015"):
    if year=="2012":
        return ScalarUncertaintyItem("lumi", 0.026) # for 8 TeV
    elif year=="2015":
        return ScalarUncertaintyItem("lumi", 0.027) # for 13 TeV 2015, see https://twiki.cern.ch/twiki/bin/viewauth/CMS/TWikiLUM
    elif year=="2016":
        return ScalarUncertaintyItem("lumi", 0.025) # for 13 TeV 2016, see https://twiki.cern.ch/twiki/bin/viewauth/CMS/TWikiLUM
    else:
        return ScalarUncertaintyItem("lumi", 0.025) # default, here 13 TeV 2016

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

def getBinningForTetrajetMass(binLevel=0):
    '''
    Binning for H->tb invariant mass histogram 
    tetrajet object = ldg (in pT) trijet  + ldg (in ) free bjet 
    '''
    myBins = []
    if binLevel == -1: #1 bin (counting experiment)
        myBins = [0.0, 3000.0] 
    elif binLevel == 0: #default binning
        for i in range(0, 1000, 50):
            myBins.append(i)
        for i in range(1000, 2000, 100):
            myBins.append(i)
        for i in range(2000, 3000+500, 500):
            myBins.append(i)
    elif binLevel == 1: #finer binning
        for i in range(0, 1000, 25):
            myBins.append(i)
        for i in range(1000, 2000, 50):
            myBins.append(i)
        for i in range(2000, 3000+250, 250):
            myBins.append(i)
    elif binLevel == 2: #even finer binning
        for i in range(0, 1000, 20):
            myBins.append(i)
        for i in range(1000, 2000, 40):
            myBins.append(i)
        for i in range(2000, 3000+200, 200):
            myBins.append(i)
    elif binLevel == 3: #even more finer binning
        print "%sWARNING! This binning will take hours to compute limits!%s" % (ShellStyles.ErrorStyle(), ShellStyles.NormalStyle())
        for i in range(0, 1000, 10):
            myBins.append(i)
        for i in range(1000, 2000, 20):
            myBins.append(i)
        for i in range(2000, 3000+50, 50):
            myBins.append(i)
    elif binLevel == 4: # 20 GeV bins
        for i in range(0, 3000+20, 20):
            myBins.append(i)
    elif binLevel == 5: # 30 GeV bins
        for i in range(0, 3000+30, 30):
            myBins.append(i)
    elif binLevel == 6: # 40 GeV bins
        for i in range(0, 3000+40, 40):
            myBins.append(i)
    elif binLevel == 7: # 100 GeV bins
        for i in range(0, 3000+100, 100):
            myBins.append(i)
    elif binLevel == 8: # 300 GeV bins
        for i in range(0, 3000+300, 300):
            myBins.append(i)
    elif binLevel == 9: # 50 GeV bins
        for i in range(0, 3000+50, 50):
            myBins.append(i)
    elif binLevel == 10:
        for i in range(0, 800, 20):
            myBins.append(i)
        for i in range(800, 1000, 40):
            myBins.append(i)
        for i in range(1000, 1500, 80):
            myBins.append(i)
        for i in range(1500, 2000, 100):
            myBins.append(i)
        for i in range(2000, 3000+200, 200):
            myBins.append(i)
    elif binLevel == 11:
        for i in range(0, 1000+40, 40):
            myBins.append(i)
    elif binLevel == 12: #default binning variation
        for i in range(0, 1000, 20):
            myBins.append(i)
        for i in range(1000, 1500, 100):
            myBins.append(i)
        for i in range(1500, 2000, 200):
            myBins.append(i)
        #for i in range(2000, 3000+500, 500):
        for i in range(2000, 3000, 500):  # Up to 2500
            myBins.append(i)
    elif binLevel == 13: #default binning variation
        for i in range(0, 700, 10):
            myBins.append(i)
        for i in range(700, 1000, 25):
            myBins.append(i)
        for i in range(1000, 1500, 50):
            myBins.append(i)
        for i in range(1500, 2000, 200):
            myBins.append(i)
        for i in range(2000, 2500+250, 250):
            myBins.append(i)
        for i in range(2500, 3000, 500):# Up to 2500?
            myBins.append(i)
    elif binLevel == 14:
        for i in range(0, 800, 25):
            myBins.append(i)
        for i in range(800, 1200, 50):
            myBins.append(i)
        for i in range(1200, 1500, 100):
            myBins.append(i)
        for i in range(1500, 2500, 250):
            myBins.append(i)
        for i in range(2500, 3000, 500):
            myBins.append(i)
    elif binLevel == 15:
        for i in range(0, 700, 25):
            myBins.append(i)
        for i in range(700, 1000, 50):
            myBins.append(i)
        for i in range(1000, 1400, 100):
            myBins.append(i)
        for i in range(1400, 2000, 200):
            myBins.append(i)
        for i in range(2000, 3000, 500):
            myBins.append(i)
    elif binLevel == 16:
        for i in range(0, 600, 25):
            myBins.append(i)
        for i in range(600, 800, 50):
            myBins.append(i)
        for i in range(800, 1200, 100):
            myBins.append(i)
        for i in range(1400, 2000, 200):
            myBins.append(i)
        for i in range(2000, 3000, 500):
            myBins.append(i)
    elif binLevel == 17:
        for i in range(0, 800, 50):
            myBins.append(i)
        for i in range(800, 1200, 100):
            myBins.append(i)
        for i in range(1400, 2000, 200):
            myBins.append(i)
        for i in range(2000, 3000, 500):
            myBins.append(i)
    elif binLevel == 18:
        for i in range(0, 600, 50):
            myBins.append(i)
        for i in range(600, 1000, 100):
            myBins.append(i)
        for i in range(1000, 2000, 200):
            myBins.append(i)
        for i in range(2000, 3000, 500):
            myBins.append(i)
    elif binLevel == 19:
        for i in range(0, 400, 25):
            myBins.append(i)
        for i in range(400, 600, 50):
            myBins.append(i)
        for i in range(600, 1000, 100):
            myBins.append(i)
        for i in range(1000, 2000, 200):
            myBins.append(i)
        for i in range(2000, 3000, 500):
            myBins.append(i)
    else:
        raise Exception(ShellStyles.ErrorStyle() + "Please choose bin-level from -1 to 2" + ShellStyles.NormalStyle())
    return myBins

# Binning for data-driven control plots and final shapes feeded to combine
# Format: list of left bin edges; last entry is maximum value
_dataDrivenCtrlPlotBinning = {

    # Counters
    "WeightedCounters": None,

    #NVertices plots
    "NVertices_AfterStandardSelections": None,
    "NVertices_AfterAllSelections": None,

    # Jets
    "Njets_AfterStandardSelections": [0,1,2,3,4,5,6,7,8],
    "Njets_AfterBtagSF": [0,1,2,3,4,5,6,7,8],
    "JetPt_AfterStandardSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,170,190,220,250,300,400,500,1000],
    "JetPt_AfterBtagSF": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,170,190,220,250,300,400,500,1000],
    "JetPt_AfterAllSelections": [0,20,30,40,60,70,80,90,100,120,150,200,250,300,400,500,1000],
    "JetEta_AfterStandardSelections": [-4.5,-4.0,-3.5,-3.0,-2.5,-2.2,-2.0,-1.8,-1.6,-1.4,-1.2,-1.0,-0.8,-0.6,-0.4,-0.2,-0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.5,3.0,3.5,4.0,4.5],
    "JetEta_AfterAllSelections": [-4.5,-4.0,-3.5,-3.0,-2.5,-2.0,-1.5,-1.0,-0.5,0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5],
    "Njets_AfterBtagSF": [0,1,2,3,4,5,6,7,8],

    # B tagging
    "NBjets": [0,1,2,3,4,5,6,7,8],
    "NBjets_AfterAllSelections": [0,1,2,3,4,5,6,7,8],
    "BJetPt": [0,30,50,70,90,110,130,150,200,300,400,500],
    "BJetPt_AfterBtagSF": [0,30,50,70,90,110,130,150,200,300,400,500],
    "BJetPt_AfterAllSelections": [0,20,30,50,70,90,110,130,150,200,300,400,500],
    "BJetEta": [-2.5,-2.2,-2.0,-1.8,-1.6,-1.4,-1.2,-1.0,-0.8,-0.6,-0.4,-0.2,-0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.5],
    "BJetEta_AfterAllSelections": [-2.5,-2.0,-1.5,-1.0,-0.5,0.0,0.5,1.0,1.5,2.0,2.5],
    "BtagDiscriminator": [-1.0,-0.9,0.0,0.2,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
    "BtagDiscriminator_AfterAllSelections": [0.0,0.2,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
    "BJetSelection*": [0,1,2,3,4,5,6,7,8],

    # Angular cuts
    "CollinearAngularCutsMinimum*": [0,20,40,60,80,100,120,140,160,180,200,220,240,260],
    "BackToBackAngularCutsMinimum*": [0,20,40,60,80,100,120,140,160,180,200,220,240,260],
    "ImprovedDeltaPhiCuts*": [0,20,40,60,80,100,120,140,160,180,200,220,240,260],
    "MinDeltaPhiTauJet": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180],
    "MinDeltaPhiTauJet_AfterAllSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180],
    "MaxDeltaPhiTauJet": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180],
    "MaxDeltaPhiTauJet_AfterAllSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180],

<<<<<<< HEAD
    "TransverseMass*": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,600,700,800,900,1000], #extended to 5000
#    "TransverseMass*": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,350,400,500,600,700,800,900,1000,1500], # MIT rebin
=======
    # MET
    "MET": [0,20,40,60,80,100,120,140,160,200,250,300,400,500,600,700,800],
    "MET_AfterAllSelections": [0,20,40,60,80,100,120,140,160,180,200,250,300,400,500,600,700,800],
    "METPhi": [-3.14,-2.75,-2.36,-1.96,-1.57,-1.18,-0.79,-0.39,0.00,0.39,0.79,1.18,1.57,1.96,2.36,2.75,3.14],
    "METPhi_AfterAllSelections": [-3.14,-2.36,-1.57,-0.79,0.00,0.79,1.57,2.36,3.14],
    "METPhiMinusTauPhi": [0.00,0.39,0.79,1.18,1.57,1.96,2.36,2.75,3.14],
    "METPhiMinusTauPhi_AfterAllSelections": [0.00,0.39,0.79,1.18,1.57,1.96,2.36,2.75,3.14],
    "DeltaPhiTauMet_AfterAllSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180],
    "DeltaPhiTauMET_AfterAllSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180],
>>>>>>> origin/hw_analysis

    # Tau Pt + MET
    "TauPlusMETPt": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,450,500,600,700,800,900,1000],
    "TauPlusMETPt_AfterAllSelections": [0,40,80,120,160,200,240,280,320,360,400,450,500,600,700,800,900,1000],

<<<<<<< HEAD
    "tauPt": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,170,190,220,250,300,400,500],
    "muonPt": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,170,190,220,250,300,400,500],
    "nJet": [0,1,2,3,4,5,6,7,8,9,10],
    "nTau": [0,1,2,3,4,5,6,7,8,9,10], 

    "shapeInvariantMass": [0,20,40,60,80,100,120,140,160,200,300,400,500,600,700,800,900,1000,1500,2000,3000,4000,5000],
    "InvariantMass*": [0,20,40,60,80,100,120,140,160,200,400,500,600,700,800,900,1000,1500,2000,3000,4000,5000],
=======
    # Tau
>>>>>>> origin/hw_analysis
    "SelectedTau_pT_AfterStandardSelections": [0,50,60,70,80,90,100,110,120,130,140,150,170,190,220,250,300,400,500,600,700,800,900,1000],
    "SelectedTau_eta_AfterStandardSelections": [-2.5,-2.1,-2.0,-1.8,-1.6,-1.4,-1.2,-1.0,-0.8,-0.6,-0.4,-0.2,-0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.1,2.5],
    "SelectedTau_phi_AfterStandardSelections": [-3.14,-2.75,-2.36,-1.96,-1.57,-1.18,-0.79,-0.39,0.00,0.39,0.79,1.18,1.57,1.96,2.36,2.75,3.14],
    "SelectedTau_ldgTrkPt_AfterStandardSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,170,190,220,250,300,400,500,600,700,800,900,1000],
    "SelectedTau_Rtau_AfterStandardSelections": [0.75,0.78,0.80,0.82,0.84,0.86,0.88,0.90,0.92,0.94,0.96,0.98,1.00],
    "SelectedTau_Rtau_FullRange_AfterStandardSelections": [0.0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00],
    "SelectedTau_p_AfterStandardSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,170,190,220,250,300,400,500,600,700,800,900,1000],
    "SelectedTau_LeadingTrackP_AfterStandardSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,170,190,220,250,300,400,500,600,700,800,900,1000],
    "SelectedTau_DecayMode_AfterStandardSelections": None,
    "SelectedTau_Nprongs_AfterStandardSelections": None,
    "SelectedTau_source_AfterStandardSelections": None,
    "SelectedTau_pT_AfterAllSelections": [0,50,60,80,100,150,200,300,400,500,600,700,800,900,1000],
    "SelectedTau_eta_AfterAllSelections": [-2.5,-2.1,-1.8,-1.6,-1.4,-1.2,-1.0,-0.8,-0.6,-0.4,-0.2,-0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.1,2.5],
    "SelectedTau_phi_AfterAllSelections": [-3.14,-2.36,-1.57,-0.79,0.00,0.79,1.57,2.36,3.14],
    "SelectedTau_ldgTrkPt_AfterAllSelections": [0,20,40,50,60,70,80,100,150,200,300,400,500,600,700,800,900,1000],
    "SelectedTau_Rtau_FullRange_AfterAllSelections": [0.0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00],
    "SelectedTau_Rtau_AfterAllSelections": [0.75,0.78,0.80,0.82,0.84,0.86,0.88,0.90,0.92,0.94,0.96,0.98,1.00],
    "SelectedTau_p_AfterAllSelections": [0,20,40,50,60,70,80,100,150,200,300,500,600,700,800,900,1000],
    "SelectedTau_LeadingTrackP_AfterAllSelections": [0,41,60,80,100,150,200,300,500,600,700,800,900,1000],
    "SelectedTau_DecayMode_AfterAllSelections": None,
    "SelectedTau_Nprongs_AfterAllSelections": None,
    "SelectedTau_source_AfterAllSelections": None,

    # Top
    "TopMass": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,350,400,500],
    "TopMass_AfterAllSelections": [0,20,40,60,80,100,150,200,300,500,600,700,800,900,1000],
    "TopPt": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,350,400,500,600,700,800,900,1000],
    "TopPt_AfterAllSelections": [0,20,40,60,80,100,150,200,300,500,600,700,800,900,1000],

    # W
    "WPt": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,350,400,500,600,700,800,900,1000],
    "WPt_AfterAllSelections": [0,20,40,60,80,100,150,200,300,500,600,700,800,900,1000],
    "WMass": [0,10,20,30,40,50,60,70,80,90,100,100,120,130,140,160,180,200,250,300],
    "WMass_AfterAllSelections": [0,10,20,30,40,50,60,70,80,90,100,100,120,130,140,160,180,200,250,300],

    # Transverse and invariant mass
    "TransverseMass*": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,600,800,10000], 
    "shapeInvariantMass": [0,20,40,60,80,100,120,140,160,200,300,400,500,600,700,800,900,1000,1500,2000,3000,4000,5000],
    "InvariantMass*": [0,20,40,60,80,100,120,140,160,200,400,500,600,700,800,900,1000,1500,2000,3000,4000,5000],

###############################################################
### mT and MVA binnings for H+ -> tau nu limit extraction
###############################################################
# Constant binning used in pre-approval
#    "shapeTransverseMass": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,600,800,10000], # for pre-approval
# Cut-and-count, everything in one bin (cross check)
#    "shapeTransverseMass": [0.0, 10000.0]
# Automatic binning for RtauMore, threshold 0.2, DY inclusive
#    "shapeTransverseMass": [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0, 180.0, 190.0, 200.0, 210.0, 220.0, 230.0, 240.0, 260.0, 270.0, 290.0, 310.0, 370.0, 10000.0],
# Automatic binning for  RtauMore, threshold 0.2, DY HT binned
    "shapeTransverseMass": [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0, 180.0, 190.0, 200.0, 210.0, 220.0, 230.0, 240.0, 250.0, 260.0, 270.0, 280.0, 290.0, 300.0, 310.0, 320.0, 330.0, 340.0, 350.0, 370.0, 380.0, 390.0, 400.0, 410.0, 420.0, 440.0, 460.0, 490.0, 10000.0],
## Automatic binning for RtauLess, threshold 0.2, DY inclusive
#    "shapeTransverseMass": [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0, 180.0, 190.0, 200.0, 210.0, 220.0, 230.0, 240.0, 250.0, 260.0, 270.0, 280.0, 290.0, 300.0, 310.0, 320.0, 330.0, 350.0, 360.0, 380.0, 400.0, 420.0, 450.0, 530.0, 10000.0],
# Automatic binning for  RtauLess, threshold 0.2, DY HT binned
#    "shapeTransverseMass": [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0, 180.0, 190.0, 200.0, 210.0, 220.0, 230.0, 240.0, 250.0, 260.0, 270.0, 280.0, 290.0, 300.0, 310.0, 320.0, 330.0, 340.0, 350.0, 360.0, 370.0, 380.0, 390.0, 400.0, 410.0, 420.0, 430.0, 440.0, 450.0, 460.0, 470.0, 480.0, 490.0, 500.0, 510.0, 520.0, 530.0, 540.0, 560.0, 580.0, 590.0, 600.0, 610.0, 650.0, 690.0, 720.0, 1030.0, 10000.0],
# Constant binning for MVA discriminator (experimental), T and DY inclusive
#    "MVA": [-1.0,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
# Automatic binning for MVA discriminator, 0.2 threshold, TT and DY inclusive
    "MVA": [-1.0, -0.96, -0.92, -0.88, -0.84, -0.8, -0.76, -0.72, -0.64, -0.6, -0.52, -0.44, -0.36, -0.28, -0.20, -0.12, -0.04, 0.04, 0.15, 0.24, 0.32, 0.40, 0.48, 0.56, 0.64, 0.72, 0.76, 0.8, 0.84, 0.88, 0.92, 0.96, 1.0],
###############################################################

###############################################################
### HToTB specific binning settings
###############################################################
    "HT_AfterAllSelections"   : [i for i in range(500, 1000, 50)] + [i for i in range(1000, 1500, 100)] + [i for i in range(1500, 2500+200, 200)] + [3000],
    "MHT_AfterAllSelections"  : [i for i in range(0, 140, 10)] + [i for i in range(140, 240, 20)] + [i for i in range(240, 400, 50)],
    "QGLR_AfterAllSelections" : [float(i)/100.0 for i in range(0, 105, 5)],
    "LdgTrijetPt_AfterAllSelections"        : [j for j in range(0, 500, 50)] + [k for k in range(500, 900+100, 100)],
    "SubldgTrijetPt_AfterAllSelections"     : [j for j in range(0, 500, 50)] + [k for k in range(500, 900+100, 100)],
    "LdgTrijetMass_AfterAllSelections"      : [i for i in range(40, 360+20, 20)],
    "SubldgTrijetMass_AfterAllSelections"   : [i for i in range(40, 360+20, 20)],
    "LdgTrijetBjetPt_AfterAllSelections"    : [j for j in range(0, 300, 25)] + [k for k in range(300, 700+50, 50)],
    "SubldgTrijetBjetPt_AfterAllSelections" : [j for j in range(0, 300, 25)] + [k for k in range(300, 700+50, 50)],
    "LdgTrijetBjetEta_AfterAllSelections"   : None,
    "SubldgTrijetBjetEta_AfterAllSelections": None,
    "LdgTrijetBjetBdisc_AfterAllSelections" : None,
    "SubldgTrijetBjetBdisc_AfterAllSelections": None,
    "LdgTrijetDijetPt_AfterAllSelections"   : [j for j in range(0, 500, 25)] + [k for k in range(500, 700+50, 50)],
    "SubldgTrijetDijetPt_AfterAllSelections": [j for j in range(0, 500, 25)] + [k for k in range(500, 700+50, 50)],
    "LdgTrijetDijetMass_AfterAllSelections" : [i for i in range(0, 250+10, 10)],
    "SubldgTrijetDijetMass_AfterAllSelections": [i for i in range(0, 250+10, 10)],
    "LdgTrijetTopMassWMassRatioAfterAllSelections": None,
    "TetrajetBjetPt_AfterAllSelections"     : [j for j in range(0, 300, 20)] + [k for k in range(300, 500+40, 40)] + [600, 900],
    "TetrajetBjetEta_AfterAllSelections"    : None,
    "LdgTetrajetPt_AfterAllSelections"      : [j for j in range(0, 500, 20)] + [k for k in range(500, 700, 50)] + [k for k in range(700, 900+100, 100)],
    "SubldgTetrajetPt_AfterAllSelections"   : [j for j in range(0, 500, 20)] + [k for k in range(500, 700, 50)] + [k for k in range(700, 900+100, 100)],
    "LdgTetrajetMass_AfterAllSelections"    : getBinningForTetrajetMass(18),
    "SubldgTetrajetMass_AfterAllSelections" : getBinningForTetrajetMass(18),
    "Njets_AfterAllSelections"  : [i for i in range(7, 19, 1)],
    "Jet1Pt_AfterAllSelections" : [i for i in range(0,300, 20)] + [300, 400, 500, 700, 1000],
    "Jet2Pt_AfterAllSelections" : [i for i in range(0,300, 20)] + [300, 400, 500, 700],
    "Jet3Pt_AfterAllSelections" : [i for i in range(0,300, 20)] + [300, 400, 500],
    "Jet4Pt_AfterAllSelections" : [i for i in range(0,300, 20)] + [300, 400],
    "Jet5Pt_AfterAllSelections" : [i for i in range(0,300, 20)] + [300],
    "Jet6Pt_AfterAllSelections" : [i for i in range(0,300, 20)] + [300],
    "Jet7Pt_AfterAllSelections" : [i for i in range(0,200, 10)],
    "BJet1Pt_AfterAllSelections": [i for i in range(0,300, 20)] + [300, 400, 500, 700],
    "BJet2Pt_AfterAllSelections": [i for i in range(0,300, 20)] + [300, 400, 500, 700],
    "BJet3Pt_AfterAllSelections": [i for i in range(0,300, 20)] + [300, 400, 500],
    "Jet1Eta_AfterAllSelections"  : None,
    "Jet2Eta_AfterAllSelections"  : None,
    "Jet3Eta_AfterAllSelections"  : None,
    "Jet4Eta_AfterAllSelections"  : None,
    "Jet5Eta_AfterAllSelections"  : None,
    "Jet6Eta_AfterAllSelections"  : None,
    "Jet7Eta_AfterAllSelections"  : None,
    "BJet1Eta_AfterAllSelections" : None,
    "BJet2Eta_AfterAllSelections" : None,
    "BJet3Eta_AfterAllSelections" : None,
    "MET_AfterAllSelections"      : [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 250, 300], # tmp: clash with HToTauNu
    #
    "HT_AfterStandardSelections"   : [i for i in range(500, 1000, 50)] + [i for i in range(1000, 1500, 100)] + [i for i in range(1500, 2500+200, 200)] + [3000],
    "MHT_AfterStandardSelections"  : [i for i in range(0, 140, 10)] + [i for i in range(140, 240, 20)] + [i for i in range(240, 400, 50)],
    "QGLR_AfterStandardSelections" : [float(i)/100.0 for i in range(0, 105, 5)],
    "LdgTrijetPt_AfterStandardSelections"        : [j for j in range(0, 500, 50)] + [k for k in range(500, 900+100, 100)],
    "SubldgTrijetPt_AfterStandardSelections"     : [j for j in range(0, 500, 50)] + [k for k in range(500, 900+100, 100)],
    "LdgTrijetMass_AfterStandardSelections"      : [i for i in range(40, 360+20, 20)],
    "SubldgTrijetMass_AfterStandardSelections"   : [i for i in range(40, 360+20, 20)],
    "LdgTrijetBjetPt_AfterStandardSelections"    : [j for j in range(0, 300, 25)] + [k for k in range(300, 700+50, 50)],
    "SubldgTrijetBjetPt_AfterStandardSelections" : [j for j in range(0, 300, 25)] + [k for k in range(300, 700+50, 50)],
    "LdgTrijetBjetEta_AfterStandardSelections"   : None,
    "SubldgTrijetBjetEta_AfterStandardSelections": None,
    "LdgTrijetBjetBdisc_AfterStandardSelections" : None,
    "SubldgTrijetBjetBdisc_AfterStandardSelections": None,
    "LdgTrijetDijetPt_AfterStandardSelections"   : [j for j in range(0, 500, 25)] + [k for k in range(500, 700+50, 50)],
    "SubldgTrijetDijetPt_AfterStandardSelections": [j for j in range(0, 500, 25)] + [k for k in range(500, 700+50, 50)],
    "LdgTrijetDijetMass_AfterStandardSelections" : [i for i in range(0, 250+10, 10)],
    "SubldgTrijetDijetMass_AfterStandardSelections": [i for i in range(0, 250+10, 10)],
    "LdgTrijetTopMassWMassRatioAfterStandardSelections": None,
    "TetrajetBjetPt_AfterStandardSelections"     : [j for j in range(0, 300, 20)] + [k for k in range(300, 500+40, 40)] + [600, 900],
    "TetrajetBjetEta_AfterStandardSelections"    : None,
    "LdgTetrajetPt_AfterStandardSelections"      : [j for j in range(0, 500, 20)] + [k for k in range(500, 700, 50)] + [k for k in range(700, 900+100, 100)],
    "SubldgTetrajetPt_AfterStandardSelections"   : [j for j in range(0, 500, 20)] + [k for k in range(500, 700, 50)] + [k for k in range(700, 900+100, 100)],
    "LdgTetrajetMass_AfterStandardSelections"    : getBinningForTetrajetMass(18),
    "SubldgTetrajetMass_AfterStandardSelections" : getBinningForTetrajetMass(18),
    "Njets_AfterStandardSelections"  : [i for i in range(7, 19, 1)],
    "Jet1Pt_AfterStandardSelections" : [i for i in range(0,300, 20)] + [300, 400, 500, 700, 1000],
    "Jet2Pt_AfterStandardSelections" : [i for i in range(0,300, 20)] + [300, 400, 500, 700],
    "Jet3Pt_AfterStandardSelections" : [i for i in range(0,300, 20)] + [300, 400, 500],
    "Jet4Pt_AfterStandardSelections" : [i for i in range(0,300, 20)] + [300, 400],
    "Jet5Pt_AfterStandardSelections" : [i for i in range(0,300, 20)] + [300],
    "Jet6Pt_AfterStandardSelections" : [i for i in range(0,300, 20)] + [300],
    "Jet7Pt_AfterStandardSelections" : [i for i in range(0,200, 10)],
    "BJet1Pt_AfterStandardSelections": [i for i in range(0,300, 20)] + [300, 400, 500, 700],
    "BJet2Pt_AfterStandardSelections": [i for i in range(0,300, 20)] + [300, 400, 500, 700],
    "BJet3Pt_AfterStandardSelections": [i for i in range(0,300, 20)] + [300, 400, 500],
    "Jet1Eta_AfterStandardSelections"  : None,
    "Jet2Eta_AfterStandardSelections"  : None,
    "Jet3Eta_AfterStandardSelections"  : None,
    "Jet4Eta_AfterStandardSelections"  : None,
    "Jet5Eta_AfterStandardSelections"  : None,
    "Jet6Eta_AfterStandardSelections"  : None,
    "Jet7Eta_AfterStandardSelections"  : None,
    "BJet1Eta_AfterStandardSelections" : None,
    "BJet2Eta_AfterStandardSelections" : None,
    "BJet3Eta_AfterStandardSelections" : None,
    "MET_AfterStandardSelections"      : [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 250, 300], # tmp: clash with HToTauNu
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
