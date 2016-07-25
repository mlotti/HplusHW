#######################################################################################################
# InvMassHistoHelper module: 
# To be used in parallel with a plotting script, such as "plotHisto_DataMinusEwk_Template.py".
#
# The primary goal of this module is to have a clean way of plotting several histograms, 
# each with customised setting on x-label, y-label, and binWidthX. Future additionals would 
# be staight-forwards with the appropriate expansion of the __init__ module. Each histogram requires
# name, a histogram path (in ROOT file), an x-label, a y-label and a binWidthX which defines the 
# desirable bin width in the x-axis. Therefore, to add a new histogram in 
# the plotting loop one needs create a new HistoTemplate class instance with all aforementioned qualities
# and add it (i.e. append it) to the HistoTemplateList to be plotted automatically.
# In order to remove/exclude a histogram from the plotting loop just do not append it in this list.

# NOTE: Please do not change this file. Use as it is or copy it and re-name it.
#       Remember to include this file in your plotting script, such as "plotHisto_DataMinusEwk_Template.py" 
#       or "plotFullHPlusMass.pye"
#######################################################################################################
class HistoTemplate:
    '''
    class HistoTemplate():
    Define the histogram names, their path in ROOT files, xLabels, yLabels and binWidthX. 
    '''

    def __init__(self, name, path, xlabel, ylabel, binWidthX):
        # name: Define histogram name
        # path: Define histogram path in ROOT file
        # xlabel: the xlabel for histogram. Set it to "None" if you want the original label to be used.
        # binWidthX: the bin-width of x-axis for histogram. Set it to "None" if you want the original width to be used.
        
        self.name      = name
        self.path      = path
        self.xlabel    = xlabel
        self.ylabel    = ylabel
        self.binWidthX = binWidthX

#######################################################################################################
# Class definition here
#######################################################################################################
class TH1:

    def __init__(self, name, units, xlabel, bLogX, binWidthX, ylabel, yMin, yMax, bLogY, bRatio, bNormalizeToOne, xLegMin, xLegMax, yLegMin, yLegMax, cutLines):

        self.name            = name
        self.units           = units
        if self.units == "":
            self.xlabel      = xlabel
        else:
            self.xlabel      = xlabel + " (" + units + ")"
        self.bLogX           = bLogX
        self.binWidthX       = binWidthX
        self.yMin            = yMin
        self.yMax            = yMax
        self.ylabel          = ylabel + " " + units
        self.bLogY           = bLogY
        self.bRatio          = bRatio
        self.bNormalizeToOne = bNormalizeToOne

        # print kwargs
        self.xLegMin = kwargs.get("xLegMin", 0.68)
        self.xLegMax = kwargs.get("xLegMax", 0.93)
        self.yLegMin = kwargs.get("yLegMin", 0.65)
        self.yLegMax = kwargs.get("yLegMax", 0.95)
        self.cutLines = kwargs.get("cutLines", [])

#######################################################################################################
class TH2:

    def __init__(self, name, xUnits, xlabel, bLogX, binWidthX, yUnits, ylabel, yMin, yMax, bLogY, bRatio, binWidthY, bNormalizeToOne, xLegMin, xLegMax, yLegMin, yLegMax):

        self.name            = name
        self.xUnits          = xUnits
        self.yUnits          = yUnits
        if self.xUnits == "":
            self.xlabel      = xlabel % (binWidthX)
        else:
            self.xlabel      = xlabel % (binWidthX) + " (" + xUnits + ")"
        self.bLogX           = bLogX
        self.binWidthX       = binWidthX
        if self.yUnits == "":
            self.ylabel      = ylabel % (binWidthY)
        else:
            self.ylabel      = ylabel % (binWidthY) + " (" + yUnits + ")"
        self.bRatio          = bRatio
        self.bLogY           = bLogY
        self.yMin            = yMin
        self.yMax            = yMax
        self.binWidthY       = binWidthY
        self.bNormalizeToOne = bNormalizeToOne

        # "kwargs" receives a dictionary containing all the keyword arguments to be used
        #print kwargs
        self.xLegMin = kwargs.get("xLegMin", 0.65)
        self.xLegMax = kwargs.get("xLegMax", 0.93)
        self.yLegMin = kwargs.get("yLegMin", 0.65)
        self.yLegMax = kwargs.get("yLegMax", 0.93)

