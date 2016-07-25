#include "BaseSelector.h"
#include "Branches.h"
#include "Configuration.h"

// http://www-cdf.fnal.gov/~jyhan/cms_momscl/cms_rochcor_manual.html
// http://www-cdf.fnal.gov/~jyhan/cms_momscl/cms_rochcor_wasym.html
#include "rochcor_wasym_v4.h"

#include "TDirectory.h"
#include "TH1F.h"
#include "TH2F.h"
#include "Math/VectorUtil.h"
#include "TLorentzVector.h"

#include<iostream>
#include<stdexcept>
#include<cstdlib>

class EmbeddingDebugMuonAnalysisSelector: public BaseSelector {
public:
  EmbeddingDebugMuonAnalysisSelector(const std::string& puWeight = "", const std::string& muonEff = "Run2011A");
  ~EmbeddingDebugMuonAnalysisSelector();

  void setOutput(TDirectory *dir);
  void setupBranches(BranchManager& branchManager);
  bool process(Long64_t entry);

private:
  // Input
  EventInfo fEventInfo;
  GenParticleCollection fGenTopWDecays;
  MuonCollection fMuons;

  std::string fPuWeightName;
  Branch<double> *fPuWeight;
  Branch<unsigned> *fSelectedVertexCount;
  Branch<unsigned> *fVertexCount;

  rochcor fRochcorr;

  // Output
  // Counts
  EventCounter::Count cAll;
  EventCounter::Count cGenMuons;
  EventCounter::Count cZeroMuons;
  EventCounter::Count cOneMuon;
  EventCounter::Count cMoreThanOneMuons;
  EventCounter::Count cRecoMuon;
  EventCounter::Count cRecoMuonMatched;
  EventCounter::Count cRecoMuonEff;

  // Histograms
  struct Kinematics {
    Kinematics(): hPt(0), hEta(0), hPhi(0) {}

    void book(const std::string& prefix) {
      hPt = makeTH<TH1F>((prefix+"_pt").c_str(), "Pt", 400, 0, 400);
      hEta = makeTH<TH1F>((prefix+"_eta").c_str(), "Eta", 44, -2.1, 2.1);
      hPhi = makeTH<TH1F>((prefix+"_phi").c_str(), "Phi", 128, -3.2, 3.2);
    }

    template <typename T>
    void fill(const T& p4, double weight=1.0) {
      hPt->Fill(p4.Pt(), weight);
      hEta->Fill(p4.Eta(), weight);
      hPhi->Fill(p4.Phi(), weight);
    }
    void fill(const math::XYZVector& p3, double weight=1.0) {
      hPt->Fill(std::sqrt(p3.Perp2()), weight);
      hEta->Fill(p3.Eta(), weight);
      hPhi->Fill(p3.Phi(), weight);
    }

    TH1 *hPt;
    TH1 *hEta;
    TH1 *hPhi;
  };

  Kinematics hGenMuon;
  Kinematics hGenMuon_AfterRecoFound;
  Kinematics hGenMuon_AfterEffWeight;

  Kinematics hRecoMuon_AfterRecoFound;
  Kinematics hRecoMuon_AfterEffWeight;
  Kinematics hRecoMuon_AfterEffWeightScaleUp;
  Kinematics hRecoMuon_AfterEffWeightScaleDown;
  Kinematics hRecoMuon_AfterEffWeightMuscle;
  Kinematics hRecoMuon_AfterEffWeightRochester;
  Kinematics hRecoMuon_AfterEffWeightTuneP;

  TH2 *hRecoMuonResPt_AfterRecoFound;
};


EmbeddingDebugMuonAnalysisSelector::EmbeddingDebugMuonAnalysisSelector(const std::string& puWeight, const std::string& muonEff):
  BaseSelector(),
  fGenTopWDecays("genttbarwdecays"),
  fMuons(),
  fPuWeightName(puWeight.empty() ? "" : "weightPileup_"+puWeight),
  cAll(fEventCounter.addCounter("All events")),
  cGenMuons(fEventCounter.addCounter("=> 1 gen muon (no pt,eta cuts)")),
  cZeroMuons(fEventCounter.addCounter("= 0 gen muons")),
  cOneMuon(fEventCounter.addCounter("= 1 gen muon")),
  cMoreThanOneMuons(fEventCounter.addCounter("> 1 gen muons")),
  cRecoMuon(fEventCounter.addCounter("= 1 reco muon")),
  cRecoMuonMatched(fEventCounter.addCounter("reco muon gen matched")),
  cRecoMuonEff(fEventCounter.addCounter("muon id eff weighting"))
{
  fMuons.setIdEfficiencyName("efficiency_"+muonEff);
}
EmbeddingDebugMuonAnalysisSelector::~EmbeddingDebugMuonAnalysisSelector() {}

void EmbeddingDebugMuonAnalysisSelector::setOutput(TDirectory *dir) {
  if(dir)
    dir->cd();

  hGenMuon.book("genmuon");
  hGenMuon_AfterRecoFound.book("genmuon_afterRecoFound");
  hGenMuon_AfterEffWeight.book("genmuon_afterEffWeight");

  hRecoMuon_AfterRecoFound.book("recomuon_afterRecoFound");
  hRecoMuonResPt_AfterRecoFound = makeTH<TH2F>("recomuon_afterRecoFound_PtRes", "PtRes", 40,0,400, 40, -1,1);

  hRecoMuon_AfterEffWeight.book("recomuon_afterEffWeight");
  hRecoMuon_AfterEffWeightScaleUp.book("recomuon_afterEffWeightScaleUp");
  hRecoMuon_AfterEffWeightScaleDown.book("recomuon_afterEffWeightScaleDown");
  hRecoMuon_AfterEffWeightMuscle.book("recomuon_afterEffWeightMuscle");
  hRecoMuon_AfterEffWeightRochester.book("recomuon_afterEffWeightRochester");
  hRecoMuon_AfterEffWeightTuneP.book("recomuon_afterEffWeightTuneP");
}

