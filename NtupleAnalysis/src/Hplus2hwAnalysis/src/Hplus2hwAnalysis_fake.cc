// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"
#include "EventSelection/interface/TransverseMass.h"


#include "TDirectory.h"

class Hplus2hwAnalysis_fake: public BaseSelector {
public:
  explicit Hplus2hwAnalysis_fake(const ParameterSet& config, const TH1* skimCounters);
  virtual ~Hplus2hwAnalysis_fake() {}

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

  MuonSelection fMuonSelection;

  TauSelection fTauSelection;
  TauSelection fLooseTauSelection;
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

  void doBaselineAnalysis(const Event& event, const TauSelection::Data& tauData, const int nVertices);
  void doSignalAnalysis(const Event& event, const TauSelection::Data& looseTauData, const int nVertices);

  // Non-common histograms



  WrappedTH1 *hTauPt_num_1pr;
  WrappedTH1 *hTauPt_den_1pr;

  WrappedTH1 *hTauEta_num_1pr;
  WrappedTH1 *hTauEta_den_1pr;

  WrappedTH1 *hTauPt_ratio_1pr;

  WrappedTH1 *hTauPt_num_2pr;
  WrappedTH1 *hTauPt_den_2pr;

  WrappedTH1 *hTauPt_num_3pr;
  WrappedTH1 *hTauPt_den_3pr;

  WrappedTH1 *hTauPt_num_g_1pr;
  WrappedTH1 *hTauPt_den_g_1pr;

  WrappedTH1 *hTauPt_num_g_2pr;
  WrappedTH1 *hTauPt_den_g_2pr;

  WrappedTH1 *hTauPt_num_g_3pr;
  WrappedTH1 *hTauPt_den_g_3pr;

  WrappedTH1 *hMuonPt;
  WrappedTH1 *hNJet;

  WrappedTH1 *hTauEta;
  WrappedTH1 *hMuonEta;
  WrappedTH1 *hMET;

  WrappedTH1 *hMuonPt_afterMuonSelection;
  WrappedTH1 *hMuonEta_afterMuonSelection;

  WrappedTH1 *hNTau;
  WrappedTH1 *hTauCharge;

  WrappedTH1 *hTransverseMass;
  // WrappedTH1 *hTransverseMass_ttRegion;
  // WrappedTH1 *hTransverseMass_WRegion;
  // WrappedTH1 *hTransverseMass_ttRegion_bbcuts;
  // WrappedTH1 *hTransverseMass_WRegion_bbcuts;

};


#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(Hplus2hwAnalysis_fake);


Hplus2hwAnalysis_fake::Hplus2hwAnalysis_fake(const ParameterSet& config, const TH1* skimCounters)
: BaseSelector(config, skimCounters),
  fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kHplus2hwAnalysis, fHistoWrapper),
  cAllEvents(fEventCounter.addCounter("All events")),
  fMuonSelection(config.getParameter<ParameterSet>("MuonSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  fTauSelection(config.getParameter<ParameterSet>("TauSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
  fLooseTauSelection(config.getParameter<ParameterSet>("LooseTauSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
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




void Hplus2hwAnalysis_fake::book(TDirectory *dir) {

  // Book common plots histograms
  fCommonPlots.book(dir, isData());

  // Book histograms in event selection classes
  fMETFilterSelection.bookHistograms(dir);


  fElectronSelection.bookHistograms(dir);
  fTauSelection.bookHistograms(dir);
  fLooseTauSelection.bookHistograms(dir);
  fMuonSelection.bookHistograms(dir);
  fJetSelection.bookHistograms(dir);
  fMETSelection.bookHistograms(dir);
  fBJetSelection.bookHistograms(dir);
  // Book non-common histograms
  // hAssociatedTop_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "associatedTop_Pt", "Associated t pT;p_{T} (G$
  // hAssociatedTop_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "associatedTop_Eta", "Associated t eta;#eta",$

  double bin[8] = {20,25,30,35,40,50,60,120};
  double bin_2[4] = {20,40,60,140};

  hTauPt_num_1pr =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt_num_1pr", "Tau pT num", 7, bin);
  hTauPt_den_1pr =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt_den_1pr", "Tau pT den", 7, bin);

  hTauEta_num_1pr =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauEta_num_1pr", "Tau eta num", 50, -2.5, 2.5);
  hTauEta_den_1pr =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauEta_den_1pr", "Tau eta den", 50, -2.5, 2.5);

  hTauPt_ratio_1pr =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt_ratio_1pr", "Tau pT raio", 15,10,150);

  hTauPt_num_2pr =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt_num_2pr", "Tau pT num", 7, bin);
  hTauPt_den_2pr =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt_den_2pr", "Tau pT den", 7, bin);

  hTauPt_num_3pr =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt_num_3pr", "Tau pT num", 7, bin);
  hTauPt_den_3pr =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt_den_3pr", "Tau pT den", 7, bin);

  hTauPt_num_g_1pr =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt_num_g_1pr", "Tau pT num", 7, bin);
  hTauPt_den_g_1pr =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt_den_g_1pr", "Tau pT den", 7, bin);

  hTauPt_num_g_2pr =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt_num_g_2pr", "Tau pT num", 7, bin);
  hTauPt_den_g_2pr =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt_den_g_2pr", "Tau pT den", 7, bin);

  hTauPt_num_g_3pr =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt_num_g_3pr", "Tau pT num", 7, bin);
  hTauPt_den_g_3pr =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt_den_g_3pr", "Tau pT den", 7, bin);

  hMuonPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "muPt", "Muon pT", 40, 0, 400);
  hMET =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MET", "MET", 40, 0, 400);

  hTauEta =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauEta", "Tau eta", 50, -2.5, 2.5);
  hMuonEta =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "muEta", "Muon eta", 50, -2.5, 2.5);

  hMuonEta_afterMuonSelection =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "muEta_afterMuonSelection", "Muon eta after muon selection", 50, -2.5, 2.5);
  hMuonPt_afterMuonSelection = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "muPt_afterMuonSelection", "Muon pT adter uon selection", 40, 0, 400);

  hNJet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "nJet", "# of jets", 10, 0, 10);
  hNTau =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "nTau", "# of Selected taus", 10, 0, 10);
  hTauCharge = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauCharge", "charge of taus", 6,-3, 3);

  hTransverseMass = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TransverseMass", "TransverseMass", 6, -3, 3);

  return;
}


