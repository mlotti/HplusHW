// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauTriggerEfficiencyScaleFactor_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauTriggerEfficiencyScaleFactor_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BinnedEfficiencyScaleFactor.h"

namespace edm {
  class ParameterSet;
}
namespace pat {
  class Tau;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;
  class EventWeight;

  class TauTriggerEfficiencyScaleFactor {
  public:
    typedef BinnedEfficiencyScaleFactor::Data Data;

    TauTriggerEfficiencyScaleFactor(const edm::ParameterSet& iConfig, HistoWrapper& histoWrapper);
    ~TauTriggerEfficiencyScaleFactor();

    void setRun(unsigned run) { fBinned.setRun(run); }

    double dataEfficiency(const pat::Tau& tau) const;
    double dataEfficiencyRelativeUncertainty(const pat::Tau& tau) const;
    double dataEfficiencyAbsoluteUncertainty(const pat::Tau& tau) const;

    double dataAverageEfficiency(const pat::Tau& tau) const;
    double dataAverageEfficiencyRelativeUncertainty(const pat::Tau& tau) const;
    double dataAverageEfficiencyAbsoluteUncertainty(const pat::Tau& tau) const;

    double mcEfficiency(const pat::Tau& tau) const;
    double mcEfficiencyRelativeUncertainty(const pat::Tau& tau) const;
    double mcEfficiencyAbsoluteUncertainty(const pat::Tau& tau) const;

    double scaleFactor(const pat::Tau& tau) const;
    double scaleFactorRelativeUncertainty(const pat::Tau& tau) const;
    double scaleFactorAbsoluteUncertainty(const pat::Tau& tau) const;

    Data applyEventWeight(const pat::Tau& tau, bool isData, HPlus::EventWeight& eventWeight);

  private:
    BinnedEfficiencyScaleFactor fBinned;

    WrappedTH1 *hScaleFactor;
    WrappedTH1 *hScaleFactorRelativeUncertainty;
    WrappedTH1 *hScaleFactorAbsoluteUncertainty;
  };
}


#endif
