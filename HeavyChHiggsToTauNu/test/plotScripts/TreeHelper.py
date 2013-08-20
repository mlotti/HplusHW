#######################################################################################################
# TreeHelper module: 
# To be used in parallel with a plotting script, such as "plotHisto_DataMinusEwk_Template.py".
#
# The primary goal of this module is to have a clean way of plotting several histograms, 
# each with customised setting on x-label, y-label, and binWidthX. Future additionals would 
# be staight-forwards with the appropriate expansion of the __init__ module. Each histogram requires
# name, a tree expression  (for histogram), an x-label, a y-label and a binWidthX which defines the 
# desirable bin width in the x-axis. Therefore, to add a new histogram in 
# the plotting loop one needs create a new HistoTemplate class instance with all aforementioned qualities
# and add it (i.e. append it) to the HistoTemplateList to be plotted automatically.
# In order to remove/exclude a histogram from the plotting loop just do not append it in this list.

# NOTE: Please do not change this file. Copy it and re-name it.
#       Remember to include this file in your plotting script, such as "plotHisto_DataMinusEwk_Template.py".
#       Suggestions are more than welcome.
#######################################################################################################

######################################################################
### All imported modules here
######################################################################
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import ROOT
import math
from TreeVarHelper import * 

######################################################################
### Class definition here
######################################################################
class HistoTemplate:
    '''
    class HistoTemplate():
    Define the histogram names, their path in ROOT files, xLabels, yLabels and binWidthX. 
    '''

    def __init__(self, name, expr, xlabel, ylabel, binWidthX):
        # name: Define histogram name
        # expr: Define the tree expression 
        # xlabel: the xlabel for histogram. Set it to "None" if you want the original label to be used.
        # binWidthX: the bin-width of x-axis for histogram. Set it to "None" if you want the original width to be used.
        
        self.name      = name
        self.expr      = expr
        self.xlabel    = xlabel
        self.ylabel    = ylabel
        self.binWidthX = binWidthX

#######################################################################################################
### Define a Histogram List
#######################################################################################################
HistoList = []

