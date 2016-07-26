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

class GenParticleKinematics: public BaseSelector {
public:
  explicit GenParticleKinematics(const ParameterSet& config, const TH1* skimCounters);
  virtual ~GenParticleKinematics() {}

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

  WrappedTH1 *h_gtt_TQuark_Pt;
  WrappedTH1 *h_gtt_tbW_WBoson_Pt;
  WrappedTH1 *h_gtt_tbW_BQuark_Pt;
  WrappedTH1 *h_tbH_HPlus_Pt;
  WrappedTH1 *h_tbH_TQuark_Pt;
  WrappedTH1 *h_tbH_BQuark_Pt;
  WrappedTH1 *h_tbH_tbW_WBoson_Pt;
  WrappedTH1 *h_tbH_tbW_BQuark_Pt;
  WrappedTH1 *h_gbb_BQuark_Pt;

  WrappedTH1 *h_gtt_TQuark_Eta;
  WrappedTH1 *h_gtt_tbW_WBoson_Eta;
  WrappedTH1 *h_gtt_tbW_BQuark_Eta;
  WrappedTH1 *h_tbH_HPlus_Eta;
  WrappedTH1 *h_tbH_TQuark_Eta;
  WrappedTH1 *h_tbH_BQuark_Eta;
  WrappedTH1 *h_tbH_tbW_WBoson_Eta;
  WrappedTH1 *h_tbH_tbW_BQuark_Eta;
  WrappedTH1 *h_gbb_BQuark_Eta;

  WrappedTH1 *h_gtt_TQuark_Phi;
  WrappedTH1 *h_gtt_tbW_WBoson_Phi;
  WrappedTH1 *h_gtt_tbW_BQuark_Phi;
  WrappedTH1 *h_tbH_HPlus_Phi;
  WrappedTH1 *h_tbH_TQuark_Phi;
  WrappedTH1 *h_tbH_BQuark_Phi;
  WrappedTH1 *h_tbH_tbW_WBoson_Phi;
  WrappedTH1 *h_tbH_tbW_BQuark_Phi;
  WrappedTH1 *h_gbb_BQuark_Phi;

