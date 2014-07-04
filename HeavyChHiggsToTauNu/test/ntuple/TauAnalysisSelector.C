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
  enum MCTauMultiplicity {
    kMCTauZeroTaus,
    kMCTauOneTau,
    kMCTauTwoTaus,
    kMCTauMoreThanTwoTaus,
    kMCTauNone
  };
  enum MCTauMode {
    kMCTauAll,
    kMCTauHadronic,
  };
  enum EmbeddingNormalizationMode {
    kIDEfficiency,
    kIDTriggerEfficiency,
    kIDTriggerEfficiencyTauBR,
  };

  MCTauMultiplicity parseMCTauMultiplicity(const std::string& mode) {
    if(mode == "" || mode == "none")
      return kMCTauNone;
    if(mode == "zeroTaus")
      return kMCTauZeroTaus;
    if(mode == "oneTau")
      return kMCTauOneTau;
    if(mode == "twoTaus")
      return kMCTauTwoTaus;
    if(mode == "moreThanTwoTaus")
      return kMCTauMoreThanTwoTaus;

    std::stringstream ss;
    ss << "Got mcTauMultiplicity " << mode << " which is not valid. Valid options are '', 'none', 'oneTau', 'twoTaus'";

    throw std::runtime_error(ss.str());
  }

  MCTauMode parseMCTauMode(const std::string& mode) {
    if(mode == "" || mode == "all")
      return kMCTauAll;
    if(mode == "hadronic")
      return kMCTauHadronic;

    std::stringstream ss;
    ss << "Got mcTauMode " << mode << " which is not valid. Valid options are '', 'all', 'hadronic'";

    throw std::runtime_error(ss.str());
  }

  EmbeddingNormalizationMode parseEmbeddingNormalizationMode(const std::string& mode) {
    if(mode == "" || mode == "IDEfficiency")
      return kIDEfficiency;
    if(mode == "IDTriggerEfficiency")
      return kIDTriggerEfficiency;
    if(mode == "IDTriggerEfficiencyTauBR")
      return kIDTriggerEfficiencyTauBR;
    std::stringstream ss;
    ss << "Got embeddingNormalizationMode " << mode << " which is not valid. Valid options are '', 'IDEfficiency', 'IDTriggerEfficiency', 'IDTriggerEfficiencyTauBR'";
    throw std::runtime_error(ss.str());
  }

  TH1 *makePt(const char *name) {
    return makeTH<TH1F>(name, "Tau pt", 400, 0, 400);
  }
}

// TauAnalysisSelector
class TauAnalysisSelector: public BaseSelector {
public:
  TauAnalysisSelector(const std::string& puWeight = "", bool isEmbedded=false,
                      const std::string& embeddingWTauMuFile="", const std::string& embeddingWTauMuPath="",
                      const std::string& mcTauMultiplicty="", const std::string& mcTauMode="",
                      const std::string& embeddingNormalizationMode="",
                      TH1 *embeddingMuonWeights=0);
  ~TauAnalysisSelector();

  void setOutput(TDirectory *dir);
  void setupBranches(BranchManager& branchManager);
  bool process(Long64_t entry);

private:
  bool findGenTaus(GenParticleCollection& coll, int grandMother, std::vector<GenParticleCollection::GenParticle> *result);

  // Input
  EventInfo fEventInfo;
  EmbeddingMuonCollection fMuons;
  //ElectronCollection fElectrons;
  JetCollection fJets;
  TauCollection fTaus;
  GenParticleCollection fGenTaus; // from original event in embedded, for all in normal
  GenParticleCollection fGenTausEmbedded;

  std::string fPuWeightName;
  Branch<double> *fPuWeight;
  Branch<double> *fGeneratorWeight;
  Branch<unsigned> *fSelectedVertexCount;
  Branch<unsigned> *fVertexCount;
  //Branch<bool> fElectronVetoPassed;
  Branch<bool> *fMuTriggerPassed;

