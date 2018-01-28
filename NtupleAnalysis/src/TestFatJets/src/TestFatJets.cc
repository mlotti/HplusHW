// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

#include "TDirectory.h"

#include "DataFormat/interface/AK8Jet.h"
#include "DataFormat/interface/AK8JetsSoftDrop.h"

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
  Count cSelected;
  
  FatJetSelection fFatJetSelection;
  FatJetSoftDropSelection fFatJetSoftDropSelection;
  

  // Non-common histograms
  // WrappedTH1 *hAssociatedTop_Pt;
  // WrappedTH1 *hAssociatedTop_Eta;

  WrappedTH1* h_FatJets_N;
  WrappedTH1* h_FatJets_Pt;
  WrappedTH1* h_FatJets_Eta;
  WrappedTH1* h_FatJets_Phi;
  WrappedTH1* h_FatJets_E;
  //
  WrappedTH1* h_FatJets_pdgId;
  WrappedTH1* h_FatJets_partonFlavour;
  WrappedTH1* h_FatJets_hadronFlavour;
  //
  WrappedTH1* h_FatJets_CSVdiscr;
  WrappedTH1* h_FatJets_MVAdiscr;
  WrappedTH1* h_FatJets_CvsLdiscr;
  WrappedTH1* h_FatJets_CvsBdiscr;
  //
  WrappedTH1* h_FatJets_NjettinessAK8CHStau1;
  WrappedTH1* h_FatJets_NjettinessAK8CHStau2;
  WrappedTH1* h_FatJets_NjettinessAK8CHStau3;
  WrappedTH1* h_FatJets_NjettinessAK8CHStau4;
  //
  WrappedTH1* h_FatJets_IDLoose;
  //
  WrappedTH1* h_FatJets_NSubjets;
  WrappedTH1* h_FatJets_HasBSubjet;
  //
  WrappedTH1* h_FatJets_tau21;
  WrappedTH1* h_FatJets_tau32;
  
  
  // -------------------------------------------------------
  WrappedTH1* h_LdgFatJet_Pt;
  WrappedTH1* h_LdgFatJet_Eta;
  WrappedTH1* h_LdgFatJet_Phi;
  WrappedTH1* h_LdgFatJet_E;
  WrappedTH1* h_LdgFatJet_CSVdiscr;
  WrappedTH1* h_LdgFatJet_tau1;
  WrappedTH1* h_LdgFatJet_tau2;
  WrappedTH1* h_LdgFatJet_tau3;
  WrappedTH1* h_LdgFatJet_tau4;
  WrappedTH1* h_LdgFatJet_NSubjets;
  WrappedTH1* h_LdgFatJet_HasBSubjet;
  WrappedTH1* h_LdgFatJet_tau21;
  WrappedTH1* h_LdgFatJet_tau32;
  
  WrappedTH1* h_SubldgFatJet_Pt;
  WrappedTH1* h_SubldgFatJet_Eta;
  WrappedTH1* h_SubldgFatJet_Phi;
  WrappedTH1* h_SubldgFatJet_E;
  WrappedTH1* h_SubldgFatJet_CSVdiscr;
  WrappedTH1* h_SubldgFatJet_tau1;
  WrappedTH1* h_SubldgFatJet_tau2;
  WrappedTH1* h_SubldgFatJet_tau3;
  WrappedTH1* h_SubldgFatJet_tau4;
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
    cfg_PrelimTopMVACut(config, "FakeBMeasurement.prelimTopMVACut"),
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
    cSelected(fEventCounter.addCounter("Selected Events")),
    fFatJetSelection(config.getParameter<ParameterSet>("FatJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fFatJetSoftDropSelection(config.getParameter<ParameterSet>("FatJetSoftDropSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "")
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
  fFatJetSoftDropSelection.bookHistograms(dir);
  

  // Book non-common histograms
  
  h_FatJets_N     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_N"      , "Fat Jets Multiplicity"      , 15, -0.5, 14.5    );
  h_FatJets_Pt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_Pt"     , "Fat Jets p_{T} (GeVc^{-1})" , 100, 0.0, 2000.0  );
  h_FatJets_Eta   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_Eta"    , "Fat Jets #eta"              , 120, -6.0, 6.0     );
  h_FatJets_Phi   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_Phi"    , "Fat Jets #phi"              , 120, -6.0, 6.0     );
  h_FatJets_E     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_E"      , "Fat Jets E"                 , 100, 0.0, 2000.0  );
  //
  h_FatJets_pdgId = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_pdgId"  , "Fat Jets pdgID"             , 40, -20, 20);
  h_FatJets_partonFlavour = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_partonFlavour"  , "Fat Jets parton flavour"     , 40, -20, 20);
  h_FatJets_hadronFlavour = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_hadronFlavout"  , "Fat Jets hadron flavour"     , 7, 0.0, 7.0);
  //
  h_FatJets_CSVdiscr      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_CSVdiscr"       , "Fat Jets CSV discriminant"   , 100, 0.0, 1.0);
  h_FatJets_MVAdiscr      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_MVAdiscr"       , "Fat Jets MVA discriminant"   , 100, 0.0, 1.0);
  h_FatJets_CvsLdiscr     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_CvsLdiscr"      , "Fat Jets CvsL discriminant"  , 100, 0.0, 1.0);
  h_FatJets_CvsBdiscr     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_CvsBdiscr"      , "Fat Jets CvsB discriminant"  , 100, 0.0, 1.0);
  //
  h_FatJets_NjettinessAK8CHStau1 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_NjettinessAK8CHStau1", "Fat Jets #tau_{1}", 100, 0.0, 1.0);
  h_FatJets_NjettinessAK8CHStau2 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_NjettinessAK8CHStau2", "Fat Jets #tau_{2}", 100, 0.0, 1.0);
  h_FatJets_NjettinessAK8CHStau3 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_NjettinessAK8CHStau3", "Fat Jets #tau_{3}", 100, 0.0, 1.0);
  h_FatJets_NjettinessAK8CHStau4 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_NjettinessAK8CHStau4", "Fat Jets #tau_{4}", 100, 0.0, 1.0);
  //
  h_FatJets_IDLoose = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_IDLoose", "Fat Jets with Loose ID", 2, 0.0, 2.0);
  
  h_FatJets_NSubjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_NSubjets", "Fat Jets Subjets Multiplicity", 10, -0.5, 9.5);
  h_FatJets_HasBSubjet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_HasBSubjet", "Fat Jets HasBSubjet", 2, 0.0, 2.0);
  
  h_FatJets_tau21 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_tau21", "Fat Jets #tau_{2}/#tau_{1}", 100, 0.0, 1.0);
  h_FatJets_tau32 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "FatJets_tau32", "Fat Jets #tau_{3}/#tau_{1}", 100, 0.0, 1.0);





  
  // -------------------------------------------------------------------------------------------------------------------------------------------------------
  h_LdgFatJet_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_Pt", "Leading Fat Jet p_{T} (GeVc^{-1})", 100, 0.0, 2000.0  );
  h_LdgFatJet_Eta= fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_Eta","Leading Fat Jet #eta", 60, -3.0, 3.0);
  h_LdgFatJet_Phi= fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_Phi","Leading Fat Jet $phi", 80, -4.0, 4.0);
  h_LdgFatJet_E  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_E", "Leading Fat Jet E", 100, 0.0, 2000.0);
  h_LdgFatJet_CSVdiscr = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_CSVdiscr", "Leading Fat Jet CSV discriminant", 100, 0.0, 1.0);
  h_LdgFatJet_tau1 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_tau1", "Leading Fat Jet tau1", 100, 0.0, 1.0);
  h_LdgFatJet_tau2 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_tau2", "Leading Fat Jet tau2", 100, 0.0, 1.0);
  h_LdgFatJet_tau3 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_tau3", "Leading Fat Jet tau3", 100, 0.0, 1.0);
  h_LdgFatJet_tau4 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_tau4", "Leading Fat Jet tau4", 100, 0.0, 1.0);
  h_LdgFatJet_NSubjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_NSubjets", "Leading Fat Jet Subjets Multiplicity", 10, -0.5, 9.5);
  h_LdgFatJet_HasBSubjet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_HasBSubjet", "Leading Fat Jet HasBSubjet", 2, 0.0, 2.0);
  h_LdgFatJet_tau21 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_tau21", "Leading Fat Jet #tau_{2}/#tau_{1}", 100, 0.0, 1.0);
  h_LdgFatJet_tau32 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LdgFatJet_tau32", "Leading Fat Jet #tau_{3}/#tau_{1}", 100, 0.0, 1.0);




  h_SubldgFatJet_Pt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "SubldgFatJet_Pt", "Subleading Fat Jet p_{T} (GeVc^{-1})", 100, 0.0, 2000.0  );
  h_SubldgFatJet_Eta= fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "SubldgFatJet_Eta","Subleading Fat Jet #eta", 60, -3.0, 3.0);
  h_SubldgFatJet_Phi= fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "SubldgFatJet_Phi","Subleading Fat Jet $phi", 80, -4.0, 4.0);
  h_SubldgFatJet_E  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "SubldgFatJet_E", "Subleading Fat Jet E", 100, 0.0, 2000.0);
  h_SubldgFatJet_CSVdiscr = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "SubldgFatJet_CSVdiscr", "Subleading Fat Jet CSV discriminant", 100, 0.0, 1.0);
  h_SubldgFatJet_tau1 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "SubldgFatJet_tau1", "Subleading Fat Jet tau1", 100, 0.0, 1.0);
  h_SubldgFatJet_tau2 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "SubldgFatJet_tau2", "Subleading Fat Jet tau2",  100, 0.0, 1.0);
  h_SubldgFatJet_tau3 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "SubldgFatJet_tau3", "Subleading Fat Jet tau3",  100, 0.0, 1.0);
  h_SubldgFatJet_tau4 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "SubldgFatJet_tau4", "Subleading Fat Jet tau4",  100, 0.0, 1.0);
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
  /*
    if (0) std::cout << "=== Top (ChiSq) selection" << std::endl;
    const TopSelection::Data topData = fTopSelection.analyze(fEvent, jetData, bjetData);
    // Apply preliminary chiSq cut
    bool passPrelimChiSq = cfg_PrelimTopFitChiSqr.passedCut(topData.ChiSqr());
    if (!passPrelimChiSq) return;
  */
  if (0) std::cout << "=== Top (BDT) selection" << std::endl;
  const TopSelectionBDT::Data topData = fTopSelection.analyze(fEvent, jetData, bjetData, true);
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
  //if (0) std::cout << "=== Fat Jet selection" << std::endl;
  //const FatJetSelection::Data fatjetData = fFatJetSelection.analyzeWithoutTau(fEvent);
  //if (!fatjetData.passedSelection()) return;
  
  std::vector<AK8Jet> selectedAK8Jets;
  
  // AK8 Jets Analysis
  int nFatJets = 0;
  for(AK8Jet jet: fEvent.ak8jets())
    {      
      double pt  = jet.pt();
      double eta = jet.eta();
      
      double phi = jet.phi();
      double e   = jet.e();
      
      int pdgId  = jet.pdgId();
      
      // ID
      // bool jetID   = jet.jetIDDiscriminator();
      bool IDloose = jet.IDloose();
      // bool IDtight = jet.IDtight();
      // bool IDtightLeptonVeto = jet.IDtightLeptonVeto();

      // PU ID
      // bool jetPUID    = jet.jetPUIDDiscriminator();
      // bool PUIDloose  = jet.PUIDloose();
      // bool PUIDmedium = jet.PUIDmedium();
      // bool PUIDtight  = jet.PUIDtight();
      
      // originates From 
      // bool originatesFromChargedHiggs = jet.originatesFromChargedHiggs();
      // bool originatesFromTop          = jet.originatesFromTop();
      // bool originatesFromUnknown      = jet.originatesFromUnknown();
      // bool originatesFromW            = jet.originatesFromW();
      // bool originatesFromZ            = jet.originatesFromZ();

      // Njettiness
      double NjettinessAK8CHStau1 = jet.NjettinessAK8CHStau1();
      double NjettinessAK8CHStau2 = jet.NjettinessAK8CHStau2();
      double NjettinessAK8CHStau3 = jet.NjettinessAK8CHStau3();
      double NjettinessAK8CHStau4 = jet.NjettinessAK8CHStau4();
      
      // Discriminators
      float pfCombinedCvsBJetTags = jet.pfCombinedCvsBJetTags();
      float pfCombinedCvsLJetTags = jet.pfCombinedCvsLJetTags();
      float pfCombinedInclusiveSecondaryVertexV2BJetTags = jet.pfCombinedInclusiveSecondaryVertexV2BJetTags();
      float pfCombinedMVAV2BJetTags = jet.pfCombinedMVAV2BJetTags();
      
      // Flavours
      int hadronFlavour = jet.hadronFlavour();
      int partonFlavour = jet.partonFlavour();
      
      
      if (pt < 100.0) continue;
      if (std::abs(eta) > 2.4) continue;
      if (!IDloose) continue;
      

      selectedAK8Jets.push_back(jet);

      nFatJets++;
      
      // ----------------------------------------------------------------------------------
      h_FatJets_Pt  -> Fill(pt);
      h_FatJets_Eta -> Fill(eta);
      h_FatJets_Phi -> Fill(phi);
      h_FatJets_E   -> Fill(e);
      //
      h_FatJets_pdgId -> Fill(pdgId);
      h_FatJets_partonFlavour -> Fill(hadronFlavour);
      h_FatJets_hadronFlavour -> Fill(partonFlavour);
      //
      h_FatJets_CSVdiscr  -> Fill(pfCombinedInclusiveSecondaryVertexV2BJetTags);
      h_FatJets_MVAdiscr  -> Fill(pfCombinedMVAV2BJetTags);
      h_FatJets_CvsLdiscr -> Fill(pfCombinedCvsLJetTags);
      h_FatJets_CvsBdiscr -> Fill(pfCombinedCvsBJetTags);
      //
      h_FatJets_NjettinessAK8CHStau1 -> Fill(NjettinessAK8CHStau1);
      h_FatJets_NjettinessAK8CHStau2 -> Fill(NjettinessAK8CHStau2);
      h_FatJets_NjettinessAK8CHStau3 -> Fill(NjettinessAK8CHStau3);
      h_FatJets_NjettinessAK8CHStau4 -> Fill(NjettinessAK8CHStau4);
      //
      h_FatJets_tau21 -> Fill(NjettinessAK8CHStau2/NjettinessAK8CHStau1);
      h_FatJets_tau32 -> Fill(NjettinessAK8CHStau3/NjettinessAK8CHStau2);
      
      h_FatJets_IDLoose -> Fill(IDloose);
      // --------------------------------------------------------------------------------
    }
  
  h_FatJets_N -> Fill(nFatJets);
    
  int iJet = 0;
  for (auto jet: selectedAK8Jets){
    iJet++;
    
    if (iJet == 1){
      // Leading Jet
      h_LdgFatJet_Pt -> Fill(jet.pt());
      h_LdgFatJet_Eta -> Fill(jet.eta());
      h_LdgFatJet_Phi -> Fill(jet.phi());
      h_LdgFatJet_E   -> Fill(jet.e());
      h_LdgFatJet_CSVdiscr -> Fill(jet.pfCombinedInclusiveSecondaryVertexV2BJetTags());
      h_LdgFatJet_tau1 -> Fill(jet.NjettinessAK8CHStau1());
      h_LdgFatJet_tau2 -> Fill(jet.NjettinessAK8CHStau2());
      h_LdgFatJet_tau3 -> Fill(jet.NjettinessAK8CHStau3());
      h_LdgFatJet_tau4 -> Fill(jet.NjettinessAK8CHStau4());
      
      h_LdgFatJet_tau21 -> Fill(jet.NjettinessAK8CHStau2()/jet.NjettinessAK8CHStau1());
      h_LdgFatJet_tau32 -> Fill(jet.NjettinessAK8CHStau3()/jet.NjettinessAK8CHStau2());
      
      //h_LdgFatJet_NSubjets -> 
      //h_LdgFatJet_HasBSubjet ->
    }
    if (iJet == 2){
      // Subleading Jet
      h_SubldgFatJet_Pt -> Fill(jet.pt());
      h_SubldgFatJet_Eta -> Fill(jet.eta());
      h_SubldgFatJet_Phi -> Fill(jet.phi());
      h_SubldgFatJet_E   -> Fill(jet.e());
      h_SubldgFatJet_CSVdiscr -> Fill(jet.pfCombinedInclusiveSecondaryVertexV2BJetTags());
      h_SubldgFatJet_tau1 -> Fill(jet.NjettinessAK8CHStau1());
      h_SubldgFatJet_tau2 -> Fill(jet.NjettinessAK8CHStau2());
      h_SubldgFatJet_tau3 -> Fill(jet.NjettinessAK8CHStau3());
      h_SubldgFatJet_tau4 -> Fill(jet.NjettinessAK8CHStau4());
      
      h_SubldgFatJet_tau21 -> Fill(jet.NjettinessAK8CHStau2()/jet.NjettinessAK8CHStau1());
      h_SubldgFatJet_tau32 -> Fill(jet.NjettinessAK8CHStau3()/jet.NjettinessAK8CHStau2());
      //h_SubldgFatJet_NSubjets -> 
      //h_SubldgFatJet_HasBSubjet ->
    }
  }


  std::vector<AK8JetsSoftDrop> selectedAK8SoftDropJets;
  
  // AK8 Jets Analysis
  int jetSD_index = -1;
  for(AK8JetsSoftDrop jet: fEvent.ak8jetsSoftDrop())
    {
      jetSD_index++;
      
      double pt  = jet.pt();
      double eta = jet.eta();
      // double phi = jet.phi();
      // double e   = jet.e();
      // int pdgId  = jet.pdgId();
      
      // PU ID
      // bool jetPUID    = jet.jetPUIDDiscriminator();
      //bool PUIDloose  = jet.PUIDloose();
      //bool PUIDmedium = jet.PUIDmedium();
      //bool PUIDtight  = jet.PUIDtight();
      
      // originates From 
      // bool originatesFromChargedHiggs = jet.originatesFromChargedHiggs();
      // bool originatesFromTop          = jet.originatesFromTop();
      // bool originatesFromUnknown      = jet.originatesFromUnknown();
      // bool originatesFromW            = jet.originatesFromW();
      // bool originatesFromZ            = jet.originatesFromZ();
      
      // Discriminators
      // float pfCombinedInclusiveSecondaryVertexV2BJetTags = jet.pfCombinedInclusiveSecondaryVertexV2BJetTags();
      
      // Flavours
      // int hadronFlavour = jet.hadronFlavour();
      // int partonFlavour = jet.partonFlavour();
      
      int nSubJets      = jet.nSubjets();
      bool hasBTagSubjet= jet.hasBTagSubjets();
      
      // ID
      // bool jetID   = jet.jetIDDiscriminator();
      // bool IDloose = jet.IDloose();
      // bool IDtight = jet.IDtight();
      // bool IDtightLeptonVeto = jet.IDtightLeptonVeto();
      
      if (pt < 100) continue;
      if (std::abs(eta) > 2.4) continue;
      if (!jet.jetIDDiscriminator()) continue;
      
      h_FatJets_NSubjets   -> Fill(nSubJets);
      h_FatJets_HasBSubjet -> Fill(hasBTagSubjet);
      
      selectedAK8SoftDropJets.push_back(jet);
      
      //std::cout<<"soft drop jet = "<<jet_index<<" has "<<nSubJets<<" subjets & has b-tagged? "<<hasBTagSubjet<<std::endl;
    }
  //std::cout<<"Soft Drop Fat Jets: "<<jetSD_index<<std::endl;
  
  int iSDJet = 0;
  for (auto jet: selectedAK8SoftDropJets){
    iSDJet++;
    
    if (iSDJet == 1){
      // Leading Jet
      h_LdgFatJet_NSubjets -> Fill(jet.nSubjets());
      h_LdgFatJet_HasBSubjet -> Fill(jet.hasBTagSubjets());
    }
    if (iSDJet == 2){
      // Subleading Jet
      h_SubldgFatJet_NSubjets -> Fill(jet.nSubjets());
      h_SubldgFatJet_HasBSubjet -> Fill(jet.hasBTagSubjets());
    }
  }

  
  
  //================================================================================================
  // Other) Fat Jet SoftDrop selection
  //================================================================================================

  //std::cout << "=== Fat Jet SoftDrop selection" << std::endl;
  //const FatJetSoftDropSelection::Data fatjetSoftDropData = fFatJetSoftDropSelection.analyzeWithoutTau(fEvent);
  
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
