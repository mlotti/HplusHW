// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

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
  // Helper Functions
   virtual bool RecursivelyLookForMotherId(const Event &fEvt, const int genP_index, int wantedMom_pdgId, const bool bAbsoluteMomId);
  
private:
  // Input parameters
  const double cfg_TopQuark_Pt;
  const double cfg_TopQuark_Eta;

  // Counters
  Count cAllEvents;
  Count cTrigger;
  Count cSelected;
    
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
  WrappedTH1 *h_Htb_TQuark_associated_TQuark_dR;
  WrappedTH1 *h_Htb_TQuark_associated_BQuark_dR;
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_BQuark_dR;
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_Wqq_Quark_dR;
  WrappedTH1 *h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dR;
  WrappedTH1 *h_associated_TQuark_associated_BQuark_dR;
  WrappedTH1 *h_associated_TQuark_gtt_tbW_BQuark_dR;
  WrappedTH1 *h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dR;
  WrappedTH1 *h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dR;

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(GenParticleKinematics);

GenParticleKinematics::GenParticleKinematics(const ParameterSet& config, const TH1* skimCounters)
: BaseSelector(config, skimCounters),
  cfg_TopQuark_Pt(config.getParameter<double>("TopQuark_Pt")),
  cfg_TopQuark_Eta(config.getParameter<double>("TopQuark_Eta")),  
  cAllEvents(fEventCounter.addCounter("All events")),
  cTrigger(fEventCounter.addCounter("Passed trigger")),
  cSelected(fEventCounter.addCounter("Selected events"))
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
  h_Htb_TQuark_associated_TQuark_dR         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "Htb_TQuark_associated_TQuark_dR"        , "dR(t, t)", 100, 0.0, +10.0);
  h_Htb_TQuark_associated_BQuark_dR         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "Htb_TQuark_associated_BQuark_dR"        , "dR(t, b)", 100, 0.0, +10.0);
  h_Htb_BQuark_Htb_tbW_BQuark_dR            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "Htb_BQuark_Htb_tbW_BQuark_dR"           , "dR(b, b)", 100, 0.0, +10.0);
  h_Htb_BQuark_Htb_tbW_Wqq_Quark_dR         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "Htb_BQuark_Htb_tbW_Wqq_Quark_dR"        , "dR(b, q)", 100, 0.0, +10.0);
  h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dR     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dR"    , "dR(b, q)", 100, 0.0, +10.0);
  h_associated_TQuark_associated_BQuark_dR  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "associated_TQuark_associated_BQuark_dR" , "dR(b, b)", 100, 0.0, +10.0);
  h_associated_TQuark_gtt_tbW_BQuark_dR     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "associated_TQuark_gtt_tbW_BQuark_dR"    , "dR(t, b)", 100, 0.0, +10.0);
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
  
  // Increment Counter
  cAllEvents.increment();

  if (0)
    {
      std::cout << "\n" << std::endl;
      std::cout << std::string(15*10, '=') << std::endl;
      std::cout << std::setw(12) << "Index "  << std::setw(12) << "PdgId"
		<< std::setw(12) << "Pt"      << std::setw(12) << "Eta"   << std::setw(12) << "Phi"
		<< std::setw(12) << "Energy"  << std::setw(12) << "Mass"  << std::setw(12) << "Mom-Index"
		<< std::setw(12) << "Mom-PdgId" << std::endl;
      std::cout << std::string(15*10, '=') << std::endl;    
    }
  

  // Event-based variables
  h_genMET_Et ->Fill(fEvent.genMET().et());
  h_genMET_Phi->Fill(fEvent.genMET().Phi());

  // HPlus & decay product
  math::XYZTLorentzVector Htb_HPlus_p4;
  math::XYZTLorentzVector Htb_TQuark_p4;
  math::XYZTLorentzVector Htb_BQuark_p4;
  math::XYZTLorentzVector Htb_tbW_BQuark_p4;
  math::XYZTLorentzVector Htb_tbW_WBoson_p4;
  math::XYZTLorentzVector Htb_tbW_Wqq_Quark_p4;
  math::XYZTLorentzVector Htb_tbW_Wqq_AntiQuark_p4;
  
  // Associated productions
  math::XYZTLorentzVector associated_TQuark_p4;
  math::XYZTLorentzVector associated_BQuark_p4;
  
  // Other
  math::XYZTLorentzVector gtt_tbW_Wqq_Quark_p4;
  math::XYZTLorentzVector gtt_tbW_Wqq_AntiQuark_p4;
  math::XYZTLorentzVector gtt_tbW_WBoson_p4;
  math::XYZTLorentzVector gtt_tbW_BQuark_p4;
 
  int genP_index = -1;
  // For-loop: GenParticles
  for (auto& p: fEvent.genparticles().getGenParticles()) {
    genP_index++;

    math::XYZTLorentzVector genP_p4;
    int genP_pdgId       = p.pdgId();
    double genP_pt       = p.pt();
    double genP_eta      = p.eta();
    double genP_phi      = p.phi();
    double genP_energy   = p.e();
    double genMom_index  = p.mother();
    double genMom_pdgId  = -999999.99;
    genP_p4 = p.p4();

    // Ensure a valid mom exists
    if (genMom_index >= 0){
      const Particle<ParticleCollection<double> > m = fEvent.genparticles().getGenParticles()[genMom_index];
      genMom_pdgId  = m.pdgId();      
    } 


    // Print genP info
    if (0)
      {
	std::cout << std::setw(12) << genP_index    << std::setw(12) << genP_pdgId
		  << std::setw(12) << genP_pt       << std::setw(12) << genP_eta       << std::setw(12) << genP_phi
		  << std::setw(12) << genP_energy   << std::setw(12) << genP_p4.mass() << std::setw(12) << genMom_index
		  << std::setw(12) << genMom_pdgId  << std::endl;
      }
    

    // if: Top Quarks
    if( std::abs(genP_pdgId) == 6)
      {
	    
	// g->tt (Associated production)
	if( std::abs(genMom_pdgId) == 21)
	  {

	    associated_TQuark_p4 = p.p4();
	    h_gtt_TQuark_Pt ->Fill(genP_pt);
	    h_gtt_TQuark_Eta->Fill(genP_eta);
	    h_gtt_TQuark_Phi->Fill(genP_phi);
	  }

	// H+->tb (From HPlus decay)
	if( std::abs(genMom_pdgId) == 37)
	  {
	    Htb_TQuark_p4 = p.p4();
	    h_tbH_TQuark_Pt ->Fill(genP_pt);
	    h_tbH_TQuark_Eta->Fill(genP_eta);
	    h_tbH_TQuark_Phi->Fill(genP_phi);
	  }	

      } //if: Top Quarks

    
    // if: Bottom Quarks
    if( std::abs(genP_pdgId) == 5)
      {	

	// g->bb (Associated production - Flavour excited b-quark)
	if( std::abs(genMom_pdgId) == 21)
	  {
	    associated_BQuark_p4 = p.p4();
	    h_gbb_BQuark_Pt ->Fill(genP_pt);
	    h_gbb_BQuark_Eta->Fill(genP_eta);
	    h_gbb_BQuark_Phi->Fill(genP_phi);
	  }

	// H+->tb (From HPlus decay)
	if( std::abs(genMom_pdgId) == 37)
	  {
	    Htb_BQuark_p4 = p.p4();
	    h_tbH_BQuark_Pt ->Fill(genP_pt);
	    h_tbH_BQuark_Eta->Fill(genP_eta);
	    h_tbH_BQuark_Phi->Fill(genP_phi);
	  }


	// g->tt, t->bW (From associated top decay)
	if( std::abs(genMom_pdgId) == 6 && RecursivelyLookForMotherId(fEvent, genP_index, 21, true) )
	  {
	    gtt_tbW_WBoson_p4 = p.p4();
	    h_gtt_tbW_BQuark_Pt ->Fill(genP_pt);
	    h_gtt_tbW_BQuark_Eta->Fill(genP_eta);
	    h_gtt_tbW_BQuark_Phi->Fill(genP_phi);
	  }

	
	// H+->tb, t->bW (From top decay)
	if( std::abs(genMom_pdgId) == 6 && RecursivelyLookForMotherId(fEvent, genP_index, 37, true) )
	  {
	    Htb_tbW_BQuark_p4 = p.p4();
	    h_tbH_tbW_BQuark_Pt ->Fill(genP_pt);
	    h_tbH_tbW_BQuark_Eta->Fill(genP_eta);
	    h_tbH_tbW_BQuark_Phi->Fill(genP_phi);
	  }	

      } //if: Bottom Quarks
    

    // if: W Boson
    if( std::abs(genP_pdgId) == 24)
      {

	// g->tt, t->bW (From associated top decay)
	if( std::abs(genMom_pdgId) == 6 && RecursivelyLookForMotherId(fEvent, genP_index, 21, true) )
	  {
	    gtt_tbW_BQuark_p4 = p.p4();
	    h_gtt_tbW_WBoson_Pt ->Fill(genP_pt);
	    h_gtt_tbW_WBoson_Eta->Fill(genP_eta);
	    h_gtt_tbW_WBoson_Phi->Fill(genP_phi);
	  }

	// H+->tb, t->bW (From top decay)
	if( std::abs(genMom_pdgId) == 6 && RecursivelyLookForMotherId(fEvent, genP_index, 37, true) )
	  {
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
	if( std::abs(genMom_pdgId) == 24 && RecursivelyLookForMotherId(fEvent, genP_index, 37, true) ){

	  if (genP_pdgId > 0) Htb_tbW_Wqq_Quark_p4 = p.p4();
	  if (genP_pdgId < 0) Htb_tbW_Wqq_AntiQuark_p4 = p.p4();    
	}

	// g->tt, t->bWH, t->bW, W->qq
	if( std::abs(genMom_pdgId) == 24 && RecursivelyLookForMotherId(fEvent, genP_index, 6, true) ){

	  if (genP_pdgId > 0) gtt_tbW_Wqq_Quark_p4 = p.p4();
	  if (genP_pdgId < 0) gtt_tbW_Wqq_AntiQuark_p4 = p.p4();
	}

      }  // if: Quarks
    

    // if: HPlus 
    if( std::abs(genP_pdgId) == 37)
      {
	Htb_HPlus_p4 = p.p4();
	h_tbH_HPlus_Pt ->Fill(genP_pt);
	h_tbH_HPlus_Eta->Fill(genP_eta);
	h_tbH_HPlus_Phi->Fill(genP_phi);
      } // if: HPlus
  
           
  
  }//for-loop: genParticles


  // H+->tb, t->bW, W->qq
  double dR_Htb_TQuark_Htb_BQuark            = ROOT::Math::VectorUtil::DeltaR(Htb_TQuark_p4, Htb_BQuark_p4);
  double dR_Htb_TQuark_associated_TQuark     = ROOT::Math::VectorUtil::DeltaR(Htb_TQuark_p4, associated_TQuark_p4);
  double dR_Htb_TQuark_associated_BQuark     = ROOT::Math::VectorUtil::DeltaR(Htb_TQuark_p4, associated_BQuark_p4);
  double dR_Htb_BQuark_Htb_tbW_BQuark        = ROOT::Math::VectorUtil::DeltaR(Htb_BQuark_p4, Htb_tbW_BQuark_p4);
  double dR_Htb_BQuark_Htb_tbW_Wqq_Quark     = ROOT::Math::VectorUtil::DeltaR(Htb_BQuark_p4, Htb_tbW_Wqq_Quark_p4);
  double dR_Htb_BQuark_Htb_tbW_Wqq_AntiQuark = ROOT::Math::VectorUtil::DeltaR(Htb_BQuark_p4, Htb_tbW_Wqq_AntiQuark_p4);
  
  // Associated products
  double dR_associated_TQuark_associated_BQuark  = ROOT::Math::VectorUtil::DeltaR(associated_TQuark_p4, associated_BQuark_p4);
  double dR_associated_TQuark_gtt_tbW_BQuark     = ROOT::Math::VectorUtil::DeltaR(associated_TQuark_p4, gtt_tbW_BQuark_p4); 
  double dR_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark     = ROOT::Math::VectorUtil::DeltaR(gtt_tbW_BQuark_p4, gtt_tbW_Wqq_Quark_p4);
  double dR_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark = ROOT::Math::VectorUtil::DeltaR(gtt_tbW_BQuark_p4, gtt_tbW_Wqq_AntiQuark_p4);

  // Fill dR histos
  h_Htb_TQuark_Htb_BQuark_dR                ->Fill( dR_Htb_TQuark_Htb_BQuark);
  h_Htb_TQuark_associated_TQuark_dR         ->Fill( dR_Htb_TQuark_associated_TQuark);
  h_Htb_TQuark_associated_BQuark_dR         ->Fill( dR_Htb_TQuark_associated_BQuark);
  h_Htb_BQuark_Htb_tbW_BQuark_dR            ->Fill( dR_Htb_BQuark_Htb_tbW_BQuark);
  h_Htb_BQuark_Htb_tbW_Wqq_Quark_dR         ->Fill( dR_Htb_BQuark_Htb_tbW_Wqq_Quark);
  h_Htb_BQuark_Htb_tbW_Wqq_AntiQuark_dR     ->Fill( dR_Htb_BQuark_Htb_tbW_Wqq_AntiQuark);
  h_associated_TQuark_associated_BQuark_dR  ->Fill( dR_associated_TQuark_associated_BQuark);
  h_associated_TQuark_gtt_tbW_BQuark_dR     ->Fill( dR_associated_TQuark_gtt_tbW_BQuark);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark_dR     ->Fill( dR_gtt_tbW_BQuark_gtt_tbW_Wqq_Quark);
  h_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark_dR ->Fill( dR_gtt_tbW_BQuark_gtt_tbW_Wqq_AntiQuark);

  // Htb_HPlus_p4;
  // Htb_TQuark_p4;
  // Htb_BQuark_p4;
  // Htb_tbW_WBoson_p4;
  // Htb_tbW_Wqq_Quark_p4;
  // Htb_tbW_Wqq_AntiQuark_p4;
  // associated_TQuark_p4;
  // associated_BQuark_p4;
  // gtt_tbW_WBoson_p4;
  // gtt_tbW_BQuark_p4;


  // Apply trigger
  if (!fEvent.passTriggerDecision()) return;
  cTrigger.increment();

  // Other selections
  cSelected.increment();

  return;
}


bool GenParticleKinematics::RecursivelyLookForMotherId(const Event &fEvt,
						       const int genP_index,
						       int wantedMom_pdgId,
						       const bool bAbsoluteMomId){

  if (bAbsoluteMomId) wantedMom_pdgId = std::abs(wantedMom_pdgId);
  
  // Get the mother index
  const Particle<ParticleCollection<double> > p = fEvent.genparticles().getGenParticles()[genP_index];
  double genMom_index = p.mother();
    
  // If mother index less than 0, return false
  if (genMom_index < 0) return false;
  
  // Valid mother exists, therefore get its pdgId
  const Particle<ParticleCollection<double> > m = fEvent.genparticles().getGenParticles()[genMom_index];
  double genMom_pdgId = m.pdgId();

  if (genMom_pdgId == wantedMom_pdgId)
    {
      return true;
    }
  if (RecursivelyLookForMotherId(fEvt, genMom_index, wantedMom_pdgId, bAbsoluteMomId) )
    {
      return true;
    }
  
  return false;
}
