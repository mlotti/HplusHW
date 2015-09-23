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
  explicit QCDMeasurement(const ParameterSet& config);
  virtual ~QCDMeasurement() {}

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
  // Event selection classes and event counters (in same order like they are applied)
  Count cAllEvents;
  Count cTrigger;
  Count cPrescaled;
  Count cPileupWeighted;
  Count cTopPtReweighted;
  Count cExclusiveSamplesWeighted;
  METFilterSelection fMETFilterSelection;
  Count cVertexSelection;
  TauSelection fTauSelection;
  // Counters for baseline tau leg (note that the event selection objects contain also some main counters)
  Count cBaselineTauFakeTauSFCounter;
  Count cBaselineTauTauTriggerSFCounter;
  Count cBaselineTauOneTauCounter;
  ElectronSelection fBaselineTauElectronSelection;
  MuonSelection fBaselineTauMuonSelection;
  JetSelection fBaselineTauJetSelection;
  Count cBaselineTauMetTriggerSFCounter;
  AngularCutsCollinear fBaselineTauAngularCutsCollinear;
  BJetSelection fBaselineTauBJetSelection;
  Count cBaselineTauBTaggingSFCounter;
  METSelection fBaselineTauMETSelection;
  AngularCutsBackToBack fBaselineTauAngularCutsBackToBack;
  Count cBaselineTauSelectedEvents;
  // Counters for inverted tau leg (note that the event selection objects contain also some main counters)
  Count cInvertedTauFakeTauSFCounter;
  Count cInvertedTauTauTriggerSFCounter;
  Count cInvertedTauOneTauCounter;
  ElectronSelection fInvertedTauElectronSelection;
  MuonSelection fInvertedTauMuonSelection;
  JetSelection fInvertedTauJetSelection;
  Count cInvertedTauMetTriggerSFCounter;
  AngularCutsCollinear fInvertedTauAngularCutsCollinear;
  BJetSelection fInvertedTauBJetSelection;
  Count cInvertedTauBTaggingSFCounter;
  METSelection fInvertedTauMETSelection;
  AngularCutsBackToBack fInvertedTauAngularCutsBackToBack;
  Count cInvertedTauSelectedEvents;
  
  void doInvertedAnalysis(const Event& event, const Tau& tau, const int nVertices, const bool isFakeTau);
  void doBaselineAnalysis(const Event& event, const Tau& tau, const int nVertices, const bool isFakeTau);    
 
  // Normalization histograms - baseline tau
  HistoSplitter::SplittedTripletTH1s hNormalizationBaselineTauAfterStdSelections;

  // Normalization histograms - inverted tau
  HistoSplitter::SplittedTripletTH1s hNormalizationInvertedTauAfterStdSelections;

  // Other histograms
  HistoSplitter::SplittedTripletTH1s hBaselineTauTransverseMass; // the plot for inverted tau is in common plots
  
  //WrappedTH1 *hSelectedTaus;
  //WrappedTH1 *hAntiIsolatedTaus;
};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(QCDMeasurement);

