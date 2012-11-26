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
    fHBHENoiseFilterEnabled(iConfig.getUntrackedParameter<bool>("HBHENoiseFilterEnabled")),

    fHBHENoiseFilterMETWGCounter(eventCounter.addSubCounter(prefix, "HBHE METWG Noise Filter")),
    fHBHENoiseFilterMETWGSrc(iConfig.getUntrackedParameter<edm::InputTag>("HBHENoiseFilterMETWGSrc")),
    fHBHENoiseFilterMETWGEnabled(iConfig.getUntrackedParameter<bool>("HBHENoiseFilterMETWGEnabled")),

    ftrackingFailureFilterCounter(eventCounter.addSubCounter(prefix, "tracking Failure Filter")),
    ftrackingFailureFilterSrc(iConfig.getUntrackedParameter<edm::InputTag>("trackingFailureFilterSrc")),
    ftrackingFailureFilterEnabled(iConfig.getUntrackedParameter<bool>("trackingFailureFilterEnabled")),

    fEcalDeadCellEventFilterCounter(eventCounter.addSubCounter(prefix, "Ecal Dead Cell Event Filter")),
    fEcalDeadCellEventFilterSrc(iConfig.getUntrackedParameter<edm::InputTag>("EcalDeadCellEventFilterSrc")),
    fEcalDeadCellEventFilterEnabled(iConfig.getUntrackedParameter<bool>("EcalDeadCellEventFilterEnabled"))
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

    if(fHBHENoiseFilterMETWGEnabled) {
      edm::Handle<bool> hresult;
      iEvent.getByLabel(fHBHENoiseFilterMETWGSrc, hresult);
      if(! *hresult)
	return false;
    }
    increment(fHBHENoiseFilterMETWGCounter);

    if(ftrackingFailureFilterEnabled) {
      edm::Handle<bool> hresult;
      iEvent.getByLabel(ftrackingFailureFilterSrc, hresult);
      if(! *hresult)
	return false;
    }
    increment(ftrackingFailureFilterCounter);

    if(fEcalDeadCellEventFilterEnabled) {
      edm::Handle<bool> hresult;
      iEvent.getByLabel(fEcalDeadCellEventFilterSrc, hresult);
      if(! *hresult)
	return false;
    }
    increment(fEcalDeadCellEventFilterCounter);


    increment(fAllPassedCounter);
    return true;
  }
}