  const bool fIsEmbedded;
  TH1 *fEmbeddingWTauMuWeights;
  const MCTauMultiplicity fMCTauMultiplicity;
  const MCTauMode fMCTauMode;
  const EmbeddingNormalizationMode fEmbeddingNormalizationMode;
  TH1 *fEmbeddingMuonWeights;

  TH1 *makeVertexCount(const char *name);

  // Output
  // Counts
  EventCounter::Count cAll;
  //EventCounter::Count cElectronVeto;
  EventCounter::Count cGeneratorWeight;
  EventCounter::Count cTauBRWeight;
  EventCounter::Count cGenTauFound;
  EventCounter::Count cTauMCSelection;
  EventCounter::Count cOnlyWMu;
  EventCounter::Count cWTauMuWeight;
  EventCounter::Count cTriggerEffWeight;
  EventCounter::Count cIdEffWeight;
  EventCounter::Count cMuonWeight;
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
  struct Kinematics {
    Kinematics(): hPt(0), hEta(0), hPhi(0) {}

    void book(const std::string& prefix) {
      hPt = makePt((prefix+"_pt").c_str());
      hEta = makeTH<TH1F>((prefix+"_eta").c_str(), "Eta", 44, -2.1, 2.1);
      hPhi = makeTH<TH1F>((prefix+"_phi").c_str(), "Phi", 128, -3.2, 3.2);
    }

    template <typename T>
    void fill(const T& p4, double weight=1.0) {
      hPt->Fill(p4.Pt(), weight);
      hEta->Fill(p4.Eta(), weight);
      hPhi->Fill(p4.Phi(), weight);
    }

    TH1 *hPt;
    TH1 *hEta;
    TH1 *hPhi;
  };

  Kinematics hTau_AfterDecayModeFindingIsolation;
  Kinematics hGenTau_AfterDecayModeFindingIsolation;
  TH1 *hVertexCount_AfterDecayModeFindingIsolation;

  Kinematics hTau_AfterEtaCutIsolation;
  Kinematics hGenTau_AfterEtaCutIsolation;
  TH1 *hVertexCount_AfterEtaCutIsolation;

  Kinematics hTau_AfterPtCutIsolation;
  Kinematics hGenTau_AfterPtCutIsolation;
  TH1 *hTauLeadingTrackPt_AfterPtCutIsolation;
  TH1 *hVertexCount_AfterPtCutIsolation;

  Kinematics hTau_AfterLeadingTrackPtCutIsolation;
  Kinematics hGenTau_AfterLeadingTrackPtCutIsolation;

  Kinematics hTau_AfterAgainstElectronIsolation;
  Kinematics hGenTau_AfterAgainstElectronIsolation;

  Kinematics hTau_AfterAgainstMuonIsolation;
  Kinematics hGenTau_AfterAgainstMuonIsolation;

  Kinematics hTau_AfterIsolation;
  Kinematics hGenTau_AfterIsolation;
  TH1 *hTauDecayMode_AfterIsolation;
  TH1 *hTauDecayModeAll_AfterIsolation;
  TH1 *hVertexCount_AfterIsolation;

  Kinematics hTau_AfterOneProng;
  Kinematics hGenTau_AfterOneProng;
  TH1 *hTauP_AfterOneProng;
  TH1 *hTauLeadingTrackPt_AfterOneProng;
  TH1 *hTauLeadingTrackP_AfterOneProng;
  TH1 *hTauRtau_AfterOneProng;
  TH1 *hVertexCount_AfterOneProng;

  Kinematics hTau_AfterRtau;
  Kinematics hGenTau_AfterRtau;
  TH1 *hVertexCount_AfterRtau;
};

