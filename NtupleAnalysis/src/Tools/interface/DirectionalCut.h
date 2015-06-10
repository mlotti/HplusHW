// -*- c++ -*-
#ifndef Tools_DirectionalCut_h
#define Tools_DirectionalCut_h

#include <string>
#include "Framework/interface/ParameterSet.h"
#include "Framework/interface/Exception.h"

/// Wrapper for more flexible cutting parameters (cut direction, value pair instead of cut value for fixed direction)
template <typename T>
class DirectionalCut {
  enum DirectionalCutType {
    kGT,  // greater than
    kGEQ, // greater than or equal to
    kLT,  // less than
    kLEQ, // less than or equal to
    kEQ,  // equal to
    kNEQ  // not equal to
  };
public:
  DirectionalCut(const ParameterSet& config, const std::string& name)
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
    else if (direction == "LEQ" || direction == "<=")
      fCutDirection = kLEQ;
    else {
      throw hplus::Exception("config") << "DirectionalCut: invalid cut direction (" << direction << ")! Options are: ==, !=, >, >=, <, <=";
    }
  }
  ~DirectionalCut() { }

  /// Check if cut has been passed
  bool passedCut(const T testValue) const {
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

private:
  T fValue;
  DirectionalCutType fCutDirection;
};

#endif
