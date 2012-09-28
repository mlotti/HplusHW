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
  class HistoWrapper;

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

    VertexSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~VertexSelection();

    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

    const edm::InputTag getSrc() const {
      return fSrc;
    }

  private:
    edm::InputTag fSrc;
    bool fEnabled;

    edm::Ptr<reco::Vertex> fSelectedVertex;
  };
}

#endif
