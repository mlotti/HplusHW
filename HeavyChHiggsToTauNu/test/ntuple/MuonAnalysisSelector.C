#include "BaseSelector.h"
#include "Branches.h"
#include "Configuration.h"

#include "TDirectory.h"
#include "TH1F.h"
#include "TH2F.h"
#include "Math/VectorUtil.h"

#include<iostream>
#include<stdexcept>
#include<cstdlib>

namespace BQuark {
  enum Mode {
    kDisabled,
    kBReject,
    kBAccept
  };

  inline Mode stringToMode(const std::string& bquarkMode) {
    if     (bquarkMode == "disabled")         return kDisabled;
    else if(bquarkMode == "breject")          return kBReject;
    else if(bquarkMode == "baccept")          return kBAccept;

    throw std::runtime_error("bquarkMode is '"+bquarkMode+"', allowed values are 'disabled', 'breject', 'baccept'");
   
  }
}

// MuonAnalysisSelector
class MuonAnalysisSelector: public BaseSelector {
public:
  MuonAnalysisSelector(const std::string& era = "", const std::string& puVariation="", const std::string& isolationMode="standard", const std::string& bquarkMode="disabled", bool topPtReweighting=true, const std::string& topPtReweightingScheme = "");
  ~MuonAnalysisSelector();

  void setOutput(TDirectory *dir);
  void setupBranches(BranchManager& branchManager);
  bool process(Long64_t entry);

private:
  struct METPhiCorr {
    METPhiCorr(double xSlope, double xOffset, double ySlope, double yOffset):
      fXSlope(xSlope), fXOffset(xOffset), fYSlope(ySlope), fYOffset(yOffset) {}
    ~METPhiCorr() {}

    math::XYZTLorentzVector correct(const math::XYZTLorentzVector& met, double nVertex) const {
      double x = met.Px() - nVertex*fXSlope + fXOffset;
      double y = met.Py() - nVertex*fYSlope + fYOffset;

      return math::XYZTLorentzVector(x, y, 0, std::sqrt(x*x + y*y));
    }

  private:
    const double fXSlope, fXOffset, fYSlope, fYOffset;
  };

  // Input
  EventInfo fEventInfo;
  EmbeddingMuonCollection fMuons;
  //ElectronCollection fElectrons;
  JetCollection fJets;
  Branch<math::XYZTLorentzVector> *fRawMet;
  Branch<math::XYZTLorentzVector> *fType1Met;

  const std::string fDataEra;
  const std::string fPuVariation;
  Branch<double> *fPuWeight;
  Branch<double> *fWJetsWeight;
  Branch<double> *fTopPtWeight;
  Branch<unsigned> *fSelectedVertexCount;
  Branch<unsigned> *fVertexCount;
  Branch<unsigned> *fGenNumberBQuarks;

  Branch<bool> *fElectronVetoPassed;
  Branch<bool> *fMETNoiseFiltersPassed;

  const EmbeddingMuonIsolation::Mode fIsolationMode;
  const BQuark::Mode fBQuarkMode;
  const bool fTopPtReweighting;
  std::string fTopPtReweightingScheme;
  METPhiCorr *fMETPhiCorr;

  TH1 *makePt(const char *name);
  TH1 *makeEta(const char *name);
  TH1 *makePhi(const char *name);
  TH1 *makeIso(const char *name);
  TH1 *makeVertexCount(const char *name);
  TH1 *makeMET(const char *name);

  // Output
  // Counts
  EventCounter::Count cAll;
  EventCounter::Count cBQuark;
  EventCounter::Count cMETNoiseFilters;
  EventCounter::Count cMuonKinematics;
  EventCounter::Count cMuonTriggerMatched;
  EventCounter::Count cMuonDB;
  EventCounter::Count cMuonIsolation;
  EventCounter::Count cMuonExactlyOne;
  EventCounter::Count cMuonTrigEff;
  EventCounter::Count cMuonIdEff;
  EventCounter::Count cMuonVeto;
  EventCounter::Count cElectronVeto;
  EventCounter::Count cJetSelection;
  EventCounter::Count cBTagSF;
  EventCounter::Count cBTag0;
  EventCounter::Count cBTag1;
  EventCounter::Count cBTag2;
  EventCounter::Count cBTagging;

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

