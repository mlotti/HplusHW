#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyEventConverter.h"

#include "DataFormats/CaloTowers/interface/CaloTowerCollection.h"

#include<iostream>

using edm::Handle;
using std::cout;
using std::endl;

MyMET MyEventConverter::getMetFromCaloTowers(const edm::Event& iEvent){

	double x = 0,
               y = 0;
	Handle<CaloTowerCollection> caloTowerHandle;
	iEvent.getByType(caloTowerHandle);

	if(caloTowerHandle.isValid()){
                cout << "MyEventConverter::metFromCaloTowers caloTowerHandle.isValid " << endl;
          	const CaloTowerCollection & caloTowers = *(caloTowerHandle.product());

          	CaloTowerCollection::const_iterator iTower;
          	for(iTower = caloTowers.begin(); iTower != caloTowers.end(); iTower++){
//cout << " tower id " << iTower->id().rawId() << endl;
//cout << " em et, had et " << iTower->emEt() << " "  << iTower->hadEt() << " " << iTower->et() << endl;
//cout << "momentum " << iTower->momentum().x() << " " << iTower->momentum().y() << " " << iTower->momentum().rho() << endl;
			x -= iTower->momentum().x();
                        y -= iTower->momentum().y();
		}
//cout << " met value,x,y " << met.value() << " " << met.x << " " << met.y << endl;
	}
	MyMET met(x,y);
/*FIXME
        Handle<MuonCollection> muonHandle;
        try{
          iEvent.getByLabel("muons",muonHandle);
        }catch(...) {;}

        if(muonHandle.isValid()){

          MyGlobalPoint muonCorrection;
          muonCorrection.name = "muonCorrection";
          muonCorrection.x    = 0;
          muonCorrection.y    = 0;

          const MuonCollection & recoMuons = *(muonHandle.product());

          MuonCollection::const_iterator iMuon;
          for(iMuon = recoMuons.begin(); iMuon != recoMuons.end(); iMuon++){
                muonCorrection.x -= iMuon->px();
                muonCorrection.y -= iMuon->py();
          }
          met.corrections.push_back(muonCorrection);
          met.useCorrection("muonCorrection");

          cout << " muon correction " << muonCorrection.x << " "
                                      << muonCorrection.y << endl;

        }
*/
        return met;
}

