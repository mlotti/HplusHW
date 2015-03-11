#include "BaseSelector.h"
#include "Branches.h"
#include "Configuration.h"

#include "TDirectory.h"
#include "TH1F.h"
#include "Math/VectorUtil.h"

#include<iostream>
#include<stdexcept>
#include<cstdlib>

class EmbeddingDebugTauAnalysisSelector: public BaseSelector {
public:
  EmbeddingDebugTauAnalysisSelector(const std::string& puWeight = "");
  ~EmbeddingDebugTauAnalysisSelector();

  void setOutput(TDirectory *dir);
  void setupBranches(BranchManager& branchManager);
  bool process(Long64_t entry);

private:
  // Input
  EventInfo fEventInfo;
  GenParticleCollection fGenTopWDecays;
  GenParticleCollection fGenTaus;
  MuonCollection fMuons;

  std::string fPuWeightName;
  Branch<double> *fPuWeight;
  Branch<unsigned> *fSelectedVertexCount;
  Branch<unsigned> *fVertexCount;

  // Output
  // Counts
  EventCounter::Count cAll;
  EventCounter::Count cOneTau;
  EventCounter::Count cMuonVeto;

  // Histograms
  struct Kinematics {
    Kinematics(): hPt(0), hEta(0), hPhi(0) {}

    void book(const std::string& prefix) {
      hPt = makeTH<TH1F>((prefix+"_pt").c_str(), "Pt", 400, 0, 400);
      hEta = makeTH<TH1F>((prefix+"_eta").c_str(), "Eta", 44, -2.1, 2.1);
      hPhi = makeTH<TH1F>((prefix+"_phi").c_str(), "Phi", 128, -3.2, 3.2);
    }

    void fill(const math::XYZTLorentzVector& p4, double weight=1.0) {
      hPt->Fill(p4.Pt(), weight);
      hEta->Fill(p4.Eta(), weight);
      hPhi->Fill(p4.Phi(), weight);
    }

    TH1 *hPt;
    TH1 *hEta;
    TH1 *hPhi;
  };

  Kinematics hGenTau;
  Kinematics hGenTau_AfterMuonVeto;
};


EmbeddingDebugTauAnalysisSelector::EmbeddingDebugTauAnalysisSelector(const std::string& puWeight):
  BaseSelector(),
  fGenTopWDecays("genttbarwdecays"),
  fGenTaus("gentaus", true), // is tau
  fPuWeightName(puWeight.empty() ? "" : "weightPileup_"+puWeight),
  cAll(fEventCounter.addCounter("All events")),
  cOneTau(fEventCounter.addCounter("= 1 gen tau")),
  cMuonVeto(fEventCounter.addCounter("reco muon veto"))
{}
EmbeddingDebugTauAnalysisSelector::~EmbeddingDebugTauAnalysisSelector() {}

void EmbeddingDebugTauAnalysisSelector::setOutput(TDirectory *dir) {
  if(dir)
    dir->cd();

  hGenTau.book("gentau");
  hGenTau_AfterMuonVeto.book("gentau_afterMuonVeto");
}

void EmbeddingDebugTauAnalysisSelector::setupBranches(BranchManager& branchManager) {
  fEventInfo.setupBranches(branchManager);
  if(isMC()) {
    fGenTopWDecays.setupBranches(branchManager);
    fGenTaus.setupBranches(branchManager);
  }
  fMuons.setupBranches(branchManager, isMC());
  if(!fPuWeightName.empty())
    branchManager.book(fPuWeightName, &fPuWeight);

  branchManager.book("selectedPrimaryVertex_count", &fSelectedVertexCount);
  branchManager.book("goodPrimaryVertex_count", &fVertexCount);
}

bool EmbeddingDebugTauAnalysisSelector::process(Long64_t entry) {
  double weight = 1.0;
  if(!fPuWeightName.empty()) {
    weight *= fPuWeight->value();
  }
  fEventCounter.setWeight(weight);

  cAll.increment();

  if(isMC()) {
    // Find the tau from t->W->tau
    GenParticleCollection::GenParticle genTau;

    for(size_t i=0; i<fGenTopWDecays.size(); ++i) {
      GenParticleCollection::GenParticle gen = fGenTopWDecays.get(i);
      if(std::abs(gen.pdgId()) == 15 && gen.p4().Pt() > 41 && std::abs(gen.p4().Eta()) < 2.1) {
        if(genTau.isValid()) // > 1 taus
          return true;
        genTau = gen;
      }
    }
    if(!genTau.isValid()) // = 0 taus
      return true;

    cOneTau.increment();
    hGenTau.fill(genTau.p4(), weight);

    // Find the more proper "generator tau" to access the daughter of it
    GenParticleCollection::GenParticle genTmp;
    for(size_t i=0; i<fGenTaus.size(); ++i) {
      GenParticleCollection::GenParticle gen = fGenTaus.get(i);
      double DR = ROOT::Math::VectorUtil::DeltaR(genTau.p4(), gen.p4());
      if(DR < 0.01) {
        if(genTmp.isValid())
          throw std::runtime_error("WTF, two gen taus corresponding to the one from W?");
        genTmp = gen;
      }
    }
    if(!genTmp.isValid())
      throw std::runtime_error("WTF, no gen tau corresponding to the one from W?");

    // Reject events with reco muons within pt,eta acceptance.
    // However, do not consider muons near tau->mu decay
    for(size_t i=0; i<fMuons.size(); ++i) {
      MuonCollection::Muon muon = fMuons.get(i);
      if(std::abs(genTmp.daughterPdgId()) == 13 && ROOT::Math::VectorUtil::DeltaR(genTmp.visibleP4(), muon.p4()) < 0.5)
        continue;

      if(muon.p4().Pt() > 41 && std::abs(muon.p4().Eta()) < 2.1)
        return true;
    }

    cMuonVeto.increment();
    hGenTau_AfterMuonVeto.fill(genTau.p4(), weight);

  }

  return true;
}
