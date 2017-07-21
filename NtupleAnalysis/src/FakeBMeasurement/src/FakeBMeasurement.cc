// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "Tools/interface/DirectionalCut.h"
#include "EventSelection/interface/EventSelections.h"
#include "EventSelection/interface/BJetSelection.h"

#include "TDirectory.h"
#include "Math/VectorUtil.h"

class FakeBMeasurement: public BaseSelector {
public:
  explicit FakeBMeasurement(const ParameterSet& config, const TH1* skimCounters);
  virtual ~FakeBMeasurement();

  /// Books histograms
  virtual void book(TDirectory *dir) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;

private:
  // Input parameters
  const DirectionalCut<float> cfg_PrelimTopFitChiSqr;
  const DirectionalCut<int> cfg_NumberOfBJets;
  const DirectionalCut<int> cfg_NumberOfInvertedBJets;
  const std::string cfg_InvertedBJetsDiscriminator;
  const std::string cfg_InvertedBJetsDiscriminatorWP;
  const int cfg_MaxNumberOfBJetsInTopFit;

  // Common plots
  CommonPlots fCommonPlots;
  // CommonPlots fNormalizationSystematicsSignalRegion;  // todo
  // CommonPlots fNormalizationSystematicsControlRegion; // todo

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
  // Baseline selection      
  Count cBaselineBTaggingCounter;
  Count cBaselineBTaggingSFCounter;
  METSelection fBaselineMETSelection;
  TopologySelection fBaselineTopologySelection;
  TopSelection fBaselineTopSelection;
  Count cBaselineSelected;
  // Inverted selection
  Count cInvertedBTaggingCounter;
  Count cInvertedBTaggingSFCounter;
  METSelection fInvertedMETSelection;
  TopologySelection fInvertedTopologySelection;
  TopSelection fInvertedTopSelection;
  Count cInvertedSelected;

  void doInvertedAnalysis(const JetSelection::Data& jetData, const BJetSelection::Data& bjetData, const int nVertices);
  void doBaselineAnalysis(const JetSelection::Data& jetData, const BJetSelection::Data& bjetData, const int nVertices);
  bool IsGenuineBEvent(const std::vector<Jet>& selectedBJets);
  bool HasZeroUntaggedGenuineBJets(const JetSelection::Data& jetData, const BJetSelection::Data& bjetData); // not used


  // Purity Triplets
  WrappedTH1Triplet* hInverted_FailedBJetBDisc_AfterAllSelections;
  WrappedTH1Triplet* hInverted_FailedBJetPt_AfterAllSelections;
  WrappedTH1Triplet* hInverted_FailedBJetEta_AfterAllSelections;
  WrappedTH1Triplet* hInverted_FailedBJetPdgId_AfterAllSelections;
  WrappedTH1Triplet* hInverted_FailedBJetPartonFlavour_AfterAllSelections;
  WrappedTH1Triplet* hInverted_FailedBJetHadronFlavour_AfterAllSelections;
  WrappedTH1Triplet* hInverted_FailedBJetAncestry_AfterAllSelections;

  // FakeB Triplets (Baseline)
  WrappedTH1Triplet *hBaseline_TopMassReco_ChiSqr_AfterAllSelections;
  WrappedTH1Triplet* hBaseline_TopMassReco_LdgTetrajetPt_AfterAllSelections;
  WrappedTH1Triplet* hBaseline_TopMassReco_LdgTetrajetM_AfterAllSelections;
  WrappedTH1Triplet* hBaseline_TopMassReco_SubldgTetrajetPt_AfterAllSelections;
  WrappedTH1Triplet* hBaseline_TopMassReco_SubldgTetrajetM_AfterAllSelections;
  WrappedTH1Triplet* hBaseline_TopMassReco_TetrajetBJetPt_AfterAllSelections;
  WrappedTH1Triplet* hBaseline_TopMassReco_TetrajetBJetEta_AfterAllSelections;
  WrappedTH1Triplet* hBaseline_TopMassReco_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  WrappedTH1Triplet* hBaseline_TopMassReco_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  WrappedTH1Triplet* hBaseline_TopMassReco_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_TopMassReco_LdgTrijetPt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_TopMassReco_LdgTrijetM_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_TopMassReco_SubLdgTrijetPt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_TopMassReco_SubLdgTrijetM_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_TopMassReco_LdgDijetPt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_TopMassReco_LdgDijetM_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_TopMassReco_SubLdgDijetPt_AfterAllSelections;
  WrappedTH1Triplet *hBaseline_TopMassReco_SubLdgDijetM_AfterAllSelections;