TauAnalysisSelector::TauAnalysisSelector(const std::string& puWeight, bool isEmbedded,
                                         const std::string& embeddingWTauMuFile, const std::string& embeddingWTauMuPath,
                                         const std::string& mcTauMultiplicity, const std::string& mcTauMode,
                                         const std::string& embeddingNormalizationMode,
                                         TH1 *embeddingMuonWeights):
  BaseSelector(),
  //fMuons("Emb"),
  fGenTaus(isEmbedded ? "gentausOriginal" : "gentaus", true),
  fGenTausEmbedded("gentausEmbedded", true),
  fPuWeightName(puWeight),
  fIsEmbedded(isEmbedded),
  fEmbeddingWTauMuWeights(0),
  fMCTauMultiplicity(parseMCTauMultiplicity(mcTauMultiplicity)),
  fMCTauMode(parseMCTauMode(mcTauMode)),
  fEmbeddingNormalizationMode(parseEmbeddingNormalizationMode(embeddingNormalizationMode)),
  fEmbeddingMuonWeights(embeddingMuonWeights),
  cAll(fEventCounter.addCounter("All events")),
  //cElectronVeto(fEventCounter.addCounter("Electron veto")),
  cGeneratorWeight(fEventCounter.addCounter("Vis. pt weight")),
  cTauBRWeight(fEventCounter.addCounter("Tau BR weighting")),
  cGenTauFound(fEventCounter.addCounter("Gen tau found")),
  cTauMCSelection(fEventCounter.addCounter("Tau MC requirement")),
  cOnlyWMu(fEventCounter.addCounter("Only W->mu")),
  cWTauMuWeight(fEventCounter.addCounter("W->tau->mu weighting")),
  cTriggerEffWeight(fEventCounter.addCounter("Muon trigger eff weighting")),
  cIdEffWeight(fEventCounter.addCounter("Muon ID eff weighting")),
  cMuonWeight(fEventCounter.addCounter("Muon corr weighting (from argument)")),
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

  if(isEmbedded) {
    fMuons.setIdEfficiencyName("efficiency_Run2011AB");
    fMuons.setTriggerEfficiencyName("efficiency_trigger");
  }
}

TauAnalysisSelector::~TauAnalysisSelector() {}

TH1 *TauAnalysisSelector::makeVertexCount(const char *name) { return makeTH<TH1F>(name, "Vertex count", 30, 0, 30); }

void TauAnalysisSelector::setOutput(TDirectory *dir) {
  if(dir)
    dir->cd();

  hTau_AfterDecayModeFindingIsolation.book("tau_AfterDecayModeFindingIsolation");
  hGenTau_AfterDecayModeFindingIsolation.book("gentau_AfterDecayModeFindingIsolation");
  hVertexCount_AfterDecayModeFindingIsolation = makeVertexCount("vertexCount_AfterDecayModeFindingIsolation");

  hTau_AfterEtaCutIsolation.book("tau_AfterEtaCutIsolation");
  hGenTau_AfterEtaCutIsolation.book("gentau_AfterEtaCutIsolation");
  hVertexCount_AfterEtaCutIsolation = makeVertexCount("vertexCount_AfterEtaCutIsolation");

  hTau_AfterPtCutIsolation.book("tau_AfterPtCutIsolation");
  hGenTau_AfterPtCutIsolation.book("gentau_AfterPtCutIsolation");
  hTauLeadingTrackPt_AfterPtCutIsolation = makePt("tau_AfterPtCutIsolation_leadingTrackPt");
  hVertexCount_AfterPtCutIsolation = makeVertexCount("vertexCount_AfterPtCutIsolation");

  hTau_AfterLeadingTrackPtCutIsolation.book("tau_AfterLeadingTrackPtCutIsolation");
  hGenTau_AfterLeadingTrackPtCutIsolation.book("gentau_AfterLeadingTrackPtCutIsolation");

  hTau_AfterAgainstElectronIsolation.book("tau_AfterAgainstElectronIsolation");
  hGenTau_AfterAgainstElectronIsolation.book("gentau_AfterAgainstElectronIsolation");

  hTau_AfterAgainstMuonIsolation.book("tau_AfterAgainstMuonIsolation");
  hGenTau_AfterAgainstMuonIsolation.book("gentau_AfterAgainstMuonIsolation");

  hTau_AfterIsolation.book("tau_AfterIsolation");
  hGenTau_AfterIsolation.book("gentau_AfterIsolation");
  hTauDecayMode_AfterIsolation = makeTH<TH1F>("tauDecayMode_AfterIsolation", "Decay mode", 5, 0, 5);
  hTauDecayModeAll_AfterIsolation = makeTH<TH1F>("tauDecayModeAll_AfterIsolation", "Decay mode", 16, 0, 16);
  hVertexCount_AfterIsolation = makeVertexCount("vertexCount_AfterIsolation");

  hTau_AfterOneProng.book("tau_AfterOneProng");
  hGenTau_AfterOneProng.book("gentau_AfterOneProng");
  hTauP_AfterOneProng = makePt("tau_AfterOneProng_p");
  hTauLeadingTrackPt_AfterOneProng = makePt("tau_AfterOneProng_leadingTrackPt");
  hTauLeadingTrackP_AfterOneProng = makePt("tau_AfterOneProng_leadingTrackP");
  hTauRtau_AfterOneProng = makeTH<TH1F>("tau_AfterOneProng_rtau", "Rtau", 22, 0, 1.1);
  hVertexCount_AfterOneProng = makeVertexCount("vertexCount_AfterOneProng");

  hTau_AfterRtau.book("tau_AfterRtau");
  hGenTau_AfterRtau.book("gentau_AfterRtau");
  hVertexCount_AfterRtau = makeVertexCount("vertexCount_AfterRtau");
}

