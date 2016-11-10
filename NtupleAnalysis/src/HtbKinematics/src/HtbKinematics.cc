// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

// User
#include "Auxiliary/interface/Table.h"
#include "Auxiliary/interface/Tools.h"
#include "Tools/interface/MCTools.h"
#include "Tools/interface/DirectionalCut.h"
#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

// ROOT
#include "TDirectory.h"
#include "Math/VectorUtil.h"

struct PtComparator
{
  bool operator() (const math::XYZTLorentzVector p1, const math::XYZTLorentzVector p2) const { return ( p1.pt() > p2.pt() ); }
};


class HtbKinematics: public BaseSelector {
public:
  explicit HtbKinematics(const ParameterSet& config, const TH1* skimCounters);
  virtual ~HtbKinematics() {}

  /// Books histograms
  virtual void book(TDirectory *dir) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;
   
private:
  // Input parameters
  const double cfg_Verbose;
  const ParameterSet PSet_JetSelection;
  const double cfg_JetPtCut;
  const double cfg_JetEtaCut;
  const DirectionalCut<int> cfg_JetNumberCut;
  const ParameterSet PSet_ElectronSelection;
  const double cfg_ElectronPtCut;
  const double cfg_ElectronEtaCut;
  const DirectionalCut<int> cfg_ElectronNumberCut;
  const ParameterSet PSet_MuonSelection;
  const double cfg_MuonPtCut;
  const double cfg_MuonEtaCut;
  const DirectionalCut<int> cfg_MuonNumberCut;
  const ParameterSet PSet_HtSelection;
  const DirectionalCut<float> cfg_HtCut;
  const HistogramSettings cfg_PtBinSetting;
  const HistogramSettings cfg_EtaBinSetting;
  const HistogramSettings cfg_PhiBinSetting;
  const HistogramSettings cfg_MassBinSetting;
  const HistogramSettings cfg_DeltaEtaBinSetting;
  const HistogramSettings cfg_DeltaPhiBinSetting;
  const HistogramSettings cfg_DeltaRBinSetting;
  
  Tools auxTools;
  
  // Counters
  Count cAllEvents;  
  Count cHtb_HPlus;
  Count cHtb_TQuark;
  Count cHtb_BQuark;
  Count cHtb_tbW_BQuark;
  Count cHtb_tbW_WBoson;
  Count cHtb_tbW_Wqq_Quark;
  Count cHtb_tbW_Wqq_AntiQuark;
  Count cHtb_tbW_Wqq_Leptons;
  Count cgtt_TQuark;
  Count cgbb_BQuark;
  Count cgtt_tbW_Wqq_Quark;
  Count cgtt_tbW_Wqq_AntiQuark;
  Count cgtt_tbW_Wqq_Leptons;
  Count cgtt_tbW_WBoson;
  Count cgtt_tbW_BQuark;

  Count cSubNoPreselections;
  Count cSubPassedLeptonVeto;
  Count cSubPassedJetsCut;
  Count cSubPassedHtCut;
  
  // Event Variables
  WrappedTH1 *h_genMET_Et;
  WrappedTH1 *h_genMET_Phi;
  WrappedTH1 *h_genHT_GenParticles;
  WrappedTH1 *h_genHT_GenJets;  
  WrappedTH1 *h_SelGenJet_N_NoPreselections;
  WrappedTH1 *h_SelGenJet_N_AfterLeptonVeto;
  WrappedTH1 *h_SelGenJet_N_AfterLeptonVetoNJetsCut;
  WrappedTH1 *h_SelGenJet_N_AfterPreselections;  
  
  // GenParticles
  WrappedTH1 *h_gtt_TQuark_Pt;
  WrappedTH1 *h_gtt_tbW_WBoson_Pt;
  WrappedTH1 *h_gtt_tbW_BQuark_Pt;
  WrappedTH1 *h_gtt_tbW_Wqq_Quark_Pt;
  WrappedTH1 *h_gtt_tbW_Wqq_AntiQuark_Pt;
  WrappedTH1 *h_tbH_HPlus_Pt;
  WrappedTH1 *h_tbH_TQuark_Pt;
  WrappedTH1 *h_tbH_BQuark_Pt;
  WrappedTH1 *h_tbH_tbW_WBoson_Pt;
  WrappedTH1 *h_tbH_tbW_BQuark_Pt;
  WrappedTH1 *h_gbb_BQuark_Pt;
  WrappedTH1 *h_Htb_tbW_Wqq_Quark_Pt;
  WrappedTH1 *h_Htb_tbW_Wqq_AntiQuark_Pt;
  //
  WrappedTH1 *h_gtt_TQuark_Eta;
  WrappedTH1 *h_gtt_tbW_WBoson_Eta;
  WrappedTH1 *h_gtt_tbW_BQuark_Eta;
  WrappedTH1 *h_gtt_tbW_Wqq_Quark_Eta;
  WrappedTH1 *h_gtt_tbW_Wqq_AntiQuark_Eta;  
  WrappedTH1 *h_tbH_HPlus_Eta;
  WrappedTH1 *h_tbH_TQuark_Eta;
  WrappedTH1 *h_tbH_BQuark_Eta;
  WrappedTH1 *h_tbH_tbW_WBoson_Eta;
  WrappedTH1 *h_tbH_tbW_BQuark_Eta;
  WrappedTH1 *h_gbb_BQuark_Eta;
  WrappedTH1 *h_Htb_tbW_Wqq_Quark_Eta;
  WrappedTH1 *h_Htb_tbW_Wqq_AntiQuark_Eta;
  //
  WrappedTH1 *h_gtt_TQuark_Rap;
  WrappedTH1 *h_gtt_tbW_WBoson_Rap;
  WrappedTH1 *h_gtt_tbW_BQuark_Rap;
  WrappedTH1 *h_gtt_tbW_Wqq_Quark_Rap;
  WrappedTH1 *h_gtt_tbW_Wqq_AntiQuark_Rap;  
  WrappedTH1 *h_tbH_HPlus_Rap;
  WrappedTH1 *h_tbH_TQuark_Rap;
  WrappedTH1 *h_tbH_BQuark_Rap;
  WrappedTH1 *h_tbH_tbW_WBoson_Rap;
  WrappedTH1 *h_tbH_tbW_BQuark_Rap;
  WrappedTH1 *h_gbb_BQuark_Rap;
  WrappedTH1 *h_Htb_tbW_Wqq_Quark_Rap;
  WrappedTH1 *h_Htb_tbW_Wqq_AntiQuark_Rap;
  //  
  WrappedTH1 *h_Htb_TQuark_Htb_BQuark_dR;
  WrappedTH1 *h_Htb_TQuark_gtt_TQuark_dR;
  WrappedTH1 *h_Htb_TQuark_gbb_BQuark_dR;
  //
  WrappedTH1 *h_Htb_TQuark_Htb_BQuark_dEta;
  WrappedTH1 *h_Htb_TQuark_gtt_TQuark_dEta;
  WrappedTH1 *h_Htb_TQuark_gbb_BQuark_dEta;
  //
  WrappedTH1 *h_Htb_TQuark_Htb_BQuark_dPhi;
  WrappedTH1 *h_Htb_TQuark_gtt_TQuark_dPhi;
  WrappedTH1 *h_Htb_TQuark_gbb_BQuark_dPhi;
  //  
  WrappedTH1 *h_Htb_TQuark_Htb_BQuark_dRap;
  WrappedTH1 *h_Htb_TQuark_gtt_TQuark_dRap;
  WrappedTH1 *h_Htb_TQuark_gbb_BQuark_dRap;
  //  
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_BQuark_dR;
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_Wqq_Quark_dR;
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dR;
  WrappedTH1 *h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dR;
  WrappedTH1 *h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dR;
  WrappedTH1 *h_gtt_TQuark_gbb_BQuark_dR;
  WrappedTH1 *h_gtt_TQuark_gtt_tbW_BQuark_dR;
  WrappedTH1 *h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dR;
  WrappedTH1 *h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dR;
  //
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_BQuark_dEta;
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_Wqq_Quark_dEta;
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dEta;
  WrappedTH1 *h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dEta;
  WrappedTH1 *h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dEta;
  WrappedTH1 *h_gtt_TQuark_gbb_BQuark_dEta;
  WrappedTH1 *h_gtt_TQuark_gtt_tbW_BQuark_dEta;
  WrappedTH1 *h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dEta;
  WrappedTH1 *h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dEta;
  //
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_BQuark_dPhi;
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_Wqq_Quark_dPhi;
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dPhi;
  WrappedTH1 *h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dPhi;
  WrappedTH1 *h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dPhi;
  WrappedTH1 *h_gtt_TQuark_gbb_BQuark_dPhi;
  WrappedTH1 *h_gtt_TQuark_gtt_tbW_BQuark_dPhi;
  WrappedTH1 *h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dPhi;
  WrappedTH1 *h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dPhi;
  //  
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_BQuark_dRap;
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_Wqq_Quark_dRap;
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dRap;
  WrappedTH1 *h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dRap;
  WrappedTH1 *h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dRap;
  WrappedTH1 *h_gtt_TQuark_gbb_BQuark_dRap;
  WrappedTH1 *h_gtt_TQuark_gtt_tbW_BQuark_dRap;
  WrappedTH1 *h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dRap;
  WrappedTH1 *h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dRap;

  // GenParticles: BQuarks
  WrappedTH1 *h_BQuark1_Pt;
  WrappedTH1 *h_BQuark2_Pt;
  WrappedTH1 *h_BQuark3_Pt;
  WrappedTH1 *h_BQuark4_Pt;
  //
  WrappedTH1 *h_BQuark1_Eta;
  WrappedTH1 *h_BQuark2_Eta;
  WrappedTH1 *h_BQuark3_Eta;
  WrappedTH1 *h_BQuark4_Eta;
  // GenParticles: BQuarks pair closest together
  WrappedTH1 *h_BQuarkPair_dRMin_pT;
  WrappedTH1 *h_BQuarkPair_dRMin_dEta;
  WrappedTH1 *h_BQuarkPair_dRMin_dPhi;
  WrappedTH1 *h_BQuarkPair_dRMin_dR;
  WrappedTH1 *h_BQuarkPair_dRMin_Mass;
  WrappedTH2 *h_BQuarkPair_dRMin_Eta1_Vs_Eta2;
  WrappedTH2 *h_BQuarkPair_dRMin_Phi1_Vs_Phi2;
  WrappedTH2 *h_BQuarkPair_dRMin_Pt1_Vs_Pt2;
  WrappedTH2 *h_BQuarkPair_dRMin_dEta_Vs_dPhi;
  WrappedTH1 *h_BQuarkPair_dRMin_jet1_dR;
  WrappedTH1 *h_BQuarkPair_dRMin_jet1_dEta;
  WrappedTH1 *h_BQuarkPair_dRMin_jet1_dPhi;
  WrappedTH1 *h_BQuarkPair_dRMin_jet2_dR;
  WrappedTH1 *h_BQuarkPair_dRMin_jet2_dEta;
  WrappedTH1 *h_BQuarkPair_dRMin_jet2_dPhi;

  // GenParticles: bqq trijet system (H+)
  WrappedTH1 *h_Htb_tbW_bqq_Pt;
  WrappedTH1 *h_Htb_tbW_bqq_Rap;
  WrappedTH1 *h_Htb_tbW_bqq_Mass;
  WrappedTH1 *h_Htb_tbW_bqq_dRMax_dR;
  WrappedTH1 *h_Htb_tbW_bqq_dRMax_dRap;
  WrappedTH1 *h_Htb_tbW_bqq_dRMax_dPhi;
  WrappedTH2 *h_Htb_tbW_bqq_dRMax_dRap_Vs_dPhi;

  // GenParticles: bqq trijet system (associated top)
  WrappedTH1 *h_gtt_tbW_bqq_Pt;
  WrappedTH1 *h_gtt_tbW_bqq_Rap;
  WrappedTH1 *h_gtt_tbW_bqq_Mass;
  WrappedTH1 *h_gtt_tbW_bqq_dRMax_dR;
  WrappedTH1 *h_gtt_tbW_bqq_dRMax_dRap;
  WrappedTH1 *h_gtt_tbW_bqq_dRMax_dPhi;
  WrappedTH2 *h_gtt_tbW_bqq_dRMax_dRap_Vs_dPhi;

  // GenJets
  WrappedTH1 *h_GenJet1_Pt;
  WrappedTH1 *h_GenJet2_Pt;
  WrappedTH1 *h_GenJet3_Pt;
  WrappedTH1 *h_GenJet4_Pt;
  WrappedTH1 *h_GenJet5_Pt;
  WrappedTH1 *h_GenJet6_Pt;
  //
  WrappedTH1 *h_GenJet1_Eta;
  WrappedTH1 *h_GenJet2_Eta;
  WrappedTH1 *h_GenJet3_Eta;
  WrappedTH1 *h_GenJet4_Eta;
  WrappedTH1 *h_GenJet5_Eta;
  WrappedTH1 *h_GenJet6_Eta;

  // tt system
  WrappedTH1 *h_tt_Pt;
  WrappedTH1 *h_tt_Eta;
  WrappedTH1 *h_tt_Rap; 
  WrappedTH1 *h_tt_Mass;

