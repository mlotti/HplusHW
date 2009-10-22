#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

vector<MyJet> MyEventConverter::getJets(const edm::Event& iEvent, const edm::InputTag& label) {
        vector<MyJet> jets;

        edm::Handle<reco::CaloJetCollection> calojetHandle;
        iEvent.getByLabel(label, calojetHandle);

        if(!calojetHandle.isValid())
                return jets;

        const reco::CaloJetCollection & calojets = *(calojetHandle.product());
        cout << "calojet collection size " << calojets.size() << endl;

        for(unsigned int i = 0; i < calojets.size(); ++i){
                //cout << "jet et " << calojets[i].pt() << endl;
                //cout << "tag1 et " << (tag1[i].first)->pt() << " " << tag1[i].second << endl;
                MyJet jet = myJetConverter(calojets[i]);

                for(unsigned int iBtag = 0; iBtag < btaggingAlgos.size(); ++iBtag){
                        edm::Handle<reco::JetTagCollection> btagHandle;
                        iEvent.getByLabel(btaggingAlgos[iBtag],btagHandle);
                        const reco::JetTagCollection & tag = *(btagHandle.product());

                        jet.tagInfo[btaggingAlgos[iBtag].label()] = tag[i].second;
//			jet.tagInfo[btaggingAlgos[iBtag].label()] = tag[i].discriminator();
                        //cout << "discriminator = " << tag[i].second << " " << btaggingAlgos[iBtag].label() << end$
                }
                jets.push_back(jet);
        }
        return jets;
}
