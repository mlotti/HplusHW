#include "BaseSelector.h"
#include "Branches.h"
#include "Configuration.h"

#include "TDirectory.h"
#include "TH1F.h"
#include "Math/VectorUtil.h"

// EmbeddingMuonIsolationSelector
class EmbeddingMuonIsolationSelector: public BaseSelector {
public:
  EmbeddingMuonIsolationSelector(const std::string& puWeight = "", const std::string& isolationMode = "disabled");
  ~EmbeddingMuonIsolationSelector();

  void setOutput(TDirectory *dir);
  void setupBranches(BranchManager& branchManager);
  bool process(Long64_t entry);

private:
  // Input
  EventInfo fEventInfo;
  EmbeddingMuonCollection fMuons;
  TauCollection fTaus;

  std::string fPuWeightName;
  Branch<double> *fPuWeight;
  Branch<unsigned> *fVertexCount;
  Branch<bool> *fIsoMuTrigger;

  EmbeddingMuonIsolation::Mode fIsolationMode;

  // Output
  // Counts
  EventCounter::Count cAll;
  EventCounter::Count cTauID;
  EventCounter::Count cMuonIsolation;
  EventCounter::Count cIsoMuTrigger;

  // Histograms
  class Histos {
  public:
    Histos(const std::string& postfix): fPostfix(postfix) {}

    void makeHistos();

    void fillTau(TauCollection::Tau& tau, double weight);
    void fillVertex(unsigned nvertex, double weight);
  private:
    TH1 *makeEta(const char *name);
    TH1 *makePt(const char *name);
    TH1 *makePhi(const char *name);
    TH1 *makeRtau(const char *name);
    TH1 *makeVertexCount(const char *name);

    std::string fPostfix;
    TH1 *hTauEta;
    TH1 *hTauPt;
    TH1 *hTauPhi;
    TH1 *hTauLeadingTrackPt;
    TH1 *hTauRtau;
    TH1 *hVertexCount;
  };

  Histos hAfterTauID;
  Histos hAfterMuonIsolation;
  Histos hAfterIsoMuTrigger;
};

EmbeddingMuonIsolationSelector::EmbeddingMuonIsolationSelector(const std::string& puWeight, const std::string& isolationMode):
  BaseSelector(),
  fMuons(),
  fPuWeightName(puWeight),
  fIsolationMode(EmbeddingMuonIsolation::stringToMode(isolationMode)),
  cAll(fEventCounter.addCounter("All events")),
  cTauID(fEventCounter.addCounter("Tau ID")),
  cMuonIsolation(fEventCounter.addCounter("Muon isolation")),
  cIsoMuTrigger(fEventCounter.addCounter("IsoMu trigger")),
  hAfterTauID("AfterTauID"),
  hAfterMuonIsolation("AfterMuonIsolation"),
  hAfterIsoMuTrigger("AfterIsoMuTrigger")
{}

EmbeddingMuonIsolationSelector::~EmbeddingMuonIsolationSelector() {}

TH1 *EmbeddingMuonIsolationSelector::Histos::makeEta(const char *name) { return makeTH<TH1F>(name, "Tau eta", 25, -2.5, 2.5); }
TH1 *EmbeddingMuonIsolationSelector::Histos::makePt(const char *name)  { return makeTH<TH1F>(name, "Tau pt", 25, 0, 250); }
TH1 *EmbeddingMuonIsolationSelector::Histos::makePhi(const char *name)  { return makeTH<TH1F>(name, "Tau phi", 32, -3.2, 3.2); }
TH1 *EmbeddingMuonIsolationSelector::Histos::makeRtau(const char *name)  { return makeTH<TH1F>(name, "Rtau", 10, 0.6, 1.1); }
TH1 *EmbeddingMuonIsolationSelector::Histos::makeVertexCount(const char *name) { return makeTH<TH1F>(name, "Vertex count", 30, 0, 30); }

