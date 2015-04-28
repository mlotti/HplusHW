#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"
#include "DataFormat/interface/Event.h"
//#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TLorentzVector.h"
#include "Math/GenVector/VectorUtil.h"
#include "TVector3.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TDirectory.h"

class CorrelationAnalysis: public BaseSelector {
public:
  explicit CorrelationAnalysis(const ParameterSet& config);
  virtual ~CorrelationAnalysis() {}

  virtual void book(TDirectory *dir) override;
  virtual void setupBranches(BranchManager& branchManager) override;
  virtual void process(Long64_t entry) override;
  //  double DeltaPhi(const Tau& tau, const fEvent.met_Type1());
  //  double DeltaPhiTauMet(const Tau&  tau, const double met_et, const double met_phi); 
private:
  Event fEvent;

  const float fTauPtCut;
  //  const float fMetCut;

  Count cAllEvents;
  Count cWeighted;
  Count cTauSelection;
  Count cMuonVeto;
  Count cElectronVeto;
  Count cJetSelection;
  Count cBJetSelection;
  Count cMetCut;  
  Count cBackToBackCut;
  Count cCollinearCut;
  Count cSelectedJets;
  //  Count cSelectedBJets;
  Count cSelectedTrueBJets;
  Count cSelectedBtaggedJets;
  Count cSelectedTrueBtaggedJets;
  Count cSelectedNonBJets;
  Count cSelectedFakeBtaggedJets;
  Count cTauCandidates;
  Count cTauDecayMode;
  Count cTauPtCut;
  Count cTauEtaCut;
  Count cTauLeadingTrackCut;
  Count cTauAgainstElectronCut;
  Count cTauAgainstMuonCut;
  Count cTauDiscriminatorCut;
  Count cTauRtauCut;
  Count cTauNprongCut;
  Count cTauTrueTau;

  WrappedTH1 *hTauPt;
  WrappedTH1 *hTauEta;
  WrappedTH1 *hTauPhi;
  WrappedTH1 *hRtau;
  WrappedTH1 *hNselectedTaus; 
  WrappedTH1 *hMuonPt;
  WrappedTH1 *hMuonEta;
  WrappedTH1 *hNmuons;

  WrappedTH1 *hElectronPt;
  WrappedTH1 *hElectronEta;
  WrappedTH1 *hNelectrons;

  WrappedTH1 *hJetPt;
  WrappedTH1 *hJetEta;
  WrappedTH1 *hJetPhi;
  WrappedTH1 *hNjets;
  WrappedTH1 *hNBjets;
  WrappedTH1 *hNtrueBjets;
  WrappedTH1 *hgenJetPt;
  WrappedTH1 *hgenJetEta;
  WrappedTH1 *hgenJetPhi;
  WrappedTH1 *hBJetPt;
  WrappedTH1 *hBJetEta;
  WrappedTH1 *hrealBJetPt;
  WrappedTH1 *hrealBJetEta;
  WrappedTH1 *hrealMaxBJetPt;
  WrappedTH1 *hrealMaxBJetEta;  
  WrappedTH1 *hjetBProbabilityBJetTags;
  WrappedTH1 *hjetProbabilityBJetTags;
  WrappedTH1 *htrackCountingHighPurBJetTags;
  WrappedTH1 *htrackCountingHighEffBJetTags;
  WrappedTH1 *hMet;
  WrappedTH1 *hMetPhi;
  WrappedTH1 *hMetJetInHole;
  WrappedTH1 *hMetNoJetInHole;
  WrappedTH1 *hMetJetInHole02;
  WrappedTH1 *hMetNoJetInHole02;
  WrappedTH1 *hPt3Jets; 
  WrappedTH1 *h3jetPtcut; 
  WrappedTH2 *hDPhiTauMetVsPt3jets;
  WrappedTH2 *hDPhiTauMetVsDphiJet1Met;
  WrappedTH2 *hDPhiTauMetVsDphiJet2Met;
  WrappedTH2 *hDPhiTauMetVsDphiJet3Met;
  WrappedTH1 *hM3jets;
  WrappedTH1 *hDeltaPhiTauMet;
  WrappedTH1 *htransverseMass;
  WrappedTH1 *htransverseMassTriangleCut; 
  WrappedTH1 *htransverseMass3JetCut;
  WrappedTH1 *htransverseMass_bbAndColCut;
  WrappedTH1 *htransverseMass_bbCut;
  WrappedTH2 *hgenjetEtaVsDeltaPt; 
  WrappedTH2 *hgenjetPhiVsDeltaPt; 
  WrappedTH2 *hgenjetPtVsDeltaPt; 
  WrappedTH1 *hDeltaRJetGenJet; 
  WrappedTH1 *hDeltaPt;
  WrappedTH2 *hJetEtSumVsJetTauMetEtSum;
  WrappedTH1 *hJetTauMetEtSum;
  WrappedTH1 *hDrTau3Jets;
  WrappedTH1 *hJetTauEtSum;
  WrappedTH1 *hJetEtSum;
  WrappedTH1 *hDPhi3JetsMet;
  WrappedTH1 *hRadiusbb;
  WrappedTH1 *hRadiusCol;
  WrappedTH1 *hconstantEtSum; 
  WrappedTH1 *hslopeEtSum; 

