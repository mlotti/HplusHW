#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexWeight.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/VertexReco/interface/Vertex.h"


namespace HPlus {
  VertexWeight::VertexWeight(const edm::ParameterSet& iConfig):
    fSrc(iConfig.getParameter<edm::InputTag>("src")),
    fWeights(iConfig.getParameter<std::vector<double> >("weights")),
    fEnabled(iConfig.getParameter<bool>("enabled"))
  {}
  VertexWeight::~VertexWeight() {}

  std::pair<double, size_t> VertexWeight::getWeightAndSize(const edm::Event& iEvent, const edm::EventSetup& iSetup) const {
    edm::Handle<edm::View<reco::Vertex> > hvertex;
    iEvent.getByLabel(fSrc, hvertex);

    if(!fEnabled)
      return std::make_pair(1.0, hvertex->size());

    size_t n = hvertex->size();
    if(n >= fWeights.size())
      n = fWeights.size()-1;

    return std::make_pair(fWeights[n], hvertex->size());
  }

  double VertexWeight::getWeight(const edm::Event& iEvent, const edm::EventSetup& iSetup) const {
    return getWeightAndSize(iEvent, iSetup).first;
  }
}
