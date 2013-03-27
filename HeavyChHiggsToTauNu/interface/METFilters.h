// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_METFilters_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_METFilters_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

#include<string>

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class METFilters {
  public:
    METFilters(const edm::ParameterSet& iConfig, EventCounter& eventCounter, const std::string& prefix = "METFilters");
    ~METFilters();

    bool passedEvent(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  private:
    // Input items
    const edm::InputTag fBeamHaloFilterSrc;
    const bool fBeamHaloFilterEnabled;
    const edm::InputTag fHBHENoiseFilterSrc;
    const bool fHBHENoiseFilterEnabled;
    const edm::InputTag fHBHENoiseFilterMETWGSrc;
    const bool fHBHENoiseFilterMETWGEnabled;
    const edm::InputTag fTrackingFailureFilterSrc;
    const bool fTrackingFailureFilterEnabled;
    const edm::InputTag fEcalDeadCellEventFilterSrc;
    const bool fEcalDeadCellEventFilterEnabled;
    const edm::InputTag fEcalDeadCellTPFilterSrc;
    const bool fEcalDeadCellTPFilterEnabled;
    const edm::InputTag fTriggerResultsSrc; // used to store some met filters as trigger paths
    std::vector<std::string> fHcalLaserFilterStrings;
    const bool fHcalLaserFilterEnabled;
    const edm::InputTag fBadEESuperCrystalFilterSrc;
    const bool fBadEESuperCrystalFilterEnabled;
    const edm::InputTag fEcalCrystalsWithLargeLaserCorrectionFilterSrc;
    const bool fEcalCrystalsWithLargeLaserCorrectionFilterEnabled;
    std::vector<std::string> fTrackingOddEventFilterStrings;
    const bool fTrackingOddEventFilterEnabled;
    const edm::InputTag fMuonsWithWrongMomentaFilterSrc;
    const bool fMuonsWithWrongMomentaFilterEnabled;
    const edm::InputTag fInconsistentMuonPFCandidateFilterSrc;
    const bool fInconsistentMuonPFCandidateFilterEnabled;

    // Subcounters
    Count fAllEventCounter;
    Count fBeamHaloFilterCounter;
    Count fHBHENoiseFilterCounter;
    Count fHBHENoiseFilterMETWGCounter;
    Count fTrackingFailureFilterCounter;
    Count fEcalDeadCellEventFilterCounter;
    Count fEcalDeadCellTPFilterCounter;
    Count fHcalLaserFilterCounter;
    Count fBadEESuperCrystalFilterCounter;
    Count fEcalCrystalsWithLargeLaserCorrectionFilterCounter;
    Count fTrackingOddEventFilterCounter;
    Count fMuonsWithWrongMomentaFilterCounter;
    Count fInconsistentMuonPFCandidateFilterCounter;
    Count fAllPassedCounter;
    
    bool fTriggerResultsListPrintedStatus;
  };
}

#endif
