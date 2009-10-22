#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

vector<MyJet> MyEventConverter::getMuons(const edm::Event& iEvent, const edm::InputTag& label){
	vector<MyJet> muons;

        Handle<MuonCollection> muonHandle;
        iEvent.getByLabel(label, muonHandle);
        if(!muonHandle.isValid())
                return muons;

        const MuonCollection & recoMuons = *(muonHandle.product());
        int offlineMuons = recoMuons.size();
        cout << "Offline mu collection size " << offlineMuons << endl;

        MuonCollection::const_iterator iMuon;
        for(iMuon = recoMuons.begin(); iMuon != recoMuons.end(); ++iMuon){
        	MyJet muon = myJetConverter(*iMuon);
                muons.push_back(muon);
		/*
                cout << "Muon: et= " << iMuon->et();
                cout << " eta= "     << iMuon->eta();
                cout << " phi= "     << iMuon->phi();
                cout << endl;
		*/
        }
	return muons;
}
