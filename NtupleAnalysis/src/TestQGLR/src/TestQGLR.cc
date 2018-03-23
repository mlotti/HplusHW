// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "Tools/interface/DirectionalCut.h"
#include "EventSelection/interface/EventSelections.h"
#include "EventSelection/interface/BJetSelection.h"

#include "TDirectory.h"
#include "Math/VectorUtil.h"

class TestQGLR: public BaseSelector {
public:
  explicit TestQGLR(const ParameterSet& config, const TH1* skimCounters);
  virtual ~TestQGLR();

  /// Books histograms
  virtual void book(TDirectory *dir) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;
  virtual bool isBJet(const Jet& jet, const std::vector<Jet>& bjets);
  virtual bool areSameJets(const Jet& jet1, const Jet& jet2);

private:
  // Input parameters (Baseline Bjets)
  const DirectionalCut<int> cfg_BaselineNumberOfBJets;
  const DirectionalCut<double> cfg_LdgTopMVACut;
  const DirectionalCut<double> cfg_SubldgTopMVACut;
  const DirectionalCut<double> cfg_MinTopMVACut;
  const std::string cfg_BjetDiscr;

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
  QuarkGluonLikelihoodRatio fQuarkGluonLikelihoodRatio;
  // Baseline selection      
  Count cBaselineBTaggingCounter;
  Count cBaselineBTaggingSFCounter;
  BJetSelection fBaselineBJetSelection;
  METSelection fBaselineMETSelection;
  TopSelectionBDT fBaselineTopSelection;
  Count cBaselineSelected;
  Count cBaselineSelectedCR;
  // Inverted selection
  Count cInvertedBTaggingCounter;
  Count cInvertedBTaggingSFCounter;
  BJetSelection fInvertedBJetSelection;
  METSelection fInvertedMETSelection;
  TopSelectionBDT fInvertedTopSelection;
  Count cInvertedSelected;
  Count cInvertedSelectedCR;

  void DoBaselineAnalysis(const JetSelection::Data& jetData, const BJetSelection::Data& bjetData, const int nVertices);
  void DoInvertedAnalysis(const JetSelection::Data& jetData, const BJetSelection::Data& bjetData, const int nVertices);

  // Sanity checks
  WrappedTH1Triplet* hQGLR_isGenuineB;
  
  // FakeB Triplets (Baseline)
  WrappedTH1Triplet* hBaseline_QGLR_AfterStandardSelections;
  
  // FakeB Triplets (Inverted)
  WrappedTH1Triplet* hInverted_QGLR_AfterStandardSelections;
};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(TestQGLR);

