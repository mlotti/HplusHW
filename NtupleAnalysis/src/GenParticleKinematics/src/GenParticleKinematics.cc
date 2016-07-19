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
  Count cgtt_TQuark;
  Count cgbb_BQuark;
  Count cgtt_tbW_Wqq_Quark;
  Count cgtt_tbW_Wqq_AntiQuark;
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
  cHtb_tbW_Wqq_Quark(fEventCounter.addCounter("H+->tb, t->bW, q")),
  cHtb_tbW_Wqq_AntiQuark(fEventCounter.addCounter("H+->tb, t->bW, qbar")),
  cgtt_TQuark(fEventCounter.addCounter("g->tt, t")),
  cgbb_BQuark(fEventCounter.addCounter("g->bb, b")),
  cgtt_tbW_Wqq_Quark(fEventCounter.addCounter("g->tt, t->bW, W->qq, q")),
  cgtt_tbW_Wqq_AntiQuark(fEventCounter.addCounter("g->tt, t->bW, W->qq, qbar")),
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
  h_gbb_BQuark_Pt     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,  "gbb_BQuark_Pt"   , "gtt, b-quark pT, "   , 100, 0.0, 500.0);

  h_gtt_TQuark_Eta     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_TQuark_Eta"    , "gtt, t-quark pT"     , 50, -2.5, +2.5);
  h_gtt_tbW_WBoson_Eta =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_WBoson_Eta", "gtt, tWb W-boson pT" , 50, -2.5, +2.5);
  h_gtt_tbW_BQuark_Eta =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_BQuark_Eta", "gtt, tWb b-quark pT" , 50, -2.5, +2.5);
  h_tbH_HPlus_Eta      =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_HPlus_Eta"     , "tbH, HPlus pT"       , 50, -2.5, +2.5);
  h_tbH_TQuark_Eta     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_TQuark_Eta"    , "tbH, t-quark pT"     , 50, -2.5, +2.5);
  h_tbH_BQuark_Eta     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_BQuark_Eta"    , "tbH, b-quark pT"     , 50, -2.5, +2.5);
  h_tbH_tbW_WBoson_Eta =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_tbW_WBoson_Eta", "tbH, tbW, W-boson pT", 50, -2.5, +2.5);
  h_tbH_tbW_BQuark_Eta =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_tbW_BQuark_Eta", "tbH, tbW, b-quark pT", 50, -2.5, +2.5);
  h_gbb_BQuark_Eta     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,  "gbb_BQuark_Eta"   , "gtt, b-quark pT, "   , 50, -2.5, +2.5);

  h_gtt_TQuark_Phi     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gtt_TQuark_Phi"    , "gtt, t-quark pT"     , 100, -3.1416, +3.1416);
  h_gtt_tbW_WBoson_Phi =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gtt_tbW_WBoson_Phi", "gtt, tWb W-boson pT" , 100, -3.1416, +3.1416);
  h_gtt_tbW_BQuark_Phi =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gtt_tbW_BQuark_Phi", "gtt, tWb b-quark pT" , 100, -3.1416, +3.1416);
  h_tbH_HPlus_Phi      =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_HPlus_Phi"     , "tbH, HPlus pT"       , 100, -3.1416, +3.1416);
  h_tbH_TQuark_Phi     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_TQuark_Phi"    , "tbH, t-quark pT"     , 100, -3.1416, +3.1416);
  h_tbH_BQuark_Phi     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_BQuark_Phi"    , "tbH, b-quark pT"     , 100, -3.1416, +3.1416);
  h_tbH_tbW_WBoson_Phi =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_tbW_WBoson_Phi", "tbH, tbW, W-boson pT", 100, -3.1416, +3.1416);
  h_tbH_tbW_BQuark_Phi =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_tbW_BQuark_Phi", "tbH, tbW, b-quark pT", 100, -3.1416, +3.1416);
  h_gbb_BQuark_Phi     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir,  "gbb_BQuark_Phi"   , "gtt, b-quark pT, "   , 100, -3.1416, +3.1416);

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
  MCTools mcTools(fEvent);

  
  // Increment Counter
  cAllEvents.increment();
  
  // Define the table
  Table table_genP("Evt | Index | PdgId | Pt | Eta | Phi | Energy | Mom (Index) | Mom (PdgId) | Daus | Daus (Index)", "Text"); //LaTeX
        
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
 
  int genP_index = -1;
  
  // For-loop: GenParticles
  for (auto& p: fEvent.genparticles().getGenParticles()) {

    genP_index++;
    math::XYZTLorentzVector genP_p4;
    genP_p4 = p.p4();
    int genP_pdgId       = p.pdgId();
    double genP_pt       = p.pt();
    double genP_eta      = p.eta();
    double genP_phi      = p.phi();
    double genP_energy   = p.e();
    int genMom_index     = p.mother();
    int genMom_pdgId     = -999999;
    // TLorentzVector genP_p4Vis       = mcTools.GetVisibleP4(genP_index);   
    std::vector<int> genP_daughters = mcTools.GetDaughters(genP_index, genP_pdgId, true);

    // Print genParticle properties
    if (0) mcTools.PrintGenParticle(genP_index);
    

    // Print daughter tree
    if (0) mcTools.PrintDaughtersRecursively(genP_index);

      
    // Ensure a valid mom exists
    if (genMom_index >= 0){
      const Particle<ParticleCollection<double> > m = fEvent.genparticles().getGenParticles()[genMom_index];
      genMom_pdgId  = m.pdgId();      
    } 

    // Add table rows
    table_genP.AddRowColumn(genP_index, auxTools.ToString(entry, 1)        );
    table_genP.AddRowColumn(genP_index, auxTools.ToString(genP_index)      );
    table_genP.AddRowColumn(genP_index, auxTools.ToString(genP_pdgId, 4)   );
    table_genP.AddRowColumn(genP_index, auxTools.ToString(genP_pt , 3)     );
    table_genP.AddRowColumn(genP_index, auxTools.ToString(genP_eta, 3)     );
    table_genP.AddRowColumn(genP_index, auxTools.ToString(genP_phi, 3)     );
    table_genP.AddRowColumn(genP_index, auxTools.ToString(genP_energy, 4)  );
    table_genP.AddRowColumn(genP_index, auxTools.ToString(genMom_index)    );
    table_genP.AddRowColumn(genP_index, auxTools.ToString(genMom_pdgId)    );
    table_genP.AddRowColumn(genP_index, auxTools.ToString(genP_daughters.size()) );
    table_genP.AddRowColumn(genP_index, auxTools.ConvertIntVectorToString(genP_daughters) );

    // if: Top Quarks
    if( std::abs(genP_pdgId) == 6)
      {	
	
	// g->tt (Associated production)
	if( std::abs(genMom_pdgId) == 21)
	  {
	    cgtt_TQuark.increment();
	    gtt_TQuark_p4 = p.p4();
	    h_gtt_TQuark_Pt ->Fill(genP_pt);
	    h_gtt_TQuark_Eta->Fill(genP_eta);
	    h_gtt_TQuark_Phi->Fill(genP_phi);
	  }

	// H+->tb (From HPlus decay)
	if( std::abs(genMom_pdgId) == 37)
	  {

	    cHtb_TQuark.increment();
	    Htb_TQuark_p4 = p.p4();
	    h_tbH_TQuark_Pt ->Fill(genP_pt);
	    h_tbH_TQuark_Eta->Fill(genP_eta);
	    h_tbH_TQuark_Phi->Fill(genP_phi);
	  }	

      } //if: Top Quarks

    
    // if: Bottom Quarks
    if( std::abs(genP_pdgId) == 5)
      {	
	  
	// g->bb, b (Associated production - Flavour excited b-quark)
	if( std::abs(genMom_pdgId) == 21)
	  {	    
	    cgbb_BQuark.increment();
	    gbb_BQuark_p4 = p.p4();
	    h_gbb_BQuark_Pt ->Fill(genP_pt);
	    h_gbb_BQuark_Eta->Fill(genP_eta);
	    h_gbb_BQuark_Phi->Fill(genP_phi);
	  }

	// H+->tb, b (From HPlus decay)
	if( std::abs(genMom_pdgId) == 37)
	  {
	    cHtb_BQuark.increment();	    
	    Htb_BQuark_p4 = p.p4();
	    h_tbH_BQuark_Pt ->Fill(genP_pt);
	    h_tbH_BQuark_Eta->Fill(genP_eta);
	    h_tbH_BQuark_Phi->Fill(genP_phi);
	  }


	// g->tt, t->bW, b (From associated top decay)
	if( std::abs(genMom_pdgId) == 6 && mcTools.RecursivelyLookForMotherId(genP_index, 21, true) )
	  {

	    cgtt_tbW_WBoson.increment();
	    gtt_tbW_WBoson_p4 = p.p4();
	    h_gtt_tbW_BQuark_Pt ->Fill(genP_pt);
	    h_gtt_tbW_BQuark_Eta->Fill(genP_eta);
	    h_gtt_tbW_BQuark_Phi->Fill(genP_phi);
	  }

	
	// H+->tb, t->bW, b (From top decay)
	if( std::abs(genMom_pdgId) == 6 && mcTools.RecursivelyLookForMotherId(genP_index, 37, true) )
	  {

	    // In a small fraction of events we have H+ -> t b, t->t + X (X= b K0_s e+ e- K*+ K*-).
	    // This will force only the hardest b-quark being considered
	    cHtb_tbW_BQuark.increment();

	    // if ( cHtb_tbW_BQuark.value() != cHtb_BQuark.value() )
	    //   {
	    // 	std::cout << "entry = " << entry << std::endl;
	    // 	break;
	    //   }
	    // std::cout << "genP_index = " << genP_index << std::endl;
	    
	    Htb_tbW_BQuark_p4 = p.p4();
	    h_tbH_tbW_BQuark_Pt ->Fill(genP_pt);
	    h_tbH_tbW_BQuark_Eta->Fill(genP_eta);
	    h_tbH_tbW_BQuark_Phi->Fill(genP_phi);
	  }	

      } //if: Bottom Quarks
    

    // if: W Boson
    if( std::abs(genP_pdgId) == 24)
      {

	if (mcTools.RecursivelyLookForMotherId(genP_index, genP_pdgId, true) ) continue;
	
	// g->tt, t->bW (From associated top decay)
	if( std::abs(genMom_pdgId) == 6 && mcTools.RecursivelyLookForMotherId(genP_index, 21, true) )
	  {

	    cgtt_tbW_BQuark.increment();
	    gtt_tbW_BQuark_p4 = p.p4();
	    h_gtt_tbW_WBoson_Pt ->Fill(genP_pt);
	    h_gtt_tbW_WBoson_Eta->Fill(genP_eta);
	    h_gtt_tbW_WBoson_Phi->Fill(genP_phi);
	  }

	// H+->tb, t->bW (From top decay)
	if( std::abs(genMom_pdgId) == 6 && mcTools.RecursivelyLookForMotherId(genP_index, 37, true) )
	  {
	    cHtb_tbW_WBoson.increment();
	    Htb_tbW_WBoson_p4 = p.p4();
	    h_tbH_tbW_WBoson_Pt ->Fill(genP_pt);
	    h_tbH_tbW_WBoson_Eta->Fill(genP_eta);
	    h_tbH_tbW_WBoson_Phi->Fill(genP_phi);
	  }
	
      } // if: W Boson


    // if: Quarks (down=1, top=6)
    if( std::abs(genP_pdgId) >=1 && std::abs(genP_pdgId) <= 6 )
      {
	
	// H+->tb, t->bW, W->qq
	if( std::abs(genMom_pdgId) == 24 && mcTools.RecursivelyLookForMotherId(genP_index, 37, true) ){

	  if (genP_pdgId > 0)
	    {
	      cHtb_tbW_Wqq_Quark.increment();	
	      Htb_tbW_Wqq_Quark_p4 = p.p4();
	    }
	  
	  if (genP_pdgId < 0)
	    {
	      cHtb_tbW_Wqq_AntiQuark.increment();
	      Htb_tbW_Wqq_AntiQuark_p4 = p.p4();
	    }
	}

	// g->tt, t->bWH, t->bW, W->qq
	if( std::abs(genMom_pdgId) == 24 && mcTools.RecursivelyLookForMotherId(genP_index, 6, true) ){

	  if (genP_pdgId > 0)
	    {
	      cgtt_tbW_Wqq_Quark.increment();
	      gtt_tbW_Wqq_Quark_p4 = p.p4();
	    }
	  
	  if (genP_pdgId < 0)
	    {
	      cgtt_tbW_Wqq_AntiQuark.increment();
	      gtt_tbW_Wqq_AntiQuark_p4 = p.p4();
	    }
	  
	}

      }  // if: Quarks
    

    // if: HPlus 
    if( std::abs(genP_pdgId) == 37)
      {
	// Avoid double counting
	if (mcTools.RecursivelyLookForMotherId(genP_index, genP_pdgId, true) ) continue;
	
	cHtb_HPlus.increment();
	Htb_HPlus_p4 = p.p4();
	h_tbH_HPlus_Pt ->Fill(genP_pt);
	h_tbH_HPlus_Eta->Fill(genP_eta);
	h_tbH_HPlus_Phi->Fill(genP_phi);

      } // if: HPlus
  
           
  
  }//for-loop: genParticles


  // Print the table with genP info
  if (cfg_Verbose) table_genP.Print();
  
  
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
