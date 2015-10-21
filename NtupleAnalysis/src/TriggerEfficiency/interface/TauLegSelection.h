#ifndef TriggerEfficiency_TauLegSelection_h
#define TriggerEfficiency_TauLegSelection_h

#include "TriggerEfficiency/interface/BaseSelection.h"

#include "Math/VectorUtil.h"

class TauLegSelection : public BaseSelection {
 public:
  explicit TauLegSelection(const ParameterSet&, EventCounter&, HistoWrapper&);
  ~TauLegSelection();

  bool offlineSelection(Event&,bool pu = false);
  bool onlineSelection(Event&);

  void bookHistograms(TDirectory*);
  void print();

 private:
  WrappedTH1 *hMuPt;
  WrappedTH1 *hTauPt;
  WrappedTH1 *hInvM;
  WrappedTH1 *hMt;

  Count cTauLegAll;
  Count cTauLegMu;
  Count cTauLegTau;
  Count cTauLegInvMass;
  Count cTauLegMt;
};
TauLegSelection::TauLegSelection(const ParameterSet& setup, EventCounter& fEventCounter, HistoWrapper& histoWrapper):
  BaseSelection(histoWrapper),
  cTauLegAll(fEventCounter.addCounter("TauLeg:all")),
  cTauLegMu(fEventCounter.addCounter("TauLeg:mu")),
  cTauLegTau(fEventCounter.addCounter("TauLeg:tau")),
  cTauLegInvMass(fEventCounter.addCounter("TauLeg:invMass")),
  cTauLegMt(fEventCounter.addCounter("TauLeg:Mt"))
{
  init(setup);
  //  fHistoWrapper = histoWrapper;
}
TauLegSelection::~TauLegSelection(){}

void TauLegSelection::bookHistograms(TDirectory* dir){
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kVital, dir, "Histograms");
  hMuPt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "mupt", "mupt", 200, 0, 200.0);
  hTauPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "taupt", "taupt", 200, 0, 200.0);
  hInvM  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "InvMass", "InvMass", 200, 0, 200.0);
  hMt    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Mt", "Mt", 200, 0, 200.0);
}

void TauLegSelection::print(){
  std::cout << "        Tau leg: all events    " << cTauLegAll.value() << std::endl;
  std::cout << "        Tau leg: mu selection  " << cTauLegMu.value() << std::endl;
  std::cout << "        Tau leg: tau selection " << cTauLegTau.value() << std::endl;
  std::cout << "        Tau leg: muTauInvMass  " << cTauLegInvMass.value() << std::endl;
  std::cout << "        Tau leg: muMetMt       " << cTauLegMt.value() << std::endl;
}

bool TauLegSelection::offlineSelection(Event& fEvent, bool pu){

  cTauLegAll.increment();

  boost::optional<Muon> selectedMuon;
  size_t nmuons = 0;
  for(Muon muon: fEvent.muons()) {
    if(!(muon.pt() > 17)) continue;
    if(!(std::abs(muon.eta()) < 2.1)) continue;
    if(!muon.configurableDiscriminators()) continue;
    //    if(!(muon.isGlobalMuon())) continue;

    nmuons++;
    if(!selectedMuon || (muon.pt() > selectedMuon->pt()) ) selectedMuon = muon;
  }
  if(nmuons != 1) return false;
  if(!pu) hMuPt->Fill(selectedMuon->pt());

  cTauLegMu.increment();

  boost::optional<Tau> selectedTau;
  size_t ntaus = 0;
  for(Tau tau: fEvent.taus()) {
    double drMuTau = ROOT::Math::VectorUtil::DeltaR(selectedMuon->p4(),tau.p4());
    if(drMuTau < 0.4) continue;

    if(!(tau.pt() > 20)) continue;
    if(pu && !(tau.pt() > 50)) continue;
    if(!(std::abs(tau.eta()) < 2.1)) continue;
    if(!(tau.lChTrkPt() > 20)) continue;
    if(!(tau.nProngs() == 1)) continue;
    if(!tau.decayModeFinding()) continue;
    if(!tau.configurableDiscriminators()) continue;

    ntaus++;
    if(!selectedTau || (tau.pt() > selectedTau->pt()) ) selectedTau = tau;
  }
  if(ntaus != 1) return false;
  xvariable = selectedTau->pt();
  if(pu) xvariable = fEvent.vertexInfo().value();
  if(!pu) hTauPt->Fill(selectedTau->pt());

  cTauLegTau.increment();

  double muTauInvMass = (selectedMuon->p4() + selectedTau->p4()).M();
  if(!pu) hInvM->Fill(muTauInvMass);
  //  std::cout << "check muTauInvMass " << selectedMuon->pt() << " " << selectedTau->pt() << " " << muTauInvMass << std::endl;
  if(!(muTauInvMass < 80)) return false;
  
  cTauLegInvMass.increment();

  double muMetMt = sqrt( 2 * selectedMuon->pt() * fEvent.met_Type1().et() * (1-cos(selectedMuon->phi()-fEvent.met_Type1().phi())) );
  if(!pu) hMt->Fill(muMetMt);
  if(!(muMetMt < 40)) return false;

  cTauLegMt.increment();

  //bool selected = false;
  //  if(ntaus > 0 && nmuons > 0 && muTauInvMass < 80 && muMetMt < 40) selected = true;
  //  if(ntaus > 0 && nmuons > 0) selected = true;
  //return selected;
  return true;
}

bool TauLegSelection::onlineSelection(Event& fEvent){
  return fEvent.configurableTriggerDecision2();
}
#endif
