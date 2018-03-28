// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

#include "TDirectory.h"

#include "DataFormat/interface/AK8Jet.h"

class TestFatJets: public BaseSelector {
public:
  explicit TestFatJets(const ParameterSet& config, const TH1* skimCounters);
  virtual ~TestFatJets() {}

  /// Books histograms
  virtual void book(TDirectory *dir) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;

private:
  // Input parameters
  // const DirectionalCut<float> cfg_PrelimTopFitChiSqr;
  const DirectionalCut<double> cfg_PrelimTopMVACut;

  // Common plots
  CommonPlots fCommonPlots;
  // Event selection classes and event counters (in same order like they are applied)
  Count cAllEvents;
  Count cTrigger;
  METFilterSelection fMETFilterSelection;
  Count cVertexSelection;
  ElectronSelection fElectronSelection;
  MuonSelection fMuonSelection;
  TauSelection fTauSelection;
  JetSelection fJetSelection;
  BJetSelection fBJetSelection;
  Count cBTaggingSFCounter;
  METSelection fMETSelection;
  //TopologySelection fTopologySelection;
  TopSelectionBDT fTopSelection;
  FatJetSelection fFatJetSelection;
  Count cSelected;
  
  // Histograms
  WrappedTH1* h_FatJets_N;
  WrappedTH1* h_FatJets_Pt;
  WrappedTH1* h_FatJets_Eta;
  WrappedTH1* h_FatJets_Phi;
  WrappedTH1* h_FatJets_E;
  WrappedTH1* h_FatJets_PrunedMass;
  WrappedTH1* h_FatJets_PrunedMassCorr;
  WrappedTH1* h_FatJets_SoftDropMass;
  WrappedTH1* h_FatJets_IDLoose;
  WrappedTH1* h_FatJets_pdgId;
  WrappedTH1* h_FatJets_partonFlavour;
  WrappedTH1* h_FatJets_hadronFlavour;
  WrappedTH1* h_FatJets_NjettinessAK8tau1;
  WrappedTH1* h_FatJets_NjettinessAK8tau2;
  WrappedTH1* h_FatJets_NjettinessAK8tau3;
  WrappedTH1* h_FatJets_NumberOfDaughters;
  WrappedTH1* h_FatJets_NSubjets;
  WrappedTH1* h_FatJets_SDsubjet1_csv;
  WrappedTH1* h_FatJets_SDsubjet1_pt;
  WrappedTH1* h_FatJets_SDsubjet1_eta;
  WrappedTH1* h_FatJets_SDsubjet1_phi;
  WrappedTH1* h_FatJets_SDsubjet1_mass;
  WrappedTH1* h_FatJets_SDsubjet2_csv;
  WrappedTH1* h_FatJets_SDsubjet2_pt;
  WrappedTH1* h_FatJets_SDsubjet2_eta;
  WrappedTH1* h_FatJets_SDsubjet2_phi;
  WrappedTH1* h_FatJets_SDsubjet2_mass;
  WrappedTH1* h_FatJets_tau21;
  WrappedTH1* h_FatJets_tau32;
  
  
  // -------------------------------------------------------
  WrappedTH1* h_LdgFatJet_Pt;
  WrappedTH1* h_LdgFatJet_Eta;
  WrappedTH1* h_LdgFatJet_Phi;
  WrappedTH1* h_LdgFatJet_E;
  WrappedTH1* h_LdgFatJet_tau1;
  WrappedTH1* h_LdgFatJet_tau2;
  WrappedTH1* h_LdgFatJet_tau3;
  WrappedTH1* h_LdgFatJet_NSubjets;
  WrappedTH1* h_LdgFatJet_HasBSubjet;
  WrappedTH1* h_LdgFatJet_tau21;
  WrappedTH1* h_LdgFatJet_tau32;
  
