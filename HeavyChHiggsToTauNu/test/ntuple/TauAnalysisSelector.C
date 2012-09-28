#include "BaseSelector.h"
#include "Branches.h"
#include "Configuration.h"

#include "TDirectory.h"
#include "TH1F.h"
#include "Math/VectorUtil.h"


// TauAnalysisSelector
class TauAnalysisSelector: public BaseSelector {
public:
  TauAnalysisSelector(const std::string& puWeight = "");
  ~TauAnalysisSelector();

  void setOutput(TDirectory *dir);
  void setupBranches(TTree *tree);
  bool process(Long64_t entry);

private:
  // Input
  EventInfo fEventInfo;
  TauCollection fTaus;

  std::string fPuWeightName;
  Branch<double> fPuWeight;

  TH1 *makeEta(const char *name);
  TH1 *makePt(const char *name);
  TH1 *makePhi(const char *name);

  // Output
  // Counts
  EventCounter::Count cAll;
  EventCounter::Count cDecayModeFinding;
  EventCounter::Count cEtaCut;
  EventCounter::Count cPtCut;
  EventCounter::Count cLeadingTrackPtCut;
  EventCounter::Count cAgainstElectron;
  EventCounter::Count cAgainstMuon;
  EventCounter::Count cIsolation;
  EventCounter::Count cOneProng;
  EventCounter::Count cRtau;

  // Histograms
  TH1 *hTauEta_AfterDecayModeFindingIsolation;
  TH1 *hTauPt_AfterDecayModeFindingIsolation;

  TH1 *hTauPt_AfterEtaCutIsolation;

  TH1 *hTauPhi_AfterPtCutIsolation;
  TH1 *hTauLeadingTrackPt_AfterPtCutIsolation;

  TH1 *hTauDecayMode_AfterIsolation;
  TH1 *hTauDecayModeAll_AfterIsolation;

  TH1 *hTauPt_AfterOneProng;
  TH1 *hTauP_AfterOneProng;
  TH1 *hTauLeadingTrackPt_AfterOneProng;
  TH1 *hTauLeadingTrackP_AfterOneProng;
  TH1 *hTauRtau_AfterOneProng;

  TH1 *hTauPt_AfterRtau;
};

TauAnalysisSelector::TauAnalysisSelector(const std::string& puWeight):
  BaseSelector(),
  fPuWeightName(puWeight),
  cAll(fEventCounter.addCounter("All events")),
  cDecayModeFinding(fEventCounter.addCounter("Decay mode finding")),
  cEtaCut(fEventCounter.addCounter("Eta cut")),
  cPtCut(fEventCounter.addCounter("Pt cut")),
  cLeadingTrackPtCut(fEventCounter.addCounter("Leading track pt")),
  cAgainstElectron(fEventCounter.addCounter("Against electron")),
  cAgainstMuon(fEventCounter.addCounter("Against muon")),
  cIsolation(fEventCounter.addCounter("Isolation")),
  cOneProng(fEventCounter.addCounter("One prong")),
  cRtau(fEventCounter.addCounter("Rtau"))
{}

TauAnalysisSelector::~TauAnalysisSelector() {}

TH1 *TauAnalysisSelector::makeEta(const char *name) { return makeTH<TH1F>(name, "Tau eta", 25, -2.5, 2.5); }
TH1 *TauAnalysisSelector::makePt(const char *name)  { return makeTH<TH1F>(name, "Tau pt", 25, 0, 250); }
TH1 *TauAnalysisSelector::makePhi(const char *name)  { return makeTH<TH1F>(name, "Tau phi", 32, -3.2, 3.2); }

void TauAnalysisSelector::setOutput(TDirectory *dir) {
  if(dir)
    dir->cd();

  hTauEta_AfterDecayModeFindingIsolation = makeEta("tauEta_AfterDecayModeFindingIsolation");
  hTauPt_AfterDecayModeFindingIsolation = makePt("tauPt_AfterDecayModeFindingIsolation");

  hTauPt_AfterEtaCutIsolation = makePt("tauPt_AfterEtaCutIsolation");

  hTauPhi_AfterPtCutIsolation = makePhi("tauPhi_AfterPtCutIsolation");
  hTauLeadingTrackPt_AfterPtCutIsolation = makePt("tauLeadingTrackPt_AfterPtCutIsolation");

  hTauDecayMode_AfterIsolation = makeTH<TH1F>("tauDecayMode_AfterIsolation", "Decay mode", 5, 0, 5);
  hTauDecayModeAll_AfterIsolation = makeTH<TH1F>("tauDecayModeAll_AfterIsolation", "Decay mode", 16, 0, 16);

  hTauPt_AfterOneProng = makePt("tauPt_AfterOneProng");
  hTauP_AfterOneProng = makePt("tauP_AfterOneProng");
  hTauLeadingTrackPt_AfterOneProng = makePt("tauLeadingTrackPt_AfterOneProng");
  hTauLeadingTrackP_AfterOneProng = makePt("tauLeadingTrackP_AfterOneProng");
  hTauRtau_AfterOneProng = makeTH<TH1F>("tauRtau_AfterOneProng", "Rtau", 22, 0, 1.1);

  hTauPt_AfterRtau = makePt("tauPt_AfterRtau");
}

