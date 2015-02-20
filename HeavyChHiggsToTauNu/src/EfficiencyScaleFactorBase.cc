#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EfficiencyScaleFactorBase.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/Exception.h"

#include "boost/optional/optional.hpp"

#include <limits>

namespace HPlus {
  EfficiencyScaleFactorBase::Data::Data():
    fWeight(1.0),
    fWeightAbsUncPlus(0.0),
    fWeightAbsUncMinus(0.0)
  {}
  EfficiencyScaleFactorBase::Data::~Data() {}

  EfficiencyScaleFactorBase::EfficiencyScaleFactorBase(const edm::ParameterSet& iConfig):
    fUseMaxUncertainty(iConfig.getParameter<bool>("useMaxUncertainty")),
    fVariationEnabled(iConfig.getParameter<bool>("variationEnabled")),
    fVariationSFShiftBy(std::numeric_limits<double>::quiet_NaN()),
    fVariationDataShiftBy(std::numeric_limits<double>::quiet_NaN()),
    fVariationMCShiftBy(std::numeric_limits<double>::quiet_NaN())
  {
    std::string mode = iConfig.getUntrackedParameter<std::string>("mode");
    if(mode == "dataEfficiency") {
      fMode = kDataEfficiency;
      if(fVariationEnabled)
        fVariationDataShiftBy = iConfig.getParameter<double>("variationDataShiftBy");
    }
    else if(mode == "mcEfficiency") {
      fMode = kMCEfficiency;
      if(fVariationEnabled)
        fVariationMCShiftBy = iConfig.getParameter<double>("variationMCShiftBy");
    }
    else if(mode == "scaleFactor") {
      fMode = kScaleFactor;
      if(fVariationEnabled) {
        if(fUseMaxUncertainty)
          fVariationSFShiftBy = iConfig.getParameter<double>("variationSFShiftBy");
        else {
          fVariationDataShiftBy = iConfig.getParameter<double>("variationDataShiftBy");
          fVariationMCShiftBy = iConfig.getParameter<double>("variationMCShiftBy");
        }
      }
    }
    else if(mode == "disabled")
      fMode = kDisabled;
    else
      throw cms::Exception("Configuration") << "EfficiencyScaleFactorBase: Unsupported value for parameter 'mode' " << mode << ", should be 'dataEfficiency', 'mcEfficiency', 'scaleFactor', or 'disabled'" << std::endl;
  }

  EfficiencyScaleFactorBase::~EfficiencyScaleFactorBase() {}

  std::pair<double, double> EfficiencyScaleFactorBase::parseUncertainty(const edm::ParameterSet& pset) {
    if(pset.exists("uncertaintyPlus")) {
      double uncPlus = pset.getParameter<double>("uncertaintyPlus");
      double uncMinus = pset.getParameter<double>("uncertaintyMinus");
      if(fUseMaxUncertainty) {
        double uncMax = std::max(uncPlus, uncMinus);
        return std::make_pair(uncMax, uncMax);
      }
      return std::make_pair(uncPlus, uncMinus);
    }

    // Backwards compatibility
    double unc = pset.getParameter<double>("uncertainty");
    return std::make_pair(unc, unc);
  }

  std::pair<double, double> EfficiencyScaleFactorBase::parseUncertainty(const boost::property_tree::ptree& pt) {
    using boost::property_tree::ptree;

    boost::optional<double> uncPlus = pt.get_optional<double>("uncertaintyPlus");
    if(uncPlus) {
      double uncMinus = pt.get<double>("uncertaintyMinus");
      if(fUseMaxUncertainty) {
        double uncMax = std::max(*uncPlus, uncMinus);
        return std::make_pair(uncMax, uncMax);
      }
      return std::make_pair(*uncPlus, uncMinus);
    }

    // Backwards compatibility
    double unc = pt.get<double>("uncertainty");
    return std::make_pair(unc, unc);
  }

  void EfficiencyScaleFactorBase::varyData(double *eff, double *uncPlus, double *uncMinus) const {
    if(fVariationEnabled && (fMode == kDataEfficiency || (fMode == kScaleFactor && !fUseMaxUncertainty))) {
      if(fVariationDataShiftBy > 0.0)
        (*eff) += (*eff)*fVariationDataShiftBy*(*uncPlus);
      else
        (*eff) += (*eff)*fVariationDataShiftBy*(*uncMinus);
      *uncPlus = 0.0;
      *uncMinus = 0.0;
    }
  }

  void EfficiencyScaleFactorBase::varyMC(double *eff, double *uncPlus, double *uncMinus) const {
    if(fVariationEnabled && (fMode == kMCEfficiency || (fMode == kScaleFactor && !fUseMaxUncertainty))) {
      if(fVariationMCShiftBy > 0.0)
        (*eff) += (*eff)*fVariationMCShiftBy*(*uncPlus);
      else
        (*eff) += (*eff)*fVariationMCShiftBy*(*uncMinus);
    }
  }

  void EfficiencyScaleFactorBase::varySF(double *sf, double *unc) const {
    if(fVariationEnabled && fMode == kScaleFactor && fUseMaxUncertainty) {
      (*sf) += (*sf)*fVariationSFShiftBy*(*unc);
      *unc = 0.0;
    }
  }
}
