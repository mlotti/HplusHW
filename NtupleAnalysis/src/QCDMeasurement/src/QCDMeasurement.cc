// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "DataFormat/interface/Event.h"
#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

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
  
  void doInvertedAnalysis(const Event& event, const TauSelection::Data& tauData, const int nVertices);
  void doBaselineAnalysis(const Event& event, const TauSelection::Data& tauData, const int nVertices);    
 
  // Non-common histograms
  WrappedTH1 *hSelectedTaus;
  WrappedTH1 *hAntiIsolatedTaus;
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
  cBaselineTauMetTriggerSFCounter(fEventCounter.addCounter("BaselineTau: met trigger SF")),
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
  cInvertedTauFakeTauSFCounter(fEventCounter.addCounter("InvertedTau: fake tau SF")),
  cInvertedTauTauTriggerSFCounter(fEventCounter.addCounter("InvertedTau: tau trigger SF")),
  cInvertedTauOneTauCounter(fEventCounter.addCounter("InvertedTau: exactly one tau")),
  fInvertedTauElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, "VetoInvertedTau"),
  fInvertedTauMuonSelection(config.getParameter<ParameterSet>("MuonSelection"),
                fEventCounter, fHistoWrapper, &fCommonPlots, "VetoInvertedTau"),
  cInvertedTauMetTriggerSFCounter(fEventCounter.addCounter("InvertedTau: met trigger SF")),
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

  // Book histograms defined in this analysis module
  // For normalization
  
  // For testing
  
}

void QCDMeasurement::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}

void QCDMeasurement::process(Long64_t entry) {

//====== Initialize
  fCommonPlots.initialize();
  fCommonPlots.setFactorisationBinForEvent(std::vector<float> {});

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
  if (tauData.isAntiIsolated()) {
    // There are only anti-isolated taus -> inverted
    doInvertedAnalysis(fEvent, tauData, nVertices);
  } else {
    // There is an isolated tau -> baseline
    doBaselineAnalysis(fEvent, tauData, nVertices);
  }
  // If further tests or selections are needed, please include them in the doInvertedAnalysis/doBaselineAnalysis methods
}
 
  ////////////////////////////////////////////////////////////////////////////////////////////////

