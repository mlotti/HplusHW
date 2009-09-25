// -*- C++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_VertexConverter_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_VertexConverter_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyVertex.h"

class TransientVertex;
namespace reco { class Vertex; }

class VertexConverter {
public:
  static MyVertex convert(const reco::Vertex&);
  static MyVertex convert(const TransientVertex&);

};

#endif
