#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Framework/interface/TriggerNames.h"

map<string,bool> MyEventConverter::getTriggerResults(const edm::Event& iEvent){

	map<string,bool> trigger;

	vector<Handle<TriggerResults> > hltHandles;
	iEvent.getManyByType(hltHandles);
	cout << "check MyEventConverter::getTriggerResults " << hltHandles.size() << endl;

	for(vector<Handle<TriggerResults> >::const_iterator iHandle = hltHandles.begin();
            iHandle!= hltHandles.end(); ++iHandle){
		if((*iHandle)->size() < 10) continue;

        	const std::string hltTableName = iHandle->provenance()->processName();
        	if(printTrigger) cout << "trigger table " << hltTableName 
                                      << " size " << (*iHandle)->size() << endl;

                TriggerNames triggerNames;
                triggerNames.init(**iHandle);
                vector<string> hlNames = triggerNames.triggerNames();
                int n = 0;
                for(vector<string>::const_iterator i = hlNames.begin();
                                                   i!= hlNames.end(); i++){
                        if(printTrigger) cout << "trigger: " << *i << " " << (*iHandle)->accept(n) << endl;

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
/*
        Handle<TriggerResults> hltHandle;

//          iEvent.getByLabel(edm::InputTag("TriggerResults::HLT"),hltHandle);
	iEvent.getByLabel(triggerTable,hltHandle);

        if(hltHandle.isValid()){
                cout << "trigger table size " << hltHandle->size() << endl;

                TriggerNames triggerNames;
                triggerNames.init(*hltHandle);
                vector<string> hlNames = triggerNames.triggerNames();
                int n = 0;
                for(vector<string>::const_iterator i = hlNames.begin();
                                                   i!= hlNames.end(); i++){
                        if(printTrigger) cout << "trigger: " << *i << " " << hltHandle->accept(n) << endl;

			for(vector<InputTag>::const_iterator iSelect = HLTSelection.begin(); 
                                                             iSelect!= HLTSelection.end(); iSelect++){
				if(iSelect->label() != *i) continue;

				trigger[*i] = hltHandle->accept(n);
			}
                        n++;
                }
		printTrigger = false;
        }
*/
	return trigger;
}
