#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

vector<MyJet> MyEventConverter::getPATJets(const edm::Event& iEvent){
        vector<MyJet> jets;

	edm::Handle<edm::View<pat::Jet> > jetHandle;
        try{
          iEvent.getByLabel("selectedLayer1Jets", jetHandle);
        }catch(...) {;}


        if(jetHandle.isValid()){
	  const edm::View<pat::Jet> & recoJets = *(jetHandle.product());
          cout << "jet collection size " << recoJets.size() << endl;

          for(unsigned int i = 0; i < recoJets.size(); ++i){
                //cout << "jet et " << recoJets[i].pt() << endl;
                //cout << "tag1 et " << (tag1[i].first)->pt() << " " << tag1[i].second << endl;
                MyJet jet = myJetConverter(recoJets[i]);

                map<string,double> tagInfo;
                for(unsigned int iBtag = 0; iBtag < btaggingAlgos.size(); ++iBtag){
			tagInfo[btaggingAlgos[iBtag].label()] = recoJets[i].bDiscriminator(btaggingAlgos[iBtag].label());
                }
                jet.tagInfo = tagInfo;

                jets.push_back(jet);
          }
        }
        return jets;
}
