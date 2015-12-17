#ifndef TriggerEfficiency_METLegSelection_h
#define TriggerEfficiency_METLegSelection_h

#include "TriggerEfficiency/interface/TrgBaseSelection.h"
#include "EventSelection/interface/EventSelections.h"
#include "Math/VectorUtil.h"

class METLegSelection : public TrgBaseSelection {
 public:
  explicit METLegSelection(const ParameterSet&, EventCounter&, HistoWrapper&);
  ~METLegSelection();

  bool offlineSelection(Event&,Xvar);
  bool onlineSelection(Event&);

  void bookHistograms(TDirectory* dir);
  void print();

 private:
  bool caloMETSelection(Event&);
  std::string onlineselectionstr;

  TauSelection fTauSelection;
  ElectronSelection fElectronSelection;
  MuonSelection fMuonSelection;
  JetSelection fJetSelection;
  BJetSelection fBJetSelection;
};

METLegSelection::METLegSelection(const ParameterSet& setup, EventCounter& fEventCounter, HistoWrapper& histoWrapper) :
  TrgBaseSelection(histoWrapper),
  fTauSelection(setup.getParameter<ParameterSet>("TauSelection")),
  fElectronSelection(setup.getParameter<ParameterSet>("ElectronSelection"),"Veto"),
  fMuonSelection(setup.getParameter<ParameterSet>("MuonSelection"),"Veto"),
  fJetSelection(setup.getParameter<ParameterSet>("JetSelection")),
  fBJetSelection(setup.getParameter<ParameterSet>("BJetSelection"))
{
  init(setup);
  onlineselectionstr = *(setup.getParameterOptional<std::string>("onlineSelection"));
}
METLegSelection::~METLegSelection(){}

void METLegSelection::bookHistograms(TDirectory* dir){}

void METLegSelection::print(){}

bool METLegSelection::offlineSelection(Event& fEvent, Xvar xvar){

  xvariable = fEvent.met_Type1().et();
  if(xvar == pu) xvariable = fEvent.vertexInfo().value();

  const TauSelection::Data tauData = fTauSelection.silentAnalyze(fEvent);
  if (!tauData.hasIdentifiedTaus()) return false;

  const ElectronSelection::Data eData = fElectronSelection.silentAnalyze(fEvent);
  if (eData.hasIdentifiedElectrons()) return false;

  const MuonSelection::Data muData = fMuonSelection.silentAnalyze(fEvent);
  if (muData.hasIdentifiedMuons()) return false;
  
  const JetSelection::Data jetData = fJetSelection.silentAnalyze(fEvent, tauData.getSelectedTau());
  if (!jetData.passedSelection()) return false;
  
  const BJetSelection::Data bjetData = fBJetSelection.silentAnalyze(fEvent, jetData);
  if (!bjetData.passedSelection()) return false;

  return true;
  /*
  std::vector<Tau> selectedTaus;
  for(Tau tau: fEvent.taus()) {
    if(!(tau.pt() > 41)) continue;
    if(!(std::abs(tau.eta()) < 2.1)) continue;
    //    if(!(tau.lChTrkPt() > 20)) continue;
    if(!(tau.nProngs() == 1)) continue;
    if(!tau.decayModeFinding()) continue;
    if(!tau.configurableDiscriminators()) continue;
    
    selectedTaus.push_back(tau);
  }
  size_t ntaus = selectedTaus.size();

  size_t njets = 0;
  for(Jet jet: fEvent.jets()) {
    bool skipJet = false;
    for(std::vector<Tau>::iterator i = selectedTaus.begin(); i!= selectedTaus.end(); ++i){
      double deltaR = ROOT::Math::VectorUtil::DeltaR(jet.p4(),i->p4());
      if(deltaR < 0.5) skipJet = true;
    }
    if(skipJet) continue;
    if(!(jet.pt() > 30)) continue;
    //    if(!jet.PUIDtight()) continue;

    ++njets;
  }

  size_t nmuons = 0;
  for(Muon muon: fEvent.muons()) {
    if(muon.pt() > 15 && std::abs(muon.eta()) < 2.1)
      ++nmuons;
  }

  size_t nelectrons = 0;
  for(Electron electron: fEvent.electrons()) {
    if(electron.pt() > 15 && std::abs(electron.eta()) < 2.4)
      ++nelectrons;
  }

  bool selected = false;
  //  if(ntaus > 0 && njets > 2 && nmuons == 0 && nelectrons == 0) selected = true;
  //  if(ntaus > 0) selected = true;
  if(ntaus > 0 && njets > 2) selected = true;
  return selected;
  */
}
bool METLegSelection::onlineSelection(Event& fEvent){
  if(fEvent.configurableTrigger2IsEmpty()) return caloMETSelection(fEvent);
  bool hltdecision = fEvent.configurableTriggerDecision2();
  //  std::cout << "check METLegSelection::onlineSelection " << hltdecision << " " << fEvent.L1met().et() << std::endl;
return hltdecision;
  double L1METcut  = 50;
  if(onlineselectionstr == "MET120") L1METcut = 70;
  double l1MET = fEvent.L1met().et();
  return l1MET > L1METcut && hltdecision;
}

bool METLegSelection::caloMETSelection(Event& fEvent){
  double L1METcut  = 50;
  double HLTMETcut = 80;
  if(onlineselectionstr == "MET120") {
    L1METcut = 70;
    HLTMETcut = 120;
  }
  double l1MET = fEvent.L1met().et();
  double caloMET = fEvent.calomet().et();
  return l1MET > L1METcut && caloMET > HLTMETcut;
  //  return caloMET > HLTMETcut;
}

#endif
