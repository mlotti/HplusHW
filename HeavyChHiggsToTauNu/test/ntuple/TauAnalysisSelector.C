#include "BaseSelector.h"
#include "Branches.h"
#include "Configuration.h"

#include "TFile.h"
#include "TDirectory.h"
#include "TH1F.h"
#include "TEfficiency.h"
#include "Math/VectorUtil.h"

#include<stdexcept>
#include<sstream>

namespace {
  enum MCTauMode {
    kMCTauOneTau,
    kMCTauTwoTaus,
    kMCTauNone
  };

  MCTauMode parseMCTauMode(const std::string& mode) {
    if(mode == "" || mode == "none")
      return kMCTauNone;
    if(mode == "oneTau")
      return kMCTauOneTau;
    if(mode == "twoTaus")
      return kMCTauTwoTaus;

    std::stringstream ss;
    ss << "Gor mcTauMode " << mode << " which is not valid. Valid options are '', 'none', 'oneTau', 'twoTaus'";

    throw std::runtime_error(ss.str());
  }
}

// TauAnalysisSelector
class TauAnalysisSelector: public BaseSelector {
public:
  TauAnalysisSelector(const std::string& puWeight = "", bool isEmbedded=false,
                      const std::string& embeddingWTauMuFile="", const std::string& embeddingWTauMuPath="",
                      const std::string& mcTauMode="");
  ~TauAnalysisSelector();

  void setOutput(TDirectory *dir);
  void setupBranches(TTree *tree);
  bool process(Long64_t entry);

private:
  // Input
  EventInfo fEventInfo;
  EmbeddingMuonCollection fMuons;
  //ElectronCollection fElectrons;
  JetCollection fJets;
  TauCollection fTaus;
  GenParticleCollection fGenTaus; // from original event in embedded, for all in normal

  std::string fPuWeightName;
  Branch<double> fPuWeight;
  Branch<unsigned> fSelectedVertexCount;
  Branch<unsigned> fVertexCount;
  //Branch<bool> fElectronVetoPassed;
  Branch<bool> fMuTriggerPassed;

  const bool fIsEmbedded;
  TH1 *fEmbeddingWTauMuWeights;
  const MCTauMode fMCTauMode;

  TH1 *makeEta(const char *name);
  TH1 *makePt(const char *name);
  TH1 *makePhi(const char *name);
  TH1 *makeVertexCount(const char *name);

  // Output
  // Counts
  EventCounter::Count cAll;
  //EventCounter::Count cElectronVeto;
  EventCounter::Count cTauMCSelection;
  EventCounter::Count cOnlyWMu;
  EventCounter::Count cWTauMuWeight;
  EventCounter::Count cJetSelection;
  EventCounter::Count cPrimaryVertex;
  EventCounter::Count cAllTauCandidates;
  EventCounter::Count cPrePtCut;
  EventCounter::Count cDecayModeFinding;
  EventCounter::Count cEtaCut;
  EventCounter::Count cPtCut;
  EventCounter::Count cLeadingTrackPtCut;
  EventCounter::Count cEcalCracks;
  EventCounter::Count cEcalGap;
  EventCounter::Count cAgainstElectron;
  EventCounter::Count cAgainstMuon;
  EventCounter::Count cIsolation;
  EventCounter::Count cOneProng;
  EventCounter::Count cRtau;
  EventCounter::Count cMuTrigger;

  // Histograms
  TH1 *hTauEta_AfterDecayModeFindingIsolation;
  TH1 *hTauPt_AfterDecayModeFindingIsolation;
  TH1 *hVertexCount_AfterDecayModeFindingIsolation;

  TH1 *hTauPt_AfterEtaCutIsolation;
  TH1 *hVertexCount_AfterEtaCutIsolation;

  TH1 *hTauPhi_AfterPtCutIsolation;
  TH1 *hTauLeadingTrackPt_AfterPtCutIsolation;
  TH1 *hVertexCount_AfterPtCutIsolation;

