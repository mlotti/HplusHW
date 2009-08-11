#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyMeasurement1D.h"

//ClassImp(MyMeasurement1D)

MyMeasurement1D::MyMeasurement1D(double aValue, double aError):
  theValue(aValue), theError(aError)
{}

MyMeasurement1D::~MyMeasurement1D(){}

double MyMeasurement1D::value() const { return theValue;}
double MyMeasurement1D::error() const { return theError;}

double MyMeasurement1D::significance() const {
	if (theError == 0) return 0;
	else return theValue/theError;
}
