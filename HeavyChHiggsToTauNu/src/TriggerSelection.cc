#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"

namespace HPlus {
  TriggerSelection::Data::Data(const TriggerSelection *triggerSelection, bool passedEvent):
    fTriggerSelection(triggerSelection), fPassedEvent(passedEvent) {}
  TriggerSelection::Data::~Data() {}
  
  TriggerSelection::TriggerSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fPath(iConfig.getUntrackedParameter<std::string>("trigger")),
    fTriggerCount(eventCounter.addSubCounter("Trigger","Triggered ("+fPath+")")),
    fEventWeight(eventWeight)
  {}

  TriggerSelection::~TriggerSelection() {}

  TriggerSelection::Data TriggerSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    bool passEvent = false;
    edm::Handle<pat::TriggerEvent> trigger;
    iEvent.getByLabel(fSrc, trigger);
    
    pat::TriggerPathRefVector accepted = trigger->acceptedPaths();
    for(pat::TriggerPathRefVector::const_iterator iter = accepted.begin(); iter != accepted.end(); ++iter) {
      if((*iter)->name() == fPath && (*iter)->wasAccept()) {
        increment(fTriggerCount);
         passEvent = true;
      }
    }
    return Data(this, passEvent);
  }
}
