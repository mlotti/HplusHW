#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EmbeddingMTWeightFit.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

namespace HPlus {
  EmbeddingMTWeightFit::Data::Data(): fWeight(1.0) {}
  EmbeddingMTWeightFit::Data::~Data() {}

  EmbeddingMTWeightFit::EmbeddingMTWeightFit(const edm::ParameterSet& iConfig):
    fFormula("MTWeight", iConfig.getParameter<std::string>("formula").c_str()),
    fVariationDir(iConfig.getParameter<int>("variationDirection")),
    fEnabled(iConfig.getParameter<bool>("enabled")),
    fVariationEnabled(iConfig.getParameter<bool>("variationEnabled"))
  {}

  EmbeddingMTWeightFit::~EmbeddingMTWeightFit() {}

  EmbeddingMTWeightFit::Data EmbeddingMTWeightFit::getEventWeight(double transverseMass) {
    Data ret;

    if(fEnabled) {
      ret.fWeight = fFormula.Eval(transverseMass);
      if(fVariationEnabled) {
        if(fVariationDir > 0)
          ret.fWeight = ret.fWeight*ret.fWeight;
        else
          ret.fWeight = 1.0;
      }
    }
    return ret;
  }
}
