#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectronFwd.h"
#include "DataFormats/EgammaReco/interface/BasicClusterShapeAssociation.h"
#include "DataFormats/EgammaReco/interface/BasicCluster.h"
#include "DataFormats/Common/interface/ValueMap.h"


vector<MyJet> MyEventConverter::getElectrons(const edm::Event& iEvent,const edm::EventSetup& iSetup){
	vector<MyJet> electrons;

        Handle<GsfElectronCollection> electronHandle;
        try{
          iEvent.getByLabel("pixelMatchGsfElectrons",electronHandle);
        }catch(...) {;}

        if(electronHandle.isValid()){
	  const GsfElectronCollection & recoElectrons = *(electronHandle.product());
          cout << "Offline electron collection size " << recoElectrons.size() << endl;

	  for(unsigned int i = 0; i < recoElectrons.size(); ++i){
		MyJet electron = myJetConverter(&(recoElectrons[i]));

		map<string,double> tagInfo;
		edm::Ref<reco::GsfElectronCollection> iElectron(electronHandle,i);
		for(unsigned int ietag = 0; ietag < electronIdLabels.size(); ++ietag){
			edm::Handle<edm::ValueMap<float> > electronIdHandle;
			iEvent.getByLabel(electronIdLabels[ietag], electronIdHandle );
			const edm::ValueMap<float> & electronId = *(electronIdHandle.product());

			tagInfo[electronIdLabels[ietag].label()] = electronId[iElectron];
		}

		Handle< EcalRecHitCollection > pEBRecHits;
		iEvent.getByLabel( reducedBarrelRecHitCollection, pEBRecHits );

		Handle< EcalRecHitCollection > pEERecHits;
		iEvent.getByLabel( reducedEndcapRecHitCollection, pEERecHits );

		EcalClusterLazyTools lazyTools(iEvent,iSetup,reducedBarrelRecHitCollection,reducedEndcapRecHitCollection);
		tagInfo = etag(&(*iElectron),lazyTools,tagInfo);

		electron.tagInfo = tagInfo;
		electrons.push_back(electron);
	  }
	}

	return electrons;
}
