#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

vector<MyJet> MyEventConverter::getPATElectrons(const edm::Event& iEvent){

	vector<MyJet> electrons;

	edm::Handle<edm::View<pat::Electron> > electronHandle;
        try{
          iEvent.getByLabel("selectedLayer1Electrons",electronHandle);
        }catch(...) {;}

        if(electronHandle.isValid()){
	  const edm::View<pat::Electron> & recoElectrons = *(electronHandle.product());

          int offlineElectrons = recoElectrons.size();
          cout << "Offline e collection size " << offlineElectrons << endl;

	  edm::View<pat::Electron>::const_iterator iElectron;
          for(iElectron = recoElectrons.begin(); 
              iElectron!= recoElectrons.end(); iElectron++){

        	MyJet electron = myJetConverter(*iElectron);
                electrons.push_back(electron);
		
                cout << "Electron: et= " << iElectron->et();
                cout << " eta= "     << iElectron->eta();
                cout << " phi= "     << iElectron->phi();
                cout << endl;
		
          }

        }
	return electrons;
}
