#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

vector<MyJet> MyEventConverter::getExtraObjects(const edm::Event& iEvent){

	vector<MyJet> extraObjects;

	// filling selected muons removed from the event by mu->tau replacement
        Handle<MuonCollection> muonHandle;
        try{
          iEvent.getByLabel("selectedMuons",muonHandle);
        }catch(...) {;}

        if(muonHandle.isValid()){
          const MuonCollection & recoMuons = *(muonHandle.product());

          int offlineMuons = recoMuons.size();
          cout << "ExtraObjects: selected muon collection size " << offlineMuons << endl;

          MuonCollection::const_iterator iMuon;
          for(iMuon = recoMuons.begin(); iMuon != recoMuons.end(); iMuon++){

        	MyJet muon = myJetConverter(*iMuon);
		muon.tagInfo["mu2tau_selectedMuon"] = 1;
                extraObjects.push_back(muon);
		/*
                cout << "Muon: et= " << iMuon->et();
                cout << " eta= "     << iMuon->eta();
                cout << " phi= "     << iMuon->phi();
                cout << endl;
		*/
          }
        }
	return extraObjects;
}
