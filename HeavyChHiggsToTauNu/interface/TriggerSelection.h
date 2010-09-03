// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TriggerSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TriggerSelection_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

#include<string>

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class TriggerSelection {
  public:
    TriggerSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter);
    ~TriggerSelection();

    bool analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    // Input parameters
    edm::InputTag fSrc;
    std::string fPath;

    // Counters
    Count fTriggerCount;
  };
}

#endif
