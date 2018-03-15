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
  const std::string cfg_BaselineBJetsDiscr;
  const std::string cfg_BaselineBJetsDiscrWP;
  const DirectionalCut<double> cfg_LdgTopMVACut;
  const DirectionalCut<double> cfg_SubldgTopMVACut;
  const DirectionalCut<double> cfg_MinTopMVACut;
  const std::string cfg_BjetDiscr;

  // Common plots
  CommonPlots fCommonPlots;
  // CommonPlots fNormalizationSystematicsSignalRegion;  // fixme
  // CommonPlots fNormalizationSystematicsControlRegion; // fixme

  // Event selection classes and event counters (in same order like they are applied)
  Count cAllEvents;
  Count cTrigger;
  METFilterSelection fMETFilterSelection;
  Count cVertexSelection;
  ElectronSelection fElectronSelection;
  MuonSelection fMuonSelection;
  TauSelection fTauSelection;
  JetSelection fJetSelection;
  // Baseline selection      
  Count cBaselineBTaggingCounter;
  Count cBaselineBTaggingSFCounter;
  BJetSelection fBaselineBJetSelection;
  METSelection fBaselineMETSelection;
  QuarkGluonLikelihoodRatio fBaselineQGLRSelection;
  TopSelectionBDT fBaselineTopSelection;
  FatJetSelection fBaselineFatJetSelection;
  Count cBaselineSelected;
  Count cBaselineSelectedCR;
  // Inverted selection
  Count cInvertedBTaggingCounter;
  Count cInvertedBTaggingSFCounter;
  BJetSelection fInvertedBJetSelection;
  METSelection fInvertedMETSelection;
  QuarkGluonLikelihoodRatio fInvertedQGLRSelection;
  TopSelectionBDT fInvertedTopSelection;
  FatJetSelection fInvertedFatJetSelection;
  Count cInvertedSelected;
  Count cInvertedSelectedCR;

  void DoBaselineAnalysis(const JetSelection::Data& jetData, const BJetSelection::Data& bjetData, const int nVertices);
  void DoInvertedAnalysis(const JetSelection::Data& jetData, const int nVertices);

  // Splitted histograms
  HistoSplitter::SplittedTripletTH1s hQGLR_CRone;
  HistoSplitter::SplittedTripletTH1s hQGLR_SR;
  HistoSplitter::SplittedTripletTH1s hQGLR_CRtwo;
  HistoSplitter::SplittedTripletTH1s hQGLR_VR;
  
  // Sanity checks
  WrappedTH1 *hBaseline_IsGenuineB; 
  WrappedTH1 *hInverted_IsGenuineB; 

  // FakeB Triplets (Baseline)
  WrappedTH1Triplet *hBaseline_QGLR_AfterStandardSelections;
  WrappedTH1Triplet *hBaseline_QGLR_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_QGLR_AfterCRSelections;

  // FakeB Triplets (Inverted)
  WrappedTH1Triplet *hInverted_QGLR_AfterStandardSelections;
  WrappedTH1Triplet *hInverted_QGLR_AfterAllSelections;
  WrappedTH1Triplet *hInverted_QGLR_AfterCRSelections;
  
};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(TestQGLR);