#######################################################################################################
# Default keywords arguments
#######################################################################################################
kwargsLegTH1Default     = {"xLegMin": 0.65, "xLegMax": 0.90, "yLegMin": 0.65, "yLegMax": 0.92, "cutLines": []}
kwargsLegTH1Alt         = {"xLegMin": 0.2, "xLegMax": 0.45, "yLegMin": 0.65, "yLegMax": 0.92, "cutLines": []}
kwargsLegTH1InvMass     = {"xLegMin": 0.65, "xLegMax": 0.90, "yLegMin": 0.65, "yLegMax": 0.92, "cutLines": [80.0, 0.0]}
kwargsLegTH1InvMass_GEN = {"xLegMin": 0.65, "xLegMax": 0.90, "yLegMin": 0.65, "yLegMax": 0.92, "cutLines": [0.0]}
kwargsLegTH1TopMass     = {"xLegMin": 0.65, "xLegMax": 0.90, "yLegMin": 0.65, "yLegMax": 0.92, "cutLines": [172.5]}
kwargsLegTH2Default     = {"xLegMin": 0.60, "xLegMax": 0.85, "yLegMin": 0.85, "yLegMax": 0.92}
kwargsLegTH1Alt         = {"xLegMin": 0.2, "xLegMax": 0.45, "yLegMin": 0.85, "yLegMax": 0.92}
kwargs = {}

#######################################################################################################
# Define TH1 histograms
#######################################################################################################
TH1List = []
kwargs = kwargsLegTH1Default