void Hplus2hwAnalysis_fake::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
  return;
}



void Hplus2hwAnalysis_fake::process(Long64_t entry) {

  ////////////
  // Initialize
  ////////////

  fCommonPlots.initialize();
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

  if(muData.getSelectedMuons().size() != 1)
    return;

//  if(muData.getSelectedMuons()[0].charge() == muData.getSelectedMuons()[1].charge())
//    return;

  ////////////
  // Dummy Trigger SF for first check
  ////////////
//2016BF

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


//2016GH
/*
  if (fEvent.isMC()) {
    if (26 <= muData.getSelectedMuons()[1].pt() && muData.getSelectedMuons()[1].pt() < 30) fEventWeight.multiplyWeight(0.9752);
    if (30 <= muData.getSelectedMuons()[1].pt() && muData.getSelectedMuons()[1].pt() < 40) fEventWeight.multiplyWeight(0.9869);
    if (40 <= muData.getSelectedMuons()[1].pt() && muData.getSelectedMuons()[1].pt() < 50) fEventWeight.multiplyWeight(0.9919);
    if (50 <= muData.getSelectedMuons()[1].pt() && muData.getSelectedMuons()[1].pt() < 60) fEventWeight.multiplyWeight(0.9929);
    if (60 <= muData.getSelectedMuons()[1].pt() && muData.getSelectedMuons()[1].pt() < 80) fEventWeight.multiplyWeight(0.9924);
    if (80 <= muData.getSelectedMuons()[1].pt() && muData.getSelectedMuons()[1].pt() < 120) fEventWeight.multiplyWeight(0.9896);
    if (120 <= muData.getSelectedMuons()[1].pt() && muData.getSelectedMuons()[1].pt() < 200) fEventWeight.multiplyWeight(0.9870);
    if (200 <= muData.getSelectedMuons()[1].pt() && muData.getSelectedMuons()[1].pt() < 500) fEventWeight.multiplyWeight(0.9925);

  }
*/

  ////////////
  // Dummy muon ID SF for first check //tightID
  ////////////

  if (fEvent.isMC()) {
    if (20 <= muData.getSelectedMuons()[0].pt() && muData.getSelectedMuons()[0].pt() < 25) fEventWeight.multiplyWeight(0.991);
    if (25 <= muData.getSelectedMuons()[0].pt() && muData.getSelectedMuons()[0].pt() < 30) fEventWeight.multiplyWeight(0.982);
    if (30 <= muData.getSelectedMuons()[0].pt() && muData.getSelectedMuons()[0].pt() < 40) fEventWeight.multiplyWeight(0.981);
    if (40 <= muData.getSelectedMuons()[0].pt() && muData.getSelectedMuons()[0].pt() < 50) fEventWeight.multiplyWeight(0.981);
    if (50 <= muData.getSelectedMuons()[0].pt() && muData.getSelectedMuons()[0].pt() < 60) fEventWeight.multiplyWeight(0.978);
    if (60 <= muData.getSelectedMuons()[0].pt() && muData.getSelectedMuons()[0].pt() < 120) fEventWeight.multiplyWeight(0.986);
    if (120 <= muData.getSelectedMuons()[0].pt() && muData.getSelectedMuons()[0].pt() < 200) fEventWeight.multiplyWeight(1.024);

  }

/*
  if (fEvent.isMC()) {
    if (20 <= muData.getSelectedMuons()[1].pt() && muData.getSelectedMuons()[1].pt() < 25) fEventWeight.multiplyWeight(0.991);
    if (25 <= muData.getSelectedMuons()[1].pt() && muData.getSelectedMuons()[1].pt() < 30) fEventWeight.multiplyWeight(0.982);
    if (30 <= muData.getSelectedMuons()[1].pt() && muData.getSelectedMuons()[1].pt() < 40) fEventWeight.multiplyWeight(0.981);
    if (40 <= muData.getSelectedMuons()[1].pt() && muData.getSelectedMuons()[1].pt() < 50) fEventWeight.multiplyWeight(0.981);
    if (50 <= muData.getSelectedMuons()[1].pt() && muData.getSelectedMuons()[1].pt() < 60) fEventWeight.multiplyWeight(0.978);
    if (60 <= muData.getSelectedMuons()[1].pt() && muData.getSelectedMuons()[1].pt() < 120) fEventWeight.multiplyWeight(0.986);
    if (120 <= muData.getSelectedMuons()[1].pt() && muData.getSelectedMuons()[1].pt() < 200) fEventWeight.multiplyWeight(1.024);

  }

*/



  ////////////
  // Invariant mass near Z
  ////////////
/*
  double InvMass = (muData.getSelectedMuons()[0].p4() + muData.getSelectedMuons()[1].p4()).M();

  if (InvMass < 80)
    return;

  if (InvMass > 100)
    return;
*/
  ////////////
  // 6) Tau
  ////////////

  const TauSelection::Data tauData = fTauSelection.analyze(fEvent);

  const TauSelection::Data looseTauData = fLooseTauSelection.analyzeTight(fEvent);


  double drMuTau1 = 0;

  double drMuTau2 = 0;

  double drMuMu = 0;

//  fCommonPlots.fillControlPlotsAfterTauSelection(fEvent, tauData);

  if (!(looseTauData.hasIdentifiedTaus()))
    return;

  if(looseTauData.getSelectedTaus().size() != 2)
    return;

  if(looseTauData.getSelectedTaus()[0].charge() != looseTauData.getSelectedTaus()[1].charge())
    return;

  // make sure that the muons are not too close to muons
//  drMuMu = ROOT::Math::VectorUtil::DeltaR(muData.getSelectedMuons()[0].p4(),muData.getSelectedMuons()[1].p4());
//  if(drMuMu < 0.3)
//    return;

//  hTauPt_ratio_1pr->Fill(InvMass);

  std::vector<float> myFactorisationInfo;




  if (tauData.hasIdentifiedTaus()) {



      //====== Tau ID SF
    if (fEvent.isMC()) {
      fEventWeight.multiplyWeight(tauData.getTauIDSF());
    }

      // Apply fake tau SF
    if (fEvent.isMC()) {
      fEventWeight.multiplyWeight(tauData.getTauMisIDSF());
    }

//    if (tauData.getSelectedTaus().size() != 1) {
//      return;
//    }

    for(unsigned int i=0; i<tauData.getSelectedTaus().size(); i++){

        // make sure that the taus are not too close to muons
      drMuTau1 = ROOT::Math::VectorUtil::DeltaR(muData.getSelectedMuons()[0].p4(),tauData.getSelectedTaus()[i].p4());
      if(drMuTau1 < 0.5) {
        return;
      }

//      drMuTau2 = ROOT::Math::VectorUtil::DeltaR(muData.getSelectedMuons()[1].p4(),tauData.getSelectedTaus()[i].p4());
//      if(drMuTau2 < 0.5) {
//        return;
//      }
    }

      // Do rest of event selection
    doSignalAnalysis(fEvent, tauData, nVertices);

    hNTau->Fill(tauData.getSelectedTaus().size());

      // take tight weight away

      //====== Tau ID SF
    if (fEvent.isMC()) {
      fEventWeight.multiplyWeight(1.0/tauData.getTauIDSF());
    }

      // Apply fake tau SF
    if (fEvent.isMC()) {
      fEventWeight.multiplyWeight(1.0/tauData.getTauMisIDSF());
    }
  } // if has tight tau

  if (looseTauData.hasIdentifiedTaus()) {
      // Sanity check passed: at least one isolated tau exists
      // Set factorisation bin

      // loose id

      //====== Tau ID SF
    if (fEvent.isMC()) {
      fEventWeight.multiplyWeight(looseTauData.getTauIDSF());
    }

      // Apply fake tau SF
    if (fEvent.isMC()) {
      fEventWeight.multiplyWeight(looseTauData.getTauMisIDSF());
    }


    for(unsigned int i=0; i<looseTauData.getSelectedTaus().size(); i++){

        // make sure that the taus are not too close to muons
      drMuTau1 = ROOT::Math::VectorUtil::DeltaR(muData.getSelectedMuons()[0].p4(),looseTauData.getSelectedTaus()[i].p4());
      if(drMuTau1 < 0.5) {
        return;
      }

//      drMuTau2 = ROOT::Math::VectorUtil::DeltaR(muData.getSelectedMuons()[1].p4(),looseTauData.getSelectedTaus()[i].p4());
//      if(drMuTau2 < 0.5) {
//        return;
//      }
    }



    hMuonPt->Fill(muData.getSelectedMuons()[0].pt());
//    hMuonPt->Fill(muData.getSelectedMuons()[1].pt());

//    hNJet->Fill(jetData.getNumberOfSelectedJets());

//    hNTau->Fill(looseTauData.getSelectedTaus().size());

      // Do rest of event selection
    doBaselineAnalysis(fEvent, looseTauData, nVertices);
  } // has loose tau

  ////////////
  // 4) Electron veto (Fully hadronic + orthogonality)
  ////////////

  const ElectronSelection::Data eData = fElectronSelection.analyze(fEvent);
  if (eData.hasIdentifiedElectrons())
    return;

  fEventSaver.save();
}

