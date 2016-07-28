// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

// User
#include "Auxiliary/interface/Table.h"
#include "Auxiliary/interface/Tools.h"
#include "Tools/interface/MCTools.h"
#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

// ROOT
#include "TDirectory.h"
#include "Math/VectorUtil.h"

struct PtComparator
{
  bool operator() (const math::XYZTLorentzVector p1, const math::XYZTLorentzVector p2) const { return ( p1.pt() > p2.pt() ); }
};


class Kinematics: public BaseSelector {
public:
  explicit Kinematics(const ParameterSet& config, const TH1* skimCounters);
  virtual ~Kinematics() {}

  /// Books histograms
  virtual void book(TDirectory *dir) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;
   
private:
  // Input parameters
  const double cfg_Verbose;
  const double cfg_TopQuark_Pt;
  const double cfg_TopQuark_Eta;
  Tools auxTools;
  
  // Counters
  Count cAllEvents;
  // Count cTrigger;
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

  
  // Non-common histograms
  WrappedTH1 *h_genMET_Et;
  WrappedTH1 *h_genMET_Phi;

  WrappedTH1 *h_genHT_GenParticles;
  WrappedTH1 *h_genHT_GenJets;  

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

  WrappedTH1 *h_gtt_TQuark_Phi;
  WrappedTH1 *h_gtt_tbW_WBoson_Phi;
  WrappedTH1 *h_gtt_tbW_BQuark_Phi;
  WrappedTH1 *h_gtt_tbW_Wqq_Quark_Phi;
  WrappedTH1 *h_gtt_tbW_Wqq_AntiQuark_Phi;  
  WrappedTH1 *h_tbH_HPlus_Phi;
  WrappedTH1 *h_tbH_TQuark_Phi;
  WrappedTH1 *h_tbH_BQuark_Phi;
  WrappedTH1 *h_tbH_tbW_WBoson_Phi;
  WrappedTH1 *h_tbH_tbW_BQuark_Phi;
  WrappedTH1 *h_gbb_BQuark_Phi;
  WrappedTH1 *h_Htb_tbW_Wqq_Quark_Phi;
  WrappedTH1 *h_Htb_tbW_Wqq_AntiQuark_Phi;
  
  WrappedTH1 *h_Htb_TQuark_Htb_BQuark_dR;
  WrappedTH1 *h_Htb_TQuark_gtt_TQuark_dR;
  WrappedTH1 *h_Htb_TQuark_gbb_BQuark_dR;
  
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_BQuark_dR;
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_Wqq_Quark_dR;
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dR;
  WrappedTH1 *h_gtt_TQuark_gbb_BQuark_dR;
  WrappedTH1 *h_gtt_TQuark_gtt_tbW_BQuark_dR;
  WrappedTH1 *h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dR;
  WrappedTH1 *h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dR;

  WrappedTH1 *h_BQuark_Ldg_Pt;
  WrappedTH1 *h_BQuark_NLdg_Pt;
  WrappedTH1 *h_BQuark_NNLdg_Pt;
  WrappedTH1 *h_BQuark_NNNLdg_Pt;

  WrappedTH1 *h_BQuark_Ldg_Eta;
  WrappedTH1 *h_BQuark_NLdg_Eta;
  WrappedTH1 *h_BQuark_NNLdg_Eta;
  WrappedTH1 *h_BQuark_NNNLdg_Eta;

  WrappedTH1 *h_BQuark_Ldg_Phi;
  WrappedTH1 *h_BQuark_NLdg_Phi;
  WrappedTH1 *h_BQuark_NNLdg_Phi;
  WrappedTH1 *h_BQuark_NNNLdg_Phi;

  WrappedTH1 *h_GenJet_Multiplicity;
  WrappedTH1 *h_SelGenJet_Multiplicity;
  WrappedTH1 *h_SelGenJet_LdgDiJet_Mass;

  WrappedTH1 *h_SelGenJet_MaxDiJetMass_Pt;
  WrappedTH1 *h_SelGenJet_MaxDiJetMass_Eta;
  WrappedTH1 *h_SelGenJet_MaxDiJetMass_Rapidity; 
  WrappedTH1 *h_SelGenJet_MaxDiJetMass_Mass;
  WrappedTH1 *h_SelGenJet_MaxDiJetMass_dR;
  
  WrappedTH1 *h_GenJet_Ldg_Pt;
  WrappedTH1 *h_GenJet_NLdg_Pt;
  WrappedTH1 *h_GenJet_NNLdg_Pt;
  WrappedTH1 *h_GenJet_NNNLdg_Pt;

  WrappedTH1 *h_GenJet_Ldg_Eta;
  WrappedTH1 *h_GenJet_NLdg_Eta;
  WrappedTH1 *h_GenJet_NNLdg_Eta;
  WrappedTH1 *h_GenJet_NNNLdg_Eta;

