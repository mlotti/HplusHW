// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "DataFormat/interface/Event.h"
#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

#include "TDirectory.h"

class BTagEfficiencyAnalysis: public BaseSelector {
public:
  enum BTagPartonType {
    kBTagB,
    kBTagC,
    kBtagG,
    kBtagLight,
  };
  explicit BTagEfficiencyAnalysis(const ParameterSet& config, const TH1* skimCounters);
  virtual ~BTagEfficiencyAnalysis() {}

  /// Books histograms
  virtual void book(TDirectory *dir) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;

private:
  // Input parameters
  const double fJetPtCutMin;
  const double fJetPtCutMax;
  const double fJetEtaCutMin;
  const double fJetEtaCutMax;

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
  METSelection fMETSelection;
  Count cSelected;
    
  // Non-common histograms
  WrappedTH1* hAllBjets;
  WrappedTH1* hAllCjets;
  WrappedTH1* hAllGjets;
  WrappedTH1* hAllLightjets;
  WrappedTH1* hPassedBjets;
  WrappedTH1* hPassedCjets;
  WrappedTH1* hPassedGjets;
  WrappedTH1* hPassedLightjets;
};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(BTagEfficiencyAnalysis);

BTagEfficiencyAnalysis::BTagEfficiencyAnalysis(const ParameterSet& config, const TH1* skimCounters)
: BaseSelector(config, skimCounters),
  fJetPtCutMin(config.getParameter<double>("jetPtCutMin")),
  fJetPtCutMax(config.getParameter<double>("jetPtCutMax")),
  fJetEtaCutMin(config.getParameter<double>("jetEtaCutMin")),
  fJetEtaCutMax(config.getParameter<double>("jetEtaCutMax")),
  cAllEvents(fEventCounter.addCounter("All events")),
  cTrigger(fEventCounter.addCounter("Passed trigger")),
  fMETFilterSelection(config.getParameter<ParameterSet>("METFilter"),
                fEventCounter, fHistoWrapper, nullptr, ""),
  cVertexSelection(fEventCounter.addCounter("Primary vertex selection")),
  fTauSelection(config.getParameter<ParameterSet>("TauSelection"),
                fEventCounter, fHistoWrapper, nullptr, ""),
  cFakeTauSFCounter(fEventCounter.addCounter("Fake tau SF")),
  cTauTriggerSFCounter(fEventCounter.addCounter("Tau trigger SF")),
  cMetTriggerSFCounter(fEventCounter.addCounter("Met trigger SF")),
  fElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"),
                fEventCounter, fHistoWrapper, nullptr, "Veto"),
  fMuonSelection(config.getParameter<ParameterSet>("MuonSelection"),
                fEventCounter, fHistoWrapper, nullptr, "Veto"),
  fJetSelection(config.getParameter<ParameterSet>("JetSelection"),
                fEventCounter, fHistoWrapper, nullptr, ""),
  fAngularCutsCollinear(config.getParameter<ParameterSet>("AngularCutsCollinear"),
                fEventCounter, fHistoWrapper, nullptr, ""),
  fBJetSelection(config.getParameter<ParameterSet>("BJetSelection"),
                fEventCounter, fHistoWrapper, nullptr, ""),
  fMETSelection(config.getParameter<ParameterSet>("METSelection"),
                fEventCounter, fHistoWrapper, nullptr, ""),
  cSelected(fEventCounter.addCounter("Selected events"))
{ }