void TauAnalysisSelector::setupBranches(BranchManager& branchManager) {
  fEventInfo.setupBranches(branchManager);
  if(fIsEmbedded) {
    branchManager.book("weightGenerator", &fGeneratorWeight);

    fMuons.setupBranches(branchManager, isMC());
    //fElectrons.setupBranches(branchManager, isMC());
    fJets.setupBranches(branchManager);
    fGenTausEmbedded.setupBranches(branchManager);
  }
  fTaus.setupBranches(branchManager, isMC() && !fIsEmbedded);
  if(isMC())
    fGenTaus.setupBranches(branchManager);

  if(!fPuWeightName.empty())
    branchManager.book(fPuWeightName, &fPuWeight);

  branchManager.book("selectedPrimaryVertex_count", &fSelectedVertexCount);
  branchManager.book("goodPrimaryVertex_count", &fVertexCount);
  if(fIsEmbedded) {
    branchManager.book("trigger_Mu40_eta2p1", &fMuTriggerPassed);
  }

  //branchManager.book("ElectronVetoPassed", &fElectronVetoPassed);
}


//////////////////////////////////////////////////
bool TauAnalysisSelector::findGenTaus(GenParticleCollection& coll, int grandMother, std::vector<GenParticleCollection::GenParticle> *result) {
  for(size_t i=0; i<coll.size(); ++i) {
    GenParticleCollection::GenParticle gen = coll.get(i);
    if(!(gen.p4().Pt() > 41)) continue;
    if(!(std::abs(gen.p4().Eta()) < 2.1)) continue;

    if(std::abs(gen.motherPdgId()) == 24 && std::abs(gen.grandMotherPdgId()) == grandMother) { 
      int daughter = std::abs(gen.daughterPdgId());
      if(fMCTauMode == kMCTauHadronic && (daughter == 11 || daughter == 13)) {
        return false;
      }
      result->push_back(gen);
    }
  }
  return true;
}


