// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "DataFormat/interface/Event.h"
#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"
#include "EventSelection/interface/TransverseMass.h"

#include "TDirectory.h"

class QCDMeasurement: public BaseSelector {
public:
  explicit QCDMeasurement(const ParameterSet& config, const TH1* skimCounters);
  virtual ~QCDMeasurement();

  /// Books histograms
  virtual void book(TDirectory *dir) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;

private:
  // Input parameters

  /// Common plots
  CommonPlots fCommonPlots;
  CommonPlots fNormalizationSystematicsSignalRegion;
  CommonPlots fNormalizationSystematicsControlRegion;
  // Event selection classes and event counters (in same order like they are applied)
  Count cAllEvents;
  Count cTrigger;
  METFilterSelection fMETFilterSelection;
  Count cVertexSelection;
  TauSelection fTauSelection;
  // Counters for baseline tau leg (note that the event selection objects contain also some main counters)
  Count cBaselineTauTauIDCounter;
  Count cBaselineTauTauIDSFCounter;
  Count cBaselineTauFakeTauSFCounter;
  Count cBaselineTauTauTriggerSFCounter;
  Count cBaselineTauOneTauCounter;
  Count cBaselineTauMetTriggerSFCounter;
  ElectronSelection fBaselineTauElectronSelection;
  MuonSelection fBaselineTauMuonSelection;
  JetSelection fBaselineTauJetSelection;
  AngularCutsCollinear fBaselineTauAngularCutsCollinear;
  BJetSelection fBaselineTauBJetSelection;
  Count cBaselineTauBTaggingSFCounter;
  METSelection fBaselineTauMETSelection;
  AngularCutsBackToBack fBaselineTauAngularCutsBackToBack;
  Count cBaselineTauSelectedEvents;
  // Counters for inverted tau leg (note that the event selection objects contain also some main counters)
  Count cInvertedTauTauIDSFCounter;
  Count cInvertedTauFakeTauSFCounter;
  Count cInvertedTauTauTriggerSFCounter;
  Count cInvertedTauOneTauCounter;
  Count cInvertedTauMetTriggerSFCounter;
  ElectronSelection fInvertedTauElectronSelection;
  MuonSelection fInvertedTauMuonSelection;
  JetSelection fInvertedTauJetSelection;
  AngularCutsCollinear fInvertedTauAngularCutsCollinear;
  BJetSelection fInvertedTauBJetSelection;
  Count cInvertedTauBTaggingSFCounter;
  METSelection fInvertedTauMETSelection;
  AngularCutsBackToBack fInvertedTauAngularCutsBackToBack;
  Count cInvertedTauSelectedEvents;
  
  void doInvertedAnalysis(const Event& event, const Tau& tau, const int nVertices, const bool isGenuineTau);
  void doBaselineAnalysis(const Event& event, const Tau& tau, const int nVertices, const bool isGenuineTau);    
 
  //====== Normalization histograms - baseline tau
  // After standard selections
  HistoSplitter::SplittedTripletTH1s hNormalizationBaselineTauAfterStdSelections;
  HistoSplitter::SplittedTripletTH1s hMtBaselineTauAfterStdSelections; // For QCD shape uncertainty

  //====== Normalization histograms - inverted tau
  // After standard selections
  HistoSplitter::SplittedTripletTH1s hNormalizationInvertedTauAfterStdSelections;
  HistoSplitter::SplittedTripletTH1s hMtInvertedTauAfterStdSelections; // For QCD shape uncertainty

  //  HistoSplitter::SplittedTripletTH1s hClosureTestInvertedTauBveto;
  // HistoSplitter::SplittedTripletTH1s hClosureTestBaselineTauBveto; 


  // Purity histograms (no need to split in bins of tau pt, therefore just a triplet)
  // Add here more purity histograms at different point of event selections, if necessary
  WrappedTH1Triplet* hInvertedTauTauPtAfterAllSelections;
  
