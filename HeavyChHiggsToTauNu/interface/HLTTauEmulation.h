#ifndef HLTTauEmulation_h
#define HLTTauEmulation_h

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/TauReco/interface/CaloTau.h"

typedef math::XYZTLorentzVector LorentzVector;

class HLTTauEmulation {
    public:
	HLTTauEmulation(const edm::ParameterSet&,double,double);
	~HLTTauEmulation();

	bool passedEvent(const edm::Event& iEvent, const edm::EventSetup& iSetup,LorentzVector);

    private:
    	edm::InputTag tauSrc;

	double tauPtCut;
	double tauLTrkCut;
};

#endif
