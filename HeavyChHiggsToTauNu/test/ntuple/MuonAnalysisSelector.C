#include "BaseSelector.h"
#include "Branches.h"

#include "TDirectory.h"
#include "TH1F.h"
#include "Math/VectorUtil.h"

#include<iostream>
#include<stdexcept>

class MyMuonCollection: public MuonCollection{
public:
  class Muon: public MuonCollection::Muon {
  public:
    Muon(MyMuonCollection *mc, size_t i): MuonCollection::Muon(mc, i) {}
    ~Muon() {}

    double chargedHadronIso_01to04() { return static_cast<MyMuonCollection *>(fCollection)->fChargedHadronIso_01to04.value()[fIndex]; }
    double puChargedHadronIso_01to04() { return static_cast<MyMuonCollection *>(fCollection)->fPuChargedHadronIso_01to04.value()[fIndex]; }
    double neutralHadronIso_01to04() { return static_cast<MyMuonCollection *>(fCollection)->fNeutralHadronIso_01to04.value()[fIndex]; }
    double photonIso_01to04() { return static_cast<MyMuonCollection *>(fCollection)->fPhotonIso_01to04.value()[fIndex]; }

    double standardRelativeIsolation() {
      return (chargedHadronIso() + std::max(0.0, photonIso() + neutralHadronIso() - 0.5*puChargedHadronIso()))/p4().Pt();
    }
    double embeddingIsolation() {
      return chargedHadronIso_01to04() + std::max(0.0, photonIso_01to04() - 0.5*puChargedHadronIso_01to04());
    }
  };

  MyMuonCollection() {}
  ~MyMuonCollection() {}

  void setupBranches(TTree *tree) {
    MuonCollection::setupBranches(tree);

    fChargedHadronIso_01to04.setupBranch(tree, (fPrefix+"_f_pfChargedHadrons_01to04").c_str());
    fPuChargedHadronIso_01to04.setupBranch(tree, (fPrefix+"_f_pfPUChargedHadrons_01to04").c_str());
    fNeutralHadronIso_01to04.setupBranch(tree, (fPrefix+"_f_pfNeutralHadrons_01to04").c_str());
    fPhotonIso_01to04.setupBranch(tree, (fPrefix+"_f_pfPhotons_01to04").c_str());
  }
  void setEntry(Long64_t entry) {
    MuonCollection::setEntry(entry);

    fChargedHadronIso_01to04.setEntry(entry);
    fPuChargedHadronIso_01to04.setEntry(entry);
    fNeutralHadronIso_01to04.setEntry(entry);
    fPhotonIso_01to04.setEntry(entry);
  }
  Muon get(size_t i) {
    return Muon(this, i);
  }

private:
  BranchObj<std::vector<double> > fChargedHadronIso_01to04;
  BranchObj<std::vector<double> > fPuChargedHadronIso_01to04;
  BranchObj<std::vector<double> > fNeutralHadronIso_01to04;
  BranchObj<std::vector<double> > fPhotonIso_01to04;
};

// MuonAnalysisSelector
class MuonAnalysisSelector: public BaseSelector {
public:
  MuonAnalysisSelector(const std::string& puWeight = "", const std::string& isolationMode="standard");
  ~MuonAnalysisSelector();

  void setOutput(TDirectory *dir);
  void setupBranches(TTree *tree);
  bool process(Long64_t entry);

private:
  // Input
  EventInfo fEventInfo;
  MyMuonCollection fMuons;
  JetCollection fJets;
  BranchObj<math::XYZTLorentzVector> fRawMet;

  std::string fPuWeightName;
  Branch<double> fPuWeight;

  Branch<bool> fElectronVetoPassed;

  enum IsolationMode {
    kDisabled,
    kStandard,
    kEmbedding
  };
  IsolationMode fIsolationMode;

  // Output
  // Counts
  EventCounter::Count cAll;
  EventCounter::Count cMuonKinematics;
  EventCounter::Count cMuonDB;
  EventCounter::Count cMuonIsolation;
  EventCounter::Count cMuonExactlyOne;
  EventCounter::Count cMuonVeto;
  EventCounter::Count cElectronVeto;
  EventCounter::Count cJetSelection;

  // Histograms
  TH1F *hMuonChargedHadronIso_AfterDB;
  TH1F *hMuonPuChargedHadronIso_AfterDB;
  TH1F *hMuonNeutralHadronIso_AfterDB;
  TH1F *hMuonPhotonIso_AfterDB;
  TH1F *hMuonIso_AfterDB;

  TH1F *hMuonEmbIso_AfterDB;
  TH1F *hMuonStdIso_AfterDB;

