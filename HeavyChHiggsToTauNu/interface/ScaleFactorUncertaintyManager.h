// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_ScaleFactorUncertaintyManager_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_ScaleFactorUncertaintyManager_h

#include <string>

class TH1F;

namespace edm {
  class ParameterSet;
  class Event;
}

namespace HPlus {
  class ScaleFactorUncertaintyManager {
  public:
    enum ScaleFactorOrderType {
      kSFOrderTotalCount,
      kSFOrderTriggerSF,
      kSFOrderBtagSF
    };
    explicit ScaleFactorUncertaintyManager(const std::string& sName);
    ~ScaleFactorUncertaintyManager();

    void setScaleFactorUncertainties(double eventWeight, double triggerSF, double triggerSFAbsUncertainty, double btagSF, double btagSFAbsUncertainty);

  private:
    TH1F* hCumulativeUncertainties;
    TH1F* hTriggerSF;
    TH1F* hBtagSF;
  };
}

#endif

