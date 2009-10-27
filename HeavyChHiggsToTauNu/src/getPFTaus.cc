#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

vector<MyJet> MyEventConverter::getPFTaus(const edm::Event& iEvent){
	vector<MyJet> pftaus;

  	Handle<PFTauCollection> thePFTauHandle;
	try{
	  iEvent.getByLabel("pfRecoTauProducer",thePFTauHandle);
        }catch(...) {;}

	if(thePFTauHandle.isValid()){
	  const PFTauCollection & pfTaus = *(thePFTauHandle.product());

	  int nPfTaus = pfTaus.size();
	  cout << "PFtau collection size " << nPfTaus << endl;	

	  PFTauCollection::const_iterator iTau;
	  for(iTau = pfTaus.begin(); iTau != pfTaus.end(); iTau++){
                if(!iTau->leadPFChargedHadrCand()) continue;
                MyJet tau = myJetConverter(*iTau);
                pftaus.push_back(tau);
          }
	}

/*
        Handle<PFIsolatedTauTagInfoCollection> isolatedTauHandle;
        try{
          iEvent.getByLabel("pfConeIsolation",isolatedTauHandle);
        }catch(...) {;}

        if(isolatedTauHandle.isValid()){
          const PFIsolatedTauTagInfoCollection & isolatedTaus =
                                                *(isolatedTauHandle.product());
          int offlineTaus = isolatedTaus.size();
          cout << "PFtau collection size " << offlineTaus << endl;

          PFIsolatedTauTagInfoCollection::const_iterator iTau;
          for(iTau = isolatedTaus.begin(); iTau != isolatedTaus.end(); iTau++){
		MyJet tau = myJetConverter(*iTau);
                pftaus.push_back(tau);
          }
        }
*/
	return pftaus;
}
