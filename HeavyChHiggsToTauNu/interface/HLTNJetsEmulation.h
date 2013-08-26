#ifndef HLTNJetsEmulation_h
#define HLTNJetsEmulation_h

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/JetReco/interface/CaloJet.h"

#include <vector>

typedef math::XYZTLorentzVector LorentzVector;

class HLTNJetsEmulation {
    public:
        HLTNJetsEmulation(const edm::ParameterSet&);
        ~HLTNJetsEmulation();

	void setParameters(int,double);
        bool passedEvent(const edm::Event&, const edm::EventSetup&,std::vector<LorentzVector>);
	std::vector<LorentzVector> HLTJets();

    private:
        edm::InputTag jetSrc;

	int    nJetsMin;
        double jetPtCut;

	std::vector<LorentzVector> passedJets;
};

#endif
