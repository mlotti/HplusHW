#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "DataFormat/interface/Event.h"

#include "TH1F.h"
#include "TDirectory.h"

class GeneratorComparison: public BaseSelector {
public:
  explicit GeneratorComparison(const ParameterSet& config);
  virtual ~GeneratorComparison() {}

  virtual void book(TDirectory *dir) override;
  virtual void setupBranches(BranchManager& branchManager) override;
  virtual void process(Long64_t entry) override;

private:
  Event fEvent;

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

  WrappedTH1 *hAssociatedTauPt;
  WrappedTH1 *hAssociatedTauPhi;
  WrappedTH1 *hAssociatedTauEta;

  WrappedTH1 *hAssociatedTauProng;

  WrappedTH1 *hAssociatedOneProngTauPt;
  WrappedTH1 *hAssociatedOneProngTauPhi;
  WrappedTH1 *hAssociatedOneProngTauEta;
  
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
};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(GeneratorComparison);

GeneratorComparison::GeneratorComparison(const ParameterSet& config):
  BaseSelector(config),
  fEvent(config),
  
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

  hTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, tauDir, "tauPt", "Tau pT", 40, 0, 400);
  hTauEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, tauDir, "tauEta", "Tau eta", 50, -2.5, 2.5);
  hTauPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, tauDir, "tauPhi", "Tau phi", 100, -3.1416, 3.1416);

  hAssociatedTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, hplusDir, "associatedTauPt", "Hplus tau pT", 40, 0, 400);
  hAssociatedTauEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, hplusDir, "associatedTauEta", "Hplus Tau eta", 50, -2.5, 2.5);
  hAssociatedTauPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, hplusDir, "associatedTauPhi", "Hplus Tau phi", 100, -3.1416, 3.1416);

  hAssociatedTauProng = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, hplusDir, "associatedTauProng", "Hplus Tau prong", 11, -5.5, 5.5);

  hAssociatedOneProngTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, hplusDir, "associatedOneProngTauPt", "Hplus 1-prong tau pT", 40, 0, 400);
  hAssociatedOneProngTauEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, hplusDir, "associatedOneProngTauEta", "Hplus 1-prong tau eta", 50, -2.5, 2.5);
  hAssociatedOneProngTauPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, hplusDir, "associatedOneProngTauPhi", "Hplus 1-prong tau phi", 100, -3.1416, 3.1416);

  hHplusPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, hplusDir, "hplusPt", "Hplus pT", 40, 0, 400);
  hHplusEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, hplusDir, "hplusEta", "Hplus eta", 50, -2.5, 2.5);
  hHplusPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, hplusDir, "hplusPhi", "Hplus phi", 100, -3.1416, 3.1416);

  hAssociatedBPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, hplusDir, "associatedBPt", "Associated b pT", 40, 0, 400);
  hAssociatedBEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, hplusDir, "associatedBEta", "Associated b eta", 50, -2.5, 2.5);
  hAssociatedBPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, hplusDir, "associatedBPhi", "Associated b phi", 100, -3.1416, 3.1416);

  hAssociatedTPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, hplusDir, "associatedTPt", "Associated t pT", 40, 0, 400);
  hAssociatedTEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, hplusDir, "associatedTEta", "Associated t eta", 50, -2.5, 2.5);
  hAssociatedTPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, hplusDir, "associatedTPhi", "Associated t phi", 100, -3.1416, 3.1416);

  hAssociatedSecondaryBPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, hplusDir, "associatedSecondaryBPt", "Associated secondary b pT", 40, 0, 400);
  hAssociatedSecondaryBEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, hplusDir, "associatedSecondaryBEta", "Associated secondary b eta", 50, -2.5, 2.5);
  hAssociatedSecondaryBPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, hplusDir, "associatedSecondaryBPhi", "Associated secondary b phi", 100, -3.1416, 3.1416);

  hAssociatedSecondaryTPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, hplusDir, "associatedSecondaryTPt", "Associated secondary t pT", 40, 0, 400);
  hAssociatedSecondaryTEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, hplusDir, "associatedSecondaryTEta", "Associated secondary t eta", 50, -2.5, 2.5);
  hAssociatedSecondaryTPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, hplusDir, "associatedSecondaryTPhi", "Associated secondary t phi", 100, -3.1416, 3.1416);

  hMetEt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "metEt", "Gen MET", 40, 0, 400);
  hMetPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "metPhi", "Gen MET phi", 100, -3.1416, 3.1416);
}

