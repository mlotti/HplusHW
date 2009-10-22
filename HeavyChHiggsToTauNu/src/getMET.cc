#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

#include "DataFormats/METReco/interface/CaloMET.h"
#include "DataFormats/METReco/interface/CaloMETCollection.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/METReco/interface/PFMETCollection.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/METReco/interface/METCollection.h"

template <class T>
MyMET getMEThelper(const edm::Event& iEvent, const edm::InputTag& label, const char *print) {
        Handle<T> met;
        iEvent.getByLabel(label, met);
        if(!met.isValid())
                return MyMET();

        typename T::const_iterator imet = met->begin();
        std::cout << "     " << print << " " << label.label() << " :" << imet->px() << " " << imet->py() << std::endl;
        return MyMET(imet->px(), imet->py());
}

void MyEventConverter::getCaloMETs(const edm::Event& iEvent, std::map<std::string, MyMET>& mets) {
        MyMET met;
        for(unsigned int iColl = 0; iColl < metCollections.size(); ++iColl){
                met = getMEThelper<reco::METCollection>(iEvent, metCollections[iColl], "CaloMET");
                mets[metCollections[iColl].label()] = met;
        }
}

void MyEventConverter::getMET(const edm::Event& iEvent, std::map<std::string, MyMET>& mets){
        getCaloMETs(iEvent, mets);
	mets["pfMET"] = getMEThelper<reco::PFMETCollection>(iEvent, edm::InputTag("pfMet"), "PF MET");
	mets["tcMET"] = getMEThelper<reco::METCollection>(iEvent, edm::InputTag("tcMet"), "track corrected MET");
}