  std::vector<double> fECALDeadCellEtaTable;
  std::vector<double> fECALDeadCellPhiTable;


};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(CorrelationAnalysis);

CorrelationAnalysis::CorrelationAnalysis(const ParameterSet& config):
  BaseSelector(config),
  fEvent(config),
  fTauPtCut(config.getParameter<float>("tauPtCut")),
  //  fMetCut(config.getParameter<float>("metCut")),
  cAllEvents(fEventCounter.addCounter("All events")),
  cWeighted(fEventCounter.addCounter("Weighted")),
  cTauSelection(fEventCounter.addCounter("Tau selection")),
  cMuonVeto(fEventCounter.addCounter("Muon veto")),
  cElectronVeto(fEventCounter.addCounter("Electron veto")),
  cJetSelection(fEventCounter.addCounter("Jet selection")),
  cBJetSelection(fEventCounter.addCounter("B-jet selection")),
  cMetCut(fEventCounter.addCounter("Met cut")),
  cBackToBackCut(fEventCounter.addCounter("BackToBack cut")),
  cCollinearCut(fEventCounter.addCounter("Collinear cut")),
  cSelectedJets(fEventCounter.addSubCounter("B-jet selection","Selected jets")),
  cSelectedBtaggedJets(fEventCounter.addSubCounter("B-jet selection","Selected b-jets")),
  cSelectedTrueBJets(fEventCounter.addSubCounter("B-jet selection","True b-jets")),
  cSelectedTrueBtaggedJets(fEventCounter.addSubCounter("B-jet selection","b-tagged true b-jets")),
  cSelectedNonBJets(fEventCounter.addSubCounter("B-jet selection","Non b-jets")),
  cSelectedFakeBtaggedJets(fEventCounter.addSubCounter("B-jet selection","b-tagged non b-jets")),
  cTauCandidates(fEventCounter.addSubCounter("Tau-jet selection","tau candidates")),
  cTauDecayMode(fEventCounter.addSubCounter("Tau-jet selection","tau decay mode")),
  cTauPtCut(fEventCounter.addSubCounter("Tau-jet selection","tau pt cut")),
  cTauEtaCut(fEventCounter.addSubCounter("Tau-jet selection","tau eta cut")),
  cTauLeadingTrackCut(fEventCounter.addSubCounter("Tau-jet selection","tau leading track cut")),
  cTauAgainstElectronCut(fEventCounter.addSubCounter("Tau-jet selection","against electron cut")),
  cTauAgainstMuonCut(fEventCounter.addSubCounter("Tau-jet selection","against muon cut")),
  cTauDiscriminatorCut(fEventCounter.addSubCounter("Tau-jet selection","tau discriminator cut")),
  cTauRtauCut(fEventCounter.addSubCounter("Tau-jet selection","tau Rtau cut")),
  cTauNprongCut(fEventCounter.addSubCounter("Tau-jet selection","tau Nprong cut")),
  cTauTrueTau(fEventCounter.addSubCounter("Tau-jet selection","true tau selected"))
{ } 



