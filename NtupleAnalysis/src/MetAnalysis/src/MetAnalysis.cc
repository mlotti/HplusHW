#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"
#include "DataFormat/interface/Event.h"
#include "Math/GenVector/VectorUtil.h"
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
  WrappedTH1 *hgenJetPt;
  WrappedTH1 *hgenJetEta;
  WrappedTH1 *hgenJetPhi;
  WrappedTH1 *hBJetPt;

  WrappedTH1 *hMet;
  WrappedTH1 *hMetPhi;
  WrappedTH1 *hMetJetInHole;
  WrappedTH1 *hMetNoJetInHole;
  WrappedTH1 *hMetJetInHole02;
  WrappedTH1 *hMetNoJetInHole02;
  WrappedTH1 *hMetJetInHole_bjet;
  WrappedTH1 *hMetJetInHole_gjet;
  WrappedTH1 *hDeltaPhiMetNoJetInHole; 
  WrappedTH1 *hDeltaPhiMetJetInHole; 

  WrappedTH2 *hgenjetEtaVsDeltaPtInHole; 
  WrappedTH2 *hgenjetPhiVsDeltaPtInHole; 
  WrappedTH2 *hgenjetPtVsDeltaPtInHole; 
  WrappedTH2 *hgenjetEtaVsDeltaPt; 
  WrappedTH2 *hgenjetPhiVsDeltaPt; 
  WrappedTH2 *hgenjetPtVsDeltaPt; 
  WrappedTH1 *hDeltaRJetGenJet; 
  WrappedTH1 *hDeltaPt;
  WrappedTH1 *hDeltaPtInHole;
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
  hTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt", "Tau pT", 200, 0, 1000);
  hTauEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauEta", "Tau eta", 50, -2.5, 2.5);
  hTauPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPhi", "Tau phi", 100, -3.1416, 3.1416);

  hMuonPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "muonPt", "Muon pT", 100, 0, 500);
  hMuonEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "muonEta", "Muon eta", 60, -3, 3);

  hElectronPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "electronPt", "Electron pT", 100, 0, 500);

  hJetPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "jetPt", "Jet pT", 200, 0, 1000);
  hJetEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "jetEta", "Jet eta", 100, -5, 5);
  hJetPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "jetPhi", "Jet phi", 90, 0, 180);

  hgenJetPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genjetPt", "genJet pT", 200, 0, 1000);
  hgenJetEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genjetEta", "genJet eta", 100, -5, 5);
  hgenJetPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "genjetPhi", "genJet phi", 90, 0, 180);

  hBJetPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "bJetPt", "B jet pT", 200, 0, 1000);

  hMet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Met", "Met", 200, 0., 1000.);
  hMetPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetPhi", "Met phi", 90, 0., 180.);
  hMetJetInHole= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetJetInHole", "MetJetInHole", 200, 0., 1000.);
  hMetNoJetInHole= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetNoJetInHole", "MetNoJetInHole", 200, 0., 1000.);
  hMetJetInHole02= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetJetInHole02", "MetJetInHoleDR02", 200, 0., 1000.);
  hMetNoJetInHole02= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetNoJetInHole02", "MetNoJetInHoleDR02", 200, 0., 1000.);
  hMetJetInHole_bjet= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetJetInHole_bjet", "MetJetInHole_bjet", 200, 0., 1000.);
  hMetJetInHole_gjet= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetJetInHole_gjet", "MetJetInHole_gjet", 200, 0., 1000.);
  //hMetJetInHole= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetJetInHole", "MetJetInHole", 200, 0., 1000.);
  // hMetNoJetInHole= fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "MetNoJetInHole", "MetNoJetInHole", 200, 0., 1000.);
  hDeltaPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "DeltaPt", "DeltaPt", 100, -1.5, 1.5);
  hDeltaPtInHole = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "DeltaPtInHole", "DeltaPtInHole", 100, -1.5, 1.5);
  hDeltaPhiMetNoJetInHole = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "DeltaPhiMetNoJetInHole", "DeltaPhiMetNoJetInHole", 90, 0., 180);
  hDeltaPhiMetJetInHole = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "DeltaPhiMetJetInHole", "DeltaPhiMetJetInHole", 90, 0., 180);
  hgenjetEtaVsDeltaPtInHole = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "genjetEtaVsDeltaPtInHole", "genjetEtaVsDeltaPtInHole", 250, -2.5, 2.5,100,-1.5,1.5);
  hgenjetPhiVsDeltaPtInHole = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "genjetPhiVsDeltaPtInHole", "genjetPhiVsDeltaPtInHole", 90, 0., 180,100,-1.5,1.5);
  hgenjetPtVsDeltaPtInHole = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "genjetPtVsDeltaPtInHole", "genjetPtVsDeltaPtInHole", 200, 0., 1000,100,-1.5,1.5);
  hgenjetEtaVsDeltaPt = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "genjetEtaVsDeltaPt", "genjetEtaVsDeltaPt", 250, -2.5, 2.5,100,-1.5,1.5);
  hgenjetPhiVsDeltaPt = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "genjetPhiVsDeltaPt", "genjetPhiVsDeltaPt", 90, 0., 180,100,-1.5,1.5);
  hgenjetPtVsDeltaPt = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, dir, "genjetPtVsDeltaPt", "genjetPtVsDeltaPt", 200, 0., 1000,100,-1.5,1.5);
  hDeltaRJetGenJet = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "deltaRJetGenJet", "deltaRJetGenJet", 100, 0.,5);  


}