QCDMeasurement::QCDMeasurement(const ParameterSet& config)
: BaseSelector(config),
  fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kQCDMeasurement, fHistoWrapper),
  cAllEvents(fEventCounter.addCounter("All events")),
  cTrigger(fEventCounter.addCounter("Passed trigger")),
  cPrescaled(fEventCounter.addCounter("Prescaled")),
  cPileupWeighted(fEventCounter.addCounter("Weighted events with PU")),
  cTopPtReweighted(fEventCounter.addCounter("Weighted events with top pT")),
  cExclusiveSamplesWeighted(fEventCounter.addCounter("Weighted events for exclusive samples")),
  fMETFilterSelection(config.getParameter<ParameterSet>("METFilter"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  cVertexSelection(fEventCounter.addCounter("Primary vertex selection")),
  fTauSelection(config.getParameter<ParameterSet>("TauSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  // Baseline tau counters and selection objects (no common plots produced)
  cBaselineTauFakeTauSFCounter(fEventCounter.addCounter("BaselineTau: fake tau SF")),
  cBaselineTauTauTriggerSFCounter(fEventCounter.addCounter("BaselineTau: tau trigger SF")),
  cBaselineTauOneTauCounter(fEventCounter.addCounter("BaselineTau: exactly one tau")),
  fBaselineTauElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"),
                fEventCounter, fHistoWrapper, nullptr, "VetoBaselineTau"),
  fBaselineTauMuonSelection(config.getParameter<ParameterSet>("MuonSelection"),
                fEventCounter, fHistoWrapper, nullptr, "VetoBaselineTau"),
  fBaselineTauJetSelection(config.getParameter<ParameterSet>("JetSelection"),
                fEventCounter, fHistoWrapper, nullptr, "BaselineTau"),
  cBaselineTauMetTriggerSFCounter(fEventCounter.addCounter("BaselineTau: met trigger SF")),
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
  cInvertedTauFakeTauSFCounter(fEventCounter.addCounter("InvertedTau: fake tau SF")),
  cInvertedTauTauTriggerSFCounter(fEventCounter.addCounter("InvertedTau: tau trigger SF")),
  cInvertedTauOneTauCounter(fEventCounter.addCounter("InvertedTau: exactly one tau")),
  fInvertedTauElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, "VetoInvertedTau"),
  fInvertedTauMuonSelection(config.getParameter<ParameterSet>("MuonSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, "VetoInvertedTau"),
  fInvertedTauJetSelection(config.getParameter<ParameterSet>("JetSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, "InvertedTau"),
  cInvertedTauMetTriggerSFCounter(fEventCounter.addCounter("InvertedTau: met trigger SF")),
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

void QCDMeasurement::book(TDirectory *dir) {
  // Book common plots histograms
  fCommonPlots.book(dir);
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
  TDirectory* myNormDir = fHistoWrapper.mkdir(HistoLevel::kInformative, dir, myInclusiveLabel);
  TDirectory* myNormEWKFakeTausDir = fHistoWrapper.mkdir(HistoLevel::kInformative, dir, myFakeLabel);
  TDirectory* myNormGenuineTausDir = fHistoWrapper.mkdir(HistoLevel::kInformative, dir, myGenuineLabel);
  std::vector<TDirectory*> myNormalizationDirs = {myNormDir, myNormEWKFakeTausDir, myNormGenuineTausDir};

  // Normalization bin settings
  const int nMetBins = 100;
  const float fMetMin = 0.0;
  const float fMetMax = 500.0;
  // Create normalization histograms for baseline tau (use kSystematics only for the primary normalization histogram, otherwise kInformative)
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myNormalizationDirs,
    hNormalizationBaselineTauAfterStdSelections,
    "NormalizationMETBaselineTauAfterStdSelections", ";MET (GeV);N_{events}",
    nMetBins, fMetMin, fMetMax);
  
  // Create normalization histograms for inverted tau (use kSystematics only for the primary normalization histogram, otherwise kInformative)
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kSystematics, myNormalizationDirs,
    hNormalizationInvertedTauAfterStdSelections,
    "NormalizationMETInvertedTauAfterStdSelections", ";MET (GeV);N_{events}",
    nMetBins, fMetMin, fMetMax);
  
  // ====== Other histograms
  // Create directories for other plots
  myInclusiveLabel = "ForQCDMeasurement";
  myFakeLabel = myInclusiveLabel+"EWKFakeTaus";
  myGenuineLabel = myInclusiveLabel+"EWKGenuineTaus";
  TDirectory* myQCDDir = fHistoWrapper.mkdir(HistoLevel::kInformative, dir, myInclusiveLabel);
  TDirectory* myQCDEWKFakeTausDir = fHistoWrapper.mkdir(HistoLevel::kInformative, dir, myFakeLabel);
  TDirectory* myQCDGenuineTausDir = fHistoWrapper.mkdir(HistoLevel::kInformative, dir, myGenuineLabel);
  std::vector<TDirectory*> myQCDPlotDirs = {myQCDDir, myQCDEWKFakeTausDir, myQCDGenuineTausDir};
  const int nMtBins = fCommonPlots.getMtBinSettings().bins();
  const float fMtMin = fCommonPlots.getMtBinSettings().min();
  const float fMtMax = fCommonPlots.getMtBinSettings().max();

  // Create shape histograms for baseline tau (inverted tau histograms are in common plots)
  histoSplitter.createShapeHistogramTriplet<TH1F>(true, HistoLevel::kInformative, myQCDPlotDirs,
    hBaselineTauTransverseMass,
    "BaselineTauShapeTransverseMass", ";m_{T} (GeV);N_{events}",
    nMtBins, fMtMin, fMtMax);
  
  // Other histograms (testing etc.)
  
}

void QCDMeasurement::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}

void QCDMeasurement::process(Long64_t entry) {

//====== Initialize
  fCommonPlots.initialize();
  cAllEvents.increment();

//====== Apply trigger
  if (!(fEvent.passTriggerDecision()))
    return;
  cTrigger.increment();
  
//====== Set prescale // FIXME missing code
  cPrescaled.increment();
  
//====== PU reweighting // FIXME missing code
  if (fEvent.isMC()) {
    //fEventWeight.multiplyWeight(0.5);
    cPileupWeighted.increment();
  }

//====== Top pT weighting // FIXME missing code
  if (fEvent.isMC()) {
    cTopPtReweighted.increment();
  }
  
//====== Combining of W+jets and Z+jets inclusive and exclusive samples // FIXME missing code
  cExclusiveSamplesWeighted.increment();
  
//====== MET filters to remove events with spurious sources of fake MET
  const METFilterSelection::Data metFilterData = fMETFilterSelection.analyze(fEvent);
  if (!metFilterData.passedSelection())
    return;
  
//====== GenParticle analysis
  // if needed
  
//====== Check that primary vertex exists
  int nVertices = fEvent.vertexInfo().value();
  if (nVertices < 1)
    return;
  cVertexSelection.increment();
  fCommonPlots.setNvertices(nVertices);

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
      // Apply fake tau SF
      if (fEvent.isMC()) {
        // FIXME: code for applying the SF is currently missing
        cBaselineTauFakeTauSFCounter.increment();
      }
      // Apply tau trigger SF
      // FIXME: code for applying the SF is currently missing
      cBaselineTauTauTriggerSFCounter.increment();
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
      // Apply fake tau SF
      if (fEvent.isMC()) {
        // FIXME: code for applying the SF is currently missing
        cInvertedTauFakeTauSFCounter.increment();
      }
      // Apply tau trigger SF
      // FIXME: code for applying the SF is currently missing
      cInvertedTauTauTriggerSFCounter.increment();
      // Do rest of event selection
      doBaselineAnalysis(fEvent, tauData.getSelectedTau(), nVertices, tauData.isGenuineTau());
    }
  }
  // If further tests or selections are needed, please include them in the doInvertedAnalysis/doBaselineAnalysis methods
}
 
////////////////////////////////////////////////////////////////////////////////////////////////

void QCDMeasurement::doBaselineAnalysis(const Event& event, const Tau& tau, const int nVertices, const bool isFakeTau) {
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

//====== MET trigger SF
  // FIXME: code for applying the SF is currently missing
  cBaselineTauMetTriggerSFCounter.increment();

//====== Collinear angular cuts
  const METSelection::Data silentMETData = fBaselineTauMETSelection.silentAnalyze(fEvent, nVertices);
  const double METvalue = silentMETData.getMET().R();
  const AngularCutsCollinear::Data collinearData = fBaselineTauAngularCutsCollinear.analyze(fEvent, tau, jetData, silentMETData);
  if (!collinearData.passedSelection())
    return;

//====== Point of standard selections
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hNormalizationBaselineTauAfterStdSelections, isFakeTau, METvalue);
  
//====== b-jet selection
  const BJetSelection::Data bjetData = fBaselineTauBJetSelection.analyze(fEvent, jetData);
  if (!bjetData.passedSelection())
    return;

//====== b tag SF
  if (fEvent.isMC()) {
    // FIXME missing code
    cBaselineTauBTaggingSFCounter.increment();
  }

//====== MET selection
  const METSelection::Data METData = fBaselineTauMETSelection.analyze(fEvent, nVertices);
  if (!METData.passedSelection())
    return;
  
//====== Back-to-back angular cuts
  const AngularCutsBackToBack::Data backToBackData = fBaselineTauAngularCutsBackToBack.analyze(fEvent, tau, jetData, METData);
  if (!backToBackData.passedSelection())
    return;

//====== All cuts passed
  cBaselineTauSelectedEvents.increment();
  // Fill final plots
  double myTransverseMass = TransverseMass::reconstruct(tau, METData.getMET());
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hBaselineTauTransverseMass, isFakeTau, myTransverseMass);
  