  WrappedTH1 *h_GenJet_Ldg_Phi;
  WrappedTH1 *h_GenJet_NLdg_Phi;
  WrappedTH1 *h_GenJet_NNLdg_Phi;
  WrappedTH1 *h_GenJet_NNNLdg_Phi;

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(Kinematics);

Kinematics::Kinematics(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    cfg_Verbose(config.getParameter<bool>("Verbose")),
    cfg_TopQuark_Pt(config.getParameter<double>("TopQuark_Pt")),
    cfg_TopQuark_Eta(config.getParameter<double>("TopQuark_Eta")),  
    cAllEvents(fEventCounter.addCounter("All events")),
    cHtb_HPlus(fEventCounter.addCounter("H+")),
    cHtb_TQuark(fEventCounter.addCounter("H+->tb, t")),
    cHtb_BQuark(fEventCounter.addCounter("H+->tb, b")),
    cHtb_tbW_BQuark(fEventCounter.addCounter("H+->tb, t->bW, b")),
    cHtb_tbW_WBoson(fEventCounter.addCounter("H+->tb, t->bW, W+")),
    cHtb_tbW_Wqq_Quark(fEventCounter.addCounter("H+->tb, t->bW, W->qq, q")),
    cHtb_tbW_Wqq_AntiQuark(fEventCounter.addCounter("H+->tb, t->bW, W->qq, qbar")),
    cHtb_tbW_Wqq_Leptons(fEventCounter.addCounter("H+->tb, t->bW, W->l v")),
    cgtt_TQuark(fEventCounter.addCounter("g->tt, t")),
    cgbb_BQuark(fEventCounter.addCounter("g->bb, b")),
    cgtt_tbW_Wqq_Quark(fEventCounter.addCounter("g->tt, t->bW, W->qq, q")),
    cgtt_tbW_Wqq_AntiQuark(fEventCounter.addCounter("g->tt, t->bW, W->qq, qbar")),
    cgtt_tbW_Wqq_Leptons(fEventCounter.addCounter("g->tt, t->bW, W->l v")),
    cgtt_tbW_WBoson(fEventCounter.addCounter("g->tt, t->bW, W")),
    cgtt_tbW_BQuark(fEventCounter.addCounter("g->tt, t->bW, b"))
  
{ }

void Kinematics::book(TDirectory *dir) {

  // Book histograms
  h_genMET_Et         =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genMET_Et"          , "gen MET Et"           , 100,  0.0   ,  +500.0);  
  h_genMET_Phi        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genMET_Phi"         , "gen MET Phi"          , 100, -3.1416,   +3.1416);
  h_genHT_GenParticles=  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genHT_GenParticles" , "gen HT, GenParticles" , 150,  0.0   , +1500.0);
  h_genHT_GenJets     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genHT_GenJets"      , "gen HT, GenJets"      , 150,  0.0   , +1500.0);

  h_gtt_TQuark_Pt            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_TQuark_Pt"           , "gtt, t-quark pT"        , 100, 0.0, 500.0);
  h_gtt_tbW_WBoson_Pt        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_WBoson_Pt"       , "gtt, tWb W-boson pT"    , 100, 0.0, 500.0);
  h_gtt_tbW_BQuark_Pt        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_BQuark_Pt"       , "gtt, tWb b-quark pT"    , 100, 0.0, 500.0);
  h_gtt_tbW_Wqq_Quark_Pt     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_Wqq_Quark_Pt"    , "gtt, tWb, Wqq, Q pT"    , 100, 0.0, 500.0);
  h_gtt_tbW_Wqq_AntiQuark_Pt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_Wqq_AntiQuark_Pt", "gtt, tWb, Wqq, Qbar pT" , 100, 0.0, 500.0);
  h_tbH_HPlus_Pt             =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_HPlus_Pt"            , "tbH, HPlus pT"          , 100, 0.0, 500.0);
  h_tbH_TQuark_Pt            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_TQuark_Pt"           , "tbH, t-quark pT"        , 100, 0.0, 500.0);
  h_tbH_BQuark_Pt            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_BQuark_Pt"           , "tbH, b-quark pT"        , 100, 0.0, 500.0);
  h_tbH_tbW_WBoson_Pt        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_tbW_WBoson_Pt"       , "tbH, tbW, W-boson pT"   , 100, 0.0, 500.0);
  h_tbH_tbW_BQuark_Pt        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_tbW_BQuark_Pt"       , "tbH, tbW, b-quark pT"   , 100, 0.0, 500.0);
  h_gbb_BQuark_Pt            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gbb_BQuark_Pt"           , "gtt, b-quark pT, "      , 100, 0.0, 500.0);
  h_Htb_tbW_Wqq_Quark_Pt     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_Wqq_Quark_Pt"    , "Htb, tbW, Q pT, "       , 100, 0.0, 500.0);
  h_Htb_tbW_Wqq_AntiQuark_Pt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_Wqq_AntiQuark_Pt", "Htb, tbW, Qbar pT, "    , 100, 0.0, 500.0);

  h_gtt_TQuark_Eta            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_TQuark_Eta"           , "gtt, t-quark eta"        , 50, -2.5, +2.5);
  h_gtt_tbW_WBoson_Eta        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_WBoson_Eta"       , "gtt, tWb W-boson eta"    , 50, -2.5, +2.5);
  h_gtt_tbW_BQuark_Eta        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_BQuark_Eta"       , "gtt, tWb b-quark eta"    , 50, -2.5, +2.5);
  h_gtt_tbW_Wqq_Quark_Eta     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_Wqq_Quark_Eta"    , "gtt, tWb, Wqq, Q eta"    , 50, -2.5, +2.5);
  h_gtt_tbW_Wqq_AntiQuark_Eta =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_Wqq_AntiQuark_Eta", "gtt, tWb, Wqq, Qbar eta" , 50, -2.5, +2.5);
  h_tbH_HPlus_Eta             =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_HPlus_Eta"            , "tbH, HPlus eta"          , 50, -2.5, +2.5);
  h_tbH_TQuark_Eta            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_TQuark_Eta"           , "tbH, t-quark eta"        , 50, -2.5, +2.5);
  h_tbH_BQuark_Eta            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_BQuark_Eta"           , "tbH, b-quark eta"        , 50, -2.5, +2.5);
  h_tbH_tbW_WBoson_Eta        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_tbW_WBoson_Eta"       , "tbH, tbW, W-boson eta"   , 50, -2.5, +2.5);
  h_tbH_tbW_BQuark_Eta        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_tbW_BQuark_Eta"       , "tbH, tbW, b-quark eta"   , 50, -2.5, +2.5);
  h_gbb_BQuark_Eta            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gbb_BQuark_Eta"           , "gtt, b-quark eta, "      , 50, -2.5, +2.5);
  h_Htb_tbW_Wqq_Quark_Eta     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_Wqq_Quark_Eta"    , "Htb, tbW, Q eta, "       , 50, -2.5, +2.5);
  h_Htb_tbW_Wqq_AntiQuark_Eta =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_tbW_Wqq_AntiQuark_Eta", "Htb, tbW, Qbar eta, "    , 50, -2.5, +2.5);

  h_gtt_TQuark_Phi            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gtt_TQuark_Phi"           , "gtt, t-quark phi"       , 100, -3.1416, +3.1416);
  h_gtt_tbW_WBoson_Phi        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gtt_tbW_WBoson_Phi"       , "gtt, tWb W-boson phi"   , 100, -3.1416, +3.1416);
  h_gtt_tbW_BQuark_Phi        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gtt_tbW_BQuark_Phi"       , "gtt, tWb b-quark phi"   , 100, -3.1416, +3.1416);
  h_gtt_tbW_Wqq_Quark_Phi     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gtt_tbW_Wqq_Quark_Phi"    , "gtt, tWb, Wqq, Q phi"   , 100, -3.1416, +3.1416);
  h_gtt_tbW_Wqq_AntiQuark_Phi =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gtt_tbW_Wqq_AntiQuark_Phi", "gtt, tWb, Wqq, Qbar phi", 100, -3.1416, +3.1416);
  h_tbH_HPlus_Phi             =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_HPlus_Phi"            , "tbH, HPlus phi"         , 100, -3.1416, +3.1416);
  h_tbH_TQuark_Phi            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_TQuark_Phi"           , "tbH, t-quark phi"       , 100, -3.1416, +3.1416);
  h_tbH_BQuark_Phi            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_BQuark_Phi"           , "tbH, b-quark phi"       , 100, -3.1416, +3.1416);
  h_tbH_tbW_WBoson_Phi        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_tbW_WBoson_Phi"       , "tbH, tbW, W-boson phi"  , 100, -3.1416, +3.1416);
  h_tbH_tbW_BQuark_Phi        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_tbW_BQuark_Phi"       , "tbH, tbW, b-quark phi"  , 100, -3.1416, +3.1416);
  h_gbb_BQuark_Phi            =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gbb_BQuark_Phi"           , "gtt, b-quark phi, "     , 100, -3.1416, +3.1416);
  h_Htb_tbW_Wqq_Quark_Phi     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "Htb_tbW_Wqq_Quark_Phi"    , "Htb, tbW, Q phi, "      , 100, -3.1416, +3.1416);
  h_Htb_tbW_Wqq_AntiQuark_Phi =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "Htb_tbW_Wqq_AntiQuark_Phi", "Htb, tbW, Qbar phi, "   , 100, -3.1416, +3.1416);

