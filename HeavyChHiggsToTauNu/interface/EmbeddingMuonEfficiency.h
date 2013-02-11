// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_EmbeddingMuonEfficiency_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_EmbeddingMuonEfficiency_h

//#include "FWCore/Utilities/interface/InputTag.h"

#include<vector>

namespace edm {
  class ParameterSet;
  class Event;
}

namespace HPlus {
  class HistoWrapper;
  class EventWeight;

  class EmbeddingMuonEfficiency {
    enum Mode {
      kEfficiency,
      kDisabled
    };

  public:
    class Data {
    public:
      Data();
      ~Data();

      void check() const;

      double getEventWeight() const {
        check();
        return fWeight;
      }
      double getEventWeightAbsoluteUncertainty() const {
        check();
        return fWeightAbsUnc;
      }

      friend class EmbeddingMuonEfficiency;

    private:
      double fWeight;
      double fWeightAbsUnc;
    };

    EmbeddingMuonEfficiency(const edm::ParameterSet& iConfig, HistoWrapper& histoWrapper);
    ~EmbeddingMuonEfficiency();

    Data applyEventWeight(const edm::Event& iEvent, EventWeight& eventWeight);

  private:
    // edm::InputTag fMuonSrc;
      struct EffValue {
        unsigned firstRun;
        unsigned lastRun;
        double value;
        double uncertainty;
      };
      std::vector<EffValue> fDataValues;
      double fMCValue;
      double fMCUncertainty;
      Mode fMode;
  };
}

#endif
