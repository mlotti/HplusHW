#ifndef TriggerEfficiency_TauLegSelection_h
#define TriggerEfficiency_TauLegSelection_h

#include "TriggerEfficiency/interface/BaseSelection.h"

class TauLegSelection : public BaseSelection {
 public:
  TauLegSelection();
  ~TauLegSelection();

  bool offlineSelection(const Event&);
  bool onlineSelection(const Event&);

 private:

};
TauLegSelection::TauLegSelection(){}
TauLegSelection::~TauLegSelection(){}

bool TauLegSelection::offlineSelection(const Event& fEvent){

  if(!this->passedCtrlTtrigger(fEvent)) return false;

  boost::optional<Tau> selectedTau;
  size_t ntaus = 0;
  for(Tau tau: fEvent.taus()) {
    if(!(tau.pt() > 20)) continue;
    if(!(std::abs(tau.eta()) < 2.1)) continue;
    if(!(tau.lTrkPt() > 20)) continue;
    if(!(tau.nProngs() == 1)) continue;
    if(!tau.decayModeFinding()) continue;

    ntaus++;
    if(!selectedTau || (tau.pt() > selectedTau->pt()) ) selectedTau = tau;
  }
  if(!selectedTau) return false;
  xvariable = selectedTau->pt();

  boost::optional<Muon> selectedMuon;
  size_t nmuons = 0;
  for(Muon muon: fEvent.muons()) {
    if(!(muon.pt() > 15)) continue;
    if(!(muon.isGlobalMuon())) continue;

    nmuons++;
    if(!selectedMuon || (muon.pt() > selectedMuon->pt()) ) selectedMuon = muon;
  }
  if(!selectedMuon) return false;

  double muTauInvMass = (selectedMuon->p4() + selectedTau->p4()).M();
  double muMetMt = sqrt( 2 * selectedMuon->pt() * fEvent.met_Type1().et() * (1-cos(selectedMuon->phi()-fEvent.met_Type1().phi())) );

  bool selected = false;
  if(ntaus > 0 && nmuons > 0 && muTauInvMass < 80 && muMetMt < 40) selected = true;
  return selected;
}
bool TauLegSelection::onlineSelection(const Event& fEvent){
  return true;
}

#endif
