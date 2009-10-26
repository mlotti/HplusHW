#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

vector<MyJet> MyEventConverter::getPATTaus(const edm::Event& iEvent){

	vector<MyJet> taus;

        edm::Handle<edm::View<pat::Tau> > tauHandle;
	try{
	  iEvent.getByLabel("selectedLayer1Taus",tauHandle);
	}catch(...) {;}

	if(tauHandle.isValid()){
	  const edm::View<pat::Tau> & recoTaus = *(tauHandle.product());

	  int nTaus = recoTaus.size();
          cout << "tau collection size " << nTaus << endl;

          edm::View<pat::Tau>::const_iterator iTau;
          for(iTau = recoTaus.begin();
              iTau!= recoTaus.end(); iTau++){

            /* FIXME
                MyJet tau = myJetConverter(*iTau);
                taus.push_back(tau);
            */

                cout << "Tau: et= " << iTau->et();
                cout << " eta= "     << iTau->eta();
                cout << " phi= "     << iTau->phi();
                cout << endl;
          }
	}

	return taus;
}
