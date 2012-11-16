#include "BaseSelector.h"
#include "Branches.h"
#include "Configuration.h"

#include "TDirectory.h"
#include "TH1F.h"
#include "Math/VectorUtil.h"

#include<iostream>
#include<stdexcept>
#include<cstdlib>


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
  EmbeddingMuonCollection fMuons;
  //ElectronCollection fElectrons;
  JetCollection fJets;
  BranchObj<math::XYZTLorentzVector> fRawMet;

  std::string fPuWeightName;
  Branch<double> fPuWeight;
  Branch<unsigned> fSelectedVertexCount;
  Branch<unsigned> fVertexCount;

  Branch<bool> fElectronVetoPassed;
  Branch<bool> fHBHENoiseFilterPassed;

  EmbeddingMuonIsolation::Mode fIsolationMode;

  TH1 *makePt(const char *name);
  TH1 *makeIso(const char *name);
  TH1 *makeVertexCount(const char *name);

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
  TH1 *hMuonChargedHadronIso_AfterDB;
  TH1 *hMuonPuChargedHadronIso_AfterDB;
  TH1 *hMuonNeutralHadronIso_AfterDB;
  TH1 *hMuonPhotonIso_AfterDB;
  TH1 *hMuonIso_AfterDB;

  TH1 *hMuonEmbIso_AfterDB;
  TH1 *hMuonStdIso_AfterDB;

  TH1 *hMuonVertexCount_AfterDB;
  TH1 *hMuonVertexCount_AfterDB_MuFromW;

  TH1 *hMuonVertexCount_AfterIsolation;
  TH1 *hMuonVertexCount_AfterIsolation_MuFromW;

  TH1 *hSelectedMuonPt_AfterMuonSelection;
  TH1 *hSelectedMuonPt_AfterMuonVeto;
  TH1 *hSelectedMuonPt_AfterElectronVeto;
  TH1 *hSelectedMuonPt_AfterJetSelection;
  TH1 *hSelectedMuonPt_AfterJetSelection_Unweighted;

  TH1 *hSelectedMuonChargedHadronEmbIso_AfterJetSelection;
  TH1 *hSelectedMuonPuChargedHadronEmbIso_AfterJetSelection;
  TH1 *hSelectedMuonNeutralHadronEmbIso_AfterJetSelection;
  TH1 *hSelectedMuonPhotonEmbIso_AfterJetSelection;
  TH1 *hSelectedMuonChargedHadronStdIso_AfterJetSelection;
  TH1 *hSelectedMuonPuChargedHadronStdIso_AfterJetSelection;
  TH1 *hSelectedMuonNeutralHadronStdIso_AfterJetSelection;
  TH1 *hSelectedMuonPhotonStdIso_AfterJetSelection;

  TH1 *hSelectedMuonEmbIso_AfterJetSelection;
  TH1 *hSelectedMuonStdIso_AfterJetSelection;

  TH1 *hSelectedMuonPt_AfterJetSelection_MuFromW;
  TH1 *hSelectedMuonPt_AfterJetSelection_MuFromTauFromW;
  TH1 *hSelectedMuonPt_AfterJetSelection_MuOther;

  TH1 *hSelectedMuonPt_AfterJetSelection_MuFromW_Unweighted;
  TH1 *hSelectedMuonPt_AfterJetSelection_MuFromTauFromW_Unweighted;
  TH1 *hSelectedMuonPt_AfterJetSelection_MuOther_Unweighted;

  TH1 *hRawMet_AfterJetSelection;
  TH1 *hTransverseMassRawMet_AfterJetSelection;
  TH1 *hVertexCount_AfterJetSelection;
};

MuonAnalysisSelector::MuonAnalysisSelector(const std::string& puWeight, const std::string& isolationMode):
  BaseSelector(),
  fPuWeightName(puWeight),
  fIsolationMode(EmbeddingMuonIsolation::stringToMode(isolationMode)),
  cAll(fEventCounter.addCounter("All events")),
  cMuonKinematics(fEventCounter.addCounter("Muon kinematics")),
  cMuonDB(fEventCounter.addCounter("Muon dB")),
  cMuonIsolation(fEventCounter.addCounter("Muon isolation")),
  cMuonExactlyOne(fEventCounter.addCounter("Muons == 1")),
  cHBHENoiseFilter(fEventCounter.addCounter("HBHE noise filter (data)")), // Here only because it's here in the current embedding+signalAnalysis workflow
  cMuonVeto(fEventCounter.addCounter("Veto additional muons")),
  cElectronVeto(fEventCounter.addCounter("Electron veto")),
  cJetSelection(fEventCounter.addCounter("Jet selection"))
{}
MuonAnalysisSelector::~MuonAnalysisSelector() {}

