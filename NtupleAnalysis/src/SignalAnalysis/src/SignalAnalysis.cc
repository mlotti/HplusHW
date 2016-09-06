// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"
#include "EventSelection/interface/TransverseMass.h"

#include "TDirectory.h"

class SignalAnalysis: public BaseSelector {
public:
  explicit SignalAnalysis(const ParameterSet& config, const TH1* skimCounters);
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
  METFilterSelection fMETFilterSelection;
  Count cVertexSelection;
  TauSelection fTauSelection;
  Count cFakeTauSFCounter;
  Count cTauTriggerSFCounter;
  Count cMetTriggerSFCounter;
  ElectronSelection fElectronSelection;
  MuonSelection fMuonSelection;
  JetSelection fJetSelection;
  AngularCutsCollinear fAngularCutsCollinear;
  BJetSelection fBJetSelection;
  Count cBTaggingSFCounter;
  METSelection fMETSelection;
  AngularCutsBackToBack fAngularCutsBackToBack;
  //  JetCorrelations fJetCorrelations;
  Count cSelected;
    
  // Non-common histograms
 
  WrappedTH1 *hTransverseMass_ttRegion;
  //  WrappedTH1 *hTransverseMass_WRegion;
  WrappedTH1 *hTransverseMass_ttRegion_bbcuts;
  //  WrappedTH1 *hTransverseMass_WRegion_bbcuts;
};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(SignalAnalysis);