### Define Histograms and their attributes here
### Standard variables
hTauPt = HistoTemplate("hTauPt", "%s >> TauPt(36, 40.0, 400.0)" % (TauPt), "p_{T}^{#tau-jet} (GeV/c)", "Events / %0.f GeV/c", None)
hMet = HistoTemplate("hMet", "%s >> Met(25, 0.0, 500.0)" % (Met), "E_{T}^{miss} (GeV)", "Events / %0.f GeV", None)
hMt_TauMet = HistoTemplate("hMt_TauMet", "%s >> Mt_TauMet(30, 0.0, 600.0)" % (Mt), "m_{T}(#tau-jet, E_{T}^{miss} (GeV/c^{2})", "Events / %0.f GeV/c^{2}", None)
hMHT = HistoTemplate("hMHT", "%s:%s >> MHT(50, 0.0, 1000.0)" % (MHT,MHT), "H_{T}^{miss} (GeV/c)", "Events / %0.f GeV/c", None)
hMHT_AllJets = HistoTemplate("hMHT_AllJets", "%s >> MHT_AllJets(50, 0.0, 1000.0)" % (MHT_AllJets), "H_{T}^{miss} (GeV/c)", "Events / %0.f GeV/c", None)
hMHT_SelJets = HistoTemplate("hMHT_SelJets", "%s >> MHT_SelJet(50, 0.0, 1000.0)" % (MHT_SelJets), "H_{T}^{miss} (GeV/c)", "Events / %0.f GeV/c", None)
hMHT_SelJetsInclTau = HistoTemplate("hMHT_SelJetsInclTau", "%s >> MHT_SelJetsInclTau(50, 0.0, 1000.0)" % (MHT_SelJetsInclTau), "H_{T}^{miss} (GeV/c)", "Events / %0.f GeV/c", None)
hDeltaPhiTauMet = HistoTemplate("hDeltaPhiTauMet", "%s >> DeltaPhiTauMet(18, 0.0, 180.0)" % (DeltaPhiTauMet),"#Delta#phi(#tau-jet, E_{T}^{miss}) (#circ)", "Events / %.1f ^{#circ}", None)
hDeltaPhiMetLdgJet = HistoTemplate("hDeltaPhiMetLdgJet", "%s >> DeltaPhiMetLdgJet(18, 0.0, 180.0)" % (DeltaPhiMetLdgJet), "#Delta#phi(jet_{1}, E_{T}^{miss}) (#circ)", "Events / %.1f ^{#circ}", None)
hDeltaPhiMetNLdgJet = HistoTemplate("hDeltaPhiMetNLdgJet", "%s >> DeltaPhiMetNLdgJet(18, 0.0, 180.0)" % (DeltaPhiMetNLdgJet), "#Delta#phi(jet_{2}, E_{T}^{miss}) (#circ)", "Events / %.1f ^{#circ}", None)
hDeltaPhiMetNNLdgJet = HistoTemplate("hDeltaPhiMetNNLdgJet", "%s >> DeltaPhiMetNNLdgJet(18, 0.0, 180.0)" % (DeltaPhiMetNNLdgJet), "#Delta#phi(jet_{2}, E_{T}^{miss}) (#circ)", "Events / %.1f ^{#circ}", None)
hDeltaPhiMetLdgJet_Vs_DeltaPhiTauMet = HistoTemplate("hDeltaPhiMetLdgJet_Vs_DeltaPhiTauMet", "%s:%s >> DeltaPhiMetLdgJet_Vs_DeltaPhiTauMet" % (DeltaPhiMetLdgJet, DeltaPhiTauMet), "#Delta#phi(#tau-jet, E_{T}^{miss}) (#circ)", "#Delta#phi(jet_{1}, E_{T}^{miss}) (#circ)", None)
hDeltaPhiMetNLdgJet_Vs_DeltaPhiTauMet = HistoTemplate("hDeltaPhiMetNLdgJet_Vs_DeltaPhiTauMet", "%s:%s >> DeltaPhiMetNLdgJet_Vs_DeltaPhiTauMet" % (DeltaPhiMetNLdgJet, DeltaPhiTauMet), "#Delta#phi(#tau-jet, E_{T}^{miss}) (#circ)", "#Delta#phi(jet_{2}, E_{T}^{miss}) (#circ)", None)
hDeltaPhiMetNNLdgJet_Vs_DeltaPhiTauMet = HistoTemplate("hDeltaPhiMetNNLdgJet_Vs_DeltaPhiTauMet", "%s:%s >> DeltaPhiMetNNLdgJet_Vs_DeltaPhiTauMet" % (DeltaPhiMetNNLdgJet, DeltaPhiTauMet), "#Delta#phi(#tau-jet, E_{T}^{miss}) (#circ)", "#Delta#phi(jet_{3}, E_{T}^{miss}) (#circ)", None)