void CorrelationAnalysis::book(TDirectory *dir) {

  hTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt", "Tau pT", 200, 0, 1000);
  hTauEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauEta", "Tau eta", 50, -2.5, 2.5);
  hTauPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPhi", "Tau phi", 100, -180, 180);
  hRtau =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Rtau", "Tau Rtau", 200, 0, 1);
  hNselectedTaus=  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "NselectedTaus", "N taus", 10, 0, 10);

  hMuonPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "muonPt", "Muon pT", 100, 0, 500);
  hMuonEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "muonEta", "Muon eta", 60, -3, 3);
  hNmuons = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Nmuons", "Nmuons", 20, 0, 20);

  hElectronPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "electronPt", "Electron pT", 100, 0, 500);
  hElectronEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "electronEta", "Electron pT", 100, -3, 3);
  hNelectrons = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Nelectrons", "Nelectrons", 20, 0, 20);

  hJetPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "jetPt", "Jet pT", 200, 0, 1000);
  hJetEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "jetEta", "Jet eta", 100, -5, 5);
  hJetPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "jetPhi", "Jet phi", 90, -180, 180);
  hNjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Njets", "Njets", 50, 0, 50);
  hgenJetPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genjetPt", "genJet pT", 200, 0, 1000);
  hgenJetEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genjetEta", "genJet eta", 100, -5, 5);
  hgenJetPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genjetPhi", "genJet phi", 90, -180, 180);
  hBJetPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "bJetPt", "B jet pT", 200, 0, 1000);
  hBJetEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "bjetEta", "b-jet eta", 100, -2.5, 2.5);
  hNBjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "NBjets", "NBjets", 20, 0, 20);
  hjetBProbabilityBJetTags = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "jetBProbabilityBJetTags", "jetBProbabilityBJetTags", 200, 0, 10);
  hjetProbabilityBJetTags = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "jetProbabilityBJetTags", "jetProbabilityBJetTags", 200, 0, 10);
  htrackCountingHighEffBJetTags = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "trackCountingHighEffBJetTags", "trackCountingHighEffBJetTags", 200, 0, 50);
  htrackCountingHighPurBJetTags = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "trackCountingHighPurBJetTags", "trackCountingHighPurBJetTags", 200, 0, 50);
  hMet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Met", "Met", 200, 0., 1000.);
  hMetPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetPhi", "Met phi", 90, -180., 180.);
  hMetJetInHole= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetJetInHole", "MetJetInHole", 200, 0., 1000.);
  hMetNoJetInHole= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetNoJetInHole", "MetNoJetInHole", 200, 0., 1000.);
  hMetJetInHole02= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetJetInHole02", "MetJetInHoleDR02", 200, 0., 1000.);
  hMetNoJetInHole02= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetNoJetInHole02", "MetNoJetInHoleDR02", 200, 0., 1000.);
  hPt3Jets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Pt3Jets", "Pt3Jets", 200, 0., 1000.);
  h3jetPtcut = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "TheeJetPtcut", "TheeJetPtcut", 200, 0., 400.);
  hM3jets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "M3Jets", "M3Jets", 200, 0., 600.);
  hDeltaPhiTauMet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "DeltaPhiTauMet", "DeltaPhiTauMet", 90, 0., 180);
  hDPhiTauMetVsPt3jets = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "DPhiTauMetVsPt3jets", "Pt3jets;#Delta#phi(#tau jet,MET) (^{o});p_{T}^{3 jets}(GeV)", 180, 0., 180, 100, 0., 400.);
  hDrTau3Jets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "DrTau3Jets", "DrTau3Jets", 100, 0.,5);
  hJetEtSum =fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "JetEtSum", "JetEtSum", 200, 0, 1000);
  hJetTauEtSum = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "JetTauEtSum", "JetTauEtSum", 200, 0, 1000);
  hJetTauMetEtSum = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "JetTauMetEtSum", "JetTauMetEtSum", 200, 0, 1000);
  hDPhi3JetsMet= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "DPhi3JetsMet", "DPhi3JetsMet", 90, 0., 180);
  hJetEtSumVsJetTauMetEtSum = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "JetEtSumVsJetTauMetEtSum", "JetEtSumVsJetTauMetEtSum", 100, 0., 1000, 100, 0., 1000.);
  hDPhiTauMetVsDphiJet1Met = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "DPhiTauMetVsDphiJet1Met", "DPhiTauMetVsDphiJet1Met", 90, 0., 180, 90, 0., 180.);
  hDPhiTauMetVsDphiJet2Met = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "DPhiTauMetVsDphiJet2Met", ";#Delta#phi(#tau jet2)", 90, 0., 180, 90, 0., 180.);
  hDPhiTauMetVsDphiJet3Met = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "DPhiTauMetVsDphiJet3Met", ";#Delta#phi(#tau jet3)", 90, 0., 180, 90, 0., 180.);
  htransverseMass = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMass", "transverseMass", 200, 0., 800);
  htransverseMassTriangleCut = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMassTriangleCut", "transverseMassTriangleCut", 200, 0., 800);  
  htransverseMass3JetCut = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMass3JetCut", "transverseMass3JetCut", 200, 0., 800); 
  htransverseMass_bbCut = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMass_bbCut", "transverseMass_bbCut", 200, 0., 800);
  htransverseMass_bbAndColCut = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMass_bbAndColCut", "transverseMass_bbAndColCut", 200, 0., 800);
  hRadiusbb = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Radiusbb", "Radiusbb", 90, 0., 180);
  hRadiusCol = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "RadiusCol", "RadiusCol", 90, 0., 180);
  hconstantEtSum = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "constantEtSum", "constantEtSum", 100, 0., 400);
  hslopeEtSum = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "slopeEtSum", "slopeEtSum", 100, 0., 2);

  hNtrueBjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "NtrueBjets", "NtrueBjets", 20, 0, 20);
  hgenJetPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genjetPt", "genJet pT", 200, 0, 1000);
  hgenJetEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genjetEta", "genJet eta", 100, -5, 5);
  hgenJetPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genjetPhi", "genJet phi", 90, 0, 180);
  hrealBJetPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "realBJetPt", "trueBJet pT", 200, 0, 1000);
  hrealBJetEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "realBJetEta", "trueBJet eta", 100, -2.5, 2.5);
  hrealMaxBJetPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "realMaxBJetPt", "trueMaxBJet pT", 200, 0, 1000);
  hrealMaxBJetEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "realMaxBJetEta", "trueMaxBJet eta", 100, -5, 5);
  hgenjetEtaVsDeltaPt = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "genjetEtaVsDeltaPt", "genjetEtaVsDeltaPt", 250, -2.5, 2.5,100,-1.5,1.5);
  hgenjetPhiVsDeltaPt = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "genjetPhiVsDeltaPt", "genjetPhiVsDeltaPt", 90, 0., 180,100,-1.5,1.5);
  hgenjetPtVsDeltaPt = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "genjetPtVsDeltaPt", "genjetPtVsDeltaPt", 200, 0., 1000,100,-1.5,1.5);
  hDeltaRJetGenJet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "deltaRJetGenJet", "deltaRJetGenJet", 100, 0.,5);  
  hDeltaPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "DeltaPt", "DeltaPt", 100, -1.5, 1.5);


}

