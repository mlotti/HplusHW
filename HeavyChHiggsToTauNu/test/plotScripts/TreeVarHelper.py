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

#######################################################################################################
### Define the tree Variables: HIG-12-037 #HIG-11-019
#######################################################################################################
JetCollection   = "selJetsInclTau" #"jets" "allIdentifiedJets"
print "*** NOTE! The jet-collection used is: \"%s\"" % (JetCollection)

### Tau-jet 
TauPt       = "tau_p4.Pt()"
TauEta      = "abs(tau_p4.Eta())"
TauIso      = "tau_id_byMediumCombinedIsolationDeltaBetaCorr" #"tau_id_byTightIsolation"
Rtau        = "tau_leadPFChargedHadrCand_p4.P() / tau_p4.P()"
TauEleDisc  = "tau_id_againstElectronMVA" #"tau_id_againstElectronMedium"
TauMuDisc   = "tau_id_againstMuonTight" #"tau_id_againstMuonTight"
TauIsFake   = "TauIsFake" #True if the selected tau is fake (MC only)
TauOneProng = "tau_signalPFChargedHadrCands_n";

### Isolated e/mu veto

### Jets
NJets       = "jets_p4@.size()"
JetsPt      = "Sum$(jets_p4.Pt()>=30)"
JetsEta     = "Sum$(abs(jets_p4.Eta())<=2.4)"
NFwdJets    = "Sum$(abs(jets_p4.Eta()) >= 1.5)" #TEC starts at eta>=1.0

### MET
Met = "met_p4.Et()"

### Btagging
Btag = "passedBTagging"

### DeltaPhi(tau,MET)
DeltaPhiTauMet = "TMath::ACos(( tau_p4.X()*met_p4.px() + tau_p4.Y()*met_p4.py())/( tau_p4.Et()*met_p4.Et() ))*(180/TMath::Pi())"

### mT(tau,MET) 
Mt = "TMath::Sqrt(2*tau_p4.Et()*met_p4.Et()*( 1.0 - ( tau_p4.X()*met_p4.px() + tau_p4.Y()*met_p4.py())/( tau_p4.Et()*met_p4.Et() )))"

### Event Shape Variables
Sphericity    = "sphericity"
Aplanarity    = "aplanarity"
Planarity     = "planarity"
Circularity   = "circularity"
AlphaT        = "alphaT"
Cparameter    = "Cparameter"
Dparameter    = "Dparameter"
JetThrust     = "jetThrust"
MT_QOne       = "MomemntumTensor_QOne"
MT_QTwo       = "MomentumTensor_QTwo"
MT_QThree     = "MomentumTensor_QThree"
ST_QOne       = "SpherocityTensor_QOne"
ST_QTwo       = "SpherocityTensor_QTwo"
ST_QThree     = "SpherocityTensor_QThree"
Y             = "(TMath::Sqrt(3.0)/2.0)*(MomentumTensor_QTwo-MomentumTensor_QOne)"
SphericityAlt = "1.5*(MomentumTensor_QTwo+MomentumTensor_QOne)"
AplanarityAlt = "1.5*(MomentumTensor_QOne)"
PlanarityAlt  = "1.5*(shpericity-2*aplanarity)"
vDiJetMassesNoTau    = "vDiJetMassesNoTau"
vDiJetMassesNoTauSum = "Length$(vDiJetMassesNoTau)"

### Leading Jets 
LdgJet             = JetCollection + "_p4[0]"
NLdgJet            = JetCollection + "_p4[1]"
NNLdgJet           = JetCollection + "_p4[2]"
Ht                 = "Sum$(" + JetCollection + "_p4.Et())"
MHT                = "MHT_p4.Et()" 
MHT_SelJets        = "MHT_SelJets_p4.Et()" 
MHT_AllJets        = "MHT_AllJets_p4.Et()"
MHT_SelJetsInclTau = "TMath::Sqrt( pow(Sum$("+JetCollection+"_p4.Px()),2) + pow(Sum$("+JetCollection+"_p4.Py()),2) )" # I think this is correct (need to double-check)

### DeltaPhi(jet,MHT)
DeltaPhiMHTLdgJetInclTau   = "TMath::ACos(( MHT_p4.X()*"+JetCollection+"_p4[0].px() + MHT_p4.Y()*"+JetCollection+"_p4[0].py())/( MHT_p4.Et()*"+JetCollection+"_p4[0].Et() ))*(180/TMath::Pi())"
DeltaPhiMHTNLdgJetInclTau  = "TMath::ACos(( MHT_p4.X()*"+JetCollection+"_p4[1].px() + MHT_p4.Y()*"+JetCollection+"_p4[1].py())/( MHT_p4.Et()*"+JetCollection+"_p4[1].Et() ))*(180/TMath::Pi())"
DeltaPhiMHTNNLdgJetInclTau = "TMath::ACos(( MHT_p4.X()*"+JetCollection+"_p4[2].px() + MHT_p4.Y()*"+JetCollection+"_p4[2].py())/( MHT_p4.Et()*"+JetCollection+"_p4[2].Et() ))*(180/TMath::Pi())"

