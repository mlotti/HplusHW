// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_EventWeight_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_EventWeight_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"

namespace edm {
  //class ParameterSet;
  class Event;
}

class TH1;

namespace HPlus {
  /**
    Class for keeping the event weight (from prescale and from factorizing)
  **/
  class EventWeight {
   public:
    EventWeight(const edm::ParameterSet& iConfig);
    ~EventWeight();
    /// Reads the prescale for the event and sets the event weight as the prescale
    void updatePrescale(const edm::Event& iEvent);
    /// Adds a weight by multiplying the current weight
    void multiplyWeight(double w) { fWeight *= w; }
    /// Getter for weight
    double getWeight() const { return fWeight; }

   private:
    edm::InputTag fPrescaleSrc;
    bool fPrescaleAvailableStatus;
    double fWeight;
    TH1* hPrescaleHistoLowScale;
    TH1* hPrescaleHistoMediumScale;
    TH1* hPrescaleHistoHighScale;
  };
}

#endif
