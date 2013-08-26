#ifndef HLTPFMHTEmulation_h
#define HLTPFMHTEmulation_h

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/JetReco/interface/PFJet.h"

class HLTPFMHTEmulation {
    public:
        HLTPFMHTEmulation(const edm::ParameterSet&);
        ~HLTPFMHTEmulation();

	void setParameters(double);
        bool passedEvent(const edm::Event&, const edm::EventSetup&);

    private:
        edm::InputTag pfjetSrc;

        double mhtCut;
};

#endif