# Standard
TauCandJetPt          = TH1("TauSelection/TauCand_JetPt", "GeV/c", "p_{T}^{#tau_{h} cand}", False, 10, "Events / %0.0f", None, None, True, True, False, *kwargs)
Met                   = TH1("MET/met", "GeV", "E_{T}^{miss}", False, 10, "Events / %0.0f", None, None, True, False, False, *kwargs)
kwargs = kwargsLegTH1InvMass
TransverseMass        = TH1("shapeTransverseMass", "GeV/c^{2}", "m_{T}(#tau_{h}, E_{T}^{miss})", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
InvariantMass         = TH1("shapeInvariantMass", "GeV/c^{2}", "m(#tau_{h}, E_{T}^{miss})", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)

kwargs = kwargsLegTH1Default
# Full HPlus mass-related
Discriminant          = TH1("FullHiggsMass/Discriminant", "GeV^{2}", "D", False, 2000, "Events / %0.0f", None, None, False, False, False, *kwargs)
Discriminant_GEN      = TH1("FullHiggsMass/Discriminant_GEN", "GeV^{2}", "D (GEN)", False, 2000, "Events / %0.0f", None, None, False, False, False, *kwargs)
Discriminant_GEN_NeutrinosReplacedWithMET = TH1("FullHiggsMass/Discriminant_GEN_NeutrinosReplacedWithMET", "GeV^{2}", "D (#nu_{#tau}#rightarrowE_{T}^{miss}, GEN)", False, 2000, "Events / %0.0f", None, None, False, False, False, *kwargs)
METSignificance = TH1("FullHiggsMass/METSignificance", "", "E_{T}^{miss} Significance", False, 10, "Events / %0.0f", None, None, False, False, False, *kwargs)
NeutrinoNumberInPassedEvents = TH1("FullHiggsMass/NeutrinoNumberInPassedEvents", "", "Number of #nu's (Passed Evts)", False, 1, "Events / %0.0f", None, None, False, False, False, *kwargs)
NeutrinoNumberInRejectedEvents = TH1("FullHiggsMass/NeutrinoNumberInRejectedEvents", "", "Number of #nu's (Rejected Evts)", False, 1, "Events / %0.0f", None, None, False, False, False, *kwargs)

kwargs = kwargsLegTH1InvMass_GEN
HiggsMass_GEN         = TH1("FullHiggsMass/HiggsMass_GEN", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})_{GEN}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMass_GEN_NeutrinosReplacedWithMET = TH1("FullHiggsMass/HiggsMass_GEN_NeutrinosReplacedWithMET", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau}#rightarrowE_{T}^{miss})_{GEN}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMass_GEN_greater = TH1("FullHiggsMass/HiggsMass_GEN_greater", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})_{GEN, greater}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMass_GEN_smaller = TH1("FullHiggsMass/HiggsMass_GEN_smaller", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})_{GEN, smaller}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMass_GEN_tauNuAngleMax = TH1("FullHiggsMass/HiggsMass_GEN_tauNuAngleMax", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})_{GEN, angle max}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMass_GEN_tauNuAngleMin = TH1("FullHiggsMass/HiggsMass_GEN_tauNuAngleMin", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})_{GEN, angle min}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMass_GEN_tauNuDeltaEtaMax = TH1("FullHiggsMass/HiggsMass_GEN_tauNuDeltaEtaMax", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})_{GEN, #Delta#eta max}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMass_GEN_tauNuDeltaEtaMin = TH1("FullHiggsMass/HiggsMass_GEN_tauNuDeltaEtaMin", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})_{GEN, #Delta#eta min}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMass_GEN_NuToMET_greater = TH1("FullHiggsMass/HiggsMass_GEN_NuToMET_greater", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau}#rightarrowE_{T}^{miss})_{GEN, greater}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMass_GEN_NuToMET_smaller = TH1("FullHiggsMass/HiggsMass_GEN_NuToMET_smaller", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau}#rightarrowE_{T}^{miss})_{GEN, smaller}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMass_GEN_NuToMET_tauNuAngleMax = TH1("FullHiggsMass/HiggsMass_GEN_NuToMET_tauNuAngleMax", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau}#rightarrowE_{T}^{miss})_{GEN, angle max}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMass_GEN_NuToMET_tauNuAngleMin = TH1("FullHiggsMass/HiggsMass_GEN_NuToMET_tauNuAngleMin", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau}#rightarrowE_{T}^{miss})_{GEN, angle min}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMass_GEN_NuToMET_tauNuDeltaEtaMax = TH1("FullHiggsMass/HiggsMass_GEN_NuToMET_tauNuDeltaEtaMax", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau}#rightarrowE_{T}^{miss})_{GEN, #Delta#eta max}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMass_GEN_NuToMET_tauNuDeltaEtaMin = TH1("FullHiggsMass/HiggsMass_GEN_NuToMET_tauNuDeltaEtaMin", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau}#rightarrowE_{T}^{miss})_{GEN, #Delta#eta min}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)

