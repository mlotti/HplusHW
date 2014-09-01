// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_EmbeddingMTWeightFit_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_EmbeddingMTWeightFit_h

#include "TF1.h"

namespace edm {
  class ParameterSet;
}

namespace HPlus {
  class HistoWrapper;
  class EventWeight;

  class EmbeddingMTWeightFit {
  public:
    class Data {
    public:
      Data();
      ~Data();

      const double getEventWeight() const {
        return fWeight;
      }

      friend class EmbeddingMTWeightFit;

    private:
      double fWeight;
    };


    explicit EmbeddingMTWeightFit(const edm::ParameterSet& iConfig);
    ~EmbeddingMTWeightFit();

    Data getEventWeight(double transverseMass);

  private:
    const TF1 fFormula;
    const int fVariationDir;
    const bool fEnabled;
    const bool fVariationEnabled;
  };
}

#endif
