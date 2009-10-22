#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Framework/interface/TriggerNames.h"

void MyEventConverter::getTriggerResults(const edm::Event& iEvent, const edm::InputTag& label, std::map<std::string, bool>& trigger){
        Handle<TriggerResults> hltHandle;
        iEvent.getByLabel(label, hltHandle);

        if(!hltHandle.isValid())
                return;
        cout << "trigger table size " << hltHandle->size() << endl;

        TriggerNames triggerNames;
        triggerNames.init(*hltHandle);
        const std::vector<std::string>& hlNames = triggerNames.triggerNames();
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
