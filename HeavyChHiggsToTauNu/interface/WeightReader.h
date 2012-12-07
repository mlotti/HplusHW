// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_WeightReader_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_WeightReader_h

#include "FWCore/Utilities/interface/InputTag.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class WeightReader {
  public:
    WeightReader(const edm::ParameterSet& iConfig);
    ~WeightReader();

    double getWeight(const edm::Event& iEvent, const edm::EventSetup& iSetup) const;

  private:
    edm::InputTag fWeightSrc;
    bool fEnabled;
  };
}

#endif
