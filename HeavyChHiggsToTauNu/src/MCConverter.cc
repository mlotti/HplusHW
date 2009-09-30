#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MCConverter.h"

#include "DataFormats/JetReco/interface/GenJet.h"
#include "FWCore/Framework/interface/Event.h"

using std::vector;
using edm::Handle;
using reco::GenJetCollection;
using reco::GenJet;

MyMCParticle MCConverter::convert(const GenJet& genJet){
	MyMCParticle mcJet(genJet.px(),genJet.py(),genJet.pz(),genJet.energy());
	mcJet.pid = 0; //= genJet.pdgId();
	mcJet.status = 4;
	return mcJet;
}

void MCConverter::addMCJets(const edm::Event& iEvent, vector<MyMCParticle>& mcParticles){
	Handle<GenJetCollection> genJetHandle;
        try{
          iEvent.getByLabel("iterativeCone5GenJets",genJetHandle);
        }catch(...) {;}

        if(genJetHandle.isValid()){

		const reco::GenJetCollection & genJetCollection = *(genJetHandle.product());
                //cout << "MC GenJets " << genJetCollection.size();

	        GenJetCollection::const_iterator iJet;
        	for(iJet = genJetCollection.begin(); iJet!= genJetCollection.end(); ++iJet){

			if(iJet->et() < 20 || fabs(iJet->eta()) > 2.5) continue;
			//cout << "     GenJet Et,eta " << iJet->et() << " " << iJet->eta() << endl;
	                MyMCParticle mcJet = convert(*iJet);
                	mcParticles.push_back(mcJet);
        	}
		//cout << ", saved " << mcParticles.size() << endl;
	}
}
