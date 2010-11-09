#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"

namespace HPlus {
  TriggerSelection::Data::Data(const TriggerPath *triggerPath, bool passedEvent):
    fTriggerPath(triggerPath), fPassedEvent(passedEvent) {}
  TriggerSelection::Data::~Data() {}
  
  TriggerSelection::TriggerSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fTriggerMETEmulation(iConfig.getUntrackedParameter<edm::ParameterSet>("TriggerMETEmulation"), eventCounter, eventWeight),
    fTriggerCount(eventCounter.addSubCounter("Trigger","Passed"))
  {
	std::vector<std::string> paths = iConfig.getUntrackedParameter<std::vector<std::string> >("triggers");
    	for(size_t i = 0; i < paths.size(); ++i){
      		TriggerPath* path = new TriggerPath(iConfig,paths[i],eventCounter,eventWeight);
		triggerPaths.push_back(path);
    	}
  }

  TriggerSelection::~TriggerSelection() {
	for(std::vector<TriggerPath* >::const_iterator i = triggerPaths.begin(); i != triggerPaths.end(); ++i) delete *i;
  }

  TriggerSelection::Data TriggerSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
	bool passEvent = false;
	TriggerPath* returnPath = NULL;
	for(std::vector<TriggerPath* >::const_iterator i = triggerPaths.begin(); i != triggerPaths.end(); ++i){
		TriggerSelection::Data data = (*i)->analyze(iEvent,iSetup);
		if(data.passedEvent()) {
			passEvent = true;
			returnPath = *i;
		}
	}

        // Trigger MET emulation
	if(passEvent) {
          TriggerMETEmulation::Data triggerMETEmulationData = fTriggerMETEmulation.analyze(iEvent, iSetup);
          if(!triggerMETEmulationData.passedEvent()) passEvent = false;
	}

        if(passEvent) increment(fTriggerCount);
	return Data(returnPath, passEvent);
  }


  TriggerSelection::TriggerPath::TriggerPath(const edm::ParameterSet& iConfig, std::string path, EventCounter& eventCounter, EventWeight& eventWeight):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fPath(path),
    fTriggerCount(eventCounter.addSubCounter("Trigger","Triggered ("+fPath+")")),
    fEventWeight(eventWeight)
  {}

  TriggerSelection::TriggerPath::~TriggerPath() {}

  TriggerSelection::Data TriggerSelection::TriggerPath::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
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