void CorrelationAnalysis::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}



void CorrelationAnalysis::process(Long64_t entry) {
  cAllEvents.increment();

  fEventWeight.multiplyWeight(0.5);
  cWeighted.increment();


  std::vector<Tau> selectedTaus;
  for(Tau tau: fEvent.taus()) {
    cTauCandidates.increment();

    if(!tau.decayModeFinding())
      continue;
    cTauDecayMode.increment();

    hTauPt->Fill(tau.pt());
    hTauEta->Fill(tau.eta());
    hTauPhi->Fill(tau.phi()* 180/3.14159265);

    if(!(tau.pt() > fTauPtCut))
      continue;
     cTauPtCut.increment();

    if(!(std::abs(tau.eta()) < 2.4))
      continue;
    cTauEtaCut.increment();

    if(!(tau.lTrkPt() > 10))
      continue;
    cTauLeadingTrackCut.increment();

    if(!tau.againstElectronTightMVA5())
      continue;
    cTauAgainstElectronCut.increment();

    if(!tau.againstMuonTightMVA())
      continue;
    cTauAgainstMuonCut.increment();


    if(!tau.byMediumCombinedIsolationDeltaBetaCorr3Hits())
      //    if(!tau.byMediumIsolationMVA3newDMwoLT())
      continue;
    cTauDiscriminatorCut.increment();

    //    double pTau = tau.pt() * std::cosh(tau.eta());
    //    double pLeadingTrack = tau.lTrkPt() * std::cosh(tau.lTrkEta());    
    double rTau = -999;
    //  if (pTau > 0 ) rTau = pLeadingTrack/ pTau; 
    if (tau.pt() > 0 ) rTau = tau.lTrkPt()/ tau.pt();   
    hRtau->Fill(rTau);
    if(!(rTau > 0.7))
      continue;
    cTauRtauCut.increment();

    if(!(tau.nProngs() == 1))
      continue;
    cTauNprongCut.increment();
  

    if (std::abs(tau.pdgId()) == 15) {
      cTauTrueTau.increment();
    }

     //   std::cout  << "  (tau.phi() "<< tau.phi() << std::endl; 
    selectedTaus.push_back(tau);
  }

  hNselectedTaus->Fill(selectedTaus.size());

  if(selectedTaus.empty())
      return;
  cTauSelection.increment();


  size_t nmuons = 0;
  for(Muon muon: fEvent.muons()) {
    hMuonPt->Fill(muon.pt());
    if(muon.pt() > 15) hMuonEta->Fill(muon.eta());
    if(muon.pt() > 15 && std::abs(muon.eta()) < 2.1)
      ++nmuons;
  }

  hNmuons->Fill(nmuons);
  if(nmuons > 0)
     return;
  cMuonVeto.increment();



  size_t nelectrons = 0;
  for(Electron electron: fEvent.electrons()) {
    hElectronPt->Fill(electron.pt());
    if (electron.pt() > 15) hElectronEta->Fill(electron.eta());
 
   if(electron.pt() > 15 && std::abs(electron.eta()) < 2.4)
      ++nelectrons;
  }
  //  std::cout  << " electrons  "<< nelectrons << std::endl; 
  hNelectrons->Fill(nelectrons);
 

 if(nelectrons > 0)
    return;
  cElectronVeto.increment();


  
  double myMet = fEvent.met_Type1().et();
  hMet->Fill(myMet); 
  hMetPhi->Fill(fEvent.met_Type1().phi()* 180/3.14159265);
 
  //  double myGenMet = fEvent.GenMET.et();

  // if(myMet <  fMetCut)
  //    return;
  //  cMetCut.increment();




  std::vector<Jet> selectedJets;
  for(Jet jet: fEvent.jets()) {
    hJetPt->Fill(jet.pt());
    if(jet.pt() > 30) hJetEta->Fill(jet.eta());
    hJetPhi->Fill(jet.phi()* 180/3.14159265);
    //    double jetID = jet.pdgId();

    if(jet.pt() > 30 && std::abs(jet.eta()) < 2.4) {
     
      bool skipJet = false;
      for(std::vector<Tau>::iterator i = selectedTaus.begin(); i!=
	    selectedTaus.end(); ++i){
	double deltaR = ROOT::Math::VectorUtil::DeltaR(jet.p4(),i->p4());
	double deltaPhi = ROOT::Math::VectorUtil::DeltaPhi(jet.p4(),i->p4());
	if(deltaR < 0.5) skipJet = true;
      }
      
      if (!skipJet) selectedJets.push_back(jet);
      
      for(GenJet genjet: fEvent.genjets()) {
	double myDeltaEta = jet.eta() - genjet.eta();
	double myDeltaPhi = (jet.phi() - genjet.phi())* 180/3.14159265;
	double myDeltaR = std::sqrt(myDeltaEta*myDeltaEta + myDeltaPhi*myDeltaPhi);
	hDeltaRJetGenJet->Fill(myDeltaR);
	//  hDeltaPt->Fill(deltaPt);
	if ( myDeltaR < 0.4) {
	  double deltaPt = (genjet.pt() - jet.pt())/genjet.pt();
	  hDeltaPt->Fill(deltaPt);
	  hgenjetEtaVsDeltaPt->Fill(genjet.eta(),deltaPt);
	  hgenjetPhiVsDeltaPt->Fill(genjet.phi()* 180/3.14159265,deltaPt);
	  hgenjetPtVsDeltaPt->Fill(genjet.pt(),deltaPt);
	  
	}
	
      }      
    }
  }

  std::vector<GenJet> genJets;
  //  GenJet genBjetMax;
  //  GenJet genBjetMin;
  //  double ptmax = 0;
  for(GenJet genjet: fEvent.genjets()) {
    hgenJetPt->Fill(genjet.pt());
    hgenJetEta->Fill(genjet.eta());
    hgenJetPhi->Fill(genjet.phi()* 180/3.14159265);
    /*
    if (genjet.pdgId() == 5) {
      hgenBJetPt->Fill(genjet.pt());
      hgenBJetEta->Fill(genjet.eta());
      if (genjet.pt() > ptmax) {
	ptmax = genjet.pt();
	genBjetMax= genjet;
      }
    }
    */
    if(genjet.pt() > 30 && std::abs(genjet.eta()) < 2.4) {
      genJets.push_back(genjet);
    }

  }

  //  hgenMaxBJetPt->Fill(genBjetMax.pt());
  //  hgenMaxBJetEta->Fill(genBjetMax.eta()); 


  if(selectedJets.size() < 3)
    return;
  cJetSelection.increment();


  //  for(PFCand pfcand: fEvent.PFCands()) {
  //  }



 // Calculate transverse mass 
  Tau tau = selectedTaus[0];
  math::XYZTLorentzVector myTau;
  myTau = tau.p4(); 
  double myCosPhi = 999;

  if (myMet > 0 && tau.pt() > 0)
    myCosPhi = (myTau.X() * std::cos(fEvent.met_Type1().phi()) + myTau.Y() * std::sin(fEvent.met_Type1().phi())) / tau.pt();
  double myDeltaPhi=-999;
  if ( myCosPhi < 1) myDeltaPhi =   std::acos(myCosPhi)* 180/3.14159265;

  double transverseMass = -999;
  double myTransverseMassSquared = 0;
  if (std::abs(myCosPhi) < 1)
    myTransverseMassSquared = 2 * tau.pt() * myMet * (1.0-myCosPhi);
  if (myTransverseMassSquared >= 0)
    transverseMass = TMath::Sqrt(myTransverseMassSquared);
  //  htransverseMass->Fill(transverseMass);

 


  size_t njets = 0;
    for(Jet& jet: selectedJets) {
      //      if (njets == 0)  jet1 = jet.p4();
      ++njets;
    }
  hNjets->Fill(njets);


  // B tagging
  std::vector<Jet> selectedBtaggedJets;

  size_t nbjets = 0;  
  for(Jet& jet: selectedJets) {
    cSelectedJets.increment();
    if (std::abs(jet.pdgId()) == 5) {
      cSelectedTrueBJets.increment();
    }
    if (std::abs(jet.pdgId()) != 5) {
      cSelectedNonBJets.increment();
    }
    hjetProbabilityBJetTags->Fill(jet.jetProbabilityBJetTags());
    hjetBProbabilityBJetTags->Fill(jet.jetBProbabilityBJetTags());
    htrackCountingHighEffBJetTags->Fill(jet.trackCountingHighEffBJetTags());
    htrackCountingHighPurBJetTags->Fill(jet.trackCountingHighPurBJetTags());
    //    std::cout << "  combinedInclusiveSecondaryVertexV2BjetTags() " <<  jet.combinedInclusiveSecondaryVertexV2BjetTags() << "  simpleSecondaryVertexHighEffBjetTags() " <<  jet.simpleSecondaryVertexHighEffBjetTags() << "  pileupJetIdfullDiscriminant()  " <<  jet.pileupJetIdfullDiscriminant() << std::endl;   
    //  if(jet.jetProbabilityBJetTags() > 0.898)
    if(jet.jetProbabilityBJetTags() > 0.9){   
    //    if(jet.trackCountingHighEffBJetTags() > 0.9){
    //    if(jet.trackCountingHighPurBJetTags() > 0.3){
      cSelectedBtaggedJets.increment();
      hBJetPt->Fill(jet.pt());
      hBJetEta->Fill(jet.eta());
      selectedBtaggedJets.push_back(jet);      
      ++nbjets;
      if (std::abs(jet.pdgId()) == 5) {
	cSelectedTrueBtaggedJets.increment();
      }
      if (std::abs(jet.pdgId()) != 5) {
	cSelectedFakeBtaggedJets.increment();
      }
    }
  }
  hNBjets->Fill(nbjets);


  if(selectedBtaggedJets.size() < 1)
    return;
  cBJetSelection.increment();


  
  
  Jet* trueBjetMax = 0;
  Jet* trueBjetMin = 0;

  double ptmax = 0;
  size_t ntrueBjets = 0;
  for(Jet& jet: selectedBtaggedJets) {
    if (std::abs(jet.pdgId()) == 5) {
      //      cSelectedTrueBJets.increment();
      hrealBJetPt->Fill(jet.pt());
      hrealBJetEta->Fill(jet.eta());
      if (jet.pt() > ptmax) {
	ptmax = jet.pt();
	trueBjetMax= &jet;
	++ntrueBjets;
      }
    }
  }
  //  std::cout << "  selectedBJets  "<<   selectedBJets.size()   << "  ptmax  "<<  ptmax   << std::endl;
  hNtrueBjets->Fill(ntrueBjets);
  if ( trueBjetMax != 0) {
    hrealMaxBJetPt->Fill(trueBjetMax->pt());
    hrealMaxBJetEta->Fill(trueBjetMax->eta()); 
  }

  //  MET cut
  //if(myMet <  fMetCut)
  if(myMet <  60)
    return;
  cMetCut.increment();

  htransverseMass->Fill(transverseMass);



  // Tail suppression

  Jet jet1 = selectedJets[0];
  Jet jet2 = selectedJets[1];
  Jet jet3 = selectedJets[2];

  double DeltaPhiTauMET  =  std::abs(ROOT::Math::VectorUtil::DeltaPhi(tau,fEvent.met_Type1())) * 180/3.14159265; 
  double DeltaPhiJet1MET  =  std::abs(ROOT::Math::VectorUtil::DeltaPhi(jet1,fEvent.met_Type1())) * 180/3.14159265; 
  double DeltaPhiJet2MET  = std::abs(ROOT::Math::VectorUtil::DeltaPhi(jet2,fEvent.met_Type1())) * 180/3.14159265;
  double DeltaPhiJet3MET  = std::abs(ROOT::Math::VectorUtil::DeltaPhi(jet3,fEvent.met_Type1())) * 180/3.14159265;
  double DeltaPhiTaujet1  =  std::abs(ROOT::Math::VectorUtil::DeltaPhi(tau,jet1)) * 180/3.14159265;
  
  hDPhiTauMetVsDphiJet1Met->Fill( DeltaPhiTauMET,DeltaPhiJet1MET);
  hDPhiTauMetVsDphiJet2Met->Fill( DeltaPhiTauMET, DeltaPhiJet2MET);
  hDPhiTauMetVsDphiJet3Met->Fill( DeltaPhiTauMET, DeltaPhiJet3MET);
  hDeltaPhiTauMet->Fill((DeltaPhiTauMET));


  // QCD tail killer cuts
  // back-to-back and collinear cuts with jet1
  double radius_bb = 60; 
  double radius_col = 30;  
  double bb_cut = std::sqrt(radius_bb*radius_bb - (180 - DeltaPhiTauMET)*(180 - DeltaPhiTauMET)); 
  double col_cut = std::sqrt(radius_col*radius_col - (180 - DeltaPhiJet1MET)* (180 - DeltaPhiJet1MET));
  double Rbb = std::sqrt(DeltaPhiJet1MET*DeltaPhiJet1MET + (180 - DeltaPhiTauMET)*(180 - DeltaPhiTauMET)); 
  double Rcol = std::sqrt(DeltaPhiTauMET*DeltaPhiTauMET - (180 - DeltaPhiJet1MET)* (180 - DeltaPhiJet1MET));
  hRadiusbb->Fill(Rbb);
  hRadiusCol->Fill(Rcol);

  if (DeltaPhiJet1MET < bb_cut) return;
  cBackToBackCut.increment();   
  htransverseMass_bbCut->Fill(transverseMass);

  if (DeltaPhiTauMET  < col_cut) return;
  cCollinearCut.increment();   
  htransverseMass_bbAndColCut->Fill(transverseMass);

 

 // Correlation cuts
  math::XYZTLorentzVector threeJets;
  threeJets = jet1.p4() + jet2.p4() + jet3.p4();

  hPt3Jets->Fill(threeJets.pt());
  // hMJets->Fill(threeJets.M());
  //  std::cout << "   threeJets.M()"<<   threeJets.M()   << std::endl;

  hDPhiTauMetVsPt3jets->Fill(std::abs(DeltaPhiTauMET),threeJets.pt());
 
  double ptcut = 400.0 * (1.0 - DeltaPhiTauMET/180.0);
  double ptConstant =  threeJets.pt() /(1.0 - DeltaPhiTauMET/180.0);
  h3jetPtcut->Fill(ptConstant);

  double drTau3Jets = ROOT::Math::VectorUtil::DeltaR(tau.p4(),threeJets);
  hDrTau3Jets->Fill(drTau3Jets); 


 // mt with 3jet and  triangle cut
  if (threeJets.pt()  > ptcut )    htransverseMass3JetCut->Fill(transverseMass);

  if (!(threeJets.pt()  < ptcut && DeltaPhiTauMET  > 60)) { 
    htransverseMassTriangleCut->Fill(transverseMass);
  }

 
  double DeltaPhi3jetsMet = std::abs(ROOT::Math::VectorUtil::DeltaPhi(threeJets, fEvent.met_Type1())) * 57.3;
  hDPhi3JetsMet->Fill(DeltaPhi3jetsMet);   
  double JetEtSum = jet1.pt() + jet2.pt() + jet3.pt();
  double JetTauEtSum = jet1.pt() + jet2.pt() + jet3.pt()+ tau.pt();
  double JetTauMetEtSum = jet1.pt() + jet2.pt() + jet3.pt()+ tau.pt() + myMet;
  double TauMetEtSum = tau.pt() + myMet;
  // assume known slope
  double constantEtSum = JetTauMetEtSum - 1.4 *  JetEtSum;
  // assume known constant term
  double slopeEtSum = (JetTauMetEtSum - 100)/JetEtSum;
  hconstantEtSum->Fill(constantEtSum);
  hslopeEtSum->Fill(slopeEtSum);

  
  hJetEtSum->Fill(JetEtSum);
  hJetTauEtSum->Fill(JetTauEtSum);
  hJetTauMetEtSum->Fill(JetTauMetEtSum);
  hJetEtSumVsJetTauMetEtSum->Fill(JetEtSum,JetTauMetEtSum);
 



  fEventSaver.save();
}