void MetAnalysis::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}

void MetAnalysis::process(Long64_t entry) {
  cAllEvents.increment();

  fEventWeight.multiplyWeight(0.5);
  cWeighted.increment();

  //   std::cout  << "  muons  "<<Muon muon: fEvent.muons()  << std::endl;            

  std::vector<Tau> selectedTaus;
  for(Tau tau: fEvent.taus()) {
    hTauPt->Fill(tau.pt());
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
    /*
    if(!tau.againstMuonTightMVA())
      continue;
    if(!tau.byMediumIsolationMVA3newDMwoLT())
      continue;
    */
    if(!(tau.nProngs() == 1))
      continue;
    
    //hTauPt->Fill(tau.pt());
    hTauEta->Fill(tau.eta());
    //    hTauPhi->Fill(tau.phi()* 180/3.14159265);
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
  hMetPhi->Fill(fEvent.met_Type1().phi()* 180/3.14159265); 


  bool jetInEcalHole = false;
  bool jetInEcalHole02 = false;  
  bool jetInEcalHole_bjet = false;
  bool jetInEcalHole_gjet = false;

  std::vector<Jet> selectedJets;
  for(Jet jet: fEvent.jets()) {
    hJetPt->Fill(jet.pt());
    hJetEta->Fill(jet.eta());
    hJetPhi->Fill(jet.phi()* 180/3.14159265);

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
	if (myDeltaR < deltaR) {
	  jetInEcalHole = true;
	  if (jet.pdgId() == 5) jetInEcalHole_bjet = true;
	  if (jet.pdgId() == 0) jetInEcalHole_gjet = true;
	}
	if (myDeltaR < deltaR+0.1) jetInEcalHole02 = true;
      }
      double DeltaPhiJetMET  =   ROOT::Math::VectorUtil::DeltaPhi(jet,fEvent.met_Type1()) * 180/3.14159265;
    
     if (jetInEcalHole) {
       hDeltaPhiMetJetInHole->Fill(DeltaPhiJetMET);
     }
     if (!jetInEcalHole) {
       hDeltaPhiMetNoJetInHole->Fill(DeltaPhiJetMET);
     }
     // matching genjet
     for(GenJet genjet: fEvent.genjets()) {
       double myDeltaEta = jet.eta() - genjet.eta();
       double myDeltaPhi = (jet.phi() - genjet.phi())* 180/3.14159265;
       double myDeltaR = std::sqrt(myDeltaEta*myDeltaEta + myDeltaPhi*myDeltaPhi);
       hDeltaRJetGenJet->Fill(myDeltaR);
       //  hDeltaPt->Fill(deltaPt);
      if ( myDeltaR < 0.4) {
	double deltaPt = (genjet.pt() - jet.pt())/genjet.pt();
	if (!jetInEcalHole) {
	  hDeltaPt->Fill(deltaPt);
	  hgenjetEtaVsDeltaPt->Fill(genjet.eta(),deltaPt);
	  hgenjetPhiVsDeltaPt->Fill(genjet.phi()* 180/3.14159265,deltaPt);
	  hgenjetPtVsDeltaPt->Fill(genjet.pt(),deltaPt);
	}	 	 
	if (jetInEcalHole) {
	  hDeltaPtInHole->Fill(deltaPt);
	  hgenjetEtaVsDeltaPtInHole->Fill(genjet.eta(),deltaPt);
	  hgenjetPhiVsDeltaPtInHole->Fill(genjet.phi()* 180/3.14159265,deltaPt);
	  hgenjetPtVsDeltaPtInHole->Fill(genjet.pt(),deltaPt);	 	 
	}
      }
     }
    }
  }
  if ( jetInEcalHole ) hMetJetInHole->Fill(myMet); 
  if ( !jetInEcalHole ) hMetNoJetInHole->Fill(myMet);
  if ( jetInEcalHole02 ) hMetJetInHole02->Fill(myMet); 
  if ( !jetInEcalHole02 ) hMetNoJetInHole02->Fill(myMet);
  if ( jetInEcalHole_bjet ) hMetJetInHole_bjet->Fill(myMet); 
  if ( jetInEcalHole_gjet ) hMetJetInHole_gjet->Fill(myMet); 

  //  for(GenParticleGenerated genparticle: fEvent.genparticles()) {
  //  } 
  //  double mypt = fEvent.met_Type1().et();

  std::vector<GenJet> genJets;
  for(GenJet genjet: fEvent.genjets()) {
    hgenJetPt->Fill(genjet.pt());
    hgenJetEta->Fill(genjet.eta());
    hgenJetPhi->Fill(genjet.phi()* 180/3.14159265);
    if(genjet.pt() > 30 && std::abs(genjet.eta()) < 2.4) {
      genJets.push_back(genjet);
    }

  }



  if(selectedJets.size() < 3)
    return;
  cJetSelection.increment();


  /*  for(Jet& jet: selectedJets) {
    if(jet.secondaryVertex() > 0.898)
      hBJetPt->Fill(jet.pt());
  }
*/
  fEventSaver.save();
}