DeltaPhiMHTLdgJet   = "TMath::ACos(( MHT_p4.X()*jets_p4[0].px() + MHT_p4.Y()*jets_p4[0].py())/( MHT_p4.Et()*jets_p4[0].Et() ))*(180/TMath::Pi())"
DeltaPhiMHTNLdgJet  = "TMath::ACos(( MHT_p4.X()*jets_p4[1].px() + MHT_p4.Y()*jets_p4[1].py())/( MHT_p4.Et()*jets_p4[1].Et() ))*(180/TMath::Pi())"
DeltaPhiMHTNNLdgJet = "TMath::ACos(( MHT_p4.X()*jets_p4[2].px() + MHT_p4.Y()*jets_p4[2].py())/( MHT_p4.Et()*jets_p4[2].Et() ))*(180/TMath::Pi())"

### DeltaPhi(jet,MET)
### Using the JetCollection here make no sense as it is very likely that the angle tau-MET is the same as LdgJet-MET (tau is leading jet)
DeltaPhiMetLdgJetInclTau   = "TMath::ACos(( met_p4.px()*"+JetCollection+"_p4[0].px() + met_p4.py()*"+JetCollection+"_p4[0].py())/( met_p4.Et()*"+JetCollection+"_p4[0].Et() ))*(180/TMath::Pi())"
DeltaPhiMetNLdgJetInclTau  = "TMath::ACos(( met_p4.px()*"+JetCollection+"_p4[1].px() + met_p4.py()*"+JetCollection+"_p4[1].py())/( met_p4.Et()*"+JetCollection+"_p4[1].Et() ))*(180/TMath::Pi())"
DeltaPhiMetNNLdgJetInclTau = "TMath::ACos(( met_p4.px()*"+JetCollection+"_p4[2].px() + met_p4.py()*"+JetCollection+"_p4[2].py())/( met_p4.Et()*"+JetCollection+"_p4[2].Et() ))*(180/TMath::Pi())"

DeltaPhiMetLdgJet   = "TMath::ACos(( met_p4.px()*jets_p4[0].px() + met_p4.py()*jets_p4[0].py())/( met_p4.Et()*jets_p4[0].Et() ))*(180/TMath::Pi())"
DeltaPhiMetNLdgJet  = "TMath::ACos(( met_p4.px()*jets_p4[1].px() + met_p4.py()*jets_p4[1].py())/( met_p4.Et()*jets_p4[1].Et() ))*(180/TMath::Pi())"
DeltaPhiMetNNLdgJet = "TMath::ACos(( met_p4.px()*jets_p4[2].px() + met_p4.py()*jets_p4[2].py())/( met_p4.Et()*jets_p4[2].Et() ))*(180/TMath::Pi())"

### Other
LdgJetNLdgJetPtSum          = JetCollection+"_p4[0].Pt() + "+JetCollection+"_p4[1].Pt()"
DeltaHtTwoLdgJets           = Ht + "-" + LdgJetNLdgJetPtSum
DeltaPtLdgJetNLdgJet        = JetCollection+"_p4[0].Pt() - "+JetCollection+"_p4[1].Pt()"
DeltaPhiMHTMet              = "TMath::ACos(( met_p4.px()*MHT_p4.px() + met_p4.py()*MHT_p4.py())/( met_p4.Et()*MHT_p4.Et() ))*(180/TMath::Pi())"
DeltaPtLdgJetNLdgJetDivMet  = "TMath::Sqrt(pow("+JetCollection+"_p4[0].px() + "+JetCollection+"_p4[1].px(),2) + pow("+JetCollection+"_p4[0].py() + "+JetCollection+"_p4[1].py(),2))/( met_p4.Et() )"
DeltaPtLdgJetNLdgJetDivMHT  = "TMath::Sqrt(pow("+JetCollection+"_p4[0].px() + "+JetCollection+"_p4[1].px(),2) + pow("+JetCollection+"_p4[0].py() + "+JetCollection+"_p4[1].py(),2))/( "+MHT_SelJetsInclTau+")" #( MHT_SelJets_p4.Et() )"

### Non-Isolated Electrons (relIso > 0.2)
NonIsoEle_Size          = "nonIsoElectrons_p4@.size()"
NonIsoEle_RelIso        = "nonIsoElectrons_RelIso"
NonIsoEle_IPwrtBeamSpot = "nonIsoElectrons_IPwrtBeamSpot"
NonIsoEle_DistanceOSTrk = "nonIsoElectrons_DistanceOSTrk" 
NonIsoEle_EleMuDeltaR   = "nonIsoElectrons_ElectronMuonDeltaR"

### Non-Isolated Muons (relIso > 0.2)
NonIsoMu_Size           = "nonIsoMuons_p4@.size()"
NonIsoMu_RelIso         = "nonIsoMuons_RelIso"
NonIsoMu_IPZwrtPV       = "nonIsoMuons_IPZwrtPV"
NonIsoMu_IPTwrtBeamLine = "nonIsoMuons_IPTwrtBeamLine"
NonIsoMu_Bjet_DeltaR   = "nonIsoMuons_p4"
