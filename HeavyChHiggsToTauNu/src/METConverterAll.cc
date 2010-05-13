#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METConverterAll.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/METReco/interface/CaloMET.h"
#include "DataFormats/METReco/interface/CaloMETCollection.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/METReco/interface/PFMETCollection.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/METReco/interface/METCollection.h"

#include<sstream>

METConverterAll::METConverterAll() {}
METConverterAll::~METConverterAll() {}

template <typename T>
void metHelper(const edm::Event& iEvent, std::map<std::string, MyMET>& mets) {
        std::vector<edm::Handle<T> > metHandles;
        iEvent.getManyByType(metHandles);

	for(typename std::vector<edm::Handle<T> >::const_iterator iHandle = metHandles.begin(); iHandle!= metHandles.end(); ++iHandle){
                typename T::const_iterator imet = (*iHandle)->begin();
                const std::string& metCollectionName(iHandle->provenance()->moduleLabel());
                mets[metCollectionName] = MyMET(imet->px(),imet->py());
	}
}

void METConverterAll::convert(const edm::Event& iEvent, std::map<std::string, MyMET>& mets) {
        metHelper<reco::CaloMETCollection>(iEvent, mets);
        metHelper<reco::PFMETCollection>(iEvent, mets);
        metHelper<reco::METCollection>(iEvent, mets);

        if(edm::isDebugEnabled()) {
                std::stringstream ss;
                for(std::map<std::string, MyMET>::const_iterator iter = mets.begin(); iter != mets.end(); ++iter) {
                        ss << "     " << iter->first << " :" << iter->second.X() << " " << iter->second.Y() << std::endl;
                }
                LogDebug("MyEventConverter") << "METs: " << std::endl << ss.str() << std::endl;
        }
}
