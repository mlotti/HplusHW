// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_VertexWeightReader_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_VertexWeightReader_h

#include "FWCore/Utilities/interface/InputTag.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;

namespace HPlus {
  class VertexWeightReader {
  public:
    VertexWeightReader(const edm::ParameterSet& iConfig);
    ~VertexWeightReader();

    double getWeight(const edm::Event& iEvent, const edm::EventSetup& iSetup) const;
    size_t getNumberOfVertices(const edm::Event& iEvent, const edm::EventSetup& iSetup) const;

  private:
    edm::InputTag fPUVertexWeightSrc;
    edm::InputTag fVertexSrc;
    bool fEnabled;
  };
}

#endif
