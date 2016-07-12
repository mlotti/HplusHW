// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_SelectionCounterPackager_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_SelectionCounterPackager_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

#include <string>
#include <vector>

#include "TObject.h"

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;
  class WrappedTH2;
  
  class SelectionCounterItem {
   public:
    SelectionCounterItem(Count passedCounter, Count subCounter, WrappedTH1* histogram);
    SelectionCounterItem(Count passedCounter, Count subCounter, WrappedTH2* histogram);
    ~SelectionCounterItem();
    
    bool hasPassedCounts() const { return (fLocalCounter > 0); }
    bool hasNoPassedCounts() const { return (fLocalCounter == 0); }
    
    void fill(float value) const;
    void fill(float valueX, float valueY) const;
    void reset() { fLocalCounter = 0; }
    void incrementSubCounter();
    void incrementPassedCounter();

   private:
    // Settings for the histogram
    /*const string& fName;
    const string& fHistoLabel;
    const int fHistoBins;
    const float fHistoMin;
    const float fHistoMax;*/
    
    // Variables
    Count fPassedCounter;
    Count fSubCounter;
    int fLocalCounter;
    /// Histogram related to the selection item; more specific histogramming can be implemented elsewhere
    WrappedTH1* fHistogramTH1;
    WrappedTH2* fHistogramTH2;
  };
  
  class SelectionCounterPackager {
   public:
    /**
     * Class for encapsulating a local counter and an EventCounter
     * Use case: for example in looping over tau candidates the
     * sub counters and local counters can be grouped together
     * making the code more readable 
     */
    SelectionCounterPackager(EventCounter& eventCounter);
    ~SelectionCounterPackager();

    /// Returns index of the created sub counter
    size_t addSubCounter(const std::string& base, const std::string& name, WrappedTH1* histogram);
    /// Returns index of the created sub counter
    size_t addSubCounter(const std::string& base, const std::string& name, WrappedTH2* histogram);
    /// Increments the sub counter corresponding to the index
    void incrementSubCount(size_t index) { fSelectionCounterItems.at(index).incrementSubCounter(); }
    /// Increments the passed counters per event (call after all objects such as jets have been handled)
    void incrementPassedCounters();
    /// Fills 1D histogram (weight is taken automatically into account)
    void fill(size_t index, float value) { fSelectionCounterItems.at(index).fill(value); }
    /// Fills 2D histogram (weight is taken automatically into account)
    void fill(size_t index, float valueX, float valueY) { fSelectionCounterItems.at(index).fill(valueX, valueY); }
    /// Resets the local counters
    void reset();

    /// Checks if the local counter corresponding to the index is greater than zero
    bool hasPassedCounts(size_t index) const { return fSelectionCounterItems.at(index).hasPassedCounts(); }
    /// Checks if the local counter corresponding to the index is zero
    bool hasNoPassedCounts(size_t index) const { return fSelectionCounterItems.at(index).hasNoPassedCounts(); }

   private:
    EventCounter& fEventCounter;

    std::vector<SelectionCounterItem> fSelectionCounterItems;
  };
  
}

#endif
