// -*- C++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_VertexConverter_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_VertexConverter_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyVertex.h"

#include<vector>

class TransientVertex;
namespace reco { 
  class Vertex;
  class TransientTrack;
}

class VertexConverter {
public:
  static MyVertex convert(const reco::Vertex&);
  static MyVertex convert(const TransientVertex&);
  static void addSecondaryVertices(const std::vector<reco::TransientTrack>&, std::vector<MyVertex>&);

};

#endif