TH1 *MuonAnalysisSelector::makePt(const char *name) { return makeTH<TH1F>(name, "Muon pt", 40, 0, 400); }
TH1 *MuonAnalysisSelector::makeIso(const char *name) { return makeTH<TH1F>(name, "Muon isolation", 50, 0, 5); }
TH1 *MuonAnalysisSelector::makeVertexCount(const char *name) { return makeTH<TH1F>(name, "Vertex count", 30, 0, 30); }

void MuonAnalysisSelector::setOutput(TDirectory *dir) {
  if(dir)
    dir->cd();

  hMuonChargedHadronIso_AfterDB = makeIso("muonChargedHadronIso_AfterDB");
  hMuonPuChargedHadronIso_AfterDB = makeIso("muonPuChargedHadronIso_AfterDB");
  hMuonNeutralHadronIso_AfterDB = makeIso("muonNeutralHadronIso_AfterDB");
  hMuonPhotonIso_AfterDB = makeIso("muonPhotonIso_AfterDB");
  hMuonIso_AfterDB = makeIso("muonIso_AfterDB");

  hMuonEmbIso_AfterDB = makeIso("muonEmbIso_AfterDB");
  hMuonStdIso_AfterDB = makeIso("muonStdIso_AfterDB");

  hMuonVertexCount_AfterDB = makeVertexCount("muonVertexCount_AfterDB");
  hMuonVertexCount_AfterDB_MuFromW = makeVertexCount("muonVertexCount_AfterDB_MuFromW");

  hMuonVertexCount_AfterIsolation = makeVertexCount("muonVertexCount_AfterIsolation");
  hMuonVertexCount_AfterIsolation_MuFromW = makeVertexCount("muonVertexCount_AfterIsolation_MuFromW");

  hSelectedMuonPt_AfterMuonSelection = makePt("selectedMuonPt_AfterMuonSelection");
  hSelectedMuonPt_AfterMuonVeto = makePt("selectedMuonPt_AfterMuonVeto");
  hSelectedMuonPt_AfterElectronVeto = makePt("selectedMuonPt_AfterElectronVeto");
  hSelectedMuonPt_AfterJetSelection = makePt("selectedMuonPt_AfterJetSelection");
  hSelectedMuonPt_AfterJetSelection_Unweighted = makePt("selectedMuonPt_AfterJetSelection_Unweighted");

  hSelectedMuonChargedHadronEmbIso_AfterJetSelection = makeIso("selectedMuonChargedHadronEmbIso_AfterJetSelection");
  hSelectedMuonPuChargedHadronEmbIso_AfterJetSelection = makeIso("selectedMuonPuChargedHadronEmbIso_AfterJetSelection");
  hSelectedMuonNeutralHadronEmbIso_AfterJetSelection = makeIso("selectedMuonNeutralHadronEmbIso_AfterJetSelection");
  hSelectedMuonPhotonEmbIso_AfterJetSelection = makeIso("selectedMuonPhotonEmbIso_AfterJetSelection");
  hSelectedMuonChargedHadronStdIso_AfterJetSelection = makeIso("selectedMuonChargedHadronStdIso_AfterJetSelection");
  hSelectedMuonPuChargedHadronStdIso_AfterJetSelection = makeIso("selectedMuonPuChargedHadronStdIso_AfterJetSelection");
  hSelectedMuonNeutralHadronStdIso_AfterJetSelection = makeIso("selectedMuonNeutralHadronStdIso_AfterJetSelection");
  hSelectedMuonPhotonStdIso_AfterJetSelection = makeIso("selectedMuonPhotonStdIso_AfterJetSelection");

  hSelectedMuonEmbIso_AfterJetSelection = makeIso("selectedMuonEmbIso_AfterJetSelection");
  hSelectedMuonStdIso_AfterJetSelection = makeIso("selectedMuonStdIso_AfterJetSelection");

  hSelectedMuonPt_AfterJetSelection_MuFromW = makePt("selectedMuonPt_AfterJetSelection_MuFromW");
  hSelectedMuonPt_AfterJetSelection_MuFromTauFromW = makePt("selectedMuonPt_AfterJetSelection_MuFromTauFromW");
  hSelectedMuonPt_AfterJetSelection_MuOther = makePt("selectedMuonPt_AfterJetSelection_MuOther");
  hSelectedMuonPt_AfterJetSelection_MuFromW_Unweighted = makePt("selectedMuonPt_AfterJetSelection_MuFromW_Unweighted");
  hSelectedMuonPt_AfterJetSelection_MuFromTauFromW_Unweighted = makePt("selectedMuonPt_AfterJetSelection_MuFromTauFromW_Unweighted");
  hSelectedMuonPt_AfterJetSelection_MuOther_Unweighted = makePt("selectedMuonPt_AfterJetSelection_MuOther_Unweighted");

  hRawMet_AfterJetSelection = makeTH<TH1F>("uncorrectedMet_AfterJetSelection", "Uncorrected PF MET", 40, 0, 400);
  hTransverseMassRawMet_AfterJetSelection = makeTH<TH1F>("transverseMassUncorrectedMet_AfterJetSelection", "Transverse mass", 40, 0, 400);
  hVertexCount_AfterJetSelection = makeVertexCount("vertexCount_AfterJetSelection");
}

