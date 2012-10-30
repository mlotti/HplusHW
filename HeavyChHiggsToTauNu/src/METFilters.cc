#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METFilters.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"

namespace HPlus {
  METFilters::METFilters(const edm::ParameterSet& iConfig, EventCounter& eventCounter, const std::string& prefix):
    fAllEventCounter(eventCounter.addSubCounter(prefix, "All events")),
    fHBHENoiseFilterCounter(eventCounter.addSubCounter(prefix, "HBHE Noise Filter")),
    fAllPassedCounter(eventCounter.addSubCounter(prefix, "Passed all filters")),
    fHBHENoiseFilterSrc(iConfig.getUntrackedParameter<edm::InputTag>("HBHENoiseFilterSrc")),
    fHBHENoiseFilterEnabled(iConfig.getUntrackedParameter<bool>("HBHENoiseFilterEnabled"))
  {}
  METFilters::~METFilters() {}

  bool METFilters::passedEvent(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    increment(fAllEventCounter);

    if(fHBHENoiseFilterEnabled) {
      edm::Handle<bool> hresult;
      iEvent.getByLabel(fHBHENoiseFilterSrc, hresult);
      if(! *hresult)
	return false;
    }
    increment(fHBHENoiseFilterCounter);


    increment(fAllPassedCounter);
    return true;
  }
}
