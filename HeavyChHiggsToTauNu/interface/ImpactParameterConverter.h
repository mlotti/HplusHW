// -*- C++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_ImpactParameterConverter_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_ImpactParameterConverter_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyImpactParameter.h"
#include "DataFormats/GeometryVector/interface/GlobalVector.h"

namespace reco {
  class TransientTrack;
  class CaloJet;
  class Conversion;
  class Vertex;
}

class ImpactParameterConverter {
public:
  ImpactParameterConverter(const reco::Vertex&);
  ~ImpactParameterConverter();

  MyImpactParameter convert(const reco::TransientTrack&) const;
  MyImpactParameter convert(const reco::TransientTrack&, const reco::CaloJet&) const;
  MyImpactParameter convert(const reco::TransientTrack&, const reco::Conversion&) const;
  MyImpactParameter convert(const reco::TransientTrack&, const GlobalVector&) const;
private:
  const reco::Vertex& primaryVertex;
};

#endif