  // deltaR
  h_Htb_TQuark_Htb_BQuark_dR                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_TQuark_Htb_BQuark_dR"               , "dR(t, b)", 100, 0.0, +10.0);
  h_Htb_TQuark_gtt_TQuark_dR                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_TQuark_gtt_TQuark_dR"               , "dR(t, t)", 100, 0.0, +10.0);
  h_Htb_TQuark_gbb_BQuark_dR                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_TQuark_gbb_BQuark_dR"               , "dR(t, b)", 100, 0.0, +10.0);
  h_Htb_BQuark_Htb_tbW_BQuark_dR            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_BQuark_Htb_tbW_BQuark_dR"           , "dR(b, b)", 100, 0.0, +10.0);
  h_Htb_BQuark_Htb_tbW_Wqq_Quark_dR         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_BQuark_Htb_tbW_Wqq_Quark_dR"        , "dR(b, q)", 100, 0.0, +10.0);
  h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dR     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dR"    , "dR(b, q)", 100, 0.0, +10.0);
  h_gtt_TQuark_gbb_BQuark_dR                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_TQuark_gbb_BQuark_dR"               , "dR(b, b)", 100, 0.0, +10.0);
  h_gtt_TQuark_gtt_tbW_BQuark_dR            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_TQuark_gtt_tbW_BQuark_dR"           , "dR(t, b)", 100, 0.0, +10.0);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dR     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dR"    , "dR(b, q)", 100, 0.0, +10.0);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dR", "dR(b, q)", 100, 0.0, +10.0);
  
  // B-quarks
  h_BQuark_Ldg_Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark_Ldg_Pt"   , "Ldg b-quark, pT"                         , 100, 0.0, +500.0);
  h_BQuark_NLdg_Pt   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark_NLdg_Pt"  , "Next-to-Ldg b-quark, pT"                 , 100, 0.0, +500.0);
  h_BQuark_NNLdg_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark_NNLdg_Pt" , "Next-to-Next-to-Ldg b-quark, pT"         , 100, 0.0, +500.0);
  h_BQuark_NNNLdg_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark_NNNLdg_Pt", "Next-to-Next-to-Next-to-Ldg b-quark, pT" , 100, 0.0, +500.0);

  h_BQuark_Ldg_Eta    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark_Ldg_Eta"   , "Ldg b-quark, eta"                         , 50, -2.5, +2.5);
  h_BQuark_NLdg_Eta   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark_NLdg_Eta"  , "Next-to-Ldg b-quark, eta"                 , 50, -2.5, +2.5);
  h_BQuark_NNLdg_Eta  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark_NNLdg_Eta" , "Next-to-Next-to-Ldg b-quark, eta"         , 50, -2.5, +2.5);
  h_BQuark_NNNLdg_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "BQuark_NNNLdg_Eta", "Next-to-Next-to-Next-to-Ldg b-quark, eta" , 50, -2.5, +2.5);

  h_BQuark_Ldg_Phi    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "BQuark_Ldg_Phi"   , "Ldg b-quark, phi"                         , 100, -3.1416, +3.1416);
  h_BQuark_NLdg_Phi   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "BQuark_NLdg_Phi"  , "Next-to-Ldg b-quark, phi"                 , 100, -3.1416, +3.1416);
  h_BQuark_NNLdg_Phi  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "BQuark_NNLdg_Phi" , "Next-to-Next-to-Ldg b-quark, phi"         , 100, -3.1416, +3.1416);
  h_BQuark_NNNLdg_Phi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "BQuark_NNNLdg_Phi", "Next-to-Next-to-Next-to-Ldg b-quark, phi" , 100, -3.1416, +3.1416);

  // GenJets
  h_GenJet_Multiplicity         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet_Multiplicity"        , "GenJet multiplicity, N"             , 20, 0.0, +20.0);
  h_SelGenJet_Multiplicity      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelGenJet_Multiplicity"     , "Selected GenJet multiplicity, N"    , 20, 0.0, +20.0);
  h_SelGenJet_LdgDiJet_Mass     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelGenJet_LdgDiJet_Mass"    , "Selected GenJet LdgDiJet Mass, mass", 100, 0.0, +1000.0);

  h_SelGenJet_MaxDiJetMass_Pt       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelGenJet_MaxDiJetMass_Pt"      , "Selected MaxDiJet, Pt"         , 100, 0.0, +500.0);
  h_SelGenJet_MaxDiJetMass_Eta      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelGenJet_MaxDiJetMass_Eta"     , "Selected MaxDiJet, Eta"        ,  50, -2.5, +2.5);
  h_SelGenJet_MaxDiJetMass_Rapidity = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelGenJet_MaxDiJetMass_Rapidity", "Selected MaxDiJet, Rapidity"   , 100,-5.0, +5.0);
  h_SelGenJet_MaxDiJetMass_Mass     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelGenJet_MaxDiJetMass_Mass"    , "Selected GenJet MaxDiJet, Mass", 150, 0.0, +1500.0);
  h_SelGenJet_MaxDiJetMass_dR       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelGenJet_MaxDiJetMass_dR"      , "Selected GenJet MaxDiJet, dR"  , 100, 0.0, +10.0);

  h_GenJet_Ldg_Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet_Ldg_Pt"   , "Ldg genJet, pT"                         , 100, 0.0, +500.0);
  h_GenJet_NLdg_Pt   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet_NLdg_Pt"  , "Next-to-Ldg genJet, pT"                 , 100, 0.0, +500.0);
  h_GenJet_NNLdg_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet_NNLdg_Pt" , "Next-to-Next-to-Ldg genJet, pT"         , 100, 0.0, +500.0);
  h_GenJet_NNNLdg_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet_NNNLdg_Pt", "Next-to-Next-to-Next-to-Ldg genJet, pT" , 100, 0.0, +500.0);

  h_GenJet_Ldg_Eta    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet_Ldg_Eta"   , "Ldg genJet, eta"                         , 50, -2.5, +2.5);
  h_GenJet_NLdg_Eta   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet_NLdg_Eta"  , "Next-to-Ldg genJet, eta"                 , 50, -2.5, +2.5);
  h_GenJet_NNLdg_Eta  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet_NNLdg_Eta" , "Next-to-Next-to-Ldg genJet, eta"         , 50, -2.5, +2.5);
  h_GenJet_NNNLdg_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "GenJet_NNNLdg_Eta", "Next-to-Next-to-Next-to-Ldg genJet, eta" , 50, -2.5, +2.5);

  h_GenJet_Ldg_Phi    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GenJet_Ldg_Phi"   , "Ldg genJet, phi"                         , 100, -3.1416, +3.1416);
  h_GenJet_NLdg_Phi   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GenJet_NLdg_Phi"  , "Next-to-Ldg genJet, phi"                 , 100, -3.1416, +3.1416);
  h_GenJet_NNLdg_Phi  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GenJet_NNLdg_Phi" , "Next-to-Next-to-Ldg genJet, phi"         , 100, -3.1416, +3.1416);
  h_GenJet_NNNLdg_Phi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GenJet_NNNLdg_Phi", "Next-to-Next-to-Next-to-Ldg genJet, phi" , 100, -3.1416, +3.1416);

  return;
}

