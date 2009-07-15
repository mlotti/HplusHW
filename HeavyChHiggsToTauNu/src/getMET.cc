#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

#include "DataFormats/METReco/interface/CaloMET.h"
#include "DataFormats/METReco/interface/CaloMETCollection.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/METReco/interface/PFMETCollection.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/METReco/interface/METCollection.h"

MyMET MyEventConverter::getCaloMET(const edm::Event& iEvent){

        MyMET met;

        Handle<reco::CaloMETCollection> caloMET;
        try{
            iEvent.getByLabel("met",caloMET);
        }catch(...) {;}

        if(caloMET.isValid()){
          reco::CaloMETCollection::const_iterator imet = caloMET->begin();
          met.Set(imet->px(),imet->py());
        }

        cout << " calo MET : " << met.value()
             << "  x : " << met.X()
             << "  y : " << met.Y() << endl;

/*FIXME
        for(unsigned int iCorr = 0; iCorr < metCorrections.size(); ++iCorr){
                edm::Handle<reco::CaloMETCollection> metHandle;
		try{
                  iEvent.getByLabel(metCorrections[iCorr],metHandle);
		}catch(...) {;}

                if(metHandle.isValid()){
		  MyGlobalPoint correction;
		  correction.name = metCorrections[iCorr].label();
		  
                  reco::CaloMETCollection::const_iterator imet = metHandle->begin();
		  correction.x = imet->px() - met.x();
		  correction.y = imet->py() - met.y();

		  cout << "     MET " << correction.name << " : " 
                       << correction.x << " "
                       << correction.y << endl;

		  met.corrections.push_back(correction);
                }
        }
*/
	return met;
}

MyMET MyEventConverter::getPFMET(const edm::Event& iEvent){

	MyMET met;

	Handle<reco::PFMETCollection> pfMET;
        try{
            iEvent.getByLabel("pfMet",pfMET);
        }catch(...) {;}

	if(pfMET.isValid()){

	  reco::PFMETCollection::const_iterator imet = pfMET->begin();
	  met.Set(imet->px(),imet->py());
		    
          cout << "     PF MET : " << met.x() << " "
                                   << met.y() << endl;
	}
	return met;
}

MyMET MyEventConverter::getTCMET(const edm::Event& iEvent){

	MyMET met;

	// track corrected MET
	Handle<reco::METCollection> tcMET;
	try{
		iEvent.getByLabel("tcMet",tcMET);
	}catch(...) {;}

        if(tcMET.isValid()){

          reco::METCollection::const_iterator imet = tcMET->begin();
	  met.Set(imet->px(),imet->py());

          cout << "     track corrected MET : " << met.x() << " "
                                                << met.y() << endl;
        }
        return met;
}
