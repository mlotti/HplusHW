// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"
#include "Framework/interface/TreeWriter.h"

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

  TreeWriter fTreeWriter;
  // Event selection classes and event counters (in same order like they are applied)
  Count cAllEvents;

  MuonSelection fMuonSelection;

  TauSelection fTauSelection;
//  Count cTauSelection;

  Count cOverTwoTausCounter;

  Count cTauIDSFCounter;
  Count cFakeTauSFCounter;


  ElectronSelection fElectronSelection;

  METFilterSelection fMETFilterSelection;

//  MuonSelection fMuonSelection;


//  METSelection fMETSelection;
//  Count cElectronVeto;


//  Count cMuonSelection;

//  Count cJetSelection;
//  Count cMETSelection;

  JetSelection fJetSelection;

  BJetSelection fBJetSelection;

  METSelection fMETSelection;

  Count cSelected;

  double drMuTau1 = 0;

  double drMuTau2 = 0;

  double drTauTau = 0;

  // Non-common histograms

  WrappedTH1 *hTauPt;
  WrappedTH1 *hMuonPt;
  WrappedTH1 *hNJet;

  WrappedTH1 *hTauEta;
  WrappedTH1 *hMuonEta;
  WrappedTH1 *hMET;

  WrappedTH1 *hMuonPt_afterMuonSelection;
  WrappedTH1 *hMuonEta_afterMuonSelection;

  WrappedTH1 *hNTau;
  WrappedTH1 *hTauCharge;

  WrappedTH1 *hCheck;
  WrappedTH1 *hTransverseMass;
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
  fMuonSelection(config.getParameter<ParameterSet>("MuonSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  fTauSelection(config.getParameter<ParameterSet>("TauSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  cOverTwoTausCounter(fEventCounter.addCounter("Over two selected tau leptons")),
  cTauIDSFCounter(fEventCounter.addCounter("Tau ID SF")),
  cFakeTauSFCounter(fEventCounter.addCounter("Fake tau SF")),
  fElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
  fMETFilterSelection(config.getParameter<ParameterSet>("METFilter"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
//  fMuonSelection(config.getParameter<ParameterSet>("MuonSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
//  cTauSelection(fEventCounter.addCounter("Tau selection")),
//  cMuonSelection(fEventCounter.addCounter("Muon selection")),
//  cJetSelection(fEventCounter.addCounter("Jet selection")),
  fJetSelection(config.getParameter<ParameterSet>("JetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
//  cMETSelection(fEventCounter.addCounter("MET selection")),
  fBJetSelection(config.getParameter<ParameterSet>("BJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  fMETSelection(config.getParameter<ParameterSet>("METSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  cSelected(fEventCounter.addCounter("Selected events"))
{ }




void Hplus2hwAnalysis::book(TDirectory *dir) {

  // Book common plots histograms
  fCommonPlots.book(dir, isData());

  // Book histograms in event selection classes
  fMETFilterSelection.bookHistograms(dir);


  fElectronSelection.bookHistograms(dir);
  fTauSelection.bookHistograms(dir);
  fMuonSelection.bookHistograms(dir);
  fJetSelection.bookHistograms(dir);
  fMETSelection.bookHistograms(dir);
  fBJetSelection.bookHistograms(dir);
  // Book non-common histograms
  // hAssociatedTop_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "associatedTop_Pt", "Associated t pT;p_{T} (G$
  // hAssociatedTop_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "associatedTop_Eta", "Associated t eta;#eta",$

  hTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt", "Tau pT", 40, 0, 400);
  hMuonPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "muPt", "Muon pT", 40, 0, 400);
  hMET =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MET", "MET", 40, 0, 400);

  hTauEta =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauEta", "Tau eta", 50, -2.5, 2.5);
  hMuonEta =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "muEta", "Muon eta", 50, -2.5, 2.5);

  hMuonEta_afterMuonSelection =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "muEta_afterMuonSelection", "Muon eta after muon selection", 50, -2.5, 2.5);
  hMuonPt_afterMuonSelection = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "muPt_afterMuonSelection", "Muon pT adter uon selection", 40, 0, 400);

  hNJet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "nJet", "# of jets", 10, 0, 10);
  hNTau =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "nTau", "# of Selected taus", 10, 0, 10);
  hTauCharge = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauCharge", "charge of taus", 6,-3, 3);

  hCheck = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "OS_tau_with_mu_is_genuine", "OS tau with mu is genuine", 6,-3, 3);

  hTransverseMass = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass", "TransverseMass", 200, 0, 2000);

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

  fTreeWriter.initialize();

  fCommonPlots.setFactorisationBinForEvent(std::vector<float> {});
  cAllEvents.increment();


  ////////////
  // Apply Trigger
  ////////////

  if (!(fEvent.passTriggerDecision()))
    return;

  int nVertices = fEvent.vertexInfo().value();

  ////////////
  // 3) Primarty Vertex (Check that a PV exists)
  ////////////

  if (nVertices < 1)
    return;

  ////////////
  // MET filters (to remove events with spurious sources of fake MET)
  ////////////

  const METFilterSelection::Data metFilterData = fMETFilterSelection.analyze(fEvent);
  if (!metFilterData.passedSelection()) 
    return;

  ////////////
  // 5) Muon
  ////////////

  const MuonSelection::Data muData = fMuonSelection.analyze(fEvent);
  if(!(muData.hasIdentifiedMuons()))
    return;

  if (muData.getSelectedMuons().size() != 1)
    return;

  ////////////
  // Dummy Trigger SF for first check
  ////////////

  if (fEvent.isMC()) {
    if (26 <= muData.getSelectedMuons()[0].pt() && muData.getSelectedMuons()[0].pt() < 30) fEventWeight.multiplyWeight(0.9664);
    if (30 <= muData.getSelectedMuons()[0].pt() && muData.getSelectedMuons()[0].pt() < 40) fEventWeight.multiplyWeight(0.9781);
    if (40 <= muData.getSelectedMuons()[0].pt() && muData.getSelectedMuons()[0].pt() < 50) fEventWeight.multiplyWeight(0.9819);
    if (50 <= muData.getSelectedMuons()[0].pt() && muData.getSelectedMuons()[0].pt() < 60) fEventWeight.multiplyWeight(0.9822);
    if (60 <= muData.getSelectedMuons()[0].pt() && muData.getSelectedMuons()[0].pt() < 80) fEventWeight.multiplyWeight(0.9804);
    if (80 <= muData.getSelectedMuons()[0].pt() && muData.getSelectedMuons()[0].pt() < 120) fEventWeight.multiplyWeight(0.9780);
    if (120 <= muData.getSelectedMuons()[0].pt() && muData.getSelectedMuons()[0].pt() < 200) fEventWeight.multiplyWeight(0.9752);
    if (200 <= muData.getSelectedMuons()[0].pt() && muData.getSelectedMuons()[0].pt() < 500) fEventWeight.multiplyWeight(0.9704);

  }

  hMuonPt_afterMuonSelection->Fill(muData.getSelectedMuons()[0].pt());
  hMuonEta_afterMuonSelection->Fill(muData.getSelectedMuons()[0].eta());

  ////////////
  // 6) Tau
  ////////////

  const TauSelection::Data tauData = fTauSelection.analyze(fEvent);
  if (!tauData.hasIdentifiedTaus())
    return;



//  if(fEvent.isMC())  fTreeWriter.write(fEvent,tauData);

  ////////////
  // 7) Jet selection
  ////////////

  const JetSelection::Data jetData = fJetSelection.analyze(fEvent, tauData.getSelectedTau());
  if (!jetData.passedSelection())
    return;


  ////////////
  // 8) BJet selection
  ////////////

  const BJetSelection::Data bjetData = fBJetSelection.analyze(fEvent, jetData);

  if (!bjetData.passedSelection())
    return;

  ////////////
  // 9) BJet SF
  ////////////

  if (fEvent.isMC()) {
    fEventWeight.multiplyWeight(bjetData.getBTaggingScaleFactorEventWeight());
  }
//  cBTaggingSFCounter.increment();
//  fCommonPlots.fillControlPlotsAfterBtagSF(fEvent,jetData,bjetData);


  ////////////
  // 10) MET selection
  ////////////

  const METSelection::Data METData = fMETSelection.analyze(fEvent, nVertices);
  if (!METData.passedSelection())
    return;


//  cMETSelection.increment();

  if(tauData.getSelectedTaus().size() != 2)
    return;

  if(tauData.getSelectedTaus()[0].charge() == tauData.getSelectedTaus()[1].charge())
    return;


  if(fEvent.isMC())  fTreeWriter.write(fEvent,tauData);

  if (fEvent.isMC() && !tauData.getSelectedTaus()[0].isGenuineTau()) {
    return;
  }

  if (fEvent.isMC() && !tauData.getSelectedTaus()[1].isGenuineTau()) {
    return;
  }


/*
  drTauTau = ROOT::Math::VectorUtil::DeltaR(tauData.getSelectedTaus()[0].p4(),tauData.getSelectedTaus()[1].p4());
  if(drTauTau < 0.5)
    return;

*/
  // make sure that the taus are not too close to muon
/*  drMuTau1 = ROOT::Math::VectorUtil::DeltaR(muData.getSelectedMuons()[0].p4(),tauData.getSelectedTaus()[0].p4());
  if(drMuTau1 < 0.5)
    return;

  drMuTau2 = ROOT::Math::VectorUtil::DeltaR(muData.getSelectedMuons()[0].p4(),tauData.getSelectedTaus()[1].p4());
  if(drMuTau2 < 0.5)
    return;
*/
  cOverTwoTausCounter.increment();

  fCommonPlots.fillControlPlotsAfterTauSelection(fEvent, tauData);


  ////////////
  // 6) Tau ID SF
  ////////////

  if (fEvent.isMC()) {
    fEventWeight.multiplyWeight(tauData.getTauIDSF());
//    fEventWeight.multiplyWeight(tauData.getTauIDSF());
    cTauIDSFCounter.increment();
  }

  ////////////
  // 6) Tau misID SF
  ////////////

  if (fEvent.isMC()) {
    fEventWeight.multiplyWeight(tauData.getTauMisIDSF());
    cFakeTauSFCounter.increment();
  }


  if(tauData.getSelectedTaus()[0].decayMode()>1 && tauData.getSelectedTaus()[0].decayMode()<10) {
    return;
  }

  if(tauData.getSelectedTaus()[1].decayMode()>1 && tauData.getSelectedTaus()[1].decayMode()<10) {
    return;
  }

  ////////////
  // 4) Electron veto (Fully hadronic + orthogonality)
  ////////////

  const ElectronSelection::Data eData = fElectronSelection.analyze(fEvent);
  if (eData.hasIdentifiedElectrons())
    return;

//  TTree t("t","a Tree with data");

//  t.Branch("event",&fEvent.taus());

//  t.Fill();;


//  fCommonPlots.fillControlPlotsAfterMETFilter(fEvent);

  ////////////
  // 7) Jet selection
  ////////////

/*  const JetSelection::Data jetData = fJetSelection.analyze(fEvent, tauData.getSelectedTau());
  if (!jetData.passedSelection())
    return;
*/

  ////////////
  // 8) BJet selection
  ////////////

//  const BJetSelection::Data bjetData = fBJetSelection.analyze(fEvent, jetData);

//  if (!bjetData.passedSelection())
//    return;

  ////////////
  // 9) BJet SF
  ////////////

//  if (fEvent.isMC()) {
//    fEventWeight.multiplyWeight(bjetData.getBTaggingScaleFactorEventWeight());
//  }
//  cBTaggingSFCounter.increment();
//  fCommonPlots.fillControlPlotsAfterBtagSF(fEvent,jetData,bjetData);


  ////////////
  // 10) MET selection
  ////////////

//  const METSelection::Data METData = fMETSelection.analyze(fEvent, nVertices);
//  if (!METData.passedSelection())
//    return;


//  cMETSelection.increment();

  ////////////
  // All cuts passed
  ////////////

  // check if the tau lepton that has the SS as the muon is fake or not

  if (fEvent.isMC()) {
    if (tauData.getSelectedTaus()[0].charge() != muData.getSelectedMuons()[0].charge() && tauData.getSelectedTaus()[0].isGenuineTau()) {
      hCheck->Fill(1);
    } else if (tauData.getSelectedTaus()[1].charge() != muData.getSelectedMuons()[0].charge() && tauData.getSelectedTaus()[1].isGenuineTau()) {
      hCheck->Fill(1);
    } else {
      hCheck->Fill(-1); //tau is SS with the muon and that tau is NOT genuine
    }
  }

//

  for(unsigned int i=0; i<2; i++){
    hTauPt->Fill(tauData.getSelectedTaus()[i].pt());
    hTauEta->Fill(tauData.getSelectedTaus()[i].eta());
    hTauCharge->Fill(tauData.getSelectedTaus()[i].charge());
  }

  hMuonPt->Fill(muData.getSelectedMuons()[0].pt());
  hMuonEta->Fill(muData.getSelectedMuons()[0].eta());

  hNTau->Fill(tauData.getSelectedTaus().size());

  hMET->Fill(METData.getMET().R());

//  hNJet->Fill(jetData.getNumberOfSelectedJets());

  double myTransverseMass = TransverseMass::reconstruct(tauData.getSelectedTaus()[0],tauData.getSelectedTaus()[1],muData.getSelectedMuons()[0], METData.getMET());
//  double myTransverseMass = TransverseMass::reconstruct(muData.getSelectedMuons()[0],muData.getSelectedMuons()[1],muData.getSelectedMuons()[2],muData.getSelectedMuons()[3],muData.getSelectedMuons()[4], METData.getMET());
  hTransverseMass->Fill(myTransverseMass);


  cSelected.increment();

  ////////////
  // Fill final plots
  ////////////



  fCommonPlots.fillControlPlotsAfterAllSelections(fEvent);

  ////////////
  // Finalize
  ////////////

  fEventSaver.save();


}
