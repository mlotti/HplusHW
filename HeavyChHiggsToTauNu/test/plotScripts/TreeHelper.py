#!/usr/bin/env python

######################################################################
# All imported modules here
######################################################################
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or

######################################################################
### Tree Variables: HIG-12-037 #HIG-11-019
######################################################################
### 1) Tau-jet 
TauPt      = "tau_p4.Pt()"
TauEta     = "abs(tau_p4.Eta())"
TauIso     = "tau_id_byMediumCombinedIsolationDeltaBetaCorr" #"tau_id_byTightIsolation"
Rtau       = "tau_leadPFChargedHadrCand_p4.P() / tau_p4.P()"
TauEleDisc = "tau_id_againstElectronMVA" #"tau_id_againstElectronMedium"
TauMuDisc  = "tau_id_againstMuonTight" #"tau_id_againstMuonTight"
TauIsFake  = "TauIsFake" #True if the selected tau is fake (MC only)

### 2) Isolated e/mu veto

### 3) Jets
NJets    = "jets_p4@.size()"
JetsPt   = "Sum$(jets_p4.Pt()>=30)"
JetsEta  = "Sum$(abs(jets_p4.Eta())<=2.4)"
NFwdJets = "Sum$(abs(jets_p4.Eta()) >= 1.5)" #TEC starts at eta>=1.0

### 4) MET
Met = "met_p4.Et()"

### 5) Btagging
Btag = "passedBTagging"

### 6) DeltaPhi(tau,MET)
DeltaPhiTauMet = "TMath::ACos(( tau_p4.X()*met_p4.px() + tau_p4.Y()*met_p4.py())/( tau_p4.Et()*met_p4.Et() ))*(180/TMath::Pi())"

### 7) mT(tau,MET) 
Mt = "TMath::Sqrt(2*tau_p4.Et()*met_p4.Et()*( 1.0 - ( tau_p4.X()*met_p4.px() + tau_p4.Y()*met_p4.py())/( tau_p4.Et()*met_p4.Et() )))"

### A) Event Shape Variables
Sphericity    = "sphericity"
Aplanarity    = "aplanarity"
Planarity     = "planarity"
Circularity   = "circularity"
AlphaT        = "alphaT"
QOne          = "QOne"
QTwo          = "QTwo"
QThree        = "QThree"
Y             = "(TMath::Sqrt(3)/2.0)*(QTwo-QOne)"
SphericityAlt = "1.5*(QTwo+QOne)"
AplanarityAlt = "1.5*(QOne)"
PlanarityAlt  = "1.5*(shpericity-2*aplanarity)"

### B) Leading Jets 
LdgJet      = "jets_p4[0]"
NLdgJet     = "jets_p4[1]"
NNLdgJet    = "jets_p4[2]"
Ht          = "Sum$(jets_p4.Pt())"
MHT         = "MHT_p4.Pt()" 
MHT_SelJets = "MHT_SelJets_p4.Pt()" 
MHT_AllJets = "MHT_AllJets_p4.Pt()" 
MHTcustom   = "TMath::Sqrt( pow(Sum$(jets_p4.Px()),2) + pow(Sum$(jets_p4.Py()),2) )" # I think this is correct (need to check)

### C) DeltaPhi(jet,MHT)
DeltaPhiMHTLdgJet   = "TMath::ACos(( MHT_p4.X()*jets_p4[0].px() + MHT_p4.Y()*jets_p4[0].py())/( MHT_p4.Et()*jets_p4[0].Et() ))*(180/TMath::Pi())"
DeltaPhiMHTNLdgJet  = "TMath::ACos(( MHT_p4.X()*jets_p4[1].px() + MHT_p4.Y()*jets_p4[1].py())/( MHT_p4.Et()*jets_p4[1].Et() ))*(180/TMath::Pi())"
DeltaPhiMHTNNLdgJet = "TMath::ACos(( MHT_p4.X()*jets_p4[2].px() + MHT_p4.Y()*jets_p4[2].py())/( MHT_p4.Et()*jets_p4[2].Et() ))*(180/TMath::Pi())"

