#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Framework/interface/TriggerNames.h"

map<string,bool> MyEventConverter::getTriggerResults(const edm::Event& iEvent){

	map<string,bool> trigger;

        Handle<TriggerResults> hltHandle;

        try{
          iEvent.getByLabel(edm::InputTag("TriggerResults::HLT"),hltHandle);
        }catch(...) {;}

        if(hltHandle.isValid()){
                cout << "trigger table size " << hltHandle->size() << endl;

                TriggerNames triggerNames;
                triggerNames.init(*hltHandle);
                vector<string> hlNames = triggerNames.triggerNames();
                int n = 0;
                for(vector<string>::const_iterator i = hlNames.begin();
                                                   i!= hlNames.end(); i++){
                        //cout << "trigger: " << *i << " "
                        //     << hltHandle->accept(n) << endl;

			for(vector<InputTag>::const_iterator iSelect = HLTSelection.begin(); 
                                                             iSelect!= HLTSelection.end(); iSelect++){
				if(iSelect->label() != *i) continue;

				trigger[*i] = hltHandle->accept(n);
			}
                        n++;
                }
        }
	return trigger;
}