  TH1 *hTauDecayMode_AfterIsolation;
  TH1 *hTauDecayModeAll_AfterIsolation;
  TH1 *hVertexCount_AfterIsolation;

  TH1 *hTauPt_AfterOneProng;
  TH1 *hTauP_AfterOneProng;
  TH1 *hTauLeadingTrackPt_AfterOneProng;
  TH1 *hTauLeadingTrackP_AfterOneProng;
  TH1 *hTauRtau_AfterOneProng;
  TH1 *hVertexCount_AfterOneProng;

  TH1 *hTauPt_AfterRtau;
  TH1 *hVertexCount_AfterRtau;
};

TauAnalysisSelector::TauAnalysisSelector(const std::string& puWeight, bool isEmbedded,
                                         const std::string& embeddingWTauMuFile, const std::string& embeddingWTauMuPath,
                                         const std::string& mcTauMode):
  BaseSelector(),
  //fMuons("Emb"),
  fGenTaus(isEmbedded ? "gentausOriginal" : "gentaus"),
  fPuWeightName(puWeight),
  fIsEmbedded(isEmbedded),
  fEmbeddingWTauMuWeights(0),
  fMCTauMode(parseMCTauMode(mcTauMode)),
  cAll(fEventCounter.addCounter("All events")),
  //cElectronVeto(fEventCounter.addCounter("Electron veto")),
  cTauMCSelection(fEventCounter.addCounter("Tau MC requirement")),
  cOnlyWMu(fEventCounter.addCounter("Only W->mu")),
  cWTauMuWeight(fEventCounter.addCounter("W->tau->mu weighting")),
  cJetSelection(fEventCounter.addCounter("Jet selection")),
  cPrimaryVertex(fEventCounter.addCounter("Primary vertex")),
  cAllTauCandidates(fEventCounter.addCounter(">= 1 tau candidate")),
  cPrePtCut(fEventCounter.addCounter("Pre Pt cut")),
  cDecayModeFinding(fEventCounter.addCounter("Decay mode finding")),
  cEtaCut(fEventCounter.addCounter("Eta cut")),
  cPtCut(fEventCounter.addCounter("Pt cut")),
  cLeadingTrackPtCut(fEventCounter.addCounter("Leading track pt")),
  cEcalCracks(fEventCounter.addCounter("ECAL fiducial: cracks")),
  cEcalGap(fEventCounter.addCounter("ECAL fiducial: gap")),
  cAgainstElectron(fEventCounter.addCounter("Against electron")),
  cAgainstMuon(fEventCounter.addCounter("Against muon")),
  cIsolation(fEventCounter.addCounter("Isolation")),
  cOneProng(fEventCounter.addCounter("One prong")),
  cRtau(fEventCounter.addCounter("Rtau")),
  cMuTrigger(fEventCounter.addCounter("Mu trigger"))
{
  if(isEmbedded && !embeddingWTauMuFile.empty()) {
    TFile *file = TFile::Open(embeddingWTauMuFile.c_str());
    TEfficiency *eff = dynamic_cast<TEfficiency *>(file->Get(embeddingWTauMuPath.c_str()));
    TAxis *xaxis = eff->GetPassedHistogram()->GetXaxis();
    fEmbeddingWTauMuWeights = new TH1F("weights", "weights", xaxis->GetNbins(), xaxis->GetBinLowEdge(xaxis->GetFirst()), xaxis->GetBinUpEdge(xaxis->GetLast()));
    fEmbeddingWTauMuWeights->SetDirectory(0);
    for(int bin=1; bin <= xaxis->GetNbins(); ++bin) {
      fEmbeddingWTauMuWeights->SetBinContent(bin, eff->GetEfficiency(bin));
      std::cout << "Bin " << bin << " low edge " << fEmbeddingWTauMuWeights->GetXaxis()->GetBinLowEdge(bin) << " value " << fEmbeddingWTauMuWeights->GetBinContent(bin) << std::endl;
    }
    fEmbeddingWTauMuWeights->SetBinContent(xaxis->GetNbins()+1, fEmbeddingWTauMuWeights->GetBinContent(xaxis->GetNbins()));
    file->Close();
  }
}

