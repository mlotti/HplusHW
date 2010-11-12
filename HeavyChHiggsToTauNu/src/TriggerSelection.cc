#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/HLTReco/interface/TriggerTypeDefs.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

#include "TH1F.h"

namespace HPlus {
  TriggerSelection::Data::Data(const TriggerPath *triggerPath, bool passedEvent):
    fTriggerPath(triggerPath), fPassedEvent(passedEvent) {}
  TriggerSelection::Data::~Data() {}
  
  TriggerSelection::TriggerSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fMetCut(iConfig.getUntrackedParameter<double>("hltMetCut")),
    fEventWeight(eventWeight),
    fTriggerPathCount(eventCounter.addSubCounter("Trigger", "Path passed")),
    fTriggerCount(eventCounter.addSubCounter("Trigger","Passed"))
  {
	std::vector<std::string> paths = iConfig.getUntrackedParameter<std::vector<std::string> >("triggers");
    	for(size_t i = 0; i < paths.size(); ++i){
      		TriggerPath* path = new TriggerPath(paths[i],eventCounter);
		triggerPaths.push_back(path);
    	}

        edm::Service<TFileService> fs;
        hHltMet = fs->make<TH1F>("hlt_met", "hlt_met", 100, 0., 100.);

  }

  TriggerSelection::~TriggerSelection() {
	for(std::vector<TriggerPath* >::const_iterator i = triggerPaths.begin(); i != triggerPaths.end(); ++i) delete *i;
  }

  TriggerSelection::Data TriggerSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
	bool passEvent = false;
	TriggerPath* returnPath = NULL;

        edm::Handle<pat::TriggerEvent> trigger;
        iEvent.getByLabel(fSrc, trigger);

	for(std::vector<TriggerPath* >::const_iterator i = triggerPaths.begin(); i != triggerPaths.end(); ++i){
		if((*i)->analyze(*trigger)) {
			passEvent = true;
			returnPath = *i;
		}
	}

        // Cut on HLT MET
        if(passEvent) {
          increment(fTriggerPathCount);

          pat::TriggerObjectRefVector hltMets = trigger->objects(trigger::TriggerMET);
          // precaution
          if(hltMets.size() != 1)
            throw cms::Exception("LogicError") << "Size of HLT MET collection is " << hltMets.size() << " instead of 1" << std::endl;
          pat::TriggerObjectRef hltMet = hltMets[0];
          hHltMet->Fill(hltMet->et(), fEventWeight.getWeight());
          if(hltMet->et() <= fMetCut)
            passEvent = false;
        }
 
        if(passEvent) increment(fTriggerCount);
	return Data(returnPath, passEvent);
  }


  TriggerSelection::TriggerPath::TriggerPath(const std::string& path, EventCounter& eventCounter):
    fPath(path),
    fTriggerCount(eventCounter.addSubCounter("Trigger","Triggered ("+fPath+")"))
  {}

  TriggerSelection::TriggerPath::~TriggerPath() {}

  bool TriggerSelection::TriggerPath::analyze(const pat::TriggerEvent& trigger) {
    pat::TriggerPathRefVector accepted = trigger.acceptedPaths();
    for(pat::TriggerPathRefVector::const_iterator iter = accepted.begin(); iter != accepted.end(); ++iter) {
      if((*iter)->name() == fPath && (*iter)->wasAccept()) {
        increment(fTriggerCount);
        return true;
      }
    }
    return false;
  }
}
