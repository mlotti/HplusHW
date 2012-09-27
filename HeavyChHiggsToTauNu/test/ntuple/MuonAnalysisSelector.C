#include "BaseSelector.h"
#include "Branches.h"
#include "Configuration.h"

#include "TDirectory.h"
#include "TH1F.h"
#include "Math/VectorUtil.h"

#include<iostream>
#include<stdexcept>
#include<cstdlib>

class MyMuonCollection: public MuonCollection{
public:
  class Muon: public MuonCollection::Muon {
  public:
    Muon(MyMuonCollection *mc, size_t i): MuonCollection::Muon(mc, i) {}
    ~Muon() {}

    double chargedHadronIsoEmb() { return static_cast<MyMuonCollection *>(fCollection)->fChargedHadronIsoEmb.value()[fIndex]; }
    double puChargedHadronIsoEmb() { return static_cast<MyMuonCollection *>(fCollection)->fPuChargedHadronIsoEmb.value()[fIndex]; }
    double neutralHadronIsoEmb() { return static_cast<MyMuonCollection *>(fCollection)->fNeutralHadronIsoEmb.value()[fIndex]; }
    double photonIsoEmb() { return static_cast<MyMuonCollection *>(fCollection)->fPhotonIsoEmb.value()[fIndex]; }

    double standardRelativeIsolation() {
      return (chargedHadronIso() + std::max(0.0, photonIso() + neutralHadronIso() - 0.5*puChargedHadronIso()))/p4().Pt();
    }
    double embeddingIsolation() {
      return chargedHadronIsoEmb() + std::max(0.0, photonIsoEmb() - 0.5*puChargedHadronIsoEmb());
    }
  };

  MyMuonCollection() {}
  ~MyMuonCollection() {}

  void setupBranches(TTree *tree, bool isMC) {
    MuonCollection::setupBranches(tree, isMC);

    fChargedHadronIsoEmb.setupBranch(tree, (fPrefix+"_f_chargedHadronIsoEmb").c_str());
    fPuChargedHadronIsoEmb.setupBranch(tree, (fPrefix+"_f_puChargedHadronIsoEmb").c_str());
    fNeutralHadronIsoEmb.setupBranch(tree, (fPrefix+"_f_neutralHadronIsoEmb").c_str());
    fPhotonIsoEmb.setupBranch(tree, (fPrefix+"_f_photonIsoEmb").c_str());
  }
  void setEntry(Long64_t entry) {
    MuonCollection::setEntry(entry);

    fChargedHadronIsoEmb.setEntry(entry);
    fPuChargedHadronIsoEmb.setEntry(entry);
    fNeutralHadronIsoEmb.setEntry(entry);
    fPhotonIsoEmb.setEntry(entry);
  }
  Muon get(size_t i) {
    return Muon(this, i);
  }

private:
  BranchObj<std::vector<double> > fChargedHadronIsoEmb;
  BranchObj<std::vector<double> > fPuChargedHadronIsoEmb;
  BranchObj<std::vector<double> > fNeutralHadronIsoEmb;
  BranchObj<std::vector<double> > fPhotonIsoEmb;
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
  Branch<unsigned> fVertexCount;

  Branch<bool> fElectronVetoPassed;
  Branch<bool> fHBHENoiseFilterPassed;

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
  EventCounter::Count cHBHENoiseFilter;
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

  TH1F *hMuonVertexCount_AfterDB;
  TH1F *hMuonVertexCount_AfterDB_MuFromW;

  TH1F *hMuonVertexCount_AfterIsolation;
  TH1F *hMuonVertexCount_AfterIsolation_MuFromW;

  TH1F *hSelectedMuonPt_AfterMuonSelection;
  TH1F *hSelectedMuonPt_AfterMuonVeto;
  TH1F *hSelectedMuonPt_AfterElectronVeto;
  TH1F *hSelectedMuonPt_AfterJetSelection;
  TH1F *hSelectedMuonPt_AfterJetSelection_Unweighted;

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

  TH1F *hSelectedMuonPt_AfterJetSelection_MuFromW;
  TH1F *hSelectedMuonPt_AfterJetSelection_MuFromTauFromW;
  TH1F *hSelectedMuonPt_AfterJetSelection_MuOther;

  TH1F *hSelectedMuonPt_AfterJetSelection_MuFromW_Unweighted;
  TH1F *hSelectedMuonPt_AfterJetSelection_MuFromTauFromW_Unweighted;
  TH1F *hSelectedMuonPt_AfterJetSelection_MuOther_Unweighted;

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
  cHBHENoiseFilter(fEventCounter.addCounter("HBHE noise filter (data)")), // Here only because it's here in the current embedding+signalAnalysis workflow
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

  hMuonVertexCount_AfterDB = makeTH<TH1F>("muonVertexCount_AfterDB", "", 50, 0, 50);
  hMuonVertexCount_AfterDB_MuFromW = makeTH<TH1F>("muonVertexCount_AfterDB_MuFromW", "", 50, 0, 50);

