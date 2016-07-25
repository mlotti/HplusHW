// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_PtrVectorCast_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_PtrVectorCast_h

#include "DataFormats/Common/interface/Ptr.h"

namespace HPlus {
  template <typename Destination, typename Source>
  edm::PtrVector<Destination> PtrVectorCast(const edm::PtrVector<Source>& src) {
    edm::PtrVector<Destination> dst(src.id());
    for(size_t i=0; i<src.size(); ++i) {
      edm::Ptr<Source> ptr = src[i];
      dst.push_back(edm::Ptr<Destination>(ptr.id(), dynamic_cast<const Destination *>(ptr.get()), ptr.key()));
    }
    return dst;
  }
}


#endif
