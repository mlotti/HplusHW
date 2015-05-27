// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_VertexWeight_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_VertexWeight_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"
//#include "PhysicsTools/Utilities/interface/Lumi3DReWeighting.h" // no longer needed for Fall11

#include<vector>

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

  class VertexWeight {
  public:
    VertexWeight(const edm::ParameterSet& iConfig, HPlus::HistoWrapper& histoWrapper);
    ~VertexWeight();

    std::pair<double, size_t> getWeightAndSize(const edm::Event& iEvent, const edm::EventSetup& iSetup, bool getSize=true) const;
    double getWeight(const edm::Event& iEvent, const edm::EventSetup& iSetup) const;

  private:
    edm::InputTag fVertexSrc;
    edm::InputTag fPuSummarySrc;
    mutable edm::LumiReWeighting fLumiWeights; // the weight() methods are NOT const...
    //mutable edm::Lumi3DReWeighting fLumi3DWeights;

    TH1 *hWeights;
    WrappedTH1 *hTrueInteractionsMinus1;
    WrappedTH1 *hTrueInteractions0;
    WrappedTH1 *hTrueInteractionsPlus1;

    bool fEnabled,fwEnabled;
    double myLumiWeights(float) const;
  };
}

#endif