  hMuonVertexCount_AfterIsolation = makeTH<TH1F>("muonVertexCount_AfterIsolation", "", 50, 0, 50);
  hMuonVertexCount_AfterIsolation_MuFromW = makeTH<TH1F>("muonVertexCount_AfterIsolation_MuFromW", "", 50, 0, 50);

  hSelectedMuonPt_AfterMuonSelection = makeTH<TH1F>("selectedMuonPt_AfterMuonSelection", "Selected muon pt", 40, 0, 400);
  hSelectedMuonPt_AfterMuonVeto = makeTH<TH1F>("selectedMuonPt_AfterMuonVeto", "Selected muon pt", 40, 0, 400);
  hSelectedMuonPt_AfterElectronVeto = makeTH<TH1F>("selectedMuonPt_AfterElectronVeto", "Selected muon pt", 40, 0, 400);
  hSelectedMuonPt_AfterJetSelection = makeTH<TH1F>("selectedMuonPt_AfterJetSelection", "Selected muon pt", 40, 0, 400);
  hSelectedMuonPt_AfterJetSelection_Unweighted = makeTH<TH1F>("selectedMuonPt_AfterJetSelection_Unweighted", "Selected muon pt", 40, 0, 400);

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

  hSelectedMuonPt_AfterJetSelection_MuFromW = makeTH<TH1F>("selectedMuonPt_AfterJetSelection_MuFromW", "Selected muon pt", 40, 0, 400);
  hSelectedMuonPt_AfterJetSelection_MuFromTauFromW = makeTH<TH1F>("selectedMuonPt_AfterJetSelection_MuFromTauFromW", "Selected muon pt", 40, 0, 400);
  hSelectedMuonPt_AfterJetSelection_MuOther = makeTH<TH1F>("selectedMuonPt_AfterJetSelection_MuOther", "Selected muon pt", 40, 0, 400);
  hSelectedMuonPt_AfterJetSelection_MuFromW_Unweighted = makeTH<TH1F>("selectedMuonPt_AfterJetSelection_MuFromW_Unweighted", "Selected muon pt", 40, 0, 400);
  hSelectedMuonPt_AfterJetSelection_MuFromTauFromW_Unweighted = makeTH<TH1F>("selectedMuonPt_AfterJetSelection_MuFromTauFromW_Unweighted", "Selected muon pt", 40, 0, 400);
  hSelectedMuonPt_AfterJetSelection_MuOther_Unweighted = makeTH<TH1F>("selectedMuonPt_AfterJetSelection_MuOther_Unweighted", "Selected muon pt", 40, 0, 400);

  hRawMet_AfterJetSelection = makeTH<TH1F>("uncorrectedMet_AfterJetSelection", "Uncorrected PF MET", 40, 0, 400);
  hTransverseMassRawMet_AfterJetSelection = makeTH<TH1F>("transverseMassUncorrectedMet_AfterJetSelection", "Transverse mass", 40, 0, 400);
}

void MuonAnalysisSelector::setupBranches(TTree *tree) {
  fEventInfo.setupBranches(tree);
  fMuons.setupBranches(tree, isMC());
  fJets.setupBranches(tree);
  if(!fPuWeightName.empty())
    fPuWeight.setupBranch(tree, fPuWeightName.c_str());
  fVertexCount.setupBranch(tree, "vertexCount");
  fElectronVetoPassed.setupBranch(tree, "ElectronVetoPassed");
  if(isData())
    fHBHENoiseFilterPassed.setupBranch(tree, "HBHENoiseFilter");
  fRawMet.setupBranch(tree, "pfMet_p4");
}

