#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexSelection.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/VertexReco/interface/Vertex.h"


namespace HPlus {
  VertexSelection::Data::Data(const VertexSelection *vertexSelection, bool passedEvent):
    fVertexSelection(vertexSelection), fPassedEvent(passedEvent) {}
  VertexSelection::Data::~Data() {}

  VertexSelection::VertexSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fEnabled(iConfig.getUntrackedParameter<bool>("enabled")),
    fEventWeight(eventWeight)
  {}

  VertexSelection::~VertexSelection() {}

  VertexSelection::Data VertexSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    // Reset variables
    fSelectedVertex = edm::Ptr<reco::Vertex>();

    if(!fEnabled)
      return Data(this, true);

    edm::Handle<edm::View<reco::Vertex> > hvertex;
    iEvent.getByLabel(fSrc, hvertex);

    if(hvertex->empty())
      return Data(this, false);

    fSelectedVertex = hvertex->ptrAt(0);
    return Data(this, true);
  }
}