  WrappedTH1* h_SubldgFatJet_Pt;
  WrappedTH1* h_SubldgFatJet_Eta;
  WrappedTH1* h_SubldgFatJet_Phi;
  WrappedTH1* h_SubldgFatJet_E;
  WrappedTH1* h_SubldgFatJet_tau1;
  WrappedTH1* h_SubldgFatJet_tau2;
  WrappedTH1* h_SubldgFatJet_tau3;
  WrappedTH1* h_SubldgFatJet_NSubjets;
  WrappedTH1* h_SubldgFatJet_HasBSubjet;
  WrappedTH1* h_SubldgFatJet_tau21;
  WrappedTH1* h_SubldgFatJet_tau32;
  
  

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(TestFatJets);

TestFatJets::TestFatJets(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    // cfg_PrelimTopFitChiSqr(config, "FakeBMeasurement.prelimTopFitChiSqrCut"),
    cfg_PrelimTopMVACut(config, "FakeBMeasurement.LdgTopMVACut"),
    fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kHplus2tbAnalysis, fHistoWrapper),
    cAllEvents(fEventCounter.addCounter("all events")),
    cTrigger(fEventCounter.addCounter("passed trigger")),
    fMETFilterSelection(config.getParameter<ParameterSet>("METFilter"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cVertexSelection(fEventCounter.addCounter("passed PV")),
    fElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fMuonSelection(config.getParameter<ParameterSet>("MuonSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fTauSelection(config.getParameter<ParameterSet>("TauSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fJetSelection(config.getParameter<ParameterSet>("JetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fBJetSelection(config.getParameter<ParameterSet>("BJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cBTaggingSFCounter(fEventCounter.addCounter("b tag SF")),
    fMETSelection(config.getParameter<ParameterSet>("METSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    //fTopologySelection(config.getParameter<ParameterSet>("TopologySelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fTopSelection(config.getParameter<ParameterSet>("TopSelectionBDT"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fFatJetSelection(config.getParameter<ParameterSet>("FatJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cSelected(fEventCounter.addCounter("Selected Events"))
{ }


void TestFatJets::book(TDirectory *dir) {

  
  // Book common plots histograms
  fCommonPlots.book(dir, isData());

  // Book histograms in event selection classes
  fMETFilterSelection.bookHistograms(dir);
  fElectronSelection.bookHistograms(dir);
  fMuonSelection.bookHistograms(dir);
  fTauSelection.bookHistograms(dir);
  fJetSelection.bookHistograms(dir);
  fBJetSelection.bookHistograms(dir);
  fMETSelection.bookHistograms(dir);
  //fTopologySelection.bookHistograms(dir);
  fTopSelection.bookHistograms(dir);
  fFatJetSelection.bookHistograms(dir);

  // Book non-common histograms
  h_FatJets_N     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_N"      , "Fat Jets Multiplicity"      , 15, -0.5, 14.5    );
  h_FatJets_Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_Pt"     , "Fat Jets p_{T} (GeVc^{-1})" , 100, 0.0, 2000.0  );
  h_FatJets_Eta   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_Eta"    , "Fat Jets #eta"              , 120, -6.0, 6.0     );
  h_FatJets_Phi   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_Phi"    , "Fat Jets #phi"              , 120, -6.0, 6.0     );
  h_FatJets_E     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_E"      , "Fat Jets E"                 , 100, 0.0, 2000.0  );
  h_FatJets_pdgId = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_pdgId"  , "Fat Jets pdgID"             , 40, -20, 20);
  h_FatJets_partonFlavour = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_partonFlavour"  , "Fat Jets parton flavour"     , 40, -20, 20);
  h_FatJets_hadronFlavour = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_hadronFlavout"  , "Fat Jets hadron flavour"     , 7, 0.0, 7.0);
  h_FatJets_NjettinessAK8tau1 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_NjettinessAK8tau1", "Fat Jets #tau_{1}", 100, 0.0, 1.0);
  h_FatJets_NjettinessAK8tau2 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_NjettinessAK8tau2", "Fat Jets #tau_{2}", 100, 0.0, 1.0);
  h_FatJets_NjettinessAK8tau3 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_NjettinessAK8tau3", "Fat Jets #tau_{3}", 100, 0.0, 1.0);
  h_FatJets_IDLoose = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_IDLoose", "Fat Jets with Loose ID", 2, 0.0, 2.0);
  h_FatJets_NSubjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_NSubjets", "Fat Jets Subjets Multiplicity", 10, -0.5, 9.5);
  h_FatJets_tau21 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_tau21", "Fat Jets #tau_{2}/#tau_{1}", 100, 0.0, 1.0);
  h_FatJets_tau32 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_tau32", "Fat Jets #tau_{3}/#tau_{1}", 100, 0.0, 1.0);
  h_FatJets_PrunedMass = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir,"FatJets_PrunedMass", "Fat Jets Pruned Mass", 100, 0.0, 2000.0  );
  h_FatJets_PrunedMassCorr = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir,"FatJets_PrunedMassCorr", "Fat Jets Prined Mass corrected", 100, 0.0, 2000.0  );
  h_FatJets_SoftDropMass = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir,"FatJets_SoftDropMass", "Fat Jets Soft Drop Mass", 100, 0.0, 2000.0  );
  h_FatJets_NumberOfDaughters = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir,"FatJets_NumberOfDaughters", "Fat Jets Daughter multiplicity", 100, 0, 100);
  h_FatJets_SDsubjet1_csv = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_SDsubjet1_csv", "Soft Drop Subjet 1 CSV", 100, 0.0, 1.0);
  h_FatJets_SDsubjet1_pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_SDsubjet1_pt", "Soft Drop Subjet 1 p_{t} (GeV)", 100, 0.0, 2000.0  );
  h_FatJets_SDsubjet1_eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_SDsubjet1_eta","Soft Drop Subjet 1 #eta", 120, -6.0, 6.0);
  h_FatJets_SDsubjet1_phi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_SDsubjet1_phi","Soft Drop Subjet 1 #phi", 120, -6.0, 6.0);
  h_FatJets_SDsubjet1_mass= fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_SDsubjet1_mass","Soft Drop Subjet 1 mass", 100, 0.0, 2000.0);
  h_FatJets_SDsubjet2_csv = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_SDsubjet2_csv", "Soft Drop Subjet 2 CSV", 100, 0.0, 1.0);
  h_FatJets_SDsubjet2_pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_SDsubjet2_pt", "Soft Drop Subjet 2 p_{t} (GeV)", 100, 0.0, 2000.0  );
  h_FatJets_SDsubjet2_eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_SDsubjet2_eta","Soft Drop Subjet 2 #eta", 120, -6.0, 6.0);
  h_FatJets_SDsubjet2_phi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_SDsubjet2_phi","Soft Drop Subjet 2 #phi", 120, -6.0, 6.0);
  h_FatJets_SDsubjet2_mass= fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_SDsubjet2_mass","Soft Drop Subjet 2 mass", 100, 0.0, 2000.0);
  // -------------------------------------------------------------------------------------------------------------------------------------------------------
  h_LdgFatJet_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_Pt", "Leading Fat Jet p_{T} (GeVc^{-1})", 100, 0.0, 2000.0  );
  h_LdgFatJet_Eta= fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_Eta","Leading Fat Jet #eta", 60, -3.0, 3.0);
  h_LdgFatJet_Phi= fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_Phi","Leading Fat Jet $phi", 80, -4.0, 4.0);
  h_LdgFatJet_E  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_E", "Leading Fat Jet E", 100, 0.0, 2000.0);
  h_LdgFatJet_tau1 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_tau1", "Leading Fat Jet tau1", 100, 0.0, 1.0);
  h_LdgFatJet_tau2 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_tau2", "Leading Fat Jet tau2", 100, 0.0, 1.0);
  h_LdgFatJet_tau3 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_tau3", "Leading Fat Jet tau3", 100, 0.0, 1.0);
  h_LdgFatJet_NSubjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_NSubjets", "Leading Fat Jet Subjets Multiplicity", 10, -0.5, 9.5);
  h_LdgFatJet_HasBSubjet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_HasBSubjet", "Leading Fat Jet HasBSubjet", 2, 0.0, 2.0);
  h_LdgFatJet_tau21 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_tau21", "Leading Fat Jet #tau_{2}/#tau_{1}", 100, 0.0, 1.0);
  h_LdgFatJet_tau32 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_tau32", "Leading Fat Jet #tau_{3}/#tau_{1}", 100, 0.0, 1.0);
  h_SubldgFatJet_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "SubldgFatJet_Pt", "Subleading Fat Jet p_{T} (GeVc^{-1})", 100, 0.0, 2000.0  );
  h_SubldgFatJet_Eta= fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "SubldgFatJet_Eta","Subleading Fat Jet #eta", 60, -3.0, 3.0);
  h_SubldgFatJet_Phi= fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "SubldgFatJet_Phi","Subleading Fat Jet $phi", 80, -4.0, 4.0);
  h_SubldgFatJet_E  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "SubldgFatJet_E", "Subleading Fat Jet E", 100, 0.0, 2000.0);
  h_SubldgFatJet_tau1 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "SubldgFatJet_tau1", "Subleading Fat Jet tau1", 100, 0.0, 1.0);
  h_SubldgFatJet_tau2 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "SubldgFatJet_tau2", "Subleading Fat Jet tau2",  100, 0.0, 1.0);
  h_SubldgFatJet_tau3 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "SubldgFatJet_tau3", "Subleading Fat Jet tau3",  100, 0.0, 1.0);
  h_SubldgFatJet_NSubjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "SubldgFatJet_NSubjets", "Subleading Fat Jet Subjets Multiplicity", 10, -0.5, 9.5);
  h_SubldgFatJet_HasBSubjet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "SubldgFatJet_HasBSubjet", "Subleading Fat Jet HasBSubjet", 2, 0.0, 2.0);
  h_SubldgFatJet_tau21 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "SubldgFatJet_tau21", "Subleading Fat Jet #tau_{2}/#tau_{1}", 100, 0.0, 1.0);
  h_SubldgFatJet_tau32 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "SubldgFatJet_tau32", "Subleading Fat Jet #tau_{3}/#tau_{1}", 100, 0.0, 1.0);
  return;
}


