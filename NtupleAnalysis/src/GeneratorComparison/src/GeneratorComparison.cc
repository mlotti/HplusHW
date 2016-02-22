#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "DataFormat/interface/Event.h"
#include "MiniAOD2TTree/interface/NtupleAnalysis_fwd.h"

#include "TH1F.h"
#include "TDirectory.h"

class GeneratorComparison: public BaseSelector {
public:
  explicit GeneratorComparison(const ParameterSet& config, const TH1* skimCounters);
  virtual ~GeneratorComparison() {}

  virtual void book(TDirectory *dir) override;
  virtual void setupBranches(BranchManager& branchManager) override;
  virtual void process(Long64_t entry) override;

private:
  const std::string fParticle;

  const float fTauPtCut;
  const float fTauEtaCut;
  const float fBjetEtCut;
  const float fBjetEtaCut;

  Count cAllEvents;

  Count cTauPtSelection;
  Count cTauProngSelection;
  Count cTauMotherSelection;
  Count cTauEtaSelection;
  Count cBJetEtSelection;
  Count cBJetEtaSelection;

  Count cCombinedSelection;

  WrappedTH1 *hTauPt;
  WrappedTH1 *hTauEta;
  WrappedTH1 *hTauPhi;

  WrappedTH1 *hVisibleTauPt;
  WrappedTH1 *hVisibleTauEta;
  WrappedTH1 *hVisibleTauPhi;

  WrappedTH1 *hAssociatedTauPt;
  WrappedTH1 *hAssociatedTauPhi;
  WrappedTH1 *hAssociatedTauEta;

  WrappedTH1 *hAssociatedVisibleTauPt;
  WrappedTH1 *hAssociatedVisibleTauPhi;
  WrappedTH1 *hAssociatedVisibleTauEta;

  WrappedTH1 *hAssociatedTauProng;

  WrappedTH1 *hAssociatedOneProngTauPt;
  WrappedTH1 *hAssociatedOneProngTauPhi;
  WrappedTH1 *hAssociatedOneProngTauEta;
  
  WrappedTH1 *hAssociatedOneProngVisibleTauPt;
  WrappedTH1 *hAssociatedOneProngVisibleTauPhi;
  WrappedTH1 *hAssociatedOneProngVisibleTauEta;

  WrappedTH1 *hAssociatedThreeProngTauPt;
  WrappedTH1 *hAssociatedThreeProngTauPhi;
  WrappedTH1 *hAssociatedThreeProngTauEta;
  
  WrappedTH1 *hAssociatedThreeProngVisibleTauPt;
  WrappedTH1 *hAssociatedThreeProngVisibleTauPhi;
  WrappedTH1 *hAssociatedThreeProngVisibleTauEta;

  WrappedTH1 *hHplusPt;
  WrappedTH1 *hHplusEta;
  WrappedTH1 *hHplusPhi;

  WrappedTH1 *hAssociatedBPt;
  WrappedTH1 *hAssociatedBEta;
  WrappedTH1 *hAssociatedBPhi;

  WrappedTH1 *hAssociatedTPt;
  WrappedTH1 *hAssociatedTEta;
  WrappedTH1 *hAssociatedTPhi;

  // "secondary" associated particles: the non-associated t-quark from ttbar (light H+) and the b-jet from associated t-quark (heavy H+)
  WrappedTH1 *hAssociatedSecondaryBPt;
  WrappedTH1 *hAssociatedSecondaryBEta;
  WrappedTH1 *hAssociatedSecondaryBPhi;

  WrappedTH1 *hAssociatedSecondaryTPt;
  WrappedTH1 *hAssociatedSecondaryTEta;
  WrappedTH1 *hAssociatedSecondaryTPhi;

  WrappedTH1 *hMetEt;
  WrappedTH1 *hMetPhi;
  
  WrappedTH1 *hTauRtau1Pr0Pizero;
  WrappedTH1 *hTauRtau1Pr1Pizero;
  WrappedTH1 *hTauRtau1Pr2Pizero;
  WrappedTH1 *hTauRtau3Pr0Pizero;
  WrappedTH1 *hTauRtau3Pr1Pizero;
  
