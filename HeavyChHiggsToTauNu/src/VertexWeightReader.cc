#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexWeightReader.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/VertexReco/interface/Vertex.h"

namespace HPlus {
  VertexWeightReader::VertexWeightReader(const edm::ParameterSet& iConfig):
    fPUVertexWeightSrc(iConfig.getParameter<edm::InputTag>("PUVertexWeightSrc")),
    fVertexSrc(iConfig.getParameter<edm::InputTag>("vertexSrc")),
    fEnabled(iConfig.getParameter<bool>("enabled")) {
  }
  VertexWeightReader::~VertexWeightReader() {}

  double VertexWeightReader::getWeight(const edm::Event& iEvent, const edm::EventSetup& iSetup) const {
    if (!fEnabled)
      return 1.0;
    edm::Handle<double> myWeightHandle;
    iEvent.getByLabel(fPUVertexWeightSrc, myWeightHandle);
    return *myWeightHandle;
  }

  size_t VertexWeightReader::getNumberOfVertices(const edm::Event& iEvent, const edm::EventSetup& iSetup) const {
    edm::Handle<edm::View<reco::Vertex> > hvertex;
    iEvent.getByLabel(fVertexSrc, hvertex);
    return hvertex->size();
  }


}