bool MuonAnalysisSelector::process(Long64_t entry) {
  fEventInfo.setEntry(entry);
  fMuons.setEntry(entry);
  fJets.setEntry(entry);
  fPuWeight.setEntry(entry);
  fVertexCount.setEntry(entry);
  fElectronVetoPassed.setEntry(entry);
  fHBHENoiseFilterPassed.setEntry(entry);
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
    if(!MuonID::pt(muon)) continue;
    if(!MuonID::eta(muon)) continue;
    selectedMuons.push_back(muon);
  }

  if(selectedMuons.empty()) return true;
  cMuonKinematics.increment();

  // dB
  for(size_t i=0; i<selectedMuons.size(); ++i) {
    if(!MuonID::dB(selectedMuons[i])) continue;
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

      hMuonVertexCount_AfterDB->Fill(fVertexCount.value(), weight);
      bool isMuFromW = isMC() && std::abs(muon.pdgId()) == 13 && std::abs(muon.motherPdgId()) == 24;
      if(isMuFromW)
        hMuonVertexCount_AfterDB_MuFromW->Fill(fVertexCount.value(), weight);

      if(fIsolationMode == kStandard) {
        hMuonChargedHadronIso_AfterDB->Fill(muon.chargedHadronIso(), weight);
        hMuonPuChargedHadronIso_AfterDB->Fill(muon.puChargedHadronIso(), weight);
        hMuonNeutralHadronIso_AfterDB->Fill(muon.neutralHadronIso(), weight);
        hMuonPhotonIso_AfterDB->Fill(muon.photonIso(), weight);
        hMuonIso_AfterDB->Fill(stdIsoVar, weight);

        if(!MuonID::standardRelativeIsolation(stdIsoVar)) continue;
      }
      else if(fIsolationMode == kEmbedding) {

        hMuonChargedHadronIso_AfterDB->Fill(muon.chargedHadronIsoEmb(), weight);
        hMuonPuChargedHadronIso_AfterDB->Fill(muon.puChargedHadronIsoEmb(), weight);
        hMuonNeutralHadronIso_AfterDB->Fill(muon.neutralHadronIsoEmb(), weight);
        hMuonPhotonIso_AfterDB->Fill(muon.photonIsoEmb(), weight);
        hMuonIso_AfterDB->Fill(embIsoVar, weight);

        if(!MuonID::embeddingIsolation(embIsoVar)) continue;
      }
      hMuonVertexCount_AfterIsolation->Fill(fVertexCount.value(), weight);
      if(isMuFromW)
        hMuonVertexCount_AfterIsolation_MuFromW->Fill(fVertexCount.value(), weight);

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

  // HBHENoiseFilter
  if(isData() && !fHBHENoiseFilterPassed.value()) return true;
  cHBHENoiseFilter.increment();

  // Muon veto
  int muonVetoCount = 0;
  for(size_t i=0; i<nmuons; ++i) {
    MyMuonCollection::Muon muon = fMuons.get(i);
    // Skip selected muon
    if(muon.index() == selectedMuon.index()) continue;

    if(!MuonVeto::pt(muon)) continue;
    if(!MuonVeto::eta(muon)) continue;
    if(!MuonVeto::dB(muon)) continue;
    if(!MuonVeto::subdetectorIsolation(muon)) continue;
    ++muonVetoCount;

    /*
    std::cout << "Event " << fEventInfo.event() << ":" << fEventInfo.lumi() << ":" << fEventInfo.run()
              << " muon pt " << muon.p4().Pt() << " eta " << muon.p4().Eta() << " phi " << muon.p4().Phi()
              << std::endl;
    */
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
  hSelectedMuonPt_AfterJetSelection_Unweighted->Fill(selectedMuon.p4().Pt());

  hSelectedMuonChargedHadronEmbIso_AfterJetSelection->Fill(selectedMuon.chargedHadronIsoEmb(), weight);
  hSelectedMuonPuChargedHadronEmbIso_AfterJetSelection->Fill(selectedMuon.puChargedHadronIsoEmb(), weight);
  hSelectedMuonNeutralHadronEmbIso_AfterJetSelection->Fill(selectedMuon.neutralHadronIsoEmb(), weight);
  hSelectedMuonPhotonEmbIso_AfterJetSelection->Fill(selectedMuon.photonIsoEmb(), weight);

  hSelectedMuonChargedHadronStdIso_AfterJetSelection->Fill(selectedMuon.chargedHadronIso(), weight);
  hSelectedMuonPuChargedHadronStdIso_AfterJetSelection->Fill(selectedMuon.puChargedHadronIso(), weight);
  hSelectedMuonNeutralHadronStdIso_AfterJetSelection->Fill(selectedMuon.neutralHadronIso(), weight);
  hSelectedMuonPhotonStdIso_AfterJetSelection->Fill(selectedMuon.photonIso(), weight);

  hSelectedMuonEmbIso_AfterJetSelection->Fill(selectedMuon.embeddingIsolation(), weight);
  hSelectedMuonStdIso_AfterJetSelection->Fill(selectedMuon.standardRelativeIsolation(), weight);

  if(isMC()) {
    //std::cout << selectedMuon.pdgId() << " " << selectedMuon.motherPdgId() << " " << selectedMuon.grandMotherPdgId() << std::endl;
    if(std::abs(selectedMuon.pdgId()) == 13) {
      if(std::abs(selectedMuon.motherPdgId()) == 24) {
        hSelectedMuonPt_AfterJetSelection_MuFromW->Fill(selectedMuon.p4().Pt(), weight);
        hSelectedMuonPt_AfterJetSelection_MuFromW_Unweighted->Fill(selectedMuon.p4().Pt());
      }
      else if(std::abs(selectedMuon.motherPdgId()) == 15 && std::abs(selectedMuon.grandMotherPdgId()) == 24)
        hSelectedMuonPt_AfterJetSelection_MuFromTauFromW->Fill(selectedMuon.p4().Pt(), weight);
        hSelectedMuonPt_AfterJetSelection_MuFromTauFromW_Unweighted->Fill(selectedMuon.p4().Pt());
    }
    else {
      hSelectedMuonPt_AfterJetSelection_MuOther->Fill(selectedMuon.p4().Pt(), weight);
      hSelectedMuonPt_AfterJetSelection_MuOther_Unweighted->Fill(selectedMuon.p4().Pt());
    }
  }

  hRawMet_AfterJetSelection->Fill(fRawMet.value().Pt(), weight);

  double transverseMass = std::sqrt(2 * selectedMuon.p4().Pt() * fRawMet.value().Pt() * (1-std::cos(selectedMuon.p4().Phi()-fRawMet.value().Phi())));
  hTransverseMassRawMet_AfterJetSelection->Fill(transverseMass, weight);

  return true;
}

