#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

vector<MyJet> MyEventConverter::getPFTaus(const edm::Event& iEvent,string label){
	vector<MyJet> pftaus;

  	Handle<PFTauCollection> thePFTauHandle;
	try{
	  //fixedConeHighEffPFTauProducer,fixedConePFTauProducer,shrinkingConePFTauProducer
	  iEvent.getByLabel(edm::InputTag(label),thePFTauHandle);
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
	return pftaus;
}