void QCDMeasurement::doBaselineAnalysis( const Event& event, const TauSelection::Data& tauData, const int nVertices ) {
  //====== Electron veto
  const ElectronSelection::Data eData = fElectronSelection.analyze(event);
  if (eData.hasIdentifiedElectrons())
    return false;
  cBaselineEvetoCounter.increment();
  //====== Muon veto
  const MuonSelection::Data muData = fMuonSelection.analyze(event);
  if (muData.hasIdentifiedMuons())
    return false;
  cBaselineMuvetoCounter.increment();
 
  //====== Jet selection
  const JetSelection::Data jetData = fJetSelection.analyze(event, tauData);
  if (!jetData.passedSelection())
    return false;
  cBaselineJetsCounter.increment();

  const METSelection::Data silentMETData = fMETSelection.silentAnalyze(event, nVertices); 
  //  myHandler.fillShapeHistogram(hMETBaselineTauIdAfterJets, silentMETData.getSelectedMET()->et());
  //  myHandler.fillShapeHistogram(hMETBaselineTauIdAfterMetSF, silentMETdata.getSelectedMET()->et());
  //  fCommonPlotsBaselineAfterMetSF->fill();
  //double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTau()), *(silentMETData.getSelectedMET()));
  //  myHandler.fillShapeHistogram(hMTBaselineTauIdAfterMetSF, transverseMass);
  const BJetSelection::Data silentBjetData = fBJetSelection.silentAnalyze(event, jetData);
  //  if (silentBtagData.passedEvent()) {
  //    myHandler.fillShapeHistogram(hMETBaselineTauIdAfterMetSFPlusBtag, silentMETData.getSelectedMET()->et(), myWeightWithBtagSF);
  //  }
  //  if (silentBtagData.getSelectedJets().size() < 1) {
  //   myHandler.fillShapeHistogram(hMETBaselineTauIdAfterMetSFPlusBveto, silentMETData.getSelectedMET()->et(), myWeightWithBtagSF);
  // }



  //====== Collinear angular cuts
   const AngularCutsCollinear::Data collinearData = fAngularCutsCollinear.analyze(event, tauData, jetData, silentMETData);
  if (!collinearData.passedSelection())
    return false;
  cBaselineQCDTailKillerCollinearCounter.increment();

  const AngularCutsBackToBack::Data silentBackToBackData = fAngularCutsBackToBack.silentAnalyze(event, tauData, jetData, METData);


  /*
  // At this point, let's fill histograms for closure test and for normalisation
    myHandler.fillShapeHistogram(hMETBaselineTauIdAfterCollinearCuts, silentMETData.getSelectedMET()->et()); // no btag scale factor needed
    if (tauData.isGenuineTau() || iEvent.isRealData() || (!tauData.isGenuineTau() && !tauMatchData.isEWKFakeTauLike())) {
	myHandler.fillShapeHistogram(hMETBaselineTauIdAfterCollinearCutsPlusFilteredEWKFakeTaus, silentMETData.getSelectedMET()->et());
    } else {
	myHandler.fillShapeHistogram(hMETBaselineTauIdAfterCollinearCutsOnlyEWKFakeTaus, silentMETData.getSelectedMET()->et());
    }

    myHandler.fillShapeHistogram(hMTBaselineTauIdAfterCollinearCuts, transverseMass); // no btag scale factor needed
    if (invariantMass > 0.) myHandler.fillShapeHistogram(hInvMassBaselineTauIdAfterCollinearCuts, invariantMass);
    fCommonPlotsBaselineAfterCollinearCuts->fill();

 
    // Fill normalization systematics plots
    fNormalizationSystematicsSignalRegion.fillAllControlPlots(iEvent, transverseMass);
    // Use btag scale factor in histogram filling if btagging or btag veto is applied
    // double myWeightWithBtagSF = fEventWeight.getWeight() * btagDataTmp.getScaleFactor();
    hNBBaselineTauIdJet->Fill(silentBtagData.getSelectedJets().size(), myWeightWithBtagSF);
    if (silentBtagData.passedEvent()) {
      // mT with b veto in bins
      myHandler.fillShapeHistogram(hMTBaselineTauIdAfterCollinearCutsPlusBtag, transverseMass, myWeightWithBtagSF);
      fCommonPlotsBaselineAfterCollinearCutsPlusBtag->fill();
      if ( silentBackToBackData.passedSelection() ) {
        myHandler.fillShapeHistogram(hMTBaselineTauIdAfterCollinearCutsPlusBtagPlusBackToBackCuts, transverseMass, myWeightWithBtagSF);
        fCommonPlotsBaselineAfterCollinearCutsPlusBtagPlusBackToBackCuts->fill();
      }
    }
    if (silentBtagData.getSelectedJets().size() < 1) {
      // mT with b veto in bins
      myHandler.fillShapeHistogram(hMETBaselineTauIdAfterCollinearCutsPlusBveto, silentMetData.getSelectedMET()->et(), myWeightWithBtagSF);
      myHandler.fillShapeHistogram(hMTBaselineTauIdAfterCollinearCutsPlusBveto, transverseMass, myWeightWithBtagSF);
      fCommonPlotsBaselineAfterCollinearCutsPlusBveto->fill();
      if ( silentBackToBackData.passedSelection()) {
        myHandler.fillShapeHistogram(hMTBaselineTauIdAfterCollinearCutsPlusBvetoPlusBackToBackCuts, transverseMass, myWeightWithBtagSF);
        fCommonPlotsBaselineAfterCollinearCutsPlusBvetoPlusBackToBackCuts->fill();
      }
    }

  */

  // bool isGenuineTau() 
  // getFakeTauID() const


//====== Point of standard selections
  fCommonPlots.fillControlPlotsAfterMETTriggerScaleFactor(event);
  fCommonPlots.fillControlPlotsAfterTopologicalSelections(event);

//====== b-jet selection
  const BJetSelection::Data bjetData = fBJetSelection.analyze(event, jetData);

  // Apply b tag scale factor
  // FIXME missing code
  // Fill final shape plots with b tag efficiency applied as an event weight
  if (silentMETData.passedSelection()) {
    const AngularCutsBackToBack::Data silentBackToBackData = fAngularCutsBackToBack.silentAnalyze(event, tauData, jetData, silentMETData);
    if (silentBackToBackData.passedSelection()) {
      fCommonPlots.fillControlPlotsAfterAllSelectionsWithProbabilisticBtag(event, silentMETData, bjetData.getBTaggingPassProbability());
    }
  }
  if (!bjetData.passedSelection())
    return false;
  cBaselineBtagCounter.increment();

//====== MET selection
  const METSelection::Data METData = fMETSelection.analyze(event, nVertices);
  if (!METData.passedSelection())
    return false;
  cBaselineMetCounter.increment();


//====== Back-to-back angular cuts
  const AngularCutsBackToBack::Data backToBackData = fAngularCutsBackToBack.analyze(event, tauData, jetData, METData);
  if (!backToBackData.passedSelection())
    return false;
  cBaselineQCDTailKillerBackToBackCounter.increment();
  /*
  if (qcdTailKillerDataCollinear.passedBackToBackCuts()) {
      myHandler.fillShapeHistogram(hMETBaselineTauIdAfterCollinearCutsPlusBackToBackCuts, metDataTmp.getSelectedMET()->et());
      if (tauMatchData.isGenuineTau() || iEvent.isRealData() || (!tauMatchData.isGenuineTau() && !tauMatchData.isEWKFakeTauLike())) {
	myHandler.fillShapeHistogram(hMETBaselineTauIdAfterCollinearCutsPlusBackToBackCutsPlusFilteredEWKFakeTaus, metDataTmp.getSelectedMET()->et());
      } else {
	myHandler.fillShapeHistogram(hMETBaselineTauIdAfterCollinearCutsPlusBackToBackCutsOnlyEWKFakeTaus, metDataTmp.getSelectedMET()->et());
      }
      myHandler.fillShapeHistogram(hMTBaselineTauIdAfterCollinearCutsPlusBackToBackCuts, transverseMass);
      if (invariantMass > 0.) myHandler.fillShapeHistogram(hInvMassBaselineTauIdAfterCollinearCutsPlusBackToBackCuts, invariantMass);
      fCommonPlotsBaselineAfterCollinearCutsPlusBackToBackCuts->fill();
    }
  */


//====== All cuts passed
//  cSelected.increment();
  cBaselineSelectedEventsCounter.increment();
  // Fill final plots
  fCommonPlots.fillControlPlotsAfterAllSelections(event);
  
//====== Finalize
  fEventSaver.save();
  return true;
}


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void QCDMeasurement::doInvertedAnalysis( const Event& event, const TauSelection::Data& tauData, const int nVertices ) {

  myHandler.fillShapeHistogram(hQCDMeasurementIdSelectedTauEtAfterTauVeto, tauData.getSelectedTau()->pt());

  //====== Electron veto
  const ElectronSelection::Data eData = fElectronSelection.silentAnalyze(event);
  if (eData.hasIdentifiedElectrons())
    return false;
  cInvertedElectronVetoCounter.increment();

//====== Muon veto
  const MuonSelection::Data muData = fMuonSelection.silentAnalyze(event);
  if (muData.hasIdentifiedMuons())
    return false;
  cInvertedMuonVetoCounter.increment();

//====== Jet selection
  const JetSelection::Data jetData = fJetSelection.silentAnalyze(event, tauData);
  if (!jetData.passedSelection())
    return false;
  cInvertedNJetsCounter.increment();

//====== Collinear angular cuts
  const METSelection::Data silentMETData = fMETSelection.silentAnalyze(event, nVertices);
  myHandler.fillShapeHistogram(hMETQCDMeasurementIdAfterJets, silentMETData.getSelectedMET()->et());

  // Obtain transverse mass and invariant mass for plotting
  double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTau()), *(silentMETData.getSelectedMET()));
  double deltaPhi = DeltaPhi::reconstruct(*(tauData.getSelectedTau()), *(silentMETData.getSelectedMET())) * 57.3; // converted to degrees
  BTagging::Data silentBtagData = fBTagging.silentAnalyze(iEvent, iSetup, jetData.getSelectedJets());

  myHandler.fillShapeHistogram(hQCDMeasurementIdSelectedTauEtAfterJetCut, tauData.getSelectedTau()->pt());
  myHandler.fillShapeHistogram(hMETQCDMeasurementIdAfterMetSF, silentMETData.getSelectedMET()->et());
  myHandler.fillShapeHistogram(hMTQCDMeasurementIdAfterMetSF, transverseMass);




  const AngularCutsCollinear::Data collinearData = fAngularCutsCollinear.silentAnalyze(event, tauData, jetData, silentMETData);
  fCommonPlots.fillControlPlotsAtCollinearDeltaPhiCuts(iEvent, CollinearData);
  if (!collinearData.passedSelection())
    return false;
  fCommonPlots.fillControlPlotsAtCollinearDeltaPhiCuts(iEvent, CollinearData);
  fCommonPlotsInvertedAfterCollinearCuts->fill();

 



  myHandler.fillShapeHistogram(hQCDMeasurementIdSelectedTauEtAfterCollinearCuts, tauData.getSelectedTau()->pt());
  myHandler.fillShapeHistogram(hMETQCDMeasurementIdAfterCollinearCuts, silentMETData.getSelectedMET()->et());
    
  if (tauMatchData.isGenuineTau() || iEvent.isRealData() || (!tauMatchData.isGenuineTau() && !tauMatchData.isEWKFakeTauLike())) {
    myHandler.fillShapeHistogram(hMETQCDMeasurementIdAfterCollinearCutsPlusFilteredEWKFakeTaus, metDataTmp.getSelectedMET()->et());
  } else {
    myHandler.fillShapeHistogram(hMETQCDMeasurementIdAfterCollinearCutsOnlyEWKFakeTaus, metDataTmp.getSelectedMET()->et());
  }

  myHandler.fillShapeHistogram(hMTQCDMeasurementIdAfterCollinearCuts, transverseMass);
  if (tauMatchData.isGenuineTau() || iEvent.isRealData() || (!tauMatchData.isGenuineTau() && !tauMatchData.isEWKFakeTauLike()))
    myHandler.fillShapeHistogram(hMTQCDMeasurementIdAfterCollinearCutsPlusFilteredEWKFakeTaus, transverseMass);
  if (invariantMass > 0.) myHandler.fillShapeHistogram(hInvMassQCDMeasurementIdAfterCollinearCuts, invariantMass);
  if (collinearData.passedBackToBackCuts()) {// && metDataTmp.passedEvent() && topSelectionDataTmp.passedEvent()) { // Pass also back-to-back cuts and MET cut
    myHandler.fillShapeHistogram(hMETQCDMeasurementIdAfterCollinearCutsPlusBackToBackCuts, silentMETtData.getSelectedMET()->et());
    if (tauMatchData.isGenuineTau() || iEvent.isRealData() || (!tauMatchData.isGenuineTau() && !tauMatchData.isEWKFakeTauLike())) {
      myHandler.fillShapeHistogram(hMETQCDMeasurementIdAfterCollinearCutsPlusBackToBackCutsPlusFilteredEWKFakeTaus, silentMETData.getSelectedMET()->et());
    } else {
      myHandler.fillShapeHistogram(hMETQCDMeasurementIdAfterCollinearCutsPlusBackToBackCutsOnlyEWKFakeTaus, silentMETData.getSelectedMET()->et());
    }
    myHandler.fillShapeHistogram(hMTQCDMeasurementIdAfterCollinearCutsPlusBackToBackCuts, transverseMass);
    if (invariantMass > 0.) myHandler.fillShapeHistogram(hInvMassQCDMeasurementIdAfterCollinearCutsPlusBackToBackCuts, invariantMass);
    fCommonPlotsInvertedAfterCollinearCutsPlusBackToBackCuts->fill();
  }
  // Fill normalization systematics plots
  fNormalizationSystematicsControlRegion.fillAllControlPlots(iEvent, transverseMass);

  // Use btag scale factor in histogram filling if btagging or btag veto is applied
  //    BTagging::Data btagDataTmp = fBTagging.silentAnalyze(iEvent, iSetup, jetData.getSelectedJets());
  //    double myWeightWithBtagSF = fEventWeight.getWeight() * btagDataTmp.getScaleFactor();
  // MT with b tagging
  if(silentBtagData.passedEvent()) {
    increment(fInvertedBTaggingBeforeMETCounter); // NOTE: Will not give correct value for MC because btag SF is not applied
    myHandler.fillShapeHistogram(hMTQCDMeasurementIdAfterCollinearCutsPlusBtag, transverseMass, myWeightWithBtagSF);
    fCommonPlotsInvertedAfterCollinearCutsPlusBtag->fill();
    if (qcdTailKillerDataCollinear.passedBackToBackCuts()) {
      myHandler.fillShapeHistogram(hMTQCDMeasurementIdAfterCollinearCutsPlusBtagPlusBackToBackCuts, transverseMass, myWeightWithBtagSF);
      fCommonPlotsInvertedAfterCollinearCutsPlusBtag->fill();
    }
  }
  // MT with b veto
  if( btagDataTmp.getSelectedJets().size() < 1) {
    increment(fInvertedBjetVetoCounter);// NOTE: Will not give correct value for MC because btag SF is not applied
    myHandler.fillShapeHistogram(hMETQCDMeasurementIdAfterCollinearCutsPlusBveto, metDataTmp.getSelectedMET()->et(), myWeightWithBtagSF);
    myHandler.fillShapeHistogram(hMTQCDMeasurementIdAfterCollinearCutsPlusBveto, transverseMass, myWeightWithBtagSF);
    fCommonPlotsInvertedAfterCollinearCutsPlusBtag->fill();
    if (qcdTailKillerDataCollinear.passedBackToBackCuts()) {
      myHandler.fillShapeHistogram(hMTQCDMeasurementIdAfterCollinearCutsPlusBvetoPlusBackToBackCuts, transverseMass, myWeightWithBtagSF);
      fCommonPlotsInvertedAfterCollinearCutsPlusBvetoPlusBackToBackCuts->fill();
    }
  }
  