kwargs = kwargsLegTH1InvMass
HiggsMass             = TH1("FullHiggsMass/HiggsMass", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMassPositiveDiscriminant = TH1("FullHiggsMass/HiggsMassPositiveDiscriminant", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})_{D^{+}}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMassNegativeDiscriminant = TH1("FullHiggsMass/HiggsMassNegativeDiscriminant", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})_{D^{-}}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMass_betterSolution = TH1("FullHiggsMass/HiggsMass_betterSolution", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})_{better}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMass_worseSolution = TH1("FullHiggsMass/HiggsMass_worseSolution", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})_{worse}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMass_greater = TH1("FullHiggsMass/HiggsMass_greater", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})_{greater}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMass_smaller = TH1("FullHiggsMass/HiggsMass_smaller", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})_{smaller}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMass_tauNuAngleMax = TH1("FullHiggsMass/HiggsMass_tauNuAngleMax", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})_{angle max}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMass_tauNuAngleMin = TH1("FullHiggsMass/HiggsMass_tauNuAngleMin", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})_{angle min}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMass_tauNuDeltaEtaMax = TH1("FullHiggsMass/HiggsMass_tauNuDeltaEtaMax", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})_{#Delta#eta max}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMass_tauNuDeltaEtaMin = TH1("FullHiggsMass/HiggsMass_tauNuDeltaEtaMin", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})_{#Delta#eta min}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMassPure = TH1("FullHiggsMass/HiggsMassPure", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})_{pure}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMassImpure = TH1("FullHiggsMass/HiggsMassImpure", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})_{impure}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMassBadTau = TH1("FullHiggsMass/HiggsMassBadTau", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMassBadMET = TH1("FullHiggsMass/HiggsMassBadMET", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMassBadTauAndMET = TH1("FullHiggsMass/HiggsMassBadTauAndMET", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMassBadBjet = TH1("FullHiggsMass/HiggsMassBadBjet", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMassBadBjetAndTau = TH1("FullHiggsMass/HiggsMassBadBjetAndTau", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMassBadBjetAndMET = TH1("FullHiggsMass/HiggsMassBadBjetAndMET", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
HiggsMassBadBjetAndMETAndTau = TH1("FullHiggsMass/HiggsMassBadBjetAndMETAndTau", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)

kwargs = kwargsLegTH1TopMass
TopMassSolution = TH1("FullHiggsMass/TopMassSolution", "GeV/c^{2}", "m_{top} solution", False, 20, "Events / %0.0f", None, None, True, False, False, *kwargs)
TopInvariantMassInGenerator = TH1("FullHiggsMass/TopInvariantMassInGenerator", "GeV/c^{2}", "m_{top, GEN}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)

kwargs = kwargsLegTH1Default
SelectedNeutrinoPzSolution = TH1("FullHiggsMass/SelectedNeutrinoPzSolution", "GeV/c", "p_{z, #nu}", False, 20, "Events / %0.0f", None, None, False, False, False, *kwargs)
DiscriminantPure = TH1("FullHiggsMass/DiscriminantPure", "GeV^{2}", "D (pure)", True, 2000, "Events / %0.0f", None, None, False, False, False, *kwargs)
DiscriminantImpure = TH1("FullHiggsMass/DiscriminantImpure", "GeV^{2}", "D (impure)", True, 2000, "Events / %0.0f", None, None, False, False, False, *kwargs)
NeutrinosTauAngle1 = TH1("FullHiggsMass/NeutrinosTauAngle1", "GeV^{2}", "", False, 10, "Events / %0.0f", None, None, False, False, False, *kwargs)
NeutrinosTauAngle2 = TH1("FullHiggsMass/NeutrinosTauAngle2", "GeV^{2}", "", False, 10, "Events / %0.0f", None, None, False, False, False, *kwargs)
BDeltaR = TH1("FullHiggsMass/BDeltaR", "", "#DeltaR(b-jet, b-quark)", False, 0.2, "Events / %0.2f", None, None, True, False, False, *kwargs)
TauDeltaR = TH1("FullHiggsMass/TauDeltaR", "", "#DeltaR(#tau_{h}, #tau-visible)", False, 0.2, "Events / %0.2f", None, None, True, False, False, *kwargs)
METDeltaPt = TH1("FullHiggsMass/METDeltaPt", "GeV", "E_{T}^{miss} - E_{T, GEN}^{miss}", False, 10, "Events / %0.0f", None, None, False, False, False, *kwargs)
METDeltaPhi = TH1("FullHiggsMass/METDeltaPhi", "#circ", "#Delta#phi(E_{T}^{miss} - E_{T, GEN}^{miss})", False, 10, "Events / %0.0f", None, None, False, False, False, *kwargs)

DeltaPhiTauAndMetForBadMet = TH1("FullHiggsMass/DeltaPhiTauAndMetForBadMet", "#circ", "#Delta#phi(#tau_{h} , E_{T}^{miss})_{E_{T, bad}^{miss}}", False, 10, "Events / %0.0f", None, None, False, False, False, *kwargs)
DeltaPhiTauAndBjetForBadMet = TH1("FullHiggsMass/DeltaPhiTauAndBjetForBadMet", "#circ", "#Delta#phi(#tau_{h} , b-jet)_{E_{T, bad}^{miss}}", False, 10, "Events / %0.0f", None, None, False, False, False, *kwargs)
DeltaRTauAndMetForBadMet = TH1("FullHiggsMass/DeltaRTauAndMetForBadMet", "", "#DeltaR(#tau_{h} , E_{T}^{miss})_{E_{T, bad}^{miss}}", False, 0.2, "Events / %0.2f", None, None, False, False, False, *kwargs)
DeltaRTauAndBjetForBadMet = TH1("FullHiggsMass/DeltaRTauAndBjetForBadMet", "", "#DeltaR(#tau_{h} , b-jet)_{E_{T, bad}^{miss}}", False, 0.2, "Events / %0.2f", None, None, False, False, False, *kwargs)

#######################################################################################################
# Append TH1 histograms to plotting lists
#######################################################################################################
#TH1List.append(TauCandJetPt)
#TH1List.append(Met)
#TH1List.append(TransverseMass)
#TH1List.append(InvariantMass)
#
#TH1List.append(Discriminant)
#TH1List.append(Discriminant_GEN)
#TH1List.append(Discriminant_GEN_NeutrinosReplacedWithMET)
TH1List.append(HiggsMassPositiveDiscriminant)
TH1List.append(HiggsMassNegativeDiscriminant)
#TH1List.append(HiggsMass_betterSolution)
#TH1List.append(HiggsMass_worseSolution)
#TH1List.append(TopInvariantMassInGenerator)
#TH1List.append(METSignificance)
#TH1List.append(NeutrinoNumberInPassedEvents)
#TH1List.append(NeutrinoNumberInRejectedEvents)
TH1List.append(HiggsMass)
#TH1List.append(HiggsMass_greater)
#TH1List.append(HiggsMass_smaller)
#TH1List.append(HiggsMass_tauNuAngleMax)
#TH1List.append(HiggsMass_tauNuAngleMin)
#TH1List.append(HiggsMass_tauNuDeltaEtaMax)
#TH1List.append(HiggsMass_tauNuDeltaEtaMin)
#
#TH1List.append(HiggsMass_GEN)
#TH1List.append(HiggsMass_GEN_NeutrinosReplacedWithMET)
#TH1List.append(HiggsMass_GEN_greater)
#TH1List.append(HiggsMass_GEN_smaller)
#TH1List.append(HiggsMass_GEN_tauNuAngleMax)
#TH1List.append(HiggsMass_GEN_tauNuAngleMin)
#TH1List.append(HiggsMass_GEN_tauNuDeltaEtaMax)
#TH1List.append(HiggsMass_GEN_tauNuDeltaEtaMin)
#TH1List.append(HiggsMass_GEN_NuToMET_greater)
#TH1List.append(HiggsMass_GEN_NuToMET_smaller)
#TH1List.append(HiggsMass_GEN_NuToMET_tauNuAngleMax)
#TH1List.append(HiggsMass_GEN_NuToMET_tauNuAngleMin)
#TH1List.append(HiggsMass_GEN_NuToMET_tauNuDeltaEtaMax)
#TH1List.append(HiggsMass_GEN_NuToMET_tauNuDeltaEtaMin)
#TH1List.append(TopMassSolution)
#TH1List.append(SelectedNeutrinoPzSolution)
#
#TH1List.append(HiggsMassPure)
#TH1List.append(HiggsMassImpure)
#TH1List.append(HiggsMassBadTau)
#TH1List.append(HiggsMassBadMET)
#TH1List.append(HiggsMassBadTauAndMET)
#TH1List.append(HiggsMassBadBjet)
#TH1List.append(HiggsMassBadBjetAndTau)
#TH1List.append(HiggsMassBadBjetAndMET)
#TH1List.append(HiggsMassBadBjetAndMETAndTau)
#
#TH1List.append(DiscriminantPure)
#TH1List.append(DiscriminantImpure)
#TH1List.append(NeutrinosTauAngle1)
#TH1List.append(NeutrinosTauAngle2)
#TH1List.append(BDeltaR)
#TH1List.append(TauDeltaR)
#TH1List.append(METDeltaPt)
#TH1List.append(METDeltaPhi)
#
#TH1List.append(DeltaPhiTauAndMetForBadMet)
#TH1List.append(DeltaPhiTauAndBjetForBadMet)
#TH1List.append(DeltaRTauAndMetForBadMet)
#TH1List.append(DeltaRTauAndBjetForBadMet)

#######################################################################################################
# Define TH2 histograms
#######################################################################################################
TH2List = []
kwargs = kwargsLegTH2Default

TransMassVsInvMass = TH2("FullHiggsMass/TransMassVsInvMass", "GeV/c^{2}", "m_{T}(#tau_{h}, E_{T}^{miss}) / %0.0f", False, 20, "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau}) / %0.0f", None, None, False, False, 20, False, *kwargs)
TransMassVsInvMassPositiveDiscriminant = TH2("FullHiggsMass/TransMassVsInvMassPositiveDiscriminant", "GeV/c^{2}", "m_{T}(#tau_{h}, E_{T}^{miss}) / %0.0f", False, 20, "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})_{D^{+}} / %0.0f", None, None, False, False, 20, False, *kwargs)
TransMassVsInvMassNegativeDiscriminant = TH2("FullHiggsMass/TransMassVsInvMassNegativeDiscriminant", "GeV/c^{2}", "m_{T}(#tau_{h}, E_{T}^{miss}) / %0.0f", False, 20, "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau})_{D^{-}} / %0.0f", None, None, False, False, 20, False, *kwargs)
TopMassVsInvMass = TH2("FullHiggsMass/TopMassVsInvMass", "GeV/c^{2}", "m_{top} / %0.0f", False, 20, "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau}) / %0.0f", None, None, False, False, 20, False, *kwargs)
TopMassVsNeutrinoNumber = TH2("FullHiggsMass/TopMassVsNeutrinoNumber", "GeV/c^{2}", "m_{top} / %0.0f", False, 20, "", "Number of #nu's / %0.f", None, None, False, False, 1, False, *kwargs)
InvMassVsNeutrinoNumber = TH2("FullHiggsMass/InvMassVsNeutrinoNumber", "GeV/c^{2}", "m(#tau_{h}, #nu_{#tau}) / %0.0f", False, 20, "", "Number of #nu's / %0.f", None, None, False, False, 1, False, *kwargs)
METSignificanceVsBadMet = TH2("FullHiggsMass/METSignificanceVsBadMet", "", "E_{T}^{miss} Significance / %0.0f", False, 20, "GeV", "E_{T, bad}^{miss}/ %0.f", None, None, False, False, 20, False, *kwargs)

#######################################################################################################
# Append TH2 histograms to plotting lists
#######################################################################################################
TH2List.append(TransMassVsInvMass)
TH2List.append(TransMassVsInvMassPositiveDiscriminant)
TH2List.append(TransMassVsInvMassNegativeDiscriminant)
TH2List.append(TopMassVsInvMass)
TH2List.append(TopMassVsNeutrinoNumber)
TH2List.append(InvMassVsNeutrinoNumber)
TH2List.append(METSignificanceVsBadMet)
