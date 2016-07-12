// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_EventWeight_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_EventWeight_h

namespace edm {
  class ParameterSet;
}

namespace HPlus {
  /**
    Class for keeping the event weight (from prescale and from factorizing)
  **/
  class EventWeight {
   public:
    EventWeight(const edm::ParameterSet& iConfig);
    ~EventWeight();

    void beginEvent() { fWeight = 1.0; }

    /// Adds a weight by multiplying the current weight
    void multiplyWeight(double w) { fWeight *= w; }
    /// Getter for weight
    double getWeight() const { return fWeight; }

   private:
    double fWeight;
  };
}

#endif