bool TauAnalysisSelector::process(Long64_t entry) {
  double weight = 1.0;
  if(!fPuWeightName.empty()) {
    weight *= fPuWeight->value();
  }
  fEventCounter.setWeight(weight);

  cAll.increment();

  if(fIsEmbedded) {
    weight *= fGeneratorWeight->value();
    fEventCounter.setWeight(weight);
  }
  cGeneratorWeight.increment();

  /*
  std::cout << "FOO Event " << fEventInfo.event() << ":" << fEventInfo.lumi() << ":" << fEventInfo.run()
            << " electronVeto passed? " << fElectronVetoPassed->value()
            << std::endl;

  if( (fEventInfo.event() == 10069461 && fEventInfo.lumi() == 33572) ||
      (fEventInfo.event() == 10086951 && fEventInfo.lumi() == 33630) ||
      (fEventInfo.event() == 101065527 && fEventInfo.lumi() == 336953) ||
      (fEventInfo.event() == 101450418 && fEventInfo.lumi() == 338236) ||
      (fEventInfo.event() == 101460111 && fEventInfo.lumi() == 338268) ) {
    std::cout << "BAR Event " << fEventInfo.event() << ":" << fEventInfo.lumi() << ":" << fEventInfo.run()
              << " electronVeto passed? " << fElectronVetoPassed->value()
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

  if(!fElectronVetoPassed->value()) return false;
  cElectronVeto.increment();
  */

  // Tau BR
  if(fIsEmbedded && fEmbeddingNormalizationMode == kIDTriggerEfficiencyTauBR) {
    weight *= (1-0.357); // from my thesis, which took the numbers from PDG
    fEventCounter.setWeight(weight);
  }
  cTauBRWeight.increment();

  // MC status
  std::vector<GenParticleCollection::GenParticle> genTaus;
  GenParticleCollection::GenParticle theGenTau;
  if(isMC()) {
    bool canContinue = true;
    if(fIsEmbedded) {
      canContinue = findGenTaus(fGenTausEmbedded, 2212, &genTaus);
      canContinue = canContinue && genTaus.size() != 0;
    }
    else
      canContinue = findGenTaus(fGenTaus, 6, &genTaus);
    if(!canContinue)
      return false;
  }
  cGenTauFound.increment();
  if(isMC() && fMCTauMultiplicity != kMCTauNone) {
    size_t ntaus = genTaus.size();
    if(fIsEmbedded) {
      std::vector<GenParticleCollection::GenParticle> genTausOrig;
      findGenTaus(fGenTaus, 6, &genTausOrig);
      ntaus = genTausOrig.size();
    }

    if(fIsEmbedded) {
      // For embedded the embedded tau is counted as one
      if(fMCTauMultiplicity == kMCTauZeroTaus) return true;
      if(fMCTauMultiplicity == kMCTauOneTau && ntaus != 0) return true;
      if(fMCTauMultiplicity == kMCTauTwoTaus && ntaus != 1) return true;
      if(fMCTauMultiplicity == kMCTauMoreThanTwoTaus && ntaus < 2) return true;
    }
    else {
      if(fMCTauMultiplicity == kMCTauZeroTaus && ntaus != 0) return true;
      if(fMCTauMultiplicity == kMCTauOneTau && ntaus != 1) return true;
      if(fMCTauMultiplicity == kMCTauTwoTaus && ntaus != 2) return true;
      if(fMCTauMultiplicity == kMCTauMoreThanTwoTaus && ntaus < 3) return true;
    }
   
    if(genTaus.size() > 0)
      theGenTau = genTaus[0];
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

    originalMuonIsWMu = std::abs(embeddingMuon.pdgId()) == 13 && std::abs(embeddingMuon.motherPdgId()) == 24 && std::abs(embeddingMuon.grandMotherPdgId()) == 6;
    if(!originalMuonIsWMu) return true;
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

  // Muon trigger efficiency weighting
  if(fIsEmbedded && (fEmbeddingNormalizationMode == kIDTriggerEfficiency || fEmbeddingNormalizationMode == kIDTriggerEfficiencyTauBR)) {
    weight *= 1/embeddingMuon.triggerEfficiency();
    fEventCounter.setWeight(weight);
  }
  cTriggerEffWeight.increment();

  // Muon ID efficiency weighting
  if(fIsEmbedded) {
    weight *= 1/embeddingMuon.idEfficiency();
    fEventCounter.setWeight(weight);
  }
  cIdEffWeight.increment();

  // Weighting by arbitrary histogram, given in constructor argument
  if(fIsEmbedded && fEmbeddingMuonWeights) {
    embeddingMuon.ensureValidity();
    int bin = fEmbeddingMuonWeights->FindFixBin(embeddingMuon.p4().Pt());
    weight *= fEmbeddingMuonWeights->GetBinContent(bin);
    fEventCounter.setWeight(weight);
  }
  cMuonWeight.increment();

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

  if(fSelectedVertexCount->value() <= 0) return true;
  cPrimaryVertex.increment();

  std::vector<TauCollection::Tau> selectedTaus;
  std::vector<TauCollection::Tau> tmp;

  if(fTaus.size() < 1) return true;
  cAllTauCandidates.increment();

  // Pre pT cut (for some reason in the region pT < 10 there is significantly more normal than embedded)
  for(size_t i=0; i<fTaus.size(); ++i) {
    TauCollection::Tau tau = fTaus.get(i);
    if(tau.p4().Pt() < 10) continue;
    if(!TauID::isolation(tau)) continue;
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
      hTau_AfterDecayModeFindingIsolation.fill(tau.p4(), weight);
    }
    tmp.push_back(tau);
  }
  selectedTaus.swap(tmp);
  tmp.clear();
  if(selectedTaus.empty()) return true;
  cDecayModeFinding.increment();
  if(atLeastOneIsolated) {
    if(theGenTau.isValid()) hGenTau_AfterDecayModeFindingIsolation.fill(theGenTau.p4(), weight);
    hVertexCount_AfterDecayModeFindingIsolation->Fill(fVertexCount->value(), weight);
  }

  // Eta cut
  atLeastOneIsolated = false;
  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];
    if(!TauID::eta(tau)) continue;

    if(TauID::isolation(tau)) {
      atLeastOneIsolated = true;
      hTau_AfterEtaCutIsolation.fill(tau.p4(), weight);
    }
    tmp.push_back(tau);
  }
  selectedTaus.swap(tmp);
  tmp.clear();
  if(selectedTaus.empty()) return true;
  cEtaCut.increment();
  if(atLeastOneIsolated) {
    hGenTau_AfterEtaCutIsolation.fill(theGenTau.p4(), weight);
    hVertexCount_AfterEtaCutIsolation->Fill(fVertexCount->value(), weight);
  }

  // Pt cut
  atLeastOneIsolated = false;
  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];
    if(!TauID::pt(tau)) continue;

    if(TauID::isolation(tau)) {
      atLeastOneIsolated = true;
      hTau_AfterPtCutIsolation.fill(tau.p4(), weight);
      hTauLeadingTrackPt_AfterPtCutIsolation->Fill(tau.leadPFChargedHadrCandP4().Pt(), weight);
    }
    tmp.push_back(tau);
  }
  selectedTaus.swap(tmp);
  tmp.clear();
  if(selectedTaus.empty()) return true;
  cPtCut.increment();
  if(atLeastOneIsolated) {
    hGenTau_AfterPtCutIsolation.fill(theGenTau.p4(), weight);
    hVertexCount_AfterPtCutIsolation->Fill(fVertexCount->value(), weight);
  }

  // Leading track pt
  atLeastOneIsolated = false;
  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];
    if(!TauID::leadingChargedHadrCandPt(tau)) continue;
    tmp.push_back(tau);

    if(TauID::isolation(tau)) {
      atLeastOneIsolated = true;
      hTau_AfterLeadingTrackPtCutIsolation.fill(tau.p4(), weight);
    }
  }
  selectedTaus.swap(tmp);
  tmp.clear();
  if(selectedTaus.empty()) return true;
  cLeadingTrackPtCut.increment();
  if(atLeastOneIsolated) {
    hGenTau_AfterLeadingTrackPtCutIsolation.fill(theGenTau.p4(), weight);
  }

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
  atLeastOneIsolated = false;
  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];
    if(!TauID::againstElectron(tau)) continue;
    tmp.push_back(tau);

    if(TauID::isolation(tau)) {
      atLeastOneIsolated = true;
      hTau_AfterAgainstElectronIsolation.fill(tau.p4(), weight);
    }
  }
  selectedTaus.swap(tmp);
  tmp.clear();
  if(selectedTaus.empty()) return true;
  cAgainstElectron.increment();
  if(atLeastOneIsolated) {
    hGenTau_AfterAgainstElectronIsolation.fill(theGenTau.p4(), weight);
  }

  // Against muon
  atLeastOneIsolated = false;
  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];
    if(!TauID::againstMuon(tau)) continue;
    tmp.push_back(tau);

    if(TauID::isolation(tau)) {
      atLeastOneIsolated = true;
      hTau_AfterAgainstMuonIsolation.fill(tau.p4(), weight);
    }
  }
  selectedTaus.swap(tmp);
  tmp.clear();
  if(selectedTaus.empty()) return true;
  cAgainstMuon.increment();
  if(atLeastOneIsolated) {
    hGenTau_AfterAgainstMuonIsolation.fill(theGenTau.p4(), weight);
  }

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

    hTau_AfterIsolation.fill(tau.p4(), weight);
    hTauDecayModeAll_AfterIsolation->Fill(decayMode, weight);
    hTauDecayMode_AfterIsolation->Fill(fill, weight);

    tmp.push_back(tau);
  }
  selectedTaus.swap(tmp);
  tmp.clear();
  if(selectedTaus.empty()) return true;
  cIsolation.increment();
  hVertexCount_AfterIsolation->Fill(fVertexCount->value(), weight);
  if(theGenTau.isValid()) hGenTau_AfterIsolation.fill(theGenTau.p4(), weight);

  // One prong
  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];
    if(!TauID::oneProng(tau)) continue;
    tmp.push_back(tau);

    hTau_AfterOneProng.fill(tau.p4(), weight);
    hTauP_AfterOneProng->Fill(tau.p4().P(), weight);
    hTauLeadingTrackPt_AfterOneProng->Fill(tau.leadPFChargedHadrCandP4().Pt(), weight);
    hTauLeadingTrackP_AfterOneProng->Fill(tau.leadPFChargedHadrCandP4().P(), weight);
    hTauRtau_AfterOneProng->Fill(tau.rtau(), weight);
  }
  selectedTaus.swap(tmp);
  tmp.clear();
  if(selectedTaus.empty()) return true;
  cOneProng.increment();
  hGenTau_AfterOneProng.fill(theGenTau.p4(), weight);
  hVertexCount_AfterOneProng->Fill(fVertexCount->value(), weight);

  // Rtau
  for(size_t i=0; i<selectedTaus.size(); ++i) {
    TauCollection::Tau& tau = selectedTaus[i];
    if(!TauID::rtau(tau)) continue;

    hTau_AfterRtau.fill(tau.p4(), weight);

    tmp.push_back(tau);
  }
  selectedTaus.swap(tmp);
  tmp.clear();
  if(selectedTaus.empty()) return true;
  cRtau.increment();
  hVertexCount_AfterRtau->Fill(fVertexCount->value(), weight);
  if(theGenTau.isValid()) hGenTau_AfterRtau.fill(theGenTau.p4(), weight);

  // Tau ID finished

  // Trigger
  /*
  if(fIsEmbedded) {
    if(!fMuTriggerPassed->value()) return true;
  }
  */
  cMuTrigger.increment();


  if(false) {
    std::cout << "Event " << fEventInfo.event() << ":" << fEventInfo.lumi() << ":" << fEventInfo.run() << std::endl;
    for(size_t i=0; i< selectedTaus.size(); ++i) {
      TauCollection::Tau& tau = selectedTaus[i];
      std::cout << "  selected tau pt " << tau.p4().Pt() << " eta " << tau.p4().Eta() << " phi " << tau.p4().Phi() << std::endl;
      if(fIsEmbedded) {
        embeddingMuon.ensureValidity();
        double DR = ROOT::Math::VectorUtil::DeltaR(tau.p4(), embeddingMuon.p4());
        if(DR < 0.5) {
          std::cout << "    matched to embedding muon, DR " << DR << std::endl;
        }
      }
      for(size_t j=0; j<fGenTaus.size(); ++j) {
        GenParticleCollection::GenParticle gen = fGenTaus.get(j);
        double DR = ROOT::Math::VectorUtil::DeltaR(tau.p4(), gen.p4());
        if(DR < 0.5) {
          std::cout << "    matched to generator tau, DR " << DR
                    << " mother " << gen.motherPdgId()
                    << " grandmother " << gen.grandMotherPdgId()
                    << std::endl;
        }
      }
    }
  }

  return true;
}