  // GenJets: Dijet with largest mass
  WrappedTH1 *h_MaxDiJetMass_Pt;
  WrappedTH1 *h_MaxDiJetMass_Eta;
  WrappedTH1 *h_MaxDiJetMass_Rap; 
  WrappedTH1 *h_MaxDiJetMass_Mass;
  WrappedTH1 *h_MaxDiJetMass_dR;
  WrappedTH1 *h_MaxDiJetMass_dRrap;
  WrappedTH1 *h_MaxDiJetMass_dEta;
  WrappedTH1 *h_MaxDiJetMass_dPhi;
  WrappedTH1 *h_MaxDiJetMass_dRap;
  WrappedTH2 *h_MaxDiJetMass_dEta_Vs_dPhi;
  WrappedTH2 *h_MaxDiJetMass_dRap_Vs_dPhi;  

  // Correlations 
  WrappedTH2 *h_BQuark1_BQuark2_dEta_Vs_dPhi;
  WrappedTH2 *h_BQuark1_BQuark3_dEta_Vs_dPhi;
  WrappedTH2 *h_BQuark1_BQuark4_dEta_Vs_dPhi;
  WrappedTH2 *h_BQuark2_BQuark3_dEta_Vs_dPhi;
  WrappedTH2 *h_BQuark2_BQuark4_dEta_Vs_dPhi;
  WrappedTH2 *h_BQuark3_BQuark4_dEta_Vs_dPhi;