void TauAnalysisSelector::setupBranches(TTree *tree) {
  fEventInfo.setupBranches(tree);
  fTaus.setupBranches(tree);
  if(!fPuWeightName.empty())
    fPuWeight.setupBranch(tree, fPuWeightName.c_str());
}

bool TauAnalysisSelector::process(Long64_t entry) {
  fEventInfo.setEntry(entry);
  fTaus.setEntry(entry);
  fPuWeight.setEntry(entry);

  double weight = 1.0;
  if(!fPuWeightName.empty()) {
    weight *= fPuWeight.value();
  }
  fEventCounter.setWeight(weight);

  cAll.increment();

  std::vector<TauCollection::Tau> selectedTaus;
  std::vector<TauCollection::Tau> tmp;

  // Decay mode finding
  for(size_t i=0; i<fTaus.size(); ++i) {
    TauCollection::Tau tau = fTaus.get(i);
    if(!TauID::decayModeFinding(tau)) continue;

    if(TauID::isolation(tau)) {
      hTauEta_AfterDecayModeFindingIsolation->Fill(tau.p4().Eta(), weight);
      hTauPt_AfterDecayModeFindingIsolation->Fill(tau.p4().Pt(), weight);
    }
    selectedTaus.push_back(tau);
  }
  if(selectedTaus.empty()) return true;
  cDecayModeFinding.increment();

  // Eta cut
  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];
    if(!TauID::eta(tau)) continue;

    if(TauID::isolation(tau)) {
      hTauPt_AfterEtaCutIsolation->Fill(tau.p4().Pt(), weight);
    }
    tmp.push_back(tau);
  }
  selectedTaus.swap(tmp);
  tmp.clear();
  if(selectedTaus.empty()) return true;
  cEtaCut.increment();

  // Pt cut
  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];
    if(!TauID::pt(tau)) continue;

    if(TauID::isolation(tau)) {
      hTauPhi_AfterPtCutIsolation->Fill(tau.p4().Phi(), weight);
      hTauLeadingTrackPt_AfterPtCutIsolation->Fill(tau.leadPFChargedHadrCandP4().Pt(), weight);
    }
    tmp.push_back(tau);
  }
  selectedTaus.swap(tmp);
  tmp.clear();
  if(selectedTaus.empty()) return true;
  cPtCut.increment();

  // Leading track pt
  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];
    if(!TauID::leadingChargedHadrCandPt(tau)) continue;
    tmp.push_back(tau);
  }
  selectedTaus.swap(tmp);
  tmp.clear();
  if(selectedTaus.empty()) return true;
  cLeadingTrackPtCut.increment();

  // Against electron
  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];
    if(!TauID::againstElectron(tau)) continue;
    tmp.push_back(tau);
  }
  selectedTaus.swap(tmp);
  tmp.clear();
  if(selectedTaus.empty()) return true;
  cAgainstElectron.increment();

  // Against muon
  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];
    if(!TauID::againstMuon(tau)) continue;
    tmp.push_back(tau);
  }
  selectedTaus.swap(tmp);
  tmp.clear();
  if(selectedTaus.empty()) return true;
  cAgainstMuon.increment();

  // Tau candidate selection finished

  // Isolation
  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];

    if(!TauID::isolation(tau)) continue;

    int decayMode = tau.decayMode();
    int fill = -1;
    if     (decayMode <= 2)  fill = decayMode; // 0 = pi+, 1 = pi+pi0, 2 = pi+pi0pi0
    else if(decayMode == 10) fill = 3; // pi+pi-pi+
    else                     fill = 4; // Other
    hTauDecayModeAll_AfterIsolation->Fill(decayMode, weight);
    hTauDecayMode_AfterIsolation->Fill(fill, weight);

    tmp.push_back(tau);
  }
  selectedTaus.swap(tmp);
  tmp.clear();
  if(selectedTaus.empty()) return true;
  cIsolation.increment();

  // One prong
  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];
    if(!TauID::oneProng(tau)) continue;
    tmp.push_back(tau);

    hTauPt_AfterOneProng->Fill(tau.p4().Pt(), weight);
    hTauP_AfterOneProng->Fill(tau.p4().P(), weight);
    hTauLeadingTrackPt_AfterOneProng->Fill(tau.leadPFChargedHadrCandP4().Pt(), weight);
    hTauLeadingTrackP_AfterOneProng->Fill(tau.leadPFChargedHadrCandP4().P(), weight);
    hTauRtau_AfterOneProng->Fill(tau.rtau(), weight);

    tmp.push_back(tau);
  }
  selectedTaus.swap(tmp);
  tmp.clear();
  if(selectedTaus.empty()) return true;
  cOneProng.increment();

  // Rtau
  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];
    if(!TauID::rtau(tau)) continue;

    hTauPt_AfterRtau->Fill(tau.p4().Pt(), weight);

    tmp.push_back(tau);
  }
  selectedTaus.swap(tmp);
  tmp.clear();
  if(selectedTaus.empty()) return true;
  cRtau.increment();

  // Tau ID finished

  return true;
}