TestQGLR::TestQGLR(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    cfg_BaselineNumberOfBJets(config, "FakeBMeasurement.baselineBJetsCut"),
    cfg_BaselineBJetsDiscr(config.getParameter<std::string>("FakeBMeasurement.baselineBJetsDiscr")),
    cfg_BaselineBJetsDiscrWP(config.getParameter<std::string>("FakeBMeasurement.baselineBJetsDiscrWP")),
    cfg_LdgTopMVACut(config, "FakeBMeasurement.LdgTopMVACut"),
    cfg_SubldgTopMVACut(config, "FakeBMeasurement.SubldgTopMVACut"),
    cfg_MinTopMVACut(config, "FakeBMeasurement.minTopMVACut"),
    cfg_BjetDiscr(config.getParameter<std::string>("FakeBBjetSelection.bjetDiscr")),
    fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kFakeBMeasurement, fHistoWrapper),
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
    cBaselineBTaggingCounter(fEventCounter.addCounter("Baseline: passed b-jet selection")),
    cBaselineBTaggingSFCounter(fEventCounter.addCounter("Baseline: b tag SF")),
    fBaselineBJetSelection(config.getParameter<ParameterSet>("BJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fBaselineMETSelection(config.getParameter<ParameterSet>("METSelection")),
    fBaselineQGLRSelection(config.getParameter<ParameterSet>("QGLRSelection")),// fEventCounter, fHistoWrapper, &fCommonPlots, "Baseline"),
    fBaselineTopSelection(config.getParameter<ParameterSet>("TopSelectionBDT"), fEventCounter, fHistoWrapper, &fCommonPlots, "Baseline"),
    fBaselineFatJetSelection(config.getParameter<ParameterSet>("FatJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Baseline"),
    cBaselineSelected(fEventCounter.addCounter("Baseline: selected events")),
    cBaselineSelectedCR(fEventCounter.addCounter("Baseline: selected CR events")),
    cInvertedBTaggingCounter(fEventCounter.addCounter("Inverted: passed b-jet selection")),
    cInvertedBTaggingSFCounter(fEventCounter.addCounter("Inverted: b tag SF")),
    fInvertedBJetSelection(config.getParameter<ParameterSet>("FakeBBjetSelection")),//, fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fInvertedMETSelection(config.getParameter<ParameterSet>("METSelection")),
    fInvertedQGLRSelection(config.getParameter<ParameterSet>("QGLRSelection")),// fEventCounter, fHistoWrapper, &fCommonPlots, "Inverted"),
    fInvertedTopSelection(config.getParameter<ParameterSet>("TopSelectionBDT"), fEventCounter, fHistoWrapper, &fCommonPlots, "Inverted"),
    fInvertedFatJetSelection(config.getParameter<ParameterSet>("FatJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Inverted"),
    cInvertedSelected(fEventCounter.addCounter("Inverted: selected events")),
    cInvertedSelectedCR(fEventCounter.addCounter("Inverted: selected CR events"))
{ }


TestQGLR::~TestQGLR() {  
  // CRone (Baseline b-jets, Inverted Top MVA2)
  fCommonPlots.getHistoSplitter().deleteHistograms(hQGLR_CRone);
  // SR (Baseline b-jets, Baseline Top MVA2)
  fCommonPlots.getHistoSplitter().deleteHistograms(hQGLR_SR);
  // VR (Inverted b-jets, Inverted Top MVA2)
  fCommonPlots.getHistoSplitter().deleteHistograms(hQGLR_CRtwo);
  // VR (Inverted b-jets, Baseline Top MVA2)
  fCommonPlots.getHistoSplitter().deleteHistograms(hQGLR_VR);

  // FakeB Triplets (Baseline)
  delete hBaseline_QGLR_AfterStandardSelections;
  delete hBaseline_QGLR_AfterAllSelections;
  delete hBaseline_QGLR_AfterCRSelections;

  // FakeB Triplets (Inverted)
  delete hInverted_QGLR_AfterStandardSelections;
  delete hInverted_QGLR_AfterAllSelections;
  delete hInverted_QGLR_AfterCRSelections;
}

void TestQGLR::book(TDirectory *dir) {

  
  // Book common plots histograms
  fCommonPlots.book(dir, isData());
  // fNormalizationSystematicsSignalRegion.book(dir, isData()); // fixme
  // fNormalizationSystematicsControlRegion.book(dir, isData()); // fixme

  // Book histograms in event selection classes
  fMETFilterSelection.bookHistograms(dir);
  fElectronSelection.bookHistograms(dir);
  fMuonSelection.bookHistograms(dir);
  fTauSelection.bookHistograms(dir);
  fJetSelection.bookHistograms(dir);
  // Baseline selection
  fBaselineBJetSelection.bookHistograms(dir);
  fBaselineMETSelection.bookHistograms(dir);
  fBaselineQGLRSelection.bookHistograms(dir);
  fBaselineTopSelection.bookHistograms(dir);
  fBaselineFatJetSelection.bookHistograms(dir);
  // Inverted selection
  fInvertedBJetSelection.bookHistograms(dir);
  fInvertedMETSelection.bookHistograms(dir);
  fInvertedQGLRSelection.bookHistograms(dir);
  fInvertedTopSelection.bookHistograms(dir);
  fInvertedFatJetSelection.bookHistograms(dir);
  
  // ====== Histogram settings
  HistoSplitter histoSplitter = fCommonPlots.getHistoSplitter();

  // Obtain binning
  const int nQGLRBins = 100;
  const float fQGLRMin = 0.0;
  const float fQGLRMax = 1.0;
  /*
  const int nNBins        = fCommonPlots.getNjetsBinSettings().bins();
  const float fNMin       = fCommonPlots.getNjetsBinSettings().min();
  const float fNMax       = fCommonPlots.getNjetsBinSettings().max();

  const int nBtagBins     = fCommonPlots.getBJetDiscBinSettings().bins();
  const float fBtagMin    = fCommonPlots.getBJetDiscBinSettings().min();
  const float fBtagMax    = fCommonPlots.getBJetDiscBinSettings().max();
  
  const int  nPtBins      = 2*fCommonPlots.getPtBinSettings().bins();
  const float fPtMin      = 2*fCommonPlots.getPtBinSettings().min();
  const float fPtMax      = 2*fCommonPlots.getPtBinSettings().max();

  const int  nEtaBins     = fCommonPlots.getEtaBinSettings().bins();
  const float fEtaMin     = fCommonPlots.getEtaBinSettings().min();
  const float fEtaMax     = fCommonPlots.getEtaBinSettings().max();

  const int  nBDiscBins   = fCommonPlots.getBJetDiscBinSettings().bins();
  const float fBDiscMin   = fCommonPlots.getBJetDiscBinSettings().min();
  const float fBDiscMax   = fCommonPlots.getBJetDiscBinSettings().max();

  const int nDEtaBins     = fCommonPlots.getDeltaEtaBinSettings().bins();
  const double fDEtaMin   = fCommonPlots.getDeltaEtaBinSettings().min();
  const double fDEtaMax   = fCommonPlots.getDeltaEtaBinSettings().max();

  const int nDPhiBins     = fCommonPlots.getDeltaPhiBinSettings().bins();
  const double fDPhiMin   = fCommonPlots.getDeltaPhiBinSettings().min();
  const double fDPhiMax   = fCommonPlots.getDeltaPhiBinSettings().max();

  const int nDRBins       = fCommonPlots.getDeltaRBinSettings().bins();
  const double fDRMin     = fCommonPlots.getDeltaRBinSettings().min();
  const double fDRMax     = fCommonPlots.getDeltaRBinSettings().max();

  const int nWMassBins    = fCommonPlots.getWMassBinSettings().bins();
  const float fWMassMin   = fCommonPlots.getWMassBinSettings().min();
  const float fWMassMax   = fCommonPlots.getWMassBinSettings().max();

  const int nTopMassBins  = fCommonPlots.getTopMassBinSettings().bins();
  const float fTopMassMin = fCommonPlots.getTopMassBinSettings().min();
  const float fTopMassMax = fCommonPlots.getTopMassBinSettings().max();

  const int nInvMassBins  = fCommonPlots.getInvMassBinSettings().bins();
  const float fInvMassMin = fCommonPlots.getInvMassBinSettings().min();
  const float fInvMassMax = fCommonPlots.getInvMassBinSettings().max();

  const int nMetBins  = fCommonPlots.getMetBinSettings().bins();
  const float fMetMin = fCommonPlots.getMetBinSettings().min();
  const float fMetMax = fCommonPlots.getMetBinSettings().max();

  const int nHtBins  = fCommonPlots.getHtBinSettings().bins();
  const float fHtMin = fCommonPlots.getHtBinSettings().min();
  const float fHtMax = fCommonPlots.getHtBinSettings().max();
  */
  
  // Create directories for normalization
  std::string myInclusiveLabel  = "ForFakeBSanity";
  std::string myFakeLabel       = myInclusiveLabel+"EWKFakeB";
  std::string myGenuineLabel    = myInclusiveLabel+"EWKGenuineB";
  // TDirectory* myNormDir         = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabel);
  // TDirectory* myNormEWKFakeBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
  // TDirectory* myNormGenuineBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
  // std::vector<TDirectory*> myNormalizationDirs = {myNormDir, myNormEWKFakeBDir, myNormGenuineBDir};
  
  // Other histograms
  myInclusiveLabel = "ForTestQGLR";
  myFakeLabel      = myInclusiveLabel+"EWKFakeB";
  myGenuineLabel   = myInclusiveLabel+"EWKGenuineB";
  // Create directories
  TDirectory* myFakeBDir         = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabel);
  TDirectory* myFakeBEWKFakeBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
  TDirectory* myFakeBGenuineBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
  std::vector<TDirectory*> myFakeBDirs = {myFakeBDir, myFakeBEWKFakeBDir, myFakeBGenuineBDir};
  
  // Splitted Histo Triplets
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hQGLR_CRone, "QGLR_CRone", ";QGLR;Occur / %0.f", nQGLRBins, fQGLRMin, fQGLRMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hQGLR_SR, "QGLR_SR", ";QGLR;Occur / %0.f", nQGLRBins, fQGLRMin, fQGLRMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hQGLR_CRtwo, "QGLR_CRtwo", ";QGLR;Occur / %0.f", nQGLRBins, fQGLRMin, fQGLRMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myFakeBDirs, hQGLR_VR, "QGLR_VR", ";QGLR;Occur / %0.f", nQGLRBins, fQGLRMin, fQGLRMax);

  // Normal Histos
  hBaseline_IsGenuineB = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, myFakeBDir, "Baseline_IsGenuineB", ";is genuine-b;Events / %0.0f", 2, 0.0, 2.0);
  hInverted_IsGenuineB = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, myFakeBDir, "Inverted_IsGenuineB", ";is genuine-b;Events / %0.0f", 2, 0.0, 2.0);

  // Baseline selection (StandardSelections)
  hBaseline_QGLR_AfterStandardSelections = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_QGLR_AfterStandardSelections", ";QGLR;Occur / %.0f", nQGLRBins, fQGLRMin, fQGLRMax);
  // Baseline selection (AllSelections)
  hBaseline_QGLR_AfterAllSelections = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_QGLR_AfterAllSelections", ";QGLR;Occur / %.0f", nQGLRBins, fQGLRMin, fQGLRMax);
  // Baseline selection (CRSelections)
  hBaseline_QGLR_AfterCRSelections = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_QGLR_AfterCRSelections", ";QGLR;Occur / %.0f", nQGLRBins, fQGLRMin, fQGLRMax);

  // Inverted selection (StandardSelections)
  hInverted_QGLR_AfterStandardSelections = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_QGLR_AfterStandardSelections", ";QGLR;Occur / %.0f", nQGLRBins, fQGLRMin, fQGLRMax);
  // Inverted selection (AllSelections)
  hInverted_QGLR_AfterAllSelections = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_QGLR_AfterAllSelections", ";QGLR;Occur / %.0f", nQGLRBins, fQGLRMin, fQGLRMax);
  // Inverted selection (CRSelections)
  hInverted_QGLR_AfterCRSelections = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Inverted_QGLR_AfterCRSelections", ";QGLR;Occur / %.0f", nQGLRBins, fQGLRMin, fQGLRMax);

  return;
}