  TH1 *hSelectedMuonEta_AfterJetSelection;
  TH1 *hSelectedMuonPhi_AfterJetSelection;
  //TH2 *hSelectedMuonPtEta_AfterJetSelection;

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
  TH1 *hType1Met_AfterJetSelection;
  TH1 *hType1MetPhi_AfterJetSelection;
  TH1 *hTransverseMassRawMet_AfterJetSelection;
  TH1 *hTransverseMassType1Met_AfterJetSelection;
  TH1 *hVertexCount_AfterJetSelection;
  TH1 *hNBJets_AfterJetSelection;

  TH1 *hMetCorrX;
  TH1 *hMetCorrY;

  TH1 *hSelectedMuonPt_AfterBTag0;
  TH1 *hType1Met_AfterBTag0;
  TH1 *hTransverseMassType1Met_AfterBTag0;

  TH1 *hSelectedMuonPt_AfterBTag1;
  TH1 *hType1Met_AfterBTag1;
  TH1 *hTransverseMassType1Met_AfterBTag1;

  TH1 *hSelectedMuonPt_AfterBTag2;
  TH1 *hType1Met_AfterBTag2;
  TH1 *hTransverseMassType1Met_AfterBTag2;

  TH1 *hSelectedMuonPt_AfterBTagging;
  TH1 *hType1Met_AfterBTagging;
  TH1 *hType1MetPhi_AfterBTagging;
  TH1 *hTransverseMassType1Met_AfterBTagging;
};

MuonAnalysisSelector::MuonAnalysisSelector(const std::string& era, const std::string& puVariation, const std::string& isolationMode, const std::string& bquarkMode, bool topPtReweighting, const std::string& topPtReweightingScheme):
  BaseSelector(),
  fDataEra(era),
  fPuVariation(puVariation),
  fIsolationMode(EmbeddingMuonIsolation::stringToMode(isolationMode)),
  fBQuarkMode(BQuark::stringToMode(bquarkMode)),
  fTopPtReweighting(topPtReweighting),
  fTopPtReweightingScheme(topPtReweightingScheme.empty() ? topPtReweightingScheme : "_"+topPtReweightingScheme),
  fMETPhiCorr(0),
  cAll(fEventCounter.addCounter("All events")),
  cBQuark(fEventCounter.addCounter("B-quark MC filter")),
  cMETNoiseFilters(fEventCounter.addCounter("MET noise filters (data)")),
  cMuonKinematics(fEventCounter.addCounter("Muon kinematics")),
  cMuonTriggerMatched(fEventCounter.addCounter("Muon trigger matching")),
  cMuonDB(fEventCounter.addCounter("Muon dB")),
  cMuonIsolation(fEventCounter.addCounter("Muon isolation")),
  cMuonExactlyOne(fEventCounter.addCounter("Muons == 1")),
  cMuonTrigEff(fEventCounter.addCounter("Muon trigger eff SF")),
  cMuonIdEff(fEventCounter.addCounter("Muon ID eff SF")),
  cMuonVeto(fEventCounter.addCounter("Veto additional muons")),
  cElectronVeto(fEventCounter.addCounter("Electron veto")),
  cJetSelection(fEventCounter.addCounter("Jet selection")),
  cBTagSF(fEventCounter.addCounter("BTag scale factor")),
  cBTag0(fEventCounter.addCounter("BTag: 0 jets")),
  cBTag1(fEventCounter.addCounter("BTag: 1 jets")),
  cBTag2(fEventCounter.addCounter("BTag: >= 2 jets")),
  cBTagging(fEventCounter.addCounter("BTagging (>= 1 jets)"))
{}
MuonAnalysisSelector::~MuonAnalysisSelector() {
  delete fMETPhiCorr;
}

