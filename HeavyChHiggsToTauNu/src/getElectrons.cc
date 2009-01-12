#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

//#include "DataFormats/EgammaCandidates/interface/PixelMatchGsfElectronFwd.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectronFwd.h"
#include "DataFormats/EgammaReco/interface/BasicClusterShapeAssociation.h"
#include "DataFormats/EgammaReco/interface/BasicCluster.h"
#include "DataFormats/Common/interface/ValueMap.h"


vector<MyJet> MyEventConverter::getElectrons(const edm::Event& iEvent){
	vector<MyJet> electrons;

        Handle<GsfElectronCollection> electronHandle;
        try{
          iEvent.getByLabel("pixelMatchGsfElectrons",electronHandle);
        }catch(...) {;}

        if(electronHandle.isValid()){

//          const GsfElectronCollection & recoElectrons = *(electronHandle.product());

          unsigned int offlineElectrons = electronHandle->size();
          cout << "Offline electron collection size " << offlineElectrons << endl;

	  edm::Handle<edm::ValueMap<float> > electronIdHandle;
	  iEvent.getByLabel( electronIdLabel , electronIdHandle );
	  const edm::ValueMap<float> & electronId = *(electronIdHandle.product());
/*
          GsfElectronCollection::const_iterator iElectron;
          for(iElectron = recoElectrons.begin(); 
              iElectron != recoElectrons.end(); iElectron++){
*/
	  for(unsigned int i = 0; i < offlineElectrons; ++i){

		edm::Ref<reco::GsfElectronCollection> iElectron(electronHandle,i);
		bool electronIdDecision = electronId[iElectron];

//		bool electronIdDecision = electronIdAlgo->result(&(*iElectron),iEvent,iSetup);

		if(electronIdDecision) {

			Handle<BasicClusterShapeAssociationCollection> clusterShapeHandle;

			if( fabs(iElectron->superCluster()->seed()->eta())<1.479 ){
  			  iEvent.getByLabel(barrelClusterShapeAssocProducer, clusterShapeHandle);
  			} else {
  			  iEvent.getByLabel(endcapClusterShapeAssocProducer, clusterShapeHandle);
  			}

			// Find entry in map corresponding to seed BasicCluster of SuperCluster
  			BasicClusterShapeAssociationCollection::const_iterator seedShpItr;
  			seedShpItr = clusterShapeHandle->find(iElectron->superCluster()->seed());
			const ClusterShapeRef& clusterShapeRef = seedShpItr->val;

			MyJet electron = myJetConverter(&(*iElectron),clusterShapeRef);
                	electrons.push_back(electron);

 	               	cout << "Electron: et= " << iElectron->et();
        	        cout << " eta= "         << iElectron->eta();
                	cout << " phi= "         << iElectron->phi();
                	cout << endl;

		}
	  }
	}

	return electrons;
}
