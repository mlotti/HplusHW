#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TriggerSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/HLTReco/interface/TriggerTypeDefs.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

#include "TH1F.h"

namespace HPlus {
  TriggerSelection::Data::Data(const TriggerSelection *triggerSelection, const TriggerPath *triggerPath, bool passedEvent):
    fTriggerSelection(triggerSelection), fTriggerPath(triggerPath), fPassedEvent(passedEvent) {}
  TriggerSelection::Data::~Data() {}
  
  TriggerSelection::TriggerSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fMetCut(iConfig.getUntrackedParameter<double>("hltMetCut")),
    fEventWeight(eventWeight),
    fTriggerPathCount(eventCounter.addSubCounter("Trigger", "Path passed")),
    fTriggerCount(eventCounter.addSubCounter("Trigger","Passed")),
    fTriggerHltMetExistsCount(eventCounter.addSubCounter("Trigger debug", "HLT MET object exists"))
  {
	std::vector<std::string> paths = iConfig.getUntrackedParameter<std::vector<std::string> >("triggers");
    	for(size_t i = 0; i < paths.size(); ++i){
      		TriggerPath* path = new TriggerPath(paths[i],eventCounter);
		triggerPaths.push_back(path);
    	}

        edm::Service<TFileService> fs;
        hHltMetBeforeTrigger = makeTH<TH1F>(*fs, "Trigger_HLT_MET_Before_Trigger", "HLT_MET_After_Trigger;HLT_MET, GeV;N_{events} / 3 GeV", 100, 0., 300.);
        hHltMetAfterTrigger = makeTH<TH1F>(*fs, "Trigger_HLT_MET_After_Trigger", "HLT_MET_After_Trigger;HLT_MET, GeV;N_{events} / 3 GeV", 100, 0., 300.);
        hHltMetSelected = makeTH<TH1F>(*fs, "Trigger_HLT_MET_Selected", "HLT_MET_Selected;HLT_MET, GeV;N_{events} / 3 GeV", 100, 0., 300.);

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
        if(passEvent)
          increment(fTriggerPathCount);

	// Get HLT MET object but only if the trigger has been passed (otherwise it makes no sense to emulate MET)
        if(passEvent) {
          // Print all trigger object types of all triggers
          /*
          const pat::TriggerObjectCollection *objs = trigger->objects();
          for(pat::TriggerObjectCollection::const_iterator iObj = objs->begin(); iObj != objs->end(); ++iObj) {
            std::vector<int> types = iObj->triggerObjectTypes();
            if(types.empty())
              continue;
            std::cout << "Object , object types ";
            for(std::vector<int>::const_iterator iType = types.begin(); iType != types.end(); ++iType) {
              std::cout << *iType << " ";
            }
            std::cout << std::endl;
          }
          */


	  pat::TriggerObjectRefVector hltMets = trigger->objects(trigger::TriggerMET);
	  if(hltMets.size() == 0) {
	    fHltMet = pat::TriggerObjectRef();
	    if(fMetCut >= 0)
	      passEvent = false;
	  }
	  else if(hltMets.size() == 1) {
	    increment(fTriggerHltMetExistsCount);
	    fHltMet = hltMets[0];
            hHltMetBeforeTrigger->Fill(fHltMet->et(), fEventWeight.getWeight());
	    if (passEvent)
              hHltMetAfterTrigger->Fill(fHltMet->et(), fEventWeight.getWeight());

	    // Cut on HLT MET
	    if(fHltMet->et() <= fMetCut) {
	      passEvent = false;
            } else if (passEvent) {
              hHltMetSelected->Fill(fHltMet->et(), fEventWeight.getWeight());
            }
	  }
	  else
	    // precaution
	    throw cms::Exception("LogicError") << "Size of HLT MET collection is " << hltMets.size() << " instead of 1" << std::endl;
        }

        if(passEvent) increment(fTriggerCount);
	return Data(this, returnPath, passEvent);
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
	// std::cout << "*** (*iter)->name() = " << (*iter)->name() << std::endl;
        increment(fTriggerCount);
        return true;
      }
    }
    return false;
  }
}
