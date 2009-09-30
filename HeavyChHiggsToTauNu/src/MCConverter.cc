#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MCConverter.h"

#include "FWCore/Framework/interface/Event.h"

#include "DataFormats/JetReco/interface/GenJet.h"
#include "SimDataFormats/Vertex/interface/SimVertexContainer.h"

using std::vector;
using edm::Handle;
using edm::SimVertexContainer;
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


MyGlobalPoint MCConverter::getMCPrimaryVertex(const edm::Event& iEvent){
	Handle<SimVertexContainer> simVertices;
	iEvent.getByLabel("g4SimHits",simVertices);

	MyGlobalPoint mcPV;
	if(simVertices->size() > 0){
		mcPV.SetX((*simVertices)[0].position().x());
		mcPV.SetY((*simVertices)[0].position().y());
		mcPV.SetZ((*simVertices)[0].position().z());
	}else{
                mcPV.SetX(-999);
                mcPV.SetY(-999);
                mcPV.SetZ(-999);
	}
	return mcPV;
}
