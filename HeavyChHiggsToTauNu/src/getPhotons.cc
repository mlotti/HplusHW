#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"
#include "DataFormats/EgammaCandidates/interface/Photon.h"

vector<MyJet> MyEventConverter::getPhotons(const edm::Event& iEvent){
	vector<MyJet> photons;

        Handle<reco::PhotonCollection> photonHandle;
        try{
          iEvent.getByLabel("correctedPhotons",photonHandle);
        }catch(...) {;}

        if(photonHandle.isValid()){

		const PhotonCollection& recoPhotons = *(photonHandle.product());

		int offlinePhotons = recoPhotons.size();
          	cout << "Offline photon collection size " << offlinePhotons << endl;

		PhotonCollection::const_iterator iPhoton;
		for(iPhoton = recoPhotons.begin(); iPhoton != recoPhotons.end(); ++iPhoton){

			MyJet photon = myJetConverter(*iPhoton);
			photons.push_back(photon);

			cout << "Photon: et= " << iPhoton->et();
                        cout << " eta= "       << iPhoton->eta();
                        cout << " phi= "       << iPhoton->phi();
                        cout << endl;
		}
	}


        Handle<reco::ConversionCollection> convertedPhotonHandle;
        try{
          iEvent.getByLabel("correctedPhotons",convertedPhotonHandle);
        }catch(...) {;}

        if(convertedPhotonHandle.isValid()){

                const ConversionCollection& recoPhotons = *(convertedPhotonHandle.product());

                int offlinePhotons = recoPhotons.size();
                cout << "Offline converted photon collection size " << offlinePhotons << endl;

                ConversionCollection::const_iterator iPhoton;
                for(iPhoton = recoPhotons.begin(); iPhoton != recoPhotons.end(); ++iPhoton){

                        MyJet photon = myJetConverter(*iPhoton);
                        photons.push_back(photon);

                        cout << "Converted photon: et= " << iPhoton->pairMomentum().perp();
                        cout << " eta= "                 << iPhoton->pairMomentum().eta();
                        cout << " phi= "                 << iPhoton->pairMomentum().phi();
                        cout << endl;
                }
        }

	return photons;
}
