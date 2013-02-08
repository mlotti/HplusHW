// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_BaseSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_BaseSelection_h

#include "DataFormats/Provenance/interface/EventID.h"

namespace edm {
  class Event;
}

namespace HPlus {
  class EventCounter;
  class HistoWrapper;

  class BaseSelection {
  public:
    BaseSelection(EventCounter& eventCounter, HistoWrapper& histoWrapper);
    virtual ~BaseSelection();

    /**
     * Intended usage is the following:
     *
     * - in analyze(), call ensureAnalyzeAllowed()
     * - in silentAnalyze(), call ensureSilentAnalyzeAllowed()
     *
     * Call to both is allowed only if iEvent.id() differs from
     * fEventID. fEventID is set in ensureAnalyzeAllowed.
     */
    void ensureAnalyzeAllowed(const edm::Event& iEvent);
    void ensureSilentAnalyzeAllowed(const edm::Event& iEvent) const;

    EventCounter& getEventCounter() const { return fEventCounter; }
    HistoWrapper& getHistoWrapper() const { return fHistoWrapper; }
    EventCounter* getEventCounterPointer() const { return &fEventCounter; }
    HistoWrapper* getHistoWrapperPointer() const { return &fHistoWrapper; }
    
  protected:
    EventCounter& fEventCounter;
    HistoWrapper& fHistoWrapper;

  private:
    // These are unsigned ints in practice
    edm::EventNumber_t fEventNumber;
    edm::LuminosityBlockNumber_t fLumiNumber;
    edm::RunNumber_t fRunNumber;
  };
}

#endif