void TestFatJets::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
  return;
}


void TestFatJets::process(Long64_t entry) {

  //====== Initialize
  fCommonPlots.initialize();
  fCommonPlots.setFactorisationBinForEvent(std::vector<float> {});
  cAllEvents.increment();

  //================================================================================================   
  // 1) Apply trigger 
  //================================================================================================   
  if (0) std::cout << "=== Trigger" << std::endl;
  if ( !(fEvent.passTriggerDecision()) ) return;
  
  cTrigger.increment();
  int nVertices = fEvent.vertexInfo().value();
  fCommonPlots.setNvertices(nVertices);
  fCommonPlots.fillControlPlotsAfterTrigger(fEvent);

  //================================================================================================   
  // 2) MET filters (to remove events with spurious sources of fake MET)
  //================================================================================================   
  if (0) std::cout << "=== MET Filter" << std::endl;
  const METFilterSelection::Data metFilterData = fMETFilterSelection.analyze(fEvent);
  if (!metFilterData.passedSelection()) return;
  fCommonPlots.fillControlPlotsAfterMETFilter(fEvent);  

  //================================================================================================   
  // 3) Primarty Vertex (Check that a PV exists)
  //================================================================================================   
  if (0) std::cout << "=== Vertices" << std::endl;
  if (nVertices < 1) return;
  cVertexSelection.increment();
  fCommonPlots.fillControlPlotsAtVertexSelection(fEvent);
  
  //================================================================================================   
  // 4) Electron veto (Fully hadronic + orthogonality)
  //================================================================================================   
  if (0) std::cout << "=== Electron veto" << std::endl;
  const ElectronSelection::Data eData = fElectronSelection.analyze(fEvent);
  if (eData.hasIdentifiedElectrons()) return;

  //================================================================================================
  // 5) Muon veto (Fully hadronic + orthogonality)
  //================================================================================================
  if (0) std::cout << "=== Muon veto" << std::endl;
  const MuonSelection::Data muData = fMuonSelection.analyze(fEvent);
  if (muData.hasIdentifiedMuons()) return;

  //================================================================================================   
  // 6) Tau Veto (HToTauNu Orthogonality)
  //================================================================================================   
  if (0) std::cout << "=== Tau Veto" << std::endl;
  const TauSelection::Data tauData = fTauSelection.analyze(fEvent);
  if (tauData.hasIdentifiedTaus() ) return;
  
  //================================================================================================
  // 7) Jet selection
  //================================================================================================
  if (0) std::cout << "=== Jet selection" << std::endl;
  const JetSelection::Data jetData = fJetSelection.analyzeWithoutTau(fEvent);
  if (!jetData.passedSelection()) return;
  //fCommonPlots.fillControlPlotsAfterTopologicalSelections(fEvent, true);
 
  //================================================================================================  
  // 8) BJet selection
  //================================================================================================
  if (0) std::cout << "=== BJet selection" << std::endl;
  const BJetSelection::Data bjetData = fBJetSelection.analyze(fEvent, jetData);
  if (!bjetData.passedSelection()) return;
  //fCommonPlots.fillControlPlotsAfterBjetSelection(fEvent, bjetData);
  
  //================================================================================================  
  // 9) BJet SF  
  //================================================================================================
  if (0) std::cout << "=== BJet SF" << std::endl;
  if (fEvent.isMC()) 
    {
      fEventWeight.multiplyWeight(bjetData.getBTaggingScaleFactorEventWeight());
    }
  cBTaggingSFCounter.increment();

  //================================================================================================
  // 10) MET selection
  //================================================================================================
  if (0) std::cout << "=== MET selection" << std::endl;
  const METSelection::Data METData = fMETSelection.analyze(fEvent, nVertices);
  // if (!METData.passedSelection()) return;

  //================================================================================================
  // 11) Topology selection
  //================================================================================================
  //if (0) std::cout << "=== Topology selection" << std::endl;
  //const TopologySelection::Data topologyData = fTopologySelection.analyze(fEvent, jetData);
  // if (!topologyData.passedSelection()) return; 

  //================================================================================================
  // 12) Top selection
  //================================================================================================
  if (0) std::cout << "=== Top (BDT) selection" << std::endl;
  const TopSelectionBDT::Data topData = fTopSelection.analyze(fEvent, jetData, bjetData);
  bool passPrelimMVACut = cfg_PrelimTopMVACut.passedCut( std::max(topData.getMVAmax1(), topData.getMVAmax2()) ); //fixme?
  bool hasFreeBJet      = topData.hasFreeBJet();
  if (!hasFreeBJet) return;
  if (!passPrelimMVACut) return;

  //================================================================================================
  // Standard Selections
  //================================================================================================
  if (0) std::cout << "=== Standard Selections" << std::endl;
  //fCommonPlots.fillControlPlotsAfterStandardSelections(fEvent, jetData, bjetData, METData, topologyData, topData, bjetData.isGenuineB());
  
  //================================================================================================
  // All Selections
  //================================================================================================
  //if (!topologyData.passedSelection()) return;
  //if (!topData.passedSelection()) return;

  //if (0) std::cout << "=== All Selections" << std::endl;
  //cSelected.increment();
  
  //================================================================================================
  // Other) Fat Jet selection
  //================================================================================================
  //
  if (0) std::cout << "=== Fat Jet selection" << std::endl;
  const FatJetSelection::Data fatjetData = fFatJetSelection.analyzeWithoutTop(fEvent);
  //if (!fatjetData.passedSelection()) return;
  
  int nFatJets = 0;
  
  h_FatJets_N -> Fill(fatjetData.getNumberOfSelectedFatJets());
  for (auto jet: fatjetData.getSelectedFatJets())
    {
      nFatJets++;
      
      double pt = jet.pt();
      double eta= jet.eta();
      double phi= jet.phi();			
      double e  = jet.e();
      double mass_pruned = jet.ak8PFJetsCHSPrunedMass();
      double mass_prunedCorr = jet.corrPrunedMass();
      double mass_sd = jet.ak8PFJetsCHSSoftDropMass();
      double tau1 = jet.NjettinessAK8tau1();
      double tau2 = jet.NjettinessAK8tau2();
      double tau3 = jet.NjettinessAK8tau3();
      
      bool IDloose = jet.IDloose();
      
      int pdgId = jet.pdgId();
      int hadronFlavour = jet.hadronFlavour();
      int partonFlavour = jet.partonFlavour();
      int nDaughters = jet.numberOfDaughters();
      
            
      h_FatJets_Pt  -> Fill(pt);
      h_FatJets_Eta -> Fill(eta);
      h_FatJets_Phi -> Fill(phi);
      h_FatJets_E   -> Fill(e);
      h_FatJets_PrunedMass -> Fill(mass_pruned);
      h_FatJets_PrunedMassCorr -> Fill(mass_prunedCorr);
      h_FatJets_SoftDropMass -> Fill(mass_sd);
      h_FatJets_IDLoose -> Fill(IDloose);
      h_FatJets_pdgId -> Fill(pdgId);
      h_FatJets_partonFlavour -> Fill(partonFlavour);
      h_FatJets_hadronFlavour -> Fill(hadronFlavour);
      h_FatJets_NjettinessAK8tau1 -> Fill(tau1);
      h_FatJets_NjettinessAK8tau2 -> Fill(tau2);
      h_FatJets_NjettinessAK8tau3 -> Fill(tau3);
      h_FatJets_NumberOfDaughters -> Fill(nDaughters);
      h_FatJets_tau21 -> Fill(tau2/tau1);
      h_FatJets_tau32 -> Fill(tau3/tau2);
      
      int nSDsubjets = jet.nsoftdropSubjets();
      h_FatJets_NSubjets -> Fill(nSDsubjets);
      
      // Leading Fat Jets
      if (nFatJets == 1){
	h_LdgFatJet_Pt   -> Fill(pt);
	h_LdgFatJet_Eta  -> Fill(eta);
	h_LdgFatJet_Phi  -> Fill(phi);
	h_LdgFatJet_E    -> Fill(e);
	h_LdgFatJet_tau1 -> Fill(tau1);
	h_LdgFatJet_tau2 -> Fill(tau2);
	h_LdgFatJet_tau3 -> Fill(tau3);
	h_LdgFatJet_tau21-> Fill(tau2/tau1);
	h_LdgFatJet_tau32-> Fill(tau3/tau2);
      }
      if (nFatJets == 2){
	// Subleading Fat Jets
	h_SubldgFatJet_Pt    -> Fill(pt);
	h_SubldgFatJet_Eta   -> Fill(eta);
	h_SubldgFatJet_Phi   -> Fill(phi);
	h_SubldgFatJet_E     -> Fill(e);
	h_SubldgFatJet_tau1  -> Fill(tau1);
	h_SubldgFatJet_tau2  -> Fill(tau2);
	h_SubldgFatJet_tau3  -> Fill(tau3);
	h_SubldgFatJet_tau21 -> Fill(tau2/tau1);
	h_SubldgFatJet_tau32 -> Fill(tau3/tau2);
      }
      // Subjets Histos
      if (nSDsubjets < 1) continue;
      
      double sd1_csv = jet.sdsubjet1_csv();
      double sd1_pt  = jet.sdsubjet1_pt();
      double sd1_eta = jet.sdsubjet1_eta();
      double sd1_phi = jet.sdsubjet1_phi();
      double sd1_mass= jet.sdsubjet1_mass();
      h_FatJets_SDsubjet1_csv  -> Fill(sd1_csv);
      h_FatJets_SDsubjet1_pt   -> Fill(sd1_pt);
      h_FatJets_SDsubjet1_eta  -> Fill(sd1_eta);
      h_FatJets_SDsubjet1_phi  -> Fill(sd1_phi);
      h_FatJets_SDsubjet1_mass -> Fill(sd1_mass);
      
      if (nSDsubjets < 2) continue;

      double sd2_csv = jet.sdsubjet2_csv();
      double sd2_pt  = jet.sdsubjet2_pt();
      double sd2_eta = jet.sdsubjet2_eta();
      double sd2_phi = jet.sdsubjet2_phi();
      double sd2_mass= jet.sdsubjet2_mass();
      h_FatJets_SDsubjet2_csv  -> Fill(sd2_csv);
      h_FatJets_SDsubjet2_pt   -> Fill(sd2_pt);
      h_FatJets_SDsubjet2_eta  -> Fill(sd2_eta);
      h_FatJets_SDsubjet2_phi  -> Fill(sd2_phi);
      h_FatJets_SDsubjet2_mass -> Fill(sd2_mass);
    }
  
    
  //================================================================================================
  // Fill final plots
  //===============================================================================================
  //fCommonPlots.fillControlPlotsAfterAllSelections(fEvent, 1);
  
  //================================================================================================
  // Finalize
  //================================================================================================
  fEventSaver.save();

  return;
}
