#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TrackConverter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/BTauReco/interface/JetTag.h"
#include "DataFormats/JetReco/interface/CaloJet.h"

#include "JetMETCorrections/Objects/interface/JetCorrector.h"

JetConverter::JetConverter(const TrackConverter& tc, const edm::Event& event, const edm::EventSetup& iSetup,
                           const std::vector<std::string>& labels, const std::vector<std::string>& btags):
  trackConverter(tc),
  jetEnergyCorrectionTypes(labels),
  btagAlgos(btags),
  iEvent(event) {
  
  jetEnergyCorrections.reserve(labels.size());
  
  for(unsigned int i = 0; i < labels.size(); ++i){
    jetEnergyCorrections.push_back(JetCorrector::getJetCorrector(jetEnergyCorrectionTypes[i], iSetup));
  }
}

JetConverter::~JetConverter() {}

/*
MyJet JetConverter::convert(const edm::Ref<edm::View<reco::CaloJet> >& caloJet) const {
        MyJet jet(convert(*caloJet));
        //tag(caloJet, jet.tagInfo);
        return jet;
}
*/

MyJet JetConverter::convert(const reco::CaloJet& caloJet) const {
        MyJet jet(caloJet.px(), caloJet.py(), caloJet.pz(), caloJet.energy());
        trackConverter.addTracksInCone(jet);

        // Jet energy corrections
        for(unsigned int i = 0; i < jetEnergyCorrectionTypes.size(); ++i){
                double factor = jetEnergyCorrections[i]->correction(caloJet);
                jet.addEnergyCorrection(jetEnergyCorrectionTypes[i], factor);
		//cout << "    jet correction " << jetEnergyCorrectionName << " " 
                //                              << jetEnergyCorrectionFactor << endl;
        }

        tag(caloJet, jet.tagInfo);

        return jet;
}

MyJet JetConverter::convert(const pat::Jet& recoJet) const {
        MyJet jet(recoJet.px(), recoJet.py(), recoJet.pz(), recoJet.energy());
        trackConverter.addTracksInCone(jet);

        // FIXME
        // Jet energy corrections?

        tag(recoJet, jet.tagInfo);

	return jet;
}

MyJet JetConverter::convert(const reco::JetTag& recJet) const {
        return convert(*dynamic_cast<const reco::CaloJet*>(recJet.first.get()));
}

//void JetConverter::tag(const edm::Ref<edm::View<reco::CaloJet> >& jetRef, TagType& tagInfo) const {
void JetConverter::tag(const reco::CaloJet& jet, TagType& tagInfo) const {
        edm::Handle<reco::JetTagCollection> handle;
        for(unsigned int i = 0; i < btagAlgos.size(); ++i){
                iEvent.getByLabel(btagAlgos[i], handle);
                const reco::JetTagCollection& tag(*handle);

                tagInfo[btagAlgos[i]] = reco::JetFloatAssociation::getValue(tag, jet);
        }
}

void JetConverter::tag(const pat::Jet& jet, TagType& tagInfo) const {
        for(unsigned int i = 0; i < btagAlgos.size(); ++i){
                tagInfo[btagAlgos[i]] = jet.bDiscriminator(btagAlgos[i]);
        }
}
