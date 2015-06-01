// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_BaseSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_BaseSelection_h

class TDirectory;
class EventCounter;
class HistoWrapper;
class EventID;
class CommonPlots;

#include <string>

class BaseSelection {
  public:
    BaseSelection(EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots = 0, const std::string& postfix = "");
    virtual ~BaseSelection();

    virtual void bookHistograms(TDirectory* dir);
    
    /**
     * Intended usage is the following:
     *
     * - in analyze(), call ensureAnalyzeAllowed()
     * - in silentAnalyze(), call ensureSilentAnalyzeAllowed()
     *
     * Call to both is allowed only if iEvent.id() differs from
     * fEventID. fEventID is set in ensureAnalyzeAllowed.
     */
    void ensureAnalyzeAllowed(const EventID& iEventID);
    void ensureSilentAnalyzeAllowed(const EventID& iEventID) const;

    void disableHistogramsAndCounters();
    void enableHistogramsAndCounters();
    
    EventCounter& getEventCounter() const { return fEventCounter; }
    HistoWrapper& getHistoWrapper() const { return fHistoWrapper; }
    EventCounter* getEventCounterPointer() const { return &fEventCounter; }
    HistoWrapper* getHistoWrapperPointer() const { return &fHistoWrapper; }
    bool fCommonPlotsIsEnabled() const { return (fCommonPlots != 0); }

  protected:
    EventCounter& fEventCounter;
    HistoWrapper& fHistoWrapper;
    CommonPlots* fCommonPlots;
    const std::string sPostfix;
  
  private:
    unsigned long long fEventNumber;
    unsigned int fLumiNumber;
    unsigned int fRunNumber;
  };

#endif
