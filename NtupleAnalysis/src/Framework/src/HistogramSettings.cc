// -*- c++ -*-
#include "Framework/interface/HistogramSettings.h"

HistogramSettings::HistogramSettings(const ParameterSet& config)
: fBins(config.getParameter<int>("nBins")),
  fAxisMin(config.getParameter<float>("axisMin")),
  fAxisMax(config.getParameter<float>("axisMax")) { }

HistogramSettings::~HistogramSettings() { }
