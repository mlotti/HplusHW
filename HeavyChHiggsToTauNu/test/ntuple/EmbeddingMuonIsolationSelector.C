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
  void setupBranches(TTree *tree);
  bool process(Long64_t entry);

private:
  // Input
  EventInfo fEventInfo;
  EmbeddingMuonCollection fMuons;
  TauCollection fTaus;

  std::string fPuWeightName;
  Branch<double> fPuWeight;
  Branch<unsigned> fVertexCount;

  enum IsolationMode {
    kDisabled,
    kStandard,
    kChargedHadrRel10,
    kChargedHadrRel15,
    kTauLike
  };
  IsolationMode fIsolationMode;

  TH1 *makeEta(const char *name);
  TH1 *makePt(const char *name);
  TH1 *makePhi(const char *name);
  TH1 *makeRtau(const char *name);
  TH1 *makeVertexCount(const char *name);

  // Output
  // Counts
  EventCounter::Count cAll;
  EventCounter::Count cTauID;
  EventCounter::Count cMuonIsolation;

  // Histograms
  TH1 *hTauEta_AfterTauID;
  TH1 *hTauPt_AfterTauID;
  TH1 *hTauPhi_AfterTauID;
  TH1 *hTauLeadingTrackPt_AfterTauID;
  TH1 *hTauRtau_AfterTauID;
  TH1 *hVertexCount_AfterTauID;

  TH1 *hTauEta_AfterMuonIsolation;
  TH1 *hTauPt_AfterMuonIsolation;
  TH1 *hTauPhi_AfterMuonIsolation;
  TH1 *hTauLeadingTrackPt_AfterMuonIsolation;
  TH1 *hTauRtau_AfterMuonIsolation;
  TH1 *hVertexCount_AfterMuonIsolation;
};

EmbeddingMuonIsolationSelector::EmbeddingMuonIsolationSelector(const std::string& puWeight, const std::string& isolationMode):
  BaseSelector(),
  fPuWeightName(puWeight),
  cAll(fEventCounter.addCounter("All events")),
  cTauID(fEventCounter.addCounter("Tau ID")),
  cMuonIsolation(fEventCounter.addCounter("Muon isolation"))
{
  if     (isolationMode == "disabled")         fIsolationMode = kDisabled;
  else if(isolationMode == "standard")         fIsolationMode = kStandard;
  else if(isolationMode == "chargedHadrRel10") fIsolationMode = kChargedHadrRel10;
  else if(isolationMode == "chargedHadrRel15") fIsolationMode = kChargedHadrRel15;
  else if(isolationMode == "taulike")        fIsolationMode = kTauLike;
  else throw std::runtime_error("isolationMode is '"+isolationMode+"', allowed values are 'disabled', 'standard', 'chargedHadrRel10', 'chargedHadrRel15', 'taulike'");
}

EmbeddingMuonIsolationSelector::~EmbeddingMuonIsolationSelector() {}

TH1 *EmbeddingMuonIsolationSelector::makeEta(const char *name) { return makeTH<TH1F>(name, "Tau eta", 25, -2.5, 2.5); }
TH1 *EmbeddingMuonIsolationSelector::makePt(const char *name)  { return makeTH<TH1F>(name, "Tau pt", 25, 0, 250); }
TH1 *EmbeddingMuonIsolationSelector::makePhi(const char *name)  { return makeTH<TH1F>(name, "Tau phi", 32, -3.2, 3.2); }
TH1 *EmbeddingMuonIsolationSelector::makeRtau(const char *name)  { return makeTH<TH1F>(name, "Rtau", 10, 0.6, 1.1); }
TH1 *EmbeddingMuonIsolationSelector::makeVertexCount(const char *name) { return makeTH<TH1F>(name, "Vertex count", 30, 0, 30); }

