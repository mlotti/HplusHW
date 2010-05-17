#include "HiggsAnalysis/MyEventNTPLMaker/interface/TriggerConverter.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyEvent.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/Event.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
//#include "FWCore/Framework/interface/TriggerNames.h"
//#include "FWCore/Common/interface/TriggerNames.h"

using edm::Handle;
using edm::TriggerResults;
using edm::TriggerNames;
using edm::InputTag;
using std::vector;
using std::string;

TriggerConverter::TriggerConverter(const edm::ParameterSet& iConfig){
	triggerNames = new TriggerNames(iConfig);
	triggerDecision = false;
}

TriggerConverter::~TriggerConverter(){
	delete triggerNames;
}

bool TriggerConverter::getTriggerDecision(){
	return triggerDecision; //can only be called after TriggerConverter::getTriggerResults
}

void TriggerConverter::getTriggerResults(const edm::Event& iEvent, std::map<std::string, bool>& trigger, bool printTrigger){
        vector<Handle<TriggerResults> > hltHandles;
	iEvent.getManyByType(hltHandles);
        if(edm::isDebugEnabled())
                LogDebug("MyEventConverter") << "check MyEventConverter::getTriggerResults " << hltHandles.size() << std::endl;

	for(vector<Handle<TriggerResults> >::const_iterator iHandle = hltHandles.begin();
            iHandle!= hltHandles.end(); ++iHandle){
		if((*iHandle)->size() < 10) continue;

        	const std::string hltTableName = iHandle->provenance()->processName();
        	if(edm::isDebugEnabled() && printTrigger)
                        LogDebug("MyEventConverter") << "trigger table " << hltTableName 
                                                     << " size " << (*iHandle)->size() << std::endl;

                vector<string> hlNames = triggerNames->triggerNames();
                int n = 0;
                for(vector<string>::const_iterator i = hlNames.begin();
                                                   i!= hlNames.end(); i++){
                        if(edm::isDebugEnabled() && printTrigger)
                                LogDebug("MyEventConverter") << "trigger: " << *i << " " << (*iHandle)->accept(n) << std::endl;

			string s_trigger = hltTableName + "_" + *i;
			trigger[s_trigger] = (*iHandle)->accept(n);
			/*
                        for(vector<InputTag>::const_iterator iSelect = HLTSelection.begin();
                                                             iSelect!= HLTSelection.end(); iSelect++){
				if(iSelect->label() == *i && (*iHandle)->accept(n) == 1) {
                                        triggerDecision = true;
                                        LogDebug("MyEventConverter") << "event triggered with " << *i << std::endl;
                                }
                        }
			*/
                        n++;
                }
	}
}

void TriggerConverter::addTriggerObjects(MyEvent *saveEvent, const edm::Event& iEvent) {
  std::vector<edm::Handle<trigger::TriggerEvent> > handles;
  iEvent.getManyByType(handles);

  for(std::vector<edm::Handle<trigger::TriggerEvent> >::const_iterator iHandle = handles.begin(); iHandle != handles.end(); ++iHandle) {
    std::string name("HLTObjects_");
    name += iHandle->provenance()->processName();
    //std::cout << name << std::endl;
    const trigger::TriggerObjectCollection& objects((*iHandle)->getObjects());

    if(edm::isDebugEnabled())
      LogDebug("MyEventConverter") << "Adding " << objects.size() << " HLT objects with name " << name << std::endl;
    //std::cout << "Object collection size " << objects.size() << std::endl;

    std::vector<MyJet>& ret(saveEvent->addCollection(name));
    for(trigger::TriggerObjectCollection::const_iterator iObject = objects.begin(); iObject != objects.end(); ++iObject) {
      //std::cout << "  " << iObject->id() << "  " << iObject->pt() << std::endl;
      MyJet jet(iObject->px(), iObject->py(), iObject->pz(), iObject->energy());
      jet.type = iObject->id();
      ret.push_back(jet);
    }

    //std::cout << std::endl;
  }
  //std::cout << std::endl;
}
