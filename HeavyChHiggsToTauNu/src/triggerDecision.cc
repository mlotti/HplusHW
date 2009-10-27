#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Framework/interface/TriggerNames.h"

#include<iostream>

using edm::Handle;
using edm::TriggerResults;
using edm::TriggerNames;
using edm::InputTag;
using std::vector;
using std::string;
using std::cout;
using std::endl;

bool MyEventConverter::triggerDecision(const edm::Event& iEvent){

	bool triggerdecision = false;

        Handle<TriggerResults> hltHandle;

        try{
          iEvent.getByLabel("TriggerResults",hltHandle);
        }catch(...) {;}

        if(hltHandle.isValid()){
                cout << "trigger table size " << hltHandle->size() << endl;

                TriggerNames triggerNames;
                triggerNames.init(*hltHandle);
                vector<string> hlNames = triggerNames.triggerNames();
                int n = 0;
                for(vector<string>::const_iterator i = hlNames.begin();
                                                   i!= hlNames.end(); i++){
                        cout << "trigger: " << *i << " "
                             << hltHandle->accept(n) << endl;

//			for(vector<InputTag>::const_iterator iSelect = HLTSelection.begin(); 
//                                                             iSelect!= HLTSelection.end(); iSelect++){
//				if(iSelect->label() == *i && hltHandle->accept(n) == 1) {
					triggerdecision = true;
					cout << "event triggered with " << *i << endl;
//				}
//			}
                        n++;
                }
        }
	return triggerdecision;
}
