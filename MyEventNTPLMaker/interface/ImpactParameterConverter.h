// -*- C++ -*-
#ifndef HiggsAnalysis_MyEventNTPLMaker_ImpactParameterConverter_h
#define HiggsAnalysis_MyEventNTPLMaker_ImpactParameterConverter_h

#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyImpactParameter.h"
#include "DataFormats/GeometryVector/interface/GlobalVector.h"
#include "DataFormats/EgammaCandidates/interface/Conversion.h"

// Forward declarations
namespace reco {
  class TransientTrack;
  class Vertex;
}

// We need a namespace for the explicit specialization
namespace ipcHelper {
  template <typename T>
  struct TypeHelper {
    static GlobalVector direction(const T& particle) {
      return GlobalVector(particle.px(), particle.py(), particle.pz());
    }
  };
  template <>
  struct TypeHelper<reco::Conversion> {
    static GlobalVector direction(const reco::Conversion& photon) {
      return GlobalVector(photon.pairMomentum().x(), photon.pairMomentum().y(), photon.pairMomentum().z());
    }
  };
}

class ImpactParameterConverter {
public:
  ImpactParameterConverter(const reco::Vertex&);
  ~ImpactParameterConverter();

  MyImpactParameter convert(const reco::TransientTrack&) const;
  MyImpactParameter convert(const reco::TransientTrack&, const GlobalVector&) const;

  template <typename T>
  MyImpactParameter convert(const reco::TransientTrack& transientTrack, const T& particle) const {
    return convert(transientTrack, ipcHelper::TypeHelper<T>::direction(particle));
  }
private:
  const reco::Vertex& primaryVertex;
};

#endif