TauAnalysisSelector::~TauAnalysisSelector() {}

TH1 *TauAnalysisSelector::makeEta(const char *name) { return makeTH<TH1F>(name, "Tau eta", 25, -2.5, 2.5); }
TH1 *TauAnalysisSelector::makePt(const char *name)  { return makeTH<TH1F>(name, "Tau pt", 25, 0, 250); }
TH1 *TauAnalysisSelector::makePhi(const char *name)  { return makeTH<TH1F>(name, "Tau phi", 32, -3.2, 3.2); }
TH1 *TauAnalysisSelector::makeVertexCount(const char *name) { return makeTH<TH1F>(name, "Vertex count", 30, 0, 30); }

void TauAnalysisSelector::setOutput(TDirectory *dir) {
  if(dir)
    dir->cd();

  hTauEta_AfterDecayModeFindingIsolation = makeEta("tauEta_AfterDecayModeFindingIsolation");
  hTauPt_AfterDecayModeFindingIsolation = makePt("tauPt_AfterDecayModeFindingIsolation");
  hVertexCount_AfterDecayModeFindingIsolation = makeVertexCount("vertexCount_AfterDecayModeFindingIsolation");

  hTauPt_AfterEtaCutIsolation = makePt("tauPt_AfterEtaCutIsolation");
  hVertexCount_AfterEtaCutIsolation = makeVertexCount("vertexCount_AfterEtaCutIsolation");

  hTauPhi_AfterPtCutIsolation = makePhi("tauPhi_AfterPtCutIsolation");
  hTauLeadingTrackPt_AfterPtCutIsolation = makePt("tauLeadingTrackPt_AfterPtCutIsolation");
  hVertexCount_AfterPtCutIsolation = makeVertexCount("vertexCount_AfterPtCutIsolation");

  hTauDecayMode_AfterIsolation = makeTH<TH1F>("tauDecayMode_AfterIsolation", "Decay mode", 5, 0, 5);
  hTauDecayModeAll_AfterIsolation = makeTH<TH1F>("tauDecayModeAll_AfterIsolation", "Decay mode", 16, 0, 16);
  hVertexCount_AfterIsolation = makeVertexCount("vertexCount_AfterIsolation");

  hTauPt_AfterOneProng = makePt("tauPt_AfterOneProng");
  hTauP_AfterOneProng = makePt("tauP_AfterOneProng");
  hTauLeadingTrackPt_AfterOneProng = makePt("tauLeadingTrackPt_AfterOneProng");
  hTauLeadingTrackP_AfterOneProng = makePt("tauLeadingTrackP_AfterOneProng");
  hTauRtau_AfterOneProng = makeTH<TH1F>("tauRtau_AfterOneProng", "Rtau", 22, 0, 1.1);
  hVertexCount_AfterOneProng = makeVertexCount("vertexCount_AfterOneProng");

  hTauPt_AfterRtau = makePt("tauPt_AfterRtau");
  hVertexCount_AfterRtau = makeVertexCount("vertexCount_AfterRtau");
}

void TauAnalysisSelector::setupBranches(TTree *tree) {
  fEventInfo.setupBranches(tree);
  if(fIsEmbedded) {
    fMuons.setupBranches(tree, isMC());
    //fElectrons.setupBranches(tree, isMC());
    fJets.setupBranches(tree);
  }
  fTaus.setupBranches(tree, isMC() && !fIsEmbedded);
  if(isMC())
    fGenTaus.setupBranches(tree);

  if(!fPuWeightName.empty())
    fPuWeight.setupBranch(tree, fPuWeightName.c_str());
  fSelectedVertexCount.setupBranch(tree, "selectedPrimaryVertex_count");
  fVertexCount.setupBranch(tree, "goodPrimaryVertex_count");
  if(fIsEmbedded) {
    fMuTriggerPassed.setupBranch(tree, "trigger_Mu40_eta2p1");
  }

  //fElectronVetoPassed.setupBranch(tree, "ElectronVetoPassed");

}