  WrappedTH1 *hTauSpinEffects1Pr0Pizero;
  WrappedTH1 *hTauSpinEffects1Pr1Pizero;
  WrappedTH1 *hTauSpinEffects1Pr2Pizero;
  WrappedTH1 *hTauSpinEffects3Pr0Pizero;
  WrappedTH1 *hTauSpinEffects3Pr1Pizero;
   
  WrappedTH1 *hWTauRtau1Pr0Pizero;
  WrappedTH1 *hWTauRtau1Pr1Pizero;
  WrappedTH1 *hWTauRtau1Pr2Pizero;
  WrappedTH1 *hWTauRtau3Pr0Pizero;
  WrappedTH1 *hWTauRtau3Pr1Pizero;
  
  WrappedTH1 *hWTauSpinEffects1Pr0Pizero;
  WrappedTH1 *hWTauSpinEffects1Pr1Pizero;
  WrappedTH1 *hWTauSpinEffects1Pr2Pizero;
  WrappedTH1 *hWTauSpinEffects3Pr0Pizero;
  WrappedTH1 *hWTauSpinEffects3Pr1Pizero; 
};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(GeneratorComparison);

GeneratorComparison::GeneratorComparison(const ParameterSet& config, const TH1* skimCounters):
  BaseSelector(config, skimCounters),
  
  fTauPtCut(config.getParameter<float>("tauPtCut")),
  fTauEtaCut(config.getParameter<float>("tauEtaCut")),
  fBjetEtCut(config.getParameter<float>("bjetEtCut")),
  fBjetEtaCut(config.getParameter<float>("bjetEtaCut")),

  cAllEvents(fEventCounter.addCounter("All events")),

  cTauPtSelection(fEventCounter.addCounter("Tau pt selection")),
  cTauProngSelection(fEventCounter.addCounter("Tau prong selection")),
  cTauMotherSelection(fEventCounter.addCounter("Tau mother selection")),
  cTauEtaSelection(fEventCounter.addCounter("Tau eta selection")),
  cBJetEtSelection(fEventCounter.addCounter("B-jet pt  selection")),
  cBJetEtaSelection(fEventCounter.addCounter("B-jet eta selection")),

  cCombinedSelection(fEventCounter.addCounter("Combined selection"))
{}

