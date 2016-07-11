// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_WeightReader_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_WeightReader_h

#include "FWCore/Utilities/interface/InputTag.h"

#include<string>

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

  class WeightReader {
  public:
    WeightReader(const edm::ParameterSet& iConfig, HistoWrapper& histoWrapper, const std::string& directory);
    ~WeightReader();

    double getWeight(const edm::Event& iEvent, const edm::EventSetup& iSetup) const;

  private:
    edm::InputTag fWeightSrc;
    bool fEnabled;

    WrappedTH1 *hWeightsLow;
    WrappedTH1 *hWeightsMedium;
    WrappedTH1 *hWeightsHigh;
    WrappedTH1 *hWeightsVeryHigh;
  };
}

#endif
