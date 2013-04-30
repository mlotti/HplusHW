// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_EmbeddingMuonEfficiency_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_EmbeddingMuonEfficiency_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ConstantEfficiencyScaleFactor.h"

#include<vector>

namespace edm {
  class ParameterSet;
  class Event;
}

namespace pat {
  class Muon;
}

namespace HPlus {
  class HistoWrapper;
  class EventWeight;

  class EmbeddingMuonEfficiency {
  public:
    class Data: public EfficiencyScaleFactorBase::Data {
      typedef EfficiencyScaleFactorBase::Data Base;
    public:
      Data();
      template <typename T>
      explicit Data(const T& data) {
        fWeight = data.getEventWeight();
        fWeightAbsUnc = data.getEventWeightAbsoluteUncertainty();
      }
      ~Data();

      void check() const;

      const double getEventWeight() const { check(); return Base::getEventWeight(); }
      const double getEventWeightAbsoluteUncertainty() const { check(); return Base::getEventWeightAbsoluteUncertainty(); }
      const double getEventWeightRelativeUncertainty() const { check(); return Base::getEventWeightRelativeUncertainty(); }

      friend class EmbeddingMuonEfficiency;
    };

    EmbeddingMuonEfficiency(const edm::ParameterSet& iConfig, HistoWrapper& histoWrapper);
    ~EmbeddingMuonEfficiency();

    void setRun(unsigned run) { fEfficiencyScaleFactor.setRun(run); }

    Data getEventWeight(const edm::Event& iEvent);
    Data getEventWeight(const pat::Muon& muon, bool isData);

  private:
    edm::InputTag fMuonSrc;
    ConstantEfficiencyScaleFactor fEfficiencyScaleFactor;
  };
}

#endif