### Event Shape Variables
hAlphaT = HistoTemplate("hAlphaT", "%s >> AlphaT(32, 0.0, 1.6)" % (AlphaT), "#alpha_{T}", "Events / %0.2f", None)
hAlphaT_Vs_Met = HistoTemplate("hAlphaT_Vs_Met", "%s,%s >> AlphaT_Vs_Met" % (AlphaT, Met), "E_{T}^{miss} (GeV)", "#alpha_{T}", None)
hAplanarity = HistoTemplate("hAplanarity", "%s >> Aplanarity(10, 0.0, 0.5)" % (Aplanarity), "Aplanarity (A)", "Events / %0.2f", None)
hCircularity = HistoTemplate("hCircularity", "%s >> Circularity(10, 0.0, 1.0)" % (Circularity), "Circularity (C)", "Events / %0.2f", None)
hCparameter = HistoTemplate("hCparameter", "%s >> Cparameter(10, 0.0, 1.0)" % (Cparameter), "C_{param}", "Events / %0.2f", None)
hDparameter = HistoTemplate("hDparameter", "%s >> Dparameter(10, 0.0, 1.0)" % (Dparameter), "D_{param}", "Events / %0.2f", None)
hJetThrust = HistoTemplate("hJetThrust", "%s >> JetThrust(10, 0.0, 1.0)" % (JetThrust), "T_{z}", "Events / %0.2f", None)
hPlanarity = HistoTemplate("hPlanarity", "%s >> Planarity(10, 0.0, 0.5)" % (Planarity), "Planarity (P)", "Events / %0.2f", None)
hSphericity = HistoTemplate("hSphericity", "%s >> Sphericity(10, 0.0, 1.0)" % (Sphericity), "Sphericity (S)", "Events / %0.2f", None)
hNFwdJets = HistoTemplate("hNFwdJets", "%s >> NFwdJets(8, 0.0, 8.0)" % (NFwdJets), "N_{jets}^{fwd}", "Events / %0.f", None)
hY_Vs_Sphericity = HistoTemplate("hY_Vs_Sphericity", "%s:%s >> Y_Vs_Sphericity" % (Y, Sphericity), "Sphericity (S)", "Y = (#sqrt{3}/2)*(Q_{2}-Q_{1})", None)
hHt = HistoTemplate("hHt", "%s >> HT(50, 0.0, 1000.0)" % (Ht), "H_{T} (GeV)", "Events / %0.f GeV", None)
hvDiJetMassesNoTau = HistoTemplate("hvDiJetMassesNoTau", "%s >> vDiJetMassesNoTau(50, 0.0, 500.0)" % (vDiJetMassesNoTau), "m(jet_{#alpha}, jet_{#beta}) (GeV/c^{2})", "Events / %0.f GeV/c^{2}", None)
hvDiJetMassesNoTauSum = HistoTemplate("hvDiJetMassesNoTauSum", "%s >> vDiJetMassesNoTauSum(10, 0.5, 10.5)" % (vDiJetMassesNoTauSum), "N(jet_{#alpha}, jet_{#beta}) ", "Events / %0.1f ", None)

### Isolated Lepton Veto
hEleMuDeltaR_Vs_Mt = HistoTemplate("hEleMuDeltaR_Vs_Mt", "%s:%s >> EleMuDeltaR_Vs_NonIsoMu_RelIso" % (NonIsoEle_EleMuDeltaR, Mt), "m_{T}(#tau-jet, E_{T}^{miss} (GeV/c^{2})", "#DeltaR(e, #mu)", None)
hEleMuDeltaR_Vs_NonIsoMu_RelIso = HistoTemplate("hEleMuDeltaR_Vs_NonIsoMu_RelIso", "%s:%s >> EleMuDeltaR_Vs_NonIsoMu_RelIso" % (NonIsoEle_EleMuDeltaR, NonIsoMu_RelIso), "Relative Isolation (#mu)", "#DeltaR(e, #mu)", None)
hNonIsoEle_DistanceOSTrk = HistoTemplate("hNonIsoEle_DistanceOSTrk", "%s >> NonIsoEle_DistanceOSTrk(20, 0.0, 20.0)" % (NonIsoEle_DistanceOSTrk), "Distance (OS Trk) (e)", "Events / %0.1f", None)
hNonIsoEle_EleMuDeltaR = HistoTemplate("hNonIsoEle_EleMuDeltaR", "%s >> NonIsoEle_EleMuDeltaR(20, 0.0, 10.0)" % (NonIsoEle_EleMuDeltaR), "#DeltaR(e, #mu)", "Events / %0.1f", None)
hNonIsoEle_IPwrtBeamSpot = HistoTemplate("hNonIsoEle_IPwrtBeamSpot", "%s >> NonIsoEle_IPwrtBeamSpot(20, 0.0, 10.0)" % (NonIsoEle_IPwrtBeamSpot), "IP_{beam-spot}^{e}", "Events / %0.2f", None)
hNonIsoEle_RelIso = HistoTemplate("hNonIsoEle_RelIso", "%s >> MonIsoEle_RelIso(50, 0.0, 100.0)" % (NonIsoEle_RelIso), "Relative Isolation (e)", "Events / %0.0f", None)
hNonIsoEle_Size = HistoTemplate("hNonIsoEle_Size", "%s >> NonIsoEle_Size(10, 0.0, 10.0)" % (NonIsoEle_Size), "N_{e}^{non-iso}", "Events / %0.f", None)
hNonIsoMu_IPTwrtBeamLine = HistoTemplate("hNonIsoMu_IPTwrtBeamLine", "%s >> NonIsoMu_IPTwrtBeamLine(25, -0.25, 0.25)" % (NonIsoMu_IPTwrtBeamLine), "IPT_{beam-line}^{#mu}", "Events / %0.2f", None)
hNonIsoMu_IPZwrtPV = HistoTemplate("hNonIsoMu_IPZwrtPV", "%s >> MonIsoMu_IPZwrtPV(40, -1.5, 0.5)" % (NonIsoMu_IPZwrtPV), "IPZ_{PV}^{#mu}", "Events / %0.2f", None)
hNonIsoMu_RelIso = HistoTemplate("hNonIsoMu_RelIso", "%s >> MonIsoMu_RelIso(50, 0.0, 100.0)" % (NonIsoMu_RelIso), "Relative Isolation (#mu)", "Events / %0.0f", None)
hNonIsoMu_Size = HistoTemplate("hNonIsoMu_Size", "%s >> NonIsoMu_Size(10, 0.0, 10.0)" % (NonIsoMu_Size), "N_{#mu}^{non-iso}", "Events / %0.f", None)

