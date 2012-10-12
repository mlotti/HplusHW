// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_EventCounter_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_EventCounter_h

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
  class Count;

  // Prevent copying
  class EventCounter: private boost::noncopyable {
    struct Counter {
      Counter(const std::string& n);
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

    EventCounter(const edm::ParameterSet& iConfig);
    ~EventCounter();

    Count addCounter(const std::string& name);
    Count addSubCounter(const std::string& base, const std::string& name);

    void incrementCount(size_t counterIndex, size_t countIndex, int value);
    void setWeightPointer(const double* ptr) { eventWeightPointer = ptr; }

    void endLuminosityBlock(const edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup);
    void endJob();

  private:
    size_t findOrInsertCounter(const std::string& name);

    std::vector<edm::InputTag> inputCountTags_;
    std::vector<Counter> allCounters_; // main counter is always at index 0

    std::string label;
    const double* eventWeightPointer;
    mutable bool finalized;
    bool printMainCounter;
    bool printSubCounters;
  };

  class Count {
  public:
    friend class EventCounter;

    // Construction is by the default copy constructor
    ~Count();

    void increment(int value=1) {
      check();
      counter_->incrementCount(counterIndex_, countIndex_, value);
    }

  private:
    // No default construction
    Count(); // NOT IMPLEMENTED

    // Prevent construction outside HPlusEventCounter
    Count(EventCounter *counter, size_t counterIndex, size_t countIndex);

    void check() const;

    EventCounter *counter_;
    size_t counterIndex_;
    size_t countIndex_;
  };

  inline
  void increment(Count& count, int value=1) {
    count.increment(value);
  }
}

#endif