TH1 *MuonAnalysisSelector::makePt(const char *name) { return makeTH<TH1F>(name, "Muon pt", 40, 0, 400); }
TH1 *MuonAnalysisSelector::makeEta(const char *name) { return makeTH<TH1F>(name, "Eta", 50, -2.5, 2.5); }
TH1 *MuonAnalysisSelector::makePhi(const char *name) { return makeTH<TH1F>(name, "Phi", 72, -3.1415926, 3.1415926); }
TH1 *MuonAnalysisSelector::makeMET(const char *name) { return makeTH<TH1F>(name, "MET", 40, 0, 400); }
TH1 *MuonAnalysisSelector::makeIso(const char *name) { return makeTH<TH1F>(name, "Muon isolation", 50, 0, 5); }
TH1 *MuonAnalysisSelector::makeVertexCount(const char *name) { return makeTH<TH1F>(name, "Vertex count", 30, 0, 30); }

void MuonAnalysisSelector::setOutput(TDirectory *dir) {
  // exploit this function to know whether we are in MC or data
  // nbumbers from Christian's slides, I guess they're meant for 2012
  if(fDataEra.find("ABCD") == std::string::npos) {
    if(isMC()) fMETPhiCorr = new METPhiCorr(-1.99574e-2, 1.16618e-1, -1.28027e-1, 2.76366e-1);
    else       fMETPhiCorr = new METPhiCorr(3.21747e-1, 2.66312e-1, -1.74688e-1, -2.25229e-1);
  }
  else {
    if(isMC()) fMETPhiCorr = new METPhiCorr(-2.00390e-2, 1.14375e-1, -1.19791e-1, 2.13507e-1);
    else       fMETPhiCorr = new METPhiCorr(3.40559e-1, 4.23682e-1, -1.76396e-1, -4.71264e-1);
  }

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

  hSelectedMuonEta_AfterJetSelection = makeEta("selectedMuonEta_AfterJetSelection");
  hSelectedMuonPhi_AfterJetSelection = makePhi("selectedMuonPhi_AfterJetSelection");

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

  hRawMet_AfterJetSelection = makeMET("uncorrectedMet_AfterJetSelection");
  hType1Met_AfterJetSelection = makeMET("type1Met_AfterJetSelection");
  hType1MetPhi_AfterJetSelection = makePhi("type1MetPhi_AfterJetSelection");
  hTransverseMassRawMet_AfterJetSelection = makeMET("transverseMassUncorrectedMet_AfterJetSelection");
  hTransverseMassType1Met_AfterJetSelection = makeMET("transverseMassType1Met_AfterJetSelection");

  hVertexCount_AfterJetSelection = makeVertexCount("vertexCount_AfterJetSelection");
  hNBJets_AfterJetSelection = makeTH<TH1F>("nbjets_AfterJetSelection", "Number of b jets", 10, 0, 10);

  hMetCorrX = makeTH<TH1F>("metcorr_x", "MET correction X due to muon scale correction", 200, -10, 10);
  hMetCorrY = makeTH<TH1F>("metcorr_y", "MET correction Y due to muon scale correction", 200, -10, 10);

  hSelectedMuonPt_AfterBTag0 = makePt("selectedMuonPt_AfterBTag0");
  hType1Met_AfterBTag0 = makeMET("type1Met_AfterBTag0");
  hTransverseMassType1Met_AfterBTag0 = makeMET("transverseMassType1Met_AfterBTag0");

  hSelectedMuonPt_AfterBTag1 = makePt("selectedMuonPt_AfterBTag1");
  hType1Met_AfterBTag1 = makeMET("type1Met_AfterBTag1");
  hTransverseMassType1Met_AfterBTag1 = makeMET("transverseMassType1Met_AfterBTag1");

  hSelectedMuonPt_AfterBTag2 = makePt("selectedMuonPt_AfterBTag2");
  hType1Met_AfterBTag2 = makeMET("type1Met_AfterBTag2");
  hTransverseMassType1Met_AfterBTag2 = makeMET("transverseMassType1Met_AfterBTag2");

  hSelectedMuonPt_AfterBTagging = makePt("selectedMuonPt_AfterBTagging");
  hType1Met_AfterBTagging = makeMET("type1Met_AfterBTagging");
  hType1MetPhi_AfterBTagging = makePhi("type1MetPhi_AfterBTagging");
  hTransverseMassType1Met_AfterBTagging = makeMET("transverseMassType1Met_AfterBTagging");
}