  // Other histograms
  HistoSplitter::SplittedTripletTH1s hBaselineTauTransverseMass; // the plot for baseline tau is in common plots
  WrappedTH1 *hTauPt_inv_afterTau_realtau;
  WrappedTH1 *hTauPt_inv_afterTau;
  WrappedTH1 *hTauPt_baseline_afterTau_realtau;
  WrappedTH1 *hTauPt_baseline_afterTau;
  WrappedTH1 *hTauPt_inv_afterJets_realtau;
  WrappedTH1 *hTauPt_inv_afterJets;
  WrappedTH1 *hTauPt_inv_afterBtag_realtau;
  WrappedTH1 *hTauPt_inv_afterBtag;
  WrappedTH1 *hMet_inv_afterTau_realtau;
  WrappedTH1 *hMet_inv_afterTau;
  WrappedTH1 *hMet_inv_afterJets_realtau;
  WrappedTH1 *hMet_inv_afterJets;
  WrappedTH1 *hMet_inv_afterBtag_realtau;
  WrappedTH1 *hMet_inv_afterBtag;
  WrappedTH1 *hTransverseMass_inverted_Bveto;
  WrappedTH1 *hTransverseMass_baseline_Bveto;
  WrappedTH1 *hTransverseMass_inverted_Bveto_genuineTau;
  WrappedTH1 *hTransverseMass_baseline_Bveto_genuineTau;
  WrappedTH1 *hTransverseMass_inverted_all;
  WrappedTH1 *hTransverseMass_baseline_all;
  WrappedTH1 *hTransverseMass_inverted_all_genuineTau;
  WrappedTH1 *hTransverseMass_baseline_all_genuineTau;
  WrappedTH1 *hTransverseMass_inverted_BBveto;
  WrappedTH1 *hTransverseMass_baseline_BBveto;
  WrappedTH1 *hTransverseMass_baseline_Bveto_BBveto;
  WrappedTH1 *hTransverseMass_inverted_Bveto_BBveto;
  WrappedTH1 *hTransverseMass_inverted_BBveto_genuineTau;
  WrappedTH1 *hTransverseMass_baseline_BBveto_genuineTau;
  WrappedTH1 *hTransverseMass_inverted_Bveto_noMet;
  WrappedTH1 *hTransverseMass_baseline_Bveto_noMet;
  WrappedTH1 *hTransverseMass_inverted_BBveto_noMet;
  WrappedTH1 *hTransverseMass_baseline_BBveto_noMet;
  WrappedTH1 *hTransverseMass_baseline_Bveto_BBveto_noMet;
  WrappedTH1 *hTransverseMass_inverted_Bveto_BBveto_noMet;
  WrappedTH1 *hTransverseMass_inverted_Bveto_genuineTau_noMet;
  WrappedTH1 *hTransverseMass_baseline_Bveto_genuineTau_noMet;
  WrappedTH1 *hTransverseMass_inverted_BBveto_genuineTau_noMet;
  WrappedTH1 *hTransverseMass_baseline_BBveto_genuineTau_noMet;

  //WrappedTH1 *hAntiIsolatedTaus;
};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(QCDMeasurement);

