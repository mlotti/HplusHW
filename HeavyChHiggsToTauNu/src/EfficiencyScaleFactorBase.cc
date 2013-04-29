#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EfficiencyScaleFactorBase.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/Exception.h"


namespace HPlus {
  EfficiencyScaleFactorBase::Data::Data():
    fWeight(1.0),
    fWeightAbsUnc(0.0),
    fWeightRelUnc(0.0)
  {}
  EfficiencyScaleFactorBase::Data::~Data() {}

  EfficiencyScaleFactorBase::EfficiencyScaleFactorBase(const edm::ParameterSet& iConfig) {
    std::string mode = iConfig.getUntrackedParameter<std::string>("mode");
    if(mode == "efficiency")
      fMode = kEfficiency;
    else if(mode == "scaleFactor")
      fMode = kScaleFactor;
    else if(mode == "disabled")
      fMode = kDisabled;
    else
      throw cms::Exception("Configuration") << "EfficiencyScaleFactorBase: Unsupported value for parameter 'mode' " << mode << ", should be 'efficiency', 'scaleFactor', or 'disabled'" << std::endl;
  }

  EfficiencyScaleFactorBase::~EfficiencyScaleFactorBase() {}
}