void MuonAnalysisSelector::setupBranches(BranchManager& branchManager) {
  fEventInfo.setupBranches(branchManager);

  if(!fDataEra.empty()) {
    fMuons.setIdEfficiencyName("efficiency_id_"+fDataEra);
    fMuons.setTriggerEfficiencyName("efficiency_trigger");
  }
  fMuons.setupBranches(branchManager, isMC());
  //fElectrons.setupBranches(branchManager, isMC());
  fJets.setupBranches(branchManager);
  branchManager.book("selectedPrimaryVertex_count", &fSelectedVertexCount);
  branchManager.book("goodPrimaryVertex_count", &fVertexCount);
  //branchManager.book("vertex_count", &fVertexCount);
  if(isMC())
    branchManager.book("gen_number_BQuarks", &fGenNumberBQuarks);

  if(isMC()) {
    if(!fDataEra.empty()) {
      branchManager.book("weightPileup_"+fDataEra+fPuVariation, &fPuWeight);
      branchManager.book("weightWJets_"+fDataEra+fPuVariation, &fWJetsWeight);
    }
    //branchManager.book("weightTopPt"+fTopPtReweightingScheme, &fTopPtWeight);
    branchManager.book("weight"+fTopPtReweightingScheme, &fTopPtWeight);
  }

  branchManager.book("ElectronVetoPassed", &fElectronVetoPassed);
  if(isData())
    branchManager.book("METNoiseFiltersPassed", &fMETNoiseFiltersPassed);
  branchManager.book("pfMetRaw_p4", &fRawMet);
  branchManager.book("pfMetType1_p4", &fType1Met);
}