QCDMeasurement::QCDMeasurement(const ParameterSet& config, const TH1* skimCounters)
: BaseSelector(config, skimCounters),
  fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kQCDMeasurement, fHistoWrapper),
  fNormalizationSystematicsSignalRegion(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kQCDNormalizationSystematicsSignalRegion, fHistoWrapper),
  fNormalizationSystematicsControlRegion(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kQCDNormalizationSystematicsControlRegion, fHistoWrapper),
  cAllEvents(fEventCounter.addCounter("All events")),
  cTrigger(fEventCounter.addCounter("Passed trigger")),
  fMETFilterSelection(config.getParameter<ParameterSet>("METFilter"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  cVertexSelection(fEventCounter.addCounter("Primary vertex selection")),
  fTauSelection(config.getParameter<ParameterSet>("TauSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  // Baseline tau counters and selection objects (no common plots produced)
  cBaselineTauTauIDCounter(fEventCounter.addCounter("BaselineTau: tau ID")),
  cBaselineTauTauIDSFCounter(fEventCounter.addCounter("BaselineTau: tau ID SF")),
  cBaselineTauFakeTauSFCounter(fEventCounter.addCounter("BaselineTau: fake tau SF")),
  cBaselineTauTauTriggerSFCounter(fEventCounter.addCounter("BaselineTau: tau trigger SF")),
  cBaselineTauOneTauCounter(fEventCounter.addCounter("BaselineTau: exactly one tau")),
  cBaselineTauMetTriggerSFCounter(fEventCounter.addCounter("BaselineTau: met trigger SF")),
  fBaselineTauElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"),
                fEventCounter, fHistoWrapper, nullptr, "VetoBaselineTau"),
  fBaselineTauMuonSelection(config.getParameter<ParameterSet>("MuonSelection"),
                fEventCounter, fHistoWrapper, nullptr, "VetoBaselineTau"),
  fBaselineTauJetSelection(config.getParameter<ParameterSet>("JetSelection"),
                fEventCounter, fHistoWrapper, nullptr, "BaselineTau"),
  fBaselineTauAngularCutsCollinear(config.getParameter<ParameterSet>("AngularCutsCollinear"),
                fEventCounter, fHistoWrapper, nullptr, "BaselineTau"),
  fBaselineTauBJetSelection(config.getParameter<ParameterSet>("BJetSelection"),
                fEventCounter, fHistoWrapper, nullptr, "BaselineTau"),
  cBaselineTauBTaggingSFCounter(fEventCounter.addCounter("BaselineTau: b tag SF")),
  fBaselineTauMETSelection(config.getParameter<ParameterSet>("METSelection"),
                fEventCounter, fHistoWrapper, nullptr, "BaselineTau"),
  fBaselineTauAngularCutsBackToBack(config.getParameter<ParameterSet>("AngularCutsBackToBack"),
                fEventCounter, fHistoWrapper, nullptr, "BaselineTau"),
  cBaselineTauSelectedEvents(fEventCounter.addCounter("BaselineTau: selected events")),
  // Inverted tau counters and selection objects (common plots produced)
  cInvertedTauTauIDSFCounter(fEventCounter.addCounter("InvertedTau: tau ID SF")),
  cInvertedTauFakeTauSFCounter(fEventCounter.addCounter("InvertedTau: fake tau SF")),
  cInvertedTauTauTriggerSFCounter(fEventCounter.addCounter("InvertedTau: tau trigger SF")),
  cInvertedTauOneTauCounter(fEventCounter.addCounter("InvertedTau: exactly one tau")),
  cInvertedTauMetTriggerSFCounter(fEventCounter.addCounter("InvertedTau: met trigger SF")),
  fInvertedTauElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, "VetoInvertedTau"),
  fInvertedTauMuonSelection(config.getParameter<ParameterSet>("MuonSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, "VetoInvertedTau"),
  fInvertedTauJetSelection(config.getParameter<ParameterSet>("JetSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, "InvertedTau"),
  fInvertedTauAngularCutsCollinear(config.getParameter<ParameterSet>("AngularCutsCollinear"),
                fEventCounter, fHistoWrapper, &fCommonPlots, "InvertedTau"),
  fInvertedTauBJetSelection(config.getParameter<ParameterSet>("BJetSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, "InvertedTau"),
  cInvertedTauBTaggingSFCounter(fEventCounter.addCounter("InvertedTau: b tag SF")),
  fInvertedTauMETSelection(config.getParameter<ParameterSet>("METSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, "InvertedTau"),
  fInvertedTauAngularCutsBackToBack(config.getParameter<ParameterSet>("AngularCutsBackToBack"),
                fEventCounter, fHistoWrapper, &fCommonPlots, "InvertedTau"),
  cInvertedTauSelectedEvents(fEventCounter.addCounter("InvertedTau: selected events"))
{ }

QCDMeasurement::~QCDMeasurement() {
  fCommonPlots.getHistoSplitter().deleteHistograms(hNormalizationBaselineTauAfterStdSelections);
  fCommonPlots.getHistoSplitter().deleteHistograms(hMtBaselineTauAfterStdSelections);
  fCommonPlots.getHistoSplitter().deleteHistograms(hNormalizationInvertedTauAfterStdSelections);
  fCommonPlots.getHistoSplitter().deleteHistograms(hMtInvertedTauAfterStdSelections);
  //  fCommonPlots.getHistoSplitter().deleteHistograms(hClosureTestInvertedTauBveto);
  // fCommonPlots.getHistoSplitter().deleteHistograms(hClosureTestBaselineTauBveto);
  delete hInvertedTauTauPtAfterAllSelections;
  fCommonPlots.getHistoSplitter().deleteHistograms(hBaselineTauTransverseMass);
}

void QCDMeasurement::book(TDirectory *dir) {
  // Book common plots histograms
  fCommonPlots.book(dir, isData());
  fNormalizationSystematicsSignalRegion.book(dir, isData());
  fNormalizationSystematicsControlRegion.book(dir, isData());
  //   fCommonPlotsBaselineAfterMetSF(fCommonPlots.createCommonPlotsFilledAtEveryStep("BaselineAfterMetSF",false,"")),
  // Book histograms in event selection classes
  fMETFilterSelection.bookHistograms(dir);
  fTauSelection.bookHistograms(dir);
  
  fBaselineTauElectronSelection.bookHistograms(dir);
  fBaselineTauMuonSelection.bookHistograms(dir);
  fBaselineTauJetSelection.bookHistograms(dir);
  fBaselineTauAngularCutsCollinear.bookHistograms(dir);
  fBaselineTauBJetSelection.bookHistograms(dir);
  fBaselineTauMETSelection.bookHistograms(dir);
  fBaselineTauAngularCutsBackToBack.bookHistograms(dir);

  fInvertedTauElectronSelection.bookHistograms(dir);
  fInvertedTauMuonSelection.bookHistograms(dir);
  fInvertedTauJetSelection.bookHistograms(dir);
  fInvertedTauAngularCutsCollinear.bookHistograms(dir);
  fInvertedTauBJetSelection.bookHistograms(dir);
  fInvertedTauMETSelection.bookHistograms(dir);
  fInvertedTauAngularCutsBackToBack.bookHistograms(dir);

  // ====== Normalization histograms
  HistoSplitter histoSplitter = fCommonPlots.getHistoSplitter();
  // Create directories for normalization
  std::string myInclusiveLabel = "ForQCDNormalization";
  std::string myFakeLabel = myInclusiveLabel+"EWKFakeTaus";
  std::string myGenuineLabel = myInclusiveLabel+"EWKGenuineTaus";
  TDirectory* myNormDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabel);
  TDirectory* myNormEWKFakeTausDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
  TDirectory* myNormGenuineTausDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
  std::vector<TDirectory*> myNormalizationDirs = {myNormDir, myNormEWKFakeTausDir, myNormGenuineTausDir};

  // Normalization bin settings
  const float fMetMin = fCommonPlots.getMetBinSettings().min();
  const float fMetMax = fCommonPlots.getMetBinSettings().max();
  const int nMetBins = fMetMax-fMetMin; // Use 1 GeV bin width
  const int nMtBins = fCommonPlots.getMtBinSettings().bins();
  const float fMtMin = fCommonPlots.getMtBinSettings().min();
  const float fMtMax = fCommonPlots.getMtBinSettings().max();
  if ((fMetMax-fMetMin) / nMetBins > 10.0) {
    throw hplus::Exception("config") << "MET histogram bin width is larger than 10 GeV! This is not good for QCD measurement (edit python/parameters/signalAnalysisParameters.py)";
  }
  // Create normalization histograms for baseline tau (use kSystematics only for the primary normalization histogram, otherwise kInformative)
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myNormalizationDirs,
    hNormalizationBaselineTauAfterStdSelections,
    "NormalizationMETBaselineTauAfterStdSelections", ";MET (GeV);N_{events}",
    nMetBins, fMetMin, fMetMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myNormalizationDirs,
    hMtBaselineTauAfterStdSelections,
    "NormalizationMtBaselineTauAfterStdSelections", ";m_{T} (GeV);N_{events}",
    nMtBins, fMtMin, fMtMax);
  
  // Create normalization histograms for inverted tau (use kSystematics only for the primary normalization histogram, otherwise kInformative)
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myNormalizationDirs,
    hNormalizationInvertedTauAfterStdSelections,
    "NormalizationMETInvertedTauAfterStdSelections", ";MET (GeV);N_{events}",
    nMetBins, fMetMin, fMetMax);
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myNormalizationDirs,
    hMtInvertedTauAfterStdSelections,
    "NormalizationMtInvertedTauAfterStdSelections", ";m_{T} (GeV);N_{events}",
    nMtBins, fMtMin, fMtMax);

  // ====== Purity histograms
  // Create directories and obtain binning
  myInclusiveLabel = "QCDPurity";
  myFakeLabel = myInclusiveLabel+"EWKFakeTaus";
  myGenuineLabel = myInclusiveLabel+"EWKGenuineTaus";
  TDirectory* myPurityDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabel);
  TDirectory* myPurityEWKFakeTausDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
  TDirectory* myPurityGenuineTausDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
  std::vector<TDirectory*> myPurityDirs = {myPurityDir, myPurityEWKFakeTausDir, myPurityGenuineTausDir};
  const int nPtBins = fCommonPlots.getPtBinSettings().bins();
  const float fPtMin = fCommonPlots.getPtBinSettings().min();
  const float fPtMax = fCommonPlots.getPtBinSettings().max();
  // Create purity histograms
  hInvertedTauTauPtAfterAllSelections = fHistoWrapper.makeTHTriplet<TH1F>(true, HistoLevel::kInformative, myPurityDirs,
                                                                          "InvertedTauTauPtAfterAllSelections",
                                                                          "InvertedTauTauPtAfterAllSelections:#tau p_{T} (GeV):N_{events}",
                                                                          nPtBins, fPtMin, fPtMax);

  // ====== Other histograms
  // Create directories for other plots and obtain binning
  myInclusiveLabel = "ForQCDMeasurement";
  myFakeLabel = myInclusiveLabel+"EWKFakeTaus";
  myGenuineLabel = myInclusiveLabel+"EWKGenuineTaus";
  TDirectory* myQCDDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myInclusiveLabel);
  TDirectory* myQCDEWKFakeTausDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myFakeLabel);
  TDirectory* myQCDGenuineTausDir = fHistoWrapper.mkdir(HistoLevel::kSystematics, dir, myGenuineLabel);
  std::vector<TDirectory*> myQCDPlotDirs = {myQCDDir, myQCDEWKFakeTausDir, myQCDGenuineTausDir};

  // Create shape histograms for baseline tau (inverted tau histograms are in common plots)
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


  // Other histograms (testing etc.)
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


}

void QCDMeasurement::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}

void QCDMeasurement::process(Long64_t entry) {

//====== Initialize
  fCommonPlots.initialize();
  fNormalizationSystematicsSignalRegion.initialize();
  fNormalizationSystematicsControlRegion.initialize();
  cAllEvents.increment();
  int nVertices = fEvent.vertexInfo().value();
  fCommonPlots.setNvertices(nVertices);
  fNormalizationSystematicsSignalRegion.setNvertices(nVertices);
  fNormalizationSystematicsControlRegion.setNvertices(nVertices);

//====== Apply trigger
  if (!(fEvent.passTriggerDecision()))
    return;
  cTrigger.increment();
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
  std::vector<float> myFactorisationInfo;
  if (tauData.isAntiIsolated()) {
    // There are only anti-isolated taus -> inverted
    if (tauData.hasAntiIsolatedTaus()) {
      // Sanity check passed: at least one anti-isolated tau exists
      // Set factorisation bin
      myFactorisationInfo.push_back(tauData.getAntiIsolatedTau().pt());
      fCommonPlots.setFactorisationBinForEvent(myFactorisationInfo);
      fNormalizationSystematicsControlRegion.setFactorisationBinForEvent(myFactorisationInfo);
      fNormalizationSystematicsControlRegion.fillControlPlotsAfterTauSelection(fEvent, tauData);

      //====== Tau ID SF 
      if (fEvent.isMC()) {
	// inverted = not passed tau id = no SF used.
	//fEventWeight.multiplyWeight(tauData.getTauIDSF());
      }
      cInvertedTauTauIDSFCounter.increment();

      // Apply fake tau SF
      if (fEvent.isMC()) {
        fEventWeight.multiplyWeight(tauData.getAntiIsolatedTauMisIDSF());
      }
      cInvertedTauFakeTauSFCounter.increment();
      // Apply tau trigger SF
      if (fEvent.isMC()) {
        fEventWeight.multiplyWeight(tauData.getAntiIsolatedTauTriggerSF());
      }
      cInvertedTauTauTriggerSFCounter.increment();
      if (tauData.getAntiIsolatedTaus().size() == 1) {
        cInvertedTauOneTauCounter.increment();
      }
      // Do rest of event selection
      doInvertedAnalysis(fEvent, tauData.getAntiIsolatedTau(), nVertices, tauData.getAntiIsolatedTauIsGenuineTau());
    }
  } else {
    // There is an isolated tau -> baseline
    if (tauData.hasIdentifiedTaus()) {
      // Sanity check passed: at least one isolated tau exists
      // Set factorisation bin
      myFactorisationInfo.push_back(tauData.getSelectedTau().pt());
      fCommonPlots.setFactorisationBinForEvent(myFactorisationInfo);
      fNormalizationSystematicsSignalRegion.setFactorisationBinForEvent(myFactorisationInfo);
      fNormalizationSystematicsSignalRegion.fillControlPlotsAfterTauSelection(fEvent, tauData);

      cBaselineTauTauIDCounter.increment();
      //====== Tau ID SF       
      if (fEvent.isMC()) {
	fEventWeight.multiplyWeight(tauData.getTauIDSF());
      }
      cBaselineTauTauIDSFCounter.increment();

      // Apply fake tau SF
      if (fEvent.isMC()) {
        fEventWeight.multiplyWeight(tauData.getTauMisIDSF());
      }
      cBaselineTauFakeTauSFCounter.increment();
      // Apply tau trigger SF
      if (fEvent.isMC()) {
        fEventWeight.multiplyWeight(tauData.getTauTriggerSF());
      }
      cBaselineTauTauTriggerSFCounter.increment();
      if (tauData.getSelectedTaus().size() == 1) {
        cBaselineTauOneTauCounter.increment();
      }
      // Do rest of event selection
      doBaselineAnalysis(fEvent, tauData.getSelectedTau(), nVertices, tauData.isGenuineTau());
    }
  }
  // If further tests or selections are needed, please include them in the doInvertedAnalysis/doBaselineAnalysis methods
}
 
////////////////////////////////////////////////////////////////////////////////////////////////

void QCDMeasurement::doBaselineAnalysis(const Event& event, const Tau& tau, const int nVertices, const bool isGenuineTau) {
//====== MET trigger SF
  const METSelection::Data silentMETData = fBaselineTauMETSelection.silentAnalyze(fEvent, nVertices);
  if (event.isMC()) {
    fEventWeight.multiplyWeight(silentMETData.getMETTriggerSF());
  }
  cBaselineTauMetTriggerSFCounter.increment();
  //std::cout << "Baseline: met=" << silentMETData.getMET().R() << ", SF=" << silentMETData.getMETTriggerSF() << std::endl;


  if (event.isMC()) {
    if (isGenuineTau) hTauPt_baseline_afterTau_realtau->Fill(tau.pt());
  }
  if (!event.isMC() ) {
    hTauPt_baseline_afterTau->Fill(tau.pt());
  }
  if (event.isMC() && !isGenuineTau ) {
    hTauPt_baseline_afterTau->Fill(tau.pt());
  }
  
//====== Electron veto
  const ElectronSelection::Data eData = fBaselineTauElectronSelection.analyze(event);
  if (eData.hasIdentifiedElectrons())
    return;

//====== Muon veto
  const MuonSelection::Data muData = fBaselineTauMuonSelection.analyze(event);
  if (muData.hasIdentifiedMuons())
    return;

//====== Jet selection
  const JetSelection::Data jetData = fBaselineTauJetSelection.analyze(event, tau);
  if (!jetData.passedSelection())
    return;

//====== Collinear angular cuts
  const double METvalue = silentMETData.getMET().R();
  const AngularCutsCollinear::Data collinearData = fBaselineTauAngularCutsCollinear.analyze(fEvent, tau, jetData, silentMETData);
  if (!collinearData.passedSelection())
    return;

//====== Point of standard selections
  double myTransverseMass = TransverseMass::reconstruct(tau, silentMETData.getMET());
  const BJetSelection::Data silentBjetData = fBaselineTauBJetSelection.silentAnalyze(fEvent, jetData);
  const AngularCutsBackToBack::Data silentBackToBackData = fBaselineTauAngularCutsBackToBack.silentAnalyze(fEvent, tau, jetData, silentMETData);
  fNormalizationSystematicsSignalRegion.setGenuineTauStatus(isGenuineTau);
  fNormalizationSystematicsSignalRegion.fillControlPlotsForQCDShapeUncertainty(fEvent, collinearData, silentBjetData, silentMETData, silentBackToBackData);
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hNormalizationBaselineTauAfterStdSelections, isGenuineTau, METvalue);
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hMtBaselineTauAfterStdSelections, isGenuineTau, myTransverseMass);
  
//====== b-jet selection
  const BJetSelection::Data bjetData = fBaselineTauBJetSelection.analyze(fEvent, jetData);
  if (!bjetData.passedSelection()) {
   // plot closure test
    hTransverseMass_baseline_Bveto_noMet->Fill(myTransverseMass);

    if (!silentBackToBackData.passedSelection()) hTransverseMass_baseline_Bveto_BBveto_noMet->Fill(myTransverseMass);
    if (event.isMC() && isGenuineTau ) {
      hTransverseMass_baseline_Bveto_genuineTau_noMet->Fill(myTransverseMass);
    }

    if (silentMETData.passedSelection()) {  
      //      if (silentBackToBackData.passedSelection()) {
	hTransverseMass_baseline_Bveto->Fill(myTransverseMass);
	if (!silentBackToBackData.passedSelection()) hTransverseMass_baseline_Bveto_BBveto->Fill(myTransverseMass);
	if (event.isMC() && isGenuineTau ) {
	  hTransverseMass_baseline_Bveto_genuineTau->Fill(myTransverseMass);
	}
	//     }
    }
    return;
  }
  if (!silentBackToBackData.passedSelection()) {
    hTransverseMass_baseline_BBveto_noMet->Fill(myTransverseMass);
    if (event.isMC() && isGenuineTau ) {
      hTransverseMass_baseline_BBveto_genuineTau_noMet->Fill(myTransverseMass);
    }

  }


//====== b tag SF
  if (fEvent.isMC()) {
    fEventWeight.multiplyWeight(bjetData.getBTaggingScaleFactorEventWeight());
    cBaselineTauBTaggingSFCounter.increment();
  }

//====== MET selection
  const METSelection::Data METData = fBaselineTauMETSelection.analyze(fEvent, nVertices);
  if (!METData.passedSelection())
    return;
  
//====== Back-to-back angular cuts
  const AngularCutsBackToBack::Data backToBackData = fBaselineTauAngularCutsBackToBack.analyze(fEvent, tau, jetData, METData);
  if (!backToBackData.passedSelection()) {

    hTransverseMass_baseline_BBveto->Fill(myTransverseMass);
    if (event.isMC() && isGenuineTau ) {
      hTransverseMass_baseline_BBveto_genuineTau->Fill(myTransverseMass);
    }

    return;
  }


//====== All cuts passed
  cBaselineTauSelectedEvents.increment();
  // Fill final plots
  
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hBaselineTauTransverseMass, isGenuineTau, myTransverseMass);
  
