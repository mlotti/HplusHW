#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "DataFormat/interface/Event.h"

#include "TH1F.h"
#include "TDirectory.h"

class TriggerEfficiency: public BaseSelector {
public:
  explicit TriggerEfficiency(const ParameterSet& config);
  virtual ~TriggerEfficiency() {}

  virtual void book(TDirectory *dir) override;
  virtual void setupBranches(BranchManager& branchManager) override;
  virtual void process(Long64_t entry) override;

private:
  Event fEvent;

  const float fTauPtCut;


};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(TriggerEfficiency);

TriggerEfficiency::TriggerEfficiency(const ParameterSet& config):
  BaseSelector(config),
  fEvent(config),
  fTauPtCut(config.getParameter<float>("tauPtCut"))
{}

void TriggerEfficiency::book(TDirectory *dir) {
//  hTauPt =  fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, dir, "tauPt", "Tau pT", 40, 0, 400);
}

void TriggerEfficiency::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
}

void TriggerEfficiency::process(Long64_t entry) {


}