  WrappedTH1 *h_gtt_TQuark_Status;
  WrappedTH1 *h_gtt_tbW_WBoson_Status;
  WrappedTH1 *h_gtt_tbW_BQuark_Status;
  WrappedTH1 *h_tbH_HPlus_Status;
  WrappedTH1 *h_tbH_TQuark_Status;
  WrappedTH1 *h_tbH_BQuark_Status;
  WrappedTH1 *h_tbH_tbW_WBoson_Status;
  WrappedTH1 *h_tbH_tbW_BQuark_Status;
  WrappedTH1 *h_gbb_BQuark_Status;

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

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(GenParticleKinematics);

GenParticleKinematics::GenParticleKinematics(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    cfg_Verbose(config.getParameter<bool>("Verbose")),
    cfg_TopQuark_Pt(config.getParameter<double>("TopQuark_Pt")),
    cfg_TopQuark_Eta(config.getParameter<double>("TopQuark_Eta")),  
    cAllEvents(fEventCounter.addCounter("All events")),
    // cTrigger(fEventCounter.addCounter("Passed trigger")),
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

void GenParticleKinematics::book(TDirectory *dir) {

  // Book histograms
  h_genMET_Et         =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genMET_Et" , "gen MET Et" , 100,  0.0   , 500.0);
  h_genMET_Phi        =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genMET_Phi", "gen MET Phi", 100, -3.1416,  +3.1416);

  h_gtt_TQuark_Pt     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_TQuark_Pt"    , "gtt, t-quark pT"     , 100, 0.0, 500.0);
  h_gtt_tbW_WBoson_Pt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_WBoson_Pt", "gtt, tWb W-boson pT" , 100, 0.0, 500.0);
  h_gtt_tbW_BQuark_Pt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_BQuark_Pt", "gtt, tWb b-quark pT" , 100, 0.0, 500.0);
  h_tbH_HPlus_Pt      =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_HPlus_Pt"     , "tbH, HPlus pT"       , 100, 0.0, 500.0);
  h_tbH_TQuark_Pt     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_TQuark_Pt"    , "tbH, t-quark pT"     , 100, 0.0, 500.0);
  h_tbH_BQuark_Pt     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_BQuark_Pt"    , "tbH, b-quark pT"     , 100, 0.0, 500.0);
  h_tbH_tbW_WBoson_Pt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_tbW_WBoson_Pt", "tbH, tbW, W-boson pT", 100, 0.0, 500.0);
  h_tbH_tbW_BQuark_Pt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_tbW_BQuark_Pt", "tbH, tbW, b-quark pT", 100, 0.0, 500.0);
  h_gbb_BQuark_Pt     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gbb_BQuark_Pt"    , "gtt, b-quark pT, "   , 100, 0.0, 500.0);

  h_gtt_TQuark_Eta     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_TQuark_Eta"    , "gtt, t-quark pT"     , 50, -2.5, +2.5);
  h_gtt_tbW_WBoson_Eta =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_WBoson_Eta", "gtt, tWb W-boson pT" , 50, -2.5, +2.5);
  h_gtt_tbW_BQuark_Eta =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_BQuark_Eta", "gtt, tWb b-quark pT" , 50, -2.5, +2.5);
  h_tbH_HPlus_Eta      =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_HPlus_Eta"     , "tbH, HPlus pT"       , 50, -2.5, +2.5);
  h_tbH_TQuark_Eta     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_TQuark_Eta"    , "tbH, t-quark pT"     , 50, -2.5, +2.5);
  h_tbH_BQuark_Eta     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_BQuark_Eta"    , "tbH, b-quark pT"     , 50, -2.5, +2.5);
  h_tbH_tbW_WBoson_Eta =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_tbW_WBoson_Eta", "tbH, tbW, W-boson pT", 50, -2.5, +2.5);
  h_tbH_tbW_BQuark_Eta =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_tbW_BQuark_Eta", "tbH, tbW, b-quark pT", 50, -2.5, +2.5);
  h_gbb_BQuark_Eta     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gbb_BQuark_Eta"    , "gtt, b-quark pT, "   , 50, -2.5, +2.5);

  h_gtt_TQuark_Phi     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gtt_TQuark_Phi"    , "gtt, t-quark pT"     , 100, -3.1416, +3.1416);
  h_gtt_tbW_WBoson_Phi =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gtt_tbW_WBoson_Phi", "gtt, tWb W-boson pT" , 100, -3.1416, +3.1416);
  h_gtt_tbW_BQuark_Phi =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gtt_tbW_BQuark_Phi", "gtt, tWb b-quark pT" , 100, -3.1416, +3.1416);
  h_tbH_HPlus_Phi      =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_HPlus_Phi"     , "tbH, HPlus pT"       , 100, -3.1416, +3.1416);
  h_tbH_TQuark_Phi     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_TQuark_Phi"    , "tbH, t-quark pT"     , 100, -3.1416, +3.1416);
  h_tbH_BQuark_Phi     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_BQuark_Phi"    , "tbH, b-quark pT"     , 100, -3.1416, +3.1416);
  h_tbH_tbW_WBoson_Phi =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_tbW_WBoson_Phi", "tbH, tbW, W-boson pT", 100, -3.1416, +3.1416);
  h_tbH_tbW_BQuark_Phi =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_tbW_BQuark_Phi", "tbH, tbW, b-quark pT", 100, -3.1416, +3.1416);
  h_gbb_BQuark_Phi     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gbb_BQuark_Phi"    , "gtt, b-quark pT, "   , 100, -3.1416, +3.1416);

  h_gtt_TQuark_Status     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gtt_TQuark_Status"    , "gtt, t-quark pT"     , 100, 0.0, +100.0);
  h_gtt_tbW_WBoson_Status =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gtt_tbW_WBoson_Status", "gtt, tWb W-boson pT" , 100, 0.0, +100.0);
  h_gtt_tbW_BQuark_Status =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gtt_tbW_BQuark_Status", "gtt, tWb b-quark pT" , 100, 0.0, +100.0);
  h_tbH_HPlus_Status      =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_HPlus_Status"     , "tbH, HPlus pT"       , 100, 0.0, +100.0);
  h_tbH_TQuark_Status     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_TQuark_Status"    , "tbH, t-quark pT"     , 100, 0.0, +100.0);
  h_tbH_BQuark_Status     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_BQuark_Status"    , "tbH, b-quark pT"     , 100, 0.0, +100.0);
  h_tbH_tbW_WBoson_Status =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_tbW_WBoson_Status", "tbH, tbW, W-boson pT", 100, 0.0, +100.0);
  h_tbH_tbW_BQuark_Status =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_tbW_BQuark_Status", "tbH, tbW, b-quark pT", 100, 0.0, +100.0);
  h_gbb_BQuark_Status     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gbb_BQuark_Status"    , "gtt, b-quark pT, "   , 100, 0.0, +100.0);

  // deltaR
  h_Htb_TQuark_Htb_BQuark_dR                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "Htb_TQuark_Htb_BQuark_dR"               , "dR(t, b)", 100, 0.0, +10.0);
  h_Htb_TQuark_gtt_TQuark_dR                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "Htb_TQuark_gtt_TQuark_dR"               , "dR(t, t)", 100, 0.0, +10.0);
  h_Htb_TQuark_gbb_BQuark_dR                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "Htb_TQuark_gbb_BQuark_dR"               , "dR(t, b)", 100, 0.0, +10.0);
  h_Htb_BQuark_Htb_tbW_BQuark_dR            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "Htb_BQuark_Htb_tbW_BQuark_dR"           , "dR(b, b)", 100, 0.0, +10.0);
  h_Htb_BQuark_Htb_tbW_Wqq_Quark_dR         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "Htb_BQuark_Htb_tbW_Wqq_Quark_dR"        , "dR(b, q)", 100, 0.0, +10.0);
  h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dR     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dR"    , "dR(b, q)", 100, 0.0, +10.0);
  h_gtt_TQuark_gbb_BQuark_dR                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gtt_TQuark_gbb_BQuark_dR"               , "dR(b, b)", 100, 0.0, +10.0);
  h_gtt_TQuark_gtt_tbW_BQuark_dR            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gtt_TQuark_gtt_tbW_BQuark_dR"           , "dR(t, b)", 100, 0.0, +10.0);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dR     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dR"    , "dR(b, q)", 100, 0.0, +10.0);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dR = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dR", "dR(b, q)", 100, 0.0, +10.0);

  // B-quarks
  // h_BQuark_Ldg_Pt   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "BQuark_Ldg_Pt"  , "Ldg b-quark, pT"                 , 100, 0.0, +500.0);
  // h_BQuark_NLdg_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "BQuark_NLdg_Pt" , "Next-to-Ldg b-quark, pT"         , 100, 0.0, +500.0);
  // h_BQuark_NNLdg_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "BQuark_NNLdg_Pt", "Next-to-Next-to-Ldg b-quark, pT" , 100, 0.0, +500.0);
  
  // TDirectory *WDir = dir->mkdir("W");
  // hWTauRtau1Pr0Pizero = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, WDir, "tauRtau1Pr0Pizero", "tauRtau1Pr0Pizero", 60, 0.0, 1.2);
  
  return;
}

