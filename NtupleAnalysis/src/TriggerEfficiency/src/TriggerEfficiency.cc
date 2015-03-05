#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "DataFormat/interface/Event.h"

#include "TH1F.h"
#include "TDirectory.h"

#include "TriggerEfficiency/interface/taulegSelection.h"
#include "TriggerEfficiency/interface/metlegSelection.h"


class TriggerEfficiency: public BaseSelector {
public:
  explicit TriggerEfficiency(const ParameterSet& config);
  virtual ~TriggerEfficiency() {}

  virtual void book(TDirectory *dir) override;
  virtual void setupBranches(BranchManager& branchManager) override;
  virtual void process(Long64_t entry) override;

private:
  bool offlineSelection(std::string);
  bool onlineSelection(std::string);

  Event fEvent;

  const std::string fOfflineSelection;
  std::vector<int> fbinning;
  std::string fxLabel;
  std::string fyLabel;

  Count cAllEvents;
  Count cSelection;

  WrappedTH1 *hNum;
  WrappedTH1 *hDen;
};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(TriggerEfficiency);

TriggerEfficiency::TriggerEfficiency(const ParameterSet& config):
  BaseSelector(config),
  fEvent(config),
  fOfflineSelection(config.getParameter<std::string>("offlineSelection")),
  fbinning(config.getParameter<std::vector<int>>("binning")),
  fxLabel(config.getParameter<std::string>("xLabel")),
  fyLabel(config.getParameter<std::string>("yLabel")),          
  cAllEvents(fEventCounter.addCounter("All events")),
  cSelection(fEventCounter.addCounter("Selection"))
{
  std::cout << "Offline selection " << fOfflineSelection << std::endl;
}

void TriggerEfficiency::book(TDirectory *dir) {

  Double_t* xbins;
  xbins = new Double_t[fbinning.size()];
  for(size_t i = 0; i < fbinning.size(); ++i){
    xbins[i] = fbinning[i];
  }

  hNum = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Numerator", "Numerator", fbinning.size()-1, xbins);
  hNum->GetXaxis()->SetTitle(fxLabel.c_str());

  hDen = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "Denominator", "Denominator", fbinning.size()-1, xbins);  
  hDen->GetXaxis()->SetTitle(fxLabel.c_str());

}

void TriggerEfficiency::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}

void TriggerEfficiency::process(Long64_t entry) {
  cAllEvents.increment();

  if(!offlineSelection(fOfflineSelection)) return;
  cSelection.increment();

  if(!onlineSelection(fOfflineSelection)){

  }
}

bool TriggerEfficiency::offlineSelection(std::string selection){
  if(selection == "taulegSelection") return taulegSelection(fEvent);
  if(selection == "metlegSelection") return metlegSelection(fEvent);
  return false;
}

bool TriggerEfficiency::onlineSelection(std::string selection){
  if(selection == "taulegSelection") return taulegOnlineSelection(fEvent);
  if(selection == "metlegSelection") return metlegOnlineSelection(fEvent);
  return false;
}
