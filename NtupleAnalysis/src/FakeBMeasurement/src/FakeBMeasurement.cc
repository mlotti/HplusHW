// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

#include "TDirectory.h"

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
  const HistogramSettings cfg_PtBinSetting;
  const HistogramSettings cfg_EtaBinSetting;

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
  LightJetSelection fLightJetSelection;
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

  // Purity histograms [(Data-EWK)/Data]
  WrappedTH1Triplet* hInverted_FailedBJetWithBestBDiscBDisc_AfterAllSelections;
  WrappedTH1Triplet* hInverted_FailedBJetWithBestBDiscPt_AfterAllSelections;
  WrappedTH1Triplet* hInverted_FailedBJetWithBestBDiscEta_AfterAllSelections;
  WrappedTH1Triplet* hInverted_FailedBJetWithBestBDiscPdgId_AfterAllSelections;
  WrappedTH1Triplet* hInverted_FailedBJetWithBestBDiscPartonFlavour_AfterAllSelections;
  WrappedTH1Triplet* hInverted_FailedBJetWithBestBDiscHadronFlavour_AfterAllSelections;
  WrappedTH1Triplet* hInverted_FailedBJetWithBestBDiscAncestry_AfterAllSelections;

  // Baseline selection
  WrappedTH1 *hBaseline_TopMassReco_ChiSqr_AfterAllSelections;
  WrappedTH1 *hBaseline_TopMassReco_LdgTrijetPt_AfterAllSelections;
  WrappedTH1 *hBaseline_TopMassReco_LdgTrijetM_AfterAllSelections;
  WrappedTH1 *hBaseline_TopMassReco_SubLdgTrijetPt_AfterAllSelections;
  WrappedTH1 *hBaseline_TopMassReco_SubLdgTrijetM_AfterAllSelections;
  WrappedTH1 *hBaseline_TopMassReco_LdgDijetPt_AfterAllSelections;
  WrappedTH1 *hBaseline_TopMassReco_LdgDijetM_AfterAllSelections;
  WrappedTH1 *hBaseline_TopMassReco_SubLdgDijetPt_AfterAllSelections;
  WrappedTH1 *hBaseline_TopMassReco_SubLdgDijetM_AfterAllSelections;

  // Inverted selection
  WrappedTH1 *hInverted_TopMassReco_ChiSqr_AfterAllSelections;
  WrappedTH1 *hInverted_TopMassReco_LdgTrijetPt_AfterAllSelections;
  WrappedTH1 *hInverted_TopMassReco_LdgTrijetM_AfterAllSelections;
  WrappedTH1 *hInverted_TopMassReco_SubLdgTrijetPt_AfterAllSelections;
  WrappedTH1 *hInverted_TopMassReco_SubLdgTrijetM_AfterAllSelections;
  WrappedTH1 *hInverted_TopMassReco_LdgDijetPt_AfterAllSelections;
  WrappedTH1 *hInverted_TopMassReco_LdgDijetM_AfterAllSelections;
  WrappedTH1 *hInverted_TopMassReco_SubLdgDijetPt_AfterAllSelections;
  WrappedTH1 *hInverted_TopMassReco_SubLdgDijetM_AfterAllSelections;

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(FakeBMeasurement);