  TH1F *hSelectedMuonPt_AfterMuonSelection;
  TH1F *hSelectedMuonPt_AfterMuonVeto;
  TH1F *hSelectedMuonPt_AfterElectronVeto;
  TH1F *hSelectedMuonPt_AfterJetSelection;

  TH1F *hSelectedMuonChargedHadronEmbIso_AfterJetSelection;
  TH1F *hSelectedMuonPuChargedHadronEmbIso_AfterJetSelection;
  TH1F *hSelectedMuonNeutralHadronEmbIso_AfterJetSelection;
  TH1F *hSelectedMuonPhotonEmbIso_AfterJetSelection;
  TH1F *hSelectedMuonChargedHadronStdIso_AfterJetSelection;
  TH1F *hSelectedMuonPuChargedHadronStdIso_AfterJetSelection;
  TH1F *hSelectedMuonNeutralHadronStdIso_AfterJetSelection;
  TH1F *hSelectedMuonPhotonStdIso_AfterJetSelection;

  TH1F *hSelectedMuonEmbIso_AfterJetSelection;
  TH1F *hSelectedMuonStdIso_AfterJetSelection;

  TH1F *hRawMet_AfterJetSelection;
  TH1F *hTransverseMassRawMet_AfterJetSelection;
};

MuonAnalysisSelector::MuonAnalysisSelector(const std::string& puWeight, const std::string& isolationMode):
  BaseSelector(),
  fPuWeightName(puWeight),
  cAll(fEventCounter.addCounter("All events")),
  cMuonKinematics(fEventCounter.addCounter("Muon kinematics")),
  cMuonDB(fEventCounter.addCounter("Muon dB")),
  cMuonIsolation(fEventCounter.addCounter("Muon isolation")),
  cMuonExactlyOne(fEventCounter.addCounter("Muons == 1")),
  cMuonVeto(fEventCounter.addCounter("Veto additional muons")),
  cElectronVeto(fEventCounter.addCounter("Electron veto")),
  cJetSelection(fEventCounter.addCounter("Jet selection"))
{
  if(isolationMode == "disabled")
    fIsolationMode = kDisabled;
  else if(isolationMode == "standard")
    fIsolationMode = kStandard;
  else if(isolationMode == "embedding")
    fIsolationMode = kEmbedding;
  else
    throw std::runtime_error("isolationMode is '"+isolationMode+"', allowed values are 'disabled', 'standard', 'embedding'");
}
MuonAnalysisSelector::~MuonAnalysisSelector() {}

void MuonAnalysisSelector::setOutput(TDirectory *dir) {
  if(dir)
    dir->cd();

  hMuonChargedHadronIso_AfterDB = makeTH<TH1F>("muonChargedHadronIso_AfterDB", "", 50, 0, 5);
  hMuonPuChargedHadronIso_AfterDB = makeTH<TH1F>("muonPuChargedHadronIso_AfterDB", "", 50, 0, 5);
  hMuonNeutralHadronIso_AfterDB = makeTH<TH1F>("muonNeutralHadronIso_AfterDB", "", 50, 0, 5);
  hMuonPhotonIso_AfterDB = makeTH<TH1F>("muonPhotonIso_AfterDB", "", 50, 0, 5);
  hMuonIso_AfterDB = makeTH<TH1F>("muonIso_AfterDB", "", 50, 0, 5);

  hMuonEmbIso_AfterDB = makeTH<TH1F>("muonEmbIso_AfterDB", "", 50, 0, 5);
  hMuonStdIso_AfterDB = makeTH<TH1F>("muonStdIso_AfterDB", "", 50, 0, 5);

  hSelectedMuonPt_AfterMuonSelection = makeTH<TH1F>("selectedMuonPt_AfterMuonSelection", "Selected muon pt", 40, 0, 400);
  hSelectedMuonPt_AfterMuonVeto = makeTH<TH1F>("selectedMuonPt_AfterMuonVeto", "Selected muon pt", 40, 0, 400);
  hSelectedMuonPt_AfterElectronVeto = makeTH<TH1F>("selectedMuonPt_AfterElectronVeto", "Selected muon pt", 40, 0, 400);
  hSelectedMuonPt_AfterJetSelection = makeTH<TH1F>("selectedMuonPt_AfterJetSelection", "Selected muon pt", 40, 0, 400);

  hSelectedMuonChargedHadronEmbIso_AfterJetSelection = makeTH<TH1F>("selectedMuonChargedHadronEmbIso_AfterJetSelection", "", 50, 0, 5);
  hSelectedMuonPuChargedHadronEmbIso_AfterJetSelection = makeTH<TH1F>("selectedMuonPuChargedHadronEmbIso_AfterJetSelection", "", 50, 0, 5);
  hSelectedMuonNeutralHadronEmbIso_AfterJetSelection = makeTH<TH1F>("selectedMuonNeutralHadronEmbIso_AfterJetSelection", "", 50, 0, 5);
  hSelectedMuonPhotonEmbIso_AfterJetSelection = makeTH<TH1F>("selectedMuonPhotonEmbIso_AfterJetSelection", "", 50, 0, 5);
  hSelectedMuonChargedHadronStdIso_AfterJetSelection = makeTH<TH1F>("selectedMuonChargedHadronStdIso_AfterJetSelection", "", 50, 0, 5);
  hSelectedMuonPuChargedHadronStdIso_AfterJetSelection = makeTH<TH1F>("selectedMuonPuChargedHadronStdIso_AfterJetSelection", "", 50, 0, 5);
  hSelectedMuonNeutralHadronStdIso_AfterJetSelection = makeTH<TH1F>("selectedMuonNeutralHadronStdIso_AfterJetSelection", "", 50, 0, 5);
  hSelectedMuonPhotonStdIso_AfterJetSelection = makeTH<TH1F>("selectedMuonPhotonStdIso_AfterJetSelection", "", 50, 0, 5);

  hSelectedMuonEmbIso_AfterJetSelection = makeTH<TH1F>("selectedMuonEmbIso_AfterJetSelection", "", 50, 0, 5);
  hSelectedMuonStdIso_AfterJetSelection = makeTH<TH1F>("selectedMuonStdIso_AfterJetSelection", "", 50, 0, 5);

  hRawMet_AfterJetSelection = makeTH<TH1F>("uncorrectedMet_AfterJetSelection", "Uncorrected PF MET", 40, 0, 400);
  hTransverseMassRawMet_AfterJetSelection = makeTH<TH1F>("transverseMassUncorrectedMet_AfterJetSelection", "Transverse mass", 40, 0, 400);
}

