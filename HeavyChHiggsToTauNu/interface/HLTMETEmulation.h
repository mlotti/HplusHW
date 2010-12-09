#ifndef HLTMETEmulation_h
#define HLTMETEmulation_h

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/METReco/interface/MET.h"

class HLTMETEmulation {
    public:
        HLTMETEmulation(const edm::ParameterSet&);
        ~HLTMETEmulation();

	void setParameters(double);
        bool passedEvent(const edm::Event&, const edm::EventSetup&);

    private:
        edm::InputTag metSrc;

        double metCut;
};

#endif
