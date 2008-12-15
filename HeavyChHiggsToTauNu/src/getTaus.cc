#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

vector<MyJet> MyEventConverter::getTaus(const edm::Event& iEvent){
	vector<MyJet> taus;

	Handle<CaloTauCollection> theCaloTauHandle;
	try{
	  iEvent.getByLabel("caloRecoTauProducer",theCaloTauHandle);
	}catch(...) {;}

	if(theCaloTauHandle.isValid()){
	  const CaloTauCollection & caloTaus = *(theCaloTauHandle.product());

	  int nCaloTaus = caloTaus.size();
          cout << "calotau collection size " << nCaloTaus << endl;

	  CaloTauCollection::const_iterator iTau;
	  for(iTau = caloTaus.begin(); iTau != caloTaus.end(); iTau++){
	     	if(!iTau->leadTrack()) continue;
                MyJet tau = myJetConverter(*iTau);
                taus.push_back(tau);
          }
	}
/*
        Handle<IsolatedTauTagInfoCollection> isolatedTauHandle;
        try{
          iEvent.getByLabel("coneIsolation",isolatedTauHandle);
        }catch(...) {;}

        if(isolatedTauHandle.isValid()){
          const IsolatedTauTagInfoCollection & isolatedTaus =
                                                *(isolatedTauHandle.product());
          int offlineTaus = isolatedTaus.size();
          cout << "Offline calotau collection size " << offlineTaus << endl;

          IsolatedTauTagInfoCollection::const_iterator iTau;
          for(iTau = isolatedTaus.begin(); iTau != isolatedTaus.end(); iTau++){
		MyJet tau = myJetConverter(*iTau);
                taus.push_back(tau);
          }
        }
*/
	return taus;
}