//====== Experimental code

  hTransverseMass_baseline_all->Fill(myTransverseMass);
   if (event.isMC() && isGenuineTau ) {
    hTransverseMass_baseline_all_genuineTau->Fill(myTransverseMass);
   }
//====== Save selected event ID for pick events
  fEventSaver.save();
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void QCDMeasurement::doInvertedAnalysis(const Event& event, const Tau& tau, const int nVertices, const bool isGenuineTau) {


//====== MET trigger SF
  const METSelection::Data silentMETData = fInvertedTauMETSelection.silentAnalyze(fEvent, nVertices);

  if (event.isMC()) {
    fEventWeight.multiplyWeight(silentMETData.getMETTriggerSF());
  }
  cInvertedTauMetTriggerSFCounter.increment();
  fCommonPlots.fillControlPlotsAfterMETTriggerScaleFactor(fEvent);
  //std::cout << "Inverted: met=" << silentMETData.getMET().R() << ", SF=" << silentMETData.getMETTriggerSF() << std::endl;

  if (event.isMC()) {
    if (isGenuineTau) hTauPt_inv_afterTau_realtau->Fill(tau.pt());
    if (isGenuineTau) hMet_inv_afterTau_realtau->Fill(silentMETData.getMET().R());
  }
  if (!event.isMC() ) {
    hTauPt_inv_afterTau->Fill(tau.pt());
    hMet_inv_afterTau->Fill(silentMETData.getMET().R());
  }
  if (event.isMC() && !isGenuineTau ) {
    hTauPt_inv_afterTau->Fill(tau.pt());
    hMet_inv_afterTau->Fill(silentMETData.getMET().R());
  }


//====== Electron veto
  const ElectronSelection::Data eData = fInvertedTauElectronSelection.analyze(event);
  if (eData.hasIdentifiedElectrons())
    return;

//====== Muon veto
  const MuonSelection::Data muData = fInvertedTauMuonSelection.analyze(event);
  if (muData.hasIdentifiedMuons())
    return;

//====== Jet selection
  const JetSelection::Data jetData = fInvertedTauJetSelection.analyze(event, tau);
  if (!jetData.passedSelection())
    return;

  if (event.isMC()) {
    if (isGenuineTau) hTauPt_inv_afterJets_realtau->Fill(tau.pt());
    if (isGenuineTau) hMet_inv_afterJets_realtau->Fill(silentMETData.getMET().R());
  }
  if (event.isMC() && !isGenuineTau ) {
    hTauPt_inv_afterJets->Fill(tau.pt());
    hMet_inv_afterJets->Fill(silentMETData.getMET().R());
  }
  if (!event.isMC() ) {
    hTauPt_inv_afterJets->Fill(tau.pt());
    hMet_inv_afterJets->Fill(silentMETData.getMET().R());
  }
//====== Collinear angular cuts
  const double METvalue = silentMETData.getMET().R();
  const AngularCutsCollinear::Data collinearData = fInvertedTauAngularCutsCollinear.analyze(fEvent, tau, jetData, silentMETData);
  if (!collinearData.passedSelection())
    return;

//====== Point of standard selections
  double myTransverseMass = TransverseMass::reconstruct(tau, silentMETData.getMET());
  fCommonPlots.fillControlPlotsAfterTopologicalSelections(fEvent);
  const BJetSelection::Data silentBjetData = fInvertedTauBJetSelection.silentAnalyze(fEvent, jetData);
  const AngularCutsBackToBack::Data silentBackToBackData = fInvertedTauAngularCutsBackToBack.silentAnalyze(fEvent, tau, jetData, silentMETData);
  fNormalizationSystematicsControlRegion.setGenuineTauStatus(isGenuineTau);
  fNormalizationSystematicsControlRegion.fillControlPlotsForQCDShapeUncertainty(fEvent, collinearData, silentBjetData, silentMETData, silentBackToBackData);
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hNormalizationInvertedTauAfterStdSelections, isGenuineTau, METvalue);
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hMtInvertedTauAfterStdSelections, isGenuineTau, myTransverseMass);
 
 
//====== b-jet selection
  const BJetSelection::Data bjetData = fInvertedTauBJetSelection.analyze(fEvent, jetData);
  if (!bjetData.passedSelection()) {
    hTransverseMass_inverted_Bveto_noMet->Fill(myTransverseMass);
    if (event.isMC() && isGenuineTau ) {
      hTransverseMass_inverted_Bveto_genuineTau_noMet->Fill(myTransverseMass);
    }

    if (!silentBackToBackData.passedSelection()) hTransverseMass_inverted_Bveto_BBveto_noMet->Fill(myTransverseMass);
    // plot closure test
    if (silentMETData.passedSelection()) {  
      //      if (silentBackToBackData.passedSelection()) {
	hTransverseMass_inverted_Bveto->Fill(myTransverseMass);
	if (!silentBackToBackData.passedSelection()) hTransverseMass_inverted_Bveto_BBveto->Fill(myTransverseMass);
	if (event.isMC() && isGenuineTau ) {
	  hTransverseMass_inverted_Bveto_genuineTau->Fill(myTransverseMass);
	}
	//     }
    } 
    return;
  }
  if (!silentBackToBackData.passedSelection()) {
    hTransverseMass_inverted_BBveto_noMet->Fill(myTransverseMass);
    if (event.isMC() && isGenuineTau ) {
      hTransverseMass_inverted_BBveto_genuineTau_noMet->Fill(myTransverseMass);
    }

  }