bool MuonAnalysisSelector::process(Long64_t entry) {
  double weight = 1.0;
  if(isMC()) {
    if(!fDataEra.empty()) {
      weight *= fPuWeight->value();
      weight *= fWJetsWeight->value();
    }
    if(fTopPtReweighting) {
      weight *= fTopPtWeight->value();
    }
  }
  fEventCounter.setWeight(weight);

  cAll.increment();

  if(isMC() && fBQuarkMode != BQuark::kDisabled) {
    if(fBQuarkMode == BQuark::kBAccept && fGenNumberBQuarks->value() == 0)
      return true;

    if(fBQuarkMode == BQuark::kBReject && fGenNumberBQuarks->value() > 0)
      return true;
  }
  //if(!(fVertexCount->value() <= 5)) return true;
  //if(!( 5 < fVertexCount->value() && fVertexCount->value() <= 10)) return true;
  //if(!(10 < fVertexCount->value() && fVertexCount->value() <= 15)) return true;
  //if(!(15 < fVertexCount->value())) return true;
  cBQuark.increment();

  // METNoiseFilter
  if(isData() && !fMETNoiseFiltersPassed->value()) return true;
  cMETNoiseFilters.increment();

// ---- MUON SELECTION
  size_t nmuons = fMuons.size();
  std::vector<EmbeddingMuonCollection::Muon> selectedMuons;
  std::vector<EmbeddingMuonCollection::Muon> tmp;

  // Muon kinematics
  for(size_t i=0; i<nmuons; ++i) {
    EmbeddingMuonCollection::Muon muon = fMuons.get(i);
    // Use corrected energy (MuScleFit)
    muon.setP4(muon.correctedP4());
    muon.assignP4();

    //if(muon.p4().Pt() < 250 || muon.p4().Pt() > 260) continue;
    if(!MuonID::pt(muon)) continue;
    if(!MuonID::eta(muon)) continue;
    if(muon.p4CorrectionType() != EmbeddingMuonCollection::Muon::kTuneP) {
      if(!MuonID::chi2(muon)) continue;
    }
    else {
      if(!MuonID::tunePPtError(muon)) continue;
    }
    selectedMuons.push_back(muon);
  }

  if(selectedMuons.empty()) return true;
  cMuonKinematics.increment();

  // Trigger matching
  for(size_t i=0; i<selectedMuons.size(); ++i) {
    EmbeddingMuonCollection::Muon& muon = selectedMuons[i];
    if(!muon.triggerMatched()) continue;
    tmp.push_back(muon);
  }
  selectedMuons.swap(tmp);
  tmp.clear();
  if(selectedMuons.empty()) return true;
  cMuonTriggerMatched.increment();

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

      hMuonVertexCount_AfterDB->Fill(fVertexCount->value(), weight);
      bool isMuFromW = isMC() && std::abs(muon.pdgId()) == 13 && std::abs(muon.motherPdgId()) == 24;
      if(isMuFromW)
        hMuonVertexCount_AfterDB_MuFromW->Fill(fVertexCount->value(), weight);

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
      hMuonVertexCount_AfterIsolation->Fill(fVertexCount->value(), weight);
      if(isMuFromW)
        hMuonVertexCount_AfterIsolation_MuFromW->Fill(fVertexCount->value(), weight);

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


// MUON TRIGGER&ID EFFICIENCY SCALE FACTOR
  if(isMC() && !fDataEra.empty() && selectedMuons.size() == 1) {
    weight *= selectedMuons[0].triggerEfficiency();
    fEventCounter.setWeight(weight);
  }
  cMuonTrigEff.increment();

  if(isMC() && !fDataEra.empty() && selectedMuons.size() == 1) {
    weight *= selectedMuons[0].idEfficiency();
    fEventCounter.setWeight(weight);
  }
  cMuonIdEff.increment();

  //EmbeddingMuonCollection::Muon& selectedMuon = selectedMuons[0];
  // Fill
  for(size_t i=0; i<selectedMuons.size(); ++i) {
    hSelectedMuonPt_AfterMuonSelection->Fill(selectedMuons[i].p4().Pt(), weight);
  }

// MUON VETO
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
    if(!MuonVeto::chi2(muon)) continue;
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
  */


// ELECTRON VETO
  if(!fElectronVetoPassed->value()) return true;
  cElectronVeto.increment();
  // Fill
  for(size_t i=0; i<selectedMuons.size(); ++i) {
    hSelectedMuonPt_AfterElectronVeto->Fill(selectedMuons[i].p4().Pt(), weight);
  }

// JET SELECTION
  size_t njets = fJets.size();
  size_t nselectedjets = 0;
  std::vector<JetCollection::Jet> cleanedJets;
  for(size_t i=0; i<njets; ++i) {
    JetCollection::Jet jet = fJets.get(i);

    // Clean selected muon from jet collection
    bool matches = false;
    for(size_t j=0; j<selectedMuons.size(); ++j) {
      double DR = ROOT::Math::VectorUtil::DeltaR(selectedMuons[j].p4(), jet.p4());
      if(DR < 0.5) {
        matches = true;
        break;
      }
    }
    if(matches) continue;
    cleanedJets.push_back(jet);

    if(!JetSelection::pt(jet)) continue;

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

    hSelectedMuonEta_AfterJetSelection->Fill(muon.p4().Eta(), weight);
    hSelectedMuonPhi_AfterJetSelection->Fill(muon.p4().Phi(), weight);

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


  math::XYZTLorentzVector rawMet = fRawMet->value();
  math::XYZTLorentzVector type1Met = fType1Met->value();

// MET PHI CALIBRATION
  if(true && fMETPhiCorr) {
    type1Met = fMETPhiCorr->correct(type1Met, fVertexCount->value());
  }
  // Calculate MET correction from muon correction
  if(selectedMuons[0].p4CorrectionType() != MuonCollection::Muon::kUncorrected) {
    const double mex = selectedMuons[0].originalP4().x() - selectedMuons[0].p4().x();
    const double mey = selectedMuons[0].originalP4().y() - selectedMuons[0].p4().y();
    hMetCorrX->Fill(mex, weight);
    hMetCorrY->Fill(mey, weight);
    const double x = type1Met.Px()+mex;
    const double y = type1Met.Py()+mey;
    type1Met.SetPxPyPzE(x, y, 0, std::sqrt(x*x + y*y));
  }

  hRawMet_AfterJetSelection->Fill(rawMet.Pt(), weight);
  hType1Met_AfterJetSelection->Fill(type1Met.Pt(), weight);
  hType1MetPhi_AfterJetSelection->Fill(type1Met.Phi(), weight);

  double transverseMassType1 = -1;
  if(selectedMuons.size() == 1) {
    double transverseMassRaw = std::sqrt(2 * selectedMuons[0].p4().Pt() * rawMet.Pt() * (1-std::cos(selectedMuons[0].p4().Phi()-rawMet.Phi())));
    transverseMassType1 = std::sqrt(2 * selectedMuons[0].p4().Pt() * type1Met.Pt() * (1-std::cos(selectedMuons[0].p4().Phi()-type1Met.Phi())));
    hTransverseMassRawMet_AfterJetSelection->Fill(transverseMassRaw, weight);
    hTransverseMassType1Met_AfterJetSelection->Fill(transverseMassType1, weight);
  }

// B TAGGING
  size_t nbtags = 0;
  double btagSF = 1.0;
  for(size_t i=0; i<cleanedJets.size(); ++i) {
    JetCollection::Jet& jet = cleanedJets[i];
    if(isMC())
      btagSF *= jet.btagScaleFactor();

    if(!jet.btagged()) continue;
    //if(!(jet.csv() > 0.898)) continue;
    ++nbtags;
  }
  weight *= btagSF;
  fEventCounter.setWeight(weight);
  cBTagSF.increment();
  hNBJets_AfterJetSelection->Fill(nbtags, weight);

  if(nbtags == 0) {
    cBTag0.increment();
    hSelectedMuonPt_AfterBTag0->Fill(selectedMuons[0].p4().Pt(), weight);
    hType1Met_AfterBTag0->Fill(type1Met.Pt(), weight);
    hTransverseMassType1Met_AfterBTag0->Fill(transverseMassType1, weight);
  }
  else if(nbtags == 1) {
    cBTag1.increment();
    hSelectedMuonPt_AfterBTag1->Fill(selectedMuons[0].p4().Pt(), weight);
    hType1Met_AfterBTag1->Fill(type1Met.Pt(), weight);
    hTransverseMassType1Met_AfterBTag1->Fill(transverseMassType1, weight);
  }
  else {
    cBTag2.increment();
    hSelectedMuonPt_AfterBTag2->Fill(selectedMuons[0].p4().Pt(), weight);
    hType1Met_AfterBTag2->Fill(type1Met.Pt(), weight);
    hTransverseMassType1Met_AfterBTag2->Fill(transverseMassType1, weight);
  }

  if(nbtags == 0) return true;
  cBTagging.increment();
  hSelectedMuonPt_AfterBTagging->Fill(selectedMuons[0].p4().Pt(), weight);
  hType1Met_AfterBTagging->Fill(type1Met.Pt(), weight);
  hType1MetPhi_AfterBTagging->Fill(type1Met.Phi(), weight);
  hTransverseMassType1Met_AfterBTagging->Fill(transverseMassType1, weight);

  return true;
}