### D) DeltaPhi(jet,MET)
DeltaPhiMetLdgJet   = "TMath::ACos(( met_p4.px()*jets_p4[0].px() + met_p4.py()*jets_p4[0].py())/( met_p4.Et()*jets_p4[0].Et() ))*(180/TMath::Pi())"
DeltaPhiMetNLdgJet  = "TMath::ACos(( met_p4.px()*jets_p4[1].px() + met_p4.py()*jets_p4[1].py())/( met_p4.Et()*jets_p4[1].Et() ))*(180/TMath::Pi())"
DeltaPhiMetNNLdgJet = "TMath::ACos(( met_p4.px()*jets_p4[2].px() + met_p4.py()*jets_p4[2].py())/( met_p4.Et()*jets_p4[2].Et() ))*(180/TMath::Pi())"

### E) Other
LdgJetNLdgJetPtSum   = "jets_p4[0].Pt() + jets_p4[1].Pt()"
DeltaHtTwoLdgJets    = Ht + "-" + LdgJetNLdgJetPtSum
DeltaPtLdgJetNLdgJet = "jets_p4[0].Pt() - jets_p4[1].Pt()"

######################################################################
### Per-event cuts: HIG-12-037 #HIG-11-019
######################################################################
### 1) Tau-jet 
TauPtCut        = TauPt + ">=41"
TauEtaCut       = TauEta + "<=2.1"
TauIsoCut       = TauIso + ">= 0.5"  #">= 1.0" 
RtauCut         = Rtau + ">= 0.7" 
TauEleDiscCut   = TauEleDisc + ">=1"
TauMuDiscCut    = TauMuDisc + ">=1"
TauIsFakeCut    = "TauIsFake==1"
TauIsNotFakeCut = "TauIsFake==0"
TauCandCut      = And(TauPtCut, TauEtaCut, TauEleDiscCut, TauMuDiscCut)
TauIDCut        = TauIsoCut + "&&" + RtauCut

### 2) Isolated e/mu veto

### 3) Jets
NJetsCut         = NJets + ">=3"
JetsPtCut        = JetsPt + ">=3"
JetsEtaCut       = JetsEta + ">=3"
NFwdJetsCutValue = "<=1"
NFwdJetsCut      = NFwdJets + NFwdJetsCutValue

### 4) MET
MetCut = Met + ">= 60" #">=50"

### 5) Btagging
BtagCut =  Btag + ">=1.0"

### 6) DeltaPhi(tau,MET)
DeltaPhiTauMetCut = DeltaPhiTauMet + "<= 160"

### 7) mT(tau,MET)
MtCutValue = " >= 80"
MtCut = Mt + MtCutValue

### A) Event Shape Variables
SphericityCut  = Sphericity + ">= 0.9"
AplanarityCut  = Aplanarity + "<= 0.1"
PlanarityCut   = Planarity  + "<= 0.3"
CircularityCut = Circularity + ">= 0.35"
AlphaTCut      = AlphaT + ">= 0.45"
QOneCut        = QOne + ">= 0.0"
QTwoCut        = QTwo + ">= 0.0"
QThreeCut      = QThree + ">= 0.0"
YCut           = Y + ">= 0.0"
SphericityAltCut = SphericityAlt + ">= 0.9"
AplanarityAltCut = AplanarityAlt + "<= 0.1"
PlanarityAltCut  = PlanarityAlt + "<= 0.3" 

### B) Leading Jets
LdgJetCut      = LdgJet + ".Pt()>=0.0"
NLdgJetCut     = NLdgJet + ".Pt()>=0.0"
NNLdgJetCut    = NNLdgJet + ".Pt()>=0.0"
HtCut          = Ht + ">= 120"
MHTCut         = MHT + ">=60"
MHT_SelJetsCut = MHT_SelJets + ">=60"
MHT_AllJetsCut = MHT_AllJets + ">=60"
MHTcustomCut   = MHTcustom + ">=60"

### C) DeltaPhi(jet, MHT)
DeltaPhiMHTLdgJetCut   = DeltaPhiMHTLdgJet + ">=60"
DeltaPhiMHTNLdgJetCut  = DeltaPhiMHTNLdgJet + ">=60"
DeltaPhiMHTNNLdgJetCut = DeltaPhiMHTNNLdgJet + ">=60"

