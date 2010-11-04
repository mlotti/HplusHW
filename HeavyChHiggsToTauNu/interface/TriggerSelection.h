// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TriggerSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TriggerSelection_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

#include<string>

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class TriggerSelection {
  public:
      /**
     * Class to encapsulate the access to the data members of
     * TauSelection. If you want to add a new accessor, add it here
     * and keep all the data of TauSelection private.
     */
    class Data {
    public:
      // The reason for pointer instead of reference is that const
      // reference allows temporaries, while const pointer does not.
      // Here the object pointed-to must live longer than this object.
      Data(const TriggerSelection *triggerSelection, bool passedEvent);
      ~Data();

      bool passedEvent() const { return fPassedEvent; }

    private:
      const TriggerSelection *fTriggerSelection;
      const bool fPassedEvent;
    };
    
    TriggerSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~TriggerSelection();

    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    // Input parameters
    edm::InputTag fSrc;
    std::string fPath;

    // Counters
    Count fTriggerCount;

    // EventWeight object
    EventWeight& fEventWeight;
  };
}

#endif
