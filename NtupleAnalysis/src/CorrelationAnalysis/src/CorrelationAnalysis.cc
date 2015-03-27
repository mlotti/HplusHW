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

  Count cAllEvents;
  Count cWeighted;
  Count cTauSelection;
  Count cMuonVeto;
  Count cElectronVeto;
  Count cJetSelection;
  

  WrappedTH1 *hTauPt;
  WrappedTH1 *hTauEta;
  WrappedTH1 *hTauPhi;
  WrappedTH1 *hRtau;
 
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

  WrappedTH1 *hBJetPt;
  WrappedTH1 *hjetSecondaryVertex;
 
  WrappedTH1 *hMet;
  WrappedTH1 *hMetPhi;
  WrappedTH1 *hMetJetInHole;
  WrappedTH1 *hMetNoJetInHole;
  WrappedTH1 *hMetJetInHole02;
  WrappedTH1 *hMetNoJetInHole02;
  WrappedTH1 *hPt3Jets; 
  WrappedTH2 *hDPhiTauMetVsPt3jets;
  WrappedTH2 *hDPhiTauMetVsDphiJet1Met;
  WrappedTH2 *hDPhiTauMetVsDphiJet2Met;
  WrappedTH2 *hDPhiTauMetVsDphiJet3Met;
  WrappedTH1 *hM3jets;
  WrappedTH1 *hDeltaPhiTauMet;
  WrappedTH1 *htransverseMass;
  WrappedTH1 *htransverseMassTriangleCut; 
 
  std::vector<double> fECALDeadCellEtaTable;
  std::vector<double> fECALDeadCellPhiTable;


};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(CorrelationAnalysis);

CorrelationAnalysis::CorrelationAnalysis(const ParameterSet& config):
  BaseSelector(config),
  fEvent(config),
  fTauPtCut(config.getParameter<float>("tauPtCut")),
  cAllEvents(fEventCounter.addCounter("All events")),
  cWeighted(fEventCounter.addCounter("Weighted")),
  cTauSelection(fEventCounter.addCounter("Tau selection")),
  cMuonVeto(fEventCounter.addCounter("Muon veto")),
  cElectronVeto(fEventCounter.addCounter("Electron veto")),
  cJetSelection(fEventCounter.addCounter("Jet selection"))
{ }

