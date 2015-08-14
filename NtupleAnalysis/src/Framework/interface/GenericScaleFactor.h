// -*- c++ -*-
#ifndef Framework_GenericScaleFactor_h
#define Framework_GenericScaleFactor_h

#include <vector>
#include <string>

class ParameterSet;

class GenericScaleFactor {
public:
  GenericScaleFactor(const ParameterSet& config);
  ~GenericScaleFactor();

  /// Returns scale factor value for an input value of a distribution
  float getScaleFactorValue(const float value) const;
  /// Sets the up or down variation (name needs to end with Up or Down)
  void setVariation(std::string name);
  
private:
  /// Helper function for finding appropriate bin
  size_t findBin(const float value);
  
private:
  /// Container for left edges of binned quantity
  std::vector<float> fBinLeftEdges;
  /// Container for scale factor values
  std::vector<float> fScaleFactors;
  /// Container for scale factor value for up variation
  std::vector<float> fScaleFactorsUpVariation;
  /// Container for scale factor value for down variation
  std::vector<float> fScaleFactorsDownVariation;
  /// Pointer to container to be used
  std::vector<float>* fActualSF;
};

#endif


