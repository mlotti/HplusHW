#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

#include "DataFormats/METReco/interface/CaloMET.h"
#include "DataFormats/METReco/interface/CaloMETCollection.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/METReco/interface/PFMETCollection.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/METReco/interface/METCollection.h"

std::map<std::string, MyMET> MyEventConverter::getMET(const edm::Event& iEvent){
	std::map<std::string, MyMET> mets;
//	std::map<std::string, MyMET> mets = getCaloMETs(iEvent);
//	mets["pfMET"] = getPFMET(iEvent);
//	mets["tcMET"] = getTCMET(iEvent);
	getCaloMETs(iEvent,mets);
	getPFMETs(iEvent,mets);
	getMETs(iEvent,mets);

	return mets;
}

std::map<std::string, MyMET> MyEventConverter::getCaloMETs(const edm::Event& iEvent){

	std::map<std::string, MyMET> mets;
/*
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
*/

        for(unsigned int iColl = 0; iColl < metCollections.size(); ++iColl){
                edm::Handle<reco::CaloMETCollection> metHandle;
		try{
                  iEvent.getByLabel(metCollections[iColl],metHandle);
		}catch(...) {;}

                if(metHandle.isValid()){
		  reco::CaloMETCollection::const_iterator imet = metHandle->begin();
		  MyMET met(imet->px(),imet->py());
		  mets[metCollections[iColl].label()] = met;

		  cout << "     CaloMET " << metCollections[iColl].label() << " : " 
                       << met.X() << " "
                       << met.Y() << endl;
                }
        }

	return mets;
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

void MyEventConverter::getCaloMETs(const edm::Event& iEvent,std::map<std::string, MyMET>& mets){

	vector<Handle<reco::CaloMETCollection> > metHandles;
        iEvent.getManyByType(metHandles);

	for(vector<Handle<reco::CaloMETCollection> >::const_iterator iHandle = metHandles.begin();
            iHandle!= metHandles.end(); ++iHandle){
		if(iHandle->isValid()){
			reco::CaloMETCollection::const_iterator imet = (*iHandle)->begin();
			const std::string metCollectionName = iHandle->provenance()->moduleLabel();

			mets[metCollectionName] = MyMET(imet->px(),imet->py());

			cout << "     " << metCollectionName << " : " 
                             << imet->px() << " " << imet->py() << endl;
		}		
	}
}

void MyEventConverter::getPFMETs(const edm::Event& iEvent,std::map<std::string, MyMET>& mets){

        vector<Handle<reco::PFMETCollection> > metHandles;
        iEvent.getManyByType(metHandles);

        for(vector<Handle<reco::PFMETCollection> >::const_iterator iHandle = metHandles.begin();
            iHandle!= metHandles.end(); ++iHandle){
                if(iHandle->isValid()){
                        reco::PFMETCollection::const_iterator imet = (*iHandle)->begin();
                        const std::string metCollectionName = iHandle->provenance()->moduleLabel();

                        mets[metCollectionName] = MyMET(imet->px(),imet->py());

                        cout << "     " << metCollectionName << " : "
                             << imet->px() << " " << imet->py() << endl;
                }
        }
}

void MyEventConverter::getMETs(const edm::Event& iEvent,std::map<std::string, MyMET>& mets){

        vector<Handle<reco::METCollection> > metHandles;
        iEvent.getManyByType(metHandles);

        for(vector<Handle<reco::METCollection> >::const_iterator iHandle = metHandles.begin();
            iHandle!= metHandles.end(); ++iHandle){
                if(iHandle->isValid()){
                        reco::METCollection::const_iterator imet = (*iHandle)->begin();
                        const std::string metCollectionName = iHandle->provenance()->moduleLabel();

                        mets[metCollectionName] = MyMET(imet->px(),imet->py());

                        cout << "     " << metCollectionName << " : "
                             << imet->px() << " " << imet->py() << endl;
                }
        }
}