//====== Experimental code

//====== Save selected event ID for pick events
  fEventSaver.save();
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void QCDMeasurement::doInvertedAnalysis(const Event& event, const Tau& tau, const int nVertices, const bool isFakeTau) {
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

//====== MET trigger SF
  // FIXME: code for applying the SF is currently missing
  cInvertedTauMetTriggerSFCounter.increment();

//====== Collinear angular cuts
  const METSelection::Data silentMETData = fInvertedTauMETSelection.silentAnalyze(fEvent, nVertices);
  const double METvalue = silentMETData.getMET().R();
  const AngularCutsCollinear::Data collinearData = fInvertedTauAngularCutsCollinear.analyze(fEvent, tau, jetData, silentMETData);
  if (!collinearData.passedSelection())
    return;

//====== Point of standard selections
  fCommonPlots.fillControlPlotsAfterTopologicalSelections(fEvent);
  fCommonPlots.getHistoSplitter().fillShapeHistogramTriplet(hNormalizationInvertedTauAfterStdSelections, isFakeTau, METvalue);
  
//====== b-jet selection
  const BJetSelection::Data bjetData = fInvertedTauBJetSelection.analyze(fEvent, jetData);
  if (!bjetData.passedSelection())
    return;

//====== b tag SF
  if (fEvent.isMC()) {
    // FIXME missing code
    cInvertedTauBTaggingSFCounter.increment();
  }

//====== MET selection
  const METSelection::Data METData = fInvertedTauMETSelection.analyze(fEvent, nVertices);
  if (!METData.passedSelection())
    return;
  
//====== Back-to-back angular cuts
  const AngularCutsBackToBack::Data backToBackData = fInvertedTauAngularCutsBackToBack.analyze(fEvent, tau, jetData, METData);
  if (!backToBackData.passedSelection())
    return;

//====== All cuts passed
  cInvertedTauSelectedEvents.increment();
  // Fill final plots
  //double myTransverseMass = TransverseMass::reconstruct(tau, METData.getMET());
  fCommonPlots.fillControlPlotsAfterAllSelections(fEvent);
  
//====== Experimental code

//====== Save selected event ID for pick events
  fEventSaver.save();
}
