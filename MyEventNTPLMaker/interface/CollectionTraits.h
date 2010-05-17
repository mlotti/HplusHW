// -*- c++ -*-
#ifndef HiggsAnalysis_MyEventNTPLMaker_CollectionTraits_h
#define HiggsAnalysis_MyEventNTPLMaker_CollectionTraits_h

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/TauReco/interface/CaloTauFwd.h"
#include "DataFormats/TauReco/interface/PFTauFwd.h"

// Use edm::View as the default collection type
template <typename T>
struct CollectionTraits {
  typedef edm::View<T> collection_type;
};

// For CaloTaus and PFTaus we need the actual type in order to use it
// with the discriminator objects
template <>
struct CollectionTraits<reco::CaloTau> {
  typedef reco::CaloTauCollection collection_type;
};

template <>
struct CollectionTraits<reco::PFTau> {
  typedef reco::PFTauCollection collection_type;
};

#endif