FakeBMeasurement::FakeBMeasurement(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    cfg_PtBinSetting(config.getParameter<ParameterSet>("CommonPlots.ptBins")),
    cfg_EtaBinSetting(config.getParameter<ParameterSet>("CommonPlots.etaBins")),
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
    fLightJetSelection(config.getParameter<ParameterSet>("LightJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
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

  // Purity histograms [(Data-EWK)/Data]
  delete hInverted_FailedBJetWithBestBDiscBDisc_AfterAllSelections;
  delete hInverted_FailedBJetWithBestBDiscPt_AfterAllSelections;
  delete hInverted_FailedBJetWithBestBDiscEta_AfterAllSelections;
  delete hInverted_FailedBJetWithBestBDiscPdgId_AfterAllSelections;
  delete hInverted_FailedBJetWithBestBDiscPartonFlavour_AfterAllSelections;
  delete hInverted_FailedBJetWithBestBDiscHadronFlavour_AfterAllSelections;
  delete hInverted_FailedBJetWithBestBDiscAncestry_AfterAllSelections;

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
  fLightJetSelection.bookHistograms(dir);
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
  
  // Normalization bin settings
  // const float fMetMin = fCommonPlots.getMetBinSettings().min();
  // const float fMetMax = fCommonPlots.getMetBinSettings().max();
  // const int nMetBins  = fMetMax-fMetMin; // Use 1 GeV bin width
  // const int nMtBins   = fCommonPlots.getMtBinSettings().bins();
  // const float fMtMin  = fCommonPlots.getMtBinSettings().min();
  // const float fMtMax  = fCommonPlots.getMtBinSettings().max();

  // if ((fMetMax-fMetMin) / nMetBins > 10.0) {
  //   throw hplus::Exception("config") << "MET histogram bin width is larger than 10 GeV! This is not good for QCD measurement (edit python/parameters/signalAnalysisParameters.py)";
  // }

  // Obtain binning
  const int  nPtBins = fCommonPlots.getPtBinSettings().bins();
  const float fPtMin = fCommonPlots.getPtBinSettings().min();
  const float fPtMax = fCommonPlots.getPtBinSettings().max();

  const int  nEtaBins = fCommonPlots.getEtaBinSettings().bins();
  const float fEtaMin = fCommonPlots.getEtaBinSettings().min();
  const float fEtaMax = fCommonPlots.getEtaBinSettings().max();

  const int  nBDiscBins = fCommonPlots.getBJetDiscBinSettings().bins();
  const float fBDiscMin = fCommonPlots.getBJetDiscBinSettings().min();
  const float fBDiscMax = fCommonPlots.getBJetDiscBinSettings().max();

  const int nMassBins  = 80;
  const float fMassMin =   0.0;
  const float fMassMax = 800.0;

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
  hInverted_FailedBJetWithBestBDiscBDisc_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myPurityDirs,
				      "Inverted_FailedBJetWithBestBDiscBDisc_AfterAllSelections",
				      "Inverted_FailedBJetWithBestBDiscBDisc_AfterAllSelections;b-tag discriminator;Events / %.2f",
				      nBDiscBins, fBDiscMin, fBDiscMax);
  
  hInverted_FailedBJetWithBestBDiscPt_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myPurityDirs,
				      "Inverted_FailedBJetWithBestBDiscPt_AfterAllSelections",
				      "Inverted_FailedBJetWithBestBDiscPt_AfterAllSelections;p_{T} (GeV/c);Events / %.0f GeV/c",
				      nPtBins, fPtMin, fPtMax);

  hInverted_FailedBJetWithBestBDiscEta_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myPurityDirs,
				      "Inverted_FailedBJetWithBestBDiscEta_AfterAllSelections",
				      "Inverted_FailedBJetWithBestBDiscEta_AfterAllSelections;#eta;Events / %.2f",
				      nEtaBins, fEtaMin, fEtaMax);

  hInverted_FailedBJetWithBestBDiscPdgId_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myPurityDirs,
				      "Inverted_FailedBJetWithBestBDiscPdgId_AfterAllSelections",
				      "Inverted_FailedBJetWithBestBDiscPdgId_AfterAllSelections;pdgId;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJetWithBestBDiscPartonFlavour_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myPurityDirs,
				      "Inverted_FailedBJetWithBestBDiscPartonFlavour_AfterAllSelections",
				      "Inverted_FailedBJetWithBestBDiscPartonFlavour_AfterAllSelections;parton flavour;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJetWithBestBDiscHadronFlavour_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kDebug, myPurityDirs,
				      "Inverted_FailedBJetWithBestBDiscHadronFlavour_AfterAllSelections",
				      "Inverted_FailedBJetWithBestBDiscHadronFlavour_AfterAllSelections;hadron flavour;Events / %.0f",
				      23, -0.5, 22.5);

  hInverted_FailedBJetWithBestBDiscAncestry_AfterAllSelections = 
    fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kVital, myPurityDirs,
				      "Inverted_FailedBJetWithBestBDiscAncestry_AfterAllSelections",
				      "Inverted_FailedBJetWithBestBDiscAncestry_AfterAllSelections;ancestry bit;EventsEvents / %.0f",
				      32, -0.5, 31.5); // min=1 (fromZ only), max=31 (from all)
  
  // Other histograms
  myInclusiveLabel = "ForFakeBMeasurement";
  myFakeLabel      = myInclusiveLabel+"EWKFakeB";
  myGenuineLabel   = myInclusiveLabel+"EWKGenuineB";
  // Create directories //fixme: are these used somewhere or somehow?
  TDirectory* myQCDDir         = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabel);
  TDirectory* myQCDEWKFakeBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
  TDirectory* myQCDGenuineBDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
  std::vector<TDirectory*> myQCDPlotDirs = {myQCDDir, myQCDEWKFakeBDir, myQCDGenuineBDir};

  // Baseline selection
  hBaseline_TopMassReco_ChiSqr_AfterAllSelections =  
    fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Baseline_TopMassReco_ChiSqr_AfterAllSelections", ";#chi^{2};Events / %.2f", 150, 0.0, 150.0);

  hBaseline_TopMassReco_LdgTrijetPt_AfterAllSelections = 
    fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Baseline_TopMassReco_LdgTrijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_TopMassReco_LdgTrijetM_AfterAllSelections =
    fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Baseline_TopMassReco_LdgTrijetM_AfterAllSelections", ";M (GeV/c^{2});Events / %0.f GeV/c^{2}", nMassBins, fMassMin, fMassMax);

  hBaseline_TopMassReco_SubLdgTrijetPt_AfterAllSelections =
    fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Baseline_TopMassReco_SubLdgTrijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_TopMassReco_SubLdgTrijetM_AfterAllSelections = 
    fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Baseline_TopMassReco_SubLdgTrijetM_AfterAllSelections", ";M (GeV/c^{2});Events / %0.f GeV/c^{2}", nMassBins, fMassMin, fMassMax);

  hBaseline_TopMassReco_LdgDijetPt_AfterAllSelections =
    fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Baseline_TopMassReco_LdgDijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_TopMassReco_LdgDijetM_AfterAllSelections = 
    fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Baseline_TopMassReco_LdgDijetM_AfterAllSelections", ";M (GeV/c^{2});Events / %0.f GeV/c^{2}", nMassBins, fMassMin, fMassMax);

  hBaseline_TopMassReco_SubLdgDijetPt_AfterAllSelections = 
    fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Baseline_TopMassReco_SubLdgDijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hBaseline_TopMassReco_SubLdgDijetM_AfterAllSelections = 
    fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Baseline_TopMassReco_SubLdgDijetM_AfterAllSelections", ";M (GeV/c^{2});Events / %0.f GeV/c^{2}", nMassBins, fMassMin, fMassMax);

  // Inverted selection
  hInverted_TopMassReco_ChiSqr_AfterAllSelections =  
    fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Inverted_TopMassReco_ChiSqr_AfterAllSelections", ";#chi^{2};Events / %2.f", 150, 0.0, 150.0);

  hInverted_TopMassReco_LdgTrijetPt_AfterAllSelections = 
    fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Inverted_TopMassReco_LdgTrijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_TopMassReco_LdgTrijetM_AfterAllSelections =
    fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Inverted_TopMassReco_LdgTrijetM_AfterAllSelections", ";M (GeV/c^{2});Events / %0.f GeV/c^{2}", nMassBins, fMassMin, fMassMax);

  hInverted_TopMassReco_SubLdgTrijetPt_AfterAllSelections =
    fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Inverted_TopMassReco_SubLdgTrijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_TopMassReco_SubLdgTrijetM_AfterAllSelections = 
    fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Inverted_TopMassReco_SubLdgTrijetM_AfterAllSelections", ";M (GeV/c^{2});Events / %0.f GeV/c^{2}", nMassBins, fMassMin, fMassMax);

  hInverted_TopMassReco_LdgDijetPt_AfterAllSelections =
    fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Inverted_TopMassReco_LdgDijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_TopMassReco_LdgDijetM_AfterAllSelections = 
    fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Inverted_TopMassReco_LdgDijetM_AfterAllSelections", ";M (GeV/c^{2});Events / %0.f GeV/c^{2}", nMassBins, fMassMin, fMassMax);

  hInverted_TopMassReco_SubLdgDijetPt_AfterAllSelections = 
    fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Inverted_TopMassReco_SubLdgDijetPt_AfterAllSelections", ";p_{T} (GeV/c);Events / %0.f GeV/c", nPtBins*2, fPtMin, fPtMax*2);

  hInverted_TopMassReco_SubLdgDijetM_AfterAllSelections = 
    fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Inverted_TopMassReco_SubLdgDijetM_AfterAllSelections", ";M (GeV/c^{2});Events / %0.f GeV/c^{2}", nMassBins, fMassMin, fMassMax);

	     
  // Create shape histograms for baseline tau (inverted tau histograms are in common plots)
  /*
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kInformative, myQCDPlotDirs,
    hBaselineTauTransverseMass,
    "BaselineTauShapeTransverseMass", ";m_{T} (GeV);N_{events}",
    nMtBins, fMtMin, fMtMax);
   
  hTransverseMass_inverted_Bveto =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_inverted_Bveto", "TransverseMass_inverted_Bveto", 200, 0, 800);
  hTransverseMass_baseline_Bveto =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_baseline_Bveto", "TransverseMass_baseline_Bveto", 200, 0, 800);
  hTransverseMass_inverted_Bveto_BBveto =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_inverted_Bveto_BBveto", "TransverseMass_inverted_Bveto_BBveto", 200, 0, 800);
  hTransverseMass_baseline_Bveto_BBveto =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_baseline_Bveto_BBveto", "TransverseMass_baseline_Bveto_BBveto", 200, 0, 800);
  hTransverseMass_inverted_all =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_inverted_all", "TransverseMass_inverted_all", 200, 0, 800);
  hTransverseMass_baseline_all =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_baseline_all", "TransverseMass_baseline_all", 200, 0, 800);
  hTransverseMass_inverted_all_genuineTau =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_inverted_all_genuineTau", "TransverseMass_inverted_all_genuineTau", 200, 0, 800);
  hTransverseMass_baseline_all_genuineTau =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_baseline_all_genuineTau", "TransverseMass_baseline_all_genuineTau", 200, 0, 800);
  hTransverseMass_inverted_Bveto_noMet =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_inverted_Bveto_noMet", "TransverseMass_inverted_Bveto_noMet", 200, 0, 800);
  hTransverseMass_baseline_Bveto_noMet =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_baseline_Bveto_noMet", "TransverseMass_baseline_Bveto_noMet", 200, 0, 800);
  hTransverseMass_inverted_Bveto_BBveto_noMet =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_inverted_Bveto_BBveto_noMet", "TransverseMass_inverted_Bveto_BBveto_noMet", 200, 0, 800);
  hTransverseMass_baseline_Bveto_BBveto_noMet =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_baseline_Bveto_BBveto_noMet", "TransverseMass_baseline_Bveto_BBveto_noMet", 200, 0, 800);
  hTransverseMass_inverted_Bveto_genuineTau =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_inverted_Bveto_genuineTau", "TransverseMass_inverted_Bveto_genuineTau", 200, 0, 800);
  hTransverseMass_baseline_Bveto_genuineTau =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_baseline_Bveto_genuineTau", "TransverseMass_baseline_Bveto_genuineTau", 200, 0, 800);
  hTransverseMass_inverted_Bveto_genuineTau_noMet =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_inverted_Bveto_genuineTau_noMet", "TransverseMass_inverted_Bveto_genuineTau_noMet", 200, 0, 800);
  hTransverseMass_baseline_Bveto_genuineTau_noMet =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_baseline_Bveto_genuineTau_noMet", "TransverseMass_baseline_Bveto_genuineTau_noMet", 200, 0, 800);

  hTransverseMass_inverted_BBveto =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_inverted_BBveto", "TransverseMass_inverted_BBveto", 200, 0, 800);
  hTransverseMass_baseline_BBveto =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_baseline_BBveto", "TransverseMass_baseline_BBveto", 200, 0, 800);
  hTransverseMass_inverted_BBveto_noMet =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_inverted_BBveto_noMet", "TransverseMass_inverted_BBveto_noMet", 200, 0, 800);
  hTransverseMass_baseline_BBveto_noMet =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_baseline_BBveto_noMet", "TransverseMass_baseline_BBveto_noMet", 200, 0, 800);
  hTransverseMass_inverted_BBveto_genuineTau =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_inverted_BBveto_genuineTau", "TransverseMass_inverted_BBveto_genuineTau", 200, 0, 800);
  hTransverseMass_baseline_BBveto_genuineTau =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_baseline_BBveto_genuineTau", "TransverseMass_baseline_BBveto_genuineTau", 200, 0, 800);

  hTransverseMass_inverted_BBveto_genuineTau_noMet =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_inverted_BBveto_genuineTau_noMet", "TransverseMass_inverted_BBveto_genuineTau_noMet", 200, 0, 800);
  hTransverseMass_baseline_BBveto_genuineTau_noMet =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_baseline_BBveto_genuineTau_noMet", "TransverseMass_baseline_BBveto_genuineTau_noMet", 200, 0, 800);
  */

  // Other histograms (testing etc.)
  /*
  hTauPt_inv_afterTau =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TauPt_inv_afterTau", "TauPt_inv_afterTau", 200, 0, 1000);
  hTauPt_inv_afterTau_realtau =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TauPt_inv_afterTau_realTau", "TauPt_inv_afterTau_realTau", 200, 0, 1000); 

  hTauPt_inv_afterJets =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TauPt_inv_afterJets", "TauPt_inv_afterJets", 200, 0, 1000);
  hTauPt_inv_afterJets_realtau =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TauPt_inv_afterJets_realTau", "TauPt_inv_afterJets_realTau", 200, 0, 1000); 

  hTauPt_inv_afterBtag =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TauPt_inv_afterBtag", "TauPt_inv_afterBtag", 200, 0, 1000);
  hTauPt_inv_afterBtag_realtau =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TauPt_inv_afterBtag_realTau", "TauPt_inv_afterBtag_realTau", 200, 0, 1000);

  hMet_inv_afterTau =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Met_inv_afterTau", "Met_inv_afterTau", 200, 0, 1000);
  hMet_inv_afterTau_realtau =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Met_inv_afterTau_realTau", "Met_inv_afterTau_realTau", 200, 0, 1000); 

  hMet_inv_afterJets =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Met_inv_afterJets", "Met_inv_afterJets", 200, 0, 1000);
  hMet_inv_afterJets_realtau =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Met_inv_afterJets_realTau", "Met_inv_afterJets_realTau", 200, 0, 1000); 

  hMet_inv_afterBtag =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Met_inv_afterBtag", "Met_inv_afterBtag", 200, 0, 1000);
  hMet_inv_afterBtag_realtau =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Met_inv_afterBtag_realTau", "Met_inv_afterBtag_realTau", 200, 0, 1000); 

  hTauPt_baseline_afterTau =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TauPt_baseline_afterTau", "TauPt_baseline_afterTau", 200, 0, 1000);
  hTauPt_baseline_afterTau_realtau =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TauPt_baseline_afterTau_realTau", "TauPt_baseline_afterTau_realTau", 200, 0, 1000); 
  */


  // Book non-common histograms
  // const int nBinsPt   = cfg_PtBinSetting.bins();
  // const double minPt  = cfg_PtBinSetting.min();
  // const double maxPt  = cfg_PtBinSetting.max();
  
  // const int nBinsEta  = cfg_EtaBinSetting.bins();
  // const double minEta = cfg_EtaBinSetting.min();
  // const double maxEta = cfg_EtaBinSetting.max();
 
  // hAssociatedTop_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "associatedTop_Pt", "Associated t pT;p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  // hAssociatedTop_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "associatedTop_Eta", "Associated t eta;#eta", nBinsEta, minEta, maxEta);
  
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


  //================================================================================================   
  // GenParticle analysis
  //================================================================================================   
  // For-loop: GenParticles
  //  if (fEvent.isMC()) {
  //    
  //    for (auto& p: fEvent.genparticles().getGenParticles()) 
  //      {
  //	
  //	int genP_pdgId  = p.pdgId();
  //	double genP_pt  = p.pt();
  //	double genP_eta = p.eta();
  //	// double genP_Status = p.status(); // PYTHIA8: http://home.thep.lu.se/~torbjorn/pythia81html/ParticleProperties.html
  //    }
  //	
  //  }
  


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
  // 4) Trigger SF
  //================================================================================================   
  // if (0) std::cout << "=== MET Trigger SF" << std::endl;
  // const METSelection::Data silentMETData = fMETSelection.silentAnalyze(fEvent, nVertices);
  // if (fEvent.isMC()) {
  //   fEventWeight.multiplyWeight(silentMETData.getMETTriggerSF());
  // }
  // cMetTriggerSFCounter.increment();
  // fCommonPlots.fillControlPlotsAfterMETTriggerScaleFactor(fEvent);
  

  //================================================================================================   
  // 5) Electron veto (Orthogonality)
  //================================================================================================   
  if (0) std::cout << "=== Electron veto" << std::endl;
  const ElectronSelection::Data eData = fElectronSelection.analyze(fEvent);
  if (eData.hasIdentifiedElectrons()) return;


  //================================================================================================
  // 6) Muon veto (Orthogonality)
  //================================================================================================
  if (0) std::cout << "=== Muon veto" << std::endl;
  const MuonSelection::Data muData = fMuonSelection.analyze(fEvent);
  if (muData.hasIdentifiedMuons()) return;


  //================================================================================================   
  // 7) Tau Veto (HToTauNu Orthogonality)
  //================================================================================================   
  if (0) std::cout << "=== Tau-Veto" << std::endl;
  const TauSelection::Data tauData = fTauSelection.analyze(fEvent);
  if (tauData.hasIdentifiedTaus() ) return;


  //================================================================================================
  // 8) Jet selection
  //================================================================================================
  if (0) std::cout << "=== Jet selection" << std::endl;
  const JetSelection::Data jetData = fJetSelection.analyzeWithoutTau(fEvent);
  if (!jetData.passedSelection()) return;


  //================================================================================================
  // Standard Selections
  //================================================================================================
  if (0) std::cout << "=== Standard selection" << std::endl;
  fCommonPlots.fillControlPlotsAfterTopologicalSelections(fEvent, true);
  

  //================================================================================================  
  // 9) BJet selection
  //================================================================================================
  if (0) std::cout << "=== BJet selection" << std::endl;
  // Disable histogram filling and counter with silent analyze
  const BJetSelection::Data bjetData = fBJetSelection.silentAnalyze(fEvent, jetData);


  //================================================================================================  
  // 10) LightJet selection
  //================================================================================================
  if (0) std::cout << "=== LightJet selection" << std::endl;
  const LightJetSelection::Data ljetData = fLightJetSelection.analyze(fEvent, jetData, bjetData);
  if (!ljetData.passedSelection()) return;


  // There are no bjets passing our selection criteria
 //if (bjetData.getNumberOfSelectedBJets() < 1)
  if (!bjetData.passedSelection())
    {
      doInvertedAnalysis(jetData, bjetData, nVertices);
    }
  else 
    {
      doBaselineAnalysis(jetData, bjetData, nVertices);
    }

  return;
}


