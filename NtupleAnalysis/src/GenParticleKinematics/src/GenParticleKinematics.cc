// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

#include "TDirectory.h"

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
  // Temporary. Needs to move to Particle Class (Particle.h, Particle.cc)
  virtual bool RecursivelyLookForMotherId(const Event &fEvt, const int genP_index, int wantedMom_pdgId, const bool bAbsoluteMomId);
  
private:
  // Input parameters
  const double cfg_TopQuark_Pt;
  const double cfg_TopQuark_Eta;

  /// Common plots
  CommonPlots fCommonPlots;
  // Event selection classes and event counters (in same order like they are applied)
  Count cAllEvents;
  Count cTrigger;
  METFilterSelection fMETFilterSelection;
  Count cVertexSelection;
  TauSelection fTauSelection;
  Count cFakeTauSFCounter;
  Count cTauTriggerSFCounter;
  Count cMetTriggerSFCounter;
  ElectronSelection fElectronSelection;
  MuonSelection fMuonSelection;
  JetSelection fJetSelection;
  AngularCutsCollinear fAngularCutsCollinear;
  BJetSelection fBJetSelection;
  Count cBTaggingSFCounter;
  METSelection fMETSelection;
  AngularCutsBackToBack fAngularCutsBackToBack;
  Count cSelected;
    
  // Non-common histograms
  WrappedTH1 *h_gtt_TQuark_Pt;
  WrappedTH1 *h_gtt_tbW_WBoson_Pt;
  WrappedTH1 *h_gtt_tbW_BQuark_Pt;
  WrappedTH1 *h_tbH_HPlus_Pt;
  WrappedTH1 *h_tbH_TQuark_Pt;
  WrappedTH1 *h_tbH_BQuark_Pt;
  WrappedTH1 *h_tbH_tbW_WBoson_Pt;
  WrappedTH1 *h_tbH_tbW_BQuark_Pt;
  WrappedTH1 *h_gtt_BQuark_Pt;

  WrappedTH1 *h_gtt_TQuark_Eta;
  WrappedTH1 *h_gtt_tbW_WBoson_Eta;
  WrappedTH1 *h_gtt_tbW_BQuark_Eta;
  WrappedTH1 *h_tbH_HPlus_Eta;
  WrappedTH1 *h_tbH_TQuark_Eta;
  WrappedTH1 *h_tbH_BQuark_Eta;
  WrappedTH1 *h_tbH_tbW_WBoson_Eta;
  WrappedTH1 *h_tbH_tbW_BQuark_Eta;
  WrappedTH1 *h_gtt_BQuark_Eta;

  WrappedTH1 *h_gtt_TQuark_Phi;
  WrappedTH1 *h_gtt_tbW_WBoson_Phi;
  WrappedTH1 *h_gtt_tbW_BQuark_Phi;
  WrappedTH1 *h_tbH_HPlus_Phi;
  WrappedTH1 *h_tbH_TQuark_Phi;
  WrappedTH1 *h_tbH_BQuark_Phi;
  WrappedTH1 *h_tbH_tbW_WBoson_Phi;
  WrappedTH1 *h_tbH_tbW_BQuark_Phi;
  WrappedTH1 *h_gtt_BQuark_Phi;

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(GenParticleKinematics);

