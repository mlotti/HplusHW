// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_VertexSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_VertexSelection_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class EventCounter;
  class EventWeight;

  class VertexSelection {
  public:
    class Data {
    public:
      Data(const VertexSelection *vertexSelection, bool passedEvent);
      ~Data();

      bool passedEvent() const { return fPassedEvent; }
      const edm::Ptr<reco::Vertex>& getSelectedVertex() const { return fVertexSelection->fSelectedVertex; }

    private:
      const VertexSelection *fVertexSelection;
      const bool fPassedEvent;
    };

    VertexSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~VertexSelection();

    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    edm::InputTag fSrc;
    bool fEnabled;

    EventWeight& fEventWeight;

    edm::Ptr<reco::Vertex> fSelectedVertex;
  };
}

#endif