void EmbeddingDebugMuonAnalysisSelector::setupBranches(BranchManager& branchManager) {
  fEventInfo.setupBranches(branchManager);
  if(isMC()) {
    fGenTopWDecays.setupBranches(branchManager);
  }
  fMuons.setupBranches(branchManager, isMC());

  if(!fPuWeightName.empty())
    branchManager.book(fPuWeightName, &fPuWeight);
  branchManager.book("selectedPrimaryVertex_count", &fSelectedVertexCount);
  branchManager.book("goodPrimaryVertex_count", &fVertexCount);
}

bool EmbeddingDebugMuonAnalysisSelector::process(Long64_t entry) {
  double weight = 1.0;
  if(!fPuWeightName.empty()) {
    weight *= fPuWeight->value();
  }
  fEventCounter.setWeight(weight);

  cAll.increment();

  if(isMC()) {    // Find the muon from t->W->mu
    std::vector<GenParticleCollection::GenParticle> genMuons;

    for(size_t i=0; i<fGenTopWDecays.size(); ++i) {
      GenParticleCollection::GenParticle gen = fGenTopWDecays.get(i);
      if(std::abs(gen.pdgId()) == 13)
        genMuons.push_back(gen);

    }

    if(genMuons.size() == 0)
      return true;

    cGenMuons.increment();

    // Inspect the "one" muon
    GenParticleCollection::GenParticle genMuon;
    bool moreThanOne = false;
    for(size_t i=0; i<genMuons.size(); ++i) {
      if(genMuons[i].p4().Pt() > 41 && std::abs(genMuons[i].p4().Eta()) < 2.1) {
        if(genMuon.isValid()) {// > 1 muons
          moreThanOne = true;
          break;
        }
        genMuon = genMuons[i];
      }
    }

    if(!genMuon.isValid()) {
      cZeroMuons.increment();
    }
    else if(!moreThanOne) {
      cOneMuon.increment();
      hGenMuon.fill(genMuon.p4(), weight);
    }
    else {
      cMoreThanOneMuons.increment();
    }

    // Switch thinking, throw away the previously defined generator
    // muon. Find the reco+ID muon of the event, and require that it
    // is generator matched (can be outside pt,eta acceptance)
    genMuon = GenParticleCollection::GenParticle();

    // Find reco+ID muon
    MuonCollection::Muon recoMuon;
    for(size_t i=0; i<fMuons.size(); ++i) {
      MuonCollection::Muon muon = fMuons.get(i);

      if(muon.p4().Pt() <= 41) continue;
      if(std::abs(muon.p4().Eta()) >= 2.1) continue;
      if(muon.normalizedChi2() >= 10) continue;

      if(recoMuon.isValid())
        return true;

      recoMuon = muon;

    }

    if(!recoMuon.isValid()) 
      return true;

    cRecoMuon.increment();

    // Generator matching
    double minDR = 0.1;
    for(size_t i=0; i<genMuons.size(); ++i) {
      double DR = ROOT::Math::VectorUtil::DeltaR(recoMuon.p4(), genMuons[i].p4());
      if(DR < minDR) {
        genMuon = genMuons[i];
        minDR = DR;
      }
    }

    if(!genMuon.isValid())
      return true;

    cRecoMuonMatched.increment();

    hGenMuon_AfterRecoFound.fill(genMuon.p4(), weight);
    hRecoMuon_AfterRecoFound.fill(recoMuon.p4(), weight);

    hRecoMuonResPt_AfterRecoFound->Fill(recoMuon.p4().Pt(), (recoMuon.p4().Pt()-genMuon.p4().Pt())/genMuon.p4().Pt(), weight);

    weight *= 1/recoMuon.idEfficiency();
    fEventCounter.setWeight(weight);

    cRecoMuonEff.increment();
    hGenMuon_AfterEffWeight.fill(genMuon.p4(), weight);
    hRecoMuon_AfterEffWeight.fill(recoMuon.p4(), weight);
    hRecoMuon_AfterEffWeightMuscle.fill(recoMuon.correctedP4(), weight);

    double scale = 0.007;
    math::XYZTLorentzVector muonP4Up = recoMuon.p4()*(1+scale);
    math::XYZTLorentzVector muonP4Down = recoMuon.p4()*(1-scale);
    hRecoMuon_AfterEffWeightScaleUp.fill(muonP4Up, weight);
    hRecoMuon_AfterEffWeightScaleDown.fill(muonP4Down, weight);

    TLorentzVector rochP4(recoMuon.p4().Px(), recoMuon.p4().Py(), recoMuon.p4().Pz(), recoMuon.p4().E());
    // in absence of charge, just take -1, the last argument (sysdev) does nothing
    fRochcorr.momcor_mc(rochP4, recoMuon.charge(), 0);
    hRecoMuon_AfterEffWeightRochester.fill(rochP4, weight);

    if(recoMuon.p4().Pt() < 200)
      hRecoMuon_AfterEffWeightTuneP.fill(recoMuon.p4(), weight);
    else
      hRecoMuon_AfterEffWeightTuneP.fill(recoMuon.tunePP3(), weight);
    
  }

  return true;
}