void CorrelationAnalysis::book(TDirectory *dir) {

  hTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt", "Tau pT", 200, 0, 1000);
  hTauEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauEta", "Tau eta", 50, -2.5, 2.5);
  hTauPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPhi", "Tau phi", 100, -3.1416, 3.1416);
  hRtau =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Rtau", "Tau Rtau", 200, 0, 1);


  hMuonPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "muonPt", "Muon pT", 100, 0, 500);
  hMuonEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "muonEta", "Muon eta", 60, -3, 3);
  hNmuons = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Nmuons", "Nmuons", 20, 0, 20);

  hElectronPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "electronPt", "Electron pT", 100, 0, 500);
  hElectronEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "electronEta", "Electron pT", 100, -3, 3);
  hNelectrons = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Nelectrons", "Nelectrons", 20, 0, 20);

  hJetPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "jetPt", "Jet pT", 200, 0, 1000);
  hJetEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "jetEta", "Jet eta", 100, -5, 5);
  hJetPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "jetPhi", "Jet phi", 90, 0, 180);
  hNjets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Njets", "Njets", 50, 0, 50);

  hBJetPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "bJetPt", "B jet pT", 200, 0, 1000);
  hjetSecondaryVertex = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "jetSecondaryVertex", "jetSecondaryVertex", 200, 0, 2);

  hMet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Met", "Met", 200, 0., 1000.);
  hMetPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetPhi", "Met phi", 90, 0., 180.);
  hMetJetInHole= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetJetInHole", "MetJetInHole", 200, 0., 1000.);
  hMetNoJetInHole= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetNoJetInHole", "MetNoJetInHole", 200, 0., 1000.);
  hMetJetInHole02= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetJetInHole02", "MetJetInHoleDR02", 200, 0., 1000.);
  hMetNoJetInHole02= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetNoJetInHole02", "MetNoJetInHoleDR02", 200, 0., 1000.);
  hPt3Jets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Pt3Jets", "Pt3Jets", 200, 0., 400.);
  hM3jets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "M3Jets", "M3Jets", 200, 0., 600.);
  hDeltaPhiTauMet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "DeltaPhiTauMet", "DeltaPhiTauMet", 90, -180., 180);
  hDPhiTauMetVsPt3jets = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "DPhiTauMetVsPt3jets", "Pt3jets;#Delta#phi(#tau jet,MET) (^{o});p_{T}^{3 jets}(GeV)", 180, 0., 180, 100, 0., 400.);
  hDPhiTauMetVsDphiJet1Met = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "DPhiTauMetVsDphiJet1Met", "DPhiTauMetVsDphiJet1Met", 90, 0., 180, 90, 0., 180.);
  hDPhiTauMetVsDphiJet2Met = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "DPhiTauMetVsDphiJet2Met", ";#Delta#phi(#tau jet2)", 90, 0., 180, 90, 0., 180.);
  hDPhiTauMetVsDphiJet3Met = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "DPhiTauMetVsDphiJet3Met", ";#Delta#phi(#tau jet3)", 90, 0., 180, 90, 0., 180.);
  htransverseMass = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMass", "transverseMass", 200, 0., 800);
  htransverseMassTriangleCut = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "transverseMassTriangleCut", "transverseMassTriangleCut", 200, 0., 800);

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
    if(!tau.decayModeFinding())
      continue;
    if(!(tau.pt() > fTauPtCut))
      continue;
    if(!(std::abs(tau.eta()) < 2.4))
      continue;
    if(!(tau.lTrkPt() > 10))
      continue;

    if(!tau.againstElectronTightMVA5())
      continue;
      /*    if(!tau.againstMuonTightMVA())
      continue;
    if(!tau.byMediumIsolationMVA3newDMwoLT())
      continue;
*/
    //    double pTau = tau.pt() * std::cosh(tau.eta());
    //   double pLeadingTrack = tau.lTrkPt() * std::cosh(tau.lTrkEta());

    double rTau = -999;
    //  if (pTau > 0 ) rTau = pLeadingTrack/ pTau; 
   if (tau.pt() > 0 ) rTau = tau.lTrkPt()/ tau.pt();   
   hRtau->Fill(rTau);

    if(!(tau.nProngs() == 1))
      continue;
  
    hTauPt->Fill(tau.pt());
    hTauEta->Fill(tau.eta());
    //    hTauPhi->Fill(tau.phi()* 180/3.14159265);
    hTauPhi->Fill(tau.phi());

    selectedTaus.push_back(tau);
  }
  if(selectedTaus.empty())
      return;
  cTauSelection.increment();


  size_t nmuons = 0;
  for(Muon muon: fEvent.muons()) {
    hMuonPt->Fill(muon.pt());
    hMuonEta->Fill(muon.eta());
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
    hElectronEta->Fill(electron.eta());
 
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



  std::vector<Jet> selectedJets;
  for(Jet jet: fEvent.jets()) {
    hJetPt->Fill(jet.pt());
    hJetEta->Fill(jet.eta());
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
    }

  }

 
  if(selectedJets.size() < 3)
    return;
  cJetSelection.increment();
 
  Jet jet1 = selectedJets[0];
  Jet jet2 = selectedJets[1];
  Jet jet3 = selectedJets[2];
  Tau tau = selectedTaus[0];
  //  std::cout << "jet1 pt "<< jet1.pt() << "jet1 id "<< jet1.pdgId() << std::endl;
  //  std::cout << "jet2 pt "<< jet2.pt() << std::endl;
  //std::cout << "jet3 pt "<< jet3.pt() << std::endl;


  double DeltaPhiTauMET  =   ROOT::Math::VectorUtil::DeltaPhi(tau,fEvent.met_Type1()) * 180/3.14159265;
   //std::cout << " deltaphi_taumet   "<<  DeltaPhiTauMET    << std::endl;
  double DeltaPhiJet1MET  =  ROOT::Math::VectorUtil::DeltaPhi(jet1,fEvent.met_Type1()) * 180/3.14159265; 
  double DeltaPhiJet2MET  = ROOT::Math::VectorUtil::DeltaPhi(jet2,fEvent.met_Type1()) * 180/3.14159265;
  double DeltaPhiJet3MET  = ROOT::Math::VectorUtil::DeltaPhi(jet3,fEvent.met_Type1()) * 180/3.14159265;
  double DeltaPhiTaujet1  =  ROOT::Math::VectorUtil::DeltaPhi(tau,jet1) * 180/3.14159265;
  
  hDPhiTauMetVsDphiJet1Met->Fill( DeltaPhiTauMET,DeltaPhiJet1MET);
  hDPhiTauMetVsDphiJet2Met->Fill( DeltaPhiTauMET, DeltaPhiJet2MET);
  hDPhiTauMetVsDphiJet3Met->Fill( DeltaPhiTauMET, DeltaPhiJet3MET);
  hDeltaPhiTauMet->Fill((DeltaPhiTauMET));
 

  math::XYZTLorentzVector threeJets;
  threeJets = jet1.p4() + jet2.p4() + jet3.p4();

  hPt3Jets->Fill(threeJets.pt());
  // hMJets->Fill(threeJets.M());
  //  std::cout << "   threeJets.M()"<<   threeJets.M()   << std::endl;
  hDPhiTauMetVsPt3jets->Fill(std::abs(DeltaPhiTauMET),threeJets.pt());
 
  double ptcut = 400.0 * (1.0 - DeltaPhiTauMET/180.0);
  /*
    LorentzVector allJets;
    double ptAllJets = 0;
      for(Jet& jet: selectedJets) {
      //  if ((*jet)->eta() > myMaxEta)
      //      std::cout << "jet eta  " << (*jet)->eta() << " jet pt  " << (*jet)->pt() << std::endl;
      allJets += (*jet)->p4();
      ptAllJets +=(*jet)->pt();
      }
  */
  
  math::XYZTLorentzVector myTau;
  myTau = jet1.p4(); 
  double myCosPhi = 999;
  double  transverseMass=-999;

  if (myMet > 0 && tau.pt() > 0)
    myCosPhi = (myTau.X() * std::cos(fEvent.met_Type1().phi()) + myTau.Y() * std::sin(fEvent.met_Type1().phi())) / tau.pt();
  // Calculate transverse mass                                                                                                                                                                     
  double myTransverseMass = -999;
  double myTransverseMassSquared = 0;
  if (std::abs(myCosPhi) < 1)
    myTransverseMassSquared = 2 * tau.pt() * myMet * (1.0-myCosPhi);
  if (myTransverseMassSquared >= 0)
    transverseMass = TMath::Sqrt(myTransverseMassSquared);
  htransverseMass->Fill(transverseMass);
  
  // with triangle cut
  
  if (!(threeJets.pt() < ptcut && DeltaPhiTauMET > 60)) {
    //increment(fTriangleCutCounter);
    htransverseMassTriangleCut->Fill(transverseMass);
  }

  

  size_t njets = 0;
    for(Jet& jet: selectedJets) {
      //      if (njets == 0)  jet1 = jet.p4();
      ++njets;
    }
  hNjets->Fill(njets);


  for(Jet& jet: selectedJets) {
    hjetSecondaryVertex->Fill(jet.secondaryVertex());
    //    std::cout << "jet eta  " << jet.eta() << " jet.secondaryVertex()  " << jet.secondaryVertex() << std::endl;   
               if(jet.secondaryVertex() > 0.898)
      hBJetPt->Fill(jet.pt());
  }

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