void TestQGLR::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
  return;
}


void TestQGLR::process(Long64_t entry) {

  //====== Initialize
  fCommonPlots.initialize();
  // fNormalizationSystematicsSignalRegion.initialize();  // fixme
  // fNormalizationSystematicsControlRegion.initialize(); // fixme

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
      DoInvertedAnalysis(jetData, nVertices); 
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

  if (0) std::cout << "\n=== TestQGLR::DoBaselineAnalysis()" << std::endl;

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
  // - MET selection
  //================================================================================================
  if (0) std::cout << "=== Baseline: MET selection" << std::endl;
  const METSelection::Data METData = fBaselineMETSelection.silentAnalyze(fEvent, nVertices);
  // if (!METData.passedSelection()) return;

  //================================================================================================
  // 10) Quark-Gluon Likelihood Ratio Selection
  //================================================================================================
  if (0) std::cout << "=== Baseline: QGLR selection" << std::endl;
  const QuarkGluonLikelihoodRatio::Data QGLRData = fBaselineQGLRSelection.analyze(fEvent, jetData, bjetData);
  if (!QGLRData.passedSelection()) return;

  //================================================================================================
  // 11) Top selection
  //================================================================================================
  if (0) std::cout << "=== Baseline: Top selection" << std::endl;
  const TopSelectionBDT::Data topData = fBaselineTopSelection.analyze(fEvent, jetData, bjetData);
  bool passMinTopMVACut = cfg_MinTopMVACut.passedCut( std::min(topData.getMVAmax1(), topData.getMVAmax2()) );
  bool hasFreeBJet      = topData.hasFreeBJet();
  if (!hasFreeBJet) return;
  if (!passMinTopMVACut) return;

  //================================================================================================
  // *) FatJet veto
  //================================================================================================
  if (0) std::cout << "\n=== Baseline: FatJet veto" << std::endl;
  const FatJetSelection::Data fatjetData = fBaselineFatJetSelection.analyze(fEvent, topData);
  if (!fatjetData.passedSelection()) return;


  // Defining the splitting of phase-space as the eta of the Tetrajet b-jet
  std::vector<float> myFactorisationInfo;
  // myFactorisationInfo.push_back(topData.getTetrajetBJet().pt() ); //new
  myFactorisationInfo.push_back(topData.getTetrajetBJet().eta() );
  fCommonPlots.setFactorisationBinForEvent(myFactorisationInfo);
  // fNormalizationSystematicsSignalRegion.setFactorisationBinForEvent(myFactorisationInfo); //fixme

  // If 1 or more untagged genuine bjets are found the event is considered fakeB. Otherwise genuineB  
  bool isGenuineB = bjetData.isGenuineB();
  hBaseline_IsGenuineB->Fill(isGenuineB);
  
  //================================================================================================
  // Preselections (aka Standard Selections)
  //================================================================================================
  if (0) std::cout << "=== Baseline: Standard Selections" << std::endl;
  // NB: CtrlPlotsAfterStandardSelections should only be called for Inverted!
  // fCommonPlots.fillControlPlotsAfterStandardSelections(fEvent, jetData, bjetData, METData, topologyData, topData, bjetData.isGenuineB());

  // Fill Triplets  (Baseline)
  hBaseline_QGLR_AfterStandardSelections->Fill(isGenuineB, QGLRData.getQGLR());

  //================================================================================================
  // All Selections
  //================================================================================================  
  if (!topData.passedSelection()) 
    {
      // If top fails fill determine if it qualifies for Control Region 1 (CRone)
      bool passLdgTopMVA    = cfg_LdgTopMVACut.passedCut( topData.getMVAmax1() );
      bool passSubldgTopMVA = cfg_SubldgTopMVACut.passedCut( topData.getMVAmax2() );
      bool passInvertedTop  = passLdgTopMVA * passSubldgTopMVA;
      if (!passInvertedTop) return;

      if (0) std::cout << "=== Baseline: Control Region 1 (CRone)" << std::endl;
      cBaselineSelectedCR.increment();

      // Fill histos (CR1)
      hBaseline_QGLR_AfterCRSelections->Fill(isGenuineB, QGLRData.getQGLR());

      // Splitted histos
      fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hQGLR_CRone, isGenuineB, QGLRData.getQGLR());
      
      return;
    }

  if (0) std::cout << "=== Baseline: Signal Region (SR)" << std::endl;
  cBaselineSelected.increment();

  //================================================================================================
  // Fill final plots
  //================================================================================================
  hBaseline_QGLR_AfterAllSelections->Fill(isGenuineB, QGLRData.getQGLR());
  
  // Splitted Histos
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hQGLR_SR, isGenuineB, QGLRData.getQGLR());

  // Save selected event ID for pick events
  fEventSaver.save();

  return;
}

