#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

vector<MyMCParticle> MyEventConverter::getMCJets(const edm::Event& iEvent){

        vector<MyMCParticle> mcParticles;

	Handle<GenJetCollection> genJetHandle;
        try{
          iEvent.getByLabel("iterativeCone5GenJets",genJetHandle);
        }catch(...) {;}

        if(genJetHandle.isValid()){

		const reco::GenJetCollection & genJetCollection = *(genJetHandle.product());
                cout << "MC GenJets " << genJetCollection.size();

	        GenJetCollection::const_iterator iJet;
        	for(iJet = genJetCollection.begin(); iJet!= genJetCollection.end(); ++iJet){

			if(iJet->et() < 20 || fabs(iJet->eta()) > 2.5) continue;
			//cout << "     GenJet Et,eta " << iJet->et() << " " << iJet->eta() << endl;
	                MyMCParticle mcJet = myMCParticleConverter(*iJet);
                	mcParticles.push_back(mcJet);
        	}
		cout << ", saved " << mcParticles.size() << endl;
	}

	return mcParticles;
}
