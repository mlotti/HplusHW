// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"
#include "EventSelection/interface/TransverseMass.h"


#include "TDirectory.h"

class Hplus2hwAnalysis: public BaseSelector {
public:
  explicit Hplus2hwAnalysis(const ParameterSet& config, const TH1* skimCounters);
  virtual ~Hplus2hwAnalysis() {}

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
//  METFilterSelection fMETFilterSelection;
//  METSelection fMETSelection;
  Count cElectronVeto;

  TauSelection fTauSelection;
//  Count cTauSelection;

  MuonSelection fMuonSelection;
//  Count cMuonSelection;

  Count cJetSelection;
//  Count cMETSelection;

  Count cSelected;


  // Non-common histograms

  WrappedTH1 *hTauPt;
  WrappedTH1 *hMuonPt;

  // WrappedTH1 *hTransverseMass_ttRegion;
  // WrappedTH1 *hTransverseMass_WRegion;
  // WrappedTH1 *hTransverseMass_ttRegion_bbcuts;
  // WrappedTH1 *hTransverseMass_WRegion_bbcuts;
};


#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(Hplus2hwAnalysis);


Hplus2hwAnalysis::Hplus2hwAnalysis(const ParameterSet& config, const TH1* skimCounters)
: BaseSelector(config, skimCounters),
  fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kHplus2hwAnalysis, fHistoWrapper),
  cAllEvents(fEventCounter.addCounter("All events")),
//  fMETFilterSelection(config.getParameter<ParameterSet>("METFilter"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
//  fMETSelection(config.getParameter<ParameterSet>("METSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  cElectronVeto(fEventCounter.addCounter("Electron Veto")),
  fTauSelection(config.getParameter<ParameterSet>("TauSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
//  cTauSelection(fEventCounter.addCounter("Tau selection")),
  fMuonSelection(config.getParameter<ParameterSet>("MuonSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
//  cMuonSelection(fEventCounter.addCounter("Muon selection")),
  cJetSelection(fEventCounter.addCounter("Jet selection")),
//  cMETSelection(fEventCounter.addCounter("MET selection")),
  cSelected(fEventCounter.addCounter("Selected events"))
{ }




void Hplus2hwAnalysis::book(TDirectory *dir) {

  // Book common plots histograms
  fCommonPlots.book(dir, isData());

  // Book histograms in event selection classes
//  fMETFilterSelection.bookHistograms(dir);
//  fMETSelection.bookHistograms(dir);

  fTauSelection.bookHistograms(dir);
  fMuonSelection.bookHistograms(dir);

  // Book non-common histograms
  // hAssociatedTop_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "associatedTop_Pt", "Associated t pT;p_{T} (G$
  // hAssociatedTop_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "associatedTop_Eta", "Associated t eta;#eta",$

  hTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt", "Tau pT", 40, 0, 400);
  hMuonPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "muonPt", "Muon pT", 40, 0, 400);
  return;
}


void Hplus2hwAnalysis::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
  return;
}



void Hplus2hwAnalysis::process(Long64_t entry) {

  ////////////
  // Initialize
  ////////////

  fCommonPlots.initialize();
  fCommonPlots.setFactorisationBinForEvent(std::vector<float> {});
  cAllEvents.increment();

  ////////////
  // Apply Trigger
  ////////////

  if (fEvent.isMC()) {
    fEventWeight.multiplyWeight(0.9);
  }

  int nVertices = fEvent.vertexInfo().value();

  ////////////
  // MET filters (to remove events with spurious sources of fake MET)
  ////////////

//  const METFilterSelection::Data metFilterData = fMETFilterSelection.analyze(fEvent);
//  if (!metFilterData.passedSelection()) return;
//  fCommonPlots.fillControlPlotsAfterMETFilter(fEvent);

  ////////////
  // 3) Primarty Vertex (Check that a PV exists)
  ////////////

  if (nVertices < 1)
    return;

  ////////////
  // 4) Electron veto (Fully hadronic + orthogonality)
  ////////////

  size_t nelectrons = 0;
  for(Electron electron: fEvent.electrons()) {
    if(electron.pt() > 15 && std::abs(electron.eta()) < 2.1)
      ++nelectrons;
  }
  if(nelectrons > 0)
    return;
  cElectronVeto.increment();



  //====== Tau ID SF
//  if (fEvent.isMC()) {
//    fEventWeight.multiplyWeight(0.9*0.9);
//  }

  ////////////
  // 6) Tau
  ////////////

//  std::vector<Tau> selectedTaus;
//  for(Tau tau: fEvent.taus()) {
//    if(!tau.decayModeFinding())
//      continue;
//    if(!(tau.pt() > 40))
//      continue;
//    if(!(std::abs(tau.eta()) < 2.4))
//      continue;
//    if(!(tau.lChTrkPt() > 10))
//      continue;
//    if(!(tau.nProngs() == 1))
//      continue;

//    hTauPt->Fill(tau.pt());
//  }
//  if(selectedTaus.empty() || selectedTaus.size() != 2)
//  if(selectedTaus.empty()) // testia varten
//    return;

//  cTauSelection.increment();

  const TauSelection::Data tauData = fTauSelection.analyze(fEvent);
  if (!tauData.hasIdentifiedTaus())
    return;

//  if (fEvent.isMC() && !tauData.isGenuineTau()) //if not genuine tau, reject the events (fake tau events are taken into account in QCDandFakeTau measurement)
//    return;

//  for(unsigned int i =0; i<tauData.getSelectedTaus().size(); i++) {
//    hTauPt->Fill(tauData.getSelectedTaus()[i].pt());
//  }

  if(tauData.getSelectedTaus().size()!=2)
    return;

  ////////////
  // 5) Muon
  ////////////

  const MuonSelection::Data muData = fMuonSelection.analyze(fEvent);
  if(!(muData.hasIdentifiedMuons()))
    return;

  if (muData.getSelectedMuons().size() != 1)
    return;


//  for(Muon muon: fEvent.muons()) {
//    if(!(muon.pt() > 23))
//      continue;
//    if(!(std::abs(muon.eta()) < 2.1))
//      continue;


//    hMuonPt->Fill(muon.pt());
//  }


//  cMuonSelection.increment();


  ////////////
  // 7) Jet selection
  ////////////
/*
  std::vector<Jet> selectedJets;
  for(Jet jet: fEvent.jets()) {
    if(jet.pt() > 30 && std::abs(jet.eta()) < 2.4)
      selectedJets.push_back(jet);
  }
  if(selectedJets.size() < 3)
    return;
  cJetSelection.increment();
*/
  ////////////
  // 8) BJet selection
  ////////////

  ////////////
  // 9) BJet SF
  ////////////

  ////////////
  // 10) MET selection
  ////////////

//  const METSelection::Data METData = fMETSelection.analyze(fEvent, nVertices);
//  if (!METData.passedSelection()) return;
//
//  for(MET mets: fEvent.met()->front()) {
//    if(!(mets.et() > 20))
//      continue;
//  }

//  cMETSelection.increment();

  ////////////
  // All cuts passed
  ////////////


  hTauPt->Fill(tauData.getSelectedTaus()[0].pt());
  hTauPt->Fill(tauData.getSelectedTaus()[1].pt());

  hMuonPt->Fill(muData.getSelectedMuons()[0].pt());

  cSelected.increment();

  ////////////
  // Fill final plots
  ////////////

//  fCommonPlots.fillControlPlotsAfterAllSelections(fEvent);

  ////////////
  // Finalize
  ////////////

  fEventSaver.save();


}
