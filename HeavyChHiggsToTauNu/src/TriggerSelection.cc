#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"

namespace HPlus {

  TriggerSelection::TriggerSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fPath(iConfig.getUntrackedParameter<std::string>("trigger")),
    fTriggerCount(eventCounter.addCounter("Triggered ("+fPath+")"))
  {}

  TriggerSelection::~TriggerSelection() {}

  bool TriggerSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<pat::TriggerEvent> trigger;
    iEvent.getByLabel(fSrc, trigger);
    
    pat::TriggerPathRefVector accepted = trigger->acceptedPaths();
    for(pat::TriggerPathRefVector::const_iterator iter = accepted.begin(); iter != accepted.end(); ++iter) {
      if((*iter)->name() == fPath && (*iter)->wasAccept()) {
        increment(fTriggerCount);
        return true;
      }
    }
    return false;
  }
}
