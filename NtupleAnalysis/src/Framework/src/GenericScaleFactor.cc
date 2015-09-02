#include "Framework/interface/GenericScaleFactor.h"
#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/Exception.h"

GenericScaleFactor::GenericScaleFactor(const ParameterSet& config)
: fBinLeftEdges(config.getParameter<std::vector<float>>("binLeftEdges")),
  fScaleFactors(config.getParameter<std::vector<float>>("scaleFactors")),
  fScaleFactorsUpVariation(config.getParameter<std::vector<float>>("scaleFactorsUpVariation")),
  fScaleFactorsDownVariation(config.getParameter<std::vector<float>>("scaleFactorsDownVariation")),
  fActualSF(&fScaleFactors) {
  // Sanity checks
  if (fBinLeftEdges.size()+1 != fScaleFactors.size())
    throw hplus::Exception("config") << "Bin left edges needs to have one less entry than the scale factor vector!";
  if (fBinLeftEdges.size()+1 != fScaleFactorsUpVariation.size())
    throw hplus::Exception("config") << "Bin left edges needs to have one less entry than the scale factor up variation vector!";
  if (fBinLeftEdges.size()+1 != fScaleFactorsDownVariation.size())
    throw hplus::Exception("config") << "Bin left edges needs to have one less entry than the scale factor down variation vector!";
}

GenericScaleFactor::~GenericScaleFactor() {}

float GenericScaleFactor::getScaleFactorValue(const float value) const {
  // Find bin
  size_t bin = findBin(value);
  // Return scale factor value
  return fActualSF->at(bin);
}

void GenericScaleFactor::setVariation(std::string name) {
  size_t len = name.size();
  if (name.find("Up") == len-2 || name.find("up") == len-2)
    fActualSF = &fScaleFactorsUpVariation;
  else if (name.find("Down") == len-4 || name.find("down") == len-4)
    fActualSF = &fScaleFactorsDownVariation;
  else
    throw hplus::Exception("logic") << "Could not deduce from variation name '" << name << "' wheather it is up or down variation (needs to end with up/down)!";
}

size_t GenericScaleFactor::findBin(const float value) const {
  // Simple approach, scan bin edges from left to right
  size_t maxValue = fBinLeftEdges.size();
  for (size_t i = 0; i < maxValue; ++i) {
    if (value < fBinLeftEdges[i])
      return i;
  }
  return maxValue;
}