void Hplus2hwAnalysis_fake::doBaselineAnalysis(const Event& event, const TauSelection::Data& tauData, const int nVertices) {


  for(unsigned int i=0; i<tauData.getSelectedTaus().size(); i++){

    if (event.isMC() && tauData.getSelectedTaus()[i].isGenuineTau()) {
      if (tauData.getSelectedTaus()[i].decayMode()==0) hTauPt_den_g_1pr->Fill(tauData.getSelectedTaus()[i].pt());
      if (tauData.getSelectedTaus()[i].decayMode()==1) hTauPt_den_g_2pr->Fill(tauData.getSelectedTaus()[i].pt());
      if (tauData.getSelectedTaus()[i].decayMode()==10) hTauPt_den_g_3pr->Fill(tauData.getSelectedTaus()[i].pt());
    }


    if (tauData.getSelectedTaus()[i].decayMode()==0) {
      hTauPt_den_1pr->Fill(tauData.getSelectedTaus()[i].pt());
      hTauEta_den_1pr->Fill(tauData.getSelectedTaus()[i].eta());
    }
    if (tauData.getSelectedTaus()[i].decayMode()==1) {
      hTauPt_den_2pr->Fill(tauData.getSelectedTaus()[i].pt());
    }
    if (tauData.getSelectedTaus()[i].decayMode()==10) {
      hTauPt_den_3pr->Fill(tauData.getSelectedTaus()[i].pt());
    }
  }
}

