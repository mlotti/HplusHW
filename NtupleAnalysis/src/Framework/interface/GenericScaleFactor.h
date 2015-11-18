// -*- c++ -*-
#ifndef Framework_GenericScaleFactor_h
#define Framework_GenericScaleFactor_h

#include "boost/optional.hpp"

#include <vector>
#include <string>

class ParameterSet;

class GenericScaleFactor {
public:
  GenericScaleFactor(boost::optional<ParameterSet> config);
  ~GenericScaleFactor();

  /// Returns scale factor value for an input value of a 1D-distribution
  float getScaleFactorValue(const float value) const;
  // Add support for 2D SF's if necessary
  //float getScaleFactorValue(const float value, const float value) const;
  
private:
  /// Helper function for finding appropriate bin
  size_t findBin(const float value) const;
  
private:
  /// Container for left edges of binned quantity
  std::vector<float> fBinLeftEdges;
  /// Container for scale factor values
  std::vector<float> fScaleFactors;
};

#endif


