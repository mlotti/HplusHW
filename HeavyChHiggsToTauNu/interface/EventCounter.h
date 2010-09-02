// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_EventCounter_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_EventCounter_h

#include <boost/utility.hpp>
#include <utility>
#include <vector>
#include <string>

// Forward declarations
namespace edm {
  class EDProducer;
  class LuminosityBlock;
  class EventSetup;
}

namespace HPlus {
  class Count;

  // Prevent copying
  class EventCounter: private boost::noncopyable {
    struct CountValue {
      CountValue(const std::string& n, const std::string& i, int v);
      bool equalName(std::string n) const;
      void produces(edm::EDProducer *producer) const;
      void produce(edm::LuminosityBlock *block) const;
      void reset();

      std::string name;
      std::string instance;
      int value;
    };
    typedef std::vector<CountValue> CountVector;
  public:

    EventCounter();
    ~EventCounter();

    Count addCounter(const std::string& name);
    Count addSubCounter(const std::string& base, const std::string& name);

    void incrementCount(size_t index, int value) {
      counter_[index].value += value;
    }

    void produces(edm::EDProducer *producer) const;

    void beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup);
    void endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) const;

  private:
    Count insert(const std::string& name);

    CountVector counter_;
    mutable bool finalized;
  };

  class Count {
  public:
    friend class EventCounter;

    Count();
    ~Count();

    void increment(int value=1) {
      check();
      counter_->incrementCount(index_, value);
    }

  private:
    // Prevent construction outside HPlusEventCounter
    Count(EventCounter *counter, size_t index);

    void check() const;

    EventCounter *counter_;
    size_t index_;
  };
}

#endif
