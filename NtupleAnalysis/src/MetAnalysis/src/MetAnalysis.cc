#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"
#include "DataFormat/interface/Event.h"

#include "TH1F.h"
#include "TDirectory.h"

class MetAnalysis: public BaseSelector {
public:
  explicit MetAnalysis(const ParameterSet& config);
  virtual ~MetAnalysis() {}

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

  std::vector<double> fECALDeadCellEtaTable;
  std::vector<double> fECALDeadCellPhiTable;


};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(MetAnalysis);

MetAnalysis::MetAnalysis(const ParameterSet& config):
  BaseSelector(config),
  fEvent(config),
  fTauPtCut(config.getParameter<float>("tauPtCut")),
  cAllEvents(fEventCounter.addCounter("All events")),
  cWeighted(fEventCounter.addCounter("Weighted")),
  cTauSelection(fEventCounter.addCounter("Tau selection")),
  cMuonVeto(fEventCounter.addCounter("Muon veto")),
  cElectronVeto(fEventCounter.addCounter("Electron veto")),
  cJetSelection(fEventCounter.addCounter("Jet selection"))
{
  fECALDeadCellEtaTable.push_back(-2.35); fECALDeadCellPhiTable.push_back(-1.52639);
  fECALDeadCellEtaTable.push_back(-2.35); fECALDeadCellPhiTable.push_back(-1.43917);
  fECALDeadCellEtaTable.push_back(-2.25); fECALDeadCellPhiTable.push_back(-1.52639);
  fECALDeadCellEtaTable.push_back(-2.25); fECALDeadCellPhiTable.push_back(-1.43917);
  fECALDeadCellEtaTable.push_back(-2.25); fECALDeadCellPhiTable.push_back(-1.35194);
  fECALDeadCellEtaTable.push_back(-2.15); fECALDeadCellPhiTable.push_back(-2.48583);
  fECALDeadCellEtaTable.push_back(-2.05); fECALDeadCellPhiTable.push_back(-2.57306);
  fECALDeadCellEtaTable.push_back(-2.05); fECALDeadCellPhiTable.push_back(-2.48583);
  fECALDeadCellEtaTable.push_back(-2.05); fECALDeadCellPhiTable.push_back(-2.39861);
  fECALDeadCellEtaTable.push_back(-1.95); fECALDeadCellPhiTable.push_back(-2.48583);
  fECALDeadCellEtaTable.push_back(-1.65); fECALDeadCellPhiTable.push_back(0.654167);
  fECALDeadCellEtaTable.push_back(-1.55); fECALDeadCellPhiTable.push_back(0.566944);
  fECALDeadCellEtaTable.push_back(-1.55); fECALDeadCellPhiTable.push_back(0.654167);
  fECALDeadCellEtaTable.push_back(-1.55); fECALDeadCellPhiTable.push_back(1.00306);
  fECALDeadCellEtaTable.push_back(-1.45); fECALDeadCellPhiTable.push_back(-3.09639);
  fECALDeadCellEtaTable.push_back(-1.45); fECALDeadCellPhiTable.push_back(-1.61361);
  fECALDeadCellEtaTable.push_back(-1.35); fECALDeadCellPhiTable.push_back(-0.130833);
  fECALDeadCellEtaTable.push_back(-1.25); fECALDeadCellPhiTable.push_back(-2.66028);
  fECALDeadCellEtaTable.push_back(-1.25); fECALDeadCellPhiTable.push_back(-1.1775);
  fECALDeadCellEtaTable.push_back(-1.15); fECALDeadCellPhiTable.push_back(-1.1775);
  fECALDeadCellEtaTable.push_back(-0.95); fECALDeadCellPhiTable.push_back(2.04972);
  fECALDeadCellEtaTable.push_back(-0.95); fECALDeadCellPhiTable.push_back(3.00917);
  fECALDeadCellEtaTable.push_back(-0.85); fECALDeadCellPhiTable.push_back(2.04972);
  fECALDeadCellEtaTable.push_back(-0.85); fECALDeadCellPhiTable.push_back(3.00917);
  fECALDeadCellEtaTable.push_back(-0.75); fECALDeadCellPhiTable.push_back(-0.741389);
  fECALDeadCellEtaTable.push_back(-0.55); fECALDeadCellPhiTable.push_back(2.7475);
  fECALDeadCellEtaTable.push_back(-0.45); fECALDeadCellPhiTable.push_back(2.7475);
  fECALDeadCellEtaTable.push_back(-0.35); fECALDeadCellPhiTable.push_back(0.218056);
  fECALDeadCellEtaTable.push_back(-0.25); fECALDeadCellPhiTable.push_back(0.130833);
  fECALDeadCellEtaTable.push_back(-0.25); fECALDeadCellPhiTable.push_back(0.218056);
  fECALDeadCellEtaTable.push_back(-0.15); fECALDeadCellPhiTable.push_back(-2.57306);
  fECALDeadCellEtaTable.push_back(-0.15); fECALDeadCellPhiTable.push_back(0.130833);
  fECALDeadCellEtaTable.push_back(-0.15); fECALDeadCellPhiTable.push_back(0.741389);
  fECALDeadCellEtaTable.push_back(-0.05); fECALDeadCellPhiTable.push_back(-2.57306);
  fECALDeadCellEtaTable.push_back(-0.05); fECALDeadCellPhiTable.push_back(0.741389);
  fECALDeadCellEtaTable.push_back(-0.05); fECALDeadCellPhiTable.push_back(0.915833);
  fECALDeadCellEtaTable.push_back(0.05); fECALDeadCellPhiTable.push_back(1.78806);
  fECALDeadCellEtaTable.push_back(0.15); fECALDeadCellPhiTable.push_back(1.78806);
  fECALDeadCellEtaTable.push_back(0.85); fECALDeadCellPhiTable.push_back(0.3925);
  fECALDeadCellEtaTable.push_back(0.85); fECALDeadCellPhiTable.push_back(1.70083);
  fECALDeadCellEtaTable.push_back(0.85); fECALDeadCellPhiTable.push_back(2.83472);
  fECALDeadCellEtaTable.push_back(0.95); fECALDeadCellPhiTable.push_back(0.654167);
  fECALDeadCellEtaTable.push_back(0.95); fECALDeadCellPhiTable.push_back(1.70083);
  fECALDeadCellEtaTable.push_back(0.95); fECALDeadCellPhiTable.push_back(2.83472);
  fECALDeadCellEtaTable.push_back(1.05); fECALDeadCellPhiTable.push_back(-3.09639);
  fECALDeadCellEtaTable.push_back(1.05); fECALDeadCellPhiTable.push_back(0.654167);
  fECALDeadCellEtaTable.push_back(1.15); fECALDeadCellPhiTable.push_back(-3.09639);
  fECALDeadCellEtaTable.push_back(1.25); fECALDeadCellPhiTable.push_back(-0.479722);
  fECALDeadCellEtaTable.push_back(1.45); fECALDeadCellPhiTable.push_back(-2.57306);
  fECALDeadCellEtaTable.push_back(1.45); fECALDeadCellPhiTable.push_back(-0.218056);
  fECALDeadCellEtaTable.push_back(1.45); fECALDeadCellPhiTable.push_back(2.7475);
  fECALDeadCellEtaTable.push_back(1.55); fECALDeadCellPhiTable.push_back(-3.09639);
  fECALDeadCellEtaTable.push_back(1.55); fECALDeadCellPhiTable.push_back(-0.741389);
  fECALDeadCellEtaTable.push_back(1.55); fECALDeadCellPhiTable.push_back(-0.654167);
  fECALDeadCellEtaTable.push_back(1.55); fECALDeadCellPhiTable.push_back(-0.566944);
  fECALDeadCellEtaTable.push_back(1.65); fECALDeadCellPhiTable.push_back(-2.83472);
  fECALDeadCellEtaTable.push_back(1.65); fECALDeadCellPhiTable.push_back(-0.741389);
  fECALDeadCellEtaTable.push_back(1.65); fECALDeadCellPhiTable.push_back(-0.654167);
  fECALDeadCellEtaTable.push_back(1.65); fECALDeadCellPhiTable.push_back(-0.566944);
  fECALDeadCellEtaTable.push_back(1.75); fECALDeadCellPhiTable.push_back(-0.654167);
  fECALDeadCellEtaTable.push_back(1.75); fECALDeadCellPhiTable.push_back(-0.566944);
  fECALDeadCellEtaTable.push_back(1.75); fECALDeadCellPhiTable.push_back(0.741389);
  fECALDeadCellEtaTable.push_back(1.75); fECALDeadCellPhiTable.push_back(0.828611);

/*
2011 towers
   fECALDeadCellEtaTable.push_back(-2.35); fECALDeadCellPhiTable.push_back(-1.52639);
    fECALDeadCellEtaTable.push_back(-2.35); fECALDeadCellPhiTable.push_back(-1.43917);
    fECALDeadCellEtaTable.push_back(-2.35); fECALDeadCellPhiTable.push_back(-1.35194);
    fECALDeadCellEtaTable.push_back(-2.25); fECALDeadCellPhiTable.push_back(-1.52639);
    fECALDeadCellEtaTable.push_back(-2.25); fECALDeadCellPhiTable.push_back(-1.43917);
    fECALDeadCellEtaTable.push_back(-2.25); fECALDeadCellPhiTable.push_back(-1.35194);
    fECALDeadCellEtaTable.push_back(-2.15); fECALDeadCellPhiTable.push_back(-1.52639);
    fECALDeadCellEtaTable.push_back(-2.15); fECALDeadCellPhiTable.push_back(-1.43917);
    fECALDeadCellEtaTable.push_back(-2.15); fECALDeadCellPhiTable.push_back(-1.35194);
    fECALDeadCellEtaTable.push_back(-1.45); fECALDeadCellPhiTable.push_back(-3.09639);
    fECALDeadCellEtaTable.push_back(-1.25); fECALDeadCellPhiTable.push_back(-1.1775);
    fECALDeadCellEtaTable.push_back(-1.15); fECALDeadCellPhiTable.push_back(-1.1775);
    fECALDeadCellEtaTable.push_back(-0.95); fECALDeadCellPhiTable.push_back(2.04972);
    fECALDeadCellEtaTable.push_back(-0.85); fECALDeadCellPhiTable.push_back(2.04972);
    fECALDeadCellEtaTable.push_back(-0.75); fECALDeadCellPhiTable.push_back(-0.741389);
    fECALDeadCellEtaTable.push_back(-0.45); fECALDeadCellPhiTable.push_back(-1.9625);
    fECALDeadCellEtaTable.push_back(-0.35); fECALDeadCellPhiTable.push_back(0.218056);
    fECALDeadCellEtaTable.push_back(-0.25); fECALDeadCellPhiTable.push_back(0.130833);
    fECALDeadCellEtaTable.push_back(-0.25); fECALDeadCellPhiTable.push_back(0.218056);
    fECALDeadCellEtaTable.push_back(-0.15); fECALDeadCellPhiTable.push_back(-2.57306);
    fECALDeadCellEtaTable.push_back(-0.15); fECALDeadCellPhiTable.push_back(0.130833);
    fECALDeadCellEtaTable.push_back(-0.15); fECALDeadCellPhiTable.push_back(0.741389);
    fECALDeadCellEtaTable.push_back(-0.05); fECALDeadCellPhiTable.push_back(-2.57306);
    fECALDeadCellEtaTable.push_back(-0.05); fECALDeadCellPhiTable.push_back(0.741389);
    fECALDeadCellEtaTable.push_back(-0.05); fECALDeadCellPhiTable.push_back(0.915833);
    fECALDeadCellEtaTable.push_back(0.15); fECALDeadCellPhiTable.push_back(1.78806);
    fECALDeadCellEtaTable.push_back(0.85); fECALDeadCellPhiTable.push_back(1.70083);
    fECALDeadCellEtaTable.push_back(0.85); fECALDeadCellPhiTable.push_back(2.83472);
    fECALDeadCellEtaTable.push_back(0.95); fECALDeadCellPhiTable.push_back(0.654167);
    fECALDeadCellEtaTable.push_back(0.95); fECALDeadCellPhiTable.push_back(1.70083);
    fECALDeadCellEtaTable.push_back(0.95); fECALDeadCellPhiTable.push_back(2.83472);
    fECALDeadCellEtaTable.push_back(1.05); fECALDeadCellPhiTable.push_back(-3.09639);
    fECALDeadCellEtaTable.push_back(1.05); fECALDeadCellPhiTable.push_back(0.654167);
    fECALDeadCellEtaTable.push_back(1.15); fECALDeadCellPhiTable.push_back(-3.09639);
    fECALDeadCellEtaTable.push_back(1.25); fECALDeadCellPhiTable.push_back(-0.479722);
    fECALDeadCellEtaTable.push_back(1.35); fECALDeadCellPhiTable.push_back(-0.479722);
    fECALDeadCellEtaTable.push_back(1.45); fECALDeadCellPhiTable.push_back(-0.218056);
    fECALDeadCellEtaTable.push_back(1.45); fECALDeadCellPhiTable.push_back(2.48583);
    fECALDeadCellEtaTable.push_back(1.45); fECALDeadCellPhiTable.push_back(2.7475);
    fECALDeadCellEtaTable.push_back(1.55); fECALDeadCellPhiTable.push_back(-0.741389);
    fECALDeadCellEtaTable.push_back(1.55); fECALDeadCellPhiTable.push_back(-0.654167);
    fECALDeadCellEtaTable.push_back(1.55); fECALDeadCellPhiTable.push_back(-0.566944);
    fECALDeadCellEtaTable.push_back(1.65); fECALDeadCellPhiTable.push_back(-0.741389);
    fECALDeadCellEtaTable.push_back(1.65); fECALDeadCellPhiTable.push_back(-0.654167);
    fECALDeadCellEtaTable.push_back(1.65); fECALDeadCellPhiTable.push_back(-0.566944);
    fECALDeadCellEtaTable.push_back(1.65); fECALDeadCellPhiTable.push_back(0.741389);
    fECALDeadCellEtaTable.push_back(1.65); fECALDeadCellPhiTable.push_back(0.828611);
    fECALDeadCellEtaTable.push_back(1.75); fECALDeadCellPhiTable.push_back(-0.741389);
    fECALDeadCellEtaTable.push_back(1.75); fECALDeadCellPhiTable.push_back(-0.654167);
    fECALDeadCellEtaTable.push_back(1.75); fECALDeadCellPhiTable.push_back(-0.566944);
    fECALDeadCellEtaTable.push_back(1.75); fECALDeadCellPhiTable.push_back(0.741389);
    fECALDeadCellEtaTable.push_back(1.75); fECALDeadCellPhiTable.push_back(0.828611);
    fECALDeadCellEtaTable.push_back(1.85); fECALDeadCellPhiTable.push_back(0.741389);
    fECALDeadCellEtaTable.push_back(2.75); fECALDeadCellPhiTable.push_back(-0.741389);
    fECALDeadCellEtaTable.push_back(2.85); fECALDeadCellPhiTable.push_back(-0.915833);
    fECALDeadCellEtaTable.push_back(2.85); fECALDeadCellPhiTable.push_back(-0.828611);
    fECALDeadCellEtaTable.push_back(2.85); fECALDeadCellPhiTable.push_back(-0.741389);
*/

}