### Add/Remove Histograms to be plotted/considered here
HistoList.append(hTauPt)
#HistoList.append(hMet)
#HistoList.append(hMt_TauMet)
#HistoList.append(hMHT)
#HistoList.append(hMHT_AllJets)
#HistoList.append(hMHT_SelJets)
#HistoList.append(hMHT_SelJetsInclTau)
#HistoList.append(hDeltaPhiTauMet)
#HistoList.append(hDeltaPhiMetLdgJet)
#HistoList.append(hDeltaPhiMetNLdgJet)
#HistoList.append(hDeltaPhiMetNNLdgJet)
#HistoList.append(hDeltaPhiMetLdgJet_Vs_DeltaPhiTauMet)
#HistoList.append(hDeltaPhiMetNLdgJet_Vs_DeltaPhiTauMet)
#HistoList.append(hDeltaPhiMetNNLdgJet_Vs_DeltaPhiTauMet)

### Event Shape Variables
#HistoList.append(hAlphaT)
#HistoList.append(hAlphaT_Vs_Met)
#HistoList.append(hAplanarity)
#HistoList.append(hCircularity)
#HistoList.append(hCparameter)
#HistoList.append(hDparameter)
#HistoList.append(hJetThrust)
#HistoList.append(hPlanarity)
#HistoList.append(hSphericity)
#HistoList.append(hNFwdJets)
#HistoList.append(hY_Vs_Sphericity)
#HistoList.append(hHt)
#HistoList.append(hvDiJetMassesNoTau)
#HistoList.append(hvDiJetMassesNoTauSum)

### Isolated Lepton Veto
#HistoList.append(hEleMuDeltaR_Vs_Mt)
#HistoList.append(hEleMuDeltaR_Vs_NonIsoMu_RelIso)
#HistoList.append(hNonIsoEle_DistanceOSTrk)
#HistoList.append(hNonIsoEle_EleMuDeltaR)
#HistoList.append(hNonIsoEle_IPwrtBeamSpot)
#HistoList.append(hNonIsoEle_RelIso)
#HistoList.append(hNonIsoEle_Size)
#HistoList.append(hNonIsoMu_IPTwrtBeamLine)
#HistoList.append(hNonIsoMu_IPZwrtPV)
#HistoList.append(hNonIsoMu_RelIso)
#HistoList.append(hNonIsoMu_Size)