void TestQGLR::DoInvertedAnalysis(const JetSelection::Data& jetData,
					  const int nVertices){

  if (0) std::cout << "\n=== TestQGLR::DoInvertedAnalysis()" << std::endl;

  //================================================================================================  
  // 8) BJet Selections
  //================================================================================================
  if (0) std::cout << "=== Inverted: BJet selection" << std::endl;
  const BJetSelection::Data invBjetData = fInvertedBJetSelection.silentAnalyze(fEvent, jetData);
  if (!invBjetData.passedSelection()) return;

   // CSVv2-Medium requirement
   unsigned int nBaselineBjets = 0;
   double bdiscWP = fInvertedBJetSelection.getDiscriminatorWP( cfg_BaselineBJetsDiscr, cfg_BaselineBJetsDiscrWP);

   for (auto bjet: invBjetData.getSelectedBJets())
     {
       if (bjet.bjetDiscriminator() < bdiscWP) continue;
       nBaselineBjets++;
     }
   bool passBaselineBjetCuts   = cfg_BaselineNumberOfBJets.passedCut(nBaselineBjets); 
   if (!passBaselineBjetCuts) return;
  
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
  // - MET selection
  //================================================================================================
  if (0) std::cout << "=== Inverted: MET selection" << std::endl;
  const METSelection::Data METData = fInvertedMETSelection.silentAnalyze(fEvent, nVertices);
  // if (!METData.passedSelection()) return;

  //================================================================================================
  // 10) Quark-Gluon Likelihood Ratio Selection
  //================================================================================================
  if (0) std::cout << "=== Inverted: QGLR selection" << std::endl;
  const QuarkGluonLikelihoodRatio::Data QGLRData = fInvertedQGLRSelection.analyze(fEvent, jetData, invBjetData);
  if (!QGLRData.passedSelection()) return;

  //================================================================================================
  // 11) Top selection
  //================================================================================================
  if (0) std::cout << "=== Inverted: Top selection" << std::endl;
  const TopSelectionBDT::Data topData = fInvertedTopSelection.analyzeWithoutBJets(fEvent, jetData.getSelectedJets(), invBjetData.getSelectedBJets(), true);
  bool passMinTopMVACut = cfg_MinTopMVACut.passedCut( std::min(topData.getMVAmax1(), topData.getMVAmax2()) );
  bool hasFreeBJet      = topData.hasFreeBJet();
  if (!hasFreeBJet) return;
  if (!passMinTopMVACut) return;

  //================================================================================================
  // *) FatJet veto
  //================================================================================================
  if (0) std::cout << "\n=== Inverted: FatJet veto" << std::endl;
  const FatJetSelection::Data fatjetData = fInvertedFatJetSelection.analyze(fEvent, topData);
  if (!fatjetData.passedSelection()) return;


  // Defining the splitting of phase-space as the eta of the Tetrajet b-jet
  std::vector<float> myFactorisationInfo;
  // myFactorisationInfo.push_back(topData.getTetrajetBJet().pt() ); //new
  myFactorisationInfo.push_back(topData.getTetrajetBJet().eta() );
  fCommonPlots.setFactorisationBinForEvent(myFactorisationInfo);
  // fNormalizationSystematicsControlRegion.setFactorisationBinForEvent(myFactorisationInfo); //fixme
  // fNormalizationSystematicsControlRegion.fillControlPlotsAfterTauSelection(fEvent, tauData); //fixme

  // If 1 or more untagged genuine bjets are found the event is considered fakeB. Otherwise genuineB
  bool isGenuineB = invBjetData.isGenuineB();
  hInverted_IsGenuineB->Fill(isGenuineB);

  //================================================================================================
  // Preselections (aka Standard Selections)
  //================================================================================================
  if (0) std::cout << "=== Inverted: Preselections" << std::endl;
  fCommonPlots.fillControlPlotsAfterStandardSelections(fEvent, jetData, invBjetData, METData, QGLRData, topData, isGenuineB);

  // Fill Triplets  (Inverted)
  hInverted_QGLR_AfterStandardSelections->Fill(isGenuineB, QGLRData.getQGLR());

  //================================================================================================
  // All Selections
  //================================================================================================
  if (!topData.passedSelection()) 
    {
      // If top fails determine if event fall into  Control Region 2 (CR2)
      bool passLdgTopMVA    = cfg_LdgTopMVACut.passedCut( topData.getMVAmax1() );
      bool passSubldgTopMVA = cfg_SubldgTopMVACut.passedCut( topData.getMVAmax2() );
      bool passInvertedTop  = passLdgTopMVA * passSubldgTopMVA;
      if (!passInvertedTop) return;

      if (0) std::cout << "=== Inverted: Control Region 2 (CR2)" << std::endl;
      cInvertedSelectedCR.increment();

      // Fill plots (CR2)
      hInverted_QGLR_AfterCRSelections->Fill(isGenuineB, QGLRData.getQGLR());
      
      // Splitted Histos
      fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hQGLR_CRtwo, isGenuineB, QGLRData.getQGLR());
      
      return;
    }

  if (0) std::cout << "=== Inverted: Verification Region (VR)" << std::endl;
  cInvertedSelected.increment();

  //================================================================================================
  // Fill final plots (VR)
  //================================================================================================
  fCommonPlots.fillControlPlotsAfterAllSelections(fEvent, (int) isGenuineB);

  // Fill plots (VR)
  hInverted_QGLR_AfterAllSelections->Fill(isGenuineB, QGLRData.getQGLR());

  // Splitted histos
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hQGLR_VR, isGenuineB, QGLRData.getQGLR());

  // Save selected event ID for pick events
  fEventSaver.save();

  return;
}
