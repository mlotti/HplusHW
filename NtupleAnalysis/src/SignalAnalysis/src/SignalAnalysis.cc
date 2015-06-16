// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "DataFormat/interface/Event.h"
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

  /// Event
  Event fEvent;
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
  BJetSelection fBJetSelection;
  Count cSelected;
    
  // Non-common histograms

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(SignalAnalysis);

SignalAnalysis::SignalAnalysis(const ParameterSet& config)
: BaseSelector(config),
  fEvent(config),
  fCommonPlots(),
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
  fBJetSelection(config.getParameter<ParameterSet>("BJetSelection"),
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
  fBJetSelection.bookHistograms(dir);
  // Book non-common histograms
  //hExample =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "example pT", "example pT", 40, 0, 400);
}

void SignalAnalysis::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}

void SignalAnalysis::process(Long64_t entry) {
  cAllEvents.increment();

//====== Apply trigger // FIXME to be debugged
//   if (!(fEvent.passTriggerDecision()))
//     return;
  cTrigger.increment();
  
//====== Set prescale // FIXME missing code
  cPrescaled.increment();
  
//====== PU reweighting // FIXME missing code
  //fEventWeight.multiplyWeight(0.5);
  cPileupWeighted.increment();

//====== Top pT weighting // FIXME missing code
  cTopPtReweighted.increment();
  
//====== Combining of W+jets and Z+jets inclusive and exclusive samples // FIXME missing code
  cExclusiveSamplesWeighted.increment();
  
//====== MET filters to remove events with spurious sources of fake MET // FIXME missing code
  cMETFilters.increment();
  
//====== GenParticle analysis
  // if needed
  
//====== Check that primary vertex exists // FIXME missing code
  cVertexSelection.increment();
  
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

//====== Collinear angular cuts // FIXME missing code  

//====== b-jet selection
  const BJetSelection::Data bjetData = fBJetSelection.analyze(fEvent, jetData);
  if (!bjetData.passedSelection())
    return;

//====== MET selection // FIXME missing code
  
//====== Back-to-back angular cuts // FIXME missing code  

//====== All cuts passed
  // Fill final plots // FIXME missing code

//====== Experimental selection code
  // if necessary
  
//====== Finalize
  fEventSaver.save();
}