### D) DeltaPhi(jet,MET)
DeltaPhiMetLdgJetCut   = DeltaPhiMetLdgJet + ">= 60"
DeltaPhiMetNLdgJetCut  = DeltaPhiMetLdgJet + ">= 60"
DeltaPhiMetNNLdgJetCut = DeltaPhiMetLdgJet + ">= 60"

### E) Other
LdgJetNLdgJetPtSumCut = LdgJetNLdgJetPtSum + ">=0"
DeltaHtTwoLdgJetsCut  = DeltaHtTwoLdgJets + ">=0"
DeltaPtLdgJetNLdgJet  = DeltaPtLdgJetNLdgJet + ">=0"


######################################################################
### Cut combinations: 
######################################################################
### Standard Cuts
JetSelectionCuts       = "" # this should suffice
JetSelectionSanityCuts = And(NJetsCut, JetsPtCut, JetsEtaCut, TauCandCut) #sanity check

JetSelectionMtCuts     = And(JetSelectionSanityCuts, MtCut)
MetBtagCuts            = And(JetSelectionSanityCuts, MetCut, BtagCut)
MetBtagDeltaPhiCuts    = And(JetSelectionSanityCuts, MetCut, BtagCut, DeltaPhiTauMetCut)
MetBtagDeltaPhiMtCuts  = And(JetSelectionSanityCuts, MetCut, BtagCut, DeltaPhiTauMetCut, MtCut)
TauIDMetBtagCuts       = And(JetSelectionSanityCuts, TauIDCut, MetCut, BtagCut)
AllSelectionCuts       = And(JetSelectionSanityCuts, TauIDCut, MetCut, BtagCut, DeltaPhiTauMetCut)

### Trial Cuts
MetBtagDeltaPhiNFwdJetCuts = And(JetSelectionSanityCuts, MetCut, BtagCut, DeltaPhiTauMetCut, NFwdJetsCut)
MetBtagDeltaPhiSpherCuts   = And(JetSelectionSanityCuts, MetCut, BtagCut, DeltaPhiTauMetCut, SphericityCut)
MetBtagDeltaPhiAplanCuts   = And(JetSelectionSanityCuts, MetCut, BtagCut, DeltaPhiTauMetCut, AplanarityCut)
MetBtagDeltaPhiPlanCuts    = And(JetSelectionSanityCuts, MetCut, BtagCut, DeltaPhiTauMetCut, PlanarityCut)
MetBtagDeltaPhiCircCuts    = And(JetSelectionSanityCuts, MetCut, BtagCut, DeltaPhiTauMetCut, CircularityCut)
MetBtagDeltaPhiAlphaTCuts  = And(JetSelectionSanityCuts, MetCut, BtagCut, DeltaPhiTauMetCut, AlphaTCut)

