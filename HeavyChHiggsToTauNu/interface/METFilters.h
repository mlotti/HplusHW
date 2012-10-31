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
    Count fAllEventCounter;
    Count fHBHENoiseFilterCounter;
    Count fAllPassedCounter;
    edm::InputTag fHBHENoiseFilterSrc;
    bool fHBHENoiseFilterEnabled;

    Count fHBHENoiseFilterMETWGCounter;
    edm::InputTag fHBHENoiseFilterMETWGSrc;
    bool fHBHENoiseFilterMETWGEnabled;

    Count ftrackingFailureFilterCounter;
    edm::InputTag ftrackingFailureFilterSrc;
    bool ftrackingFailureFilterEnabled;

    Count fEcalDeadCellEventFilterCounter;
    edm::InputTag fEcalDeadCellEventFilterSrc;
    bool fEcalDeadCellEventFilterEnabled;
  };
}

#endif
