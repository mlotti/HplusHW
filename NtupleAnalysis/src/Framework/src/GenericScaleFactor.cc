#include "Framework/interface/GenericScaleFactor.h"
#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/Exception.h"

GenericScaleFactor::GenericScaleFactor(const ParameterSet& config)
: fBinLeftEdges(config.getParameter<std::vector<float>>("binLeftEdges")),
  fScaleFactors(config.getParameter<std::vector<float>>("scaleFactors")) {
  // Sanity checks
  if (fBinLeftEdges.size()+1 != fScaleFactors.size())
    throw hplus::Exception("config") << "Bin left edges needs to have one less entry than the scale factor vector!";
}

GenericScaleFactor::~GenericScaleFactor() {}

float GenericScaleFactor::getScaleFactorValue(const float value) const {
  // Find bin
  size_t bin = findBin(value);
  // Return scale factor value
  return fScaleFactors.at(bin);
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