void BTagEfficiencyAnalysis::book(TDirectory *dir) {
  // Book histograms in event selection classes
  fTauSelection.bookHistograms(dir);
  fElectronSelection.bookHistograms(dir);
  fMuonSelection.bookHistograms(dir);
  fJetSelection.bookHistograms(dir);
  fAngularCutsCollinear.bookHistograms(dir);
  fBJetSelection.bookHistograms(dir);
  fMETSelection.bookHistograms(dir);
  // Book non-common histograms
  hAllBjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllBjets", "allBjets:Jet p_{T}, GeV:N_{jets}", 50, 0, 500);
  hAllCjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllCjets", "allCjets:Jet p_{T}, GeV:N_{jets}", 50, 0, 500);
  hAllGjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllGjets", "allGjets:Jet p_{T}, GeV:N_{jets}", 50, 0, 500);
  hAllLightjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "AllLightjets", "allLightjets:Jet p_{T}, GeV:N_{jets}", 50, 0, 500);
  hPassedBjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelectedBjets", "SelectedBjets:Jet p_{T}, GeV:N_{jets}", 50, 0, 500);
  hPassedCjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelectedCjets", "SelectedCjets:Jet p_{T}, GeV:N_{jets}", 50, 0, 500);
  hPassedGjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelectedGjets", "SelectedGjets:Jet p_{T}, GeV:N_{jets}", 50, 0, 500);
  hPassedLightjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "SelectedLightjets", "SelectedLightjets:Jet p_{T}, GeV:N_{jets}", 50, 0, 500);
}

void BTagEfficiencyAnalysis::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}

void BTagEfficiencyAnalysis::process(Long64_t entry) {

//====== Initialize
  cAllEvents.increment();

//====== Apply trigger
  if (!(fEvent.passTriggerDecision()))
    return;
  cTrigger.increment();

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
  
//====== Tau selection
  const TauSelection::Data tauData = fTauSelection.analyze(fEvent);
  if (!tauData.hasIdentifiedTaus())
    return;
  if (fEvent.isMC() && !tauData.isGenuineTau()) //if not genuine tau, reject the events (fake tau events are taken into account in QCDandFakeTau measurement)
    return;

//====== Tau ID SF
  if (fEvent.isMC()) {
    fEventWeight.multiplyWeight(tauData.getTauIDSF());
//    cTauIDSFCounter.increment();
  }

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
  /*
  const AngularCutsCollinear::Data collinearData = fAngularCutsCollinear.analyze(fEvent, tauData.getSelectedTau(), jetData, silentMETData);
  if (!collinearData.passedSelection())
    return;
  */
  
//====== Point of standard selections
  // Loop over selected jets
  for (auto& p: jetData.getSelectedJets()) {
    // Filter by jet pt and eta
    if (p.pt() < fJetPtCutMin) continue;
    if (p.pt() > fJetPtCutMax) continue;
    if (p.eta() < fJetEtaCutMin) continue;
    if (p.eta() > fJetEtaCutMax) continue;
    // Look for parton flavour
    int id = std::abs(p.pdgId()); // FIXME switch to partonFlavour
    if (id == 5) {
      hAllBjets->Fill(p.pt());
    } else if (id == 4) {
      hAllCjets->Fill(p.pt());
    } else if (id == 21) {
      hAllGjets->Fill(p.pt());
    } else if (id == 1 || id == 2 || id == 3) {
      hAllLightjets->Fill(p.pt());
    }
  }
  // Loop over selected b jets
  const BJetSelection::Data bjetData = fBJetSelection.silentAnalyze(fEvent, jetData);
  for (auto& p: bjetData.getSelectedBJets()) {
    // Filter by jet pt and eta
    if (p.pt() < fJetPtCutMin) continue;
    if (p.pt() > fJetPtCutMax) continue;
    if (p.eta() < fJetEtaCutMin) continue;
    if (p.eta() > fJetEtaCutMax) continue;
    // Look for parton flavour
    int id = std::abs(p.pdgId()); // FIXME switch to partonFlavour
    if (id == 5) {
      hPassedBjets->Fill(p.pt());
    } else if (id == 4) {
      hPassedCjets->Fill(p.pt());
    } else if (id == 21) {
      hPassedGjets->Fill(p.pt());
    } else if (id == 1 || id == 2 || id == 3) {
      hPassedLightjets->Fill(p.pt());
    }
  }
  
//====== All cuts passed
  cSelected.increment();
  // Fill final plots
  

//====== Experimental selection code
  // if necessary
  
//====== Finalize

}
