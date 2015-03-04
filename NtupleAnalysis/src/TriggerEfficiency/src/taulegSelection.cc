#include "DataFormat/interface/Event.h"

bool taulegSelection(Event fEvent){
  std::cout << "check taulegSelection 1" << std::endl;
  Tau selectedTau;
  size_t ntaus = 0;
  for(Tau tau: fEvent.taus()) {
    if(!(tau.pt() > 20)) continue;
    if(!(std::abs(tau.eta()) < 2.1)) continue;
    if(!(tau.lTrkPt() > 20)) continue;
    if(!(tau.nProngs() == 1)) continue;
    if(!tau.decayModeFinding()) continue;

    ntaus++;
    if(tau.pt() > selectedTau.pt()) selectedTau = tau;
  }

  Muon selectedMuon;
  size_t nmuons = 0;
  for(Muon muon: fEvent.muons()) {
    if(!(muon.pt() > 15)) continue;
    if(!(muon.isGlobalMuon())) continue;

    nmuons++;
    if(muon.pt() > selectedMuon.pt()) selectedMuon = muon;
  }

  double muTauInvMass = (selectedMuon.p4() + selectedTau.p4()).M();
  double muMetMt = sqrt( 2 * selectedMuon.pt() * fEvent.met().et() * (1-cos(selectedMuon.phi()-fEvent.met().phi())) );

  bool selected = false;
  std::cout << "check " << ntaus << " " << nmuons << " " << muTauInvMass  << " " << muMetMt << std::endl; 
  if(ntaus > 0 && nmuons > 0 && muTauInvMass < 80 && muMetMt < 40) selected = true;
  return selected;
}