void MetAnalysis::book(TDirectory *dir) {
  hTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt", "Tau pT", 40, 0, 400);
  hTauEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauEta", "Tau eta", 50, -2.5, 2.5);
  hTauPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPhi", "Tau phi", 100, -3.1416, 3.1416);

  hMuonPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "muonPt", "Muon pT", 100, 0, 400);
  hMuonEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "muonEta", "Muon eta", 60, -3, 3);

  hElectronPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "electronPt", "Electron pT", 40, 0, 400);

  hJetPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "jetPt", "Jet pT", 100, 0, 500);
  hJetEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "jetEta", "Jet eta", 100, -5, 5);
  hJetPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "jetPhi", "Jet phi", 90, 0, 180);

  hBJetPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "bJetPt", "B jet pT", 100, 0, 500);

  hMet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Met", "Met", 200, 0., 600.);
  hMetPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetPhi", "Met phi", 90, 0., 180.);
  hMetJetInHole= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetJetInHole", "MetJetInHole", 200, 0., 600.);
  hMetNoJetInHole= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetNoJetInHole", "MetNoJetInHole", 200, 0., 600.);
  hMetJetInHole02= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetJetInHole02", "MetJetInHoleDR02", 200, 0., 600.);
  hMetNoJetInHole02= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetNoJetInHole02", "MetNoJetInHoleDR02", 200, 0., 600.);
}

