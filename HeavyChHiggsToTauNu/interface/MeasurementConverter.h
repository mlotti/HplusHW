// -*- C++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_MeasurementConverter_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_MeasurementConverter_h

#include "DataFormats/GeometryCommonDetAlgo/interface/Measurement1D.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyMeasurement1D.h"

class MeasurementConverter {
public:
  static inline MyMeasurement1D convert(const Measurement1D& measurement) {
	return MyMeasurement1D(measurement.value(),measurement.error());
  }
};

#endif
