#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METFilters.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/METReco/interface/BeamHaloSummary.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/Common/interface/Handle.h"

namespace HPlus {
  METFilters::METFilters(const edm::ParameterSet& iConfig, EventCounter& eventCounter, const std::string& prefix):
    // Input items
    fBeamHaloFilterSrc(iConfig.getUntrackedParameter<edm::InputTag>("beamHaloSrc")),
    fBeamHaloFilterEnabled(iConfig.getUntrackedParameter<bool>("beamHaloEnabled")),
    fHBHENoiseFilterSrc(iConfig.getUntrackedParameter<edm::InputTag>("HBHENoiseFilterSrc")),
    fHBHENoiseFilterEnabled(iConfig.getUntrackedParameter<bool>("HBHENoiseFilterEnabled")),
    fHBHENoiseFilterMETWGSrc(iConfig.getUntrackedParameter<edm::InputTag>("HBHENoiseFilterMETWGSrc")),
    fHBHENoiseFilterMETWGEnabled(iConfig.getUntrackedParameter<bool>("HBHENoiseFilterMETWGEnabled")),
    fTrackingFailureFilterSrc(iConfig.getUntrackedParameter<edm::InputTag>("trackingFailureFilterSrc")),
    fTrackingFailureFilterEnabled(iConfig.getUntrackedParameter<bool>("trackingFailureFilterEnabled")),
    fEcalDeadCellEventFilterSrc(iConfig.getUntrackedParameter<edm::InputTag>("EcalDeadCellEventFilterSrc")),
    fEcalDeadCellEventFilterEnabled(iConfig.getUntrackedParameter<bool>("EcalDeadCellEventFilterEnabled")),
    fEcalDeadCellTPFilterSrc(iConfig.getUntrackedParameter<edm::InputTag>("EcalDeadCellTPFilterSrc")),
    fEcalDeadCellTPFilterEnabled(iConfig.getUntrackedParameter<bool>("EcalDeadCellTPFilterEnabled")),
    fTriggerResultsSrc(iConfig.getUntrackedParameter<edm::InputTag>("triggerResultsSrc")),
    // Counters
    fAllEventCounter(eventCounter.addSubCounter(prefix, "All events")),
    fBeamHaloFilterCounter(eventCounter.addSubCounter(prefix, "Beam halo filter")),
    fHBHENoiseFilterCounter(eventCounter.addSubCounter(prefix, "HBHE Noise filter")),
    fHBHENoiseFilterMETWGCounter(eventCounter.addSubCounter(prefix, "HBHE METWG Noise filter")),
    fTrackingFailureFilterCounter(eventCounter.addSubCounter(prefix, "tracking Failure filter")),
    fEcalDeadCellEventFilterCounter(eventCounter.addSubCounter(prefix, "Ecal Dead Cell Event filter")),
    fEcalDeadCellTPFilterCounter(eventCounter.addSubCounter(prefix, "Ecal Dead Cell TP filter")),
    fAllPassedCounter(eventCounter.addSubCounter(prefix, "Passed all filters"))
  {}
  METFilters::~METFilters() {}

  bool METFilters::passedEvent(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    increment(fAllEventCounter);
    // Obtain trigger results object (some filters have been stored as paths there)
    edm::Handle<edm::TriggerResults> triggerResults;
    iEvent.getByLabel(fTriggerResultsSrc, triggerResults);
    if (!triggerResults.isValid())
      throw cms::Exception("Assert") << "METFilters: edm::TriggerResults object is not valid!";
    const edm::TriggerNames& triggerNames = iEvent.triggerNames(*triggerResults);
    std::cout << "METFilters" << std::endl;
    for (unsigned int i = 0; i < triggerResults->size(); ++i) {
      std::cout << "  " <<  triggerNames.triggerName(i) << " status=" << triggerResults->accept(i) << std::endl;
    }
    //const edm::TriggerNames& triggerNames = iEvent.triggerNames(*htrigger);
    //for(std::vector<TriggerPath *>::const_iterator i = triggerPaths.begin(); i != triggerPaths.end(); ++i) {


//----- Beam halo filter
    if (fBeamHaloFilterEnabled) {
      edm::Handle<reco::BeamHaloSummary> hbeamhalo;
      iEvent.getByLabel(fBeamHaloFilterSrc, hbeamhalo);
      if (!hbeamhalo->CSCTightHaloId())
        return false;
    }

//----- HBHE noise filter
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

//----- Tracking failure filter
    if(fTrackingFailureFilterEnabled) {
      edm::Handle<bool> hresult;
      iEvent.getByLabel(fTrackingFailureFilterSrc, hresult);
      if(! *hresult)
	return false;
    }
    increment(fTrackingFailureFilterCounter);

//----- ECAL dead cell filter
    if(fEcalDeadCellEventFilterEnabled) {
      edm::Handle<bool> hresult;
      iEvent.getByLabel(fEcalDeadCellEventFilterSrc, hresult);
      if(! *hresult)
	return false;
    }
    increment(fEcalDeadCellEventFilterCounter);

    if (fEcalDeadCellTPFilterEnabled) {
      edm::Handle<bool> hresult;
      iEvent.getByLabel(fEcalDeadCellTPFilterSrc, hresult);
      if(! *hresult)
        return false;
    }

    // Filters passed 
    increment(fAllPassedCounter);
    return true;
  }
}