void FakeBMeasurement::doBaselineAnalysis(const JetSelection::Data& jetData,
                                          const BJetSelection::Data& bjetData,
                                          const int nVertices){

  if (!bjetData.passedSelection()) return;

  // Increment counter
  cBaselineBTaggingCounter.increment();

  //================================================================================================  
  // 10) BJet SF  
  //================================================================================================
  if (0) std::cout << "=== Baseline: BJet SF" << std::endl;
  if (fEvent.isMC()) 
    {
      fEventWeight.multiplyWeight(bjetData.getBTaggingScaleFactorEventWeight());
    }
  cBaselineBTaggingSFCounter.increment();


  //================================================================================================
  // 11) MET selection
  //================================================================================================
  if (0) std::cout << "=== Baseline: MET selection" << std::endl;
  const METSelection::Data METData = fBaselineMETSelection.analyze(fEvent, nVertices);
  if (!METData.passedSelection()) return;


  //================================================================================================
  // 12) Topology selection
  //================================================================================================
  if (0) std::cout << "=== Baseline: Topology selection" << std::endl;
  const TopologySelection::Data TopologyData = fBaselineTopologySelection.analyze(fEvent, jetData);
  if (!TopologyData.passedSelection()) return;


  //================================================================================================
  // 13) Top selection
  //================================================================================================
  if (0) std::cout << "=== Baseline: Top selection" << std::endl;
  const TopSelection::Data TopData = fBaselineTopSelection.analyze(fEvent, jetData, bjetData);
  if (!TopData.passedSelection()) return;


  //================================================================================================
  // All cuts passed
  //================================================================================================
  if (0) std::cout << "=== Baseline: Selected events" << std::endl;
  cBaselineSelected.increment();

  if (0) 
    {
      for (auto bjet: bjetData.getSelectedBJets() ) 
	{
	  std::cout << "PASS: b-discriminator = " << bjet.bjetDiscriminator() << ", pt = " << bjet.pt() << ", eta = " << bjet.eta() 
		    << ", pdgId = " << bjet.pdgId() << ", hadronFlavour = " << bjet.hadronFlavour() << ", partonFlavour = " << bjet.hadronFlavour()
		    << ", originatesFromW() = " << bjet.originatesFromW() << ", originatesFromZ() = " << bjet.originatesFromZ() 
		    << ", originatesFromTop()  = " << bjet.originatesFromTop() << ", originatesFromChargedHiggs() = " << bjet.originatesFromChargedHiggs() 
		    << ", originatesFromUnknown() = " << bjet.originatesFromUnknown() << std::endl;
	}
      std::cout << "\n" << std::endl;
    }
  
  //================================================================================================
  // Fill final plots
  //================================================================================================

  // Other histograms
  hBaseline_TopMassReco_ChiSqr_AfterAllSelections ->Fill(TopData.ChiSqr());
  hBaseline_TopMassReco_LdgTrijetPt_AfterAllSelections->Fill( TopData.getLdgTrijet().pt() );
  hBaseline_TopMassReco_LdgTrijetM_AfterAllSelections ->Fill( TopData.getLdgTrijet().M() );
  hBaseline_TopMassReco_SubLdgTrijetPt_AfterAllSelections->Fill( TopData.getSubldgTrijet().pt() );
  hBaseline_TopMassReco_SubLdgTrijetM_AfterAllSelections ->Fill( TopData.getSubldgTrijet().M() );
  hBaseline_TopMassReco_LdgDijetPt_AfterAllSelections->Fill( TopData.getLdgDijet().pt() );
  hBaseline_TopMassReco_LdgDijetM_AfterAllSelections ->Fill( TopData.getLdgDijet().M() );
  hBaseline_TopMassReco_SubLdgDijetPt_AfterAllSelections->Fill( TopData.getSubldgDijet().pt() );
  hBaseline_TopMassReco_SubLdgDijetM_AfterAllSelections ->Fill( TopData.getSubldgDijet().M() );

  // fCommonPlots.fillControlPlotsAfterAllSelections(fEvent, true);
  // fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hBaselineTransverseMass, isGenuineTau, myTransverseMass);

  // Save selected event ID for pick events
  fEventSaver.save();

  return;
}