  // FakeB Triplets (Inverted)
  WrappedTH1Triplet *hInverted_TopMassReco_ChiSqr_AfterAllSelections;
  WrappedTH1Triplet* hInverted_TopMassReco_LdgTetrajetPt_AfterAllSelections;
  WrappedTH1Triplet* hInverted_TopMassReco_LdgTetrajetM_AfterAllSelections;
  WrappedTH1Triplet* hInverted_TopMassReco_SubldgTetrajetPt_AfterAllSelections;
  WrappedTH1Triplet* hInverted_TopMassReco_SubldgTetrajetM_AfterAllSelections;
  WrappedTH1Triplet* hInverted_TopMassReco_TetrajetBJetPt_AfterAllSelections;
  WrappedTH1Triplet* hInverted_TopMassReco_TetrajetBJetEta_AfterAllSelections;
  WrappedTH1Triplet* hInverted_TopMassReco_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  WrappedTH1Triplet* hInverted_TopMassReco_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  WrappedTH1Triplet* hInverted_TopMassReco_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  WrappedTH1Triplet *hInverted_TopMassReco_LdgTrijetPt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_TopMassReco_LdgTrijetM_AfterAllSelections;
  WrappedTH1Triplet *hInverted_TopMassReco_SubLdgTrijetPt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_TopMassReco_SubLdgTrijetM_AfterAllSelections;
  WrappedTH1Triplet *hInverted_TopMassReco_LdgDijetPt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_TopMassReco_LdgDijetM_AfterAllSelections;
  WrappedTH1Triplet *hInverted_TopMassReco_SubLdgDijetPt_AfterAllSelections;
  WrappedTH1Triplet *hInverted_TopMassReco_SubLdgDijetM_AfterAllSelections;

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(FakeBMeasurement);

FakeBMeasurement::FakeBMeasurement(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    cfg_PrelimTopFitChiSqr(config, "FakeBMeasurement.prelimTopFitChiSqrCut"),
    cfg_NumberOfBJets(config, "FakeBMeasurement.numberOfBJetsCut"),
    cfg_NumberOfInvertedBJets(config, "FakeBMeasurement.numberOfInvertedBJetsCut"),
    cfg_InvertedBJetsDiscriminator(config.getParameter<std::string>("FakeBMeasurement.invertedBJetDiscr")),
    cfg_InvertedBJetsDiscriminatorWP(config.getParameter<std::string>("FakeBMeasurement.invertedBJetWorkingPoint")),
    cfg_MaxNumberOfBJetsInTopFit(config.getParameter<int>("FakeBMeasurement.maxNumberOfBJetsInTopFit")),
    fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kFakeBMeasurement, fHistoWrapper),
    cAllEvents(fEventCounter.addCounter("All events")),
    cTrigger(fEventCounter.addCounter("Passed trigger")),
    fMETFilterSelection(config.getParameter<ParameterSet>("METFilter"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cVertexSelection(fEventCounter.addCounter("Passed PV")),
    fElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fMuonSelection(config.getParameter<ParameterSet>("MuonSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fTauSelection(config.getParameter<ParameterSet>("TauSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fJetSelection(config.getParameter<ParameterSet>("JetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fBJetSelection(config.getParameter<ParameterSet>("BJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    // Baseline selection
    cBaselineBTaggingCounter(fEventCounter.addCounter("Baseline: passed b-jet selection")),
    cBaselineBTaggingSFCounter(fEventCounter.addCounter("Baseline: b tag SF")),
    fBaselineMETSelection(config.getParameter<ParameterSet>("METSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Baseline"),
    fBaselineTopologySelection(config.getParameter<ParameterSet>("TopologySelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Baseline"),
    fBaselineTopSelection(config.getParameter<ParameterSet>("TopSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Baseline"),
    cBaselineSelected(fEventCounter.addCounter("Baseline: selected events")),
    // Inverted selection
    cInvertedBTaggingCounter(fEventCounter.addCounter("Inverted: passed b-jet veto")),
    cInvertedBTaggingSFCounter(fEventCounter.addCounter("Inverted: b tag SF")),
    fInvertedMETSelection(config.getParameter<ParameterSet>("METSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Inverted"),
    fInvertedTopologySelection(config.getParameter<ParameterSet>("TopologySelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Inverted"),
    fInvertedTopSelection(config.getParameter<ParameterSet>("TopSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Inverted"),
    cInvertedSelected(fEventCounter.addCounter("Inverted: selected events"))
{ }


FakeBMeasurement::~FakeBMeasurement() {
  // fCommonPlots.getHistoSplitter().deleteHistograms(hNormalizationBaselineTauAfterStdSelections);
  // fCommonPlots.getHistoSplitter().deleteHistograms(hMtBaselineTauAfterStdSelections);

  // Purity Triplets
  delete hInverted_FailedBJetBDisc_AfterAllSelections;
  delete hInverted_FailedBJetPt_AfterAllSelections;
  delete hInverted_FailedBJetEta_AfterAllSelections;
  delete hInverted_FailedBJetPdgId_AfterAllSelections;
  delete hInverted_FailedBJetPartonFlavour_AfterAllSelections;
  delete hInverted_FailedBJetHadronFlavour_AfterAllSelections;
  delete hInverted_FailedBJetAncestry_AfterAllSelections;

  // FakeB Triplets (Baseline)
  delete hBaseline_TopMassReco_LdgTetrajetPt_AfterAllSelections;
  delete hBaseline_TopMassReco_LdgTetrajetM_AfterAllSelections;
  delete hBaseline_TopMassReco_SubldgTetrajetPt_AfterAllSelections;
  delete hBaseline_TopMassReco_SubldgTetrajetM_AfterAllSelections;
  delete hBaseline_TopMassReco_TetrajetBJetPt_AfterAllSelections;
  delete hBaseline_TopMassReco_TetrajetBJetEta_AfterAllSelections;
  delete hBaseline_TopMassReco_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  delete hBaseline_TopMassReco_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  delete hBaseline_TopMassReco_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  delete hBaseline_TopMassReco_LdgTrijetPt_AfterAllSelections;
  delete hBaseline_TopMassReco_LdgTrijetM_AfterAllSelections;
  delete hBaseline_TopMassReco_SubLdgTrijetPt_AfterAllSelections;
  delete hBaseline_TopMassReco_SubLdgTrijetM_AfterAllSelections;
  delete hBaseline_TopMassReco_LdgDijetPt_AfterAllSelections;
  delete hBaseline_TopMassReco_LdgDijetM_AfterAllSelections;
  delete hBaseline_TopMassReco_SubLdgDijetPt_AfterAllSelections;
  delete hBaseline_TopMassReco_SubLdgDijetM_AfterAllSelections;

  // FakeB Triplets (Inverted)
  delete hInverted_TopMassReco_LdgTetrajetPt_AfterAllSelections;
  delete hInverted_TopMassReco_LdgTetrajetM_AfterAllSelections;
  delete hInverted_TopMassReco_SubldgTetrajetPt_AfterAllSelections;
  delete hInverted_TopMassReco_SubldgTetrajetM_AfterAllSelections;
  delete hInverted_TopMassReco_TetrajetBJetPt_AfterAllSelections;
  delete hInverted_TopMassReco_TetrajetBJetEta_AfterAllSelections;
  delete hInverted_TopMassReco_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  delete hInverted_TopMassReco_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  delete hInverted_TopMassReco_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections;
  delete hInverted_TopMassReco_LdgTrijetPt_AfterAllSelections;
  delete hInverted_TopMassReco_LdgTrijetM_AfterAllSelections;
  delete hInverted_TopMassReco_SubLdgTrijetPt_AfterAllSelections;
  delete hInverted_TopMassReco_SubLdgTrijetM_AfterAllSelections;
  delete hInverted_TopMassReco_LdgDijetPt_AfterAllSelections;
  delete hInverted_TopMassReco_LdgDijetM_AfterAllSelections;
  delete hInverted_TopMassReco_SubLdgDijetPt_AfterAllSelections;
  delete hInverted_TopMassReco_SubLdgDijetM_AfterAllSelections;

}

void FakeBMeasurement::book(TDirectory *dir) {

  
  // Book common plots histograms
  fCommonPlots.book(dir, isData());

  // Book histograms in event selection classes
  fMETFilterSelection.bookHistograms(dir);
  fElectronSelection.bookHistograms(dir);
  fMuonSelection.bookHistograms(dir);
  fTauSelection.bookHistograms(dir);
  fJetSelection.bookHistograms(dir);
  fBJetSelection.bookHistograms(dir);
  // Baseline selection
  fBaselineMETSelection.bookHistograms(dir);
  fBaselineTopologySelection.bookHistograms(dir);
  fBaselineTopSelection.bookHistograms(dir);
  // Inverted selection
  fInvertedMETSelection.bookHistograms(dir);
  fInvertedTopologySelection.bookHistograms(dir);
  fInvertedTopSelection.bookHistograms(dir);
  
  // ====== Normalization histograms
  // HistoSplitter histoSplitter = fCommonPlots.getHistoSplitter();

  // Create directories for normalization
  std::string myInclusiveLabel  = "ForFakeBNormalization";
  std::string myFakeLabel       = myInclusiveLabel+"EWKFakeB";
  std::string myGenuineLabel    = myInclusiveLabel+"EWKGenuineB";
  TDirectory* myNormDir         = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabel);
  TDirectory* myNormEWKFakeBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
  TDirectory* myNormGenuineBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
  std::vector<TDirectory*> myNormalizationDirs = {myNormDir, myNormEWKFakeBDir, myNormGenuineBDir};
  
  // Obtain binning
  const int  nPtBins      = fCommonPlots.getPtBinSettings().bins();
  const float fPtMin      = fCommonPlots.getPtBinSettings().min();
  const float fPtMax      = fCommonPlots.getPtBinSettings().max();
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

  // Purity histograms [(Data-EWK)/Data]
  myInclusiveLabel = "FakeBPurity";
  myFakeLabel      = myInclusiveLabel+"EWKFakeB";
  myGenuineLabel   = myInclusiveLabel+"EWKGenuineB";

  // Create directories
  TDirectory* myPurityDir  = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabel);
  TDirectory* myPurityEWKFakeBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
  TDirectory* myPurityGenuineBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
  std::vector<TDirectory*> myPurityDirs = {myPurityDir, myPurityEWKFakeBDir, myPurityGenuineBDir};

  // Create histograms
  hInverted_FailedBJetBDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myPurityDirs,
				      "Inverted_FailedBJetBDisc_AfterAllSelections",
				      "Inverted_FailedBJetBDisc_AfterAllSelections;b-tag discriminator;Events / %.2f",
				      nBDiscBins, fBDiscMin, fBDiscMax);
  
  hInverted_FailedBJetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myPurityDirs,
				      "Inverted_FailedBJetPt_AfterAllSelections",
				      "Inverted_FailedBJetPt_AfterAllSelections;p_{T} (GeV/c);Events / %.0f GeV/c",
				      nPtBins, fPtMin, fPtMax);

  hInverted_FailedBJetEta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myPurityDirs,
				      "Inverted_FailedBJetEta_AfterAllSelections",
				      "Inverted_FailedBJetEta_AfterAllSelections;#eta;Events / %.2f",
				      nEtaBins, fEtaMin, fEtaMax);

  hInverted_FailedBJetPdgId_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myPurityDirs,
				      "Inverted_FailedBJetPdgId_AfterAllSelections",
				      "Inverted_FailedBJetPdgId_AfterAllSelections;pdgId;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJetPartonFlavour_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myPurityDirs,
				      "Inverted_FailedBJetPartonFlavour_AfterAllSelections",
				      "Inverted_FailedBJetPartonFlavour_AfterAllSelections;parton flavour;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJetHadronFlavour_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myPurityDirs,
				      "Inverted_FailedBJetHadronFlavour_AfterAllSelections",
				      "Inverted_FailedBJetHadronFlavour_AfterAllSelections;hadron flavour;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJetAncestry_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myPurityDirs,
				      "Inverted_FailedBJetAncestry_AfterAllSelections",
				      "Inverted_FailedBJetAncestry_AfterAllSelections;ancestry bit;EventsEvents / %.0f",
				      32, -0.5, 31.5); // min=1 (fromZ only), max=31 (from all)
  
  // Other histograms
  myInclusiveLabel = "ForFakeBMeasurement";
  myFakeLabel      = myInclusiveLabel+"EWKFakeB";
  myGenuineLabel   = myInclusiveLabel+"EWKGenuineB";
  // Create directories //fixme: are these used somewhere or somehow?
  TDirectory* myFakeBDir         = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabel);
  TDirectory* myFakeBEWKFakeBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
  TDirectory* myFakeBGenuineBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
  std::vector<TDirectory*> myFakeBDirs = {myFakeBDir, myFakeBEWKFakeBDir, myFakeBGenuineBDir};

  // Baseline selection
  hBaseline_TopMassReco_ChiSqr_AfterAllSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, "Baseline_TopMassReco_ChiSqr_AfterAllSelections", ";#chi^{2};Events / %.2f", 150, 0.0, 150.0);

  hBaseline_TopMassReco_LdgTetrajetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_TopMassReco_LdgTetrajetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);
  
  hBaseline_TopMassReco_LdgTetrajetM_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_TopMassReco_LdgTetrajetMass_AfterAllSelections", ";m_{jjbb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nInvMassBins, fInvMassMin, fInvMassMax);

  hBaseline_TopMassReco_SubldgTetrajetPt_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_TopMassReco_SubldgTetrajetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_TopMassReco_SubldgTetrajetM_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_TopMassReco_SubldgTetrajetMass_AfterAllSelections", ";m_{jjbb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nInvMassBins, fInvMassMin, fInvMassMax);

  hBaseline_TopMassReco_TetrajetBJetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_TopMassReco_TetrajetBJetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_TopMassReco_TetrajetBJetEta_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_TopMassReco_TetrajetBJetEta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  
  hBaseline_TopMassReco_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_TopMassReco_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections", ";#Delta#eta; #Delta#eta", nDEtaBins, fDEtaMin, fDEtaMax);
  
  hBaseline_TopMassReco_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_TopMassReco_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections", ";#Delta#phi (rads); #Delta#phi (rads)", nDPhiBins, fDPhiMin, fDPhiMax);
  
  hBaseline_TopMassReco_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_TopMassReco_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections", ";#Delta R; #Delta R", nDRBins, fDRMin, fDRMax);

  hBaseline_TopMassReco_LdgTrijetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_TopMassReco_LdgTrijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_TopMassReco_LdgTrijetM_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_TopMassReco_LdgTrijetM_AfterAllSelections", ";m_{jjb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hBaseline_TopMassReco_SubLdgTrijetPt_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_TopMassReco_SubLdgTrijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_TopMassReco_SubLdgTrijetM_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_TopMassReco_SubLdgTrijetM_AfterAllSelections", ";m_{jjb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hBaseline_TopMassReco_LdgDijetPt_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Baseline_TopMassReco_LdgDijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_TopMassReco_LdgDijetM_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_TopMassReco_LdgDijetM_AfterAllSelections", ";m_{jj} (GeV/c^{2});Events / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  hBaseline_TopMassReco_SubLdgDijetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_TopMassReco_SubLdgDijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_TopMassReco_SubLdgDijetM_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Baseline_TopMassReco_SubLdgDijetM_AfterAllSelections", ";m_{jj} (GeV/c^{2});Events / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  // Inverted selection
  hInverted_TopMassReco_ChiSqr_AfterAllSelections =  
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_TopMassReco_ChiSqr_AfterAllSelections", ";#chi^{2};Events / %2.f", 150, 0.0, 150);

  hInverted_TopMassReco_LdgTetrajetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_TopMassReco_LdgTetrajetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);
  
  hInverted_TopMassReco_LdgTetrajetM_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_TopMassReco_LdgTetrajetMass_AfterAllSelections", ";m_{jjjb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nInvMassBins, fInvMassMin, fInvMassMax);

  hInverted_TopMassReco_SubldgTetrajetPt_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_TopMassReco_SubldgTetrajetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_TopMassReco_SubldgTetrajetM_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_TopMassReco_SubldgTetrajetMass_AfterAllSelections", ";m_{jjjb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nInvMassBins, fInvMassMin, fInvMassMax);

  hInverted_TopMassReco_TetrajetBJetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_TopMassReco_TetrajetBJetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_TopMassReco_TetrajetBJetEta_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_TopMassReco_TetrajetBJetEta_AfterAllSelections", ";#eta;Events / %.2f", nEtaBins, fEtaMin, fEtaMax);
  
  hInverted_TopMassReco_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_TopMassReco_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections", ";#Delta#eta; #Delta#eta", nDEtaBins, fDEtaMin, fDEtaMax);
  
  hInverted_TopMassReco_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_TopMassReco_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections", ";#Delta#phi (rads); #Delta#phi (rads)", nDPhiBins, fDPhiMin, fDPhiMax);
  
  hInverted_TopMassReco_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_TopMassReco_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections", ";#Delta R; #Delta R", nDRBins, fDRMin, fDRMax);

  hInverted_TopMassReco_LdgTrijetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_TopMassReco_LdgTrijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_TopMassReco_LdgTrijetM_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_TopMassReco_LdgTrijetM_AfterAllSelections", ";m_{jjb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hInverted_TopMassReco_SubLdgTrijetPt_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_TopMassReco_SubLdgTrijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_TopMassReco_SubLdgTrijetM_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_TopMassReco_SubLdgTrijetM_AfterAllSelections", ";m_{jjb} (GeV/c^{2});Events / %0.f GeV/c^{2}", nTopMassBins, fTopMassMin, fTopMassMax);

  hInverted_TopMassReco_LdgDijetPt_AfterAllSelections =
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_TopMassReco_LdgDijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_TopMassReco_LdgDijetM_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs,
				      "Inverted_TopMassReco_LdgDijetM_AfterAllSelections", ";m_{jj} (GeV/c^{2});Events / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  hInverted_TopMassReco_SubLdgDijetPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_TopMassReco_SubLdgDijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_TopMassReco_SubLdgDijetM_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myFakeBDirs, 
				      "Inverted_TopMassReco_SubLdgDijetM_AfterAllSelections", ";m_{jj} (GeV/c^{2});Events / %0.f GeV/c^{2}", nWMassBins, fWMassMin, fWMassMax);

  return;
}


void FakeBMeasurement::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
  return;
}


void FakeBMeasurement::process(Long64_t entry) {

  //====== Initialize
  fCommonPlots.initialize();
  fCommonPlots.setFactorisationBinForEvent(std::vector<float> {});

  cAllEvents.increment();

  if (0) std::cout << "\nentry = " << entry << std::endl;

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
  const JetSelection::Data jetData = fJetSelection.analyzeWithoutTau(fEvent);
  if (!jetData.passedSelection()) return;
  // fCommonPlots.fillControlPlotsAfterTopologicalSelections(fEvent, true);
  
  //================================================================================================  
  // 8) BJet Selection
  //================================================================================================
  if (0) std::cout << "=== BJet selection" << std::endl;
  // Disable histogram filling and counter with silent analyze
  const BJetSelection::Data bjetData = fBJetSelection.silentAnalyze(fEvent, jetData);

  // Baseline (Bjets criteria pass)
  if (bjetData.passedSelection())
    {
      doBaselineAnalysis(jetData, bjetData, nVertices);
    }
  else // Inverted (Bjets criteria fail)
    {
      // Apply requirent on selected b-jets 
      bool passSelected = cfg_NumberOfBJets.passedCut(bjetData.getNumberOfSelectedBJets());
      if (!passSelected) return;
      
      // Apply requirement on inverted b-jets
      int nInvertedBJets = 0;
      float invertedBJetDiscr = fBJetSelection.getDiscriminatorWP(cfg_InvertedBJetsDiscriminator, cfg_InvertedBJetsDiscriminatorWP);
      
      // For-loop over selected jets
      for(const Jet& jet: jetData.getSelectedJets()) 
	{
	  
	  //=== Apply discriminator WP cut
	  if (jet.bjetDiscriminator() < invertedBJetDiscr) continue;
	  nInvertedBJets++;
	}
      
      // Apply inversion requirements 
      bool passInverted = cfg_NumberOfInvertedBJets.passedCut(nInvertedBJets);
      if (!passInverted) return;

      // Do the inverted analysis
      doInvertedAnalysis(jetData, bjetData, nVertices); 
    }
  return;
}


void FakeBMeasurement::doBaselineAnalysis(const JetSelection::Data& jetData,
                                          const BJetSelection::Data& bjetData,
                                          const int nVertices){
  if (!bjetData.passedSelection()) return;
  if (0) std::cout << "=== Baseline: bjetData.passedSelection() = " << bjetData.passedSelection() << std::endl;

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
  // std::cout << "\tSF = " << bjetData.getBTaggingScaleFactorEventWeight() << " (fEvent.isMC() = " << fEvent.isMC() << ")" << std::endl;
  cBaselineBTaggingSFCounter.increment();

  //================================================================================================
  // 10) MET selection
  //================================================================================================
  if (0) std::cout << "=== Baseline: MET selection" << std::endl;
  const METSelection::Data METData = fBaselineMETSelection.analyze(fEvent, nVertices);
  if (!METData.passedSelection()) return;

  //================================================================================================
  // 11) Topology
  //================================================================================================
  if (0) std::cout << "=== Baseline: Topology selection" << std::endl;
  const TopologySelection::Data topologyData = fBaselineTopologySelection.analyze(fEvent, jetData);
  // if (!topologyData.passedSelection()) return;

  //================================================================================================
  // 12) Top selection
  //================================================================================================
  if (0) std::cout << "=== Baseline: Top selection" << std::endl;
  const TopSelection::Data topData = fBaselineTopSelection.analyze(fEvent, jetData, bjetData);
  // if (!topData.passedSelection()) return;
  // Apply preliminary chiSq cut
  bool passPrelimChiSq = cfg_PrelimTopFitChiSqr.passedCut(topData.ChiSqr());
  if (!passPrelimChiSq) return;
  
  //================================================================================================
  // Standard Selections
  //================================================================================================
  if (0) std::cout << "=== Baseline: Standard Selections" << std::endl;
  // NB: CtrlPlotsAfterStandardSelections should only be called for Inverted!
  // fCommonPlots.fillControlPlotsAfterStandardSelections(fEvent, jetData, bjetData, METData, topologyData, topData, false);

  //================================================================================================
  // All Selections
  //================================================================================================
  if (!topologyData.passedSelection()) return;
  if (!topData.passedSelection()) return;

  if (0) std::cout << "=== Baseline: All Selections" << std::endl;
  cBaselineSelected.increment();

  //================================================================================================
  // Fill final plots
  //================================================================================================
  // NB: CtrlPlotsAfterAllSelections should only be called for Inverted!
  // fCommonPlots.fillControlPlotsAfterAllSelections(fEvent); NB: ONLY for Inverted!

  // If 1 or more untagged genuine bjets are found the event is considered fakeB. Otherwise genuineB
  // bool isGenuineB = IsGenuineBEvent(bjetData.getSelectedBJets()); // FIXME: OBSOLETE!
  bool isGenuineB = bjetData.isGenuineB();
  
  // GenuineB or FakeB Triplets (Baseline)
  hBaseline_TopMassReco_ChiSqr_AfterAllSelections ->Fill(isGenuineB, topData.ChiSqr());
  hBaseline_TopMassReco_LdgTetrajetPt_AfterAllSelections->Fill(isGenuineB, topData.getLdgTetrajet().pt() );
  hBaseline_TopMassReco_LdgTetrajetM_AfterAllSelections->Fill(isGenuineB, topData.getLdgTetrajet().M() );
  hBaseline_TopMassReco_SubldgTetrajetPt_AfterAllSelections->Fill(isGenuineB, topData.getSubldgTetrajet().pt() );
  hBaseline_TopMassReco_SubldgTetrajetM_AfterAllSelections->Fill(isGenuineB, topData.getSubldgTetrajet().M() );
  hBaseline_TopMassReco_TetrajetBJetPt_AfterAllSelections->Fill(isGenuineB, topData.getTetrajetBJet().pt() );
  hBaseline_TopMassReco_TetrajetBJetEta_AfterAllSelections->Fill(isGenuineB, topData.getTetrajetBJet().eta() );
  double dEta = std::abs( topData.getTetrajetBJet().p4().eta() - topData.getLdgTrijetBJet().p4().eta() );
  double dPhi = std::abs( ROOT::Math::VectorUtil::DeltaPhi( topData.getTetrajetBJet().p4(), topData.getLdgTrijetBJet().p4() ) );
  double dR = ROOT::Math::VectorUtil::DeltaR( topData.getTetrajetBJet().p4(), topData.getLdgTrijetBJet().p4()) ;
  hBaseline_TopMassReco_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections->Fill(isGenuineB, dEta);
  hBaseline_TopMassReco_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections->Fill(isGenuineB, dPhi);
  hBaseline_TopMassReco_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections->Fill(isGenuineB, dR);
  hBaseline_TopMassReco_LdgTrijetPt_AfterAllSelections->Fill(isGenuineB, topData.getLdgTrijet().pt() );
  hBaseline_TopMassReco_LdgTrijetM_AfterAllSelections ->Fill(isGenuineB, topData.getLdgTrijet().M() );
  hBaseline_TopMassReco_SubLdgTrijetPt_AfterAllSelections->Fill(isGenuineB, topData.getSubldgTrijet().pt() );
  hBaseline_TopMassReco_SubLdgTrijetM_AfterAllSelections ->Fill(isGenuineB, topData.getSubldgTrijet().M() );
  hBaseline_TopMassReco_LdgDijetPt_AfterAllSelections->Fill(isGenuineB, topData.getLdgDijet().pt() );
  hBaseline_TopMassReco_LdgDijetM_AfterAllSelections ->Fill(isGenuineB, topData.getLdgDijet().M() );
  hBaseline_TopMassReco_SubLdgDijetPt_AfterAllSelections->Fill(isGenuineB, topData.getSubldgDijet().pt() );
  hBaseline_TopMassReco_SubLdgDijetM_AfterAllSelections ->Fill(isGenuineB, topData.getSubldgDijet().M() );

  // Save selected event ID for pick events
  fEventSaver.save();

  return;
}


void FakeBMeasurement::doInvertedAnalysis(const JetSelection::Data& jetData,
                                          const BJetSelection::Data& bjetData,
                                          const int nVertices){
  if (bjetData.passedSelection()) return;
  if (0) std::cout << "=== Inverted: bjetData.passedSelection() = " << bjetData.passedSelection() << std::endl;
  
  // Increment counter
  cInvertedBTaggingCounter.increment();

  //================================================================================================  
  // 9) BJet SF  
  //================================================================================================
  if (0) std::cout << "=== Inverted: BJet SF" << std::endl;
  if (fEvent.isMC()) 
    {
      fEventWeight.multiplyWeight(bjetData.getBTaggingScaleFactorEventWeight());
    }
  // std::cout << "\tSF = " << bjetData.getBTaggingScaleFactorEventWeight() << " (fEvent.isMC() = " << fEvent.isMC() << ")" << std::endl;
  cInvertedBTaggingSFCounter.increment();

  //================================================================================================
  // 10) MET selection
  //================================================================================================
  if (0) std::cout << "=== Inverted: MET selection" << std::endl;
  const METSelection::Data METData = fInvertedMETSelection.analyze(fEvent, nVertices);
  if (!METData.passedSelection()) return;

  //================================================================================================
  // 11) Topology
  //================================================================================================
  if (0) std::cout << "=== Inverted: Topology selection" << std::endl;
  const TopologySelection::Data topologyData = fInvertedTopologySelection.analyze(fEvent, jetData);
  // if (!topologyData.passedSelection()) return;

  //================================================================================================
  // 12) Top selection
  //================================================================================================
  if (0) std::cout << "=== Inverted: Top selection" << std::endl;
  const TopSelection::Data topData = fInvertedTopSelection.analyzeWithoutBJets(fEvent, jetData, bjetData, cfg_MaxNumberOfBJetsInTopFit);
  // if (!topData.passedSelection()) return;
  // Apply preliminary chiSq cut
  bool passPrelimChiSq = cfg_PrelimTopFitChiSqr.passedCut(topData.ChiSqr());
  if (!passPrelimChiSq) return;

  //================================================================================================
  // Standard Selections
  //================================================================================================
  if (0) std::cout << "=== Inverted: Standard Selections" << std::endl;
  fCommonPlots.fillControlPlotsAfterStandardSelections(fEvent, jetData, bjetData, METData, topologyData, topData, true);

  //================================================================================================
  // All Selections
  //================================================================================================
  if (!topologyData.passedSelection()) return;
  if (!topData.passedSelection()) return;

  if (0) std::cout << "=== Inverted: All Selections" << std::endl;
  cInvertedSelected.increment();

  //================================================================================================
  // Fill final plots
  //================================================================================================
  fCommonPlots.fillControlPlotsAfterAllSelections(fEvent, 1);
  // fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hBaselineTransverseMass, isGenuineTau, myTransverseMass);

  // If 1 or more untagged genuine bjets are found the event is considered fakeB. Otherwise genuineB
  bool isGenuineB = IsGenuineBEvent(topData.getJetsUsedAsBJetsInFit());
  // bool isGenuineB = bjetData.isGenuineB(); // not correct for inverted

  // Get the failed bjet candidates randomly shuffled. Put any trg-matched objects in the front  
  Jet bjet= topData.getJetsUsedAsBJetsInFit()[2]; // FIXME: Do i need this?
  // Jet bjet= bjetData.getFailedBJetCands()[0]; // should be equivalent to previous line

  // Construct ancestry bit (Z, W, top, H+, Other)
  int ancestryBit = ( pow(2, 0)*bjet.originatesFromZ() +
		      pow(2, 1)*bjet.originatesFromW() +
		      pow(2, 2)*bjet.originatesFromTop() +
		      pow(2, 3)*bjet.originatesFromChargedHiggs() +
		      pow(2, 4)*bjet.originatesFromUnknown() );
  
  // Purity Triplets (Inverted)
  hInverted_FailedBJetBDisc_AfterAllSelections->Fill(isGenuineB, bjet.bjetDiscriminator());
  hInverted_FailedBJetPt_AfterAllSelections->Fill(isGenuineB, bjet.pt());
  hInverted_FailedBJetEta_AfterAllSelections->Fill(isGenuineB, bjet.eta());
  hInverted_FailedBJetPdgId_AfterAllSelections->Fill(isGenuineB, bjet.pdgId());
  hInverted_FailedBJetPartonFlavour_AfterAllSelections->Fill(isGenuineB, bjet.partonFlavour());
  hInverted_FailedBJetHadronFlavour_AfterAllSelections->Fill(isGenuineB, bjet.hadronFlavour());
  hInverted_FailedBJetAncestry_AfterAllSelections->Fill(isGenuineB, ancestryBit);

  // GenuineB or FakeB Triplets (Inverted)
  hInverted_TopMassReco_ChiSqr_AfterAllSelections ->Fill(isGenuineB, topData.ChiSqr());
  hInverted_TopMassReco_LdgTetrajetPt_AfterAllSelections->Fill(isGenuineB, topData.getLdgTetrajet().pt() );
  hInverted_TopMassReco_LdgTetrajetM_AfterAllSelections->Fill(isGenuineB, topData.getLdgTetrajet().M() );
  hInverted_TopMassReco_SubldgTetrajetPt_AfterAllSelections->Fill(isGenuineB, topData.getSubldgTetrajet().pt() );
  hInverted_TopMassReco_SubldgTetrajetM_AfterAllSelections->Fill(isGenuineB, topData.getSubldgTetrajet().M() );
  hInverted_TopMassReco_TetrajetBJetPt_AfterAllSelections->Fill(isGenuineB, topData.getTetrajetBJet().pt() );
  hInverted_TopMassReco_TetrajetBJetEta_AfterAllSelections->Fill(isGenuineB, topData.getTetrajetBJet().eta() );
  double dEta = std::abs( topData.getTetrajetBJet().eta() - topData.getLdgTrijetBJet().eta());
  double dPhi = std::abs( ROOT::Math::VectorUtil::DeltaPhi( topData.getTetrajetBJet().p4(), topData.getLdgTrijetBJet().p4()) );
  double dR = ROOT::Math::VectorUtil::DeltaR( topData.getTetrajetBJet().p4(), topData.getLdgTrijetBJet().p4()) ;
  hInverted_TopMassReco_DeltaEtaLdgTrijetBJetTetrajetBJet_AfterAllSelections->Fill(isGenuineB, dEta);
  hInverted_TopMassReco_DeltaPhiLdgTrijetBJetTetrajetBJet_AfterAllSelections->Fill(isGenuineB, dPhi);
  hInverted_TopMassReco_DeltaRLdgTrijetBJetTetrajetBJet_AfterAllSelections->Fill(isGenuineB, dR);
  hInverted_TopMassReco_LdgTrijetPt_AfterAllSelections->Fill(isGenuineB, topData.getLdgTrijet().pt() );
  hInverted_TopMassReco_LdgTrijetM_AfterAllSelections ->Fill(isGenuineB, topData.getLdgTrijet().M() );
  hInverted_TopMassReco_SubLdgTrijetPt_AfterAllSelections->Fill(isGenuineB, topData.getSubldgTrijet().pt() );
  hInverted_TopMassReco_SubLdgTrijetM_AfterAllSelections ->Fill(isGenuineB, topData.getSubldgTrijet().M() );
  hInverted_TopMassReco_LdgDijetPt_AfterAllSelections->Fill(isGenuineB, topData.getLdgDijet().pt() );
  hInverted_TopMassReco_LdgDijetM_AfterAllSelections ->Fill(isGenuineB, topData.getLdgDijet().M() );
  hInverted_TopMassReco_SubLdgDijetPt_AfterAllSelections->Fill(isGenuineB, topData.getSubldgDijet().pt() );
  hInverted_TopMassReco_SubLdgDijetM_AfterAllSelections ->Fill(isGenuineB, topData.getSubldgDijet().M() );

  // Save selected event ID for pick events
  fEventSaver.save();

  return;
}

bool FakeBMeasurement::IsGenuineBEvent(const std::vector<Jet>& selectedBJets)
{ 
  if (!fEvent.isMC()) return false;
  
  unsigned int nFakes=0;

  // For-loop: Selected BJets
  for(const Jet& bjet: selectedBJets)
    {

      // https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideBTagMCTools#Jet_flavour_in_PAT
      bool isFakeB = (abs(bjet.pdgId()) != 5); // For data pdgId==0
      if (isFakeB) nFakes++;

    }
  // std::cout << "BJets = " << selectedBJets().size() << ", Fakes = " << nFakes << std::endl;
  
  return (nFakes==0);
}


bool FakeBMeasurement::HasZeroUntaggedGenuineBJets(const JetSelection::Data& jetData,
						   const BJetSelection::Data& bjetData) 
{ 
  if (!fEvent.isMC()) return false;
  
  float dR_match = 0.1;
  unsigned int jet_index = 0;
  unsigned int taggedGenuineBs = 0;
  unsigned int untaggedGenuineBs = 0;

  // For-loop: Selected jets
  for(const Jet& jet: jetData.getSelectedJets()) 
    {
      jet_index++;

      // https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideBTagMCTools#Jet_flavour_in_PAT
      bool isGenuine = (abs(jet.pdgId()) == 5); // For data pdgId==0
      bool isTagged  = false;
      
      // For-loop: Selected bjets
      for(const Jet& bjet: bjetData.getSelectedBJets())
	{
	  float dR = ROOT::Math::VectorUtil::DeltaR(jet.p4(), bjet.p4());
	  if (dR <= dR_match) 
	    {
	      isTagged = true;
	      break;
	    }
	}
      // std::cout << "jet#" << jet_index << " isGenuine = " << isGenuine << ", isTagged = " << isTagged << std::endl;
      if (!isGenuine) continue;
      if (isTagged) taggedGenuineBs++;
      else untaggedGenuineBs++;
    }

  return (untaggedGenuineBs==0);
}
