// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_EmbeddingMuonEfficiency_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_EmbeddingMuonEfficiency_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EfficiencyScaleFactorBase.h"

#include<vector>
#include "boost/shared_ptr.hpp"

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
    class Data: private EfficiencyScaleFactorBase::Data {
      typedef EfficiencyScaleFactorBase::Data Base;
    public:
      Data();
      template <typename T>
      explicit Data(const T& data) {
        fWeight = data.getEventWeight();
        fWeightAbsUncPlus = data.getEventWeightAbsoluteUncertaintyPlus();
        fWeightAbsUncMinus  = data.getEventWeightAbsoluteUncertaintyMinus();
        fEfficiency = fWeight;
        fEfficiencyAbsUncPlus = fWeightAbsUncPlus;
        fEfficiencyAbsUncMinus = fWeightAbsUncMinus;
      }
      ~Data();

      void check() const;

      const double getEventWeight() const { check(); return Base::getEventWeight(); }
      const double getEventWeightAbsoluteUncertaintyPlus() const { check(); return Base::getEventWeightAbsoluteUncertaintyPlus(); }
      const double getEventWeightAbsoluteUncertaintyMinus() const { check(); return Base::getEventWeightAbsoluteUncertaintyMinus(); }
      const double getEventWeightAbsoluteUncertainty() const { check(); return Base::getEventWeightAbsoluteUncertainty(); }
      const double getEventWeightRelativeUncertainty() const { check(); return Base::getEventWeightRelativeUncertainty(); }

      const double getEfficiency() const { check(); return fEfficiency; }
      const double getEfficiencyAbsoluteUncertaintyPlus() const { check(); return fEfficiencyAbsUncPlus; }
      const double getEfficiencyAbsoluteUncertaintyMinus() const { check(); return fEfficiencyAbsUncMinus; }
      const double getEfficiencyAbsoluteUncertainty() const { check(); return std::max(fEfficiencyAbsUncPlus, fEfficiencyAbsUncMinus); }
      const double getEfficiencyRelativeUncertainty() const { return getEfficiencyAbsoluteUncertainty()/fEfficiency; }

      friend class EmbeddingMuonEfficiency;
    private:
      double fEfficiency;
      double fEfficiencyAbsUncPlus;
      double fEfficiencyAbsUncMinus;
    };

    explicit EmbeddingMuonEfficiency(const edm::ParameterSet& iConfig);
    ~EmbeddingMuonEfficiency();

    void setRun(unsigned run) { fEfficiencyScaleFactor->setRun(run); }

    Data getEventWeight(const edm::Event& iEvent);
    Data getEventWeight(const edm::Ptr<pat::Muon>& muon, bool isData) const;

  private:
    edm::InputTag fMuonSrc;
    boost::shared_ptr<EfficiencyScaleFactorBase> fEfficiencyScaleFactor;
  };
}

#endif
