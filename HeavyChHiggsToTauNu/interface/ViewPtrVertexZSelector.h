// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_PtrVertexZSelector_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_PtrVertexZSelector_h

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

template <typename T>
class ViewPtrVertexZSelector: public edm::EDProducer {
 public:

  explicit ViewPtrVertexZSelector(const edm::ParameterSet&);
  ~ViewPtrVertexZSelector();

 private:
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  typedef edm::PtrVector<T> Product;

  edm::InputTag candSrc;
  edm::InputTag vertexSrc;
  double maxZ;
};

template <typename T>
ViewPtrVertexZSelector<T>::ViewPtrVertexZSelector(const edm::ParameterSet& iConfig):
  candSrc(iConfig.getParameter<edm::InputTag>("src")),
  vertexSrc(iConfig.getParameter<edm::InputTag>("vertexSrc")),
  maxZ(iConfig.getParameter<double>("maxZ"))
{
  produces<Product>();
}

template <typename T>
ViewPtrVertexZSelector<T>::~ViewPtrVertexZSelector() {}

template <typename T>
void ViewPtrVertexZSelector<T>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<T> > hcand;
  iEvent.getByLabel(candSrc, hcand);

  edm::Handle<edm::View<reco::Vertex> > hvertex;
  iEvent.getByLabel(vertexSrc, hvertex);

  std::auto_ptr<Product> prod(new Product());

  for(typename edm::View<T>::const_iterator iCand = hcand->begin(); iCand != hcand->end(); ++iCand) {
    for(edm::View<reco::Vertex>::const_iterator iVertex = hvertex->begin(); iVertex != hvertex->end(); ++iVertex) {
      if(std::abs(iCand->vertex().z() - iVertex->z()) < maxZ)
        prod->push_back(hcand->ptrAt(iCand-hcand->begin()));
    }
  }

  iEvent.put(prod);
}

#endif
