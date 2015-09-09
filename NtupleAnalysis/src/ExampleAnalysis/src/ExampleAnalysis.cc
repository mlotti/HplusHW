#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "DataFormat/interface/Event.h"

#include "TH1F.h"
#include "TDirectory.h"

class ExampleAnalysis: public BaseSelector {
public:
  explicit ExampleAnalysis(const ParameterSet& config);
  virtual ~ExampleAnalysis() {}

  virtual void book(TDirectory *dir) override;
  virtual void setupBranches(BranchManager& branchManager) override;
  virtual void process(Long64_t entry) override;

private:
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

  WrappedTH1 *hElectronPt;

  WrappedTH1 *hJetPt;

  WrappedTH1 *hBJetPt;
};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(ExampleAnalysis);

ExampleAnalysis::ExampleAnalysis(const ParameterSet& config):
  BaseSelector(config),
  fTauPtCut(config.getParameter<float>("tauPtCut")),
  cAllEvents(fEventCounter.addCounter("All events")),
  cWeighted(fEventCounter.addCounter("Weighted")),
  cTauSelection(fEventCounter.addCounter("Tau selection")),
  cMuonVeto(fEventCounter.addCounter("Muon veto")),
  cElectronVeto(fEventCounter.addCounter("Electron veto")),
  cJetSelection(fEventCounter.addCounter("Jet selection"))
{}

void ExampleAnalysis::book(TDirectory *dir) {
  hTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt", "Tau pT", 40, 0, 400);
  hTauEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauEta", "Tau eta", 50, -2.5, 2.5);
  hTauPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPhi", "Tau phi", 100, -3.1416, 3.1416);

  hMuonPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "muonPt", "Muon pT", 40, 0, 400);

  hElectronPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "electronPt", "Electron pT", 40, 0, 400);

  hJetPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "jetPt", "Jet pT", 40, 0, 400);

  hBJetPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "bJetPt", "B jet pT", 40, 0, 400);
}

void ExampleAnalysis::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}

void ExampleAnalysis::process(Long64_t entry) {
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
    if(!(tau.lChTrkPt() > 10))
      continue;
    /*if(!tau.againstElectronTightMVA3())
      continue;
    if(!tau.againstMuonTight())
      continue;
    if(!tau.byMediumIsolationMVA2())
      continue;*/
    if(!(tau.nProngs() == 1))
      continue;

    hTauPt->Fill(tau.pt());
    hTauEta->Fill(tau.eta());
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
  if(nmuons > 0)
    return;
  cMuonVeto.increment();

  size_t nelectrons = 0;
  for(Electron electron: fEvent.electrons()) {
    hElectronPt->Fill(electron.pt());
    if(electron.pt() > 15 && std::abs(electron.eta()) < 2.4)
      ++nelectrons;
  }
  if(nelectrons > 0)
    return;
  cElectronVeto.increment();

  std::vector<Jet> selectedJets;
  for(Jet jet: fEvent.jets()) {
    hJetPt->Fill(jet.pt());
    if(jet.pt() > 30 && std::abs(jet.eta()) < 2.4)
      selectedJets.push_back(jet);
  }
  if(selectedJets.size() < 3)
    return;
  cJetSelection.increment();

//   for(Jet& jet: selectedJets) {
//     if(jet.secondaryVertex() > 0.898)
//       hBJetPt->Fill(jet.pt());
//   }

  fEventSaver.save();
}