  WrappedTH2 *h_Jet1Jet2_dEta_Vs_Jet3Jet4_dEta;
  WrappedTH2 *h_Jet1Jet2_dPhi_Vs_Jet3Jet4_dPhi;  
  WrappedTH2 *h_Jet1Jet2_dEta_Vs_Jet1Jet2_Mass;
  WrappedTH2 *h_Jet3Jet4_dEta_Vs_Jet3Jet4_Mass;

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(HtbKinematics);

HtbKinematics::HtbKinematics(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    cfg_Verbose(config.getParameter<bool>("verbose")),
    PSet_JetSelection(config.getParameter<ParameterSet>("JetSelection")),
    cfg_JetPtCut(config.getParameter<float>("JetSelection.jetPtCut")),
    cfg_JetEtaCut(config.getParameter<float>("JetSelection.jetEtaCut")),
    cfg_JetNumberCut(config, "JetSelection.numberOfJetsCut"),
    PSet_ElectronSelection(config.getParameter<ParameterSet>("ElectronSelection")),
    cfg_ElectronPtCut(config.getParameter<float>("ElectronSelection.electronPtCut")),  
    cfg_ElectronEtaCut(config.getParameter<float>("ElectronSelection.electronEtaCut")),
    cfg_ElectronNumberCut(config, "ElectronSelection.electronNCut"),
    PSet_MuonSelection(config.getParameter<ParameterSet>("MuonSelection")),
    cfg_MuonPtCut(config.getParameter<float>("MuonSelection.muonPtCut")),
    cfg_MuonEtaCut(config.getParameter<float>("MuonSelection.muonEtaCut")),
    cfg_MuonNumberCut(config, "MuonSelection.muonNCut"),
    PSet_HtSelection(config.getParameter<ParameterSet>("HtSelection")),
    cfg_HtCut(config, "HtSelection.HtCut"),
    cfg_PtBinSetting(config.getParameter<ParameterSet>("CommonPlots.ptBins")),
    cfg_EtaBinSetting(config.getParameter<ParameterSet>("CommonPlots.etaBins")),
    cfg_PhiBinSetting(config.getParameter<ParameterSet>("CommonPlots.phiBins")),
    cfg_MassBinSetting(config.getParameter<ParameterSet>("CommonPlots.invmassBins")),
    cfg_DeltaEtaBinSetting(config.getParameter<ParameterSet>("CommonPlots.deltaEtaBins")),
    cfg_DeltaPhiBinSetting(config.getParameter<ParameterSet>("CommonPlots.deltaPhiBins")),
    cfg_DeltaRBinSetting(config.getParameter<ParameterSet>("CommonPlots.deltaRBins")),
    cAllEvents(fEventCounter.addCounter("All events")),
    cHtb_HPlus(fEventCounter.addSubCounter("Branching", "H+")),
    cHtb_TQuark(fEventCounter.addSubCounter("Branching", "H+->tb, t")),
    cHtb_BQuark(fEventCounter.addSubCounter("Branching", "H+->tb, b")),
    cHtb_tbW_BQuark(fEventCounter.addSubCounter("Branching", "H+->tb, t->bW, b")),
    cHtb_tbW_WBoson(fEventCounter.addSubCounter("Branching", "H+->tb, t->bW, W+")),
    cHtb_tbW_Wqq_Quark(fEventCounter.addSubCounter("Branching", "H+->tb, t->bW, W->qq, q")),
    cHtb_tbW_Wqq_AntiQuark(fEventCounter.addSubCounter("Branching", "H+->tb, t->bW, W->qq, qbar")),
    cHtb_tbW_Wqq_Leptons(fEventCounter.addSubCounter("Branching", "H+->tb, t->bW, W->l v")),
    cgtt_TQuark(fEventCounter.addSubCounter("Branching", "g->tt, t")),
    cgbb_BQuark(fEventCounter.addSubCounter("Branching", "g->bb, b")),
    cgtt_tbW_Wqq_Quark(fEventCounter.addSubCounter("Branching", "g->tt, t->bW, W->qq, q")),
    cgtt_tbW_Wqq_AntiQuark(fEventCounter.addSubCounter("Branching", "g->tt, t->bW, W->qq, qbar")),
    cgtt_tbW_Wqq_Leptons(fEventCounter.addSubCounter("Branching", "g->tt, t->bW, W->l v")),
    cgtt_tbW_WBoson(fEventCounter.addSubCounter("Branching", "g->tt, t->bW, W")),
    cgtt_tbW_BQuark(fEventCounter.addSubCounter("Branching", "g->tt, t->bW, b")), 
    cSubNoPreselections(fEventCounter.addSubCounter("Preselections", "All Events")),
    cSubPassedLeptonVeto(fEventCounter.addSubCounter("Preselections", "Lepton Veto")),
    cSubPassedJetsCut(fEventCounter.addSubCounter("Preselections", "Jets Cut")),
    cSubPassedHtCut(fEventCounter.addSubCounter("Preselections","HT Cut"))
{ }

void HtbKinematics::book(TDirectory *dir) {

  Table cuts("Variable | Jets | Electron | Muon | HT", "Text"); //LaTeX or Text
  cuts.AddRowColumn(0, "Pt (GeV/c)");
  cuts.AddRowColumn(1, "Eta");
  cuts.AddRowColumn(2, "Cut Direction");
  cuts.AddRowColumn(3, "Cut Value");
  //  
  cuts.AddRowColumn(0, auxTools.ToString(cfg_JetPtCut) );
  cuts.AddRowColumn(0, auxTools.ToString(cfg_ElectronPtCut) );
  cuts.AddRowColumn(0, auxTools.ToString(cfg_MuonPtCut) );
  cuts.AddRowColumn(0, "-");
  //
  cuts.AddRowColumn(1, auxTools.ToString(cfg_JetEtaCut) );
  cuts.AddRowColumn(1, auxTools.ToString(cfg_ElectronEtaCut) );
  cuts.AddRowColumn(1, auxTools.ToString(cfg_MuonEtaCut) );
  cuts.AddRowColumn(1, "-");
  //
  cuts.AddRowColumn(2, PSet_JetSelection.getParameter<string>("numberOfJetsCutDirection") );
  cuts.AddRowColumn(2, PSet_ElectronSelection.getParameter<string>("electronNCutDirection") );
  cuts.AddRowColumn(2, PSet_MuonSelection.getParameter<string>("muonNCutDirection") );
  cuts.AddRowColumn(2, PSet_HtSelection.getParameter<string>("HtCutDirection") );
  //
  cuts.AddRowColumn(3, auxTools.ToString(PSet_JetSelection.getParameter<int>("numberOfJetsCutValue")) );
  cuts.AddRowColumn(3, auxTools.ToString(PSet_ElectronSelection.getParameter<int>("electronNCutValue")) );
  cuts.AddRowColumn(3, auxTools.ToString(PSet_MuonSelection.getParameter<int>("muonNCutValue")) );
  cuts.AddRowColumn(3, PSet_HtSelection.getParameter<string>("HtCutValue") );
  //
  std::cout << "\n" << std::endl;
  cuts.Print();

  
  // Fixed binning
  const int nBinsPt   = cfg_PtBinSetting.bins();
  const double minPt  = cfg_PtBinSetting.min();
  const double maxPt  = cfg_PtBinSetting.max();

  const int nBinsEta  = cfg_EtaBinSetting.bins();
  const double minEta = cfg_EtaBinSetting.min();
  const double maxEta = cfg_EtaBinSetting.max();

  const int nBinsRap  = cfg_EtaBinSetting.bins();
  const double minRap = cfg_EtaBinSetting.min();
  const double maxRap = cfg_EtaBinSetting.max();

  const int nBinsPhi  = cfg_PhiBinSetting.bins();
  const double minPhi = cfg_PhiBinSetting.min();
  const double maxPhi = cfg_PhiBinSetting.max();

  const int nBinsM  = cfg_MassBinSetting.bins();
  const double minM = cfg_MassBinSetting.min();
  const double maxM = cfg_MassBinSetting.max();
  
  const int nBinsdEta  = cfg_DeltaEtaBinSetting.bins();
  const double mindEta = cfg_DeltaEtaBinSetting.min();
  const double maxdEta = cfg_DeltaEtaBinSetting.max();

  const int nBinsdRap  = cfg_DeltaEtaBinSetting.bins();
  const double mindRap = cfg_DeltaEtaBinSetting.min();
  const double maxdRap = cfg_DeltaEtaBinSetting.max();

  const int nBinsdPhi  = cfg_DeltaPhiBinSetting.bins();
  const double mindPhi = cfg_DeltaPhiBinSetting.min();
  const double maxdPhi = cfg_DeltaPhiBinSetting.max();

  const int nBinsdR  = cfg_DeltaRBinSetting.bins();
  const double mindR = cfg_DeltaRBinSetting.min();
  const double maxdR = cfg_DeltaRBinSetting.max();

    
  // Event Variables
  h_genMET_Et         =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genMET_Et"          , ";Gen E_{T}^{miss} (GeV)"       , 60,  0.0,   +300.0);
  h_genMET_Phi        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "genMET_Phi"         , ";Gen E_{T}^{miss} #phi (rads)" , nBinsPhi, minPhi, maxPhi);
  h_genHT_GenParticles=  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genHT_GenParticles" , ";GenP H_{T} (GeV)"             ,  75,  0.0, +1500.0);
  h_genHT_GenJets     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genHT_GenJets"      , ";GenJ H_{T} (GeV)"             ,  75,  0.0, +1500.0);  

  // GenParticles  
  h_gtt_TQuark_Pt            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_TQuark_Pt"           , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_gtt_tbW_WBoson_Pt        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_WBoson_Pt"       , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_gtt_tbW_BQuark_Pt        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_BQuark_Pt"       , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_gtt_tbW_Wqq_Quark_Pt     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_Wqq_Quark_Pt"    , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_gtt_tbW_Wqq_AntiQuark_Pt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_Wqq_AntiQuark_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_tbH_HPlus_Pt             =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_HPlus_Pt"            , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_tbH_TQuark_Pt            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_TQuark_Pt"           , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_tbH_BQuark_Pt            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_BQuark_Pt"           , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_tbH_tbW_WBoson_Pt        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_tbW_WBoson_Pt"       , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_tbH_tbW_BQuark_Pt        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_tbW_BQuark_Pt"       , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_gbb_BQuark_Pt            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gbb_BQuark_Pt"           , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_Htb_tbW_Wqq_Quark_Pt     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_Wqq_Quark_Pt"    , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_Htb_tbW_Wqq_AntiQuark_Pt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_Wqq_AntiQuark_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  //
  h_gtt_TQuark_Eta            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_TQuark_Eta"           , ";#eta", nBinsEta, minEta, maxEta);
  h_gtt_tbW_WBoson_Eta        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_WBoson_Eta"       , ";#eta", nBinsEta, minEta, maxEta);
  h_gtt_tbW_BQuark_Eta        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_BQuark_Eta"       , ";#eta", nBinsEta, minEta, maxEta);
  h_gtt_tbW_Wqq_Quark_Eta     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_Wqq_Quark_Eta"    , ";#eta", nBinsEta, minEta, maxEta);
  h_gtt_tbW_Wqq_AntiQuark_Eta =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_Wqq_AntiQuark_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_tbH_HPlus_Eta             =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_HPlus_Eta"            , ";#eta", nBinsEta, minEta, maxEta);
  h_tbH_TQuark_Eta            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_TQuark_Eta"           , ";#eta", nBinsEta, minEta, maxEta);
  h_tbH_BQuark_Eta            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_BQuark_Eta"           , ";#eta", nBinsEta, minEta, maxEta);
  h_tbH_tbW_WBoson_Eta        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_tbW_WBoson_Eta"       , ";#eta", nBinsEta, minEta, maxEta);
  h_tbH_tbW_BQuark_Eta        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_tbW_BQuark_Eta"       , ";#eta", nBinsEta, minEta, maxEta);
  h_gbb_BQuark_Eta            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gbb_BQuark_Eta"           , ";#eta", nBinsEta, minEta, maxEta);
  h_Htb_tbW_Wqq_Quark_Eta     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_Wqq_Quark_Eta"    , ";#eta", nBinsEta, minEta, maxEta);
  h_Htb_tbW_Wqq_AntiQuark_Eta =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_Wqq_AntiQuark_Eta", ";#eta", nBinsEta, minEta, maxEta);
  //
  h_gtt_TQuark_Rap            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_TQuark_Rap"           , ";#omega", nBinsRap, minRap, maxRap);
  h_gtt_tbW_WBoson_Rap        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_WBoson_Rap"       , ";#omega", nBinsEta, minRap, maxRap);
  h_gtt_tbW_BQuark_Rap        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_BQuark_Rap"       , ";#omega", nBinsEta, minRap, maxRap);
  h_gtt_tbW_Wqq_Quark_Rap     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_Wqq_Quark_Rap"    , ";#omega", nBinsEta, minRap, maxRap);
  h_gtt_tbW_Wqq_AntiQuark_Rap =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_Wqq_AntiQuark_Rap", ";#omega", nBinsEta, minRap, maxRap);
  h_tbH_HPlus_Rap             =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_HPlus_Rap"            , ";#omega", nBinsEta, minRap, maxRap);
  h_tbH_TQuark_Rap            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_TQuark_Rap"           , ";#omega", nBinsEta, minRap, maxRap);
  h_tbH_BQuark_Rap            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_BQuark_Rap"           , ";#omega", nBinsEta, minRap, maxRap);
  h_tbH_tbW_WBoson_Rap        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_tbW_WBoson_Rap"       , ";#omega", nBinsEta, minRap, maxRap);
  h_tbH_tbW_BQuark_Rap        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_tbW_BQuark_Rap"       , ";#omega", nBinsEta, minRap, maxRap);
  h_gbb_BQuark_Rap            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gbb_BQuark_Rap"           , ";#omega", nBinsEta, minRap, maxRap);
  h_Htb_tbW_Wqq_Quark_Rap     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_Wqq_Quark_Rap"    , ";#omega", nBinsEta, minRap, maxRap);
  h_Htb_tbW_Wqq_AntiQuark_Rap =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_Wqq_AntiQuark_Rap", ";#omega", nBinsEta, minRap, maxRap);
  // 
  h_Htb_TQuark_Htb_BQuark_dR                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_TQuark_Htb_BQuark_dR"               , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_Htb_TQuark_gtt_TQuark_dR                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_TQuark_gtt_TQuark_dR"               , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_Htb_TQuark_gbb_BQuark_dR                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_TQuark_gbb_BQuark_dR"               , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_Htb_BQuark_Htb_tbW_BQuark_dR            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_BQuark_Htb_tbW_BQuark_dR"           , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_Htb_BQuark_Htb_tbW_Wqq_Quark_dR         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_BQuark_Htb_tbW_Wqq_Quark_dR"        , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dR     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dR"    , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dR     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dR"    , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dR", ";#DeltaR", nBinsdR, mindR, maxdR);
  h_gtt_TQuark_gbb_BQuark_dR                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_TQuark_gbb_BQuark_dR"               , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_gtt_TQuark_gtt_tbW_BQuark_dR            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_TQuark_gtt_tbW_BQuark_dR"           , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dR     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dR"    , ";#DeltaR", nBinsdR, mindR, maxdR);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dR", ";#DeltaR", nBinsdR, mindR, maxdR);
  //
  h_Htb_TQuark_Htb_BQuark_dEta                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_TQuark_Htb_BQuark_dEta"               , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_Htb_TQuark_gtt_TQuark_dEta                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_TQuark_gtt_TQuark_dEta"               , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_Htb_TQuark_gbb_BQuark_dEta                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_TQuark_gbb_BQuark_dEta"               , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_Htb_BQuark_Htb_tbW_BQuark_dEta            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_BQuark_Htb_tbW_BQuark_dEta"           , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_Htb_BQuark_Htb_tbW_Wqq_Quark_dEta         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_BQuark_Htb_tbW_Wqq_Quark_dEta"        , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dEta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dEta"    , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dEta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dEta"    , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dEta", ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_gtt_TQuark_gbb_BQuark_dEta                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_TQuark_gbb_BQuark_dEta"               , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_gtt_TQuark_gtt_tbW_BQuark_dEta            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_TQuark_gtt_tbW_BQuark_dEta"           , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dEta     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dEta"    , ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dEta", ";#Delta#eta", nBinsdEta, mindEta, maxdEta);
  //
  h_Htb_TQuark_Htb_BQuark_dPhi               = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_TQuark_Htb_BQuark_dPhi"               ,";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_Htb_TQuark_gtt_TQuark_dPhi               = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_TQuark_gtt_TQuark_dPhi"               ,";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_Htb_TQuark_gbb_BQuark_dPhi               = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_TQuark_gbb_BQuark_dPhi"               ,";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_Htb_BQuark_Htb_tbW_BQuark_dPhi           = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_BQuark_Htb_tbW_BQuark_dPhi"           ,";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_Htb_BQuark_Htb_tbW_Wqq_Quark_dPhi        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_BQuark_Htb_tbW_Wqq_Quark_dPhi"        ,";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dPhi    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dPhi"    ,";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dPhi    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dPhi"    ,";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dPhi= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dPhi",";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_gtt_TQuark_gbb_BQuark_dPhi               = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_TQuark_gbb_BQuark_dPhi"               ,";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_gtt_TQuark_gtt_tbW_BQuark_dPhi           = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_TQuark_gtt_tbW_BQuark_dPhi"           ,";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dPhi    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dPhi"    ,";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dPhi= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dPhi",";#Delta#phi (rads)", nBinsdPhi, mindPhi, maxdPhi);
  //
  h_Htb_TQuark_Htb_BQuark_dRap                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_TQuark_Htb_BQuark_dRap"               , ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  h_Htb_TQuark_gtt_TQuark_dRap                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_TQuark_gtt_TQuark_dRap"               , ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  h_Htb_TQuark_gbb_BQuark_dRap                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_TQuark_gbb_BQuark_dRap"               , ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  h_Htb_BQuark_Htb_tbW_BQuark_dRap            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_BQuark_Htb_tbW_BQuark_dRap"           , ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  h_Htb_BQuark_Htb_tbW_Wqq_Quark_dRap         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_BQuark_Htb_tbW_Wqq_Quark_dRap"        , ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dRap     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dRap"    , ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dRap     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dRap"    , ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dRap = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dRap", ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  h_gtt_TQuark_gbb_BQuark_dRap                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_TQuark_gbb_BQuark_dRap"               , ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  h_gtt_TQuark_gtt_tbW_BQuark_dRap            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_TQuark_gtt_tbW_BQuark_dRap"           , ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dRap     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dRap"    , ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dRap = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dRap", ";#Delta#omega", nBinsdRap, mindRap, maxdRap);
  
  // GenParticles: B-quarks
  h_BQuark1_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark1_Pt", ";p_{T} (GeV/c)" , nBinsPt, minPt, maxPt);
  h_BQuark2_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark2_Pt", ";p_{T} (GeV/c)" , nBinsPt, minPt, maxPt);
  h_BQuark3_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark3_Pt", ";p_{T} (GeV/c)" , nBinsPt, minPt, maxPt);
  h_BQuark4_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark4_Pt", ";p_{T} (GeV/c)" , nBinsPt, minPt, maxPt);

  h_BQuark1_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark1_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_BQuark2_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark2_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_BQuark3_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark3_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_BQuark4_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark4_Eta", ";#eta", nBinsEta, minEta, maxEta);

  // GenParticles: BQuarks pair closest together
  h_BQuarkPair_dRMin_pT   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_pT"  , ";p_{T} (GeV/c)"     ,  nBinsPt, minPt, maxPt);
  h_BQuarkPair_dRMin_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_dEta", ";#Delta#eta"        ,  nBinsdEta, mindEta, maxdEta);
  h_BQuarkPair_dRMin_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_dPhi", ";#Delta#phi (rads)" ,  nBinsdPhi, mindPhi, maxdPhi);
  h_BQuarkPair_dRMin_dR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_dR"  , ";#DeltaR"           ,  nBinsdR, mindR, maxdR);
  h_BQuarkPair_dRMin_Mass = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_Mass", ";M (GeV/c^{2})"     ,  nBinsM, minM, maxM);
  //
  h_BQuarkPair_dRMin_Eta1_Vs_Eta2 = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_Eta1_Vs_Eta2", ";#eta;#eta", nBinsEta, minEta, maxEta, nBinsEta, minEta, maxEta);
  h_BQuarkPair_dRMin_Phi1_Vs_Phi2 = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_Phi1_Vs_Phi2", ";#phi;#phi", nBinsPhi, minPhi, maxPhi, nBinsPhi, minPhi, maxPhi);
  h_BQuarkPair_dRMin_Pt1_Vs_Pt2   = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_Pt1_Vs_Pt2"  , ";p_{T} (GeV/c); p_{T} (GeV/c)", nBinsPt, minPt, maxPt, nBinsPt, minPt, maxPt);
  h_BQuarkPair_dRMin_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);
  //
  h_BQuarkPair_dRMin_jet1_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_jet1_dEta", ";#Delta#eta"        ,  nBinsdEta, mindEta, maxdEta);
  h_BQuarkPair_dRMin_jet1_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_jet1_dPhi", ";#Delta#phi (rads)" ,  nBinsdPhi, mindPhi, maxdPhi);
  h_BQuarkPair_dRMin_jet1_dR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_jet1_dR"  , ";#DeltaR"           ,  nBinsdR, mindR, maxdR);
  h_BQuarkPair_dRMin_jet2_dEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_jet2_dEta", ";#Delta#eta"        ,  nBinsdEta, mindEta, maxdEta);
  h_BQuarkPair_dRMin_jet2_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_jet2_dPhi", ";#Delta#phi (rads)" ,  nBinsdPhi, mindPhi, maxdPhi);
  h_BQuarkPair_dRMin_jet2_dR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuarkPair_dRMin_jet2_dR"  , ";#DeltaR"           ,  nBinsdR, mindR, maxdR);

  // GenParticles: bqq trijet system (H+)
  h_Htb_tbW_bqq_Pt         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_bqq_Pt"   , ";p_{T} (GeV/c)"    ,  nBinsPt, minPt, maxPt);
  h_Htb_tbW_bqq_Rap        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_bqq_Rap"  , ";#omega"           ,  nBinsRap, minRap, maxRap);
  h_Htb_tbW_bqq_Mass       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_bqq_Mass" , ";M (GeV/c^{2})"    ,  nBinsM, minM, maxM);
  //
  h_Htb_tbW_bqq_dRMax_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_bqq_dRMax_dPhi" , ";#Delta#phi (rads)",  nBinsdPhi, mindPhi, maxdPhi);
  h_Htb_tbW_bqq_dRMax_dRap = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_bqq_dRMax_dRap" , ";#Delta#omega"     ,  nBinsdRap, mindRap, maxdRap);
  h_Htb_tbW_bqq_dRMax_dR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_bqq_dRMax_dR"   , ";#DeltaR"          ,  nBinsdR, mindR, maxdR);
  h_Htb_tbW_bqq_dRMax_dRap_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "Htb_tbW_bqq_dRMax_dRap_Vs_dPhi", ";#Delta#omega;#Delta#phi (rads)", nBinsdRap, mindRap, maxdRap, nBinsdPhi, mindPhi, maxdPhi);

  // GenParticles: bqq trijet system (associated top)
  h_gtt_tbW_bqq_Pt         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_bqq_Pt"   , ";p_{T} (GeV/c^{2})",  nBinsPt, minPt, maxPt);
  h_gtt_tbW_bqq_Rap        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_bqq_Rap"  , ";#omega"           ,  nBinsRap, minRap, maxRap);
  h_gtt_tbW_bqq_Mass       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_bqq_Mass" , ";M (GeV/c^{2})"    ,  nBinsM, minM, maxM);
  //
  h_gtt_tbW_bqq_dRMax_dPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_bqq_dRMax_dPhi", ";#Delta#phi (rads)",  nBinsdPhi, mindPhi, maxdPhi);
  h_gtt_tbW_bqq_dRMax_dRap = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_bqq_dRMax_dRap", ";#Delta#omega"     ,  nBinsdRap, mindRap, maxdRap);
  h_gtt_tbW_bqq_dRMax_dR   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_bqq_dRMax_dR"  , ";#DeltaR"          ,  nBinsdR, mindR, maxdR);  
  h_gtt_tbW_bqq_dRMax_dRap_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "gtt_tbW_bqq_dRMax_dRap_Vs_dPhi", ";#Delta#omega;#Delta#phi (rads)", nBinsdRap, mindRap, maxdRap, nBinsdPhi, mindPhi, maxdPhi);
  
  // Leading Jets
  h_Jet1Jet2_dEta_Vs_Jet3Jet4_dEta = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "Jet1Jet2_dEta_Vs_Jet3Jet4_dEta", ";#Delta#eta(j_{1},j_{2});#Delta#eta(j_{3},j_{4})", nBinsdEta, mindEta, maxdEta, nBinsdEta, mindEta, maxdEta);

  h_Jet1Jet2_dPhi_Vs_Jet3Jet4_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "Jet1Jet2_dPhi_Vs_Jet3Jet4_dPhi", ";#Delta#phi(j_{1},j_{2}) (rads);#Delta#phi(j_{3},j_{4}) (rads)", nBinsdPhi, mindPhi, maxdPhi, nBinsdPhi, mindPhi, maxdPhi);

  h_Jet1Jet2_dEta_Vs_Jet1Jet2_Mass = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "Jet1Jet2_dEta_Vs_Jet1Jet2_Mass", ";#Delta#eta(j_{1},j_{2});M(j_{1},j_{2}) (GeV/c^{2})", nBinsdEta, mindEta, maxdEta, nBinsM, minM, maxM);

  h_Jet3Jet4_dEta_Vs_Jet3Jet4_Mass = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "Jet3Jet4_dEta_Vs_Jet3Jet4_Mass", ";#Delta#eta(j_{3},j_{4});M(j_{4},j_{4}) (GeV/c^{2})", nBinsdEta, mindEta, maxdEta, nBinsM, minM, maxM);
  
  // GenJets
  h_SelGenJet_N_NoPreselections         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelGenJet_N_NoPreselections"        , ";N (selected jets)" , 16, -0.5, +15.5);
  h_SelGenJet_N_AfterLeptonVeto         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelGenJet_N_AfterLeptonVeto"        , ";N (selected jets)" , 16, -0.5, +15.5);
  h_SelGenJet_N_AfterLeptonVetoNJetsCut = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelGenJet_N_AfterLeptonVetoNJetsCut", ";N (selected jets)" , 16, -0.5, +15.5);
  h_SelGenJet_N_AfterPreselections      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelGenJet_N_AfterPreselections"     , ";N (selected jets)" , 16, -0.5, +15.5);
  //
  h_GenJet1_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet1_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_GenJet2_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet2_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_GenJet3_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet3_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_GenJet4_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet4_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_GenJet5_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet5_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_GenJet6_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet6_Pt", ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  //
  h_GenJet1_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet1_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_GenJet2_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet2_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_GenJet3_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet3_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_GenJet4_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet4_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_GenJet5_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet5_Eta", ";#eta", nBinsEta, minEta, maxEta);
  h_GenJet6_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet6_Eta", ";#eta", nBinsEta, minEta, maxEta);

  // tt system
  h_tt_Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tt_Pt"   , ";p_{T} (GeV/c)"    , nBinsPt, minPt, maxPt);
  h_tt_Eta   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tt_Eta"  , ";#eta"             , nBinsEta, minEta, maxEta);
  h_tt_Rap   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tt_Rap"  , ";#omega"           , nBinsRap, minRap, maxRap);
  h_tt_Mass  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tt_Mass" , ";M (GeV/c^{2})"    , 50,  0.0, +1000.0);  

  // GenJets: Dijet with largest mass
  h_MaxDiJetMass_Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MaxDiJetMass_Pt"   , ";p_{T} (GeV/c)"    , nBinsPt, minPt, maxPt);
  h_MaxDiJetMass_Eta   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MaxDiJetMass_Eta"  , ";#eta"             , nBinsEta, minEta, maxEta);
  h_MaxDiJetMass_Rap   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MaxDiJetMass_Rap"  , ";#omega"           , nBinsRap, minRap, maxRap);
  h_MaxDiJetMass_Mass  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MaxDiJetMass_Mass" , ";M (GeV/c^{2})"    , 50,  0.0, +1000.0);  
  h_MaxDiJetMass_dEta  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MaxDiJetMass_dEta" , ";#Delta#eta"       , nBinsdEta, mindEta, maxdEta);
  h_MaxDiJetMass_dRap  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MaxDiJetMass_dRap" , ";#Delta#omega"     , nBinsdRap, mindRap, maxdRap);
  h_MaxDiJetMass_dPhi  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MaxDiJetMass_dPhi" , ";#Delta#phi"       , nBinsdPhi, mindPhi, maxdPhi);  
  h_MaxDiJetMass_dR    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MaxDiJetMass_dR"   , ";#DeltaR"          , nBinsdR, mindR, maxdR);  
  h_MaxDiJetMass_dRrap = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MaxDiJetMass_dRrap", ";#DeltaR_{#omega}" , nBinsdR, mindR, maxdR);  
  h_MaxDiJetMass_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "MaxDiJetMass_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)"  , nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);
  h_MaxDiJetMass_dRap_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "MaxDiJetMass_dRap_Vs_dPhi", ";#Delta#omega;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);

  // Correlations
  h_BQuark1_BQuark2_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "BQuark1_BQuark2_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);
  h_BQuark1_BQuark3_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "BQuark1_BQuark3_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);
  h_BQuark1_BQuark4_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "BQuark1_BQuark4_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);
  h_BQuark2_BQuark3_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "BQuark2_BQuark3_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);
  h_BQuark2_BQuark4_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "BQuark2_BQuark4_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);
  h_BQuark3_BQuark4_dEta_Vs_dPhi = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "BQuark3_BQuark4_dEta_Vs_dPhi", ";#Delta#eta;#Delta#phi (rads)", nBinsdEta, mindEta, maxdEta, nBinsdPhi, mindPhi, maxdPhi);

  return;
}

