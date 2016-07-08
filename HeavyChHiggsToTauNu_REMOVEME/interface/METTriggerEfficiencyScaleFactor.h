// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_METTriggerEfficiencyScaleFactor_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_METTriggerEfficiencyScaleFactor_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BinnedEfficiencyScaleFactor.h"

namespace edm {
  class ParameterSet;
}
namespace reco {
  class MET;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;
  class EventWeight;

  class METTriggerEfficiencyScaleFactor {
  public:
    typedef BinnedEfficiencyScaleFactor::Data Data;

    METTriggerEfficiencyScaleFactor(const edm::ParameterSet& iConfig, HistoWrapper& histoWrapper);
    ~METTriggerEfficiencyScaleFactor();

    void setRun(unsigned run) { fBinned.setRun(run); }

    Data applyEventWeight(const reco::MET& met, bool isData, HPlus::EventWeight& eventWeight);
    double getEventWeight(const reco::MET& met);

  private:
    BinnedEfficiencyScaleFactor fBinned;

    WrappedTH1 *hScaleFactor;
    WrappedTH1 *hScaleFactorRelativeUncertainty;
    WrappedTH1 *hScaleFactorAbsoluteUncertainty;
  };
}


#endif
