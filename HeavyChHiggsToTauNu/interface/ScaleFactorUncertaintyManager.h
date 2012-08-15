// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_ScaleFactorUncertaintyManager_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_ScaleFactorUncertaintyManager_h

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include <string>

namespace edm {
  class ParameterSet;
  class Event;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

  class ScaleFactorUncertaintyManager {
  public:
    explicit ScaleFactorUncertaintyManager(HistoWrapper& histoWrapper, const std::string& name, const std::string& directory = "");
    ~ScaleFactorUncertaintyManager();

    void setScaleFactorUncertainties(double eventWeight, double triggerSF, bool isFakeTau, double triggerSFAbsUncertainty, double fakeTauSF, double fakeTauAbsUncertainty, double btagSF, double btagSFAbsUncertainty);

  private:
     WrappedTH1* hTriggerSF;
     WrappedTH1* hTriggerSFAbsUncertainty;
     WrappedTH1* hTriggerSFAbsUncertaintyCounts;
     WrappedTH1* hFakeTauSF;
     WrappedTH1* hFakeTauAbsUncertainty;
     WrappedTH1* hFakeTauAbsUncertaintyCounts;
     WrappedTH1* hBtagSF;
     WrappedTH1* hBtagSFAbsUncertainty;
     WrappedTH1* hBtagSFAbsUncertaintyCounts;
  };
}

#endif

