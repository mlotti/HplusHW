// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_EventCounter2_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_EventCounter2_h

#include <boost/utility.hpp>
#include <utility>
#include <vector>
#include <string>
#include <map>

// Forward declarations
namespace edm {
  class ParameterSet;
  class LuminosityBlock;
  class EventSetup;
  class InputTag;
}
class TFileDirectory;

namespace HPlus {
  class Count2;

  // Prevent copying
  class EventCounter2: private boost::noncopyable {
    struct Counter2 {
      Counter2(const std::string& n);
      bool equalName(const std::string n) const;
      bool contains(const std::string& l) const;

      size_t insert(const std::string& label);

      std::string name;
      std::vector<std::string> labels;
      std::vector<long int> values;
      std::vector<double> weights;
      std::vector<double> weightsSquared;
    };
  public:

    EventCounter2(const edm::ParameterSet& iConfig);
    ~EventCounter2();

    Count2 addCounter(const std::string& name);
    Count2 addSubCounter(const std::string& base, const std::string& name);

    void incrementCount(size_t counterIndex, size_t countIndex, int value) {
      Counter2& counter = allCounters_.at(counterIndex);
      counter.values.at(countIndex) += value;
      double dval = value * (*eventWeightPointer);
      counter.weights.at(countIndex) += dval;
      counter.weightsSquared.at(countIndex) += dval*dval;
    }
    void setWeightPointer(const double* ptr) { eventWeightPointer = ptr; }

    void beginLuminosityBlock(const edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup);
    void endJob();

  private:
    size_t findOrInsertCounter(const std::string& name);

    std::vector<edm::InputTag> inputCountTags_;
    std::vector<Counter2> allCounters_; // main counter is always at index 0

    mutable bool finalized;
    const double* eventWeightPointer;
  };

  class Count2 {
  public:
    friend class EventCounter2;

    // Construction is by the default copy constructor
    ~Count2();

    void increment(int value=1) {
      check();
      counter_->incrementCount(counterIndex_, countIndex_, value);
    }

  private:
    // No default construction
    Count2(); // NOT IMPLEMENTED

    // Prevent construction outside HPlusEventCounter
    Count2(EventCounter2 *counter, size_t counterIndex, size_t countIndex);

    void check() const;

    EventCounter2 *counter_;
    size_t counterIndex_;
    size_t countIndex_;
  };

  inline
  void increment(Count2& count, int value=1) {
    count.increment(value);
  }
}

#endif
