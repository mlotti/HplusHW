// -*- c++ -*-
#ifndef Tools_DirectionalCut_h
#define Tools_DirectionalCut_h

#include <string>

class ParameterSet;

/// Wrapper for more flexible cutting parameters (cut direction, value pair instead of cut value for fixed direction)
template <class T>
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
  DirectionalCut(const ParameterSet& config, const std::string& name);
  ~DirectionalCut();

  /// Check if cut has been passed
  bool passedCut(const T testValue) const;

private:
  T fValue;
  DirectionalCutType fCutDirection;
};

#endif
