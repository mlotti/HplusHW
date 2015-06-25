// -*- c++ -*-
#ifndef Framework_HistogramSettings_h
#define Framework_HistogramSettings_h

#include "Framework/interface/ParameterSet.h"

/**
 * Helper class for histogram settings
 */
class HistogramSettings {
public:
  HistogramSettings(const ParameterSet& config);
  ~HistogramSettings();
  int bins() const { return fBins; }
  double min() const { return fAxisMin; }
  double max() const { return fAxisMax; }
private:
  int fBins;
  double fAxisMin;
  double fAxisMax;
};

#endif
