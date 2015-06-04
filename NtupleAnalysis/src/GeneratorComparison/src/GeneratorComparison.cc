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

  Count cAllEvents;
  Count cWeighted;
  Count cTauSelection;
  Count cMuonVeto;
  Count cElectronVeto;
  Count cJetSelection;

  Count cCombinedSelection;;

  WrappedTH1 *hTauPt;
  WrappedTH1 *hTauEta;
  WrappedTH1 *hTauPhi;

  WrappedTH1 *hAssociatedTauPt;
  WrappedTH1 *hAssociatedTauPhi;
  WrappedTH1 *hAssociatedTauEta;
  
  WrappedTH1 *hHplusPt;
  WrappedTH1 *hHplusEta;
  WrappedTH1 *hHplusPhi;

  WrappedTH1 *hAssociatedBPt;
  WrappedTH1 *hAssociatedBEta;
  WrappedTH1 *hAssociatedBPhi;

  WrappedTH1 *hAssociatedTPt;
  WrappedTH1 *hAssociatedTEta;
  WrappedTH1 *hAssociatedTPhi;

  WrappedTH1 *hMetEt;
  WrappedTH1 *hMetPhi;
};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(GeneratorComparison);

GeneratorComparison::GeneratorComparison(const ParameterSet& config):
  BaseSelector(config),
  fEvent(config),

  fTauPtCut(config.getParameter<float>("tauPtCut")),

  cAllEvents(fEventCounter.addCounter("All events")),
  cWeighted(fEventCounter.addCounter("Weighted")),
  cTauSelection(fEventCounter.addCounter("Tau selection")),
  cMuonVeto(fEventCounter.addCounter("Muon veto")),
  cElectronVeto(fEventCounter.addCounter("Electron veto")),
  cJetSelection(fEventCounter.addCounter("Jet selection")),
  cCombinedSelection(fEventCounter.addCounter("Combined selection"))
{}

void GeneratorComparison::book(TDirectory *dir) {
  TDirectory *tauDir = dir->mkdir("Taus");
  TDirectory *hplusDir = dir->mkdir("Hplus");

  hTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, tauDir, "tauPt", "Tau pT", 40, 0, 400);
  hTauEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, tauDir, "tauEta", "Tau eta", 50, -2.5, 2.5);
  hTauPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, tauDir, "tauPhi", "Tau phi", 100, -3.1416, 3.1416);

  hAssociatedTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedTauPt", "Hplus tau pT", 40, 0, 400);
  hAssociatedTauEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedTauEta", "Hplus Tau eta", 50, -2.5, 2.5);
  hAssociatedTauPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedTauPhi", "Hplus Tau phi", 100, -3.1416, 3.1416);

  hHplusPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "hplusPt", "Hplus pT", 40, 0, 400);
  hHplusEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "hplusEta", "Hplus eta", 50, -2.5, 2.5);
  hHplusPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "hplusPhi", "Hplus phi", 100, -3.1416, 3.1416);

  hAssociatedBPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedBPt", "Associated b pT", 40, 0, 400);
  hAssociatedBEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedBEta", "Associated b eta", 50, -2.5, 2.5);
  hAssociatedBPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedBPhi", "Associated b phi", 100, -3.1416, 3.1416);

  hAssociatedTPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedTPt", "Associated t pT", 40, 0, 400);
  hAssociatedTEta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedTEta", "Associated t eta", 50, -2.5, 2.5);
  hAssociatedTPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, hplusDir, "associatedTPhi", "Associated t phi", 100, -3.1416, 3.1416);

  hMetEt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "metEt", "Gen MET", 40, 0, 400);
  hMetPhi = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "metPhi", "Gen MET phi", 100, -3.1416, 3.1416);
}

void GeneratorComparison::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}

void GeneratorComparison::process(Long64_t entry) {
  cAllEvents.increment();

  fEventWeight.multiplyWeight(0.5);
  cWeighted.increment();

  bool taupt = false;
  bool taueta = false;
  bool bpt = false;
  bool beta = false;

  double taupt_th = 41;
  double taueta_th = 2.1;
  double bet_th = 30;
  double beta_th = 2.4;

  std::vector<size_t> tauIdx;
  hMetEt->Fill(fEvent.genMET().et());
  hMetPhi->Fill(fEvent.genMET().phi());
  for(GenParticle genp: fEvent.genparticles()) {
      if(abs(genp.pdgId()) == 15) {
	  hTauPt->Fill(genp.pt());
	  hTauEta->Fill(genp.eta());
	  hTauPhi->Fill(genp.phi());
	  if (abs(genp.mother()) == 37) {
	      hAssociatedTauPt->Fill(genp.pt());
	      hAssociatedTauEta->Fill(genp.eta());
	      hAssociatedTauPhi->Fill(genp.phi());
	      if (genp.tauProng() == 1) {
		if (genp.pt() > taupt_th) {taupt = true;} 
		if (genp.eta() < taueta_th) {taueta = true;}
	      }
	  }
      }
      if(abs(genp.pdgId()) == 37) { 
          hHplusPt->Fill(genp.pt());
	  hHplusEta->Fill(genp.eta());
	  hHplusPhi->Fill(genp.phi());
      }

      if (abs(genp.pdgId()) == 5 && genp.associatedWithHpm() == 1) {
          hAssociatedBPt->Fill(genp.pt());
	  hAssociatedBEta->Fill(genp.eta());
	  hAssociatedBPhi->Fill(genp.phi());
	  if (genp.pt() > bet_th) {bpt = true;} 
	  if (genp.eta() < beta_th) {beta = true;}
      }

      if (abs(genp.pdgId()) == 6 && genp.associatedWithHpm() == 1) {
          hAssociatedTPt->Fill(genp.pt());
	  hAssociatedTEta->Fill(genp.eta());
	  hAssociatedTPhi->Fill(genp.phi());
      }
  }
  if (taupt && taueta && bpt && beta) cCombinedSelection.increment();

  fEventSaver.save();
}
