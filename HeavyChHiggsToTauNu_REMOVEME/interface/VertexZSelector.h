// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_VertexZSelector_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_VertexZSelector_h

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "CommonTools/UtilAlgos/interface/SelectionAdderTrait.h"
#include "CommonTools/UtilAlgos/interface/StoreContainerTrait.h"
#include "CommonTools/UtilAlgos/interface/ParameterAdapter.h"
#include "CommonTools/UtilAlgos/interface/SelectedOutputCollectionTrait.h"

/**
 * Created with the help of
 * https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideGenericSelectors
 * and SortCollectionSelector.
 */
template <typename InputCollection,
          typename OutputCollection = typename helper::SelectedOutputCollectionTrait<InputCollection>::type, 
          typename StoreContainer = typename helper::StoreContainerTrait<OutputCollection>::type,
          typename RefAdder = typename helper::SelectionAdderTrait<InputCollection, StoreContainer>::type>
class VertexZSelector {
public:
  typedef InputCollection collection;
private:
  typedef const typename InputCollection::value_type * reference;
  typedef std::pair<reference, size_t> pair;
  typedef StoreContainer container;
  typedef typename container::const_iterator const_iterator;

public:
  VertexZSelector(const edm::ParameterSet& iConfig):
    vertexSrc(iConfig.getParameter<edm::InputTag>("vertexSrc")),
    maxZ(iConfig.getParameter<double>("maxZ"))
  {}

  const_iterator begin() const { return selected.begin(); }
  const_iterator end() const { return selected.end(); }
  size_t size() const { return selected.size(); }

  void select(const edm::Handle<InputCollection>& hinput, const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    selected.clear();

    edm::Handle<edm::View<reco::Vertex> > hvertex;
    iEvent.getByLabel(vertexSrc, hvertex);

    for(size_t idx = 0; idx < hinput->size(); ++idx) {
      for(edm::View<reco::Vertex>::const_iterator iVertex = hvertex->begin(); iVertex != hvertex->end(); ++iVertex) {
        if(std::abs((*hinput)[idx].vertex().z() - iVertex->z()) < maxZ)
          addRef(selected, hinput, idx);
      }
    }
  }

private:
  edm::InputTag vertexSrc;
  double maxZ;
  container selected;
  RefAdder addRef;
};

#endif
