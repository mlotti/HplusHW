// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_BaseSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_BaseSelection_h

class EventCounter;
class HistoWrapper;
class EventID;
class CommonPlots;

  class BaseSelection {
  public:
    BaseSelection(EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots = 0);
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
    void ensureAnalyzeAllowed(EventID& iEventID);
    void ensureSilentAnalyzeAllowed(EventID& iEventID) const;

    EventCounter& getEventCounter() const { return fEventCounter; }
    HistoWrapper& getHistoWrapper() const { return fHistoWrapper; }
    EventCounter* getEventCounterPointer() const { return &fEventCounter; }
    HistoWrapper* getHistoWrapperPointer() const { return &fHistoWrapper; }
    bool fCommonPlotsIsEnabled() const { return (fCommonPlots != 0); }

  protected:
    EventCounter& fEventCounter;
    HistoWrapper& fHistoWrapper;
    CommonPlots* fCommonPlots;

  private:
    unsigned long long fEventNumber;
    unsigned int fLumiNumber;
    unsigned int fRunNumber;
  };

#endif