GenParticleKinematics::GenParticleKinematics(const ParameterSet& config, const TH1* skimCounters)
: BaseSelector(config, skimCounters),
  cfg_TopQuark_Pt(config.getParameter<double>("TopQuark_Pt")),
  cfg_TopQuark_Eta(config.getParameter<double>("TopQuark_Eta")),  
  fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kSignalAnalysis, fHistoWrapper),
  cAllEvents(fEventCounter.addCounter("All events")),
  cTrigger(fEventCounter.addCounter("Passed trigger")),
  fMETFilterSelection(config.getParameter<ParameterSet>("METFilter"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  cVertexSelection(fEventCounter.addCounter("Primary vertex selection")),
  fTauSelection(config.getParameter<ParameterSet>("TauSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  cFakeTauSFCounter(fEventCounter.addCounter("Fake tau SF")),
  cTauTriggerSFCounter(fEventCounter.addCounter("Tau trigger SF")),
  cMetTriggerSFCounter(fEventCounter.addCounter("Met trigger SF")),
  fElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
  fMuonSelection(config.getParameter<ParameterSet>("MuonSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
  fJetSelection(config.getParameter<ParameterSet>("JetSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  fAngularCutsCollinear(config.getParameter<ParameterSet>("AngularCutsCollinear"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  fBJetSelection(config.getParameter<ParameterSet>("BJetSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  cBTaggingSFCounter(fEventCounter.addCounter("b tag SF")),
  fMETSelection(config.getParameter<ParameterSet>("METSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  fAngularCutsBackToBack(config.getParameter<ParameterSet>("AngularCutsBackToBack"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  cSelected(fEventCounter.addCounter("Selected events"))
{ }

void GenParticleKinematics::book(TDirectory *dir) {
  // Book common plots histograms
  fCommonPlots.book(dir, isData());

  // Book histograms in event selection classes
  fMETFilterSelection.bookHistograms(dir);
  fTauSelection.bookHistograms(dir);
  fElectronSelection.bookHistograms(dir);
  fMuonSelection.bookHistograms(dir);
  fJetSelection.bookHistograms(dir);
  fAngularCutsCollinear.bookHistograms(dir);
  fBJetSelection.bookHistograms(dir);
  fMETSelection.bookHistograms(dir);
  fAngularCutsBackToBack.bookHistograms(dir);

  // Book non-common histograms
  h_gtt_TQuark_Pt     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_TQuark_Pt"    , "gtt, t-quark pT"     , 100, 0.0, 500.0);
  h_gtt_tbW_WBoson_Pt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_WBoson_Pt", "gtt, tWb W-boson pT" , 100, 0.0, 500.0);
  h_gtt_tbW_BQuark_Pt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_BQuark_Pt", "gtt, tWb b-quark pT" , 100, 0.0, 500.0);
  h_tbH_HPlus_Pt      =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_HPlus_Pt"     , "tbH, HPlus pT"       , 100, 0.0, 500.0);
  h_tbH_TQuark_Pt     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_TQuark_Pt"    , "tbH, t-quark pT"     , 100, 0.0, 500.0);
  h_tbH_BQuark_Pt     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_BQuark_Pt"    , "tbH, b-quark pT"     , 100, 0.0, 500.0);
  h_tbH_tbW_WBoson_Pt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_tbW_WBoson_Pt", "tbH, tbW, W-boson pT", 100, 0.0, 500.0);
  h_tbH_tbW_BQuark_Pt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_tbW_BQuark_Pt", "tbH, tbW, b-quark pT", 100, 0.0, 500.0);
  h_gtt_BQuark_Pt     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,  "gtt_BQuark_Pt"   , "gtt, b-quark pT, "   , 100, 0.0, 500.0);

  h_gtt_TQuark_Eta     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_TQuark_Eta"    , "gtt, t-quark pT"     , 50, -2.5, +2.5);
  h_gtt_tbW_WBoson_Eta =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_WBoson_Eta", "gtt, tWb W-boson pT" , 50, -2.5, +2.5);
  h_gtt_tbW_BQuark_Eta =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "gtt_tbW_BQuark_Eta", "gtt, tWb b-quark pT" , 50, -2.5, +2.5);
  h_tbH_HPlus_Eta      =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_HPlus_Eta"     , "tbH, HPlus pT"       , 50, -2.5, +2.5);
  h_tbH_TQuark_Eta     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_TQuark_Eta"    , "tbH, t-quark pT"     , 50, -2.5, +2.5);
  h_tbH_BQuark_Eta     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_BQuark_Eta"    , "tbH, b-quark pT"     , 50, -2.5, +2.5);
  h_tbH_tbW_WBoson_Eta =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_tbW_WBoson_Eta", "tbH, tbW, W-boson pT", 50, -2.5, +2.5);
  h_tbH_tbW_BQuark_Eta =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tbH_tbW_BQuark_Eta", "tbH, tbW, b-quark pT", 50, -2.5, +2.5);
  h_gtt_BQuark_Eta     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir,  "gtt_BQuark_Eta"   , "gtt, b-quark pT, "   , 50, -2.5, +2.5);

  h_gtt_TQuark_Phi     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gtt_TQuark_Phi"    , "gtt, t-quark pT"     , 100, -3.1416, +3.1416);
  h_gtt_tbW_WBoson_Phi =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gtt_tbW_WBoson_Phi", "gtt, tWb W-boson pT" , 100, -3.1416, +3.1416);
  h_gtt_tbW_BQuark_Phi =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "gtt_tbW_BQuark_Phi", "gtt, tWb b-quark pT" , 100, -3.1416, +3.1416);
  h_tbH_HPlus_Phi      =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_HPlus_Phi"     , "tbH, HPlus pT"       , 100, -3.1416, +3.1416);
  h_tbH_TQuark_Phi     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_TQuark_Phi"    , "tbH, t-quark pT"     , 100, -3.1416, +3.1416);
  h_tbH_BQuark_Phi     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_BQuark_Phi"    , "tbH, b-quark pT"     , 100, -3.1416, +3.1416);
  h_tbH_tbW_WBoson_Phi =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_tbW_WBoson_Phi", "tbH, tbW, W-boson pT", 100, -3.1416, +3.1416);
  h_tbH_tbW_BQuark_Phi =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "tbH_tbW_BQuark_Phi", "tbH, tbW, b-quark pT", 100, -3.1416, +3.1416);
  h_gtt_BQuark_Phi     =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir,  "gtt_BQuark_Phi"   , "gtt, b-quark pT, "   , 100, -3.1416, +3.1416);

  // TDirectory *WDir = dir->mkdir("W");
  // hWTauRtau1Pr0Pizero = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, WDir, "tauRtau1Pr0Pizero", "tauRtau1Pr0Pizero", 60, 0.0, 1.2);
  
  return;
}

void GenParticleKinematics::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}


void GenParticleKinematics::process(Long64_t entry) {

  if ( !fEvent.isMC() ) return;
  
  //====== Initialize
  fCommonPlots.initialize();
  fCommonPlots.setFactorisationBinForEvent(std::vector<float> {});

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
  
  // For-loop: GenParticles
  int genP_index = -1;
  for (auto& p: fEvent.genparticles().getGenParticles()) {
    genP_index++;

    int genP_pdgId     = p.pdgId();
    math::XYZTLorentzVectorT<double> genP_p4 = p.p4();
    double genP_pt       = p.pt();
    double genP_eta      = p.eta();
    double genP_phi      = p.phi();
    double genP_energy   = p.e();
    double genMom_index  = p.mother();
    double genMom_pdgId  = -999999.99;

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

	// std::cout << "\t here-0" << std::endl;
	    
	// Associated production
	if( std::abs(genMom_pdgId) == 21)
	  {
	    // std::cout << "\t here-1" << std::endl;
	    h_gtt_TQuark_Pt ->Fill(genP_pt);
	    h_gtt_TQuark_Eta->Fill(genP_eta);
	    h_gtt_TQuark_Phi->Fill(genP_phi);
	  }

	// From HPlus decay
	if( std::abs(genMom_pdgId) == 37)
	  {
	    // std::cout << "\t here-2" << std::endl;
	    h_tbH_TQuark_Pt ->Fill(genP_pt);
	    h_tbH_TQuark_Eta->Fill(genP_eta);
	    h_tbH_TQuark_Phi->Fill(genP_phi);
	  }	

      } //if: Top Quarks

    

    // if: Bottom Quarks
    if( std::abs(genP_pdgId) == 5)
      {
	// std::cout << "\t here-3" << std::endl;
	
	// Associated production
	if( std::abs(genMom_pdgId) == 21) //fixme: unique?
	  {
	    // std::cout << "\t here-4" << std::endl;
	    h_gtt_BQuark_Pt ->Fill(genP_pt);
	    h_gtt_BQuark_Eta->Fill(genP_eta);
	    h_gtt_BQuark_Phi->Fill(genP_phi);
	  }

	// From HPlus decay
	if( std::abs(genMom_pdgId) == 37)
	  {
	    // std::cout << "\t here-5" << std::endl;
	    h_tbH_BQuark_Pt ->Fill(genP_pt);
	    h_tbH_BQuark_Eta->Fill(genP_eta);
	    h_tbH_BQuark_Phi->Fill(genP_phi);
	  }


	// From associated top decay (gtt, tbW)
	if( std::abs(genMom_pdgId) == 6 && RecursivelyLookForMotherId(fEvent, genP_index, 21, true) )
	  {

	    // std::cout << "\t here-6" << std::endl;
	    h_gtt_tbW_BQuark_Pt ->Fill(genP_pt);
	    h_gtt_tbW_BQuark_Eta->Fill(genP_eta);
	    h_gtt_tbW_BQuark_Phi->Fill(genP_phi);
	  }

	
	// From top decay (tbH, tbW)
	if( std::abs(genMom_pdgId) == 6 && RecursivelyLookForMotherId(fEvent, genP_index, 37, true) )
	  {
	    // std::cout << "\t here-7" << std::endl;
	    h_tbH_tbW_BQuark_Pt ->Fill(genP_pt);
	    h_tbH_tbW_BQuark_Eta->Fill(genP_eta);
	    h_tbH_tbW_BQuark_Phi->Fill(genP_phi);
	  }	

      } //if: Bottom Quarks

    

    // if: W Boson
    if( std::abs(genP_pdgId) == 24)
      {
	// std::cout << "\t here-8" << std::endl;
	
	// From associated top decay (gtt, tbW)
	if( std::abs(genMom_pdgId) == 6 && RecursivelyLookForMotherId(fEvent, genP_index, 21, true) )
	  {
	    // std::cout << "\t here-9" << std::endl;
	    h_gtt_tbW_WBoson_Pt ->Fill(genP_pt);
	    h_gtt_tbW_WBoson_Eta->Fill(genP_eta);
	    h_gtt_tbW_WBoson_Phi->Fill(genP_phi);
	  }

	// From top decay (tbH, tbW)
	if( std::abs(genMom_pdgId) == 6 && RecursivelyLookForMotherId(fEvent, genP_index, 37, true) )
	  {
	    // std::cout << "\t here-10" << std::endl;
	    h_tbH_tbW_WBoson_Pt ->Fill(genP_pt);
	    h_tbH_tbW_WBoson_Eta->Fill(genP_eta);
	    h_tbH_tbW_WBoson_Phi->Fill(genP_phi);
	  }
	
      } // if: W Boson
    
    
    // if: HPlus 
    if( std::abs(genP_pdgId) == 37)
      {
	// std::cout << "\t here-11" << std::endl;	
	h_tbH_HPlus_Pt ->Fill(genP_pt);
	h_tbH_HPlus_Eta->Fill(genP_eta);
	h_tbH_HPlus_Phi->Fill(genP_phi);
      } // if: HPlus
           
  
  }//for-loop: genParticles


  
//====== Apply trigger
  if (!(fEvent.passTriggerDecision()))
    return;
  cTrigger.increment();
  int nVertices = fEvent.vertexInfo().value();
  fCommonPlots.setNvertices(nVertices);
  fCommonPlots.fillControlPlotsAfterTrigger(fEvent);

  //====== MET filters to remove events with spurious sources of fake MET
  const METFilterSelection::Data metFilterData = fMETFilterSelection.analyze(fEvent);
  if (!metFilterData.passedSelection())
    return;
  
  //====== GenParticle analysis
  // if needed
  
  //====== Check that primary vertex exists
  if (nVertices < 1)
    return;
  cVertexSelection.increment();
  fCommonPlots.fillControlPlotsAtVertexSelection(fEvent);
  
  //====== Tau selection
  const TauSelection::Data tauData = fTauSelection.analyze(fEvent);
  if (!tauData.hasIdentifiedTaus())
    return;
  
  //====== Fake tau SF
  if (fEvent.isMC()) {
    fEventWeight.multiplyWeight(tauData.getTauMisIDSF());
    cFakeTauSFCounter.increment();
  }

  //====== Tau trigger SF
  if (fEvent.isMC()) {
    fEventWeight.multiplyWeight(tauData.getTauTriggerSF());
    cTauTriggerSFCounter.increment();
  }

  //====== MET trigger SF
  const METSelection::Data silentMETData = fMETSelection.silentAnalyze(fEvent, nVertices);
  if (fEvent.isMC()) {
    fEventWeight.multiplyWeight(silentMETData.getMETTriggerSF());
  }
  cMetTriggerSFCounter.increment();
  fCommonPlots.fillControlPlotsAfterMETTriggerScaleFactor(fEvent);
  //std::cout << tauData.getSelectedTau().pt() << ":" << tauData.getTauMisIDSF() << ", " << tauData.getTauTriggerSF() << ", met=" << silentMETData.getMET().R() << ", SF=" << silentMETData.getMETTriggerSF() << std::endl;
  
  //====== Electron veto
  const ElectronSelection::Data eData = fElectronSelection.analyze(fEvent);
  if (eData.hasIdentifiedElectrons())
    return;

  //====== Muon veto
  const MuonSelection::Data muData = fMuonSelection.analyze(fEvent);
  if (muData.hasIdentifiedMuons())
    return;

  //====== Jet selection
  const JetSelection::Data jetData = fJetSelection.analyze(fEvent, tauData.getSelectedTau());
  if (!jetData.passedSelection())
    return;

  //====== Collinear angular cuts
  const AngularCutsCollinear::Data collinearData = fAngularCutsCollinear.analyze(fEvent, tauData.getSelectedTau(), jetData, silentMETData);
  if (!collinearData.passedSelection())
    return;

  //====== Point of standard selections
  fCommonPlots.fillControlPlotsAfterTopologicalSelections(fEvent);

  //====== b-jet selection
  const BJetSelection::Data bjetData = fBJetSelection.analyze(fEvent, jetData);
  // Fill final shape plots with b tag efficiency applied as an event weight
  if (silentMETData.passedSelection()) {
    const AngularCutsBackToBack::Data silentBackToBackData = fAngularCutsBackToBack.silentAnalyze(fEvent, tauData.getSelectedTau(), jetData, silentMETData);
    if (silentBackToBackData.passedSelection()) {
      fCommonPlots.fillControlPlotsAfterAllSelectionsWithProbabilisticBtag(fEvent, silentMETData, bjetData.getBTaggingPassProbability());
    }
  }
  if (!bjetData.passedSelection())
    return;

  //====== b tag SF
  if (fEvent.isMC()) {
    fEventWeight.multiplyWeight(bjetData.getBTaggingScaleFactorEventWeight());
  }
  cBTaggingSFCounter.increment();

  //====== MET selection
  const METSelection::Data METData = fMETSelection.analyze(fEvent, nVertices);
  if (!METData.passedSelection())
    return;
  
  //====== Back-to-back angular cuts
  const AngularCutsBackToBack::Data backToBackData = fAngularCutsBackToBack.analyze(fEvent, tauData.getSelectedTau(), jetData, METData);
  if (!backToBackData.passedSelection())
    return;

  //====== All cuts passed
  cSelected.increment();
  // Fill final plots
  fCommonPlots.fillControlPlotsAfterAllSelections(fEvent);
  

  //====== Experimental selection code
  // if necessary
  
  //====== Finalize
  fEventSaver.save();

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