void HtbKinematics::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}


void HtbKinematics::process(Long64_t entry) {

  if ( !fEvent.isMC() ) return;
  
  // Create MCools object
  MCTools mcTools(fEvent);
  
  // Increment Counter
  cAllEvents.increment();
  

  ///////////////////////////////////////////////////////////////////////////
  // GenJets Calculations
  /////////////////////////////////////////////////////////////////////////// 
  std::vector<math::XYZTLorentzVector> selJets_p4;
  int nSelJets   = 0;
  double genJ_HT = 0.0;

  // For-loop: GenJets
  for(GenJet j: fEvent.genjets()) {

    math::XYZTLorentzVector genJ_p4;
    genJ_p4 = j.p4();
    double genJ_pt     = j.pt();
    double genJ_eta    = j.eta();

    // Apply selection cuts
    if (genJ_pt < cfg_JetPtCut) continue;
    if (std::abs(genJ_eta) > cfg_JetEtaCut) continue;
    
    // Do calculations
    nSelJets++;
    selJets_p4.push_back( genJ_p4 );
    genJ_HT += genJ_pt;
  }
 

  ///////////////////////////////////////////////////////////////////////////
  // GenParticles Calculations
  ///////////////////////////////////////////////////////////////////////////
  int nWToENu  = 0;
  int nWToMuNu = 0;

  // Indices
  int Htb_HPlus_index             = -1.0;
  int Htb_TQuark_index            = -1.0;
  int Htb_BQuark_index            = -1.0;
  int Htb_tbW_BQuark_index        = -1.0;
  int Htb_tbW_WBoson_index        = -1.0;
  int Htb_tbW_Wqq_Quark_index     = -1.0;
  int Htb_tbW_Wqq_AntiQuark_index = -1.0;
  int gtt_TQuark_index            = -1.0;
  int gbb_BQuark_index            = -1.0;
  int gtt_tbW_Wqq_Quark_index     = -1.0;
  int gtt_tbW_Wqq_AntiQuark_index = -1.0;
  int gtt_tbW_WBoson_index        = -1.0;
  int gtt_tbW_BQuark_index        = -1.0; 

  // 4-momenta
  math::XYZTLorentzVector Htb_HPlus_p4;
  math::XYZTLorentzVector Htb_TQuark_p4;
  math::XYZTLorentzVector Htb_BQuark_p4;
  math::XYZTLorentzVector Htb_tbW_BQuark_p4;
  math::XYZTLorentzVector Htb_tbW_WBoson_p4;
  math::XYZTLorentzVector Htb_tbW_Wqq_Quark_p4;
  math::XYZTLorentzVector Htb_tbW_Wqq_AntiQuark_p4;
  math::XYZTLorentzVector gtt_TQuark_p4;
  math::XYZTLorentzVector gbb_BQuark_p4;
  math::XYZTLorentzVector gtt_tbW_Wqq_Quark_p4;
  math::XYZTLorentzVector gtt_tbW_Wqq_AntiQuark_p4;
  math::XYZTLorentzVector gtt_tbW_WBoson_p4;
  math::XYZTLorentzVector gtt_tbW_BQuark_p4;


  // Define the table
  Table table("Evt | Index | PdgId | Status | Charge | Pt | Eta | Phi | E | Vertex (mm) | D0 (mm) | Lxy (mm) | Mom | Daughters", "Text"); //LaTeX or Text

  int row = 0;
  // For-loop: GenParticles
  for (auto& p: fEvent.genparticles().getGenParticles()) {

    // Consider only status=22 (intermediate) or status=23 (outgoing) particles
    // if ( (p.status() != 22) && (p.status() != 23) ) continue;


    // Particle properties
    short genP_index     = p.index();
    int genP_pdgId       = p.pdgId();
    int genP_status      = p.status();
    double genP_pt       = p.pt();
    double genP_eta      = p.eta();
    double genP_phi      = p.phi();
    double genP_energy   = p.e();
    int genP_charge      = p.charge();
    // math::XYZTLorentzVector genP_p4;
    // genP_p4 = p.p4();    

    // Associated genParticles
    std::vector<genParticle> genP_daughters;
    for (unsigned int i=0; i < p.daughters().size(); i++) genP_daughters.push_back(fEvent.genparticles().getGenParticles()[p.daughters().at(i)]);
    std::vector<genParticle> genP_mothers;
    for (unsigned int i=0; i < p.mothers().size(); i++) genP_mothers.push_back(fEvent.genparticles().getGenParticles()[p.mothers().at(i)]);
    std::vector<genParticle> genP_grandMothers;
    std::vector<unsigned int> genMoms_index;
    std::vector<unsigned int> genMoms_pdgId;
    std::vector<unsigned int> genDaus_index;
    std::vector<unsigned int> genDaus_pdgId;

    // Removed real vertex from Tree (to save size)
    ROOT::Math::XYZPoint vtxIdeal;
    vtxIdeal.SetXYZ(0, 0, 0);
    double genP_vtxX = vtxIdeal.X(); // p.vtxX()*10; // in mm
    double genP_vtxY = vtxIdeal.Y(); // p.vtxY()*10; // in mm
    double genP_vtxZ = vtxIdeal.Z(); // p.vtxZ()*10; // in mm

    // Daughter, Mom and Grand-mom properties    
    genParticle m;
    genParticle g;
    genParticle d;

    if (genP_daughters.size() > 0) d = genP_daughters.at(0);
    if (p.mothers().size() > 0)
      {
	m = genP_mothers.at(0); // fixme
	for (unsigned int i=0; i < m.mothers().size(); i++) genP_grandMothers.push_back(fEvent.genparticles().getGenParticles()[m.mothers().at(i)]);
	if (m.mothers().size() > 0) g = genP_grandMothers.at(0); // fixme
      } 

    // For convenience, save the pdgIds in vectors
    for (unsigned int i=0; i < genP_mothers.size(); i++) 
      {
	if (genP_mothers.at(i).index() < 0) continue;
	genMoms_index.push_back(genP_mothers.at(i).index());
	genMoms_pdgId.push_back(genP_mothers.at(i).pdgId());
      }
    for (unsigned int i=0; i < genP_daughters.size(); i++) 
      {
	if (genP_daughters.at(i).index() < 0) continue;
	genDaus_index.push_back(genP_daughters.at(i).index());
	genDaus_pdgId.push_back(genP_daughters.at(i).pdgId());
      }

    // Properties that need to be calculated
    double genP_Lxy = 0.0; 
    double genP_d0  = 0.0;
    if (genP_daughters.size() > 0 && genP_mothers.size() > 0)
      {
	genP_d0  = mcTools.GetD0 (p, m, d, vtxIdeal); // in mm
	genP_Lxy = mcTools.GetLxy(p, m, d, vtxIdeal); // in mm
      }
   
    
    // Print genParticle properties or decay tree ?
    if (0)
      {
    	mcTools.PrintGenParticle(p);
     	mcTools.PrintGenDaughters(p);
       }


    // Add table rows
    if (cfg_Verbose)
      {
	table.AddRowColumn(row, auxTools.ToString(entry)           );
	table.AddRowColumn(row, auxTools.ToString(genP_index)      );
	table.AddRowColumn(row, auxTools.ToString(genP_pdgId)      );
	table.AddRowColumn(row, auxTools.ToString(genP_status)     );
	table.AddRowColumn(row, auxTools.ToString(genP_charge)     );
	table.AddRowColumn(row, auxTools.ToString(genP_pt , 3)     );
	table.AddRowColumn(row, auxTools.ToString(genP_eta, 4)     );
	table.AddRowColumn(row, auxTools.ToString(genP_phi, 3)     );
	table.AddRowColumn(row, auxTools.ToString(genP_energy, 3)  );
	table.AddRowColumn(row, "(" + auxTools.ToString(genP_vtxX, 3) + ", " + auxTools.ToString(genP_vtxY, 3)  + ", " + auxTools.ToString(genP_vtxZ, 3) + ")" );
	table.AddRowColumn(row, auxTools.ToString(genP_d0 , 3)     );
	table.AddRowColumn(row, auxTools.ToString(genP_Lxy, 3)     );	
	if (genMoms_index.size() < 6)
	  {
	    table.AddRowColumn(row, auxTools.ConvertIntVectorToString(genMoms_index) );
	    // table.AddRowColumn(row, auxTools.ConvertIntVectorToString(genMoms_pdgId) );
	  }
        else table.AddRowColumn(row, ".. Too many .." );
	if (genDaus_index.size() < 6)
          {
	    table.AddRowColumn(row, auxTools.ConvertIntVectorToString(genDaus_index) );
	    // table.AddRowColumn(row, auxTools.ConvertIntVectorToString(genDaus_pdgId) );
          }
        else table.AddRowColumn(row, ".. Too many .." );
	row++;
      }
	       

    // Filtering
    // if (!p.isLastCopy()) continue;
    // if ( !mcTools.IsQuark(genP_pdgId) ) continue;
    // if (!p.isPrompt()) continue;
    // if (!p.isPromptDecayed()) continue;
    // if (!p.isPromptFinalState()) continue;
    // if (!p.isDecayedLeptonHadron()) continue;
    // if (!p.isTauDecayProduct()) continue;
    // if (!p.isPromptTauDecayProduct()) continue;
    // if (!p.isDirectTauDecayProduct()) continue;
    // if (!p.isDirectPromptTauDecayProduct()) continue;
    // if (!p.isDirectPromptTauDecayProductFinalState()) continue;
    // if (!p.isDirectHadronDecayProduct()) continue;
    // if (!p.isDirectHardProcessTauDecayProductFinalState()) continue;
    //// if (!p.isHardProcess()) continue;
    // if (!p.fromHardProcess()) continue;
    // if (!p.fromHardProcessDecayed()) continue;
    // if (!p.fromHardProcessFinalState()) continue;
    // if (!p.isHardProcessTauDecayProduct()) continue;
    // if (!p.isDirectHardProcessTauDecayProduct()) continue;
    // if (!p.fromHardProcessBeforeFSR()) continue;
    // if (!p.isFirstCopy()) continue;
    // if (!p.isLastCopyBeforeFSR()) continue;

    
    // Associated top (g->tt)
    if (genP_pdgId == -6)
      {
	if (!p.isLastCopy()) continue;
	       
	cgtt_TQuark.increment();
	gtt_TQuark_p4    = p.p4();
	gtt_TQuark_index = genP_index; 


	for (auto& d: genP_daughters) 
	  {
	    
	    if (d.pdgId() == -5)// g->tt, t->bW, b-quark
	      {
		cgtt_tbW_BQuark.increment();
		gtt_tbW_BQuark_p4 = p.p4();
		gtt_tbW_BQuark_index = genP_index;
	      }
	    else if (d.pdgId() == -24)// g->tt, t->bW, W-boson
	      {
		// NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!
		cgtt_tbW_WBoson.increment();
		gtt_tbW_WBoson_p4    = p.p4();
		gtt_tbW_WBoson_index = genP_index;
	      }
	    else throw hplus::Exception("Logic") << "HtbKinematics::process() Unexpected top-quark daughter.";

	  } // for (auto& d: genP_daughters)
      }// if (genP_pdgId == -6)
  

    // W- from Associated top (g->tt, t->bW)
    if (genP_pdgId == -24)
      {
	if (!p.isLastCopy()) continue;
	
	for (auto& d: genP_daughters) 
	  {
	    
	    if ( mcTools.IsQuark(d.pdgId() ) )// g->tt, t->bWH, t->bW, W->q qbar'
	      {
		if (d.pdgId() > 0)
		  {
		    // Quarks
		    cgtt_tbW_Wqq_Quark.increment();
		    gtt_tbW_Wqq_Quark_p4    = d.p4();
		    gtt_tbW_Wqq_Quark_index = d.index();
		  }	       
		else
		  {
		    // AntiQuarks
		    cgtt_tbW_Wqq_AntiQuark.increment();
		    gtt_tbW_Wqq_AntiQuark_p4    = d.p4();
		    gtt_tbW_Wqq_AntiQuark_index = d.index();
		  }
	      }	  
	    else if ( mcTools.IsLepton(d.pdgId() ) )// g->tt, t->bWH, t->bW, W->l v
	      {
		// NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!
		cgtt_tbW_Wqq_Leptons.increment();
		
		if ( std::abs(d.pdgId()) == 11)
		  {		      
		    if ( d.p4().pt() < cfg_ElectronPtCut) continue;
		    if ( std::abs(d.p4().eta()) > cfg_ElectronEtaCut) continue;
		    nWToENu++;
		  }
		else if ( std::abs(d.pdgId()) == 13)
		  {
		    if ( d.p4().pt() < cfg_MuonPtCut) continue;
		    if ( std::abs(d.p4().eta()) > cfg_MuonEtaCut) continue;
		    nWToMuNu++;
		  }		  
		else{}
	      }
	    else
	      {
		// throw hplus::Exception("Logic") << "HtbKinematics::process() W daughters whose origins are not accounted for. Need to rethink this.";
		std::cout << "*** HtbKinematics::process() W daughters whose origins are not accounted for. Need to rethink this." << std::endl;
	      }
	  }// for (auto& d: genP_daughters)
      }// if (genP_pdgId == -24)



    // H+
    if (genP_pdgId == 37)
      {
	if (!p.isLastCopy()) continue;

	cHtb_HPlus.increment();
	Htb_HPlus_p4 = p.p4();
	Htb_HPlus_index = genP_index;

	for (auto& d: genP_daughters) 
	  {

	    if ( d.pdgId() == 6)// H->tb, t
	      {
		
		cHtb_TQuark.increment();
		Htb_TQuark_p4 = p.p4();
		Htb_TQuark_index = genP_index;
	      }
	    else if ( d.pdgId() == -5)// H->tb, b
	      {
		cHtb_BQuark.increment();
		Htb_BQuark_p4 = p.p4();
		Htb_BQuark_index = genP_index;
	      }
	    else
	      {
		// throw hplus::Exception("Logic") << "HtbKinematics::process() B-quark whose origins are not accounted for. Need to rethink this.";
		std::cout << "*** HtbKinematics::process() H+ daughters whose origins are not accounted for. Need to rethink this." << std::endl;
	      }

	  }// for (auto& d: genP_daughters) 

      }// if (genP_pdgId == 37)
	    

    // Top (H->tb)
    if (genP_pdgId == 6)
      {

	if (!p.isLastCopy()) continue;	
	// mcTools.PrintGenParticle(p);
        // mcTools.PrintGenDaughters(p);

	for (auto& d: genP_daughters) 
	  {

	    if ( d.pdgId() == +24)// H->tb, t->bW+, W+
	      {
		// mcTools.PrintGenParticle(d);		

		// NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
		cHtb_tbW_WBoson.increment();
		Htb_tbW_WBoson_p4    = p.p4();
		Htb_tbW_WBoson_index = genP_index;
	      }
	    else if ( d.pdgId() == +5)// H->tb, t->bW+, b
	      {
		// mcTools.PrintGenParticle(d);
		
		// NOTE: t->Wb dominant, but t->Ws and t->Wd also possible! Also t->Zc and t->Zu
		cHtb_tbW_BQuark.increment();
		Htb_tbW_BQuark_p4 = p.p4();
		Htb_tbW_BQuark_index = genP_index;
	      }
	    else
	      {
		// NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!

		// std::cout << "*** HtbKinematics::process() t (H->tb) daughters whose origins are not accounted for. Need to rethink this." << std::endl;
		// mcTools.PrintGenParticle(d);
		// mcTools.PrintGenDaughters(d);
	      }
	  }// for (auto& d: genP_daughters) 
      }// if (genP_pdgId == 6)


    // W+ (H->tb, t->bW+, W+)
    if (genP_pdgId == +24)
      {

	if (!p.isLastCopy()) continue;		
	// mcTools.PrintGenParticle(p);
        // mcTools.PrintGenDaughters(p);

	for (auto& d: genP_daughters) 
	  {

	    if ( mcTools.IsQuark(d.pdgId()) ) // H+->tb, t->bW+, W+->qq
	      {	
		if (d.pdgId() > 0)
		  {
		    // Quarks
		    cHtb_tbW_Wqq_Quark.increment();
		    Htb_tbW_Wqq_Quark_p4 = d.p4();
		    Htb_tbW_Wqq_Quark_index = d.index();
		  }
		else
		  {
		    // Anti-Quarks
		    cHtb_tbW_Wqq_AntiQuark.increment();
		    Htb_tbW_Wqq_AntiQuark_p4 = d.p4();
		    Htb_tbW_Wqq_AntiQuark_index = d.index();
		  }
	      }
	    else if ( mcTools.IsLepton(d.pdgId() ) ) // H+->tb, t->bW+, W+->l v
	      {
		// NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!
		cHtb_tbW_Wqq_Leptons.increment();
		
		if ( std::abs(d.pdgId()) == 11)
		  {		      
		    if ( d.p4().pt() < cfg_ElectronPtCut) continue;
		    if ( std::abs(d.p4().eta()) > cfg_ElectronEtaCut) continue;
		    nWToENu++;
		  }
		else if ( std::abs(d.pdgId()) == 13)
		  {
		    if ( d.p4().pt() < cfg_MuonPtCut) continue;
		    if ( std::abs(d.p4().eta()) > cfg_MuonEtaCut) continue;
		    nWToMuNu++;
		  }		  
		else{}		  
	      }
	    else
	      {
		// throw hplus::Exception("Logic") << "HtbKinematics::process() W daughters whose origins are not accounted for. Need to rethink this.";
		std::cout << "*** HtbKinematics::process() W+ (H->tb) daughters whose origins are not accounted for. Need to rethink this." << std::endl;
	      }
	    
	  }// for (auto& d: genP_daughters) 

      }// if (genP_pdgId == +24)


    // Flavour-excited b-quark (g->bb)
    if (genP_pdgId == 5)
      {

	// Consider only status=23 (outgoing) particles
	if ( p.status() != 23 )  continue;

	// Comes from proton or gluon
	bool fromGluon  = std::find(genMoms_pdgId.begin(), genMoms_pdgId.end(), 21) != genMoms_pdgId.end();
	bool fromProton = std::find(genMoms_pdgId.begin(), genMoms_pdgId.end(), 2212) != genMoms_pdgId.end();
	if (fromGluon==false && fromProton==false) continue;
	
	// mcTools.PrintGenParticle(p);
        // mcTools.PrintGenDaughters(p);
	
	cgbb_BQuark.increment();
	gbb_BQuark_p4 = p.p4();
	gbb_BQuark_index = genP_index;

      }// if (genP_pdgId == 5)

	    
  }// for-loop: genParticles

  // std::cout << "PSet_JetSelection.getParameter<float>(jetPtCut) = " << PSet_JetSelection.getParameter<float>("jetPtCut") << std::endl;
  
  
  ///////////////////////////////////////////////////////////////////////////
  // BEFORE Preselection Cuts
  ///////////////////////////////////////////////////////////////////////////
  cSubNoPreselections.increment();
  h_SelGenJet_N_NoPreselections->Fill(nSelJets);
 
    
  ///////////////////////////////////////////////////////////////////////////
  // Preselection Cuts (python/parameters/hplus2tbAnalysis.py)
  ///////////////////////////////////////////////////////////////////////////
  // Lepton Veto
  if ( !cfg_ElectronNumberCut.passedCut(nWToENu) ) return;
  if ( !cfg_MuonNumberCut.passedCut(nWToMuNu) ) return;
  cSubPassedLeptonVeto.increment();
  // Fill Histos
  h_SelGenJet_N_AfterLeptonVeto->Fill(nSelJets);
  
  // Jet Selection
  if ( !cfg_JetNumberCut.passedCut(selJets_p4.size()) ) return;  
  // if ( selJets_p4.at(0).pt() < 70 ) return;
  // if ( selJets_p4.at(1).pt() < 50 ) return;
  // if ( selJets_p4.at(2).pt() < 40 ) return;
  cSubPassedJetsCut.increment();
  // Fill Histos
  h_SelGenJet_N_AfterLeptonVetoNJetsCut->Fill(nSelJets);
    
  // HT Selection
  if ( !cfg_HtCut.passedCut(genJ_HT) ) return;
  cSubPassedHtCut.increment();
  

  ///////////////////////////////////////////////////////////////////////////
  // AFTER Preselection Cuts
  ///////////////////////////////////////////////////////////////////////////
  h_SelGenJet_N_AfterPreselections->Fill(nSelJets);

  // Event Variables
  double genP_HT = (Htb_BQuark_p4.pt() + Htb_tbW_BQuark_p4.pt() + Htb_tbW_Wqq_Quark_p4.pt() + Htb_tbW_Wqq_AntiQuark_p4.pt()
		    + gtt_tbW_Wqq_Quark_p4.pt() + gtt_tbW_Wqq_AntiQuark_p4.pt() + gtt_tbW_BQuark_p4.pt()
		    + gbb_BQuark_p4.pt());
  
  std::vector<math::XYZTLorentzVector> v_dijet_p4;
  std::vector<double> v_dijet_masses;
  std::vector<double> v_dijet_dR;
  std::vector<double> v_dijet_dRrap;
  std::vector<double> v_dijet_dEta;
  std::vector<double> v_dijet_dPhi;
  std::vector<double> v_dijet_dRap;
  

  math::XYZTLorentzVector tt_p4 = Htb_TQuark_p4 + gtt_TQuark_p4;
  h_tt_Mass ->Fill( tt_p4.mass() );
  h_tt_Pt   ->Fill( tt_p4.pt()  );
  h_tt_Eta  ->Fill( tt_p4.eta() );
  h_tt_Rap  ->Fill( mcTools.GetRapidity(tt_p4) );

  double maxDijetMass_mass;
  math::XYZTLorentzVector maxDijetMass_p4;
  int maxDijetMass_pos;
  double maxDijetMass_dR;
  double maxDijetMass_dRrap;
  double maxDijetMass_dEta;
  double maxDijetMass_dPhi;
  double maxDijetMass_dRap;
  double maxDijetMass_rapidity;
  
  int iJet = 0;
  if (selJets_p4.size() > 1) {
    // For-loop: All selected jets 
    for (size_t i=0; i < selJets_p4.size(); i++)
      {
	iJet++;
	double genJ_Pt  = selJets_p4.at(i).pt();
	double genJ_Eta = selJets_p4.at(i).eta();
	// double genJ_Rap = mcTools.GetRapidity(selJets_p4.at(i));
	
	if (iJet==1)
	  {
	    
	    h_GenJet1_Pt -> Fill( genJ_Pt  );
	    h_GenJet1_Eta-> Fill( genJ_Eta );

	  }
	else if (iJet==2)
	  {
	    
	    h_GenJet2_Pt -> Fill( genJ_Pt  );
	    h_GenJet2_Eta-> Fill( genJ_Eta );

	  }
	else if (iJet==3)
	  {
	    
	    h_GenJet3_Pt -> Fill( genJ_Pt  );
	    h_GenJet3_Eta-> Fill( genJ_Eta );

	  }
	else if (iJet==4)
	  {

	    h_GenJet4_Pt -> Fill( genJ_Pt  );
	    h_GenJet4_Eta-> Fill( genJ_Eta );

	  }
	else if (iJet==5)
	  {

	    h_GenJet5_Pt -> Fill( genJ_Pt  );
	    h_GenJet5_Eta-> Fill( genJ_Eta );

	  }
	else if (iJet==6)
	  {

	    h_GenJet6_Pt -> Fill( genJ_Pt  );
	    h_GenJet6_Eta-> Fill( genJ_Eta );

	  }
	else{}
	
	// For-loop: All selected jets (nested)
	for (size_t j=i+1; j < selJets_p4.size(); j++)
	  {
	    math::XYZTLorentzVector p4_i = selJets_p4.at(i);
	    math::XYZTLorentzVector p4_j = selJets_p4.at(j);
	    math::XYZTLorentzVector p4   = p4_i + p4_j;
	    double rap_i = mcTools.GetRapidity(p4_i);
	    double rap_j = mcTools.GetRapidity(p4_j);
	    double dR    = ROOT::Math::VectorUtil::DeltaR(p4_i, p4_j);
	    double dRap  = std::fabs(rap_i - rap_j);
	    double dEta  = std::fabs(p4_i.eta() - p4_j.eta());
	    double dPhi  = std::fabs(ROOT::Math::VectorUtil::DeltaPhi(p4_i, p4_j));
	    
	    v_dijet_p4.push_back( p4 );
	    v_dijet_masses.push_back( p4.mass() );
	    v_dijet_dR.push_back( dR );
	    v_dijet_dRrap.push_back( sqrt( pow(dRap, 2) + pow(dPhi, 2) ) ); 
	    v_dijet_dEta.push_back( dEta ); 
	    v_dijet_dRap.push_back( dRap );
	    v_dijet_dPhi.push_back( dPhi );

	  }
      }

    // MaxDiJet: DiJet combination with largest mass
    maxDijetMass_pos      = std::max_element(v_dijet_masses.begin(), v_dijet_masses.end()) - v_dijet_masses.begin();
    maxDijetMass_mass     = v_dijet_masses.at(maxDijetMass_pos);
    maxDijetMass_p4       = v_dijet_p4.at(maxDijetMass_pos);
    maxDijetMass_dR       = v_dijet_dR.at(maxDijetMass_pos);
    maxDijetMass_dRrap    = v_dijet_dRrap.at(maxDijetMass_pos);
    maxDijetMass_dEta     = v_dijet_dEta.at(maxDijetMass_pos);
    maxDijetMass_dPhi     = v_dijet_dPhi.at(maxDijetMass_pos);
    maxDijetMass_dRap     = v_dijet_dRap.at(maxDijetMass_pos);
    maxDijetMass_rapidity = mcTools.GetRapidity(maxDijetMass_p4);

  }// if (selJets_p4.size() > 1) {

  //  if (selJets_p4.size() > 3) {
    double jet1_Eta = selJets_p4.at(0).eta();
    double jet2_Eta = selJets_p4.at(1).eta();
    double jet3_Eta = selJets_p4.at(2).eta();
    double jet4_Eta = selJets_p4.at(3).eta();

    double jet1_Phi = selJets_p4.at(0).phi();
    double jet2_Phi = selJets_p4.at(1).phi();
    double jet3_Phi = selJets_p4.at(2).phi();
    double jet4_Phi = selJets_p4.at(3).phi();

    
    h_Jet1Jet2_dEta_Vs_Jet3Jet4_dEta ->Fill(std::fabs(jet1_Eta - jet2_Eta), std::fabs(jet3_Eta - jet4_Eta));
    h_Jet1Jet2_dPhi_Vs_Jet3Jet4_dPhi ->Fill(std::fabs(jet1_Phi - jet2_Phi), std::fabs(jet3_Phi - jet4_Phi));
    h_Jet1Jet2_dEta_Vs_Jet1Jet2_Mass ->Fill(std::fabs(jet1_Eta - jet2_Eta), (selJets_p4.at(0) + selJets_p4.at(1)).mass() );
    h_Jet3Jet4_dEta_Vs_Jet3Jet4_Mass ->Fill(std::fabs(jet3_Eta - jet4_Eta), (selJets_p4.at(2) + selJets_p4.at(3)).mass() );
    //  } alex
  
  // Event-based histograms
  h_genMET_Et  ->Fill(fEvent.genMET().et()); 
  h_genMET_Phi ->Fill(fEvent.genMET().Phi());

  
  // Trijet system (H+)
  math::XYZTLorentzVector Htb_tbW_bqq_p4 = Htb_tbW_BQuark_p4 + Htb_tbW_Wqq_Quark_p4 + Htb_tbW_Wqq_AntiQuark_p4;

  // Find max separation
  std::vector<math::XYZTLorentzVector> bqq_p4;
  bqq_p4.push_back(Htb_tbW_BQuark_p4);
  bqq_p4.push_back(Htb_tbW_Wqq_Quark_p4);
  bqq_p4.push_back(Htb_tbW_Wqq_AntiQuark_p4);
  double deltaRMax = -1.0;
  int deltaRMax_i  = -1;
  int deltaRMax_j  = -1;
  // For-loop: All p4 of bqq system
  for (size_t i = 0; i < bqq_p4.size(); i++)    
    {
      for (size_t j = i+1; j < bqq_p4.size(); j++)
	{
	  double deltaR = ROOT::Math::VectorUtil::DeltaR(bqq_p4.at(i), bqq_p4.at(j));
	  if (deltaR > deltaRMax)
	    {
	      deltaRMax   = deltaR;
	      deltaRMax_i = i;
	      deltaRMax_j = j;
	    }
	}
    } // For-loop: All p4 of bqq system

  // double bqq_dEta = std::fabs(bqq_p4.at(deltaRMax_i).eta() - bqq_p4.at(deltaRMax_j).eta());
  double bqq_dRap = std::fabs(mcTools.GetRapidity(bqq_p4.at(deltaRMax_i) ) - mcTools.GetRapidity(bqq_p4.at(deltaRMax_j) ) );
  double bqq_dPhi = std::fabs(ROOT::Math::VectorUtil::DeltaPhi(bqq_p4.at(deltaRMax_i), bqq_p4.at(deltaRMax_j)));
  // Fill Histos
  h_Htb_tbW_bqq_Pt->Fill( Htb_tbW_bqq_p4.pt());
  h_Htb_tbW_bqq_Rap->Fill( mcTools.GetRapidity(Htb_tbW_bqq_p4) );
  h_Htb_tbW_bqq_Mass->Fill( Htb_tbW_bqq_p4.mass() );
  h_Htb_tbW_bqq_dRMax_dR->Fill( deltaRMax );
  h_Htb_tbW_bqq_dRMax_dRap->Fill( bqq_dRap );
  h_Htb_tbW_bqq_dRMax_dPhi->Fill( bqq_dPhi );
  h_Htb_tbW_bqq_dRMax_dRap_Vs_dPhi->Fill( bqq_dRap, bqq_dPhi );

  // Trijet system (associated top)
  math::XYZTLorentzVector gtt_tbW_bqq_p4 = gtt_tbW_Wqq_Quark_p4 + gtt_tbW_Wqq_AntiQuark_p4 + gtt_tbW_BQuark_p4;

  // Fix max separation (again)
  bqq_p4.clear();
  bqq_p4.push_back(gtt_tbW_BQuark_p4);
  bqq_p4.push_back(gtt_tbW_Wqq_Quark_p4);
  bqq_p4.push_back(gtt_tbW_Wqq_AntiQuark_p4);
  deltaRMax    = -1.0;
  deltaRMax_i  = -1;
  deltaRMax_j  = -1;

  // For-loop: All p4 of bqq system
  for (size_t i = 0; i < bqq_p4.size(); i++)    
    {
      for (size_t j = i+1; j < bqq_p4.size(); j++)
	{
	  double deltaR = ROOT::Math::VectorUtil::DeltaR(bqq_p4.at(i), bqq_p4.at(j));
	  if (deltaR > deltaRMax)
	    {
	      deltaRMax   = deltaR;
	      deltaRMax_i = i;
	      deltaRMax_j = j;
	    }
	}
    } // For-loop: All p4 of bqq system

  // bqq_dEta = std::fabs(bqq_p4.at(deltaRMax_i).eta() - bqq_p4.at(deltaRMax_j).eta());
  bqq_dRap = std::fabs(mcTools.GetRapidity(bqq_p4.at(deltaRMax_i) ) - mcTools.GetRapidity(bqq_p4.at(deltaRMax_j) ) );
  bqq_dPhi = std::fabs(ROOT::Math::VectorUtil::DeltaPhi(bqq_p4.at(deltaRMax_i), bqq_p4.at(deltaRMax_j)));
  // Fill Histos
  h_gtt_tbW_bqq_Pt->Fill( gtt_tbW_bqq_p4.pt() );
  h_gtt_tbW_bqq_Rap->Fill( mcTools.GetRapidity(gtt_tbW_bqq_p4) );
  h_gtt_tbW_bqq_Mass->Fill( gtt_tbW_bqq_p4.mass() );
  h_gtt_tbW_bqq_dRMax_dR->Fill( deltaRMax );
  h_gtt_tbW_bqq_dRMax_dRap->Fill( bqq_dRap );
  h_gtt_tbW_bqq_dRMax_dPhi->Fill( bqq_dPhi );
  h_gtt_tbW_bqq_dRMax_dRap_Vs_dPhi ->Fill( bqq_dRap, bqq_dPhi );

  // MaxDiJet
  h_MaxDiJetMass_Mass ->Fill( maxDijetMass_mass     );
  h_MaxDiJetMass_Pt   ->Fill( maxDijetMass_p4.pt()  );
  h_MaxDiJetMass_Eta  ->Fill( maxDijetMass_p4.eta() );
  h_MaxDiJetMass_Rap  ->Fill( maxDijetMass_rapidity );
  h_MaxDiJetMass_dR   ->Fill( maxDijetMass_dR       );
  h_MaxDiJetMass_dRrap->Fill( maxDijetMass_dRrap    );
  h_MaxDiJetMass_dEta ->Fill( maxDijetMass_dEta     );
  h_MaxDiJetMass_dPhi ->Fill( maxDijetMass_dPhi     );
  h_MaxDiJetMass_dRap ->Fill( maxDijetMass_dRap     );
  h_MaxDiJetMass_dEta_Vs_dPhi->Fill( maxDijetMass_dEta, maxDijetMass_dPhi );
  h_MaxDiJetMass_dRap_Vs_dPhi->Fill( maxDijetMass_dRap, maxDijetMass_dPhi );
  
  // Calculate HT
  h_genHT_GenParticles->Fill(genP_HT);
  h_genHT_GenJets->Fill(genJ_HT);
  
  
  // Print the table with genP info
  if (cfg_Verbose) table.Print();
  
  // H+->tb, t->bW, b (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible! Also t->Zc and t->Zu)
  h_tbH_tbW_BQuark_Pt ->Fill( Htb_tbW_BQuark_p4.pt()  );
  h_tbH_tbW_BQuark_Eta->Fill( Htb_tbW_BQuark_p4.eta() );
  h_tbH_tbW_BQuark_Rap->Fill( mcTools.GetRapidity(Htb_tbW_BQuark_p4) );

  // H+->tb, b
  h_tbH_BQuark_Pt ->Fill( Htb_BQuark_p4.pt()  );
  h_tbH_BQuark_Eta->Fill( Htb_BQuark_p4.eta() );
  h_tbH_BQuark_Rap->Fill( mcTools.GetRapidity(Htb_BQuark_p4 ) );

  // g->bb, b (flavour-excited )	       
  h_gbb_BQuark_Pt ->Fill( gbb_BQuark_p4.pt()  );
  h_gbb_BQuark_Eta->Fill( gbb_BQuark_p4.eta() );
  h_gbb_BQuark_Rap->Fill( mcTools.GetRapidity(gbb_BQuark_p4) );

  // g->tt, t->bW, b (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
  h_gtt_tbW_BQuark_Pt ->Fill( gtt_tbW_BQuark_p4.pt()  ); 
  h_gtt_tbW_BQuark_Eta->Fill( gtt_tbW_BQuark_p4.eta() );
  h_gtt_tbW_BQuark_Rap->Fill( mcTools.GetRapidity(gtt_tbW_BQuark_p4) );
    
  // H+->tb (From HPlus decay)
  h_tbH_TQuark_Pt ->Fill( Htb_TQuark_p4.pt()) ;
  h_tbH_TQuark_Eta->Fill( Htb_TQuark_p4.eta() );
  h_tbH_TQuark_Rap->Fill( mcTools.GetRapidity(Htb_TQuark_p4) );

  // g->tt (Associated top)
  h_gtt_TQuark_Pt ->Fill( gtt_TQuark_p4.pt()  );
  h_gtt_TQuark_Eta->Fill( gtt_TQuark_p4.eta() );
  h_gtt_TQuark_Rap->Fill( mcTools.GetRapidity(gtt_TQuark_p4) );
  
  // tb->H+, H+
  h_tbH_HPlus_Pt ->Fill( Htb_HPlus_p4.pt()  );
  h_tbH_HPlus_Eta->Fill( Htb_HPlus_p4.eta() );
  h_tbH_HPlus_Rap->Fill( mcTools.GetRapidity(Htb_HPlus_p4) );
  
  // H+->tb, t->bW, W-boson (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
  h_tbH_tbW_WBoson_Pt ->Fill( Htb_tbW_WBoson_p4.pt()  );
  h_tbH_tbW_WBoson_Eta->Fill( Htb_tbW_WBoson_p4.eta() );
  h_tbH_tbW_WBoson_Rap->Fill( mcTools.GetRapidity(Htb_tbW_WBoson_p4) );

  // H+->tb, t->bW, W-boson, Quark
  h_Htb_tbW_Wqq_Quark_Pt ->Fill( Htb_tbW_Wqq_Quark_p4.pt()  );
  h_Htb_tbW_Wqq_Quark_Eta->Fill( Htb_tbW_Wqq_Quark_p4.eta() );
  h_Htb_tbW_Wqq_Quark_Rap->Fill( mcTools.GetRapidity(Htb_tbW_Wqq_Quark_p4) );

  // H+->tb, t->bW, W-boson, AntiQuark
  h_Htb_tbW_Wqq_AntiQuark_Pt ->Fill( Htb_tbW_Wqq_AntiQuark_p4.pt()  );
  h_Htb_tbW_Wqq_AntiQuark_Eta->Fill( Htb_tbW_Wqq_AntiQuark_p4.eta() );
  h_Htb_tbW_Wqq_AntiQuark_Rap->Fill( mcTools.GetRapidity(Htb_tbW_Wqq_AntiQuark_p4) );

  // g->tt, t->bW, W-boson (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
  h_gtt_tbW_WBoson_Pt ->Fill( gtt_tbW_WBoson_p4.pt()  );
  h_gtt_tbW_WBoson_Eta->Fill( gtt_tbW_WBoson_p4.eta() );
  h_gtt_tbW_WBoson_Rap->Fill( mcTools.GetRapidity(gtt_tbW_WBoson_p4) );

  // g->tt, t->bW, W->qq, Quark
  h_gtt_tbW_Wqq_Quark_Pt ->Fill( gtt_tbW_Wqq_Quark_p4.pt()  );
  h_gtt_tbW_Wqq_Quark_Eta->Fill( gtt_tbW_Wqq_Quark_p4.eta() );
  h_gtt_tbW_Wqq_Quark_Rap->Fill( mcTools.GetRapidity(gtt_tbW_Wqq_Quark_p4) );

  // g->tt, t->bW, W->qq, AntiQuark
  h_gtt_tbW_Wqq_AntiQuark_Pt ->Fill( gtt_tbW_Wqq_AntiQuark_p4.pt()  );
  h_gtt_tbW_Wqq_AntiQuark_Eta->Fill( gtt_tbW_Wqq_AntiQuark_p4.eta() );
  h_gtt_tbW_Wqq_AntiQuark_Rap->Fill( mcTools.GetRapidity(gtt_tbW_Wqq_AntiQuark_p4) );

 
  // H+->tb, t->bW, W->qq
  double dR_Htb_TQuark_Htb_BQuark                = ROOT::Math::VectorUtil::DeltaR( Htb_TQuark_p4, Htb_BQuark_p4           );
  double dR_Htb_TQuark_gtt_TQuark                = ROOT::Math::VectorUtil::DeltaR( Htb_TQuark_p4, gtt_TQuark_p4           );
  double dR_Htb_TQuark_gbb_BQuark                = ROOT::Math::VectorUtil::DeltaR( Htb_TQuark_p4, gbb_BQuark_p4           );
  double dR_Htb_BQuark_Htb_tbW_BQuark            = ROOT::Math::VectorUtil::DeltaR( Htb_BQuark_p4, Htb_tbW_BQuark_p4       );
  double dR_Htb_BQuark_Htb_tbW_Wqq_Quark         = ROOT::Math::VectorUtil::DeltaR( Htb_BQuark_p4, Htb_tbW_Wqq_Quark_p4    );
  double dR_Htb_BQuark_Htb_tbW_Wqq_AntiQuark     = ROOT::Math::VectorUtil::DeltaR( Htb_BQuark_p4, Htb_tbW_Wqq_AntiQuark_p4);
  double dR_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark     = ROOT::Math::VectorUtil::DeltaR( Htb_tbW_BQuark_p4, Htb_tbW_Wqq_Quark_p4);
  double dR_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark = ROOT::Math::VectorUtil::DeltaR( Htb_tbW_BQuark_p4, Htb_tbW_Wqq_AntiQuark_p4);

  double dEta_Htb_TQuark_Htb_BQuark                = std::fabs( Htb_TQuark_p4.eta() - Htb_BQuark_p4.eta()            );
  double dEta_Htb_TQuark_gtt_TQuark                = std::fabs( Htb_TQuark_p4.eta() - gtt_TQuark_p4.eta()            );
  double dEta_Htb_TQuark_gbb_BQuark                = std::fabs( Htb_TQuark_p4.eta() - gbb_BQuark_p4.eta()            );
  double dEta_Htb_BQuark_Htb_tbW_BQuark            = std::fabs( Htb_BQuark_p4.eta() - Htb_tbW_BQuark_p4.eta()        );
  double dEta_Htb_BQuark_Htb_tbW_Wqq_Quark         = std::fabs( Htb_BQuark_p4.eta() - Htb_tbW_Wqq_Quark_p4.eta()     );
  double dEta_Htb_BQuark_Htb_tbW_Wqq_AntiQuark     = std::fabs( Htb_BQuark_p4.eta() - Htb_tbW_Wqq_AntiQuark_p4.eta() );
  double dEta_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark     = std::fabs( Htb_tbW_BQuark_p4.eta() - Htb_tbW_Wqq_Quark_p4.eta() );
  double dEta_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark = std::fabs( Htb_tbW_BQuark_p4.eta() - Htb_tbW_Wqq_AntiQuark_p4.eta() );

  double dPhi_Htb_TQuark_Htb_BQuark                = std::fabs(ROOT::Math::VectorUtil::DeltaPhi( Htb_TQuark_p4, Htb_BQuark_p4            ));
  double dPhi_Htb_TQuark_gtt_TQuark                = std::fabs(ROOT::Math::VectorUtil::DeltaPhi( Htb_TQuark_p4, gtt_TQuark_p4            ));
  double dPhi_Htb_TQuark_gbb_BQuark                = std::fabs(ROOT::Math::VectorUtil::DeltaPhi( Htb_TQuark_p4, gbb_BQuark_p4            ));
  double dPhi_Htb_BQuark_Htb_tbW_BQuark            = std::fabs(ROOT::Math::VectorUtil::DeltaPhi( Htb_BQuark_p4, Htb_tbW_BQuark_p4        ));
  double dPhi_Htb_BQuark_Htb_tbW_Wqq_Quark         = std::fabs(ROOT::Math::VectorUtil::DeltaPhi( Htb_BQuark_p4, Htb_tbW_Wqq_Quark_p4     ));
  double dPhi_Htb_BQuark_Htb_tbW_Wqq_AntiQuark     = std::fabs(ROOT::Math::VectorUtil::DeltaPhi( Htb_BQuark_p4, Htb_tbW_Wqq_AntiQuark_p4 ));
  double dPhi_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark     = std::fabs(ROOT::Math::VectorUtil::DeltaPhi( Htb_tbW_BQuark_p4, Htb_tbW_Wqq_Quark_p4 ));
  double dPhi_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark = std::fabs(ROOT::Math::VectorUtil::DeltaPhi( Htb_tbW_BQuark_p4, Htb_tbW_Wqq_AntiQuark_p4));

  double dRap_Htb_TQuark_Htb_BQuark                = std::fabs( mcTools.GetRapidity(Htb_TQuark_p4) - mcTools.GetRapidity(Htb_BQuark_p4)            );
  double dRap_Htb_TQuark_gtt_TQuark                = std::fabs( mcTools.GetRapidity(Htb_TQuark_p4) - mcTools.GetRapidity(gtt_TQuark_p4)            );
  double dRap_Htb_TQuark_gbb_BQuark                = std::fabs( mcTools.GetRapidity(Htb_TQuark_p4) - mcTools.GetRapidity(gbb_BQuark_p4)            );
  double dRap_Htb_BQuark_Htb_tbW_BQuark            = std::fabs( mcTools.GetRapidity(Htb_BQuark_p4) - mcTools.GetRapidity(Htb_tbW_BQuark_p4)        );
  double dRap_Htb_BQuark_Htb_tbW_Wqq_Quark         = std::fabs( mcTools.GetRapidity(Htb_BQuark_p4) - mcTools.GetRapidity(Htb_tbW_Wqq_Quark_p4)     );
  double dRap_Htb_BQuark_Htb_tbW_Wqq_AntiQuark     = std::fabs( mcTools.GetRapidity(Htb_BQuark_p4) - mcTools.GetRapidity(Htb_tbW_Wqq_AntiQuark_p4) );
  double dRap_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark     = std::fabs( mcTools.GetRapidity(Htb_tbW_BQuark_p4) - mcTools.GetRapidity(Htb_tbW_Wqq_Quark_p4 ));
  double dRap_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark = std::fabs( mcTools.GetRapidity(Htb_tbW_BQuark_p4) - mcTools.GetRapidity(Htb_tbW_Wqq_AntiQuark_p4));
  
  // Associated products
  double dR_gtt_TQuark_gbb_BQuark                = ROOT::Math::VectorUtil::DeltaR(gtt_TQuark_p4    , gbb_BQuark_p4            );
  double dR_gtt_TQuark_gtt_tbW_BQuark            = ROOT::Math::VectorUtil::DeltaR(gtt_TQuark_p4    , gtt_tbW_BQuark_p4        ); 
  double dR_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark     = ROOT::Math::VectorUtil::DeltaR(gtt_tbW_BQuark_p4, gtt_tbW_Wqq_Quark_p4     );
  double dR_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark = ROOT::Math::VectorUtil::DeltaR(gtt_tbW_BQuark_p4, gtt_tbW_Wqq_AntiQuark_p4 );

  double dEta_gtt_TQuark_gbb_BQuark                = std::fabs( gtt_TQuark_p4.eta()     - gbb_BQuark_p4.eta()            );
  double dEta_gtt_TQuark_gtt_tbW_BQuark            = std::fabs( gtt_TQuark_p4.eta()     - gtt_tbW_BQuark_p4.eta()        ); 
  double dEta_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark     = std::fabs( gtt_tbW_BQuark_p4.eta() - gtt_tbW_Wqq_Quark_p4.eta()     );
  double dEta_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark = std::fabs( gtt_tbW_BQuark_p4.eta() - gtt_tbW_Wqq_AntiQuark_p4.eta() );
  
  double dPhi_gtt_TQuark_gbb_BQuark                = std::fabs(ROOT::Math::VectorUtil::DeltaPhi( gtt_TQuark_p4    , gbb_BQuark_p4            ));
  double dPhi_gtt_TQuark_gtt_tbW_BQuark            = std::fabs(ROOT::Math::VectorUtil::DeltaPhi( gtt_TQuark_p4    , gtt_tbW_BQuark_p4        )); 
  double dPhi_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark     = std::fabs(ROOT::Math::VectorUtil::DeltaPhi( gtt_tbW_BQuark_p4, gtt_tbW_Wqq_Quark_p4     ));
  double dPhi_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark = std::fabs(ROOT::Math::VectorUtil::DeltaPhi( gtt_tbW_BQuark_p4, gtt_tbW_Wqq_AntiQuark_p4 ));

  double dRap_gtt_TQuark_gbb_BQuark                = std::fabs( mcTools.GetRapidity(gtt_TQuark_p4)     - mcTools.GetRapidity(gbb_BQuark_p4)            );
  double dRap_gtt_TQuark_gtt_tbW_BQuark            = std::fabs( mcTools.GetRapidity(gtt_TQuark_p4)     - mcTools.GetRapidity(gtt_tbW_BQuark_p4)        ); 
  double dRap_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark     = std::fabs( mcTools.GetRapidity(gtt_tbW_BQuark_p4) - mcTools.GetRapidity(gtt_tbW_Wqq_Quark_p4)     );
  double dRap_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark = std::fabs( mcTools.GetRapidity(gtt_tbW_BQuark_p4) - mcTools.GetRapidity(gtt_tbW_Wqq_AntiQuark_p4) );

  // Fill dR histos
  h_Htb_TQuark_Htb_BQuark_dR                ->Fill(dR_Htb_TQuark_Htb_BQuark);
  h_Htb_TQuark_gtt_TQuark_dR                ->Fill(dR_Htb_TQuark_gtt_TQuark);
  h_Htb_TQuark_gbb_BQuark_dR                ->Fill(dR_Htb_TQuark_gbb_BQuark);
  h_Htb_BQuark_Htb_tbW_BQuark_dR            ->Fill(dR_Htb_BQuark_Htb_tbW_BQuark);
  h_Htb_BQuark_Htb_tbW_Wqq_Quark_dR         ->Fill(dR_Htb_BQuark_Htb_tbW_Wqq_Quark);
  h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dR     ->Fill(dR_Htb_BQuark_Htb_tbW_Wqq_AntiQuark);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dR     ->Fill(dR_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dR ->Fill(dR_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark);
  h_gtt_TQuark_gbb_BQuark_dR                ->Fill(dR_gtt_TQuark_gbb_BQuark);
  h_gtt_TQuark_gtt_tbW_BQuark_dR            ->Fill(dR_gtt_TQuark_gtt_tbW_BQuark);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dR     ->Fill(dR_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dR ->Fill(dR_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark);

  h_Htb_TQuark_Htb_BQuark_dEta                ->Fill(dEta_Htb_TQuark_Htb_BQuark);
  h_Htb_TQuark_gtt_TQuark_dEta                ->Fill(dEta_Htb_TQuark_gtt_TQuark);
  h_Htb_TQuark_gbb_BQuark_dEta                ->Fill(dEta_Htb_TQuark_gbb_BQuark);
  h_Htb_BQuark_Htb_tbW_BQuark_dEta            ->Fill(dEta_Htb_BQuark_Htb_tbW_BQuark);
  h_Htb_BQuark_Htb_tbW_Wqq_Quark_dEta         ->Fill(dEta_Htb_BQuark_Htb_tbW_Wqq_Quark);
  h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dEta     ->Fill(dEta_Htb_BQuark_Htb_tbW_Wqq_AntiQuark);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dEta     ->Fill(dEta_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dEta ->Fill(dEta_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark);
  h_gtt_TQuark_gbb_BQuark_dEta                ->Fill(dEta_gtt_TQuark_gbb_BQuark);
  h_gtt_TQuark_gtt_tbW_BQuark_dEta            ->Fill(dEta_gtt_TQuark_gtt_tbW_BQuark);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dEta     ->Fill(dEta_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dEta ->Fill(dEta_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark);

  h_Htb_TQuark_Htb_BQuark_dPhi                ->Fill(dPhi_Htb_TQuark_Htb_BQuark);
  h_Htb_TQuark_gtt_TQuark_dPhi                ->Fill(dPhi_Htb_TQuark_gtt_TQuark);
  h_Htb_TQuark_gbb_BQuark_dPhi                ->Fill(dPhi_Htb_TQuark_gbb_BQuark);
  h_Htb_BQuark_Htb_tbW_BQuark_dPhi            ->Fill(dPhi_Htb_BQuark_Htb_tbW_BQuark);
  h_Htb_BQuark_Htb_tbW_Wqq_Quark_dPhi         ->Fill(dPhi_Htb_BQuark_Htb_tbW_Wqq_Quark);
  h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dPhi     ->Fill(dPhi_Htb_BQuark_Htb_tbW_Wqq_AntiQuark);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dPhi     ->Fill(dPhi_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dPhi ->Fill(dPhi_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark);
  h_gtt_TQuark_gbb_BQuark_dPhi                ->Fill(dPhi_gtt_TQuark_gbb_BQuark);
  h_gtt_TQuark_gtt_tbW_BQuark_dPhi            ->Fill(dPhi_gtt_TQuark_gtt_tbW_BQuark);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dPhi     ->Fill(dPhi_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dPhi ->Fill(dPhi_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark);

  h_Htb_TQuark_Htb_BQuark_dRap                ->Fill(dRap_Htb_TQuark_Htb_BQuark);
  h_Htb_TQuark_gtt_TQuark_dRap                ->Fill(dRap_Htb_TQuark_gtt_TQuark);
  h_Htb_TQuark_gbb_BQuark_dRap                ->Fill(dRap_Htb_TQuark_gbb_BQuark);
  h_Htb_BQuark_Htb_tbW_BQuark_dRap            ->Fill(dRap_Htb_BQuark_Htb_tbW_BQuark);
  h_Htb_BQuark_Htb_tbW_Wqq_Quark_dRap         ->Fill(dRap_Htb_BQuark_Htb_tbW_Wqq_Quark);
  h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dRap     ->Fill(dRap_Htb_BQuark_Htb_tbW_Wqq_AntiQuark);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark_dRap     ->Fill(dRap_Htb_tbW_BQuark_Htb_tbW_Wqq_Quark);
  h_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark_dRap ->Fill(dRap_Htb_tbW_BQuark_Htb_tbW_Wqq_AntiQuark);
  h_gtt_TQuark_gbb_BQuark_dRap                ->Fill(dRap_gtt_TQuark_gbb_BQuark);
  h_gtt_TQuark_gtt_tbW_BQuark_dRap            ->Fill(dRap_gtt_TQuark_gtt_tbW_BQuark);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dRap     ->Fill(dRap_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dRap ->Fill(dRap_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark);

  
  // Leading B-quarks
  std::vector<math::XYZTLorentzVector> bQuarks_p4;
  bQuarks_p4.push_back(Htb_BQuark_p4);
  bQuarks_p4.push_back(Htb_tbW_BQuark_p4);
  bQuarks_p4.push_back(gbb_BQuark_p4);
  bQuarks_p4.push_back(gtt_tbW_BQuark_p4);
  /// Sort bQuarks by pT 
  std::sort( bQuarks_p4.begin(), bQuarks_p4.end(), PtComparator() );

  // Require at least 4 b-quarks for these plots
  if (bQuarks_p4.size() < 4) return;

  double deltaRMin = 999999.9;
  int deltaRMin_i  = -1;
  int deltaRMin_j  = -1;
  
  // For-loop: All (pT-sorted) b-quarks
  for (size_t i = 0; i < bQuarks_p4.size(); i++)
    {

      double dEta_1_2 = std::fabs(bQuarks_p4.at(0).eta() - bQuarks_p4.at(1).eta());
      double dEta_1_3 = std::fabs(bQuarks_p4.at(0).eta() - bQuarks_p4.at(2).eta());
      double dEta_1_4 = std::fabs(bQuarks_p4.at(0).eta() - bQuarks_p4.at(3).eta());
      double dPhi_1_2 = std::fabs(bQuarks_p4.at(0).phi() - bQuarks_p4.at(1).phi());
      double dPhi_1_3 = std::fabs(bQuarks_p4.at(0).phi() - bQuarks_p4.at(2).phi());
      double dPhi_1_4 = std::fabs(bQuarks_p4.at(0).phi() - bQuarks_p4.at(3).phi());
      //
      double dEta_2_3 = std::fabs(bQuarks_p4.at(1).eta() - bQuarks_p4.at(2).eta());
      double dEta_2_4 = std::fabs(bQuarks_p4.at(1).eta() - bQuarks_p4.at(3).eta());
      double dPhi_2_3 = std::fabs(bQuarks_p4.at(1).phi() - bQuarks_p4.at(2).phi());
      double dPhi_2_4 = std::fabs(bQuarks_p4.at(1).phi() - bQuarks_p4.at(3).phi());
      //
      double dEta_3_4 = std::fabs(bQuarks_p4.at(2).eta() - bQuarks_p4.at(3).eta());
      double dPhi_3_4 = std::fabs(bQuarks_p4.at(2).phi() - bQuarks_p4.at(3).phi());
           
      // Fill 2D histos
      h_BQuark1_BQuark2_dEta_Vs_dPhi->Fill( dEta_1_2 , dPhi_1_2 );
      h_BQuark1_BQuark3_dEta_Vs_dPhi->Fill( dEta_1_3 , dPhi_1_3 );
      h_BQuark1_BQuark4_dEta_Vs_dPhi->Fill( dEta_1_4 , dPhi_1_4 );
      h_BQuark2_BQuark3_dEta_Vs_dPhi->Fill( dEta_2_3 , dPhi_2_3 );
      h_BQuark2_BQuark4_dEta_Vs_dPhi->Fill( dEta_2_4 , dPhi_2_4 );
      h_BQuark3_BQuark4_dEta_Vs_dPhi->Fill( dEta_3_4 , dPhi_3_4 );

      if (i==0)
	{
	  h_BQuark1_Pt ->Fill( bQuarks_p4.at(i).pt()  );
	  h_BQuark1_Eta->Fill( bQuarks_p4.at(i).eta() );
	}
      else if (i==1)
	{
	  h_BQuark2_Pt ->Fill( bQuarks_p4.at(i).pt()  );
	  h_BQuark2_Eta->Fill( bQuarks_p4.at(i).eta() );
	}
      else if (i==2)
	{
	  h_BQuark3_Pt ->Fill( bQuarks_p4.at(i).pt()  );
	  h_BQuark3_Eta->Fill( bQuarks_p4.at(i).eta() );
	}
      else if (i==3)
	{
	  h_BQuark4_Pt ->Fill( bQuarks_p4.at(i).pt()  );
	  h_BQuark4_Eta->Fill( bQuarks_p4.at(i).eta() );
	}
      else{}

      for (size_t j = i+1; j < bQuarks_p4.size(); j++)
	{
	  
	  double deltaR = ROOT::Math::VectorUtil::DeltaR(bQuarks_p4.at(i), bQuarks_p4.at(j));

	  if (deltaR < deltaRMin)
	    {
	      deltaRMin = deltaR;
	      deltaRMin_i = i;
	      deltaRMin_j = j;
	    }	  
	}      
    } // For-loop: All (pT-sorted) b-quarks

  // std::cout << "deltaRMin = " << deltaRMin << ", i = " << deltaRMin_i << ", j = " << deltaRMin_j <<  ", nbjets = " << bQuarks_p4.size() << std::endl;  
  math::XYZTLorentzVector bQuarkPair_dRMin_p4 = bQuarks_p4.at(deltaRMin_i) + bQuarks_p4.at(deltaRMin_j);
  double bQuarkPair_dEta = std::fabs(bQuarks_p4.at(deltaRMin_i).eta() - bQuarks_p4.at(deltaRMin_j).eta());
  double bQuarkPair_dPhi = std::fabs(ROOT::Math::VectorUtil::DeltaPhi(bQuarks_p4.at(deltaRMin_i), bQuarks_p4.at(deltaRMin_j)));
  h_BQuarkPair_dRMin_pT   ->Fill( bQuarkPair_dRMin_p4.pt() );
  h_BQuarkPair_dRMin_dEta ->Fill( bQuarkPair_dEta );
  h_BQuarkPair_dRMin_dPhi ->Fill( bQuarkPair_dPhi );
  h_BQuarkPair_dRMin_dR   ->Fill( deltaRMin );
  h_BQuarkPair_dRMin_Mass ->Fill( bQuarkPair_dRMin_p4.mass() );
  h_BQuarkPair_dRMin_Eta1_Vs_Eta2->Fill( bQuarks_p4.at(deltaRMin_i).eta(), bQuarks_p4.at(deltaRMin_j).eta());
  h_BQuarkPair_dRMin_Phi1_Vs_Phi2->Fill( bQuarks_p4.at(deltaRMin_i).phi(), bQuarks_p4.at(deltaRMin_j).phi());
  h_BQuarkPair_dRMin_Pt1_Vs_Pt2  ->Fill(bQuarks_p4.at(deltaRMin_i).pt(), bQuarks_p4.at(deltaRMin_j).pt());
  h_BQuarkPair_dRMin_dEta_Vs_dPhi->Fill( bQuarkPair_dEta, bQuarkPair_dPhi);
  //
  if (selJets_p4.size() > 0)
    {
      h_BQuarkPair_dRMin_jet1_dEta ->Fill( std::fabs(bQuarkPair_dRMin_p4.eta() - selJets_p4.at(0).eta()) );
      h_BQuarkPair_dRMin_jet1_dPhi ->Fill( std::fabs(ROOT::Math::VectorUtil::DeltaPhi(bQuarkPair_dRMin_p4, selJets_p4.at(0) ) ) );
      h_BQuarkPair_dRMin_jet1_dR   ->Fill( ROOT::Math::VectorUtil::DeltaR(bQuarkPair_dRMin_p4, selJets_p4.at(0) ) );
    }

  if (selJets_p4.size() > 1)  
    {
      h_BQuarkPair_dRMin_jet2_dEta ->Fill( std::fabs(bQuarkPair_dRMin_p4.eta() - selJets_p4.at(1).eta()) );
      h_BQuarkPair_dRMin_jet2_dPhi ->Fill( std::fabs(ROOT::Math::VectorUtil::DeltaPhi(bQuarkPair_dRMin_p4, selJets_p4.at(1) ) ) );
      h_BQuarkPair_dRMin_jet2_dR   ->Fill( ROOT::Math::VectorUtil::DeltaR(bQuarkPair_dRMin_p4, selJets_p4.at(1) ) );
    }
  
  return;
}
