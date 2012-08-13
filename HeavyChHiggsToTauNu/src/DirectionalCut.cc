#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DirectionalCut.h"

#include "FWCore/Utilities/interface/Exception.h"
#include <iostream>
#include <TMath.h>

namespace HPlus {
  DirectionalCut::DirectionalCut(size_t value, std::string direction)
  : fValue(static_cast<double>(value)) {
    initialise(direction);
  }

DirectionalCut::DirectionalCut(unsigned int value, std::string direction)
  : fValue(static_cast<double>(value)) {
    initialise(direction);
  }

  DirectionalCut::DirectionalCut(double value, std::string direction)
  : fValue(value) {
    initialise(direction);
  }

  DirectionalCut::~DirectionalCut() { }

  void DirectionalCut::initialise(std::string direction) {
    if (direction == "EQ" || direction == "==")
      fCutDirection = kEQ;
    else if (direction == "NEQ" || direction == "!=")
      fCutDirection = kNEQ;
    else if (direction == "GT" || direction == ">")
      fCutDirection = kGT;
    else if (direction == "GEQ" || direction == ">=")
      fCutDirection = kGEQ;
    else if (direction == "LT" || direction == "<")
      fCutDirection = kLT;
    else if (direction == "LEQ" || direction == ">=")
      fCutDirection = kLEQ;
    else {
      throw cms::Exception("config") << "DirectionalCut: invalid cut direction (" << direction << ")! Options are: ==, !=, >, >=, <, <=" << std::endl;
    }
  }

  bool DirectionalCut::passedCut(size_t testValue) const {
    return passedCut(static_cast<double>(testValue));
  }

  bool DirectionalCut::passedCut(unsigned int testValue) const {
    return passedCut(static_cast<double>(testValue));
  }

  bool DirectionalCut::passedCut(double testValue) const {
    if (fCutDirection == kEQ)
      return TMath::Abs(testValue-fValue) < 0.0001;
    if (fCutDirection == kNEQ)
      return TMath::Abs(testValue-fValue) > 0.0001;
    if (fCutDirection == kGT)
      return (testValue > fValue);
    if (fCutDirection == kGEQ)
      return (testValue >= fValue);
    if (fCutDirection == kLT)
      return (testValue < fValue);
    if (fCutDirection == kLEQ)
      return (testValue <= fValue);
    return false; // never reached
  }
}
