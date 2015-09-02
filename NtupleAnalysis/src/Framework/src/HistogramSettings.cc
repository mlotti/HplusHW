// -*- c++ -*-
#include "Framework/interface/HistogramSettings.h"
#include "Framework/interface/Exception.h"

HistogramSettings::HistogramSettings(const ParameterSet& config)
: fBins(config.getParameter<int>("nBins")),
  fAxisMin(config.getParameter<float>("axisMin")),
  fAxisMax(config.getParameter<float>("axisMax")) {
  // Check ackward setting
  if (fAxisMax <= fAxisMin)
    throw hplus::Exception("config") << "Axis max value (" << fAxisMax << ") smaller than or equal to min value (" << fAxisMin << ")!";
  if (fBins <= 0)
    throw hplus::Exception("config") << "Number of bins (" << fBins << ") smaller than or equal to 0!";
}

HistogramSettings::~HistogramSettings() { }
