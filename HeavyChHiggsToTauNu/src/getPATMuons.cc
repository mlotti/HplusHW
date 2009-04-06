#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Muon.h"


vector<MyJet> MyEventConverter::getPATMuons(const edm::Event& iEvent){

	vector<MyJet> muons;

	edm::Handle<edm::View<pat::Muon> > muonHandle;
        try{
          iEvent.getByLabel("selectedLayer1Muons",muonHandle);
        }catch(...) {;}

        if(muonHandle.isValid()){
	  const edm::View<pat::Muon> & recoMuons = *(muonHandle.product());

          int offlineMuons = recoMuons.size();
          cout << "Offline mu collection size " << offlineMuons << endl;

	  edm::View<pat::Muon>::const_iterator iMuon;
//          MuonCollection::const_iterator iMuon;
          for(iMuon = recoMuons.begin(); iMuon != recoMuons.end(); iMuon++){

        	MyJet muon = myJetConverter(*iMuon);
                muons.push_back(muon);
		
                cout << "Muon: et= " << iMuon->et();
                cout << " eta= "     << iMuon->eta();
                cout << " phi= "     << iMuon->phi();
                cout << endl;
		
          }

        }
	return muons;
}
