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

    Data applyEventWeight(const pat::Tau& tau, bool isData, HPlus::EventWeight& eventWeight);

  private:
    BinnedEfficiencyScaleFactor fBinned;

    WrappedTH1 *hScaleFactor;
    WrappedTH1 *hScaleFactorRelativeUncertainty;
    WrappedTH1 *hScaleFactorAbsoluteUncertainty;
  };
}


#endif
