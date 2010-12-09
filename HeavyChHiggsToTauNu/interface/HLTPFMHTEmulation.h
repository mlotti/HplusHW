#ifndef HLTTauEmulation_h
#define HLTTauEmulation_h

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/JetReco/interface/PFJet.h"

class HLTPFMHTEmulation {
    public:
        HLTPFMHTEmulation(const edm::ParameterSet&,double);
        ~HLTPFMHTEmulation();

        bool passedEvent(const edm::Event&, const edm::EventSetup&);

    private:
        edm::InputTag jetSrc;

        double mhtCut;
};

#endif
