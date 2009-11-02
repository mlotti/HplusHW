#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METConverter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/METReco/interface/CaloMET.h"
#include "DataFormats/METReco/interface/CaloMETCollection.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/METReco/interface/PFMETCollection.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/METReco/interface/METCollection.h"

#include<sstream>

METConverter::METConverter(const std::vector<edm::InputTag>& caloMetLabels, const edm::InputTag& pfMetLabel, const edm::InputTag& tcMetLabel):
  caloMets(caloMetLabels),
  pfMet(pfMetLabel),
  tcMet(tcMetLabel)
{}
METConverter::~METConverter() {}


template <class T>
MyMET metHelper(const edm::Event& iEvent, const edm::InputTag& label) {
        edm::Handle<T> met;
        iEvent.getByLabel(label, met);

        typename T::const_iterator imet = met->begin();
        return MyMET(imet->px(), imet->py());
}

template <class T>
void metHelper(const edm::Event& iEvent, const std::vector<edm::InputTag>& metCollections, std::map<std::string, MyMET>& mets) {
        for(unsigned int iColl = 0; iColl < metCollections.size(); ++iColl)
                mets[metCollections[iColl].label()] = metHelper<T>(iEvent, metCollections[iColl]);
}

void METConverter::convert(const edm::Event& iEvent, std::map<std::string, MyMET>& mets) {
        metHelper<reco::CaloMETCollection>(iEvent, caloMets, mets);
	mets["pfMET"] = metHelper<reco::PFMETCollection>(iEvent, pfMet);
	mets["tcMET"] = metHelper<reco::METCollection>(iEvent, tcMet);

        if(edm::isDebugEnabled()) {
                std::stringstream ss;
                for(std::map<std::string, MyMET>::const_iterator iter = mets.begin(); iter != mets.end(); ++iter) {
                        ss << "     " << iter->first << " :" << iter->second.X() << " " << iter->second.Y() << std::endl;
                }
                LogDebug("MyEventConverter") << "METs: " << std::endl << ss.str() << std::endl;
        }
}