void GenParticleKinematics::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}


void GenParticleKinematics::process(Long64_t entry) {


  if ( !fEvent.isMC() ) return;

  // Create MCools object
  MCTools mcTools(fEvent);
  
  // Increment Counter
  cAllEvents.increment();
  
  // Define the table
  Table table("Evt | Index | PdgId | Status | Charge | Pt | Eta | Phi | abs(d0) | Lxy | vX | vY | vZ | Mom | Daus (Index)", "Text"); //LaTeX or Text
  
  // Event-based variables
  h_genMET_Et ->Fill(fEvent.genMET().et());
  h_genMET_Phi->Fill(fEvent.genMET().Phi());
  
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
  

  // For-loop: GenParticles
  // int genP_index = -1;
  // for (auto& p: fEvent.genparticles().getGenParticles()) {
  // genP_index++;

  
  int row=0;
  // For-loop: GenParticles
  for (int genP_index=0; genP_index < fEvent.genparticles().getGenParticles().size(); genP_index++) {

    // Declarations
    genParticle p = fEvent.genparticles().getGenParticles()[genP_index];
    math::XYZTLorentzVector genP_p4;
    genParticle m;
    genParticle g;
    
    // Get genP properties
    genP_p4 = p.p4();
    // TLorentzVector genP_p4Vis  = mcTools.GetVisibleP4(genP_index);    
    int genP_pdgId       = p.pdgId();
    double genP_pt       = p.pt();
    double genP_eta      = p.eta();
    double genP_phi      = p.phi();
    // double genP_energy   = p.e();
    int genP_status      = p.status();
    int genP_charge      = p.charge();
    double genP_vtxX     = p.vtxX();
    double genP_vtxY     = p.vtxY();
    double genP_vtxZ     = p.vtxZ();
      
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
    if (0) mcTools.PrintGenParticle(genP_index);
    if (0) mcTools.PrintDaughters(genP_index, false);
    if (0) mcTools.PrintDaughters(genP_index, true);

        
    // Add table rows
    table.AddRowColumn(row, auxTools.ToString(entry)           );
    table.AddRowColumn(row, auxTools.ToString(genP_index)      );
    table.AddRowColumn(row, auxTools.ToString(genP_pdgId)      );
    table.AddRowColumn(row, auxTools.ToString(genP_status)     );
    table.AddRowColumn(row, auxTools.ToString(genP_charge)     );
    table.AddRowColumn(row, auxTools.ToString(genP_pt , 3)     );
    table.AddRowColumn(row, auxTools.ToString(genP_eta, 4)     );
    table.AddRowColumn(row, auxTools.ToString(genP_phi, 3)     );
    table.AddRowColumn(row, auxTools.ToString( mcTools.GetD0Mag(genP_index, false),3) );
    table.AddRowColumn(row, auxTools.ToString( mcTools.GetLxy(genP_index, false), 3) );
    table.AddRowColumn(row, auxTools.ToString(genP_vtxX, 3)    );
    table.AddRowColumn(row, auxTools.ToString(genP_vtxY, 3)    );
    table.AddRowColumn(row, auxTools.ToString(genP_vtxZ, 3)    );
    table.AddRowColumn(row, auxTools.ToString(genMom_index)    );
    table.AddRowColumn(row, auxTools.ConvertIntVectorToString(genP_daughters_index) );
    row++;


    // Consider only status=22 (intermediate) or status=23 (outgoing) particles
    if( (genP_status != 22) && (genP_status != 23) )continue;

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
       
    // The decay chain
    if (0)
      {
	if (genP_index == 4) mcTools.PrintDaughters(genP_index); // H+
	if (genP_index == 5) mcTools.PrintDaughters(genP_index); // b (flavour-excited)
	if (genP_index == 6) mcTools.PrintDaughters(genP_index); // t (associated)
      }

    // If particle decays to itself, get the last in the chain
    int fs_index   = mcTools.GetFinalSelf(genP_index);
    genParticle fs = fEvent.genparticles().getGenParticles()[fs_index];
    	
    // B-quarks
    if(std::abs(genP_pdgId) == 5)
      {
	
	// Has H+ mother
	if ( mcTools.HasMother(genP_index, 37, true) )
	  {
	    if (std::abs(genMom_pdgId) == 6)
	      {
		if (0) mcTools.PrintGenParticle(fs_index);
		// H+->tb, t->bW, b (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible! Also t->Zc and t->Zu)
		Htb_tbW_BQuark_p4 = fs.p4();
		cHtb_tbW_BQuark.increment();
		h_tbH_tbW_BQuark_Pt ->Fill( fs.p4().pt()  );
		h_tbH_tbW_BQuark_Eta->Fill( fs.p4().eta() );
		h_tbH_tbW_BQuark_Phi->Fill( fs.p4().phi() );
		h_tbH_tbW_BQuark_Status->Fill( fs.status() );
	      }
	    else if (std::abs(genMom_pdgId) == 37)
	      {
		if (0) mcTools.PrintGenParticle(fs_index);
		// H+->tb, b
		Htb_BQuark_p4 = fs.p4();
		cHtb_BQuark.increment();
		h_tbH_BQuark_Pt ->Fill( fs.p4().pt()  );
		h_tbH_BQuark_Eta->Fill( fs.p4().eta() );
		h_tbH_BQuark_Phi->Fill( fs.p4().phi() );
		h_tbH_BQuark_Status->Fill( fs.status() );
	      }
	    else
	      {
		if (0) mcTools.PrintGenParticle(fs_index);
		// throw hplus::Exception("Logic") << "GenParticleKinematics::process() Top quark whose origins are not accounted for. Need to rethink this.";
	      }
	  }// Has H+ mother
	else
	  {	   
	    if ( (std::abs(genMom_pdgId) == 21) || (g.pdgId() == 2212) )
	      {
		if (0) mcTools.PrintGenParticle(fs_index);
		// g->bb, b (flavour-excited )	       
		gbb_BQuark_p4 = fs.p4();
		cgbb_BQuark.increment();
		h_gbb_BQuark_Pt ->Fill( fs.p4().pt()  );
		h_gbb_BQuark_Eta->Fill( fs.p4().eta() );
		h_gbb_BQuark_Phi->Fill( fs.p4().phi() );
		h_gbb_BQuark_Status->Fill( fs.status() );
	      }
	    else if (std::abs(genMom_pdgId) == 6)
	      {
		if (0) mcTools.PrintGenParticle(fs_index);
		// g->tt, t->bW, b (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
		gtt_tbW_BQuark_p4 = fs.p4();
		cgtt_tbW_BQuark.increment();
		h_gtt_tbW_BQuark_Pt ->Fill( fs.p4().pt()  ); 
		h_gtt_tbW_BQuark_Eta->Fill( fs.p4().eta() );
		h_gtt_tbW_BQuark_Phi->Fill( fs.p4().phi() );
		h_gtt_tbW_BQuark_Status->Fill( fs.status() );
	      }
	    else if (mcTools.HasMother(genP_index, 4,  true) )
	      {
		if (0) mcTools.PrintGenParticle(fs_index);
		// g->bb, b (flavour-excited ) - rare events (~1 in 1000)
		gbb_BQuark_p4 = fs.p4();
		cgbb_BQuark.increment();
		h_gbb_BQuark_Pt ->Fill( fs.p4().pt()  );
		h_gbb_BQuark_Eta->Fill( fs.p4().eta() );
		h_gbb_BQuark_Phi->Fill( fs.p4().phi() );
		h_gbb_BQuark_Status->Fill( fs.status() );
	      }
	    else
	      {	      
		// throw hplus::Exception("Logic") << "GenParticleKinematics::process() Top quark whose origins are not accounted for. Need to rethink this.";
	      }
	  }
      }// B-quarks
    else if(std::abs(genP_pdgId) == 6) // T-Quarks
      {
	
	if (std::abs(genMom_pdgId) == 37)
	  {
	    // H+->tb (From HPlus decay)
	    Htb_TQuark_p4 = fs.p4();
	    cHtb_TQuark.increment();
	    h_tbH_TQuark_Pt ->Fill( fs.p4().pt()) ;
	    h_tbH_TQuark_Eta->Fill( fs.p4().eta() );
	    h_tbH_TQuark_Phi->Fill( fs.p4().phi() );
	    h_tbH_TQuark_Status->Fill( fs.status() );
      	  }
	else if ( (std::abs(genMom_pdgId) == 21) || (g.pdgId() == 2212) )
	  {	     
	    // g->tt (Associated top)
	    gtt_TQuark_p4 = fs.p4();
	    cgtt_TQuark.increment();
	    h_gtt_TQuark_Pt ->Fill( fs.p4().pt()  );
	    h_gtt_TQuark_Eta->Fill( fs.p4().eta() );
	    h_gtt_TQuark_Phi->Fill( fs.p4().phi() );
	    h_gtt_TQuark_Status->Fill( fs.status() );
	  }
	else if (mcTools.HasMother(genP_index, 4,  true) )
	  {
	    // g->tt (Associated top) - Rare events
	    gtt_TQuark_p4 = fs.p4();
	    cgtt_TQuark.increment();
	    h_gtt_TQuark_Pt ->Fill( fs.p4().pt()  );
	    h_gtt_TQuark_Eta->Fill( fs.p4().eta() );
	    h_gtt_TQuark_Phi->Fill( fs.p4().phi() );
	    h_gtt_TQuark_Status->Fill( fs.status() );
	  }
	else
	  {
	    // throw hplus::Exception("Logic") << "GenParticleKinematics::process() Top quark whose origins are not accounted for. Need to rethink this.";
	  }
      }// T-Quarks
    else if(std::abs(genP_pdgId) == 37) //HPlus
      {
	// tb->H+, H+
	Htb_HPlus_p4 = fs.p4();
	cHtb_HPlus.increment();
	h_tbH_HPlus_Pt ->Fill( fs.p4().pt()  );
	h_tbH_HPlus_Eta->Fill( fs.p4().eta() );
	h_tbH_HPlus_Phi->Fill( fs.p4().phi() );
	h_tbH_HPlus_Status->Fill( fs.status() );
	
      } // HPlus
    else if(std::abs(genP_pdgId) == 24) //W-bosons
      {
	
	if (mcTools.HasMother(genP_index, 37, true))
	  {
	    if (0) mcTools.PrintGenParticle(genP_index);
	    // H+->tb, t->bW, W-boson (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
	    Htb_tbW_WBoson_p4 = fs.p4();
	    cHtb_tbW_WBoson.increment();
	    h_tbH_tbW_WBoson_Pt ->Fill( fs.p4().pt()  );
	    h_tbH_tbW_WBoson_Eta->Fill( fs.p4().eta() );
	    h_tbH_tbW_WBoson_Phi->Fill( fs.p4().phi() );
	    h_tbH_tbW_WBoson_Status->Fill( fs.status() );
	    
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
		      Htb_tbW_Wqq_Quark_p4 = d.p4();
		    }
		  else
		    {
		      // Anti-Quarks
		      cHtb_tbW_Wqq_AntiQuark.increment();
		      Htb_tbW_Wqq_AntiQuark_p4 = d.p4();
		    }
		}
	      else if( mcTools.IsLepton(d.pdgId() ) )
		{
		  // H+->tb, t->bW, W->l v (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
		  cHtb_tbW_Wqq_Leptons.increment();
		  break;
		}
	      else
		{
		  throw hplus::Exception("Logic") << "GenParticleKinematics::process() W daughters whose origins are not accounted for. Need to rethink this.";
		}
	    }// For-loop: All daughters
	  }
	else
	  {
	    if (0) mcTools.PrintGenParticle(genP_index);
	    // g->tt, t->bW, W-boson (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
	    gtt_tbW_WBoson_p4 = fs.p4();
	    cgtt_tbW_WBoson.increment();
	    h_gtt_tbW_WBoson_Pt ->Fill( fs.p4().pt()  );
	    h_gtt_tbW_WBoson_Eta->Fill( fs.p4().eta() );
	    h_gtt_tbW_WBoson_Phi->Fill( fs.p4().phi() );
	    h_gtt_tbW_WBoson_Status->Fill( fs.status() );

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
		    gtt_tbW_Wqq_Quark_p4 = d.p4();
		  }	       
		else
		  {
		    // AntiQuarks
		    cgtt_tbW_Wqq_AntiQuark.increment();
		    gtt_tbW_Wqq_AntiQuark_p4 = d.p4();
		  }
	      }
	      else if( mcTools.IsLepton(d.pdgId() ) )
		{
		  // g->tt, t->bWH, t->bW, W->l v (NOTE: t->Wb dominant, but t->Ws and t->Wd also possible!)
		  cgtt_tbW_Wqq_Leptons.increment();
		  break;
		}
	      else
		{
		  throw hplus::Exception("Logic") << "GenParticleKinematics::process() W daughters whose origins are not accounted for. Need to rethink this.";
		}
	    }// For-loop: All daughters
	  }
      }//W-Bosons
    else
      {
	// throw hplus::Exception("Logic") << "GenParticleKinematics::process()";
      }    
    
  }//for-loop: genParticles

  // Print the table with genP info
  if (cfg_Verbose) table.Print();
  
  
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
  h_Htb_TQuark_Htb_BQuark_dR                ->Fill( dR_Htb_TQuark_Htb_BQuark);
  h_Htb_TQuark_gtt_TQuark_dR                ->Fill( dR_Htb_TQuark_gtt_TQuark);
  h_Htb_TQuark_gbb_BQuark_dR                ->Fill( dR_Htb_TQuark_gbb_BQuark);
  h_Htb_BQuark_Htb_tbW_BQuark_dR            ->Fill( dR_Htb_BQuark_Htb_tbW_BQuark);
  h_Htb_BQuark_Htb_tbW_Wqq_Quark_dR         ->Fill( dR_Htb_BQuark_Htb_tbW_Wqq_Quark);
  h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dR     ->Fill( dR_Htb_BQuark_Htb_tbW_Wqq_AntiQuark);
  h_gtt_TQuark_gbb_BQuark_dR                ->Fill( dR_gtt_TQuark_gbb_BQuark);
  h_gtt_TQuark_gtt_tbW_BQuark_dR            ->Fill( dR_gtt_TQuark_gtt_tbW_BQuark);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dR     ->Fill( dR_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dR ->Fill( dR_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark);

  // Htb_HPlus_p4;
  // Htb_TQuark_p4;
  // Htb_BQuark_p4;
  // Htb_tbW_WBoson_p4;
  // Htb_tbW_Wqq_Quark_p4;
  // Htb_tbW_Wqq_AntiQuark_p4;
  // gtt_TQuark_p4;
  // gbb_BQuark_p4;
  // gtt_tbW_WBoson_p4;
  // gtt_tbW_BQuark_p4;


  // Apply trigger
  // if (!fEvent.passTriggerDecision()) return;
  // cTrigger.increment();

  return;
}
