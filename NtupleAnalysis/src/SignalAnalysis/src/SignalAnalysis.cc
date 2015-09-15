// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

#include "TDirectory.h"

class SignalAnalysis: public BaseSelector {
public:
  explicit SignalAnalysis(const ParameterSet& config);
  virtual ~SignalAnalysis() {}

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
  Count cMETFilters;
  Count cVertexSelection;
  TauSelection fTauSelection;
  ElectronSelection fElectronSelection;
  MuonSelection fMuonSelection;
  JetSelection fJetSelection;
  AngularCutsCollinear fAngularCutsCollinear;
  BJetSelection fBJetSelection;
  METSelection fMETSelection;
  AngularCutsBackToBack fAngularCutsBackToBack;
  JetCorrelations fJetCorrelations;
  Count cSelected;
    
  // Non-common histograms
 

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(SignalAnalysis);

SignalAnalysis::SignalAnalysis(const ParameterSet& config)
: BaseSelector(config),
  fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kSignalAnalysis, fHistoWrapper),
  cAllEvents(fEventCounter.addCounter("All events")),
  cTrigger(fEventCounter.addCounter("Passed trigger")),
  cPrescaled(fEventCounter.addCounter("Prescaled")),
  cPileupWeighted(fEventCounter.addCounter("Weighted events with PU")),
  cTopPtReweighted(fEventCounter.addCounter("Weighted events with top pT")),
  cExclusiveSamplesWeighted(fEventCounter.addCounter("Weighted events for exclusive samples")),
  cMETFilters(fEventCounter.addCounter("MET filters")),
  cVertexSelection(fEventCounter.addCounter("Primary vertex selection")),
  fTauSelection(config.getParameter<ParameterSet>("TauSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
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
  fMETSelection(config.getParameter<ParameterSet>("METSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  fAngularCutsBackToBack(config.getParameter<ParameterSet>("AngularCutsBackToBack"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  fJetCorrelations(config.getParameter<ParameterSet>("JetCorrelations"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  cSelected(fEventCounter.addCounter("Selected events"))
{ }

void SignalAnalysis::book(TDirectory *dir) {
  // Book common plots histograms
  fCommonPlots.book(dir);
  // Book histograms in event selection classes
  fTauSelection.bookHistograms(dir);
  fElectronSelection.bookHistograms(dir);
  fMuonSelection.bookHistograms(dir);
  fJetSelection.bookHistograms(dir);
  fAngularCutsCollinear.bookHistograms(dir);
  fBJetSelection.bookHistograms(dir);
  fMETSelection.bookHistograms(dir);
  fAngularCutsBackToBack.bookHistograms(dir);
  fJetCorrelations.bookHistograms(dir);
  // Book non-common histograms
  //hExample =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "example pT", "example pT", 40, 0, 400);


}

void SignalAnalysis::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}

void SignalAnalysis::process(Long64_t entry) {

//====== Initialize
  fCommonPlots.initialize();
  fCommonPlots.setFactorisationBinForEvent(std::vector<float> {});

  cAllEvents.increment();

//====== Apply trigger // FIXME to be debugged
  if (!(fEvent.passTriggerDecision()))
    return;
  cTrigger.increment();
 
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
  
//====== MET filters to remove events with spurious sources of fake MET // FIXME missing code
  cMETFilters.increment();
  
//====== GenParticle analysis
  // if needed
  
//====== Check that primary vertex exists
  int nVertices = fEvent.NPU().value();
  if (nVertices < 1)
    return;
  cVertexSelection.increment();
  fCommonPlots.setNvertices(nVertices);
  
//====== Setup common events // FIXME missing code
    
//====== Tau selection
  const TauSelection::Data tauData = fTauSelection.analyze(fEvent);
  if (!tauData.hasIdentifiedTaus())
    return;

//====== Electron veto
  const ElectronSelection::Data eData = fElectronSelection.analyze(fEvent);
  if (eData.hasIdentifiedElectrons())
    return;

//====== Muon veto
  const MuonSelection::Data muData = fMuonSelection.analyze(fEvent);
  if (muData.hasIdentifiedMuons())
    return;

//====== Jet selection
  const JetSelection::Data jetData = fJetSelection.analyze(fEvent, tauData);
  if (!jetData.passedSelection())
    return;

//====== Collinear angular cuts
  const METSelection::Data silentMETData = fMETSelection.silentAnalyze(fEvent, nVertices);
  const AngularCutsCollinear::Data collinearData = fAngularCutsCollinear.analyze(fEvent, tauData, jetData, silentMETData);
  if (!collinearData.passedSelection())
    return;

//====== Point of standard selections
  fCommonPlots.fillControlPlotsAfterMETTriggerScaleFactor(fEvent);
  fCommonPlots.fillControlPlotsAfterTopologicalSelections(fEvent);

//====== b-jet selection
  const BJetSelection::Data bjetData = fBJetSelection.analyze(fEvent, jetData);

  // Apply b tag scale factor
  // FIXME missing code
  // Fill final shape plots with b tag efficiency applied as an event weight
  if (silentMETData.passedSelection()) {
    const AngularCutsBackToBack::Data silentBackToBackData = fAngularCutsBackToBack.silentAnalyze(fEvent, tauData, jetData, silentMETData);
    if (silentBackToBackData.passedSelection()) {
      fCommonPlots.fillControlPlotsAfterAllSelectionsWithProbabilisticBtag(fEvent, silentMETData, bjetData.getBTaggingPassProbability());
    }
  }
  if (!bjetData.passedSelection())
    return;


//====== MET selection
  const METSelection::Data METData = fMETSelection.analyze(fEvent, nVertices);
  if (!METData.passedSelection())
    return;
  //  std::cout << "   Correlations "  << std::endl;       

  //  const JetCorrelations::Data jetCorrelationsData = fJetCorrelations.analyze(fEvent, jetData,tauData, METData);  

//====== Back-to-back angular cuts
  const AngularCutsBackToBack::Data backToBackData = fAngularCutsBackToBack.analyze(fEvent, tauData, jetData, METData);
  if (!backToBackData.passedSelection())
    return;

//====== All cuts passed
  cSelected.increment();
  // Fill final plots
  fCommonPlots.fillControlPlotsAfterAllSelections(fEvent);
  

//====== Experimental selection code
  const JetCorrelations::Data jetCorrelationsData = fJetCorrelations.analyze(fEvent, jetData,tauData, METData);


  // if necessary
  
//====== Finalize
  fEventSaver.save();
}
