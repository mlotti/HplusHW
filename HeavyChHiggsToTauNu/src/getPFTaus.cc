#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

vector<MyJet> MyEventConverter::getPFTaus(const edm::Event& iEvent, const edm::InputTag& label){
	vector<MyJet> pftaus;

  	Handle<PFTauCollection> thePFTauHandle;
        //fixedConeHighEffPFTauProducer,fixedConePFTauProducer,shrinkingConePFTauProducer
        iEvent.getByLabel(label, thePFTauHandle);

	if(!thePFTauHandle.isValid())
                return pftaus;
        const PFTauCollection & pfTaus = *(thePFTauHandle.product());

        int nPfTaus = pfTaus.size();
        cout << "PFtau collection size " << nPfTaus << endl;	

        PFTauCollection::const_iterator iTau;
        for(iTau = pfTaus.begin(); iTau != pfTaus.end(); iTau++){
                if(!iTau->leadPFChargedHadrCand()) continue;
                /* FIXME
                MyJet tau = myJetConverter(*iTau);
                pftaus.push_back(tau);
                */
	}
	return pftaus;
}
