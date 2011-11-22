#include "ExtractableConstant.h"
#include <iostream>

ExtractableConstant::ExtractableConstant(int channel, float value)
: Extractable(channel),
  fValue(value),
  fUpperValue(0.0) {

}

ExtractableConstant::ExtractableConstant(std::string id, float value) 
: Extractable(id),
  fValue(value),
  fUpperValue(0.0) {

}

ExtractableConstant::ExtractableConstant(std::string id, std::string distribution, std::string description, float value)
: Extractable(id, distribution, description),
  fValue(value),
  fUpperValue(0.0) {

}

ExtractableConstant::ExtractableConstant(std::string id, std::string distribution, std::string description, float value, float upperValue)
: Extractable(id, distribution, description, true),
  fValue(value),
  fUpperValue(upperValue) {
}


ExtractableConstant::~ExtractableConstant() {

}

double ExtractableConstant::doExtract(std::vector< Dataset* > datasets, NormalisationInfo* info) {
  // As simple as returning the constant value :)
  return fValue;
}

double ExtractableConstant::doExtractAsymmetricUpperValue(std::vector< Dataset* > datasets, NormalisationInfo* info) {
  return fUpperValue;
}


void ExtractableConstant::print() {
  std::cout << "Row / Constant: ";
  Extractable::print();
  std::cout << " value=" << fValue << std::endl;
}


