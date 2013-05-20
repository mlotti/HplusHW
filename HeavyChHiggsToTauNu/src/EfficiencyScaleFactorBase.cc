#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EfficiencyScaleFactorBase.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/Exception.h"


namespace HPlus {
  EfficiencyScaleFactorBase::Data::Data():
    fWeight(1.0),
    fWeightAbsUnc(0.0)
  {}
  EfficiencyScaleFactorBase::Data::~Data() {}

  EfficiencyScaleFactorBase::EfficiencyScaleFactorBase(const edm::ParameterSet& iConfig):
    fVariationEnabled(iConfig.getParameter<bool>("variationEnabled")),
    fVariationShiftBy(iConfig.getParameter<double>("variationShiftBy"))
  {
    std::string mode = iConfig.getUntrackedParameter<std::string>("mode");
    if(mode == "dataEfficiency")
      fMode = kDataEfficiency;
    else if(mode == "mcEfficiency")
      fMode = kMCEfficiency;
    else if(mode == "scaleFactor")
      fMode = kScaleFactor;
    else if(mode == "disabled")
      fMode = kDisabled;
    else
      throw cms::Exception("Configuration") << "EfficiencyScaleFactorBase: Unsupported value for parameter 'mode' " << mode << ", should be 'dataEfficiency', 'mcEfficiency', 'scaleFactor', or 'disabled'" << std::endl;
  }

  EfficiencyScaleFactorBase::~EfficiencyScaleFactorBase() {}
}
