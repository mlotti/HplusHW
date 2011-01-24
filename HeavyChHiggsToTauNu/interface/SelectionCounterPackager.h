// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_SelectionCounterPackager_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_SelectionCounterPackager_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

#include <string>
#include <vector>

namespace HPlus {
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
    size_t addSubCounter(const std::string& base, const std::string& name);
    /// Increments the counter corresponding to the index
    void increment(int index);
    /// Resets the local counters
    void reset();

    /// Checks if the local counter corresponding to the index is greater than zero
    bool isNonZero(int index) const { return (fLocalCounter.at(index) > 0); }
    /// Checks if the local counter corresponding to the index is zero
    bool isZero(int index) const { return (fLocalCounter.at(index) == 0); }

  private:
    EventCounter& fEventCounter;
    std::vector<Count> fSubCounter;
    std::vector<int> fLocalCounter;
  };
}

#endif