void FakeBMeasurement::doInvertedAnalysis(const JetSelection::Data& jetData,
                                          const BJetSelection::Data& bjetData,
                                          const int nVertices){
  
  // Increment counter
  cInvertedBTaggingCounter.increment();

  //================================================================================================  
  // 10) BJet SF (if I have b-jets in the inverted region)
  //================================================================================================
  if (0) std::cout << "=== Inverted: BJet SF" << std::endl;
  if (fEvent.isMC()) 
    {
      fEventWeight.multiplyWeight(bjetData.getBTaggingScaleFactorEventWeight());
    }
  cInvertedBTaggingSFCounter.increment();


  //================================================================================================
  // 11) MET selection
  //================================================================================================
  if (0) std::cout << "=== Inverted: MET selection" << std::endl;
  const METSelection::Data METData = fInvertedMETSelection.analyze(fEvent, nVertices);
  if (!METData.passedSelection()) return;


  //================================================================================================
  // 12) Topology selection
  //================================================================================================
  if (0) std::cout << "=== Inverted: Topology selection" << std::endl;
  const TopologySelection::Data TopologyData = fInvertedTopologySelection.analyze(fEvent, jetData);
  if (!TopologyData.passedSelection()) return;


  //================================================================================================
  // 13) Top selection
  //================================================================================================
  if (0) std::cout << "=== Inverted: Top selection" << std::endl;
  const TopSelection::Data TopData = fInvertedTopSelection.analyzeWithoutBJets(fEvent, jetData, bjetData);
  if (!TopData.passedSelection()) return;


  //================================================================================================
  // All cuts passed
  //================================================================================================
  if (0) std::cout << "=== Inverted: Selected events" << std::endl;
  cInvertedSelected.increment();

  //================================================================================================
  // Fill final plots
  //================================================================================================
  // For-loop: Selected b-jets                                                                                                                                                                                             
  if (0) 
    {
      for (auto bjet: bjetData.getFailedBJetCandsDescendingDiscr() ) 
	{
	  std::cout << "FAIL: b-discriminator = " << bjet.bjetDiscriminator() << ", pt = " << bjet.pt() << ", eta = " << bjet.eta() 
		    << ", pdgId = " << bjet.pdgId() << ", hadronFlavour = " << bjet.hadronFlavour() << ", partonFlavour = " << bjet.hadronFlavour()
		    << ", originatesFromW() = " << bjet.originatesFromW() << ", originatesFromZ() = " << bjet.originatesFromZ() 
		    << ", originatesFromTop()  = " << bjet.originatesFromTop() << ", originatesFromChargedHiggs() = " << bjet.originatesFromChargedHiggs() 
		    << ", originatesFromUnknown() = " << bjet.originatesFromUnknown() << std::endl;
	}
      std::cout << "\n" << std::endl;
    }
  

  Jet bjet= bjetData.getFailedBJetCandsDescendingDiscr()[0];
  bool isGenuineB = abs(bjet.pdgId() == 5); // https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideBTagMCTools#Jet_flavour_in_PAT
  int ancestryBit = pow(0, bjet.originatesFromZ())  
    + pow(1, 2*bjet.originatesFromW())
    + pow(2, 2*bjet.originatesFromTop())
    + pow(3, 2*bjet.originatesFromChargedHiggs())
    + pow(4, 2*bjet.originatesFromUnknown());

  // For real data fill obth the histograms in inclusive and "FakeB" folders (but not "GenuineB")
  hInverted_FailedBJetWithBestBDiscBDisc_AfterAllSelections->Fill(isGenuineB, bjet.bjetDiscriminator());
  hInverted_FailedBJetWithBestBDiscPt_AfterAllSelections->Fill(isGenuineB, bjet.pt());
  hInverted_FailedBJetWithBestBDiscEta_AfterAllSelections->Fill(isGenuineB, bjet.eta());
  hInverted_FailedBJetWithBestBDiscPdgId_AfterAllSelections->Fill(isGenuineB, bjet.pdgId());
  hInverted_FailedBJetWithBestBDiscPartonFlavour_AfterAllSelections->Fill(isGenuineB, bjet.partonFlavour());
  hInverted_FailedBJetWithBestBDiscHadronFlavour_AfterAllSelections->Fill(isGenuineB, bjet.hadronFlavour());
  hInverted_FailedBJetWithBestBDiscAncestry_AfterAllSelections->Fill(isGenuineB, ancestryBit);

  // Other histograms
  hInverted_TopMassReco_ChiSqr_AfterAllSelections ->Fill(TopData.ChiSqr());
  hInverted_TopMassReco_LdgTrijetPt_AfterAllSelections->Fill( TopData.getLdgTrijet().pt() );
  hInverted_TopMassReco_LdgTrijetM_AfterAllSelections ->Fill( TopData.getLdgTrijet().M() );
  hInverted_TopMassReco_SubLdgTrijetPt_AfterAllSelections->Fill( TopData.getSubldgTrijet().pt() );
  hInverted_TopMassReco_SubLdgTrijetM_AfterAllSelections ->Fill( TopData.getSubldgTrijet().M() );
  hInverted_TopMassReco_LdgDijetPt_AfterAllSelections->Fill( TopData.getLdgDijet().pt() );
  hInverted_TopMassReco_LdgDijetM_AfterAllSelections ->Fill( TopData.getLdgDijet().M() );
  hInverted_TopMassReco_SubLdgDijetPt_AfterAllSelections->Fill( TopData.getSubldgDijet().pt() );
  hInverted_TopMassReco_SubLdgDijetM_AfterAllSelections ->Fill( TopData.getSubldgDijet().M() );

  // Save selected event ID for pick events
  fEventSaver.save();

  return;
}
