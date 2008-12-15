#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

MyMeasurement1D MyEventConverter::myMeasurement1DConverter(const Measurement1D& measurement){
	return MyMeasurement1D(measurement.value(),measurement.error());
}
