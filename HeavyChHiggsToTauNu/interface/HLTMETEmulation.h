#ifndef HLTTauEmulation_h
#define HLTTauEmulation_h

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/METReco/interface/MET.h"

class HLTMETEmulation {
    public:
        HLTMETEmulation(const edm::ParameterSet&,double);
        ~HLTMETEmulation();

        bool passedEvent(const edm::Event&, const edm::EventSetup&);

    private:
        edm::InputTag metSrc;

        double metCut;
};

#endif