void GeneratorComparison::book(TDirectory *dir) {
  TDirectory *tauDir = dir->mkdir("Taus");
  TDirectory *hplusDir = dir->mkdir("Hplus");

  hTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, tauDir, "tauPt", "Tau pT", 40, 0, 400);
  hTauEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, tauDir, "tauEta", "Tau eta", 50, -2.5, 2.5);
  hTauPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, tauDir, "tauPhi", "Tau phi", 100, -3.1416, 3.1416);

  hVisibleTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, tauDir, "visibleTauPt", "Tau pT", 40, 0, 400);
  hVisibleTauEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, tauDir, "visibleTauEta", "Tau eta", 50, -2.5, 2.5);
  hVisibleTauPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, tauDir, "visibleTauPhi", "Tau phi", 100, -3.1416, 3.1416);

  hAssociatedTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedTauPt", "Hplus tau pT", 40, 0, 400);
  hAssociatedTauEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedTauEta", "Hplus Tau eta", 50, -2.5, 2.5);
  hAssociatedTauPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedTauPhi", "Hplus Tau phi", 100, -3.1416, 3.1416);

  hAssociatedVisibleTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedVisibleTauPt", "Hplus tau pT", 40, 0, 400);
  hAssociatedVisibleTauEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedVisibleTauEta", "Hplus Tau eta", 50, -2.5, 2.5);
  hAssociatedVisibleTauPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedVisibleTauPhi", "Hplus Tau phi", 100, -3.1416, 3.1416);

  hHplusPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "hplusPt", "Hplus pT", 40, 0, 400);
  hHplusEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "hplusEta", "Hplus eta", 50, -2.5, 2.5);
  hHplusPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "hplusPhi", "Hplus phi", 100, -3.1416, 3.1416);

  hAssociatedTauProng = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedTauProng", "Hplus Tau prong", 11, -5.5, 5.5);

  hAssociatedOneProngTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedOneProngTauPt", "Hplus 1-prong tau pT", 40, 0, 400);
  hAssociatedOneProngTauEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedOneProngTauEta", "Hplus 1-prong tau eta", 50, -2.5, 2.5);
  hAssociatedOneProngTauPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedOneProngTauPhi", "Hplus 1-prong tau phi", 100, -3.1416, 3.1416);

  hAssociatedOneProngVisibleTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedOneProngVisibleTauPt", "Hplus 1-prong tau pT", 40, 0, 400);
  hAssociatedOneProngVisibleTauEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedOneProngVisibleTauEta", "Hplus 1-prong tau eta", 50, -2.5, 2.5);
  hAssociatedOneProngVisibleTauPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedOneProngVisibleTauPhi", "Hplus 1-prong tau phi", 100, -3.1416, 3.1416);

  hAssociatedThreeProngTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedThreeProngTauPt", "Hplus 1-prong tau pT", 40, 0, 400);
  hAssociatedThreeProngTauEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedThreeProngTauEta", "Hplus 1-prong tau eta", 50, -2.5, 2.5);
  hAssociatedThreeProngTauPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedThreeProngTauPhi", "Hplus 1-prong tau phi", 100, -3.1416, 3.1416);

  hAssociatedThreeProngVisibleTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedThreeProngVisibleTauPt", "Hplus 1-prong tau pT", 40, 0, 400);
  hAssociatedThreeProngVisibleTauEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedThreeProngVisibleTauEta", "Hplus 1-prong tau eta", 50, -2.5, 2.5);
  hAssociatedThreeProngVisibleTauPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedThreeProngVisibleTauPhi", "Hplus 1-prong tau phi", 100, -3.1416, 3.1416);

  hAssociatedBPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedBPt", "Associated b pT", 40, 0, 400);
  hAssociatedBEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedBEta", "Associated b eta", 50, -2.5, 2.5);
  hAssociatedBPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedBPhi", "Associated b phi", 100, -3.1416, 3.1416);

  hAssociatedTPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedTPt", "Associated t pT", 40, 0, 400);
  hAssociatedTEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedTEta", "Associated t eta", 50, -2.5, 2.5);
  hAssociatedTPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedTPhi", "Associated t phi", 100, -3.1416, 3.1416);

  hMetEt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "metEt", "Gen MET", 40, 0, 400);
  hMetPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "metPhi", "Gen MET phi", 100, -3.1416, 3.1416);

  hAssociatedSecondaryBPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedSecondaryBPt", "Associated secondary b pT", 40, 0, 400);
  hAssociatedSecondaryBEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedSecondaryBEta", "Associated secondary b eta", 50, -2.5, 2.5);
  hAssociatedSecondaryBPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedSecondaryBPhi", "Associated secondary b phi", 100, -3.1416, 3.1416);

  hAssociatedSecondaryTPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedSecondaryTPt", "Associated secondary t pT", 40, 0, 400);
  hAssociatedSecondaryTEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedSecondaryTEta", "Associated secondary t eta", 50, -2.5, 2.5);
  hAssociatedSecondaryTPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedSecondaryTPhi", "Associated secondary t phi", 100, -3.1416, 3.1416);
  
  hTauRtau1Pr0Pizero = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "tauRtau1Pr0Pizero", "tauRtau1Pr0Pizero", 60, 0.0, 1.2);
  hTauRtau1Pr1Pizero = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "tauRtau1Pr1Pizero", "tauRtau1Pr1Pizero", 60, 0.0, 1.2);  
  hTauRtau1Pr2Pizero = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "tauRtau1Pr2Pizero", "tauRtau1Pr2Pizero", 60, 0.0, 1.2);
  hTauRtau3Pr0Pizero = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "tauRtau3Pr0Pizero", "tauRtau1Pr0Pizero", 60, 0.0, 1.2);  
  hTauRtau3Pr1Pizero = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "tauRtau3Pr1Pizero", "tauRtau3Pr1Pizero", 60, 0.0, 1.2);  

  hTauSpinEffects1Pr0Pizero = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "tauSpinEffects1Pr0Pizero", "tauSpinEffects1Pr0Pizero", 60, 0.0, 1.2);
  hTauSpinEffects1Pr1Pizero = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "tauSpinEffects1Pr1Pizero", "tauSpinEffects1Pr1Pizero", 60, 0.0, 1.2);  
  hTauSpinEffects1Pr2Pizero = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "tauSpinEffects1Pr2Pizero", "tauSpinEffects1Pr2Pizero", 60, 0.0, 1.2);
  hTauSpinEffects3Pr0Pizero = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "tauSpinEffects3Pr0Pizero", "tauSpinEffects1Pr0Pizero", 60, 0.0, 1.2);  
  hTauSpinEffects3Pr1Pizero = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "tauSpinEffects3Pr1Pizero", "tauSpinEffects3Pr1Pizero", 60, 0.0, 1.2);  
  
  TDirectory *WDir = dir->mkdir("W");
  hWTauRtau1Pr0Pizero = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, WDir, "tauRtau1Pr0Pizero", "tauRtau1Pr0Pizero", 60, 0.0, 1.2);
  hWTauRtau1Pr1Pizero = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, WDir, "tauRtau1Pr1Pizero", "tauRtau1Pr1Pizero", 60, 0.0, 1.2);  
  hWTauRtau1Pr2Pizero = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, WDir, "tauRtau1Pr2Pizero", "tauRtau1Pr2Pizero", 60, 0.0, 1.2);
  hWTauRtau3Pr0Pizero = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, WDir, "tauRtau3Pr0Pizero", "tauRtau1Pr0Pizero", 60, 0.0, 1.2);  
  hWTauRtau3Pr1Pizero = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, WDir, "tauRtau3Pr1Pizero", "tauRtau3Pr1Pizero", 60, 0.0, 1.2);  

  hWTauSpinEffects1Pr0Pizero = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, WDir, "tauSpinEffects1Pr0Pizero", "tauSpinEffects1Pr0Pizero", 60, 0.0, 1.2);
  hWTauSpinEffects1Pr1Pizero = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, WDir, "tauSpinEffects1Pr1Pizero", "tauSpinEffects1Pr1Pizero", 60, 0.0, 1.2);  
  hWTauSpinEffects1Pr2Pizero = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, WDir, "tauSpinEffects1Pr2Pizero", "tauSpinEffects1Pr2Pizero", 60, 0.0, 1.2);
  hWTauSpinEffects3Pr0Pizero = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, WDir, "tauSpinEffects3Pr0Pizero", "tauSpinEffects1Pr0Pizero", 60, 0.0, 1.2);  
  hWTauSpinEffects3Pr1Pizero = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, WDir, "tauSpinEffects3Pr1Pizero", "tauSpinEffects3Pr1Pizero", 60, 0.0, 1.2);  
}

