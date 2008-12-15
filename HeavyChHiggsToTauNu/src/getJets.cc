#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

vector<MyJet> MyEventConverter::getJets(const edm::Event& iEvent){
        vector<MyJet> jets;

        edm::Handle<reco::CaloJetCollection> calojetHandle;
        try{
          iEvent.getByLabel("iterativeCone5CaloJets", calojetHandle);
        }catch(...) {;}


        if(calojetHandle.isValid()){
          const reco::CaloJetCollection & calojets = *(calojetHandle.product());
          cout << "calojet collection size " << calojets.size() << endl;

          for(unsigned int i = 0; i < calojets.size(); ++i){
                //cout << "jet et " << calojets[i].pt() << endl;
                //cout << "tag1 et " << (tag1[i].first)->pt() << " " << tag1[i].second << endl;
                MyJet jet = myJetConverter(&(calojets[i]));

                map<string,double> tagInfo;
                for(unsigned int iBtag = 0; iBtag < btaggingAlgos.size(); ++iBtag){
                        edm::Handle<reco::JetTagCollection> btagHandle;
                        iEvent.getByLabel(btaggingAlgos[iBtag],btagHandle);
                        const reco::JetTagCollection & tag = *(btagHandle.product());

//                        tagInfo[btaggingAlgos[iBtag].label()] = tag[i].second;
			tagInfo[btaggingAlgos[iBtag].label()] = tag[i].discriminator();
                        //cout << "discriminator = " << tag[i].second << " " << btaggingAlgos[iBtag].label() << end$
                }

                jet.tagInfo = tagInfo;

                jets.push_back(jet);
          }


        }
        return jets;
}
