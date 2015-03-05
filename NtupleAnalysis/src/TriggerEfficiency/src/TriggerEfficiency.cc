#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "DataFormat/interface/Event.h"

#include "TH1F.h"
#include "TDirectory.h"

#include "TriggerEfficiency/interface/taulegSelection.h"
#include "TriggerEfficiency/interface/metlegSelection.h"
//extern bool taulegSelection(Event&);
//extern bool metlegSelection(Event&);


class TriggerEfficiency: public BaseSelector {
public:
  explicit TriggerEfficiency(const ParameterSet& config);
  virtual ~TriggerEfficiency() {}

  virtual void book(TDirectory *dir) override;
  virtual void setupBranches(BranchManager& branchManager) override;
  virtual void process(Long64_t entry) override;

private:
  bool offlineSelection(std::string);

  Event fEvent;

  const std::string fOfflineSelection;

  Count cAllEvents;
  Count cSelection;
};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(TriggerEfficiency);

TriggerEfficiency::TriggerEfficiency(const ParameterSet& config):
  BaseSelector(config),
  fEvent(config),
  fOfflineSelection(config.getParameter<std::string>("offlineSelection")),
  cAllEvents(fEventCounter.addCounter("All events")),
  cSelection(fEventCounter.addCounter("Selection"))
{
  std::cout << "Offline selection " << fOfflineSelection << std::endl;
}

void TriggerEfficiency::book(TDirectory *dir) {
//  hTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt", "Tau pT", 40, 0, 400);
}

void TriggerEfficiency::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}

void TriggerEfficiency::process(Long64_t entry) {
  cAllEvents.increment();

  if(!offlineSelection(fOfflineSelection)) return;
  cSelection.increment();
}

bool TriggerEfficiency::offlineSelection(std::string selection){
  if(selection == "taulegSelection") return taulegSelection(fEvent);
  if(selection == "metlegSelection") return metlegSelection(fEvent);
  return false;
}
