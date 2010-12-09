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
        HLTNJetsEmulation(const edm::ParameterSet&,int,double);
        ~HLTNJetsEmulation();

        bool passedEvent(const edm::Event&, const edm::EventSetup&,std::vector<LorentzVector>);

    private:
        edm::InputTag jetSrc;

	int    nJetsMin;
        double jetPtCut;
};

#endif