void EmbeddingMuonIsolationSelector::Histos::makeHistos() {
  hTauPt = makePt(("tauPt_"+fPostfix).c_str());
  hTauEta = makeEta(("tauEta_"+fPostfix).c_str());
  hTauPhi = makePhi(("tauPhi_"+fPostfix).c_str());
  hTauLeadingTrackPt = makePt(("tauLeadingTrackPt_"+fPostfix).c_str());
  hTauRtau = makeRtau(("tauRtau_"+fPostfix).c_str());
  hVertexCount = makeVertexCount(("vertexCount_"+fPostfix).c_str());
}
void EmbeddingMuonIsolationSelector::Histos::fillTau(TauCollection::Tau& tau, double weight) {
  hTauPt->Fill(tau.p4().Pt(), weight);
  hTauEta->Fill(tau.p4().Eta(), weight);
  hTauPhi->Fill(tau.p4().Phi(), weight);
  hTauLeadingTrackPt->Fill(tau.leadPFChargedHadrCandP4().Pt(), weight);
  hTauRtau->Fill(tau.rtau(), weight);
}
void EmbeddingMuonIsolationSelector::Histos::fillVertex(unsigned nvertex, double weight) {
  hVertexCount->Fill(nvertex, weight);
}

void EmbeddingMuonIsolationSelector::setOutput(TDirectory *dir) {
  if(dir)
    dir->cd();

  hAfterTauID.makeHistos();
  hAfterMuonIsolation.makeHistos();
  hAfterIsoMuTrigger.makeHistos();
}

void EmbeddingMuonIsolationSelector::setupBranches(BranchManager& branchManager) {
  fEventInfo.setupBranches(branchManager);
  fMuons.setupBranches(branchManager, isMC());
  fTaus.setupBranches(branchManager);
  if(!fPuWeightName.empty())
    branchManager.book(fPuWeightName, &fPuWeight);
  branchManager.book("goodPrimaryVertex_count", &fVertexCount);
  branchManager.book("trigger_IsoMu30_eta2p1", &fIsoMuTrigger);
}

bool EmbeddingMuonIsolationSelector::process(Long64_t entry) {
  double weight = 1.0;
  if(!fPuWeightName.empty()) {
    weight *= fPuWeight->value();
  }
  fEventCounter.setWeight(weight);
  //std::cout << weight << std::endl;

  cAll.increment();

  std::vector<TauCollection::Tau> selectedTaus;

  // Tau ID
  for(size_t i=0; i<fTaus.size(); ++i) {
    TauCollection::Tau tau = fTaus.get(i);
    if(!TauID::decayModeFinding(tau)) continue;
    if(!TauID::eta(tau)) continue;
    if(!TauID::pt(tau)) continue;
    if(!TauID::leadingChargedHadrCandPt(tau)) continue;
    if(!TauID::againstElectron(tau)) continue;
    if(!TauID::againstMuon(tau)) continue;
    if(!TauID::isolation(tau)) continue;
    if(!TauID::oneProng(tau)) continue;
    if(!TauID::rtau(tau)) continue;
 
    hAfterTauID.fillTau(tau, weight);
    selectedTaus.push_back(tau);
  }
  if(selectedTaus.empty()) return true;
  cTauID.increment();
  hAfterTauID.fillVertex(fVertexCount->value(), weight);

  // Muon isolation
  std::vector<EmbeddingMuonCollection::Muon> selectedMuons;
  for(size_t i=0; i<fMuons.size(); ++i) {
    EmbeddingMuonCollection::Muon muon = fMuons.get(i);
    if(!MuonID::isolation(muon, fIsolationMode)) continue;
    selectedMuons.push_back(muon);
  }
  if(selectedMuons.empty()) return true;
  cMuonIsolation.increment();

  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];
    hAfterMuonIsolation.fillTau(tau, weight);
  }
  hAfterMuonIsolation.fillVertex(fVertexCount->value(), weight);

  // Mu trigger
  if(!fIsoMuTrigger->value()) return true;
  cIsoMuTrigger.increment();

  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];
    hAfterIsoMuTrigger.fillTau(tau, weight);
  }
  hAfterIsoMuTrigger.fillVertex(fVertexCount->value(), weight);

  return true;
}