bool TauAnalysisSelector::process(Long64_t entry) {
  fEventInfo.setEntry(entry);
  fMuons.setEntry(entry);
  //fElectrons.setEntry(entry);
  fJets.setEntry(entry);
  fTaus.setEntry(entry);
  fGenTaus.setEntry(entry);
  fPuWeight.setEntry(entry);
  fSelectedVertexCount.setEntry(entry);
  fVertexCount.setEntry(entry);
  fMuTriggerPassed.setEntry(entry);

  //fElectronVetoPassed.setEntry(entry);

  double weight = 1.0;
  if(!fPuWeightName.empty()) {
    weight *= fPuWeight.value();
  }
  fEventCounter.setWeight(weight);

  cAll.increment();

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

  if(!fElectronVetoPassed.value()) return false;
  cElectronVeto.increment();
  */

  // MC status
  if(isMC() && fMCTauMode != kMCTauNone) {
    size_t ntaus = 0;
    for(size_t i=0; i<fGenTaus.size(); ++i) {
      GenParticleCollection::GenParticle gen = fGenTaus.get(i);
      if(std::abs(gen.motherPdgId()) == 24 && std::abs(gen.grandMotherPdgId()) == 6) {
        ++ntaus;
      }
    }

    if(fIsEmbedded) {
      // For embedded the embedded tau is counted as one
      if(fMCTauMode == kMCTauOneTau && ntaus != 0) return true;
      if(fMCTauMode == kMCTauTwoTaus && ntaus != 1) return true;
    }
    else {
      if(fMCTauMode == kMCTauOneTau && ntaus != 1) return true;
      if(fMCTauMode == kMCTauTwoTaus && ntaus != 2) return true;
    }
  }
  cTauMCSelection.increment();

  bool originalMuonIsWMu = false;
  EmbeddingMuonCollection::Muon embeddingMuon;
  if(fIsEmbedded) {
    if(fMuons.size() != 1)
      throw std::runtime_error("Embedding muon collection size is not 1");
    embeddingMuon = fMuons.get(0);
    if(embeddingMuon.p4().Pt() < 41) return true;
    //std::cout << "Muon pt " << muon.p4().Pt() << std::endl;

    originalMuonIsWMu = std::abs(embeddingMuon.pdgId()) == 13 && std::abs(embeddingMuon.motherPdgId()) == 24;
    if(!originalMuonIsWMu) return true;
  }
  else {
    size_t ntaus = 0;
    for(size_t i=0; i<fGenTaus.size(); ++i) {
      GenParticleCollection::GenParticle gen = fGenTaus.get(i);
      if(gen.p4().Pt() < 41) continue;
      ++ntaus;
    }
    if(ntaus < 1) return true;
  }

  cOnlyWMu.increment();

  // Per-event correction for W->tau->mu
  if(fIsEmbedded && fEmbeddingWTauMuWeights) {
    embeddingMuon.ensureValidity();
    int bin = fEmbeddingWTauMuWeights->FindBin(embeddingMuon.p4().Pt());
    //std::cout << embeddingMuon.p4().Pt() << " " << bin << std::endl;
    weight *= fEmbeddingWTauMuWeights->GetBinContent(bin);
    fEventCounter.setWeight(weight);
  }
  cWTauMuWeight.increment();

  // Jet selection
  /*
  size_t njets = fJets.size();
  size_t nselectedjets = 0;
  for(size_t i=0; i<njets; ++i) {
    JetCollection::Jet jet = fJets.get(i);

    // Clean selected muon from jet collection
    bool matches = false;
    double DR = ROOT::Math::VectorUtil::DeltaR(fMuons.get(0).p4(), jet.p4());
    if(DR < 0.1) {
      matches = true;
    }
    if(matches) continue;

    // Count jets
    ++nselectedjets;
  }
  if(nselectedjets < 3) return true;
  */
  cJetSelection.increment();

  if(fSelectedVertexCount.value() <= 0) return true;
  cPrimaryVertex.increment();

  std::vector<TauCollection::Tau> selectedTaus;
  std::vector<TauCollection::Tau> tmp;

  if(fTaus.size() < 1) return true;
  cAllTauCandidates.increment();

  // Pre pT cut (for some reason in the region pT < 10 there is significantly more normal than embedded)
  for(size_t i=0; i<fTaus.size(); ++i) {
    TauCollection::Tau tau = fTaus.get(i);
    if(tau.p4().Pt() < 10) continue;
    //if(!TauID::isolation(tau)) continue;
    //if(isMC() && !fIsEmbedded && tau.genMatchP4().Pt() <= 41) continue; // temporary hack
    selectedTaus.push_back(tau);
    if(!fIsEmbedded) break; // select only the first gen tau
  }
  if(selectedTaus.empty()) return true;
  cPrePtCut.increment();

  // Decay mode finding
  bool atLeastOneIsolated = false;
  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];
    if(!TauID::decayModeFinding(tau)) continue;

    if(TauID::isolation(tau)) {
      atLeastOneIsolated = true;
      hTauEta_AfterDecayModeFindingIsolation->Fill(tau.p4().Eta(), weight);
      hTauPt_AfterDecayModeFindingIsolation->Fill(tau.p4().Pt(), weight);
    }
    tmp.push_back(tau);
  }
  selectedTaus.swap(tmp);
  tmp.clear();
  if(selectedTaus.empty()) return true;
  cDecayModeFinding.increment();
  if(atLeastOneIsolated)
    hVertexCount_AfterDecayModeFindingIsolation->Fill(fVertexCount.value(), weight);

  // Eta cut
  atLeastOneIsolated = false;
  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];
    if(!TauID::eta(tau)) continue;

    if(TauID::isolation(tau)) {
      atLeastOneIsolated = true;
      hTauPt_AfterEtaCutIsolation->Fill(tau.p4().Pt(), weight);
    }
    tmp.push_back(tau);
  }
  selectedTaus.swap(tmp);
  tmp.clear();
  if(selectedTaus.empty()) return true;
  cEtaCut.increment();
  if(atLeastOneIsolated)
    hVertexCount_AfterEtaCutIsolation->Fill(fVertexCount.value(), weight);

  // Pt cut
  atLeastOneIsolated = false;
  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];
    if(!TauID::pt(tau)) continue;

    if(TauID::isolation(tau)) {
      atLeastOneIsolated = true;
      hTauPhi_AfterPtCutIsolation->Fill(tau.p4().Phi(), weight);
      hTauLeadingTrackPt_AfterPtCutIsolation->Fill(tau.leadPFChargedHadrCandP4().Pt(), weight);
    }
    tmp.push_back(tau);
  }
  selectedTaus.swap(tmp);
  tmp.clear();
  if(selectedTaus.empty()) return true;
  cPtCut.increment();
  if(atLeastOneIsolated)
    hVertexCount_AfterPtCutIsolation->Fill(fVertexCount.value(), weight);

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

  // ECAL fiducial cuts
  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];
    if(!TauID::ecalCracks(tau)) continue;
    tmp.push_back(tau);
  }
  selectedTaus.swap(tmp);
  tmp.clear();
  if(selectedTaus.empty()) return true;
  cEcalCracks.increment();

  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];
    if(!TauID::ecalGap(tau)) continue;
    tmp.push_back(tau);
  }
  selectedTaus.swap(tmp);
  tmp.clear();
  if(selectedTaus.empty()) return true;
  cEcalGap.increment();
  

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
  hVertexCount_AfterIsolation->Fill(fVertexCount.value(), weight);

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
  hVertexCount_AfterOneProng->Fill(fVertexCount.value(), weight);

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
  hVertexCount_AfterRtau->Fill(fVertexCount.value(), weight);

  // Tau ID finished

  // Trigger
  /*
  if(fIsEmbedded) {
    if(!fMuTriggerPassed.value()) return true;
  }
  */
  cMuTrigger.increment();

  return true;
}
