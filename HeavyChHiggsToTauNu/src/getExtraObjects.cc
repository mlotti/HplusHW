#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MuonConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ImpactParameterConverter.h"

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

          MuonConverter converter(*transientTrackBuilder, ImpactParameterConverter(primaryVertex));

          MuonCollection::const_iterator iMuon;
          for(iMuon = recoMuons.begin(); iMuon != recoMuons.end(); iMuon++){

                MyJet muon = converter.convert(*iMuon);
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
