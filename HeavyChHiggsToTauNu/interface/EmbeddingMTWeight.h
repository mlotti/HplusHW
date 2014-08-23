// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_EmbeddingMTWeight_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_EmbeddingMTWeight_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BinnedEfficiencyScaleFactor.h"

namespace edm {
  class ParameterSet;
  class Event;
}


namespace HPlus {
  class HistoWrapper;
  class EventWeight;

  class EmbeddingMTWeight {
  public:
    typedef BinnedEfficiencyScaleFactor::Data Data;

    explicit EmbeddingMTWeight(const edm::ParameterSet& iConfig);
    ~EmbeddingMTWeight();

    Data getEventWeight(double transverseMass, const edm::Event& iEvent);

  private:
    BinnedEfficiencyScaleFactor fBinned;
  };
}

#endif
