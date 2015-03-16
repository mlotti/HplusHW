#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"
#include "DataFormat/interface/Event.h"
//#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "Math/GenVector/VectorUtil.h"
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

  WrappedTH1 *hMuonPt;
  WrappedTH1 *hMuonEta;

  WrappedTH1 *hElectronPt;

  WrappedTH1 *hJetPt;
  WrappedTH1 *hJetEta;
  WrappedTH1 *hJetPhi;

  WrappedTH1 *hBJetPt;

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

  hMuonPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "muonPt", "Muon pT", 100, 0, 500);
  hMuonEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "muonEta", "Muon eta", 60, -3, 3);

  hElectronPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "electronPt", "Electron pT", 100, 0, 500);

  hJetPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "jetPt", "Jet pT", 200, 0, 1000);
  hJetEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "jetEta", "Jet eta", 100, -5, 5);
  hJetPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "jetPhi", "Jet phi", 90, 0, 180);

  hBJetPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "bJetPt", "B jet pT", 200, 0, 1000);

  hMet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Met", "Met", 200, 0., 1000.);
  hMetPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetPhi", "Met phi", 90, 0., 180.);
  hMetJetInHole= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetJetInHole", "MetJetInHole", 200, 0., 1000.);
  hMetNoJetInHole= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetNoJetInHole", "MetNoJetInHole", 200, 0., 1000.);
  hMetJetInHole02= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetJetInHole02", "MetJetInHoleDR02", 200, 0., 1000.);
  hMetNoJetInHole02= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetNoJetInHole02", "MetNoJetInHoleDR02", 200, 0., 1000.);
  hPt3Jets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Pt3Jets", "Pt3Jets", 200, 0., 400.);
  hM3jets = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "M3Jets", "M3Jets", 200, 0., 600.);
  hDeltaPhiTauMet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "DeltaPhiTauMet", "DeltaPhiTauMet", 90, 0., 180);
  hDPhiTauMetVsPt3jets = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "DPhiTauMetVsPt3jets", "Pt3jets;#Delta#phi(#tau jet,MET) (^{o});p_{T}^{3 jets}(GeV)", 180, 0., 180, 100, 0., 400.);
  hDPhiTauMetVsDphiJet1Met = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "DPhiTauMetVsDphiJet1Met", "DPhiTauMetVsDphiJet1Met", 90, 0., 180, 90, 0., 180.);
  hDPhiTauMetVsDphiJet2Met = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "DPhiTauMetVsDphiJet2Met", ";#Delta#phi(#tau jet2)", 90, 0., 180, 90, 0., 180.);
  hDPhiTauMetVsDphiJet2Met = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "DPhiTauMetVsDphiJet3Met", ";#Delta#phi(#tau jet3)", 90, 0., 180, 90, 0., 180.);
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
/*
    if(!tau.againstElectronTightMVA5())
      continue;
    if(!tau.againstMuonTightMVA())
      continue;
    if(!tau.byMediumIsolationMVA3newDMwoLT())
      continue;
*/
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
    if(muon.pt() > 15 && std::abs(muon.eta()) < 2.1)
      ++nmuons;
  }
  //  if(nmuons > 0)
  //   return;
  cMuonVeto.increment();
/*
  size_t nelectrons = 0;
  for(Electron electron: fEvent.electrons()) {
    hElectronPt->Fill(electron.pt());
    if(electron.pt() > 15 && std::abs(electron.eta()) < 2.4)
      ++nelectrons;
  }
  if(nelectrons > 0)
    return;
  cElectronVeto.increment();
*/

  
  double myMet = fEvent.met_Type1().et();
  hMet->Fill(myMet); 
  hMetPhi->Fill(fEvent.met_Type1().phi()* 180/3.14159265); 



  std::vector<Jet> selectedJets;
  for(Jet jet: fEvent.jets()) {
    hJetPt->Fill(jet.pt());
    hJetEta->Fill(jet.eta());
    hJetPhi->Fill(jet.phi()* 180/3.14159265);

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
    /*
    if(jet.pt() > 50 ) {
      size_t myTableSize = fECALDeadCellEtaTable.size();
      for (size_t i = 0; i < myTableSize; ++i) {
	double myDeltaEta = jet.eta() - fECALDeadCellEtaTable[i];
	double myDeltaPhi = jet.phi() - fECALDeadCellPhiTable[i];
	//if (myDeltaEta <= myHalfCellSize || myDeltaPhi <= myHalfCellSize) return false;                                                                                                                                    
	double myDeltaR = std::sqrt(myDeltaEta*myDeltaEta + myDeltaPhi*myDeltaPhi);
	if (myDeltaR < deltaR) jetInEcalHole = true;
	if (myDeltaR < deltaR+0.1) jetInEcalHole02 = true;
      }
    }
    */
  }

 
  if(selectedJets.size() < 3)
    return;
  cJetSelection.increment();
 
  Jet jet1 = selectedJets[0];
  Jet jet2 = selectedJets[1];
  Jet jet3 = selectedJets[2];
  Tau tau = selectedTaus[0];
  //  std::cout << "jet1 pt "<< jet1.pt() << std::endl;
  //  std::cout << "jet2 pt "<< jet2.pt() << std::endl;
  // std::cout << "jet3 pt "<< jet3.pt() << std::endl;

  //  double deltaPhi = ROOT::Math::VectorUtil::DeltaPhi(jet1.p4(),jet2->p4());
  double DeltaPhiJet1MET  = (jet1.phi() - fEvent.met_Type1().phi())* 180/3.14159265;
  double DeltaPhiJet2MET  = (jet2.phi() - fEvent.met_Type1().phi())* 180/3.14159265;
  double DeltaPhiJet3MET  = (jet3.phi() - fEvent.met_Type1().phi())* 180/3.14159265;
  double DeltaPhiTauMET  = (tau.phi() - fEvent.met_Type1().phi())* 180/3.14159265;
  
  //  hDPhiTauMetVsDphiJet1Met->Fill( DeltaPhiTauMET,DeltaPhiJet1MET);
  //  hDPhiTauMetVsDphiJet2Met->Fill( std::abs(DeltaPhiTauMET), std::abs(DeltaPhiJet2MET));
  //  hDPhiTauMetVsDphiJet3Met->Fill( std::abs(DeltaPhiTauMET), std::abs(DeltaPhiJet3MET));
  hDeltaPhiTauMet->Fill(std::abs(DeltaPhiTauMET));
 

  math::XYZTLorentzVector threeJets;
  threeJets = jet1.p4() + jet2.p4() + jet3.p4();

  hPt3Jets->Fill(threeJets.pt());
  hPt3Jets->Fill(threeJets.M());
  //  hDPhiTauMetVsPt3jets->Fill(std::abs(DeltaPhiTauMET),threeJets.pt());
 
  size_t njets = 0;
    for(Jet& jet: selectedJets) {
      //      if (njets == 0)  jet1 = jet.p4();
      ++njets;
    }




/*
  for(Jet& jet: selectedJets) {
    if(jet.secondaryVertex() > 0.898)
      hBJetPt->Fill(jet.pt());
  }
*/
  fEventSaver.save();
}
