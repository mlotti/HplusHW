#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Framework/interface/TriggerNames.h"

using edm::Handle;
using edm::TriggerResults;
using edm::TriggerNames;
using edm::InputTag;
using std::vector;
using std::string;

void MyEventConverter::getTriggerResults(const edm::Event& iEvent, const edm::InputTag& label, std::map<std::string, bool>& trigger){
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

                TriggerNames triggerNames;
                triggerNames.init(**iHandle);
                vector<string> hlNames = triggerNames.triggerNames();
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
                                if(iSelect->label() != *i) continue;
				string s_trigger = hltTableName + *i;
                                trigger[s_trigger] = (*iHandle)->accept(n);
                        }
*/
                        n++;
                }
	}
	printTrigger = false;
}