######################################################################
### Function definition here
######################################################################
def GetDictionaries():
    '''
    def GetDictionaries():
    Defines the histogram names, histogram tree expressions, xLabels and yLabels. These are all mapped to a unique histogram name (hName) key.
    '''

    ### Define histogram name, expression, and binning here: "hName": "Y:X >> tmpName" % (Y, X)
    histoDict = {
        "DeltaPhiMHTLdgJet": "%s >> DeltaPhiMHTLdgJet(18, 0.0, 180.0)" % (DeltaPhiMHTLdgJet),
        #"DeltaPhiMHTNLdgJet": "%s >> DeltaPhiMHTNLdgJet(18, 0.0, 180.0)" % (DeltaPhiMHTNLdgJet),
        #"DeltaPhiMHTNNLdgJet": "%s >> DeltaPhiMHTNNLdgJet(18, 0.0, 180.0)" % (DeltaPhiMHTNNLdgJet),

        #"DeltaPhiMetLdgJet": "%s >> DeltaPhiMetLdgJet(18, 0.0, 180.0)" % (DeltaPhiMetLdgJet),
        #"DeltaPhiMetNLdgJet": "%s >> DeltaPhiMetNLdgJet(18, 0.0, 180.0)" % (DeltaPhiMetNLdgJet),
        #"DeltaPhiMetNNLdgJet": "%s >> DeltaPhiMetNNLdgJet(18, 0.0, 180.0)" % (DeltaPhiMetNNLdgJet),

        #"DeltaPhiTauMet": "%s >> DeltaPhiMHTLdgJet(18, 0.0, 180.0)" % (DeltaPhiTauMet),
        #"MHTSelJets_Vs_MHTAllJets": "%s:%s >> MHTSelJets_Vs_MHTSelJets" % (MHT_AllJets, MHT_SelJets),

        #"DeltaPhiMHTLdgJet_Vs_DeltaPhiTauMet": "%s:%s >> DeltaPhiMHTLdgJet_Vs_DeltaPhiTauMet" % (DeltaPhiMHTLdgJet, DeltaPhiTauMet),
        #"DeltaPhiMHTNLdgJet_Vs_DeltaPhiTauMet": "%s:%s >> DeltaPhiMHTNLdgJet_Vs_DeltaPhiTauMet" % (DeltaPhiMHTNLdgJet, DeltaPhiTauMet),
        #"DeltaPhiMHTNNLdgJet_Vs_DeltaPhiTauMet": "%s:%s >> DeltaPhiMHTNNLdgJet_Vs_DeltaPhiTauMet" % (DeltaPhiMHTNNLdgJet, DeltaPhiTauMet),

        #"DeltaPhiMetLdgJet_Vs_DeltaPhiTauMet": "%s:%s >> DeltaPhiMetLdgJet_Vs_DeltaPhiTauMet" % (DeltaPhiMetLdgJet, DeltaPhiTauMet),
        #"DeltaPhiMetNLdgJet_Vs_DeltaPhiTauMet": "%s:%s >> DeltaPhiMetNLdgJet_Vs_DeltaPhiTauMet" % (DeltaPhiMetNLdgJet, DeltaPhiTauMet),
        #"DeltaPhiMetNNLdgJet_Vs_DeltaPhiTauMet": "%s:%s >> DeltaPhiMetNNLdgJet_Vs_DeltaPhiTauMet" % (DeltaPhiMetNNLdgJet, DeltaPhiTauMet),

        #"MHT": "%s:%s >> MHT(50, 0.0, 1000.0)" % (MHT,MHT),
        #"MHT_SelJets": "%s >> MHT_SelJet(50, 0.0, 1000.0)" % (MHT_SelJets),
        #"MHT_AllJets": "%s >> MHT_SelJet(50, 0.0, 1000.0)" % (MHT_AllJets),
        }
    
    ### Define histogram name, expression, and binning here: "hName": "xLabel"
    xLabelDict = {
        "DeltaPhiMHTLdgJet": "#Delta#phi(jet_{1}, H_{T}^{miss}) (#circ)",
        "DeltaPhiMHTNLdgJet": "#Delta#phi(jet_{2}, H_{T}^{miss}) (#circ)",
        "DeltaPhiMHTNNLdgJet": "#Delta#phi(jet_{3}, H_{T}^{miss}) (#circ)",

        "DeltaPhiMetLdgJet": "#Delta#phi(jet_{1}, E_{T}^{miss}) (#circ)",
        "DeltaPhiMetNLdgJet": "#Delta#phi(jet_{2}, E_{T}^{miss}) (#circ)",
        "DeltaPhiMetNNLdgJet": "#Delta#phi(jet_{3}, E_{T}^{miss}) (#circ)",

        "DeltaPhiTauMet": "#Delta#phi(#tau-jet, E_{T}^{miss}) (#circ)",
        "MHTSelJets_Vs_MHTAllJets": "H_{T}^{miss} for Sel Jets (GeV/c)",

        "DeltaPhiMHTLdgJet_Vs_DeltaPhiTauMet": "#Delta#phi(#tau-jet, E_{T}^{miss}) (#circ)",
        "DeltaPhiMHTNLdgJet_Vs_DeltaPhiTauMet": "#Delta#phi(#tau-jet, E_{T}^{miss}) (#circ)",
        "DeltaPhiMHTNNLdgJet_Vs_DeltaPhiTauMet": "#Delta#phi(#tau-jet, E_{T}^{miss}) (#circ)",

        "DeltaPhiMetLdgJet_Vs_DeltaPhiTauMet": "#Delta#phi(#tau-jet, E_{T}^{miss}) (#circ)",
        "DeltaPhiMetNLdgJet_Vs_DeltaPhiTauMet": "#Delta#phi(#tau-jet, E_{T}^{miss}) (#circ)",
        "DeltaPhiMetNNLdgJet_Vs_DeltaPhiTauMet": "#Delta#phi(#tau-jet, E_{T}^{miss}) (#circ)",

        "MHT": "H_{T}^{miss} (GeV/c)",
        "MHT_SelJets": "H_{T}^{miss} (GeV/c)",
        "MHT_AllJets": "H_{T}^{miss} (GeV/c)",
        }
    
    ### Define histogram name, expression, and binning here: "hName": "yLabel"
    yLabelDict = {
        "DeltaPhiMHTLdgJet": "Events / %.1f ^{#circ}",
        "DeltaPhiMHTNLdgJet": "Events / %.1f ^{#circ}",
        "DeltaPhiMHTNNLdgJet": "Events / %.1f ^{#circ}",

        "DeltaPhiMetLdgJet": "Events / %.1f ^{#circ}",
        "DeltaPhiMetNLdgJet": "Events / %.1f ^{#circ}",
        "DeltaPhiMetNNLdgJet": "Events / %.1f ^{#circ}",

        "DeltaPhiTauMet": "Events / %.1f ^{#circ}",
        "MHTSelJets_Vs_MHTAllJets": "H_{T}^{miss} for All Jets (GeV/c)",

        "DeltaPhiMHTLdgJet_Vs_DeltaPhiTauMet": "#Delta#phi(jet_{1}, H_{T}^{miss}) (#circ)",
        "DeltaPhiMHTNLdgJet_Vs_DeltaPhiTauMet": "#Delta#phi(jet_{2}, H_{T}^{miss}) (#circ)",
        "DeltaPhiMHTNNLdgJet_Vs_DeltaPhiTauMet": "#Delta#phi(jet_{3}, H_{T}^{miss}) (#circ)",

        "DeltaPhiMetLdgJet_Vs_DeltaPhiTauMet": "#Delta#phi(jet_{1}, E_{T}^{miss}) (#circ)",
        "DeltaPhiMetNLdgJet_Vs_DeltaPhiTauMet": "#Delta#phi(jet_{2}, E_{T}^{miss}) (#circ)",
        "DeltaPhiMetNNLdgJet_Vs_DeltaPhiTauMet": "#Delta#phi(jet_{3}, E_{T}^{miss}) (#circ)",

        "MHT": "H_{T}^{miss} (GeV/c)",
        "MHT_SelJets": "H_{T}^{miss} (GeV/c)",
        "MHT_AllJets": "H_{T}^{miss} (GeV/c)",
        }
            
    return histoDict, xLabelDict, yLabelDict

######################################################################
def StartProgressBar(maxValue):
    ''' 
    def StartProgressBar(maxValue):
    Simple module to create and initialise a progress bar. The argument "maxvalue" refers to the 
    total number of tasks to be completed. This must be defined at the start of the progress bar.
    '''
    import progressbar

    widgets = [progressbar.FormatLabel(''), ' ', progressbar.Percentage(), ' ', progressbar.Bar('+'), ' ', progressbar.RotatingMarker()]
    pBar = progressbar.ProgressBar(widgets=widgets, maxval=maxValue)

    if pBar.start_time is None:
        pBar.start()

    return pBar

######################################################################
def printPSet(bPrintPset, folderName):
    '''
    def printPSet():
    Simple module that prints the parameters set in running the analysis
    '''
    if bPrintPset:
        from ROOT import gROOT
        gDirectory = gROOT.GetGlobal("gDirectory")
        named = gDirectory.Get("%s/parameterSet" % (folderName))
        raw_input("*** Press \"ENTER\" key to continue: ")
        print named.GetTitle()
        raw_input("*** Press \"ENTER\" key to continue: ")
    else:
        return