/*
  double DeltaPhi(const Tau& tau, const Jet& jet) {
    // Construct tau vector, mtau = 1.777 GeV/c2
    //   TLorentzVector myTau;
    math::XYZTLorentzVector myTau;
    myTau = tau.p4();
    math::XYZTLorentzVector myJet;
    myJet = tau.p4();
    //    myTau.SetXYZM(tau.px(), tau.py(), tau.pz(), 1.777); 
    // Calculate cosine of angle between jet and met direction
          //    double myEtMiss = TMath::Sqrt(met.px()*met.px() + met.py()*met.py());
    double myJetPt = jet.pt();
    double myCosPhi = 100;
    if (myJetPt > 0 && myTau.Pt() > 0)
      myCosPhi = (myTau.X()*myJet.X() + myTau.Y()*myJet.Y()) / (myTau.Pt()*myJetPt);
    double myDeltaPhi = -999;
    if ( myCosPhi < 1) myDeltaPhi =   acos(myCosPhi);
    return myDeltaPhi; 
  }


  double DeltaPhiTauMet(const Tau&  tau, const double met_et, const double met_phi) {
    // Construct tau vector, mtau = 1.777 GeV/c2
    math::XYZTLorentzVector myTau;
    myTau = tau.p4();

    // Calculate cosine of angle between jet and met direction
	  //    double myEtMiss = TMath::Sqrt(met.px()*met.px() + met.py()*met.py());
    double met_px = met_et*cos(met_phi);
    double met_py = met_et*sin(met_phi);
    double myCosPhi = 100;
    if (met_et > 0 && myTau.Pt() > 0)
      myCosPhi = (myTau.X()*met_px + myTau.Y()*met_py) / (myTau.Pt()*met_et);
    double myDeltaPhi = -999;
    if ( myCosPhi < 1) myDeltaPhi =   acos(myCosPhi);
    return myDeltaPhi; 
  }

*/