void MetAnalysis::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}

void MetAnalysis::process(Long64_t entry) {
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
    hTauPhi->Fill(tau.phi());

    selectedTaus.push_back(tau);
  }
  //  if(selectedTaus.empty())
  //    return;
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

  double deltaR = 0.1;
  
  double myMet = fEvent.met_Type1().et();
  hMet->Fill(myMet); 
  hMetPhi->Fill(fEvent.met_Type1().phi()); 


  bool jetInEcalHole = false;
  bool jetInEcalHole02 = false;  

  std::vector<Jet> selectedJets;
  for(Jet jet: fEvent.jets()) {
    hJetPt->Fill(jet.pt());
    hJetEta->Fill(jet.eta());
    hJetPhi->Fill(jet.phi());

    if(jet.pt() > 30 && std::abs(jet.eta()) < 2.4) {
      selectedJets.push_back(jet);
    }
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
  }

  if ( jetInEcalHole ) hMetJetInHole->Fill(myMet); 
  if ( !jetInEcalHole ) hMetNoJetInHole->Fill(myMet);
  if ( jetInEcalHole02 ) hMetJetInHole02->Fill(myMet); 
  if ( !jetInEcalHole02 ) hMetNoJetInHole02->Fill(myMet);

  if(selectedJets.size() < 3)
    return;
  cJetSelection.increment();
/*
  for(Jet& jet: selectedJets) {
    if(jet.secondaryVertex() > 0.898)
      hBJetPt->Fill(jet.pt());
  }
*/
  fEventSaver.save();
}
