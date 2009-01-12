#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

#include "DataFormats/METReco/interface/CaloMET.h"
#include "DataFormats/METReco/interface/CaloMETCollection.h"


MyMET MyEventConverter::getMET(const edm::Event& iEvent){

	MyMET met;

        Handle<reco::CaloMETCollection> caloMET;
        try{
            iEvent.getByLabel("met",caloMET);
        }catch(...) {;}

        if(caloMET.isValid()){
          reco::CaloMETCollection::const_iterator imet = caloMET->begin();
          met.x = imet->px();
          met.y = imet->py();
        }

        cout << " calo MET : " << met.value()
             << "  x : " << met.getX()
             << "  y : " << met.getY() << endl;


        for(unsigned int iCorr = 0; iCorr < metCorrections.size(); ++iCorr){
                edm::Handle<reco::CaloMETCollection> metHandle;
		try{
                  iEvent.getByLabel(metCorrections[iCorr],metHandle);
		}catch(...) {;}

                if(metHandle.isValid()){
		  MyGlobalPoint correction;
		  correction.name = metCorrections[iCorr].label();
		  
                  reco::CaloMETCollection::const_iterator imet = metHandle->begin();
		  correction.x = imet->px() - met.x;
		  correction.y = imet->py() - met.y;

		  cout << "     MET " << correction.name << " : " 
                       << correction.x << " "
                       << correction.y << endl;

		  met.corrections.push_back(correction);
                }
        }




/*

        Handle<reco::CaloMETCollection> caloMET_Type1Icone5;
        try{
            iEvent.getByLabel("corMetType1Icone5",caloMET_Type1Icone5);
        }catch(...) {;}

        if(caloMET_Type1Icone5.isValid()){
          MyGlobalPoint correction;
          correction.name = "CaloMET_Type1Icone5";

          reco::CaloMETCollection::const_iterator imet = caloMET_Type1Icone5->begin();
          correction.x = imet->px() - met.x;
          correction.y = imet->py() - met.y;

          cout << " calo MET Type1Icone5 : " << correction.x << " "
                                       << correction.y << endl;

          met.corrections.push_back(correction);
	}

        Handle<reco::CaloMETCollection> caloMET_Type1Mcone5;
        try{
            iEvent.getByLabel("corMetType1Mcone5",caloMET_Type1Mcone5);
        }catch(...) {;}

        if(caloMET_Type1Mcone5.isValid()){
          MyGlobalPoint correction;
          correction.name = "CaloMET_Type1Mcone5";

          reco::CaloMETCollection::const_iterator imet = caloMET_Type1Mcone5->begin();
          correction.x = imet->px() - met.x;
          correction.y = imet->py() - met.y;

          cout << " calo MET Type1Mcone5 : " << correction.x << " "
                                       << correction.y << endl;

          met.corrections.push_back(correction);
        }


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

        Handle<reco::CaloMETCollection> caloMET_noHF;
        try{
            iEvent.getByLabel("metNoHF",caloMET_noHF);
        }catch(...) {;}

        if(caloMET_noHF.isValid()){

	  MyGlobalPoint correction;
	  correction.name = "CaloMET_noHF";

          reco::CaloMETCollection::const_iterator imet = caloMET_noHF->begin();
          correction.x = imet->px() - met.x;
          correction.y = imet->py() - met.y;

	  cout << " calo MET No HF : " << correction.x << " "
                                       << correction.y << endl;

          met.corrections.push_back(correction);
        }

        Handle<reco::CaloMETCollection> caloMET_noHF_Type1Icone5;
        try{
            iEvent.getByLabel("corMetType1Icone5NoHF",caloMET_noHF_Type1Icone5);
        }catch(...) {;}

        if(caloMET_noHF_Type1Icone5.isValid()){
          MyGlobalPoint correction;
          correction.name = "CaloMET_noHF_Type1Icone5";

          reco::CaloMETCollection::const_iterator imet = caloMET_noHF_Type1Icone5->begin();
          correction.x = imet->px() - met.x;
          correction.y = imet->py() - met.y;

          cout << " calo MET NoHF Type1Icone5 : " << correction.x << " "
                                       << correction.y << endl;

          met.corrections.push_back(correction);
        }

        Handle<reco::CaloMETCollection> caloMET_noHF_Type1Mcone5;
        try{
            iEvent.getByLabel("corMetType1Mcone5NoHF",caloMET_noHF_Type1Mcone5);
        }catch(...) {;}

        if(caloMET_noHF_Type1Mcone5.isValid()){
          MyGlobalPoint correction;
          correction.name = "CaloMET_noHF_Type1Mcone5";

          reco::CaloMETCollection::const_iterator imet = caloMET_noHF_Type1Mcone5->begin();
          correction.x = imet->px() - met.x;
          correction.y = imet->py() - met.y;

          cout << " calo MET NoHF Type1Mcone5 : " << correction.x << " "
                                       << correction.y << endl;

          met.corrections.push_back(correction);
        }


	/// mixed cases
        Handle<reco::CaloMETCollection> caloMET_noHF_Type1Icone5_mCorr;
        try{
            iEvent.getByLabel("corMetType1Icone5NoHFmCorr",caloMET_noHF_Type1Icone5_mCorr);
        }catch(...) {;}

        if(caloMET_noHF_Type1Icone5_mCorr.isValid()){
          MyGlobalPoint correction;
          correction.name = "CaloMET_noHF_Type1Icone5_mCorr";

          reco::CaloMETCollection::const_iterator imet = caloMET_noHF_Type1Icone5_mCorr->begin();
          correction.x = imet->px() - met.x;
          correction.y = imet->py() - met.y;

          cout << " calo MET NoHF Type1Icone5mCorr : " << correction.x << " "
                                       << correction.y << endl;

          met.corrections.push_back(correction);
        }

        Handle<reco::CaloMETCollection> caloMET_noHF_Type1Mcone5_iCorr;
        try{
            iEvent.getByLabel("corMetType1Mcone5NoHFiCorr",caloMET_noHF_Type1Mcone5_iCorr);
        }catch(...) {;}

        if(caloMET_noHF_Type1Mcone5_iCorr.isValid()){
          MyGlobalPoint correction;
          correction.name = "CaloMET_noHF_Type1Mcone5_iCorr";

          reco::CaloMETCollection::const_iterator imet = caloMET_noHF_Type1Mcone5_iCorr->begin();
          correction.x = imet->px() - met.x;
          correction.y = imet->py() - met.y;

          cout << " calo MET NoHF Type1Mcone5iCorr : " << correction.x << " "
                                       << correction.y << endl;

          met.corrections.push_back(correction);
        }

*/
	return met;
}