void Kinematics::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}


void Kinematics::process(Long64_t entry) {

  if ( !fEvent.isMC() ) return;
  
  // Create MCools object
  MCTools mcTools(fEvent);
  
  // Increment Counter
  cAllEvents.increment();
  
  // Define the table
  Table table("Evt | Index | PdgId | Status | Charge | Pt | Eta | Phi | E | Vertex (mm) | Mom | Daus (Index)", "Text"); //LaTeX or Text
  // Table table("Evt | Index | PdgId | Status | Charge | Pt | Eta | Phi | E | Vertex (mm) | d0 (mm) | Lxy (mm) | Mom | Daus (Index)", "Text"); //LaTeX or Text
 
 
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

  
  int row      = 0;
  bool bWToLNu = false;
  // For-loop: GenParticles
  for (int genP_index=0; genP_index < fEvent.genparticles().getGenParticles().size(); genP_index++) {

    // Create the genParticles
    genParticle p = fEvent.genparticles().getGenParticles()[genP_index];
    genParticle m;
    genParticle g;

    // Particle properties
    int genP_pdgId       = p.pdgId();
    int genP_status      = p.status();

    // Consider only status=22 (intermediate) or status=23 (outgoing) particles
    if( (genP_status != 22) && (genP_status != 23) )continue;

    // Other Particle properties
    double genP_pt       = p.pt();
    double genP_eta      = p.eta();
    double genP_phi      = p.phi();
    double genP_energy   = p.e();
    int genP_charge      = p.charge();
    double genP_vtxX     = p.vtxX()*10; // in mm
    double genP_vtxY     = p.vtxY()*10; // in mm
    double genP_vtxZ     = p.vtxZ()*10; // in mm
    // double genP_d0       = mcTools.GetD0Mag(genP_index, false); // in mm
    // double genP_Lxy      = mcTools.GetLxy(genP_index, false); // in mm
    // math::XYZTLorentzVector genP_p4;
    // genP_p4              = p.p4();    
    // TLorentzVector genP_p4Vis  = mcTools.GetVisibleP4(genP_index);
    
    // Daughter properties
    std::vector<int> genP_daughters_index    = mcTools.GetDaughters(genP_index, false);
    // std::vector<int> genP_daughters_pdgId    = mcTools.GetDaughters(genP_index, true);
    // std::vector<int> genP_allDaughters_index = mcTools.GetAllDaughters(genP_index, false);
    // std::vector<int> genP_allDaughters_pdgId = mcTools.GetAllDaughters(genP_index, true);  
    
    // Mom and Grand-mom properties    
    int genMom_index     = p.mother();
    int genMom_pdgId     = 0;
    int genGmom_index    = -1;
    if (genMom_index >= 0)
      {
	// Mom
	m = fEvent.genparticles().getGenParticles()[genMom_index];
	genMom_pdgId  = m.pdgId();

	// Grand-mom
	genGmom_index = m.mother();
	g = fEvent.genparticles().getGenParticles()[genGmom_index];
      } 

    // Print genParticle properties or  decay tree ?
    // mcTools.PrintGenParticle(genP_index);
    // mcTools.PrintDaughters(genP_index, false);
    // mcTools.PrintDaughters(genP_index, true);


    // Add table rows
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
    // table.AddRowColumn(row, auxTools.ToString(genP_d0,  3)     );
    // table.AddRowColumn(row, auxTools.ToString(genP_Lxy, 3)     );
    table.AddRowColumn(row, auxTools.ToString(genMom_index)    );
    table.AddRowColumn(row, auxTools.ConvertIntVectorToString(genP_daughters_index) );
    row++;
	       
    
    // The following code was written based on these particles. Where needed their daughters are used
    // or if they decay to themselves their final versions are used
    // ========================================================================================================
    // Evt | Index | PdgId | Status | Pt   | Eta    | Phi     | Mom | Comments
    // ===================================================================================================
    // 0   | 4     | 37    | 22     | 378  | 0.8825 | 2.5     | 2   | H+
    // 0   | 5     | 5     | 23     | 34.4 | -1.935 | -3.08   | 2   | b flavour-excited
    // 0   | 6     | -6    | 22     | 321  | 1.783  | -0.72   | 2   | tbar associated
    // 0   | 7     | 2     | 23     | 96.9 | 1.624  | -0.128  | 2   | u spectator quark
    // 0   | 39    | 6     | 22     | 281  | 0.8383 | 2.27    | 34  | H->tb, t
    // 0   | 40    | -5    | 23     | 47.1 | 0.1406 | 2.3     | 34  | H->tb, bbar
    // 0   | 41    | -24   | 22     | 209  | 1.694  | -0.805  | 36  | g->tt, t->Wb, W-
    // 0   | 42    | -5    | 23     | 167  | 1.675  | -0.0675 | 36  | g->tt, t->Wb, bbar
    // 0   | 46    | 24    | 22     | 180  | 0.5437 | 1.98    | 39  | H->tb, t->Wb, W+
    // 0   | 47    | 5     | 23     | 120  | 1.105  | 2.71    | 39  | H->tb, t->Wb, b
    // 0   | 53    | 13    | 23     | 174  | 1.808  | -0.782  | 44  | g->tt, t->Wb, W->mu v_mu, m
    // 0   | 54    | -14   | 23     | 34.8 | 0.8297 | -0.913  | 44  | g->tt, t->Wb, W->mu v_mu, v_mu
    // 0   | 58    | -1    | 23     | 99   | 0.8182 | 2.26    | 49  | H->tb, t->Wb, W->qqbar, qbar
    // 0   | 59    | 2     | 23     | 72.7 | 0.1424 | 1.66    | 49  | H->tb, t->Wb, W->qqbar, q
    // ========================================================================================================
    
    // If particle decays to itself, get the last in the chain
    int fs_index   = mcTools.GetFinalSelf(genP_index);
    genParticle fs = fEvent.genparticles().getGenParticles()[fs_index];

    
    // B-quarks
    if(std::abs(genP_pdgId) == 5)
      {
	
	if ( mcTools.HasMother(genP_index, 37, true) ) // Has H+ mother
	  {
	    if (std::abs(genMom_pdgId) == 6) // Has top immediate mother
	      {
		// H+->tb, t->bW, b (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible! Also t->Zc and t->Zu)
		cHtb_tbW_BQuark.increment();
		Htb_tbW_BQuark_p4    = fs.p4();
		Htb_tbW_BQuark_index = fs_index;
	      }
	    else if (std::abs(genMom_pdgId) == 37) // Has top immediate mother
	      {
		// H+->tb, b
		cHtb_BQuark.increment();
		Htb_BQuark_p4    = fs.p4();
		Htb_BQuark_index = fs_index;
	      }
	    else
	      {
		// throw hplus::Exception("Logic") << "Kinematics::process() B-quark whose origins are not accounted for. Need to rethink this.";
	      }
	    
	  }// Has H+ mother
	else
	  {
	    
	    if ( (std::abs(genMom_pdgId) == 21) || (g.pdgId() == 2212) ) // Has glu immediate mother OR p grandmother
	      {
		// g->bb, b (flavour-excited )	       
		cgbb_BQuark.increment();
		gbb_BQuark_p4    = fs.p4();
		gbb_BQuark_index = fs_index;

	      }
	    else if (std::abs(genMom_pdgId) == 6) // Has top immediate mother
	      {
		// g->tt, t->bW, b (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
		cgtt_tbW_BQuark.increment();
		gtt_tbW_BQuark_p4    = fs.p4();
		gtt_tbW_BQuark_index = fs_index;

	      }
	    else if (mcTools.HasMother(genP_index, 4,  true) ) // Rare events (~1 in 1000)
	      {
		// g->bb, b (flavour-excited )
		cgbb_BQuark.increment();
		gbb_BQuark_p4    = fs.p4();
		gbb_BQuark_index = fs_index;
	      }
	    else
	      {	      
		// throw hplus::Exception("Logic") << "Kinematics::process() B-quark whose origins are not accounted for. Need to rethink this.";
	      }
	  }
	
      }// B-quarks
    else if(std::abs(genP_pdgId) == 6) // T-Quarks
      {
	
	if (std::abs(genMom_pdgId) == 37) // Has H+ mother
	  {
	    // H+->tb (From HPlus decay)
	    cHtb_TQuark.increment();
	    Htb_TQuark_p4    = fs.p4();
	    Htb_TQuark_index = fs_index;
      	  }
	else if ( (std::abs(genMom_pdgId) == 21) || (g.pdgId() == 2212) ) // Has glu immediate mother OR p grandmother
	  {	     
	    // g->tt (Associated top)
	    cgtt_TQuark.increment();
	    gtt_TQuark_p4    = fs.p4();
	    gtt_TQuark_index = fs_index; 
	  }
	else if (mcTools.HasMother(genP_index, 4,  true) ) // Rare events (~1 in 1000)
	  {
	    // g->tt (Associated top)
	    cgtt_TQuark.increment();
	    gtt_TQuark_p4    = fs.p4();
	    gtt_TQuark_index = fs_index;
	  }
	else
	  {
	    // throw hplus::Exception("Logic") << "Kinematics::process() Top quark whose origins are not accounted for. Need to rethink this.";
	  }
	
      }// T-Quarks
    else if(std::abs(genP_pdgId) == 37) //HPlus
      {

	// tb->H+, H+
	cHtb_HPlus.increment();

	Htb_HPlus_p4    = fs.p4();
	Htb_HPlus_index = fs_index;

      } // HPlus
    else if(std::abs(genP_pdgId) == 24) //W-bosons
      {
	
	if (mcTools.HasMother(genP_index, 37, true)) // Has H+ mother
	  {
	    // H+->tb, t->bW, W-boson (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
	    cHtb_tbW_WBoson.increment();
	    Htb_tbW_WBoson_p4    = fs.p4();
	    Htb_tbW_WBoson_index = fs_index;

	    // H+->tb, t->bW, W->qq (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
	    std::vector<int> daughters = mcTools.GetDaughters(fs_index, false);
	    
	    // For-loop: All daughters
	    for (unsigned short i = 0; i < daughters.size(); i++){

	      int dau_index = daughters.at(i);
	      genParticle d = fEvent.genparticles().getGenParticles()[dau_index];

	      if( mcTools.IsQuark(d.pdgId()) )
		{	
		  if (d.pdgId() > 0)
		    {
		      // Quarks
		      cHtb_tbW_Wqq_Quark.increment();
		      Htb_tbW_Wqq_Quark_p4    = d.p4();
		      Htb_tbW_Wqq_Quark_index = dau_index;
		    }
		  else
		    {
		      // Anti-Quarks
		      cHtb_tbW_Wqq_AntiQuark.increment();
		      Htb_tbW_Wqq_AntiQuark_p4    = d.p4();
		      Htb_tbW_Wqq_AntiQuark_index = dau_index;
		    }
		}
	      else if( mcTools.IsLepton(d.pdgId() ) )
		{
		  // H+->tb, t->bW, W->l v (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
		  cHtb_tbW_Wqq_Leptons.increment();
		  bWToLNu = true;
		  break;
		}
	      else
		{
		  throw hplus::Exception("Logic") << "Kinematics::process() W daughters whose origins are not accounted for. Need to rethink this.";
		}
	    } // For-loop: All daughters
	  } // Has H+ mother
	else
	  {
	    // g->tt, t->bW, W-boson (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
	    cgtt_tbW_WBoson.increment();
	    gtt_tbW_WBoson_p4    = fs.p4();
	    gtt_tbW_WBoson_index = fs_index;


	    // g->tt, t->bWH, t->bW, W->qq (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
	    std::vector<int> daughters = mcTools.GetDaughters(fs_index, false);

	    // For-loop: All daughters
	    for (unsigned short i = 0; i < daughters.size(); i++){
	      
	      int dau_index = daughters.at(i);
	      genParticle d = fEvent.genparticles().getGenParticles()[dau_index];
	      
	      if( mcTools.IsQuark(d.pdgId() ) )
	      {
		if (d.pdgId() > 0)
		  {
		    // Quarks
		    cgtt_tbW_Wqq_Quark.increment();
		    gtt_tbW_Wqq_Quark_p4    = d.p4();
		    gtt_tbW_Wqq_Quark_index = dau_index;
		  }	       
		else
		  {
		    // AntiQuarks
		    cgtt_tbW_Wqq_AntiQuark.increment();
		    gtt_tbW_Wqq_AntiQuark_p4    = d.p4();
		    gtt_tbW_Wqq_AntiQuark_index = dau_index;
		  }
	      }
	      else if( mcTools.IsLepton(d.pdgId() ) )
		{
		  // g->tt, t->bWH, t->bW, W->l v (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
		  cgtt_tbW_Wqq_Leptons.increment();
		  bWToLNu = true;
		  break;
		}
	      else
		{
		  throw hplus::Exception("Logic") << "Kinematics::process() W daughters whose origins are not accounted for. Need to rethink this.";
		}
	    }// For-loop: All daughters
	  }
	
      }//W-Bosons
    else
      {
	// throw hplus::Exception("Logic") << "Kinematics::process()";
      }    

    // Veto events with leptons from t-bW, W->l v decays
    if (bWToLNu) return;
    
  }//for-loop: genParticles


  // Declare genJet related variables
  std::vector<math::XYZTLorentzVector> v_selJets_p4;
  int nJets      = 0;
  int nSelJets   = 0;
  int iJet       = 0;
  double genJ_HT = 0.0;

  // For-loop: GenJets
  for(GenJet j: fEvent.genjets()) {
    iJet++;
    nJets++;

    math::XYZTLorentzVector genJ_p4;
    genJ_p4 = j.p4();
    double genJ_pt     = j.pt();
    double genJ_eta    = j.eta();
    double genJ_phi    = j.phi();
    // double genJ_pdgId  = j.pdgId();

    // Apply jet acceptance cuts
    if ( (genJ_pt < 30) || (std::abs(genJ_eta) > 2.4) ) continue;

    // Count the selected jets
    nSelJets++;

    // Save the the p4
    v_selJets_p4.push_back( genJ_p4 );
    
    // Calculate HT
    genJ_HT += genJ_pt;
    
    if (iJet==1)
      {
	h_GenJet_Ldg_Pt -> Fill( genJ_pt  );
	h_GenJet_Ldg_Eta-> Fill( genJ_eta );
	h_GenJet_Ldg_Phi-> Fill( genJ_phi );
      }
    else if (iJet==2)
      {
	h_GenJet_NLdg_Pt -> Fill( genJ_pt  );
	h_GenJet_NLdg_Eta-> Fill( genJ_eta );
	h_GenJet_NLdg_Phi-> Fill( genJ_phi );
      }
    else if (iJet==3)
      {
	h_GenJet_NNLdg_Pt -> Fill( genJ_pt  );
	h_GenJet_NNLdg_Eta-> Fill( genJ_eta );
	h_GenJet_NNLdg_Phi-> Fill( genJ_phi );
      }
    else if (iJet==4)
      {
	h_GenJet_NNNLdg_Pt -> Fill( genJ_pt  );
	h_GenJet_NNNLdg_Eta-> Fill( genJ_eta );
	h_GenJet_NNNLdg_Phi-> Fill( genJ_phi );
      }
    else{}
    
  }

  
  // Event-based variables
  double genP_HT = Htb_BQuark_p4.pt() + Htb_tbW_BQuark_p4.pt() + Htb_tbW_Wqq_Quark_p4.pt() + Htb_tbW_Wqq_AntiQuark_p4.pt() + gbb_BQuark_p4.pt()
    + gtt_tbW_Wqq_Quark_p4.pt() + gtt_tbW_Wqq_AntiQuark_p4.pt() + gtt_tbW_BQuark_p4.pt();

  math::XYZTLorentzVector ldgDijets_p4;
  std::vector<math::XYZTLorentzVector> v_dijet_p4;
  std::vector<double> v_dijet_masses;
  std::vector<double> v_dijet_dR;
  double maxDijetMass_mass;
  math::XYZTLorentzVector maxDijetMass_p4;
  double maxDijetMass_dR;
  double maxDijetMass_rapidity;
  
  // For-loop: Selected jets p4
  if (v_selJets_p4.size() > 1) {

    // Calculate the mass of the two ldg jets
    ldgDijets_p4 = v_selJets_p4.at(0) + v_selJets_p4.at(1);

    // For-loop:  
    for (int i=0; i < v_selJets_p4.size()-1; i++)
      {
	for (int j=i+1; j < v_selJets_p4.size(); j++)
	  {
	    math::XYZTLorentzVector p4 = ( v_selJets_p4.at(i) + v_selJets_p4.at(j) );
	    v_dijet_p4.push_back( p4 );
	    v_dijet_masses.push_back( p4.mass() );
	    v_dijet_dR.push_back( ROOT::Math::VectorUtil::DeltaR(v_selJets_p4.at(i), v_selJets_p4.at(j) ) );
	  }
      }

    int maxDijetMass_pos = std::max_element(v_dijet_masses.begin(), v_dijet_masses.end()) - v_dijet_masses.begin();
    // maxDijetMass_mass    = *std::max_element(v_dijet_masses.begin(), v_dijet_masses.end());
    maxDijetMass_mass     = v_dijet_masses.at(maxDijetMass_pos);
    maxDijetMass_p4       = v_dijet_p4.at(maxDijetMass_pos);
    maxDijetMass_dR       = v_dijet_dR.at(maxDijetMass_pos);

    // rapidity =  0.5log((E+pz)/(E-pz))
    maxDijetMass_rapidity = 0.5*log( (maxDijetMass_p4.e() + maxDijetMass_p4.pz()) / (maxDijetMass_p4.e() - maxDijetMass_p4.pz()) );
  }

  // Event-based histograms
  h_genMET_Et  ->Fill(fEvent.genMET().et()); 
  h_genMET_Phi ->Fill(fEvent.genMET().Phi());

  h_GenJet_Multiplicity    ->Fill(nJets);
  h_SelGenJet_Multiplicity ->Fill(nSelJets);
  h_SelGenJet_LdgDiJet_Mass->Fill( ldgDijets_p4.mass()   );
  
  h_SelGenJet_MaxDiJetMass_Mass    ->Fill( maxDijetMass_mass     );
  h_SelGenJet_MaxDiJetMass_Pt      ->Fill( maxDijetMass_p4.pt()  );
  h_SelGenJet_MaxDiJetMass_Eta     ->Fill( maxDijetMass_p4.eta() );
  h_SelGenJet_MaxDiJetMass_Rapidity->Fill( maxDijetMass_rapidity );
  h_SelGenJet_MaxDiJetMass_dR      ->Fill( maxDijetMass_dR       );

  
  // Calculate HT
  h_genHT_GenParticles->Fill(genP_HT);
  h_genHT_GenJets->Fill(genJ_HT);
  
  
  // Print the table with genP info
  if (cfg_Verbose) table.Print();
  
  // H+->tb, t->bW, b (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible! Also t->Zc and t->Zu)
  h_tbH_tbW_BQuark_Pt ->Fill( Htb_tbW_BQuark_p4.pt()  );
  h_tbH_tbW_BQuark_Eta->Fill( Htb_tbW_BQuark_p4.eta() );
  h_tbH_tbW_BQuark_Phi->Fill( Htb_tbW_BQuark_p4.phi() );

  // H+->tb, b
  h_tbH_BQuark_Pt ->Fill( Htb_BQuark_p4.pt()  );
  h_tbH_BQuark_Eta->Fill( Htb_BQuark_p4.eta() );
  h_tbH_BQuark_Phi->Fill( Htb_BQuark_p4.phi() );

  // g->bb, b (flavour-excited )	       
  h_gbb_BQuark_Pt ->Fill( gbb_BQuark_p4.pt()  );
  h_gbb_BQuark_Eta->Fill( gbb_BQuark_p4.eta() );
  h_gbb_BQuark_Phi->Fill( gbb_BQuark_p4.phi() );

  // g->tt, t->bW, b (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
  h_gtt_tbW_BQuark_Pt ->Fill( gtt_tbW_BQuark_p4.pt()  ); 
  h_gtt_tbW_BQuark_Eta->Fill( gtt_tbW_BQuark_p4.eta() );
  h_gtt_tbW_BQuark_Phi->Fill( gtt_tbW_BQuark_p4.phi() );
  
  // g->bb, b (flavour-excited ) - rare events (~1 in 1000)
  h_gbb_BQuark_Pt ->Fill( gbb_BQuark_p4.pt()  );
  h_gbb_BQuark_Eta->Fill( gbb_BQuark_p4.eta() );
  h_gbb_BQuark_Phi->Fill( gbb_BQuark_p4.phi() );
  
  // H+->tb (From HPlus decay)
  h_tbH_TQuark_Pt ->Fill( Htb_TQuark_p4.pt()) ;
  h_tbH_TQuark_Eta->Fill( Htb_TQuark_p4.eta() );
  h_tbH_TQuark_Phi->Fill( Htb_TQuark_p4.phi() );

  // g->tt (Associated top)
  h_gtt_TQuark_Pt ->Fill( gtt_TQuark_p4.pt()  );
  h_gtt_TQuark_Eta->Fill( gtt_TQuark_p4.eta() );
  h_gtt_TQuark_Phi->Fill( gtt_TQuark_p4.phi() );
  
  // tb->H+, H+
  h_tbH_HPlus_Pt ->Fill( Htb_HPlus_p4.pt()  );
  h_tbH_HPlus_Eta->Fill( Htb_HPlus_p4.eta() );
  h_tbH_HPlus_Phi->Fill( Htb_HPlus_p4.phi() );
  
  // H+->tb, t->bW, W-boson (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
  h_tbH_tbW_WBoson_Pt ->Fill( Htb_tbW_WBoson_p4.pt()  );
  h_tbH_tbW_WBoson_Eta->Fill( Htb_tbW_WBoson_p4.eta() );
  h_tbH_tbW_WBoson_Phi->Fill( Htb_tbW_WBoson_p4.phi() );

  // H+->tb, t->bW, W-boson, Quark
  h_Htb_tbW_Wqq_Quark_Pt ->Fill( Htb_tbW_Wqq_Quark_p4.pt()  );
  h_Htb_tbW_Wqq_Quark_Eta->Fill( Htb_tbW_Wqq_Quark_p4.eta() );
  h_Htb_tbW_Wqq_Quark_Phi->Fill( Htb_tbW_Wqq_Quark_p4.phi() );

  // H+->tb, t->bW, W-boson, AntiQuark
  h_Htb_tbW_Wqq_AntiQuark_Pt ->Fill( Htb_tbW_Wqq_AntiQuark_p4.pt()  );
  h_Htb_tbW_Wqq_AntiQuark_Eta->Fill( Htb_tbW_Wqq_AntiQuark_p4.eta() );
  h_Htb_tbW_Wqq_AntiQuark_Phi->Fill( Htb_tbW_Wqq_AntiQuark_p4.phi() );

  // g->tt, t->bW, W-boson (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
  h_gtt_tbW_WBoson_Pt ->Fill( gtt_tbW_WBoson_p4.pt()  );
  h_gtt_tbW_WBoson_Eta->Fill( gtt_tbW_WBoson_p4.eta() );
  h_gtt_tbW_WBoson_Phi->Fill( gtt_tbW_WBoson_p4.phi() );

  // g->tt, t->bW, W->qq, Quark
  h_gtt_tbW_Wqq_Quark_Pt ->Fill( gtt_tbW_Wqq_Quark_p4.pt()  );
  h_gtt_tbW_Wqq_Quark_Eta->Fill( gtt_tbW_Wqq_Quark_p4.eta() );
  h_gtt_tbW_Wqq_Quark_Phi->Fill( gtt_tbW_Wqq_Quark_p4.phi() );

  // g->tt, t->bW, W->qq, AntiQuark
  h_gtt_tbW_Wqq_AntiQuark_Pt ->Fill( gtt_tbW_Wqq_AntiQuark_p4.pt()  );
  h_gtt_tbW_Wqq_AntiQuark_Eta->Fill( gtt_tbW_Wqq_AntiQuark_p4.eta() );
  h_gtt_tbW_Wqq_AntiQuark_Phi->Fill( gtt_tbW_Wqq_AntiQuark_p4.phi() );

 
  // H+->tb, t->bW, W->qq
  double dR_Htb_TQuark_Htb_BQuark            = ROOT::Math::VectorUtil::DeltaR(Htb_TQuark_p4, Htb_BQuark_p4);
  double dR_Htb_TQuark_gtt_TQuark            = ROOT::Math::VectorUtil::DeltaR(Htb_TQuark_p4, gtt_TQuark_p4);
  double dR_Htb_TQuark_gbb_BQuark            = ROOT::Math::VectorUtil::DeltaR(Htb_TQuark_p4, gbb_BQuark_p4);
  double dR_Htb_BQuark_Htb_tbW_BQuark        = ROOT::Math::VectorUtil::DeltaR(Htb_BQuark_p4, Htb_tbW_BQuark_p4);
  double dR_Htb_BQuark_Htb_tbW_Wqq_Quark     = ROOT::Math::VectorUtil::DeltaR(Htb_BQuark_p4, Htb_tbW_Wqq_Quark_p4);
  double dR_Htb_BQuark_Htb_tbW_Wqq_AntiQuark = ROOT::Math::VectorUtil::DeltaR(Htb_BQuark_p4, Htb_tbW_Wqq_AntiQuark_p4);
  
  // Associated products
  double dR_gtt_TQuark_gbb_BQuark                = ROOT::Math::VectorUtil::DeltaR(gtt_TQuark_p4, gbb_BQuark_p4);
  double dR_gtt_TQuark_gtt_tbW_BQuark            = ROOT::Math::VectorUtil::DeltaR(gtt_TQuark_p4, gtt_tbW_BQuark_p4); 
  double dR_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark     = ROOT::Math::VectorUtil::DeltaR(gtt_tbW_BQuark_p4, gtt_tbW_Wqq_Quark_p4);
  double dR_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark = ROOT::Math::VectorUtil::DeltaR(gtt_tbW_BQuark_p4, gtt_tbW_Wqq_AntiQuark_p4);

  // Fill dR histos
  h_Htb_TQuark_Htb_BQuark_dR                ->Fill(dR_Htb_TQuark_Htb_BQuark);
  h_Htb_TQuark_gtt_TQuark_dR                ->Fill(dR_Htb_TQuark_gtt_TQuark);
  h_Htb_TQuark_gbb_BQuark_dR                ->Fill(dR_Htb_TQuark_gbb_BQuark);
  h_Htb_BQuark_Htb_tbW_BQuark_dR            ->Fill(dR_Htb_BQuark_Htb_tbW_BQuark);
  h_Htb_BQuark_Htb_tbW_Wqq_Quark_dR         ->Fill(dR_Htb_BQuark_Htb_tbW_Wqq_Quark);
  h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dR     ->Fill(dR_Htb_BQuark_Htb_tbW_Wqq_AntiQuark);
  h_gtt_TQuark_gbb_BQuark_dR                ->Fill(dR_gtt_TQuark_gbb_BQuark);
  h_gtt_TQuark_gtt_tbW_BQuark_dR            ->Fill(dR_gtt_TQuark_gtt_tbW_BQuark);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dR     ->Fill(dR_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dR ->Fill(dR_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark);

  
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

  // For-loop: All (pT-sorted) b-quarks
  for (int i = 0; i < bQuarks_p4.size(); i++)
    {
      if (i==0)
	{
	  h_BQuark_Ldg_Pt ->Fill( bQuarks_p4.at(i).pt()  );
	  h_BQuark_Ldg_Eta->Fill( bQuarks_p4.at(i).eta() );
	  h_BQuark_Ldg_Phi->Fill( bQuarks_p4.at(i).phi() );
	}
      else if (i==1)
	{
	  h_BQuark_NLdg_Pt ->Fill( bQuarks_p4.at(i).pt()  );
	  h_BQuark_NLdg_Eta->Fill( bQuarks_p4.at(i).eta() );
	  h_BQuark_NLdg_Phi->Fill( bQuarks_p4.at(i).phi() );
	}
      else if (i==2)
	{
	  h_BQuark_NNLdg_Pt ->Fill( bQuarks_p4.at(i).pt()  );
	  h_BQuark_NNLdg_Eta->Fill( bQuarks_p4.at(i).eta() );
	  h_BQuark_NNLdg_Phi->Fill( bQuarks_p4.at(i).phi() );
	}
      else if (i==3)
	{
	  h_BQuark_NNNLdg_Pt ->Fill( bQuarks_p4.at(i).pt()  );
	  h_BQuark_NNNLdg_Eta->Fill( bQuarks_p4.at(i).eta() );
	  h_BQuark_NNNLdg_Phi->Fill( bQuarks_p4.at(i).phi() );
	}
      else{}
    } // For-loop: All (pT-sorted) b-quarks
  
  return;
}