void Hplus2hwAnalysis_fake::doSignalAnalysis(const Event& event, const TauSelection::Data& tightTauData, const int nVertices) {


  for(unsigned int i=0; i<tightTauData.getSelectedTaus().size(); i++){

    if (event.isMC() && tightTauData.getSelectedTaus()[i].isGenuineTau()) {
      if (tightTauData.getSelectedTaus()[i].decayMode()==0) hTauPt_num_g_1pr->Fill(tightTauData.getSelectedTaus()[i].pt());
      if (tightTauData.getSelectedTaus()[i].decayMode()==1) hTauPt_num_g_2pr->Fill(tightTauData.getSelectedTaus()[i].pt());
      if (tightTauData.getSelectedTaus()[i].decayMode()==10) hTauPt_num_g_3pr->Fill(tightTauData.getSelectedTaus()[i].pt());
    }


    if (tightTauData.getSelectedTaus()[i].decayMode()==0) {
      hTauPt_num_1pr->Fill(tightTauData.getSelectedTaus()[i].pt());
      hTauEta_num_1pr->Fill(tightTauData.getSelectedTaus()[i].eta());
    }
    if (tightTauData.getSelectedTaus()[i].decayMode()==1) {
      hTauPt_num_2pr->Fill(tightTauData.getSelectedTaus()[i].pt());
    }
    if (tightTauData.getSelectedTaus()[i].decayMode()==10) {
      hTauPt_num_3pr->Fill(tightTauData.getSelectedTaus()[i].pt());
    }
  }
}