void MuonAnalysisSelector::setupBranches(TTree *tree) {
  fEventInfo.setupBranches(tree);
  fMuons.setupBranches(tree, isMC());
  //fElectrons.setupBranches(tree, isMC());
  fJets.setupBranches(tree);
  if(!fPuWeightName.empty())
    fPuWeight.setupBranch(tree, fPuWeightName.c_str());
  fSelectedVertexCount.setupBranch(tree, "selectedPrimaryVertex_count");
  fVertexCount.setupBranch(tree, "goodPrimaryVertex_count");
  //fVertexCount.setupBranch(tree, "vertex_count");
  fElectronVetoPassed.setupBranch(tree, "ElectronVetoPassed");
  if(isData())
    fHBHENoiseFilterPassed.setupBranch(tree, "HBHENoiseFilter");
  fRawMet.setupBranch(tree, "pfMet_p4");
}

bool MuonAnalysisSelector::process(Long64_t entry) {
  fEventInfo.setEntry(entry);
  fMuons.setEntry(entry);
  //fElectrons.setEntry(entry);
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
  std::vector<EmbeddingMuonCollection::Muon> selectedMuons;
  std::vector<EmbeddingMuonCollection::Muon> tmp;

  // Muon kinematics
  for(size_t i=0; i<nmuons; ++i) {
    EmbeddingMuonCollection::Muon muon = fMuons.get(i);
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
  if(fIsolationMode != EmbeddingMuonIsolation::kDisabled) {
    for(size_t i=0; i<selectedMuons.size(); ++i) {
      EmbeddingMuonCollection::Muon& muon = selectedMuons[i];

      double stdIsoVar = muon.standardRelativeIsolation();
      double embIsoVar = muon.tauLikeIsolation();
      hMuonStdIso_AfterDB->Fill(stdIsoVar, weight);
      hMuonEmbIso_AfterDB->Fill(embIsoVar, weight);

      hMuonVertexCount_AfterDB->Fill(fVertexCount.value(), weight);
      bool isMuFromW = isMC() && std::abs(muon.pdgId()) == 13 && std::abs(muon.motherPdgId()) == 24;
      if(isMuFromW)
        hMuonVertexCount_AfterDB_MuFromW->Fill(fVertexCount.value(), weight);

      if(fIsolationMode == EmbeddingMuonIsolation::kStandard) {
        hMuonChargedHadronIso_AfterDB->Fill(muon.chargedHadronIso(), weight);
        hMuonPuChargedHadronIso_AfterDB->Fill(muon.puChargedHadronIso(), weight);
        hMuonNeutralHadronIso_AfterDB->Fill(muon.neutralHadronIso(), weight);
        hMuonPhotonIso_AfterDB->Fill(muon.photonIso(), weight);
        hMuonIso_AfterDB->Fill(stdIsoVar, weight);

        if(!MuonID::standardRelativeIsolationCut(stdIsoVar)) continue;
      }
      else if(fIsolationMode == EmbeddingMuonIsolation::kTauLike) {

        hMuonChargedHadronIso_AfterDB->Fill(muon.chargedHadronIsoEmb(), weight);
        hMuonPuChargedHadronIso_AfterDB->Fill(muon.puChargedHadronIsoEmb(), weight);
        hMuonNeutralHadronIso_AfterDB->Fill(muon.neutralHadronIsoEmb(), weight);
        hMuonPhotonIso_AfterDB->Fill(muon.photonIsoEmb(), weight);
        hMuonIso_AfterDB->Fill(embIsoVar, weight);

        if(!MuonID::tauLikeIsolationCut(embIsoVar)) continue;
      }
      else if(fIsolationMode == EmbeddingMuonIsolation::kChargedHadrRel10) {
        hMuonChargedHadronIso_AfterDB->Fill(muon.chargedHadronIso(), weight);
        hMuonPuChargedHadronIso_AfterDB->Fill(muon.puChargedHadronIso(), weight);
        hMuonNeutralHadronIso_AfterDB->Fill(muon.neutralHadronIso(), weight);
        hMuonPhotonIso_AfterDB->Fill(muon.photonIso(), weight);
        hMuonIso_AfterDB->Fill(stdIsoVar, weight);

        if(!(muon.chargedHadronIso()/muon.p4().Pt() < 0.1)) continue;
      }
      else if(fIsolationMode == EmbeddingMuonIsolation::kChargedHadrRel15) {
        hMuonChargedHadronIso_AfterDB->Fill(muon.chargedHadronIso(), weight);
        hMuonPuChargedHadronIso_AfterDB->Fill(muon.puChargedHadronIso(), weight);
        hMuonNeutralHadronIso_AfterDB->Fill(muon.neutralHadronIso(), weight);
        hMuonPhotonIso_AfterDB->Fill(muon.photonIso(), weight);
        hMuonIso_AfterDB->Fill(stdIsoVar, weight);

        if(!(muon.chargedHadronIso()/muon.p4().Pt() < 0.15)) continue;
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

  //EmbeddingMuonCollection::Muon& selectedMuon = selectedMuons[0];
  // Fill
  for(size_t i=0; i<selectedMuons.size(); ++i) {
    hSelectedMuonPt_AfterMuonSelection->Fill(selectedMuons[i].p4().Pt(), weight);
  }

  // HBHENoiseFilter
  if(isData() && !fHBHENoiseFilterPassed.value()) return true;
  cHBHENoiseFilter.increment();

  // Muon veto
  int muonVetoCount = 0;
  for(size_t i=0; i<nmuons; ++i) {
    EmbeddingMuonCollection::Muon muon = fMuons.get(i);
    // Skip selected muon
    bool isSelected = false;
    for(size_t j=0; j<selectedMuons.size(); ++j) {
      if(muon.index() == selectedMuons[j].index()) {
        isSelected = true;
        break;
      }
    }
    if(isSelected) continue;

    if(!MuonVeto::pt(muon)) continue;
    if(!MuonVeto::eta(muon)) continue;
    if(!MuonVeto::dB(muon)) continue;
    if(!MuonVeto::isolation(muon)) continue;
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
  for(size_t i=0; i<selectedMuons.size(); ++i) {
    hSelectedMuonPt_AfterMuonVeto->Fill(selectedMuons[i].p4().Pt(), weight);
  }

  /*
  std::cout << "FOO Event " << fEventInfo.event() << ":" << fEventInfo.lumi() << ":" << fEventInfo.run()
            << " electronVeto passed? " << fElectronVetoPassed.value()
            << std::endl;
  if( (fEventInfo.event() == 10069461 && fEventInfo.lumi() == 33572) ||
      (fEventInfo.event() == 10086951 && fEventInfo.lumi() == 33630) ||
      (fEventInfo.event() == 101065527 && fEventInfo.lumi() == 336953) ||
      (fEventInfo.event() == 101450418 && fEventInfo.lumi() == 338236) ||
      (fEventInfo.event() == 101460111 && fEventInfo.lumi() == 338268) ) {
    std::cout << "BAR Event " << fEventInfo.event() << ":" << fEventInfo.lumi() << ":" << fEventInfo.run()
              << " electronVeto passed? " << fElectronVetoPassed.value()
              << " Nelectrons " << fElectrons.size()
              << std::endl;
    for(size_t i=0; i<fElectrons.size(); ++i) {
      ElectronCollection::Electron electron = fElectrons.get(i);
      std::cout << "  Electron " << i
                << " pt " << electron.p4().Pt()
                << " eta " << electron.p4().Eta()
                << " hasGsfTrack " << electron.hasGsfTrack()
                << " hasSuperCluster " << electron.hasSuperCluster()
                << " supercluster eta " << electron.superClusterEta()
                << " passIdVeto " << electron.cutBasedIdVeto()
                << std::endl;
    }
  }
  */


  // Electron veto
  if(!fElectronVetoPassed.value()) return true;
  cElectronVeto.increment();
  // Fill
  for(size_t i=0; i<selectedMuons.size(); ++i) {
    hSelectedMuonPt_AfterElectronVeto->Fill(selectedMuons[i].p4().Pt(), weight);
  }

  // Jet selection
  size_t njets = fJets.size();
  size_t nselectedjets = 0;
  for(size_t i=0; i<njets; ++i) {
    JetCollection::Jet jet = fJets.get(i);

    // Clean selected muon from jet collection
    bool matches = false;
    for(size_t j=0; j<selectedMuons.size(); ++j) {
      double DR = ROOT::Math::VectorUtil::DeltaR(selectedMuons[j].p4(), jet.p4());
      if(DR < 0.1) {
        matches = true;
        break;
      }
    }
    if(matches) continue;

    // Count jets
    ++nselectedjets;
  }
  if(nselectedjets < 3) return true;
  cJetSelection.increment();

  // Fill
  for(size_t i=0; i<selectedMuons.size(); ++i) {
    EmbeddingMuonCollection::Muon& muon = selectedMuons[i];

    hSelectedMuonPt_AfterJetSelection->Fill(muon.p4().Pt(), weight);
    hSelectedMuonPt_AfterJetSelection_Unweighted->Fill(muon.p4().Pt());

    hSelectedMuonChargedHadronEmbIso_AfterJetSelection->Fill(muon.chargedHadronIsoEmb(), weight);
    hSelectedMuonPuChargedHadronEmbIso_AfterJetSelection->Fill(muon.puChargedHadronIsoEmb(), weight);
    hSelectedMuonNeutralHadronEmbIso_AfterJetSelection->Fill(muon.neutralHadronIsoEmb(), weight);
    hSelectedMuonPhotonEmbIso_AfterJetSelection->Fill(muon.photonIsoEmb(), weight);

    hSelectedMuonChargedHadronStdIso_AfterJetSelection->Fill(muon.chargedHadronIso(), weight);
    hSelectedMuonPuChargedHadronStdIso_AfterJetSelection->Fill(muon.puChargedHadronIso(), weight);
    hSelectedMuonNeutralHadronStdIso_AfterJetSelection->Fill(muon.neutralHadronIso(), weight);
    hSelectedMuonPhotonStdIso_AfterJetSelection->Fill(muon.photonIso(), weight);

    hSelectedMuonEmbIso_AfterJetSelection->Fill(muon.tauLikeIsolation(), weight);
    hSelectedMuonStdIso_AfterJetSelection->Fill(muon.standardRelativeIsolation(), weight);
  }

  if(isMC()) {
    for(size_t i=0; i<selectedMuons.size(); ++i) {
      EmbeddingMuonCollection::Muon& muon = selectedMuons[i];
      //std::cout << muon.pdgId() << " " << muon.motherPdgId() << " " << muon.grandMotherPdgId() << std::endl;
      if(std::abs(muon.pdgId()) == 13) {
        if(std::abs(muon.motherPdgId()) == 24) {
          hSelectedMuonPt_AfterJetSelection_MuFromW->Fill(muon.p4().Pt(), weight);
          hSelectedMuonPt_AfterJetSelection_MuFromW_Unweighted->Fill(muon.p4().Pt());
        }
        else if(std::abs(muon.motherPdgId()) == 15 && std::abs(muon.grandMotherPdgId()) == 24)
          hSelectedMuonPt_AfterJetSelection_MuFromTauFromW->Fill(muon.p4().Pt(), weight);
        hSelectedMuonPt_AfterJetSelection_MuFromTauFromW_Unweighted->Fill(muon.p4().Pt());
      }
      else {
        hSelectedMuonPt_AfterJetSelection_MuOther->Fill(muon.p4().Pt(), weight);
        hSelectedMuonPt_AfterJetSelection_MuOther_Unweighted->Fill(muon.p4().Pt());
      }
    }
  }

  hRawMet_AfterJetSelection->Fill(fRawMet.value().Pt(), weight);

  if(selectedMuons.size() == 1) {
    double transverseMass = std::sqrt(2 * selectedMuons[0].p4().Pt() * fRawMet.value().Pt() * (1-std::cos(selectedMuons[0].p4().Phi()-fRawMet.value().Phi())));
    hTransverseMassRawMet_AfterJetSelection->Fill(transverseMass, weight);
  }

  return true;
}