void GeneratorComparison::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}

void GeneratorComparison::process(Long64_t entry) {
  bool tauPtPassed = false;
  bool tauMotherPassed = false;
  bool tauProngPassed = false;
  bool tauEtaPassed = false;
  bool bjetEtPassed = false;
  bool bjetEtaPassed = false;
  bool hadronicPassed = true;

  std::vector<size_t> tauIdx;
  // weight events by the sign of the generator weight (negative weights with NLO event generators)
  double weight_sign = (fEvent.genWeight().weight() > 0) ? 1. : -1.;
  hMetEt->Fill(fEvent.genMET().et(),weight_sign);
  hMetPhi->Fill(fEvent.genMET().phi(),weight_sign);
  for(GenParticle genp: fEvent.genparticles()) {
      if(abs(genp.pdgId()) == 15) {
	  hTauPt->Fill(genp.pt(),weight_sign);
	  //hTauPt->Fill(genp.tauVisiblePt());
	  hTauEta->Fill(genp.eta(),weight_sign);
	  hTauPhi->Fill(genp.phi(),weight_sign);
	  if (abs(genp.mother()) == 37) {
	      tauMotherPassed = true;
	      hAssociatedTauPt->Fill(genp.pt(),weight_sign);
	      //hAssociatedTauPt->Fill(genp.tauVisiblePt());
	      hAssociatedTauEta->Fill(genp.eta(),weight_sign);
	      hAssociatedTauPhi->Fill(genp.phi(),weight_sign);
	      hAssociatedTauProng->Fill(genp.tauProng(),weight_sign);
	      if (genp.tauProng() == 0) hadronicPassed = false;
	      if (genp.tauProng() == 1) {
		tauProngPassed = true;
		hAssociatedOneProngTauPt->Fill(genp.pt(),weight_sign);
		//hAssociatedOneProngTauPt->Fill(genp.tauVisiblePt());
		hAssociatedOneProngTauEta->Fill(genp.eta(),weight_sign);
		hAssociatedOneProngTauPhi->Fill(genp.phi(),weight_sign);
		if (genp.pt() > fTauPtCut) {tauPtPassed = true;} 
		//if (genp.tauVisiblePt() > tauPtCut) {tauPtPassed = true;} 
		if (genp.eta() < fTauEtaCut) {tauEtaPassed = true;}
		//if (genp.tauVisibleEta() < tauEtaCut) {tauEtaPassed = true;}
	      }
	  }
      }
      if(abs(genp.pdgId()) == 37) { 
          hHplusPt->Fill(genp.pt(),weight_sign);
	  hHplusEta->Fill(genp.eta(),weight_sign);
	  hHplusPhi->Fill(genp.phi(),weight_sign);
      }

      if (abs(genp.pdgId()) == 5 && genp.associatedWithHpm() == 1) {
	if (genp.et() > fBjetEtCut) {bjetEtPassed = true;} 
      	if (genp.eta() < fBjetEtaCut) {bjetEtaPassed = true;}
	hAssociatedBPt->Fill(genp.pt(),weight_sign);
	hAssociatedBEta->Fill(genp.eta(),weight_sign);
	hAssociatedBPhi->Fill(genp.phi(),weight_sign);
      }

      if (abs(genp.pdgId()) == 5 && genp.associatedWithHpm() == 2) {
      	if (genp.et() > fBjetEtCut) {bjetEtPassed = true;} 
      	if (genp.eta() < fBjetEtaCut) {bjetEtaPassed = true;}
      	hAssociatedSecondaryBPt->Fill(genp.pt(),weight_sign);
      	hAssociatedSecondaryBEta->Fill(genp.eta(),weight_sign);
	hAssociatedSecondaryBPhi->Fill(genp.phi(),weight_sign);
      }

      if (abs(genp.pdgId()) == 6 && genp.associatedWithHpm() == 1) {
          hAssociatedTPt->Fill(genp.pt(),weight_sign);
	  hAssociatedTEta->Fill(genp.eta(),weight_sign);
	  hAssociatedTPhi->Fill(genp.phi(),weight_sign);
      }

      if (abs(genp.pdgId()) == 6 && genp.associatedWithHpm() == 2) {
          hAssociatedSecondaryTPt->Fill(genp.pt(),weight_sign);
	  hAssociatedSecondaryTEta->Fill(genp.eta(),weight_sign);
	  hAssociatedSecondaryTPhi->Fill(genp.phi(),weight_sign);
      }
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