//====== Point of standard selections
  fCommonPlots.fillControlPlotsAfterMETTriggerScaleFactor(event);
  fCommonPlots.fillControlPlotsAfterTopologicalSelections(event);

//====== b-jet selection
  const BJetSelection::Data bjetData = fBJetSelection.silentAnalyze(event, jetData);

  // Apply b tag scale factor
  // FIXME missing code
  // Fill final shape plots with b tag efficiency applied as an event weight
  if (silentMETData.passedSelection()) {
    const AngularCutsBackToBack::Data silentBackToBackData = fAngularCutsBackToBack.silentAnalyze(event, tauData, jetData, silentMETData);
    if (silentBackToBackData.passedSelection()) {
      fCommonPlots.fillControlPlotsAfterAllSelectionsWithProbabilisticBtag(event, silentMETData, bjetData.getBTaggingPassProbability());
    }
  }
  if (!bjetData.passedSelection())
    return false;
  cInvertedBTaggingCounter.increment();

//====== MET selection
  const METSelection::Data METData = fMETSelection.silentAnalyze(event, nVertices);
  if (!METData.passedSelection())
    return false;
  cInvertedMetCounter.increment();

//====== Back-to-back angular cuts
  const AngularCutsBackToBack::Data backToBackData = fAngularCutsBackToBack.silentAnalyze(event, tauData, jetData, METData);
  if (!backToBackData.passedSelection())
    return false;
  cInvertedQCDTailKillerBackToBackCounter.increment();

//====== All cuts passed
  cInvertedSelectedEventsCounter.increment();
  //  cSelected.increment();
  // Fill final plots
  fCommonPlots.fillControlPlotsAfterAllSelections(event);


  return true;}