//====== b tag SF
  if (fEvent.isMC()) {
    fEventWeight.multiplyWeight(bjetData.getBTaggingScaleFactorEventWeight());
    cInvertedTauBTaggingSFCounter.increment();
  }



  if (event.isMC()) {
    if (isGenuineTau) hTauPt_inv_afterBtag_realtau->Fill(tau.pt());
    if (isGenuineTau) hMet_inv_afterBtag_realtau->Fill(silentMETData.getMET().R());
  }

  if (event.isMC() && !isGenuineTau ) {
    hTauPt_inv_afterBtag->Fill(tau.pt());
    hMet_inv_afterBtag->Fill(silentMETData.getMET().R());
  }
  if (!event.isMC()) {
    hTauPt_inv_afterBtag->Fill(tau.pt());
    hMet_inv_afterBtag->Fill(silentMETData.getMET().R());
  }

//====== MET selection
  const METSelection::Data METData = fInvertedTauMETSelection.analyze(fEvent, nVertices);
  if (!METData.passedSelection())
    return;
  
//====== Back-to-back angular cuts
  const AngularCutsBackToBack::Data backToBackData = fInvertedTauAngularCutsBackToBack.analyze(fEvent, tau, jetData, METData);
  if (!backToBackData.passedSelection()) {
    hTransverseMass_inverted_BBveto->Fill(myTransverseMass);
    if (event.isMC() && isGenuineTau ) {
      hTransverseMass_inverted_BBveto_genuineTau->Fill(myTransverseMass);
    }
    return;
  }

//====== All cuts passed
  cInvertedTauSelectedEvents.increment();
  // Fill final plots
  fCommonPlots.fillControlPlotsAfterAllSelections(fEvent);
  hInvertedTauTauPtAfterAllSelections->Fill(isGenuineTau, tau.pt());
  
//====== Experimental code
  hTransverseMass_inverted_all->Fill(myTransverseMass);
  if (event.isMC() && isGenuineTau ) {
    hTransverseMass_inverted_all_genuineTau->Fill(myTransverseMass);
  }

//====== Save selected event ID for pick events
  fEventSaver.save();
}