void MuonAnalysisSelector::setupBranches(TTree *tree) {
  fEventInfo.setupBranches(tree);
  fMuons.setupBranches(tree);
  fJets.setupBranches(tree);
  if(!fPuWeightName.empty())
    fPuWeight.setupBranch(tree, fPuWeightName.c_str());
  fElectronVetoPassed.setupBranch(tree, "ElectronVetoPassed");
  fRawMet.setupBranch(tree, "pfMet_p4");
}

bool MuonAnalysisSelector::process(Long64_t entry) {
  fEventInfo.setEntry(entry);
  fMuons.setEntry(entry);
  fJets.setEntry(entry);
  fPuWeight.setEntry(entry);
  fElectronVetoPassed.setEntry(entry);
  fRawMet.setEntry(entry);

  double weight = 1.0;
  if(!fPuWeightName.empty()) {
    weight *= fPuWeight.value();
  }
  fEventCounter.setWeight(weight);

  cAll.increment();

  size_t nmuons = fMuons.size();
  std::vector<MyMuonCollection::Muon> selectedMuons;
  std::vector<MyMuonCollection::Muon> tmp;

  // Muon kinematics
  for(size_t i=0; i<nmuons; ++i) {
    MyMuonCollection::Muon muon = fMuons.get(i);
    if(!(muon.p4().Pt() > 40)) continue;
    if(!(std::abs(muon.p4().Eta()) < 2.1)) continue;
    selectedMuons.push_back(muon);
  }

  if(selectedMuons.empty()) return true;
  cMuonKinematics.increment();

  // dB
  for(size_t i=0; i<selectedMuons.size(); ++i) {
    if(!(selectedMuons[i].dB() < 0.02)) continue;
    tmp.push_back(selectedMuons[i]);
  }
  selectedMuons.swap(tmp);
  tmp.clear();
  if(selectedMuons.empty()) return true;
  cMuonDB.increment();

  // Isolation
  if(fIsolationMode != kDisabled) {
    for(size_t i=0; i<selectedMuons.size(); ++i) {
      MyMuonCollection::Muon& muon = selectedMuons[i];

      double stdIsoVar = muon.standardRelativeIsolation();
      double embIsoVar = muon.embeddingIsolation();
      hMuonStdIso_AfterDB->Fill(stdIsoVar, weight);
      hMuonEmbIso_AfterDB->Fill(embIsoVar, weight);

      if(fIsolationMode == kStandard) {
        hMuonChargedHadronIso_AfterDB->Fill(muon.chargedHadronIso(), weight);
        hMuonPuChargedHadronIso_AfterDB->Fill(muon.puChargedHadronIso(), weight);
        hMuonNeutralHadronIso_AfterDB->Fill(muon.neutralHadronIso(), weight);
        hMuonPhotonIso_AfterDB->Fill(muon.photonIso(), weight);
        hMuonIso_AfterDB->Fill(stdIsoVar, weight);

        if(!(stdIsoVar < 0.12)) continue;
      }
      else if(fIsolationMode == kEmbedding) {

        hMuonChargedHadronIso_AfterDB->Fill(muon.chargedHadronIso_01to04(), weight);
        hMuonPuChargedHadronIso_AfterDB->Fill(muon.puChargedHadronIso_01to04(), weight);
        hMuonNeutralHadronIso_AfterDB->Fill(muon.neutralHadronIso_01to04(), weight);
        hMuonPhotonIso_AfterDB->Fill(muon.photonIso_01to04(), weight);
        hMuonIso_AfterDB->Fill(embIsoVar, weight);

        if(!(embIsoVar < 2)) continue;
      }
      tmp.push_back(muon);
    }
    selectedMuons.swap(tmp);
    tmp.clear();
    if(selectedMuons.empty()) return true;
  }
  cMuonIsolation.increment();

  // Exactly one selected muon
  if(selectedMuons.size() != 1) return true;
  cMuonExactlyOne.increment();

  MyMuonCollection::Muon& selectedMuon = selectedMuons[0];
  // Fill
  hSelectedMuonPt_AfterMuonSelection->Fill(selectedMuon.p4().Pt(), weight);

  // Muon veto
  int muonVetoCount = 0;
  for(size_t i=0; i<nmuons; ++i) {
    MyMuonCollection::Muon muon = fMuons.get(i);

    // Skip selected muon
    if(muon.index() == selectedMuon.index()) continue;

    if(!(muon.p4().Pt() > 15)) continue;
    if(!(std::abs(muon.p4().Eta()) < 2.5)) continue;
    if(!(muon.dB() < 0.02)) continue;
    double isoVar = muon.trackIso()+muon.caloIso();
    isoVar = isoVar / muon.p4().Pt();
    if(!(isoVar <= 0.15)) continue;
    ++muonVetoCount;
  }
  if(muonVetoCount > 0) return true;
  cMuonVeto.increment();
  // Fill
  hSelectedMuonPt_AfterMuonVeto->Fill(selectedMuon.p4().Pt(), weight);


  // Electron veto
  if(!fElectronVetoPassed.value()) return true;
  cElectronVeto.increment();
  // Fill
  hSelectedMuonPt_AfterElectronVeto->Fill(selectedMuon.p4().Pt(), weight);

  // Jet selection
  size_t njets = fJets.size();
  size_t nselectedjets = 0;
  for(size_t i=0; i<njets; ++i) {
    JetCollection::Jet jet = fJets.get(i);

    // Clean selected muon from jet collection
    double DR = ROOT::Math::VectorUtil::DeltaR(selectedMuon.p4(), jet.p4());
    if(DR < 0.1) continue;

    // Count jets
    ++nselectedjets;
  }
  if(nselectedjets < 3) return true;
  cJetSelection.increment();

  // Fill
  hSelectedMuonPt_AfterJetSelection->Fill(selectedMuon.p4().Pt(), weight);

  hSelectedMuonChargedHadronEmbIso_AfterJetSelection->Fill(selectedMuon.chargedHadronIso_01to04(), weight);
  hSelectedMuonPuChargedHadronEmbIso_AfterJetSelection->Fill(selectedMuon.puChargedHadronIso_01to04(), weight);
  hSelectedMuonNeutralHadronEmbIso_AfterJetSelection->Fill(selectedMuon.neutralHadronIso_01to04(), weight);
  hSelectedMuonPhotonEmbIso_AfterJetSelection->Fill(selectedMuon.photonIso_01to04(), weight);

  hSelectedMuonChargedHadronStdIso_AfterJetSelection->Fill(selectedMuon.chargedHadronIso(), weight);
  hSelectedMuonPuChargedHadronStdIso_AfterJetSelection->Fill(selectedMuon.puChargedHadronIso(), weight);
  hSelectedMuonNeutralHadronStdIso_AfterJetSelection->Fill(selectedMuon.neutralHadronIso(), weight);
  hSelectedMuonPhotonStdIso_AfterJetSelection->Fill(selectedMuon.photonIso(), weight);

  hSelectedMuonEmbIso_AfterJetSelection->Fill(selectedMuon.embeddingIsolation(), weight);
  hSelectedMuonStdIso_AfterJetSelection->Fill(selectedMuon.standardRelativeIsolation(), weight);

  hRawMet_AfterJetSelection->Fill(fRawMet.value().Pt(), weight);

  double transverseMass = std::sqrt(2 * selectedMuon.p4().Pt() * fRawMet.value().Pt() * (1-std::cos(selectedMuon.p4().Phi()-fRawMet.value().Phi())));
  hTransverseMassRawMet_AfterJetSelection->Fill(transverseMass, weight);

  return true;
}