TestQGLR::TestQGLR(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    cfg_BaselineNumberOfBJets(config, "FakeBMeasurement.baselineBJetsCut"),
    cfg_LdgTopMVACut(config, "FakeBMeasurement.LdgTopMVACut"),
    cfg_SubldgTopMVACut(config, "FakeBMeasurement.SubldgTopMVACut"),
    cfg_MinTopMVACut(config, "FakeBMeasurement.minTopMVACut"),
    cfg_BjetDiscr(config.getParameter<std::string>("FakeBBjetSelection.bjetDiscr")),
    fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kHplus2tbAnalysis, fHistoWrapper),
    // fNormalizationSystematicsSignalRegion(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kQCDNormalizationSystematicsSignalRegion, fHistoWrapper), // fixme
    // fNormalizationSystematicsControlRegion(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kQCDNormalizationSystematicsControlRegion, fHistoWrapper),// fixme
    cAllEvents(fEventCounter.addCounter("All events")),
    cTrigger(fEventCounter.addCounter("Passed trigger")),
    fMETFilterSelection(config.getParameter<ParameterSet>("METFilter"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cVertexSelection(fEventCounter.addCounter("Passed PV")),
    fElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fMuonSelection(config.getParameter<ParameterSet>("MuonSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fTauSelection(config.getParameter<ParameterSet>("TauSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fJetSelection(config.getParameter<ParameterSet>("JetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fQuarkGluonLikelihoodRatio(config.getParameter<ParameterSet>("QGLRSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cBaselineBTaggingCounter(fEventCounter.addCounter("Baseline: passed b-jet selection")),
    cBaselineBTaggingSFCounter(fEventCounter.addCounter("Baseline: b tag SF")),
    fBaselineBJetSelection(config.getParameter<ParameterSet>("BJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fBaselineMETSelection(config.getParameter<ParameterSet>("METSelection")),
    fBaselineTopSelection(config.getParameter<ParameterSet>("TopSelectionBDT"), fEventCounter, fHistoWrapper, &fCommonPlots, "Baseline"),
    cBaselineSelected(fEventCounter.addCounter("Baseline: selected events")),
    cBaselineSelectedCR(fEventCounter.addCounter("Baseline: selected CR events")),
    cInvertedBTaggingCounter(fEventCounter.addCounter("Inverted: passed b-jet selection")),
    cInvertedBTaggingSFCounter(fEventCounter.addCounter("Inverted: b tag SF")),
    fInvertedBJetSelection(config.getParameter<ParameterSet>("FakeBBjetSelection")),//, fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fInvertedMETSelection(config.getParameter<ParameterSet>("METSelection")),
    fInvertedTopSelection(config.getParameter<ParameterSet>("TopSelectionBDT"), fEventCounter, fHistoWrapper, &fCommonPlots, "Inverted"),
    cInvertedSelected(fEventCounter.addCounter("Inverted: selected events")),
    cInvertedSelectedCR(fEventCounter.addCounter("Inverted: selected CR events"))
{ }


TestQGLR::~TestQGLR() {  
 
  // Non-common histograms
  delete hQGLR_isGenuineB;

  // FakeB Triplets (Baseline)
  delete hBaseline_QGLR_AfterStandardSelections;

  // FakeB Triplets (Inverted)
  delete hInverted_QGLR_AfterStandardSelections;
}

void TestQGLR::book(TDirectory *dir) {

  std::string myInclusiveLabel  = "Triplets";
  std::string myFakeLabel       = myInclusiveLabel+"False";
  std::string myGenuineLabel    = myInclusiveLabel+"True";
  TDirectory* myInclusiveDir    = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabel);
  TDirectory* myFakeDir         = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
  TDirectory* myGenuineDir      = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
  std::vector<TDirectory*> myDirs = {myInclusiveDir, myFakeDir, myGenuineDir};
  
  // Book common plots histograms
  fCommonPlots.book(dir, isData());
  
  // Book histograms in event selection classes
  fMETFilterSelection.bookHistograms(dir);
  fElectronSelection.bookHistograms(dir);
  fMuonSelection.bookHistograms(dir);
  fTauSelection.bookHistograms(dir);
  fJetSelection.bookHistograms(dir);
  fQuarkGluonLikelihoodRatio.bookHistograms(dir);
  // Baseline selection
  fBaselineBJetSelection.bookHistograms(dir);
  fBaselineMETSelection.bookHistograms(dir);
  fBaselineTopSelection.bookHistograms(dir);
  // Inverted selection
  fInvertedBJetSelection.bookHistograms(dir);
  fInvertedMETSelection.bookHistograms(dir);
  fInvertedTopSelection.bookHistograms(dir);
  
  // ====== Histogram settings
  HistoSplitter histoSplitter = fCommonPlots.getHistoSplitter();
  
  // Histogram binning options
  int nQGLBins      = 100;
  float fQGLMin     = 0.0;
  float fQGLMax     = 1.0;
  
  // Book normal histograms
  hQGLR_isGenuineB = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myDirs, "QGLR_isGenuineB", "Quark-Gluon likelihood ratio", nQGLBins, fQGLMin, fQGLMax);
  
  // Other hustograms
  myInclusiveLabel = "ForFakeBMeasurement";
  myFakeLabel      = myInclusiveLabel+"EWKFakeB";
  myGenuineLabel   = myInclusiveLabel+"EWKGenuineB";

  // Create directories
  TDirectory* myFakeBDir         = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabel);
  TDirectory* myFakeBEWKFakeBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
  TDirectory* myFakeBGenuineBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
  std::vector<TDirectory*> myFakeBDirs = {myFakeBDir, myFakeBEWKFakeBDir, myFakeBGenuineBDir};

  // Baseline selection (StandardSelections)
  hBaseline_QGLR_AfterStandardSelections = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_QGLR_AfterStandardSelections", "Quark-Gluon likelihood ratio / %.0f", nQGLBins, fQGLMin, fQGLMax);
  hInverted_QGLR_AfterStandardSelections = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_QGLR_AfterStandardSelections", "Quark-Gluon likelihood ratio / %.0f", nQGLBins, fQGLMin, fQGLMax);
  
  return;
}


void TestQGLR::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
  return;
}


void TestQGLR::process(Long64_t entry) {

  //====== Initialize
  fCommonPlots.initialize();
  
  cAllEvents.increment();
  int nVertices = fEvent.vertexInfo().value();
  fCommonPlots.setNvertices(nVertices);

  if (0) std::cout << "\nentry = " << entry << std::endl;

  //================================================================================================   
  // 1) Apply trigger 
  //================================================================================================   
  if (0) std::cout << "=== Trigger" << std::endl;
  if ( !(fEvent.passTriggerDecision()) ) return;

  cTrigger.increment();
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
  // 4) Electron veto (Orthogonality)
  //================================================================================================   
  if (0) std::cout << "=== Electron veto" << std::endl;
  const ElectronSelection::Data eData = fElectronSelection.analyze(fEvent);
  if (eData.hasIdentifiedElectrons()) return;

  //================================================================================================
  // 5) Muon veto (Orthogonality)
  //================================================================================================
  if (0) std::cout << "=== Muon veto" << std::endl;
  const MuonSelection::Data muData = fMuonSelection.analyze(fEvent);
  if (muData.hasIdentifiedMuons()) return;

  //================================================================================================   
  // 6) Tau Veto (HToTauNu Orthogonality)
  //================================================================================================   
  if (0) std::cout << "=== Tau-Veto" << std::endl;
  const TauSelection::Data tauData = fTauSelection.analyze(fEvent);
  if (tauData.hasIdentifiedTaus() ) return;

  //================================================================================================
  // 7) Jet Selection
  //================================================================================================
  if (0) std::cout << "=== Jet selection" << std::endl;
  const JetSelection::Data jetData = fJetSelection.silentAnalyzeWithoutTau(fEvent);
  if (!jetData.passedSelection()) return;
  
  //================================================================================================  
  // 8) BJet Selection
  //================================================================================================
  if (0) std::cout << "=== BJet selection" << std::endl;
  const BJetSelection::Data bjetData = fBaselineBJetSelection.silentAnalyze(fEvent, jetData);

  // Baseline Selection
  if (bjetData.passedSelection())
    {
      DoBaselineAnalysis(jetData, bjetData, nVertices);
    }
  else
    {
      // CSVv2-Medium
      bool passMediumCuts = cfg_BaselineNumberOfBJets.passedCut(bjetData.getSelectedBJets().size());
      if (!passMediumCuts) return;
      
      // Do inverted if multiplicity requirement on CSVv2-Medium  is met
      DoInvertedAnalysis(jetData, bjetData, nVertices);
    }
  return;
}
      

bool TestQGLR::isBJet(const Jet& jet, const std::vector<Jet>& bjets) {
  for (auto bjet: bjets)
    {
      if (areSameJets(jet, bjet)) return true;
    }
  return false;
}

bool TestQGLR::areSameJets(const Jet& jet1, const Jet& jet2) {
  float dR = ROOT::Math::VectorUtil::DeltaR(jet1.p4(), jet2.p4());
  float dR_match = 0.1;
  if (dR <= dR_match) return true;
  else return false;
}


void TestQGLR::DoBaselineAnalysis(const JetSelection::Data& jetData,
                                          const BJetSelection::Data& bjetData,
                                          const int nVertices){
  // Increment counter
  cBaselineBTaggingCounter.increment();

  //================================================================================================  
  // 9) BJet SF  
  //================================================================================================
  if (0) std::cout << "=== Baseline: BJet SF" << std::endl;
  if (fEvent.isMC()) 
    {
      fEventWeight.multiplyWeight(bjetData.getBTaggingScaleFactorEventWeight());
    }
  cBaselineBTaggingSFCounter.increment();

  //================================================================================================
  // 10) MET selection
  //================================================================================================
  if (0) std::cout << "=== Baseline: MET selection" << std::endl;
  const METSelection::Data METData = fBaselineMETSelection.silentAnalyze(fEvent, nVertices);
  // if (!METData.passedSelection()) return;
 
  //================================================================================================
  // 11) Top selection
  //================================================================================================
  if (0) std::cout << "=== Baseline: Top selection" << std::endl;
  const TopSelectionBDT::Data topData = fBaselineTopSelection.analyze(fEvent, jetData, bjetData);
  bool passMinTopMVACut = cfg_MinTopMVACut.passedCut( std::min(topData.getMVAmax1(), topData.getMVAmax2()) );
  bool hasFreeBJet      = topData.hasFreeBJet();
  if (!hasFreeBJet) return;
  if (!passMinTopMVACut) return;

  // Defining the splitting of phase-space as the eta of the Tetrajet b-jet
  std::vector<float> myFactorisationInfo;
  myFactorisationInfo.push_back(topData.getTetrajetBJet().eta() );
  fCommonPlots.setFactorisationBinForEvent(myFactorisationInfo);
  // fNormalizationSystematicsSignalRegion.setFactorisationBinForEvent(myFactorisationInfo); //fixme

  // If 1 or more untagged genuine bjets are found the event is considered fakeB. Otherwise genuineB  
  bool isGenuineB = bjetData.isGenuineB();
    
  //================================================================================================
  // Preselections (aka Standard Selections)
  //================================================================================================
  if (0) std::cout << "=== Baseline: Standard Selections" << std::endl;
  
  
  //================================================================================================
  // All Selections
  //================================================================================================  
  if (!topData.passedSelection()) return;

  if (0) std::cout << "=== Baseline: Signal Region (SR)" << std::endl;
  cBaselineSelected.increment();

  //================================================================================================
  // QGLR Selection
  //================================================================================================
  const QuarkGluonLikelihoodRatio::Data qglData = fQuarkGluonLikelihoodRatio.analyze(fEvent, jetData, bjetData);
  double QGLR = qglData.getQGLR();
  
  // Fill Triplets (Baseline)
  hBaseline_QGLR_AfterStandardSelections -> Fill(isGenuineB, QGLR);

  //================================================================================================
  // Fill final plots
  //================================================================================================
  
  // Save selected event ID for pick events
  fEventSaver.save();

  return;
}

void TestQGLR::DoInvertedAnalysis(const JetSelection::Data& jetData,
				  const BJetSelection::Data& bjetData,
				  const int nVertices){

  if (0) std::cout << "\n=== TestQGLR::DoInvertedAnalysis()" << std::endl;

  //================================================================================================  
  // 8) BJet Selection
  //================================================================================================
  if (0) std::cout << "=== Inverted: BJet selection" << std::endl;
  const BJetSelection::Data invBjetData = fInvertedBJetSelection.silentAnalyze(fEvent, jetData);
  if (!invBjetData.passedSelection()) return;

  // Increment counter
  cInvertedBTaggingCounter.increment();

  //================================================================================================  
  // 9) BJet SF  
  //================================================================================================
  if (0) std::cout << "=== Inverted: BJet SF" << std::endl;
  if (fEvent.isMC()) 
    { 
      fEventWeight.multiplyWeight(invBjetData.getBTaggingScaleFactorEventWeight());
    }
  cInvertedBTaggingSFCounter.increment();

  //================================================================================================
  // 10) MET selection
  //================================================================================================
  if (0) std::cout << "=== Inverted: MET selection" << std::endl;
  const METSelection::Data METData = fInvertedMETSelection.silentAnalyze(fEvent, nVertices);
  // if (!METData.passedSelection()) return;

  //================================================================================================
  // 11) Top selection
  //================================================================================================
  if (0) std::cout << "=== Inverted: Top selection" << std::endl;
  const TopSelectionBDT::Data topData = fInvertedTopSelection.analyze(fEvent, jetData, invBjetData);
  bool passMinTopMVACut = cfg_MinTopMVACut.passedCut( std::min(topData.getMVAmax1(), topData.getMVAmax2()) );
  bool hasFreeBJet      = topData.hasFreeBJet();
  if (!hasFreeBJet) return;
  if (!passMinTopMVACut) return;

  // Defining the splitting of phase-space as the eta of the Tetrajet b-jet
  std::vector<float> myFactorisationInfo;
  myFactorisationInfo.push_back(topData.getTetrajetBJet().eta() );
  fCommonPlots.setFactorisationBinForEvent(myFactorisationInfo);
  
  // If 1 or more untagged genuine bjets are found the event is considered fakeB. Otherwise genuineB
  bool isGenuineB = invBjetData.isGenuineB();
  
  //================================================================================================
  // Preselections (aka Standard Selections)
  //================================================================================================
  if (0) std::cout << "=== Inverted: Preselections" << std::endl;
  // fCommonPlots.fillControlPlotsAfterStandardSelections(fEvent, jetData, invBjetData, METData, TopologySelection::Data(), topData, isGenuineB);
  // fCommonPlots.fillControlPlotsAfterStandardSelections(fEvent, jetData, invBjetData, qglData, topData, isGenuineB);
  
  //================================================================================================
  // All Selections 
  //================================================================================================
  if (!topData.passedSelection()) return;
  
  if (0) std::cout << "=== Inverted: Verification Region (VR)" << std::endl;
  cInvertedSelected.increment();
  
  //================================================================================================
  // QGLR Selection
  //================================================================================================
  const QuarkGluonLikelihoodRatio::Data qglData = fQuarkGluonLikelihoodRatio.analyze(fEvent, jetData, bjetData);
  double QGLR = qglData.getQGLR();

  hInverted_QGLR_AfterStandardSelections -> Fill(isGenuineB, QGLR);
    
  // Save selected event ID for pick events
  fEventSaver.save();

  return;
}