void GeneratorComparison::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}

void GeneratorComparison::process(Long64_t entry) {
  if (fEvent.isData()) return;
  
  bool tauPtPassed = false;
  bool tauMotherPassed = false;
  bool tauProngPassed = false;
  bool tauEtaPassed = false;
  bool bjetEtPassed = false;
  bool bjetEtaPassed = false;
  bool hadronicPassed = true;

  //std::vector<size_t> tauIdx;
  // Event generator weights are applied automatically through the BaseSelector
  hMetEt->Fill(fEvent.genMET().et());
  hMetPhi->Fill(fEvent.genMET().phi());
  
  // All MC taus
  for (auto& p: fEvent.genparticles().getGenTauCollection()) {
    hTauPt->Fill(p.pt());
    hTauEta->Fill(p.eta());
    hTauPhi->Fill(p.phi());
  }
  for (auto& p: fEvent.genparticles().getGenVisibleTauCollection()) {
    hVisibleTauPt->Fill(p.pt());
    hVisibleTauEta->Fill(p.eta());
    hVisibleTauPhi->Fill(p.phi());
  }
  // Tau matched to Hplus
  short myTauIndex = fEvent.genparticles().getGenTauAssociatedWithHpm();
  if (myTauIndex >= 0) {
    auto taulepton = fEvent.genparticles().getGenTauCollection()[myTauIndex];
    auto visibleTau = fEvent.genparticles().getGenVisibleTauCollection()[myTauIndex];
    // Hplus found
    tauMotherPassed = true;
    hAssociatedTauPt->Fill(taulepton.pt());
    hAssociatedTauEta->Fill(taulepton.eta());
    hAssociatedTauPhi->Fill(taulepton.phi());
    hAssociatedVisibleTauPt->Fill(visibleTau.pt());
    hAssociatedVisibleTauEta->Fill(visibleTau.eta());
    hAssociatedVisibleTauPhi->Fill(visibleTau.phi());
    auto tauprongs = fEvent.genparticles().getGenTauProngs()[myTauIndex];
    auto npizeros = fEvent.genparticles().getGenTauNpi0()[myTauIndex];
    auto rtau = fEvent.genparticles().getGenTauRtau()[myTauIndex];
    auto spinEffects = fEvent.genparticles().getGenTauSpinEffects()[myTauIndex];
    hAssociatedTauProng->Fill(tauprongs);
    if (tauprongs == 0) 
      hadronicPassed = false;
    else if (tauprongs == 1) {
      tauProngPassed = true;
      hAssociatedOneProngTauPt->Fill(taulepton.pt());
      hAssociatedOneProngTauEta->Fill(taulepton.eta());
      hAssociatedOneProngTauPhi->Fill(taulepton.phi());
      hAssociatedOneProngVisibleTauPt->Fill(visibleTau.pt());
      hAssociatedOneProngVisibleTauEta->Fill(visibleTau.eta());
      hAssociatedOneProngVisibleTauPhi->Fill(visibleTau.phi());
      if (npizeros == 0) {
        hTauRtau1Pr0Pizero->Fill(rtau);
        hTauSpinEffects1Pr0Pizero->Fill(spinEffects);
      } else if (npizeros == 1) {
        hTauRtau1Pr1Pizero->Fill(rtau);
        hTauSpinEffects1Pr1Pizero->Fill(spinEffects);
      } else if (npizeros == 2) {
        hTauRtau1Pr2Pizero->Fill(rtau);
        hTauSpinEffects1Pr2Pizero->Fill(spinEffects);
      }
    } else if (tauprongs == 3) {
      tauProngPassed = true;
      hAssociatedThreeProngTauPt->Fill(taulepton.pt());
      hAssociatedThreeProngTauEta->Fill(taulepton.eta());
      hAssociatedThreeProngTauPhi->Fill(taulepton.phi());
      hAssociatedThreeProngVisibleTauPt->Fill(visibleTau.pt());
      hAssociatedThreeProngVisibleTauEta->Fill(visibleTau.eta());
      hAssociatedThreeProngVisibleTauPhi->Fill(visibleTau.phi());
      if (npizeros == 0) {
        hTauRtau3Pr0Pizero->Fill(rtau);
        hTauSpinEffects3Pr0Pizero->Fill(spinEffects);
      } else if (npizeros == 1) {
        hTauRtau3Pr1Pizero->Fill(rtau);
        hTauSpinEffects3Pr1Pizero->Fill(spinEffects);
      }
    }
    if (tauprongs == 1 || tauprongs == 3) {
      if (visibleTau.pt() > fTauPtCut) {
        tauPtPassed = true;
      } 
      if (visibleTau.eta() < fTauEtaCut) {
        tauEtaPassed = true;
      }
    }
  }
  // H+
  if (fEvent.genparticles().getGenHplusCollection().size()) {
    auto hplus = fEvent.genparticles().getGenHplusCollection()[0];
    hHplusPt->Fill(hplus.pt());
    hHplusEta->Fill(hplus.eta());
    hHplusPhi->Fill(hplus.phi());
  }
  // Taus from W's
  for (size_t i = 0; i < fEvent.genparticles().getGenTauCollection().size(); ++i) {
    if (myTauIndex < 0 || i != static_cast<size_t>(myTauIndex)) {
      auto tauprongs = fEvent.genparticles().getGenTauProngs()[i];
      auto npizeros = fEvent.genparticles().getGenTauNpi0()[i];
      auto rtau = fEvent.genparticles().getGenTauRtau()[i];
      auto spinEffects = fEvent.genparticles().getGenTauSpinEffects()[i];
      if (tauprongs == 1) {
        if (npizeros == 0) {
          hWTauRtau1Pr0Pizero->Fill(rtau);
          hWTauSpinEffects1Pr0Pizero->Fill(spinEffects);
        } else if (npizeros == 1) {
          hWTauRtau1Pr1Pizero->Fill(rtau);
          hWTauSpinEffects1Pr1Pizero->Fill(spinEffects);
        } else if (npizeros == 2) {
          hWTauRtau1Pr2Pizero->Fill(rtau);
          hWTauSpinEffects1Pr2Pizero->Fill(spinEffects);
        }
      } else if (tauprongs == 3) {
        if (npizeros == 0) {
          hWTauRtau3Pr0Pizero->Fill(rtau);
          hWTauSpinEffects3Pr0Pizero->Fill(spinEffects);
        } else if (npizeros == 1) {
          hWTauRtau3Pr1Pizero->Fill(rtau);
          hWTauSpinEffects3Pr1Pizero->Fill(spinEffects);
        }
      }
    }
  }
  
  // b jet from H+ side
  // ok, information is lacked in gen particles, use workaround
  
  int nTopToTaus = 0;
  for (size_t i = 0; i < fEvent.genparticles().getGenTopBQuarkCollection().size(); ++i) {
    if (fEvent.genparticles().getGenTopDecayMode()[i] == kTopToTau)
      ++nTopToTaus;
  }
  // ttbar decay
  if (fEvent.genparticles().getGenTopBQuarkCollection().size() == 2 && nTopToTaus == 1) {
    for (size_t i = 0; i < fEvent.genparticles().getGenTopBQuarkCollection().size(); ++i) {
      if (fEvent.genparticles().getGenTopDecayMode()[i] == kTopToTau) {
        auto assocBjet = fEvent.genparticles().getGenTopBQuarkCollection()[i];
        if (assocBjet.pt() > fBjetEtCut) {bjetEtPassed = true;} 
        if (assocBjet.eta() < fBjetEtaCut) {bjetEtaPassed = true;}
        hAssociatedBPt->Fill(assocBjet.pt());
        hAssociatedBEta->Fill(assocBjet.eta());
        hAssociatedBPhi->Fill(assocBjet.phi());
        auto top = fEvent.genparticles().getGenTopCollection()[i];
        hAssociatedTPt->Fill(top.pt());
        hAssociatedTEta->Fill(top.eta());
        hAssociatedTPhi->Fill(top.phi());
      } else {
        auto nonAssocBjet = fEvent.genparticles().getGenTopBQuarkCollection()[i];
        if (nonAssocBjet.pt() > fBjetEtCut) {bjetEtPassed = true;} 
        if (nonAssocBjet.eta() < fBjetEtaCut) {bjetEtaPassed = true;}
        hAssociatedSecondaryBPt->Fill(nonAssocBjet.pt());
        hAssociatedSecondaryBEta->Fill(nonAssocBjet.eta());
        hAssociatedSecondaryBPhi->Fill(nonAssocBjet.phi());
        auto top = fEvent.genparticles().getGenTopCollection()[i];
        hAssociatedSecondaryTPt->Fill(top.pt());
        hAssociatedSecondaryTEta->Fill(top.eta());
        hAssociatedSecondaryTPhi->Fill(top.phi());
      }
    }
  } else if (fEvent.genparticles().getGenTopBQuarkCollection().size() == 1 && nTopToTaus == 0) {
    // just one top, assume gg->tbH+ decay
    // I.e. the one top is the secondary one
    auto nonAssocBjet = fEvent.genparticles().getGenTopBQuarkCollection()[0];
    hAssociatedSecondaryBPt->Fill(nonAssocBjet.pt());
    hAssociatedSecondaryBEta->Fill(nonAssocBjet.eta());
    hAssociatedSecondaryBPhi->Fill(nonAssocBjet.phi());
    auto top = fEvent.genparticles().getGenTopCollection()[0];
    hAssociatedSecondaryTPt->Fill(top.pt());
    hAssociatedSecondaryTEta->Fill(top.eta());
    hAssociatedSecondaryTPhi->Fill(top.phi());
    if (nonAssocBjet.pt() > fBjetEtCut) {bjetEtPassed = true;} 
    if (nonAssocBjet.eta() < fBjetEtaCut) {bjetEtaPassed = true;}
    // Find the other b jet
    // FIXME: not possible at the moment
  }

  if (hadronicPassed) {
    cAllEvents.increment();
    if (tauMotherPassed) cTauMotherSelection.increment();
    if (tauProngPassed) cTauProngSelection.increment();
    if (tauPtPassed) cTauPtSelection.increment();
    if (tauEtaPassed) cTauEtaSelection.increment();
    if (bjetEtPassed) cBJetEtSelection.increment();
    if (bjetEtaPassed) cBJetEtaSelection.increment();
    if (tauPtPassed && tauEtaPassed && bjetEtPassed && bjetEtaPassed) cCombinedSelection.increment();
  }

  fEventSaver.save();
}
