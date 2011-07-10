// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_VertexWeight_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_VertexWeight_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"

#include<vector>

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;

namespace HPlus {
  class VertexWeight {
  public:
    VertexWeight(const edm::ParameterSet& iConfig);
    ~VertexWeight();

    std::pair<double, size_t> getWeightAndSize(const edm::Event& iEvent, const edm::EventSetup& iSetup) const;
    double getWeight(const edm::Event& iEvent, const edm::EventSetup& iSetup) const;

  private:
    edm::InputTag fVertexSrc;
    mutable edm::LumiReWeighting fLumiWeights; // the weight() methods are NOT const...
    std::vector<double> fWeights;
    TH1 *hWeights;
    bool fUseSimulatedPileup;
    bool fEnabled;
  };
}

#endif
