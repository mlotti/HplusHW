// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_ScaleFactorUncertaintyManager_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_ScaleFactorUncertaintyManager_h

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include <string>

class TH1F;

namespace edm {
  class ParameterSet;
  class Event;
}

namespace HPlus {
  class ScaleFactorUncertaintyManager {
  public:
    explicit ScaleFactorUncertaintyManager(const std::string& name, const std::string& directory = "");
    ~ScaleFactorUncertaintyManager();

    void setScaleFactorUncertainties(double eventWeight, double triggerSF, double triggerSFAbsUncertainty, double btagSF, double btagSFAbsUncertainty);

  private:
    TH1F* hTriggerSF;
    TH1F* hTriggerSFAbsUncertainty;
    TH1F* hTriggerSFAbsUncertaintyCounts;
    TH1F* hBtagSF;
    TH1F* hBtagSFAbsUncertainty;
    TH1F* hBtagSFAbsUncertaintyCounts;
  };
}

#endif