void EmbeddingMuonIsolationSelector::setOutput(TDirectory *dir) {
  if(dir)
    dir->cd();

  hTauPt_AfterTauID = makePt("tauPt_AfterTauID");
  hTauEta_AfterTauID = makeEta("tauEta_AfterTauID");
  hTauPhi_AfterTauID = makePhi("tauPhi_AfterTauID");
  hTauLeadingTrackPt_AfterTauID = makePt("tauLeadingTrackPt_AfterTauID");
  hTauRtau_AfterTauID = makeRtau("tauRtau_AfterTauID");
  hVertexCount_AfterTauID = makeVertexCount("vertexCount_AfterTauID");

  hTauPt_AfterMuonIsolation = makePt("tauPt_AfterMuonIsolation");
  hTauEta_AfterMuonIsolation = makeEta("tauEta_AfterMuonIsolation");
  hTauPhi_AfterMuonIsolation = makePhi("tauPhi_AfterMuonIsolation");
  hTauLeadingTrackPt_AfterMuonIsolation = makePt("tauLeadingTrackPt_AfterMuonIsolation");
  hTauRtau_AfterMuonIsolation = makeRtau("tauRtau_AfterMuonIsolation");
  hVertexCount_AfterMuonIsolation = makeVertexCount("vertexCount_AfterMuonIsolation");

}

void EmbeddingMuonIsolationSelector::setupBranches(TTree *tree) {
  fEventInfo.setupBranches(tree);
  fMuons.setupBranches(tree, isMC());
  fTaus.setupBranches(tree);
  if(!fPuWeightName.empty())
    fPuWeight.setupBranch(tree, fPuWeightName.c_str());
  fVertexCount.setupBranch(tree, "goodPrimaryVertex_count");
}

bool EmbeddingMuonIsolationSelector::process(Long64_t entry) {
  fEventInfo.setEntry(entry);
  fMuons.setEntry(entry);
  fTaus.setEntry(entry);
  fPuWeight.setEntry(entry);
  fVertexCount.setEntry(entry);

  double weight = 1.0;
  if(!fPuWeightName.empty()) {
    weight *= fPuWeight.value();
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
 
    hTauPt_AfterTauID->Fill(tau.p4().Pt(), weight);
    hTauEta_AfterTauID->Fill(tau.p4().Eta(), weight);
    hTauPhi_AfterTauID->Fill(tau.p4().Phi(), weight);
    hTauLeadingTrackPt_AfterTauID->Fill(tau.leadPFChargedHadrCandP4().Pt(), weight);
    hTauRtau_AfterTauID->Fill(tau.rtau(), weight);

    selectedTaus.push_back(tau);
  }
  if(selectedTaus.empty()) return true;
  cTauID.increment();
  hVertexCount_AfterTauID->Fill(fVertexCount.value(), weight);

  // Muon isolation
  std::vector<EmbeddingMuonCollection::Muon> selectedMuons;
  for(size_t i=0; i<fMuons.size(); ++i) {
    EmbeddingMuonCollection::Muon muon = fMuons.get(i);
    if(fIsolationMode == kStandard  && !MuonID::standardRelativeIsolation(muon)) continue;
    if(fIsolationMode == kTauLike && !MuonID::embeddingIsolation(muon)) continue;
    if(fIsolationMode == kChargedHadrRel10 && !(muon.chargedHadronIso()/muon.p4().Pt() < 0.1)) continue;
    if(fIsolationMode == kChargedHadrRel15 && !(muon.chargedHadronIso()/muon.p4().Pt() < 0.15)) continue;
    selectedMuons.push_back(muon);
  }
  if(selectedMuons.empty()) return true;
  cMuonIsolation.increment();

  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];
    hTauPt_AfterMuonIsolation->Fill(tau.p4().Pt(), weight);
    hTauEta_AfterMuonIsolation->Fill(tau.p4().Eta(), weight);
    hTauPhi_AfterMuonIsolation->Fill(tau.p4().Phi(), weight);
    hTauLeadingTrackPt_AfterMuonIsolation->Fill(tau.leadPFChargedHadrCandP4().Pt(), weight);
    hTauRtau_AfterMuonIsolation->Fill(tau.rtau(), weight);
  }
  hVertexCount_AfterMuonIsolation->Fill(fVertexCount.value(), weight);

  return true;
}
