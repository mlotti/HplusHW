#include "Tools/interface/DirectionalCut.h"

#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/Exception.h"
#include <iostream>

template<class T> 
DirectionalCut<T>::DirectionalCut(const ParameterSet& config, const std::string& name)
: fValue(config.getParameter<T>(name+std::string("Value"))) {
  // Check that direction option is valid
  std::string direction = config.getParameter<std::string>(name+std::string("Direction"));
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
    throw hplus::Exception("config") << "DirectionalCut: invalid cut direction (" << direction << ")! Options are: ==, !=, >, >=, <, <=";
  }
}

template<class T>
DirectionalCut<T>::~DirectionalCut() { }

template<class T>
bool DirectionalCut<T>::passedCut(const T testValue) const {
  if (fCutDirection == kEQ)
    return std::fabs(testValue-fValue) < 0.0001;
  if (fCutDirection == kNEQ)
    return std::fabs(testValue-fValue) > 0.0001;
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
