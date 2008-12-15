#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

vector<MyJet> MyEventConverter::getHLTObjects(const edm::Event& iEvent){
	vector<MyJet> HLTObjects;

// HLT taus
        Handle<IsolatedTauTagInfoCollection> tauTagL3Handle;
        try{
                iEvent.getByLabel("coneIsolationL3SingleTau", tauTagL3Handle);
        }catch(...) {;}

        if(tauTagL3Handle.isValid()){
                const IsolatedTauTagInfoCollection & L3Taus = *(tauTagL3Handle.product());
                cout << "L3 tau collection size " << L3Taus.size() << endl;

                IsolatedTauTagInfoCollection::const_iterator i;
                for(i = L3Taus.begin(); i != L3Taus.end(); i++){
                        if(i->discriminator(0.1,0.065,0.4,20.,1.)){
//                                Jet thejet = *(i->jet().get());
				IsolatedTauTagInfo theHLTTau = *i;
				MyJet HLTtau = myJetConverter(theHLTTau);
				HLTtau.type = 15; // label for HLT object being tau
                		HLTObjects.push_back(HLTtau);
                        }
                }
        }


	return HLTObjects;
}