SignalAnalysis::SignalAnalysis(const ParameterSet& config, const TH1* skimCounters)
: BaseSelector(config, skimCounters),
  fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kSignalAnalysis, fHistoWrapper),
  cAllEvents(fEventCounter.addCounter("All events")),
  cTrigger(fEventCounter.addCounter("Passed trigger")),
  fMETFilterSelection(config.getParameter<ParameterSet>("METFilter"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  cVertexSelection(fEventCounter.addCounter("Primary vertex selection")),
  fTauSelection(config.getParameter<ParameterSet>("TauSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  cFakeTauSFCounter(fEventCounter.addCounter("Fake tau SF")),
  cTauTriggerSFCounter(fEventCounter.addCounter("Tau trigger SF")),
  cMetTriggerSFCounter(fEventCounter.addCounter("Met trigger SF")),
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
  cBTaggingSFCounter(fEventCounter.addCounter("b tag SF")),
  fMETSelection(config.getParameter<ParameterSet>("METSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  fAngularCutsBackToBack(config.getParameter<ParameterSet>("AngularCutsBackToBack"),
                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
// fJetCorrelations(config.getParameter<ParameterSet>("JetCorrelations"),
//                fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  cSelected(fEventCounter.addCounter("Selected events"))
{ }

void SignalAnalysis::book(TDirectory *dir) {
  // Book common plots histograms
  fCommonPlots.book(dir, isData());
  // Book histograms in event selection classes
  fMETFilterSelection.bookHistograms(dir);
  fTauSelection.bookHistograms(dir);
  fElectronSelection.bookHistograms(dir);
  fMuonSelection.bookHistograms(dir);
  fJetSelection.bookHistograms(dir);
  fAngularCutsCollinear.bookHistograms(dir);
  fBJetSelection.bookHistograms(dir);
  fMETSelection.bookHistograms(dir);
  fAngularCutsBackToBack.bookHistograms(dir);
  //  fJetCorrelations.bookHistograms(dir);
  // Book non-common histograms
  //hExample =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "example pT", "example pT", 40, 0, 400);
  hTransverseMass_ttRegion =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_ttRegion", "TransverseMass_ttRegion", 200, 0, 800);
  //  hTransverseMass_WRegion =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_WRegion", "TransverseMass_WRegion", 200, 0, 800);
  hTransverseMass_ttRegion_bbcuts =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_ttRegion_bbcuts", "TransverseMass_ttRegion_bbcuts", 200, 0, 800);
  //  hTransverseMass_WRegion_bbcuts =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass_WRegion", "TransverseMass_WRegion_bbcuts", 200, 0, 800);
}

void SignalAnalysis::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}

void SignalAnalysis::process(Long64_t entry) {

//====== Initialize
  fCommonPlots.initialize();
  fCommonPlots.setFactorisationBinForEvent(std::vector<float> {});

  cAllEvents.increment();

//====== Apply trigger
  if (!(fEvent.passTriggerDecision()))
    return;
  cTrigger.increment();
  int nVertices = fEvent.vertexInfo().value();
  fCommonPlots.setNvertices(nVertices);
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
  if (!tauData.hasIdentifiedTaus())
    return;
  if (fEvent.isMC() && !tauData.isGenuineTau()) //if not genuine tau, reject the events (fake tau events are taken into account in QCDandFakeTau measurement)
    return;
  
//====== Fake tau SF
  if (fEvent.isMC()) {
    fEventWeight.multiplyWeight(tauData.getTauMisIDSF());
    cFakeTauSFCounter.increment();
  }

//====== Tau trigger SF
  if (fEvent.isMC()) {
    fEventWeight.multiplyWeight(tauData.getTauTriggerSF());
    cTauTriggerSFCounter.increment();
  }

//====== MET trigger SF
  const METSelection::Data silentMETData = fMETSelection.silentAnalyze(fEvent, nVertices);
  if (fEvent.isMC()) {
    fEventWeight.multiplyWeight(silentMETData.getMETTriggerSF());
  }
  cMetTriggerSFCounter.increment();
  fCommonPlots.fillControlPlotsAfterMETTriggerScaleFactor(fEvent);
  //std::cout << tauData.getSelectedTau().pt() << ":" << tauData.getTauMisIDSF() << ", " << tauData.getTauTriggerSF() << ", met=" << silentMETData.getMET().R() << ", SF=" << silentMETData.getMETTriggerSF() << std::endl;
  
//====== Electron veto
  const ElectronSelection::Data eData = fElectronSelection.analyze(fEvent);
  if (eData.hasIdentifiedElectrons())
    return;

//====== Muon veto
  const MuonSelection::Data muData = fMuonSelection.analyze(fEvent);
  if (muData.hasIdentifiedMuons())
    return;

//====== Jet selection
  const JetSelection::Data jetData = fJetSelection.analyze(fEvent, tauData.getSelectedTau());
  if (!jetData.passedSelection())
    return;

//====== Collinear angular cuts
  const AngularCutsCollinear::Data collinearData = fAngularCutsCollinear.analyze(fEvent, tauData.getSelectedTau(), jetData, silentMETData);
  //  if (!collinearData.passedSelection())
  //   return;

//====== Point of standard selections
  fCommonPlots.fillControlPlotsAfterTopologicalSelections(fEvent);

//====== b-jet selection
  const BJetSelection::Data bjetData = fBJetSelection.analyze(fEvent, jetData);

  // Fill final shape plots with b tag efficiency applied as an event weight
  if (silentMETData.passedSelection()) {
    const AngularCutsBackToBack::Data silentBackToBackData = fAngularCutsBackToBack.silentAnalyze(fEvent, tauData.getSelectedTau(), jetData, silentMETData);
    if (silentBackToBackData.passedSelection()) {
      fCommonPlots.fillControlPlotsAfterAllSelectionsWithProbabilisticBtag(fEvent, silentMETData, bjetData.getBTaggingPassProbability());
    }
  }
  if (!bjetData.passedSelection())
    return;


//====== b tag SF
  if (fEvent.isMC()) {
    fEventWeight.multiplyWeight(bjetData.getBTaggingScaleFactorEventWeight());
  }
  cBTaggingSFCounter.increment();


//====== MET selection
  const METSelection::Data METData = fMETSelection.analyze(fEvent, nVertices);
  if (!METData.passedSelection())
    return;


  double myTransverseMass = TransverseMass::reconstruct(tauData.getSelectedTau(), METData.getMET());

  if (collinearData.passedSelection()) {
    hTransverseMass_ttRegion->Fill(myTransverseMass);
    //    hTransverseMass_WRegion->Fill(myTransverseMass);
  }
  

  //  const JetCorrelations::Data jetCorrelationsData = fJetCorrelations.analyze(fEvent, jetData,tauData, METData);  

//====== Back-to-back angular cuts
  const AngularCutsBackToBack::Data backToBackData = fAngularCutsBackToBack.analyze(fEvent, tauData.getSelectedTau(), jetData, METData);
  if (!backToBackData.passedSelection())
    return;


  if (!collinearData.passedSelection()) {
    hTransverseMass_ttRegion_bbcuts->Fill(myTransverseMass);
    //    hTransverseMass_WRegion_bbcuts->Fill(myTransverseMass);
  }


//====== All cuts passed
  cSelected.increment();
  // Fill final plots
  fCommonPlots.fillControlPlotsAfterAllSelections(fEvent);
  

//====== Experimental selection code
  // const JetCorrelations::Data jetCorrelationsData = fJetCorrelations.analyze(fEvent, jetData,tauData, METData);


  // if necessary
  
//====== Finalize
  fEventSaver.save();
}
