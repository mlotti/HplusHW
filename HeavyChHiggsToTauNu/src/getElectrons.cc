#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"
/*
#include "DataFormats/EgammaCandidates/interface/PixelMatchGsfElectronFwd.h"
#include "DataFormats/EgammaReco/interface/BasicClusterShapeAssociation.h"
#include "DataFormats/EgammaReco/interface/BasicCluster.h"
*/
vector<MyJet> MyEventConverter::getElectrons(const edm::Event& iEvent){
	vector<MyJet> electrons;
/*
        Handle<PixelMatchGsfElectronCollection> electronHandle;
        try{
          iEvent.getByLabel("pixelMatchGsfElectrons",electronHandle);
//          iEvent.getByLabel("electrons",electronHandle);
        }catch(...) {;}

        if(electronHandle.isValid()){

          const PixelMatchGsfElectronCollection & recoElectrons = *(electronHandle.product());

          int offlineElectrons = recoElectrons.size();
          cout << "Offline electron collection size " << offlineElectrons << endl;

          PixelMatchGsfElectronCollection::const_iterator iElectron;
          for(iElectron = recoElectrons.begin(); 
              iElectron != recoElectrons.end(); iElectron++){
		bool electronIdDecision = electronIdAlgo->result(&(*iElectron),iEvent);

		if(electronIdDecision) {

			Handle<BasicClusterShapeAssociationCollection> clusterShapeHandle;

			if( fabs(iElectron->superCluster()->seed()->eta())<1.479 ){
  			//if (iElectron->classification()<100) {
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
*/
	return electrons;
}
